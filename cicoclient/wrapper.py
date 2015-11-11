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

    def inventory(self):
        """
        Returns a node inventory. If an API key is specified, only the nodes
         provisioned by this key will be returned.

         Some additional work required to provide consistent and consumable
         output.
           - Inventory output only contains values, no keys - Add the keys to
             the output so that it can be consumed more easily.
           - Additionally, if you provide a key, you only get the ssid of the
             node. Fill in the rest of the node's details.

        :param key: API key for the admin.ci.centos.org provisioning service
        :return: [ status_code, json_inventory_dict ]
        """
        # We'll need the full inventory regardless since the node information
        # is in this call.
        resp, inventory = self.get('Inventory')

        keys = ['host_id', 'hostname', 'ip_address', 'chassis',
                'used_count', 'current_state', 'comment', 'distro',
                'rel', 'centos_version', 'architecture', 'node_pool']

        # For each host, build a dict of key=>value coming from just values
        real_inventory = dict()
        for host in inventory:
            real_inventory[host[1]] = dict()
            for key in keys:
                real_inventory[host[1]][key] = host[keys.index(key)]

        if self.api_key is not None:
            resp, self_inventory = self.get('Inventory?key=%s' % self.api_key)
            real_self_inventory = dict()

            # Inventory output will only contain the server name and session
            # ID when a key is provided. Provide the same format as with the
            # full inventory instead for consistency.
            for host in self_inventory:
                real_self_inventory[host[0]] = real_inventory[host[0]]

            inventory = real_self_inventory
        else:
            inventory = real_inventory

        return resp, inventory
