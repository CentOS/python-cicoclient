Welcome to the python-cicoclient documentation!
===============================================

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

Table of Contents
=================

.. toctree::
    :maxdepth: 2

    Installing <installing>
    Using cico with CLI <cli_usage>
    Using cico with Ansible <ansible_usage>
