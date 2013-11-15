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


def default_args(par):
    """Setup for general Arguments."""

    par.add_argument('--disable-pkg-upgrades',
                     help='In The Environment Disable Package Upgrades',
                     action='store_false',
                     default=True)

    par.add_argument('--print-only',
                     help='Print the output json, NOT Write the File',
                     action='store_true',
                     default=False)
    par.add_argument('--developer-mode',
                     help='Enable Developer Mode',
                     action='store_true',
                     default=False)
    par.add_argument('--apply-patches',
                     help='Apply Patches that RCBOPS may Recommend.',
                     action='store_true',
                     default=False)
    par.add_argument('-n',
                     '--env-name',
                     metavar='',
                     help='Environment Name',
                     default='RCBOPS Openstack Environment')


def network_args(par):
    """OS Networks."""
    net = par.add_argument_group('OS Networks Configuration Group')
    net.add_argument('-mn',
                     '--management-net',
                     metavar='',
                     help='Management Net for Openstack, Default: %(default)s',
                     default='127.0.0.0/24')
    net.add_argument('-pn',
                     '--public-net',
                     metavar='',
                     help='Public Net used by Openstack, Default: %(default)s',
                     default='127.0.0.0/24')
    net.add_argument('-nn',
                     '--nova-net',
                     metavar='',
                     help='Nova Net used by Openstack, Default: %(default)s',
                     default='127.0.0.0/24')
    net.add_argument('-sn',
                     '--swift-net',
                     metavar='',
                     help='Swift Net used by Openstack, Default: %(default)s',
                     default='127.0.0.0/24')
    net.add_argument('--vips',
                     metavar='',
                     help=('Vips for HA ENV, uses a comma seperated list with'
                           ' a value Format: ServiceName=Address'),
                     default=None)
    net.add_argument('--vips-config',
                     metavar='',
                     help=('OPTIONAL, Network Config for vips used in HA'
                           ' uses a comma seperated list with a value Format:'
                           ' Address=Vird=Network'),
                     default=None)


def rabbit_args(par):
    """RabbitMQ."""
    Rabbitmq = par.add_argument_group('RabbitMQ Configuration Group')
    Rabbitmq.add_argument('--disable-cluster',
                          help='Disable PKI Tokens',
                          action='store_false',
                          default=True)
    Rabbitmq.add_argument('-ec',
                          '--erlang-cookie',
                          metavar='',
                          help='Erlang cookie used by RabbitMQ',
                          default='AnyLongAndRandomStringWillDo')


def keystone_args(par):
    """Keystone."""
    key = par.add_argument_group('Keystone Configuration Group')
    key.add_argument('--disable-pki',
                     help='Disable PKI Tokens',
                     action='store_false',
                     default=True)
    key.add_argument('-U',
                     '--admin-username',
                     metavar='',
                     help='Admin User Name, Default: %(default)s',
                     default='admin')
    key.add_argument('-P',
                     '--admin-password',
                     metavar='',
                     help='Admin Users Password',
                     default='secrete')
    key.add_argument('-R',
                     '--admin-roles',
                     metavar='',
                     help=('Admin Roles, Pipe Separated. Format:'
                           ' Role1|Role2|Role3'),
                     type=str,
                     default='admin')
    key.add_argument('--add-users',
                     metavar='',
                     help=('Add additional users to Keystone, Comma Seperated'
                           ' list. Format: Username=Password=Role1|Role2'),
                     type=str,
                     default=None)


def monitoring_args(par):
    """Monitoring."""
    mon = par.add_argument_group('Monitoring Configuration Group')
    mon.add_argument('--disable-monit',
                     help='Disable Monit Monitoring',
                     action='store_false',
                     default=True)
    mon.add_argument('--disable-procmon',
                     help='Disable Monit Monitoring',
                     action='store_true',
                     default=False)
    mon.add_argument('--disable-metrics',
                     help='Disable Monit Metrics Monitoring',
                     action='store_true',
                     default=False)
    mon.add_argument('--other-mon',
                     help='Set other monitoring bits, This is Comma Seperated'
                          ' list. The Format is: Service=Cookbook',
                     type=str,
                     default=None)


