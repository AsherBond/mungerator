# Copyright 2012, Rackspace US, Inc.
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


def base_dictionary():
    """Return Base JSON environment."""
    return {"chef_type": "environment",
            "default_attributes": {},
            "cookbook_versions": {},
            "override_attributes": {},
            "json_class": "Chef::Environment",
            "description": "Environment for Openstack Private Cloud"}


def set_override(base, args):
    """Set the Default Override Attribute."""
    ovr = base['override_attributes']
    ovr['developer_mode'] = args.get('developer_mode')
    osops = ovr['osops'] = {}
    osops['apply_patches'] = args.get('apply_patches')
    osops['do_package_upgrades'] = args.get('do_package_upgrades')
    return ovr


def mysql_attrs(ovr, args):
    """Set MySQL Attributes."""
    mysql = ovr['mysql'] = {}
    mysql['root_network_acl'] = args.get('mysql_network_acl')
    mysql['allow_remote_root'] = args.get('mysql_root_access')
    tune = mysql['tunable'] = {}
    tune['log_queries_not_using_index'] = args.get('enable_indexed_log')


def monit_attrs(ovr, args):
    """Set Monitoring Attributes."""
    ovr['enable_monit'] = args.get('disable_monit')

    if any([args.get('disable_procmon') is False,
            args.get('disable_metrics') is False,
            args.get('other-mon') is not None]):

        monit = ovr['monitoring'] = {}

        if args.get('disable_procmon') is False:
            monit['procmon_provider'] = 'monit'
        if args.get('disable_metrics') is False:
            monit['metric_provider'] = 'collectd'
        if args.get('other_mon') is not None:
            for mon in args.get('other_mon').split(','):
                srv, cook = mon.split('=')
                monit[srv] = cook


def osnet_attrs(ovr, args):
    """Set OS Networks Attributes."""
    osnet = ovr['osops_networks'] = {}
    osnet['management'] = args.get('management_net')
    osnet['public'] = args.get('public_net')
    osnet['nova'] = args.get('nova_net')
    osnet['swift'] = args.get('swift_net')


def rabbitmq_attrs(ovr, args):
    """Set RabbitMQ Attributes."""
    rabbitmq = ovr['rabbitmq'] = {}
    rabbitmq['cluster'] = args.get('disable_cluster')
    rabbitmq['erlang_cookie'] = args.get('erlang_cookie')


def keystone_attrs(ovr, args):
    """Set Keystone Attributes."""

    keystone = ovr['keystone'] = {}
    admin_user = keystone['admin_user'] = args.get('admin_username')

    pki = keystone['pki'] = {}
    pki['enabled'] = args.get('pki')

    tenants = keystone['tenants'] = []
    tenants.append('service')
    tenants.append(admin_user)

    users = keystone['users'] = {}
    uname = users[admin_user] = {}
    uname['password'] = args.get('admin_password')

    role = uname['role'] = {}
    role['admin'] = [_role for _role in args.get('admin_roles').split('|')]
    role['admin'].append(admin_user)
    role['admin'] = list(set(role['admin']))

    if args.get('add_users'):
        for usr in args.get('add_users').split(','):
            name, password, role = usr.split('=')
            tenants.append(name)

            uname = users[name] = {}
            uname['password'] = password
            uname['default_tenant'] = name

            roles = uname['role'] = {}
            roles['Member'] = [_role for _role in role.split('|')]
            roles['Member'].append(name)
            roles['Member'] = list(set(roles['Member']))


