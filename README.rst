About
=====
python-cicoclient_ is a client, library, and a CLI interface that can be used
to communicate with the `ci.centos.org`_ infrastructure provisioning system:
Duffy_.

It provides:

* A client library for communicating with the admin.ci.centos.org REST API
* A wrapper library that leverages the client for doing each API call
* A CLI interface that leverages the wrapper to communicate with the API
  from the command line
* An Ansible_ module that leverages the wrapper to communicate with the API
  through Ansible.

.. _python-cicoclient: https://github.com/dmsimard/python-cicoclient
.. _ci.centos.org: https://ci.centos.org/
.. _Duffy: https://wiki.centos.org/QaWiki/CI/Duffy
.. _Ansible: http://www.ansible.com/

Documentation
=============
Documentation on how to install and use python-cicoclient is available on
`ReadTheDocs.org`_

.. _ReadTheDocs.org: http://python-cicoclient.readthedocs.org/en/latest/

Author
======
David Moreau Simard

Copyright
=========
Copyright 2015 Red Hat, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
