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


def nova_network_args(subparser):
    """Nova-Network."""
    n_n = subparser.add_parser(
        'nova-network',
        help='Create the environment JSON using Nova Network.'
    )
    n_n.set_defaults(nova_network=True)
    n_n.add_argument('--disable-multi-host',
                     help='Disable the use of Multi-Host',
                     action='store_false',
                     default=True)
    n_n.add_argument('--interface-bridge',
                     help=('Name of the Interface for the Network Bridge,'
                           ' Default: %(default)s'),
                     metavar='',
                     default='br0')
    n_n.add_argument('--ipv4-cidr',
                     help=('Network used by for Instance IPs,'
                           ' Default: %(default)s'),
                     metavar='',
                     default="172.16.0.0/16")
    n_n.add_argument('--network-size',
                     help='Size of the Network, Default: %(default)s',
                     metavar='',
                     default='255')
    n_n.add_argument('--label',
                     help='Label for the new instance network',
                     metavar='',
                     default='public')
    n_n.add_argument('--bridge-device',
                     help=('Device to create the network Bridge,'
                           ' Default: %(default)s'),
                     metavar='',
                     default='eth0')
    n_n.add_argument('--dns1',
                     help='Primary DNS Server, Default: %(default)s',
                     metavar='',
                     default='8.8.8.8')
    n_n.add_argument('--dns2',
                     help='Secondary DNS Server, Default: %(default)s',
                     metavar='',
                     default='8.8.4.4')
    n_n.add_argument('--num-networks',
                     help=('Number of Networks to create,'
                           ' Default: %(default)s'),
                     metavar='',
                     type=str,
                     default='1')


def neutron_args(subparser):
    """Neutron."""
    n_u = subparser.add_parser(
        'neutron',
        help='Create the environment JSON using Neutron.'
    )
    n_u.set_defaults(neutron=True)
    n_u.add_argument('--neutron_name',
                     help=('Name of the Neutron Provider,'
                           ' Default: %(default)s'),
                     metavar='',
                     default='neutron')
    n_u.add_argument('--net-type',
                     help='Type of Network to create, Default: %(default)s',
                     metavar='',
                     default='gre')
    n_u.add_argument('--interface-bridge',
                     help='Network Bridge Interface, Default: %(default)s',
                     metavar='',
                     default='br-eth0')
    n_u.add_argument('--vlans',
                     help='VLAN Setup, Default: %(default)s',
                     metavar='',
                     default='1:1000')
    n_u.add_argument('--label',
                     help='Network Bridge Label, Default: %(default)s',
                     metavar='',
                     default='ph-eth0')