def glance_args(par):
    """Glance."""
    gal = par.add_argument_group('Glance Configuration Group')
    gal.add_argument('--image-upload',
                     help='Disable Image Upload to Glance',
                     action='store_false',
                     default=False)
    gal.add_argument('--custom-image',
                     metavar='',
                     help=('Add Custom images to Glance,  Comma Seperated'
                           ' list, The Format is: Name=URL'),
                     type=str,
                     default=None)
    gal.add_argument('--fedora-image',
                     metavar='',
                     help='URL to Ubuntu Image, default: URL is SET',
                     default=False)
    gal.add_argument('--cirros-image',
                     metavar='',
                     help='URL to Cirros Image, default: URL is SET',
                     default=False)
    gal.add_argument('--ubuntu-image',
                     metavar='',
                     help='URL to Ubuntu Image, default: URL is SET',
                     default=False)
    gal.add_argument('--default-store',
                     metavar="['file', 'swift', 'rbd']",
                     choices=['file', 'swift', 'rbd'],
                     help='Storage Provider, Default: %(default)s',
                     default='file')
    gal.add_argument('--swift-key',
                     metavar='',
                     help='Key for access to swift',
                     default="secrete")
    gal.add_argument('--swift-user',
                     metavar='',
                     help='Username for access to swift',
                     default="admin")
    gal.add_argument('--swift-auth-address',
                     metavar='',
                     help='URL/IP address for access to swift',
                     default="127.0.0.1")
    gal.add_argument('--swift-auth-version',
                     metavar='',
                     help='Version of swift to interface with',
                     default="2")
    gal.add_argument('--swift-region',
                     metavar='',
                     help=('Region for Swift storage, only required if you'
                           ' have multiple regions.'),
                     default=None)
    gal.add_argument('--rbd-ceph-conf',
                     metavar='',
                     help='Location of the ceph configuration file',
                     default="/etc/ceph/ceph.conf")
    gal.add_argument('--rbd-user',
                     metavar='',
                     help='Username for access to glance',
                     default="glance")
    gal.add_argument('--rbd-pool',
                     metavar='',
                     help='Name of storage pool',
                     default="images")
    gal.add_argument('--rbd-chunk-size',
                     metavar='',
                     help='Max Number of Chunks',
                     default="8")


def database_args(par):
    """MySQL."""
    sql = par.add_argument_group('MySQL Configuration Group')
    sql.add_argument('--mysql-network-acl',
                     metavar='',
                     help='Access ACL used by MySQL, Default: %(default)s',
                     default='%')
    sql.add_argument('--mysql-root-access',
                     help='Disable MySQL Root Access',
                     action='store_false',
                     default=True)
    sql.add_argument('--enable-indexed-log',
                     help='Enable MySQL Log for Queries without an Index',
                     action='store_true',
                     default=False)


def nova_args(par):
    """Nova."""
    nov = par.add_argument_group('NOVA Configuration Group')
    nov.add_argument('--disk-ratio',
                     metavar='',
                     help='Disk Allocation, Default: %(default)s',
                     type=float,
                     default=1.0)
    nov.add_argument('--ram-ratio',
                     metavar='',
                     help='RAM Allocation, Default: %(default)s',
                     type=float,
                     default=1.0)
    nov.add_argument('--cpu-ratio',
                     metavar='',
                     help='Disk Allocation, Default: %(default)s',
                     type=float,
                     default=2.0)
    nov.add_argument('--host-instance-boot',
                     help='Start Instances on Host Boot, Default: %(default)s',
                     action='store_true',
                     default=False)
    nov.add_argument('--use-single-gw',
                     help='Use Single Default Gateway, Default: %(default)s',
                     action='store_true',
                     default=False)
    nov.add_argument('--enable-limits',
                     help='Enable Rate limiting, Default: %(default)s',
                     action='store_true',
                     default=False)
    nov.add_argument('--generic-post',
                     metavar='',
                     help='Number of POST\'s per Minute, Default: %(default)s',
                     type=str,
                     default='1000')
    nov.add_argument('--generic-delete',
                     metavar='',
                     help=('Number of DELETE\'s per Minute, Default:'
                           ' %(default)s'),
                     type=str,
                     default='1000')
    nov.add_argument('--generic-put',
                     metavar='',
                     help='Number of PUT\'s per Minute, Default: %(default)s',
                     type=str,
                     default='1000')
    nov.add_argument('--creates-post',
                     metavar='',
                     help=('Number of create POST\'s per Day, Default:'
                           ' %(default)s'),
                     type=str,
                     default='1000')
    nov.add_argument('--changes-get',
                     metavar='',
                     help='Number of Changes per Minute, Default: %(default)s',
                     type=str,
                     default='1000')
    nov.add_argument('--scheduler-filters',
                     metavar='',
                     help='Comma Seperated list, Default: %(default)s',
                     default=('AvailabilityZoneFilter,ComputeFilter,'
                              'RetryFilter'))


def libvirt_args(par):
    """Libvirt."""
    vir = par.add_argument_group('Libvirt Configuration Group')
    vir.add_argument('--vnc-listen-addr',
                     metavar='',
                     help=('Address VNC Server will listen on,'
                           ' Default: %(default)s'),
                     default='0.0.0.0')
    vir.add_argument('-v',
                     '--virt-type',
                     metavar='',
                     help=('Virtualization Type used by Openstack,'
                           ' Default: %(default)s'),
                     default='qemu')
