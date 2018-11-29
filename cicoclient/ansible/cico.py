#!/usr/bin/python
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

from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = '''
---
module: cico
short_description: Ansible module to manage ci.centos.org node lifecycle
version_added: "2.0"
author: "David Moreau Simard <dms@redhat.com>"
description:
    - Ansible module to manage ci.centos.org node lifecycle
options:
    action:
        description:
            - Action to take
        choices: [get, done, list]
        required: true
    arch:
        description:
            - Server architecture
        choices: [i386, x86_64, aarch64, ppc64le]
        default: x86_64
    release:
        description:
            - CentOS release
        choices: [5, 6, 7]
        default: 7
    flavor:
        description:
            - The flavor (size) of an altarch Node
        choices:
            - tiny
            - small
            - medium
            - lram.tiny
            - lram.small
            - lram.medium
            - xram.tiny
            - xram.small
            - xram.medium
            - xram.large
        default: small

    count:
        description:
            - Number of nodes
        default: 1
    retry_count:
        description:
            - Number of retries to do in case of failure.
        default: 1
    retry_interval:
        description:
            - Wait (in seconds) between subsequent retries.
        default: 10
    endpoint:
        description:
            - API endpoint
        default: http://admin.ci.centos.org:8080/
    api_key:
        description:
            - API key
        default: >
            CICO_API_KEY environment variable, the contents of ~/.duffy.key,
            the contents of ~/duffy.key, or None
    ssid:
        description:
            - SessionID, required with action 'done', optional with 'list'.

requirements:
    - "python >= 2.6"
    - "python-cicoclient"
'''

EXAMPLES = '''
# Retrieve full inventory
- cico:
    action: list
  register: data

# Retrieve inventory tied to API key
- cico:
    action: list
    api_key:  723ef3ce-4ea4-4e8d-9c8a-20a8249b2955
  register: data

# Retrieve inventory tied to a SSID
- cico:
    action: list
    ssid:  3e03553f-ae28-4a68-b879-f0fdbf949d5d
  register: data

# Request one CentOS 7 x86_64 node
- cico:
    action: get
    api_key: 723ef3ce-4ea4-4e8d-9c8a-20a8249b2955
  register: data

# Request one CentOS 7 x86_64 node with increased tolerance failure
- cico:
    action: get
    api_key: 723ef3ce-4ea4-4e8d-9c8a-20a8249b2955
    retry_count: 3
    retry_interval: 60
  register: data

# Request two CentOS 6 i386 nodes
- cico:
    action: get
    api_key: 723ef3ce-4ea4-4e8d-9c8a-20a8249b2955
    arch: i386
    release: 6
    count: 2
  register: data

# Release nodes requested in a registered 'get' action
- cico:
    action: done
    api_key: 723ef3ce-4ea4-4e8d-9c8a-20a8249b2955
    ssid: data.ssid

# Release nodes for a specific ssid
- cico:
    action: done
    api_key: 723ef3ce-4ea4-4e8d-9c8a-20a8249b2955
    ssid: 3e03553f-ae28-4a68-b879-f0fdbf949d5d
'''

try:
    from cicoclient.wrapper import CicoWrapper
    HAS_CICO = True
except ImportError:
    HAS_CICO = False


def main():
    argument_spec = dict(
        action=dict(required=True, choices=['get', 'done', 'list']),
        arch=dict(default='x86_64', choices=['i386', 'x86_64', 'aarch64',
                                             'ppc64le']),
        flavor=dict(default=None, choices=['tiny', 'small', 'medium',
                                              'lram.tiny', 'lram.small',
                                              'xram.tiny', 'xram.small',
                                              'xram.medium', 'xram.large']),
        release=dict(default='7', choices=['5', '6', '7']),
        count=dict(default=1, type='int'),
        retry_count=dict(default=1, type='int'),
        retry_interval=dict(default=10, type='int'),
        endpoint=dict(default='http://admin.ci.centos.org:8080/'),
        api_key=dict(default=None, no_log=True),
        ssid=dict(default=None),
    )
    module = AnsibleModule(argument_spec)

    if not HAS_CICO:
        module.fail_json(msg='cicoclient is required for this module.')

    action = module.params['action']
    arch = module.params['arch']
    release = module.params['release']
    count = module.params['count']
    retry_count = module.params['retry_count']
    retry_interval = module.params['retry_interval']
    endpoint = module.params['endpoint']
    api_key = module.params['api_key']
    ssid = module.params['ssid']
    flavor = module.params['flavor']

    if action == 'done' and ssid is None:
        module.fail_json(msg='A SSID is required when releasing nodes.')

    try:
        api = CicoWrapper(
            endpoint=endpoint,
            api_key=api_key
        )

        if api.api_key is None:
            module.fail_json(msg='An API key is required for this module.')

        if action == 'get':
            hosts, new_ssid = api.node_get(arch=arch, ver=release, count=count,
                                           retry_count=retry_count,
                                           retry_interval=retry_interval,
                                           flavor=flavor)
            data = {
                'message': 'Requested servers successfully',
                'hosts': hosts,
                'ssid': new_ssid
            }
            module.exit_json(changed=True, results=data)

        if action == 'done':
            hosts = api.node_done(ssid=ssid)
            data = {
                'message': 'Released servers successfully',
                'hosts': hosts
            }
            module.exit_json(changed=True, results=data)

        if action == 'list':
            hosts = api.inventory(ssid=ssid)

            data = {
                'message': 'Listed servers successfully',
                'hosts': hosts
            }
            module.exit_json(changed=True, results=data)

    except Exception as e:
        module.fail_json(msg=e.message)


if __name__ == '__main__':
    main()
