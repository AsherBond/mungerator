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

import os


def chef_args(par):
    """Chef Server."""

    ENV = os.environ
    HOME = ENV.get('HOME', '/root/')
    CHEF_HOME = '%s/.chef' % HOME

    chef = par.add_argument_group('Chef Server Configuration Group')
    chef.add_argument('--auth-url',
                      metavar='',
                      help='Chef Server URL, Default: "%(default)s"',
                      default=ENV.get('CHEF_SERVER_URL',
                                      'https://127.0.0.1'))
    chef.add_argument('--client-key',
                      metavar='',
                      help='Default: "%(default)s"',
                      default=ENV.get('CHEF_SERVER_PEM',
                                      '%s/admin.pem' % CHEF_HOME))
    chef.add_argument('--client-name',
                      metavar='',
                      help='CLient Name, Default: "%(default)s"',
                      default=ENV.get('CHEF_CLIENT_NAME', 'admin'))
    chef.add_argument('--db-name',
                      metavar='',
                      help=('Name for the Neutron Database,'
                            ' Default: "%(default)s"'),
                      default='quantum')
    chef.add_argument('--db-username',
                      metavar='',
                      help=('Username for the Neutron Database,'
                            ' Default: "%(default)s"'),
                      default='quantum')
    chef.add_argument('--service-user',
                      metavar='',
                      help=('Username for the Openstack Service that controls'
                            ' Neutron, Default: "%(default)s"'),
                      default='quantum')
    chef.add_argument('--disable-pkg-upgrades',
                      help='In The Environment Disable Package Upgrades',
                      action='store_true',
                      default=False)
