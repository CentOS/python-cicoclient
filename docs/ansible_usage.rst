Usage
=====
In order to be able to use the ``cico`` Ansible_ module, you need to use it from
a location that has network connectivity to the administrative endpoint, by
default this is ``http://admin.ci.centos.org:8080/``.

The ``cico`` Ansible module comes packaged with ``python-cicoclient``.

To use it, it would be convenient to add the module to your Ansible module
library. An example Ansible configuration file can be found inside the package_.

.. _Ansible: http://www.ansible.com/
.. _package: https://github.com/dmsimard/python-cicoclient/blob/master/cicoclient/ansible/ansible.cfg.example

Built-in help
~~~~~~~~~~~~~
The ``cico`` Ansible module comes built-in with Ansible documentation, you can
use ``ansible-doc`` to access it::

    $ ansible-doc -M cicoclient/ansible cico
    > CICO

      Ansible module to manage ci.centos.org node lifecycle

    Options (= is mandatory):

    = action
            Action to take (Choices: get, done, list)

    - api_key
            API key [Default: CICO_API_KEY environment variable or None]

    - arch
            Server architecture (Choices: i386, x86_64, aarch64, ppc64le) [Default: x86_64]

    - count
            Amount of nodes [Default: 1]

    - endpoint
            API endpoint [Default: http://admin.ci.centos.org:8080/]

    - release
            CentOS release (Choices: 5, 6, 7) [Default: 7]

    - flavor
        The flavor (size) of an altarch Node (ignored on baremetal x86_64)
        (Choices: tiny, small, medium, lram.tiny, lram.small, lram.medium, xram.tiny, xram.small, xram.medium, xram.large)[Default: small]

    - retry_count
            Amount of retries to do in case of failure. [Default: 1]

    - retry_interval
            Wait (in seconds) between subsequent retries. [Default: 10]

    - ssid
            SessionID, required with action 'done', optional with 'list'.

    Requirements:  python >= 2.6, python-cicoclient

    EXAMPLES:
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

    MAINTAINERS: David Moreau Simard <dms@redhat.com>

Retrieving node inventory
~~~~~~~~~~~~~~~~~~~~~~~~~
The ``cico`` inventory action will allow you to retrieve the node inventory.

- If you do not provide an API key, you will get the list of all nodes.
- If you provide an API key, you will only get the inventory of nodes that are
  tied to your API key.
- You can also provide a SSID to only return hosts matching this specific SSID.

Example::

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

Requesting nodes
~~~~~~~~~~~~~~~~
The ``cico`` get action will allow you to request one or more nodes.
This command requires an API key to be configured.

Example::

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

Releasing nodes
~~~~~~~~~~~~~~~
The ``cico`` done action command will allow you to release all the nodes tied
to a session ID.
This command requires an API key to be configured.

Example::

    # Release nodes requested in a registered 'get' action
    - cico:
        action: done
        api_key: 723ef3ce-4ea4-4e8d-9c8a-20a8249b2955
        ssid: data.results.ssid

    # Release nodes for a specific ssid
    - cico:
        action: done
        api_key: 723ef3ce-4ea4-4e8d-9c8a-20a8249b2955
        ssid: 3e03553f-ae28-4a68-b879-f0fdbf949d5d
