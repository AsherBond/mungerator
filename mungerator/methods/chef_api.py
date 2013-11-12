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

import chef


class Cheferizer(object):

    def __init__(self, url, client_pem, user):
        self.url = url
        self.location_client_pem = client_pem
        self.user = user
        self.open_client_pem = None

    def open_pem(self):
        if os.path.exists(self.location_client_pem):
            with open(self.location_client_pem, 'rb') as cp:
                self.open_client_pem = cp.read()
        else:
            raise SystemExit(
                'Your Client PEM was not found at %s'
                % self.location_client_pem
            )

    def get_env(self, name):
        with chef.ChefAPI(self.url, self.open_client_pem, self.user):
            return chef.Environment(name)

    def get_node(self, name):
        with chef.ChefAPI(self.url, self.open_client_pem, self.user):
            return chef.Node(name)

    def get_all_nodes(self, name):
        with chef.ChefAPI(self.url, self.open_client_pem, self.user):
            return chef.Search('node', q='chef_environment:%s' % name)

    def put_env(self, old_env, new_env):
        with chef.ChefAPI(self.url, self.open_client_pem, self.user):
            get_old_envs = chef.Environment(old_env).list()
            if old_env in get_old_envs.iterkeys():
                chef.Environment(old_env).delete()
            env = chef.Environment(old_env).create(**new_env)
            env.save()

    def put_node(self, old_node, new_node):
        with chef.ChefAPI(self.url, self.open_client_pem, self.user):
            get_old_nodes = chef.Node(old_node).list()
            if old_node in get_old_nodes.iterkeys():
                print('deleted old node %s' % old_node)
                chef.Node(old_node).delete()

            node = chef.Node(old_node).create(**new_node)
            node.save()
