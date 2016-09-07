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

import time

import cicoclient.client as client
import cicoclient.exceptions as exceptions


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
            raise AttributeError('Parameter api_key is required. See cico -h.')

    def inventory(self, ssid=None):
        """
        Returns a node inventory. If an SSID is specified, only the nodes tied
        to this SSID will be returned.

        :param ssid: Filter inventory to find nodes for a specific ssid
        :return: { inventory }
        """
        if ssid is not None:
            return self._ssid_inventory(self._inventory, ssid)
        else:
            return self._inventory

    @property
    def _inventory(self):
        """
        Requests node inventory from Duffy that are tied to the user's API
        key

        :return: List of nodes in a dictionary
        """
        resp, inventory = self.get('v1/Inventory?key=%s' % self.api_key)

        return inventory

    def _ssid_inventory(self, inventory, ssid):
        """
        Filters an inventory to only return servers matching ssid
        """
        matching_hosts = []
        for host in inventory:
            if host['comment'] == ssid:
                matching_hosts.append(host)

        return matching_hosts

    def node_get(self, arch=None, ver=None, count=1, retry_count=1,
                 retry_interval=10):
        """
        Requests specified amount of nodes with the provided parameters.

        :param arch: Server architecture (ex: x86_64)
        :param ver: CentOS version (ex: 7)
        :param count: Amount of servers (ex: 2)
        :param retry_count: Number of times to retry in case of failure (ex: 5)
        :param retry_interval: Wait in seconds between each retry (ex: 30)
        :return: [ [ requested_hosts ], ssid ]
        """
        args = "key=%s" % self.api_key
        if arch is not None:
            args += "&arch=%s" % arch
        if ver is not None:
            args += "&ver=%s" % ver
        args += "&count=%s" % count

        resp, body = self.get('Node/get?%s' % args)
        if not body:
            for _ in range(retry_count):
                time.sleep(retry_interval)
                resp, body = self.get('Node/get?%s' % args)
                if body:
                    break

        if not body:
            raise exceptions.NoInventory

        # The Node/get call returns limited information for the requested hosts.
        # Do a new inventory call to retrieve details about the hosts so that
        # output is consistent with the inventory call.
        requested_hosts = []
        for host in self._inventory:
            for hostname in body['hosts']:
                if host['hostname'] in hostname:
                    requested_hosts.append(host)

        return requested_hosts, body['ssid']

    def node_done(self, ssid=None):
        """
        Release the servers for the specified ssid.
        The API doesn't provide any kind of output, try to be helpful by
        providing the list of servers to be released.

        :param ssid: ssid of the server pool
        :return: [ requested_hosts ]
        """
        if ssid is None:
            raise exceptions.SsidRequired

        # There is no body replied in this call so at least get the hosts for
        # the specified ssid to return them.
        requested_hosts = []
        for host in self._inventory:
            if ssid == host['comment']:
                requested_hosts.append(host)

        args = "key={key}&ssid={ssid}".format(key=self.api_key, ssid=ssid)

        resp, body = self.get('Node/done?%s' % args)

        return requested_hosts
