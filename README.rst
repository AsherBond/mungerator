Munge Openstack Chef Things
###########################
:date: 2013-09-05 09:51
:tags: rackspace, chef, openstack, private cloud
:category: \*nix

Openstack Chef Munger
=====================

General Overview
----------------

This is a simple utility designed to create an Openstack Chef environment, Munge Node Attributes and or Munge an existing Chef Environment.

When using the utility may create a configuration file which will allow you to build your environment consistently with defaults per your requirements. See the provided **config.cfg** file for more information.

The Application has two main purposes:
  1. Build a **JSON** file which you can upload to chef for use in your Openstack Deployments. The utility has been created such that it will, by default, setup sane values. While the values provided may be sane they are **NOT** production ready. You should read over the help information as provided in the script.

  2. **Munge** Attributes for an existing environment, Node, or groups of nodes. The Mungerator function has been built to upgrade  Attributes. You may need or want to "upgrade" attributes if you have an environment using "Quantum" and not "Neutron". In this case, if Quantum is found it is munged to "Neutron".

  * To use this application you can run the local file from the ``bin`` directory, provided you have ``pychef`` installed. If you want to install this application you can, simply run the ``setup.py`` file as such ``python setup.py install``.

Run ``bin/mungerator.local.py -h`` for more information.


Installation:
  To run the applcation you will need to have ``python-dev``. You do not need to install the application to run the application. Once you have pychef and python-dev install you can go to the bin directory and run the munger.
  If you would like to install the application, install the package ``python-dev`` and ``python-setuptools`` then from the mungerator directory run ``python setup.py install``.


License
^^^^^^^

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
