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

import inspect

from mungerator.arguments import create_optional_args as create_opt_args
from mungerator.arguments import create_subparsed_args as create_sub_args
from mungerator.arguments import mungerator_args as upgrade_sub_args


def create(subparser):
    """Nova-Network."""
    sub = subparser.add_parser('create-env',
                               help='Create the environment JSON')
    sub.set_defaults(create_env=True)

    # Load all of the options args
    functions = inspect.getmembers(create_opt_args, inspect.isfunction)
    for opt_arg in [oarg for oarg in functions]:
        name, function = opt_arg
        function(sub)

    # Load all of the subparsed positional Arguments
    _subparser = sub.add_subparsers(title='Positional Arguments',
                                    metavar='Type of Network to Create')
    functions = inspect.getmembers(create_sub_args, inspect.isfunction)
    for sub_arg in [sarg for sarg in functions]:
        name, function = sub_arg
        function(_subparser)


def mungerator(subparser):
    """Upgrade an Existing Environment."""
    sub = subparser.add_parser(
        'mungerator',
        help='Run the mungerator on a chef target(s)'
    )
    sub.set_defaults(mungerator=True)

    # Load all of the options args
    functions = inspect.getmembers(upgrade_sub_args, inspect.isfunction)
    for up_arg in [uarg for uarg in functions]:
        name, function = up_arg
        function(sub)
