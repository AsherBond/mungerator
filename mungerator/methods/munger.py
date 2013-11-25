# Copyright [2013] [Kevin Carter]
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import os
import tempfile

from mungerator.methods import chef_api


def _notice(message):
    """Return a formatted string with information."""

    line = ''.join(['=' for _ in range(len(message))])
    return '%s\n%s\n%s' % (line, message, line)


def open_chef_connection(args):
    """Create a connection to chef server and terturn the connection."""

    chefserver = chef_api.Cheferizer(
        url=args.get('auth_url'),
        client_pem=args.get('client_key'),
        user=args.get('client_name')
    )
    chefserver.open_pem()
    return chefserver


def backup_attributes(backup_dict, name):
    """Save chef attributes prior to starting the run."""

    def write_backup(file_name):
        """Write attributes to a file."""

        with open(file_name, 'wb') as backup:
            backup.write(
                json.dumps(
                    backup_dict, indent=2
                )
            )

    def backeruper(file_name, file_num=0):
        """Ensure that we never overwrite an existing backup."""

        if not os.path.exists('%s.json' % file_name):
            write_backup('%s.json' % file_name)
        elif not os.path.exists('%s.%s.json' % (file_name, file_num)):
            write_backup('%s.%s.json' % (file_name, file_num))
        else:
            file_num += 1
            backeruper(file_name, file_num)

    home = os.getenv('HOME', tempfile.gettempdir())
    backup_dir = '%s%s%s' % (home, os.sep, 'mungerator_backup')
    backup_name = '%s%s%s' % (backup_dir, os.sep, name)

    print('Backup made for %s at %s' % (name, backup_name))

    if not os.path.exists(backup_dir):
        os.mkdir(backup_dir)

    backeruper(backup_name)


def _package_upgrades(args, env_attrs):
    """Set whether package Upgrades are done."""

    overrides = env_attrs.get('override_attributes')
    if overrides.get('osops'):
        osops = overrides['osops']
    else:
        osops = overrides['osops'] = {}

    if args.get('disable_pkg_upgrades') is True:
        osops['do_package_upgrades'] = False
    else:
        osops['do_package_upgrades'] = True
    return env_attrs


def quantum_name_check(args, env_attrs):
    """Check all attributes for the quantum name if its found."""

    overrides = env_attrs.get('override_attributes')
    if 'quantum' in overrides:
        new_neutron = overrides.get('quantum')
        if new_neutron is not None:
            # Check for the service user in the environment
            if new_neutron.get('service_user') is None:
                new_neutron['service_user'] = args.get('service_user')

            # Check the database setting for Quantum
            database = new_neutron.get('db')
            if database is not None:
                if 'name' not in database:
                    database['name'] = args.get('db_name')
                if 'username' not in database:
                    database['username'] = args.get('db_username')
            else:
                db = new_neutron['db'] = {}
                db['name'] = args.get('db_name')
                db['username'] = args.get('db_username')
    return env_attrs


def _super_munger(mungie):
    """Munge all attributes except the ones in the except list."""

    exempt = ['name', 'database', 'db', 'username', 'service_user']

    def check_replace(rv):
        """If quantum is found replace it."""

        if 'quantum' in rv:
            return rv.replace("quantum", "neutron"), True
        else:
            return rv, False

    def replacer(replace_value, key=None):
        """Run the replace operation."""

        if key is not None:
            if key not in exempt:
                return check_replace(replace_value)
            else:
                return replace_value, False
        else:
            return check_replace(replace_value)

    def lister(list_value):
        """If the returned value is a list examine the contents and route."""

        for item in list_value:
            if isinstance(item, basestring):
                index = list_value.index(item)
                rep, fact = replacer(replace_value=item)
                if fact is True:
                    list_value[index] = rep

            elif isinstance(item, list):
                lister(list_value=item)

            elif isinstance(item, dict):
                _super_munger(mungie=item)

    for key, value in mungie.items():
        new_key, discard_fact = replacer(key)
        if discard_fact is True:
            mungie[str(new_key)] = value
            del mungie[key]

        if isinstance(value, basestring):
            rep, fact = replacer(replace_value=value, key=new_key)
            mungie[new_key] = rep

        elif isinstance(mungie[new_key], dict):
            _super_munger(mungie=value)

        elif isinstance(mungie[new_key], list):
            lister(list_value=value)

    return mungie


