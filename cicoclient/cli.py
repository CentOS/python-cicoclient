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
import sys

from cliff.lister import Lister
from cicoclient.wrapper import CicoWrapper
from cicoclient import utils


class Inventory(Lister):
    "Return a node inventory from the ci.centos.org infrastructure."

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(Inventory, self).get_parser(prog_name)
        parser.add_argument(
            '--all',
            action='store_true',
            default=False,
            help='Display all nodes, regardless if an API key is used.'
        )
        return parser

    @utils.log_method(log)
    def take_action(self, parsed_args):
        api = CicoWrapper(
            endpoint=self.app.options.endpoint,
            api_key=self.app.options.api_key
        )

        inventory = api.inventory(all=parsed_args.all)

        columns = ('host_id', 'hostname', 'ip_address', 'chassis',
                'used_count', 'current_state', 'comment', 'distro',
                'rel', 'centos_version', 'architecture', 'node_pool')

        return (columns,
                (utils.get_dict_properties(inventory[host], columns)
                 for host in inventory))

class NodeGet(Lister):
    """Requests nodes from the ci.centos.org infrastructure"""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(NodeGet, self).get_parser(prog_name)
        parser.add_argument(
            '--arch',
            metavar='<arch>',
            choices=['i386', 'x86_64'],
            default='x86_64',
            help='Requested server architecture. Defaults to x86_64.'
        )
        parser.add_argument(
            '--ver',
            metavar='<ver>',
            choices=['5', '6', '7'],
            default='7',
            help='Requested CentOS release. Defaults to 7.'
        )
        parser.add_argument(
            '--count',
            metavar='<ver>',
            type=int,
            default=1,
            help='Requested amount of servers. Defaults to 1.'
        )
        return parser

    @utils.log_method(log)
    def take_action(self, parsed_args):
        api = CicoWrapper(
            endpoint=self.app.options.endpoint,
            api_key=self.app.options.api_key
        )

        hosts, ssid = api.node_get(arch=parsed_args.arch,
                                   ver=parsed_args.ver,
                                   count=parsed_args.count)
        message= "SSID for these servers: %s\n" % ssid
        sys.stdout.write(message)

        columns = ('host_id', 'hostname', 'ip_address', 'chassis',
                'used_count', 'current_state', 'comment', 'distro',
                'rel', 'centos_version', 'architecture', 'node_pool')

        return (columns,
        (utils.get_dict_properties(hosts[host], columns)
         for host in hosts))


class NodeDone(Lister):
    """Releases nodes from the ci.centos.org infrastructure for a ssid"""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(NodeDone, self).get_parser(prog_name)
        parser.add_argument(
            'ssid',
            metavar='<ssid>',
            help='SSID of the server pool to release'
        )
        return parser

    @utils.log_method(log)
    def take_action(self, parsed_args):
        api = CicoWrapper(
            endpoint=self.app.options.endpoint,
            api_key=self.app.options.api_key
        )

        hosts = api.node_done(ssid=parsed_args.ssid)
        message= "Released these servers with SSID: %s\n" % parsed_args.ssid
        sys.stdout.write(message)

        columns = ('host_id', 'hostname', 'ip_address', 'chassis',
                'used_count', 'current_state', 'comment', 'distro',
                'rel', 'centos_version', 'architecture', 'node_pool')

        return (columns,
        (utils.get_dict_properties(hosts[host], columns)
         for host in hosts))
