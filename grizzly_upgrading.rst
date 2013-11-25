Upgrading from Grizzly to Havana
################################
:date: 2013-11-16
:tags: migrate, rackspace, openstack, upgrade
:category: \*nix


Upgrade notes
~~~~~~~~~~~~~

General:
  When upgrading you may want to purge all of the cached chef cookbooks from the system, this simply eliminates all of the possible issues with leftover and or unmodified cookbooks when chef-client begins compiling the cookbooks. ``for i in /var/chef/cache/cookbooks/*;do rm -rf $i; done``.

  Being that the system is about to go through a major set of package upgrades, this may be a good time to upgrade all of the distribution packages upgrades prior to performing the cookbook upgrade and subsequent chef client run.


Cookbook Upgrades:
  Go to the server where you have installed chef. If you have an existing copy of the rcbops chef-cookbooks repo then navigate to that location, otherwise get the repo. ``git clone -b "v4.2.0" https://github.com/rcbops/chef-cookbooks chef-cookbooks``.

  Once you have the cookbooks, you will need to setup the submodules and update them. In the chef-cookbooks directory run ``git submodule init && git submodule sync && git submodule update``.

  Once the submodule update is complete, upload all of the cookbooks then all of the roles. ``knife cookbook upload -a -o cookbooks/ && knife role from file roles/*.rb``.


Running the Mungerator:
  Here is how to get the Mungerator. ``git clone https://github.com/cloudnull/rcbops_mungerator mungerator``.

  Once you have the mungerator you can either install it or you can simply run it. No matter what you decide you will need to have *python-dev* installed. Here is how to get python-dev

  On RHEL run ``yum install python-devel``
  On Ubuntu run ``apt-get install python-dev``

  The Mungerator needs to run on the environment in order to ensure s/quantum/neutron/g. Example mungeration command:
  ``mungerator munger --client-key /etc/chef-server/admin.pem --auth-url https://127.0.0.1:4000 all-nodes-in-env --name allinoneinone``

  This can all be done on a per-node basis as well as run on a single environment without running on any nodes. Please see ``mungerator --help`` for more information.


Known Issues
~~~~~~~~~~~~


Ubuntu
^^^^^^

-> Notes
  Not required but I recommend it, clean all packages before running the upgrade. run ``apt-get clean``

-> Ceilometer
  Install python-warlock, python-novaclient, babel. run ``apt-get -y install python-warlock python-novaclient babel``. These packages seem to not be updated as deps in the new packages. This is likely a bug upstream with the packages.  Also we should look at including these packages in the cookbook as supplementary packages so that even if ubuntu does not fix the issue, we have our deployment covered.

-> Horizon
  Install openstack-dashboard python-django-horizon. run ``apt-get install openstack-dashboard python-django-horizon`` These packages also seem to not be updated when the stock openstack-dashboard is upgraded. This is also likely an issue with the upstream packages. we should add them to the cookbooks to cover our selves when a user is upgrading.

-> QEMU
  If you are running qemu, and installing package upgrades, you will have issues with the old package not upgrading because of dependency problems. To resolve this you can simple run the following. ``apt-get update && apt-get remove qemu-utils && apt-get install qemu-utils``.

-> Neutron
  Neutron has some supporting packages that will need to upgrade post chef run if they are not upgrading during the run. [python-cmd2, python-pyparsing]. While no adverse effects have been noted by not upgrading these packages you can resolve this issue with following. ``apt-get update && apt-get install python-cmd2 python-pyparsing``


RHEL
^^^^

-> Notes
  On upgrade the YOU MUST add the RDO havana repo prior to attempting the upgrade. This will remove the grizzly RDO repo information stored in "/etc/yum.repos.d/rdo-release.repo". ``sudo yum install -y http://rdo.fedorapeople.org/openstack-havana/rdo-release-havana.rpm``

  Once the repos are added, purge the old packages and headers from yum. ``yum clean headers && yum clean packages``.

  In order to upgrade to the Havana Cookbooks the you MUST install the new Havana RDO kernel. On CentOS6 / RHEL6 we will ONLY support kernel **kernel-2.6.32-358.123.2.openstack.el6.x86_64** as provided by redhat. The reason for this is not only due to requirements in neutron but also requirements in our present HA solution. ``yum install kernel``. If a new kernel is installed, Reboot the system before continuing.
