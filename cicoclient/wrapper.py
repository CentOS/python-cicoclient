#   Copyright Red Hat, Inc. All Rights Reserved.
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#
#   Author: David Moreau Simard <dms@redhat.com>
#

import cicoclient.client as client


class CicoWrapper(client.CicoClient):
    """
    Wrapper library around the available API calls for the admin.ci.centos.org
    node infrastructure.
    """
    def __init__(self, **params):
        super(CicoWrapper, self).__init__(**params)
        self.user_agent = 'python-cicoclient-wrapper'
        try:
            self.api_key = params['api_key']
        except KeyError:
            self.api_key = None

        self.full_inventory = self._full_inventory()
        self.self_inventory = self._self_inventory()

    def _full_inventory(self):
        """
        Returns a full inventory
        Some additional work required to provide consistent and consumable
        output.
        Inventory output only contains values, no keys - Add the keys to
        the output so that it can be consumed more easily.
        """
        resp, inventory = self.get('Inventory')

        keys = ['host_id', 'hostname', 'ip_address', 'chassis',
                'used_count', 'current_state', 'comment', 'distro',
                'rel', 'centos_version', 'architecture', 'node_pool']

        real_inventory = dict()
        for host in inventory:
            real_inventory[host[1]] = dict()
            for key in keys:
                real_inventory[host[1]][key] = host[keys.index(key)]

        return real_inventory

    def _self_inventory(self):
        """
        Inventory output will only contain the server name and the session ID
        when a key is provided. Provide the same format as with the full
        inventory instead for consistency.
        """
        if self.api_key is None:
            return None

        resp, self_inventory = self.get('Inventory?key=%s' % self.api_key)
        real_self_inventory = dict()

        for host in self_inventory:
            real_self_inventory[host[0]] = self.full_inventory[host[0]]

        return real_self_inventory

    def inventory(self, all=False):
        """
        Returns a node inventory. If an API key is specified, only the nodes
         provisioned by this key will be returned.

        :return: { inventory }
        """
        if all or self.api_key is None:
            return self.full_inventory
        else:
            return self.self_inventory
