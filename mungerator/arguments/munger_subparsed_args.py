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

import argparse

from mungerator import info


NAME_HELP_STR = 'Name of the chef environment all of your nodes belong too'
KERNEL_HELP_STR = ('Kernel Version of RHEL That is supported By RAX,'
                   ' Default: "%(default)s"')


def kernel_argument(help_info=None):
    kernel = argparse.ArgumentParser(add_help=False)
    kernel.add_argument('--kernel',
                        metavar='',
                        help=help_info,
                        default=info.__supported_rhel_kernel__)
    return kernel


def name_argument(help_info=None):
    name = argparse.ArgumentParser(add_help=False)
    name.add_argument('--name',
                      required=True,
                      metavar='',
                      help=help_info,
                      default='')
    return name


def disable_rhel_check_argument():
    rhel = argparse.ArgumentParser(add_help=False)
    rhel.add_argument('--no-rhel-scan',
                      metavar='',
                      help=('Disable post operation scan for RHEL based'
                            ' Servers.'),
                      default=False)
    return rhel


def name_argument(help_info=None):
    par = argparse.ArgumentParser(add_help=False)
    par.add_argument('--name',
                     required=True,
                     metavar='',
                     help=help_info,
                     default=None)
    return par


def env_args(subparser):
    name = name_argument(help_info=NAME_HELP_STR)
    disable = disable_rhel_check_argument()
    sub = subparser.add_parser(
        'environment',
        parents=[name,
                 disable],
        help='Munge an environment, and ONLY an environment'
    )
    sub.set_defaults(environment=True)


def node_args(subparser):
    name = name_argument(help_info='node name you want to Munge')
    sub = subparser.add_parser(
        'node',
        parents=[name],
        help='Munge an node, and ONLY a node'
    )
    sub.set_defaults(node=True)


def all_nodes_args(subparser):
    disable = disable_rhel_check_argument()
    name = name_argument(help_info=NAME_HELP_STR)
    kernel = kernel_argument(help_info=KERNEL_HELP_STR)
    sub = subparser.add_parser(
        'all-nodes-in-env',
        parents=[kernel, disable, name],
        help='Munge all nodes found in an environment.'
    )
    sub.set_defaults(all_nodes_in_env=True)


def quantum_detect_args(subparser):
    disable = disable_rhel_check_argument()
    name = name_argument(help_info=NAME_HELP_STR)
    sub = subparser.add_parser(
        'quantum-detect',
        parents=[name, disable],
        help='Check for Quantum arguments on nodes'
    )
    sub.set_defaults(quantum_detect=True)


def rhel_check_args(subparser):
    name = name_argument(help_info=NAME_HELP_STR)
    kernel = kernel_argument(help_info=KERNEL_HELP_STR)
    sub = subparser.add_parser(
        'rhel-check',
        parents=[name, kernel],
        help=('Check for RHEL servers and Report back if the Kernel Needs'
              ' Upgrading.')
    )
    sub.set_defaults(rhel_check=True)
