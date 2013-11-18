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


def backup_attributes(backup_dict, name):

    def write_backup(file_name):
        with open(file_name, 'wb') as backup:
            backup.write(
                json.dumps(
                    backup_dict, indent=2
                )
            )

    def backeruper(file_name, file_num=0):
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


def quantum_db_check(args, env_attrs):
    overrides = env_attrs.get('override_attributes')
    if overrides.get('osops'):
        osops = overrides['osops']
    else:
        osops = overrides['osops'] = {}

    if args.get('disable_pkg_upgrades') is True:
        osops['do_package_upgrades'] = False
    else:
        osops['do_package_upgrades'] = True

    if 'quantum' in overrides:
        new_neutron = overrides.get('quantum')
        if new_neutron is not None:
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
    exempt = ['name', 'database', 'db', 'username']

    def check_replace(rv):
        if 'quantum' in rv:
            return rv.replace("quantum", "neutron"), True
        else:
            return rv, False

    def replacer(replace_value, key=None):
        if key is not None:
            if key not in exempt:
                return check_replace(replace_value)
            else:
                return replace_value, False
        else:
            return check_replace(replace_value)

    def lister(list_value):
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
    chefserver = chef_api.Cheferizer(
        url=args.get('auth_url'),
        client_pem=args.get('client_key'),
        user=args.get('client_name')
    )
    chefserver.open_pem()
    if env_name is None:
        env_name = args.get('environment')
    env = chefserver.get_env(name=env_name)
    env_attrs = env.to_dict()
    backup_attributes(
        backup_dict=env_attrs,
        name='%s_Environment' % env_name
    )
    new_env = _super_munger(quantum_db_check(args, env_attrs))
    chefserver.put_env(old_env=env_name, new_env=new_env)


def node(args):
    chefserver = chef_api.Cheferizer(
        url=args.get('auth_url'),
        client_pem=args.get('client_key'),
        user=args.get('client_name')
    )
    chefserver.open_pem()
    node_name = args.get('node')
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


def all_node(args):
    environment(args, env_name=args.get('all_nodes_in_env'))

    chefserver = chef_api.Cheferizer(
        url=args.get('auth_url'),
        client_pem=args.get('client_key'),
        user=args.get('client_name')
    )
    chefserver.open_pem()
    nodes = chefserver.get_all_nodes(
        args.get('all_nodes_in_env')
    )
    all_nodes = [nd['name'] for nd in nodes if nd.get('name')]
    for nd in all_nodes:
        node_dict = chefserver.get_node(name=nd).to_dict()
        for attribute in ['normal', 'default', 'override']:
            attributes = node_dict.get(attribute).to_dict()
            backup_attributes(
                backup_dict=attributes,
                name='%s_%s_Attributes' % (nd, attribute)
            )
            node_dict[attribute] = _super_munger(attributes)

        chefserver.put_node(old_node=nd, new_node=node_dict)
