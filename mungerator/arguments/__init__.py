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

try:
    import argparse
except ImportError:
    raise SystemExit('Python module "argparse" not Found for import.')


def setup_arg_parser():
    """Setup Argument Parser."""

    conf_parser = argparse.ArgumentParser(add_help=False)
    conf_parser.add_argument('-C',
                             '--config-file',
                             metavar='',
                             type=str,
                             default=None,
                             help=('Path to a Configuration file. This is'
                                   ' an optional argument used to specify'
                                   ' Anything you may want in your'
                                   ' environment. The file is in INI format'
                                   ' and requires the key "[ChefOpenstack]".'))

    args = argparse.ArgumentParser(
        parents=[conf_parser],
        usage='%(prog)s',
        formatter_class=lambda prog: argparse.HelpFormatter(
            prog,
            max_help_position=28
        ),
        description=('%(prog)s will create a basic Environment file for your'
                     ' RCBOPS Openstack Deployment.'),
        epilog='Apache2 Licensed Chef Openstack Environment Creator.')

    subparser = args.add_subparsers(title='Positional Arguments', metavar='')

    return conf_parser, args, subparser
