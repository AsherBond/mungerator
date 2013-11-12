Creates Openstack Chef Environment
##################################
:date: 2013-09-05 09:51
:tags: rackspace, chef, openstack, private cloud
:category: \*nix

Openstack Chef Environment file Generator
=========================================

General Overview
----------------

This is a simple utility designed to build an Openstack Chef environment, Munge Node Attributes and or Munge an existing Chef Environment.

The utilty will build a JSON file which you can upload to chef for use in your Openstack Deployments. The utility has been created such that it will, by default, setup sane values. While the values provided may be sane they are **NOT** production ready. You should read over the help information as provided in the script. Run ``environment_create.py -h`` for more information.

When using the utility may create a configuration file which will allow you to build your environment consistently with defaults per your requirements. See the provided **config.cfg** file for more information.

If you are Munging Attributes, this has only been built to upgrade an existing environment or Node Attributes which may use the value "Quantum" in it. In this case, if Quantum is found it is munged to "Neutron".

To Munge Attributes you need to have PyChef, presently I have no setup file and the utility is not installable, but if you go get pychef from `pip` you can run the utility from the `bin` directory.



License
^^^^^^^

Copyright [2013] [Kevin Carter]

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
