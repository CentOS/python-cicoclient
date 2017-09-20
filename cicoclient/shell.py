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

import sys

import cicoclient
from cliff.app import App
from cliff.commandmanager import CommandManager


class CicoCli(App):
    """
    CLI interface boilerplate with cliff
    """
    def __init__(self):
        super(CicoCli, self).__init__(
            description='CLI interface to admin.ci.centos.org',
            version=cicoclient.__version__,
            command_manager=CommandManager('cico.cli'),
            deferred_help=True,
            )

    def build_option_parser(self, description, version):
        parser = super(CicoCli, self).build_option_parser(description, version)

        # Global arguments
        parser.add_argument(
            '--endpoint',
            metavar='<endpoint>',
            help='Endpoint to the admin.ci.centos.org service.\n'
                 ' Defaults to: http://admin.ci.centos.org:8080/',
            default='http://admin.ci.centos.org:8080/'
        )
        parser.add_argument(
            '--api-key',
            metavar='<api-key>',
            help='API key to admin.ci.centos.org service. If not provided the'
                 ' value of the CICO_API_KEY environment variable will be used'
                 ' if defined, followed by the contents of ~/.duffy.key if'
                 ' present, finally the contents of ~/duffy.key if present.',
            default=None
        )

        return parser

    def initialize_app(self, argv):
        self.LOG.debug('initialize_app')

    def prepare_to_run_command(self, cmd):
        self.LOG.debug('prepare_to_run_command %s', cmd.__class__.__name__)

    def clean_up(self, cmd, result, err):
        self.LOG.debug('clean_up %s', cmd.__class__.__name__)
        if err:
            self.LOG.debug('got an error: %s', err)


def main(argv=sys.argv[1:]):
    cicocli = CicoCli()
    return cicocli.run(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
