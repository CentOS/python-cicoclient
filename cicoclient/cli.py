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

import logging

from cliff.lister import Lister

from cicoclient import utils
from cicoclient.wrapper import CicoWrapper


class Inventory(Lister):
    """Returns a node inventory from the ci.centos.org infrastructure."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(Inventory, self).get_parser(prog_name)
        parser.add_argument(
            '--all',
            action='store_true',
            default=False,
            help='Display all nodes, regardless if an API key is used.'
        )
        parser.add_argument(
            '--ssid',
            metavar="<ssid>",
            default=None,
            help='Only return nodes matching the provided ssid.'
        )
        return parser

    @utils.log_method(log)
    def take_action(self, parsed_args):
        api = CicoWrapper(
            endpoint=self.app.options.endpoint,
            api_key=self.app.options.api_key
        )

        inventory = api.inventory(all=parsed_args.all,
                                  ssid=parsed_args.ssid)

        columns = ('host_id', 'hostname', 'ip_address', 'chassis',
                   'used_count', 'current_state', 'comment', 'distro',
                   'rel', 'centos_version', 'architecture', 'node_pool',
                   'console_port', 'flavor')

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
            choices=['i386', 'x86_64', 'aarch64', 'ppc64le'],
            default='x86_64',
            help='Requested server architecture. Defaults to x86_64.'
        )
        parser.add_argument(
            '--release',
            metavar='<release>',
            choices=['5', '6', '7'],
            default='7',
            help='Requested CentOS release. Defaults to 7.'
        )
        parser.add_argument(
            '--count',
            metavar='<count>',
            type=int,
            default=1,
            help='Requested number of servers. Defaults to 1.'
        )
        parser.add_argument(
            '--retry-count',
            metavar='<count>',
            type=int,
            default=1,
            help='Number of retries to do in case of failure. Defaults to 1.'
        )
        parser.add_argument(
            '--retry-interval',
            metavar='<seconds>',
            type=int,
            default=10,
            help='Wait between subsequent retries. Defaults to 10 (seconds).'
        )
        parser.add_argument(
            '--flavor',
            metavar='<flavor>',
            default=None,
            choices=['tiny', 'small', 'medium', 'lram.tiny', 'lram.small',
                     'lram.medium', 'xram.tiny', 'xram.small',
                     'xram.medium', 'xram.large'],
            help='The flavor of the node.'
        )
        return parser

    @utils.log_method(log)
    def take_action(self, parsed_args):
        api = CicoWrapper(
            endpoint=self.app.options.endpoint,
            api_key=self.app.options.api_key
        )

        hosts, ssid = api.node_get(arch=parsed_args.arch,
                                   ver=parsed_args.release,
                                   count=parsed_args.count,
                                   retry_count=parsed_args.retry_count,
                                   retry_interval=parsed_args.retry_interval,
                                   flavor=parsed_args.flavor)

        columns = ('host_id', 'hostname', 'ip_address', 'chassis',
                   'used_count', 'current_state', 'comment', 'distro',
                   'rel', 'centos_version', 'architecture', 'node_pool',
                   'console_port', 'flavor')

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

        columns = ('host_id', 'hostname', 'ip_address', 'chassis',
                   'used_count', 'current_state', 'comment', 'distro',
                   'rel', 'centos_version', 'architecture', 'node_pool',
                   'console_port', 'flavor')

        return (columns,
                (utils.get_dict_properties(hosts[host], columns)
                 for host in hosts))
