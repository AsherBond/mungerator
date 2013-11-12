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

import os

ENV = os.environ
HOME = ENV.get('HOME', '/root/')
CHEF_HOME = '%s/.chef' % HOME


def chef_args(par):
    """Chef Server."""
    chef = par.add_argument_group('Chef Server Configuration Group')
    chef.add_argument('--auth-url',
                      metavar='',
                      help='Chef Server URL, Default: "%(default)s"',
                      default='https://127.0.0.1')
    chef.add_argument('--client-key',
                      metavar='',
                      help='Default: "%(default)s"',
                      default=ENV.get('CHEF_SERVER_PEM',
                                      '%s/admin.pem' % CHEF_HOME))
    chef.add_argument('--validator-key',
                      metavar='',
                      help='Default: "%(default)s"',
                      default=ENV.get('CHEF_VALIDATOR_PEM',
                                      '%s/chef-validator.pem' % CHEF_HOME))
    chef.add_argument('--client-name',
                      metavar='',
                      help='CLient Name, Default: "%(default)s"',
                      default=ENV.get('CHEF_CLIENT_NAME', 'admin'))

    mecg = chef.add_mutually_exclusive_group(required=True)
    mecg.add_argument('--environment',
                      metavar='',
                      help='Name of the chef environment you want to Munge',
                      default=None)
    mecg.add_argument('--node',
                      metavar='',
                      help='Name of the chef node you want to Munge',
                      default=None)
    mecg.add_argument('--all-nodes-in-env',
                      metavar='',
                      help='Munge all of the nodes in an Environment',
                      default=None)
