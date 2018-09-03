#!/usr/bin/env python

"""
Ansible dynamic inventory script for ci.centos.org
==================================================

Configuration
-------------
All configuration happens using environment variables.

The following variables are supported:
* `CICO_API_KEY` is the API key.
   If unset python-cicoclient will search for one automatically.
* `CICO_ENDPOINT` is the API URL, defaults to http://admin.ci.centos.org:8080
* `CICO_SSID` is the SSID to fetch hosts for.
   If unset the inventory script will fetch *all* hosts.
* `CICO_STATE` is the state of hosts to filter for.
   Defaults to 'Deployed', as these are the hosts you can connect to.
   Can be set to 'All' to get hosts in all states.

Usage
-----
In most cases, runing `ansible -i <path/to/cico_inventory.py> ...` should be
sufficient. Please export the relevant environment variables before running
`ansible` if these are required.

"""

from __future__ import print_function

import argparse
import json
import os
from collections import defaultdict
from cicoclient.wrapper import CicoWrapper


def ansible_hostvars(host):
    new_host = {}
    for key in host.keys():
        new_key = 'cico_{}'.format(key)
        new_host[new_key] = host[key]
    new_host['ansible_fqdn'] = host['hostname']
    new_host['ansible_host'] = host['ip_address']
    return new_host


def main():
    api_key = os.getenv('CICO_API_KEY', None)
    endpoint = os.environ.get('CICO_ENDPOINT', 'http://admin.ci.centos.org:8080/')
    ssid = os.environ.get('CICO_SSID', None)
    state = os.environ.get('CICO_STATE', 'Deployed')

    parser = argparse.ArgumentParser(
        description='Ansible dynamic inventory script for ci.centos.org.',
    )
    parser.add_argument(
        '--list',
        action='store_true',
        help='get the list of all hosts',
    )
    parser.add_argument(
        '--host',
        help='get the details of a specific host',
    )
    parser.add_argument(
        '--pretty',
        action='store_true',
        default=False,
        help='Pretty format (default: %(default)s).',
    )
    args = parser.parse_args()

    cicoapi = CicoWrapper(
        endpoint=endpoint,
        api_key=api_key
    )

    hosts = {}
    for host, hostvars in cicoapi.inventory(ssid=ssid).items():
        if hostvars['current_state'] == state or state.lower() == 'all':
            hosts[host] = hostvars

    inventory = defaultdict(dict)
    if args.host:
        if args.host in hosts.keys():
            inventory = ansible_hostvars(hosts[args.host])
    elif args.list:
        inventory['all']['hosts'] = hosts.keys()
        inventory['_meta'] = defaultdict(dict)
        for host, hostvars in hosts.items():
            inventory['_meta']['hostvars'][host] = ansible_hostvars(hostvars)
            host_ssid = hostvars['comment']
            if host_ssid:
                if host_ssid not in inventory:
                    inventory[host_ssid] = defaultdict(list)
                inventory[host_ssid]['hosts'].append(host)

    json_kwargs = {}
    if args.pretty:
        json_kwargs.update({'indent': 4, 'sort_keys': True})
    print(json.dumps(inventory, **json_kwargs))


if __name__ == '__main__':
    main()