def nova_attrs(ovr, args):
    """Set Nova Attributes."""

    def use_neutron(ovr):
        """Set Neutron Attributes if used."""

        network_name = ovr[args.get('neutron_name')] = {}
        ovs = network_name['ovs'] = {}
        ovs['network_type'] = args.get('net_type')
        ovs['provider_networks'] = []
        pnet = provider_net = {}
        pnet['bridge'] = args.get('interface_bridge')
        pnet['vlans'] = args.get('vlans')
        pnet['label'] = args.get('label')
        ovs['provider_networks'].append(provider_net)

    def create_limit_base(ldict, limit, verb, uri, interval, regex):
        """Built dict of limits."""
        ldict['limit'] = limit
        ldict['verb'] = verb
        ldict['uri'] = uri
        ldict['interval'] = interval
        ldict['regex'] = regex

    nova = ovr['nova'] = {}

    # if rate limiting was set Configure it.
    if args.get('enable_limits') is True:
        rate_limit = nova["ratelimit"] = {}
        api = rate_limit["api"] = {}
        api["enabled"] = True
        settings = rate_limit['settings'] = {}
        changes = settings['changes-since-limit'] = {}
        create_limit_base(
            changes,
            '50000',
            'GET',
            '*changes-since*',
            'MINUTE',
            '.*changes-since.*'
        )
        create = settings['create-servers-limit'] = {}
        create_limit_base(
            create, '50000', 'POST', '*/server', 'DAY', '^/servers'
        )
        generic_post = settings['generic-post-limit'] = {}
        create_limit_base(
            generic_post, '50000', 'POST', '*', 'MINUTE', '.*'
        )
        generic_delete = settings['generic-delete-limit'] = {}
        create_limit_base(
            generic_delete, '50000', 'DELETE', '*', 'MINUTE', '.*'
        )
        generic_put = settings['generic-put-limit'] = {}
        create_limit_base(
            generic_put, '50000', 'PUT', '*', 'MINUTE', '.*'
        )

    config = nova['config'] = {}
    config['disk_allocation_ratio'] = args.get('disk_ratio')
    config['resume_guests_state_on_host_boot'] = args.get('host_instance_boot')
    config['use_single_default_gateway'] = args.get('use_single_gw')
    config['ram_allocation_ratio'] = args.get('ram_ratio')
    config['cpu_allocation_ratio'] = args.get('cpu_ratio')
    scheduler = nova['scheduler'] = {}
    scheduler['default_filters'] = args.get('scheduler_filters', '').split(',')
    libvirt = nova['libvirt'] = {}
    libvirt['virt_type'] = args.get('virt_type')
    libvirt['vncserver_listen'] = args.get('vnc_listen_addr')
    network = nova['network'] = {}

    # In Nova Network is used, Else Set for Neutron
    if args.get('nova_network') is True:
        network['multi_host'] = args.get('disable_multi_host')
        network['public_interface'] = args.get('interface_bridge')
        net = nova['networks'] = {}
        public = net[args.get('label')] = {}
        public['bridge'] = args.get('interface_bridge')
        public['num_networks'] = args.get('num_networks')
        public['dns1'] = args.get('dns1')
        public['dns2'] = args.get('dns2')
        public['ipv4_cidr'] = args.get('ipv4_cidr')
        public['network_size'] = args.get('network_size')
        public['label'] = args.get('label')
        public['bridge_dev'] = args.get('bridge_device')
    else:
        network['provider'] = args.get('neutron_name')
        use_neutron(ovr)


def glance_attrs(ovr, args):
    """Set Glance Attributes."""

    cirros_img_url = ('https://launchpad.net/cirros/trunk/0.3.0/+download/'
                      'cirros-0.3.0-x86_64-disk.img')

    ubuntu_img_url = ('http://cloud-images.ubuntu.com/precise/current/'
                      'precise-server-cloudimg-amd64-disk1.img')

    fedora_img_url = ('http://download.fedoraproject.org/pub/fedora/linux/'
                      'releases/19/Images/x86_64/'
                      'Fedora-x86_64-19-20130627-sda.qcow2')

    glance = ovr['glance'] = {}
    image = glance['image'] = {}
    images = glance['images'] = []

    if args.get('cirros_image') is True:
        images.append('cirros')
        image['Cirros'] = cirros_img_url

    if args.get('ubuntu_image') is True:
        images.append('precise')
        image['Precise'] = ubuntu_img_url

    if args.get('fedora_image') is True:
        images.append('SchrodingersCat')
        image['SchrodingersCat'] = fedora_img_url

    if args.get('custom_image'):
        for img in args.get('custom_image_name').split(','):
            name, url = img.split('=')
            images.append(name)
            image[name] = url

    glance['image_upload'] = args.get('image_upload')

    if args.get('default_store') is not 'file':
        api = glance['api'] = {}
        api['default_store'] = args.get('default_store')
        if api['default_store'] == 'swift':
            api['swift_store_key'] = args.get('swift_key')
            api['swift_store_user'] = args.get('swift_user')
            api['swift_store_auth_address'] = args.get('swift_auth_address')
            api['swift_store_auth_version'] = args.get('swift_auth_version')
            if args.get('swift_region') is not None:
                api['store_region'] = args.get('swift_region')
        elif api['default_store'] == 'rbd':
            api['rbd_store_ceph_conf'] = args.get('')
            api['rbd_store_user'] = args.get('')
            api['rbd_store_pool'] = args.get('')
            api['rbd_store_chunk_size'] = args.get('')


def vip_attrs(ovr, args):
    """Set VIP attributes."""

    if args.get('vips'):
        addresses = []
        vips = ovr['vips'] = {}
        for img in args.get('vips').split(','):
            name, address = img.split('=')
            vips[name] = address
            addresses.append(address)

        base_vrid = 9
        config = vips['config'] = {}
        for address in sorted(set(addresses)):
            net_data = config[address] = {}
            if args.get('vips_config'):
                for vc in args.get('vips_config').split(','):
                    vip_address, vird, network = vc.split('=')
                    if vip_address in addresses:
                        net_data['network'] = network
                        net_data['vird'] = vird
                        break
                else:
                    base_vrid += 1
                    net_data['network'] = 'public'
                    net_data['vird'] = base_vrid
            else:
                base_vrid += 1
                net_data['network'] = 'public'
                net_data['vird'] = base_vrid
