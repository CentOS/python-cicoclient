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

import logging

from cliff.lister import Lister
from cicoclient.wrapper import CicoWrapper
from cicoclient import utils


class Inventory(Lister):
    "Return a node inventory from the ci.centos.org infrastructure."

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(Inventory, self).get_parser(prog_name)
        return parser

    @utils.log_method(log)
    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)", parsed_args)
        api = CicoWrapper(
            endpoint=self.app.options.endpoint,
            api_key=self.app.options.api_key
        )

        response, inventory = api.inventory()
        self.log.debug('HTTP: %s' % response)

        columns = ('host_id', 'hostname', 'ip_address', 'chassis',
                'used_count', 'current_state', 'comment', 'distro',
                'rel', 'centos_version', 'architecture', 'node_pool')

        return (columns,
                (utils.get_dict_properties(inventory[host], columns)
                 for host in inventory))