def environment(args, env_name=None):
    """Backup and then Munge all of the environment values."""

    chefserver = open_chef_connection(args)
    if env_name is None:
        env_name = args.get('name')
    env = chefserver.get_env(name=env_name)
    env_attrs = env.to_dict()
    backup_attributes(
        backup_dict=env_attrs,
        name='%s_Environment' % env_name
    )
    new_env = _package_upgrades(
        args=args, env_attrs=_super_munger(
            quantum_name_check(
                args, env_attrs
            )
        )
    )

    chefserver.put_env(old_env=env_name, new_env=new_env)


def node(args):
    """Backup and then Munge all of the node values."""

    chefserver = open_chef_connection(args)
    node_name = args.get('name')
    node = chefserver.get_node(name=node_name)
    node_dict = node.to_dict()
    for attribute in ['normal', 'default', 'override']:
        attrs = node_dict.get(attribute).to_dict()
        backup_attributes(
            backup_dict=attrs,
            name='%s_%s_Attributes' % (node_name, attribute)
        )
        node_dict[attribute] = _super_munger(attrs)

    chefserver.put_node(old_node=node_name, new_node=node_dict)


def sanitize_run_list(run_list):
    if 'role[rpc-support]' in run_list:
        run_list.pop(run_list.index('role[rpc-support]'))
    return run_list


def all_nodes_in_env(args):
    """Backup and then Munge all nodes in an environment."""

    environment(args, env_name=args.get('name'))

    chefserver = open_chef_connection(args)
    nodes = chefserver.get_all_nodes(
        args.get('name')
    )
    all_nodes = [nd['name'] for nd in nodes if nd.get('name')]
    for nd in all_nodes:
        node = chefserver.get_node(name=nd)
        node_dict = node.to_dict()

        # Check the run_list on the node
        run_list = node_dict.get('run_list')
        if run_list is not None:
            node_dict['run_list'] = sanitize_run_list(run_list)

        for attribute in ['normal', 'default', 'override']:
            attributes = node_dict.get(attribute).to_dict()

            backup_attributes(
                backup_dict=attributes,
                name='%s_%s_Attributes' % (nd, attribute)
            )
            node_dict[attribute] = _super_munger(attributes)

        chefserver.put_node(old_node=nd, new_node=node_dict)

    if args.get('disable_rhel_check') is False:
        rhel_check(args, servers=nodes)


def rhel_check(args, servers=None):
    """Search for RHEL servers registered with chef."""

    upgrade_me = {}
    supported_kernel = args.get('kernel')

    if servers is None:
        chefserver = open_chef_connection(args)
        servers = chefserver.rhel_search(env_name=args.get('name'))
    for node in servers:
        name = node['name']
        auto = node.get('automatic')
        if auto:
            kernel = auto.get('kernel')
            if kernel:
                version = kernel.get('release')
            else:
                raise SystemExit(
                    'Not able to retrieve the Kernel Version from Node %s'
                    % node
                )
        else:
            raise SystemExit(
                'Not able to retrieve the Kernel Version from Node %s'
                % node
            )

        if supported_kernel != version:
            upgrade_me[name] = version

    if upgrade_me:
        msg = ('Nodes that likely need the Kernel Upgraded, RAX Supports "%s"'
               % supported_kernel)
        print(_notice(message=msg))
        for key, value in upgrade_me.iteritems():
            notice = 'Node: %s|Current Kernel: %s' % (key, value)
            print(notice.replace('|', '\t| '))


def quantum_detect(args):
    """Look for quantum values in everything."""

    chefserver = open_chef_connection(args)
    nodes = chefserver.get_all_nodes(
        args.get('name')
    )

    all_nodes = [nd['name'] for nd in nodes if nd.get('name')]
    detected = []

    for node_name in all_nodes:
        node = chefserver.get_node(name=node_name)
        quantum = node.get('quantum')
        if quantum is not None:
            db = quantum.get('db')
            if db is not None:
                detected.append(
                    {'node': node_name,
                     'service_user': quantum.get('service_user', 'UNKNOWN'),
                     'db_name': db.get('name', 'UNKNOWN'),
                     'username': db.get('usesr', 'UNKNOWN'),
                     'password': db.get('password', 'UNKNOWN')}
                )
    if detected:
        print(_notice(message='QUANTUM FOUND IN THE ENVIRONMENT'))
        for item in detected:
            notice = ('Node: %(node)s|DB Name: %(db_name)s|'
                      ' Service User: %(service_user)s|'
                      ' Username: %(username)s|Password: %(password)s' % item)
            print(notice.replace('|', '\t| '))
