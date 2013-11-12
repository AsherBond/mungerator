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

"""This script will Create a known working CHEF environment for Openstack.

The environment JSON generated has been tailored for the cookbooks as provided
by Rackspace Private Cloud, RCBOPS, (https://github.com/rcbops). This will
set sane defaults though should be looked over and tailored to YOUR
environment.
"""

import ConfigParser
import json

from inspect import getmembers
from inspect import isfunction

import mungerator.arguments as arguments
import mungerator.methods.create_env as create_methods
import mungerator.methods.munger as mungerator_methods

from arguments import path_args as path_arguments


def execute():
    """Execute the Mungerator."""

    # Load all of the optional Arguments
    conf_parser, parser, subparser = arguments.setup_arg_parser()

    for path_arg in [parg for parg in getmembers(path_arguments, isfunction)]:
        name, function = path_arg
        _sub_arg = getattr(path_arguments, name)
        _sub_arg(subparser)

    # Get Default ARGS from file if used
    args, remaining_argv = conf_parser.parse_known_args()

    _args = vars(args)

    sysconfig = _args.get('config_file')

    if sysconfig is not None:
        config = ConfigParser.SafeConfigParser()
        config.read([sysconfig])
        default = dict(config.items("ChefOpenstack"))
        # If key is None, rip it out.
        for key, value in default.iteritems():
            if value.upper() == 'TRUE':
                default[key] = True
            elif value.upper() == 'FALSE':
                default[key] = False
            elif value.upper() == 'NONE':
                default[key] = None
            if key == 'nova_network' or key == 'neutron':
                default.pop(key)

        # Set the known defaults if file is used.
        parser.set_defaults(**default)

    # Parse the Arguments.
    parsed_args = vars(parser.parse_args(remaining_argv))

    # If key is None, rip it out.
    ready_args = dict([(key, value) for key, value in parsed_args.iteritems()
                      if value is not None])

    # Build our new Environment JSON
    if ready_args.get('create_env') is True:
        create_env(ready_args)
    elif ready_args.get('mungerator') is True:
        mungerator(ready_args)
    else:
        raise SystemExit(parser.print_help())


def mungerator(all_args):
    if all_args.get('environment'):
        mungerator_methods.environment(args=all_args)
    elif all_args.get('node'):
        mungerator_methods.node(args=all_args)
    elif all_args.get('all_nodes'):
        raise SystemExit('Not Implemented.')


def create_env(all_args):
    """Build the environment JSON.

    :param all_args: All parsed arguments in dict format.
    """

    # Get Base
    base_env = create_methods.base_dictionary()

    # Environment Name
    base_env["name"] = all_args['env_name'].replace(' ', '_')

    # Parse and set all Known Attributes.
    override = create_methods.set_override(base=base_env, args=all_args)

    # Load all of the subparsed positional Arguments
    for cmd in [arg for arg in getmembers(create_methods, isfunction)]:
        if not any([cmd[0] == 'base_dictionary', cmd[0] == 'set_override']):
            cmd[1](override, all_args)

    # Write out the network JSON to the current working Directory, or Print it
    if all_args['print_only'] is True:
        print(json.dumps(base_env, indent=4))
    else:
        file_name = '%s.json' % base_env["name"]
        with open(file_name, 'wb') as rcb_file:
            rcb_file.write(json.dumps(base_env, indent=2))
