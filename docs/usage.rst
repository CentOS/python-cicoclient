Usage
=====
In order to be able to use ``cico``, you need to use it from a location that
has network connectivity to the administrative endpoint, by default this is
``http://admin.ci.centos.org:8080/``.

Built-in CLI help
~~~~~~~~~~~~~~~~~
``cico`` comes built-in with powerful help that explains available commands,
their available arguments and output formatting options thanks to the cliff_
library.

Here's what it looks like::

        $ cico help
        usage: cico [--version] [-v] [--log-file LOG_FILE] [-q] [-h] [--debug]
                    [--endpoint <endpoint>] [--api-key <api-key>]

        CLI interface to admin.ci.centos.org

        optional arguments:
          --version             show program's version number and exit
          -v, --verbose         Increase verbosity of output. Can be repeated.
          --log-file LOG_FILE   Specify a file to log output. Disabled by default.
          -q, --quiet           Suppress output except warnings and errors.
          -h, --help            Show help message and exit.
          --debug               Show tracebacks on errors.
          --endpoint <endpoint>
                                Endpoint to the admin.ci.centos.org service. Defaults
                                to: http://admin.ci.centos.org:8080/
          --api-key <api-key>   API key to admin.ci.centos.org service. Defaults to
                                environment variable for CICO_API_KEY.

        Commands:
          complete       print bash completion command
          help           print detailed help for another command
          inventory      Return a node inventory from the ci.centos.org infrastructure.
          node done      Releases nodes from the ci.centos.org infrastructure for a ssid
          node get       Requests nodes from the ci.centos.org infrastructure

Setting your endpoint
~~~~~~~~~~~~~~~~~~~~~
The endpoint defaults to ``http://admin.ci.centos.org:8080/``. If you ever need
to set this to something else, such as a test environment, you can override the
default with the ``--endpoint`` argument.

Setting your API key
~~~~~~~~~~~~~~~~~~~~
There are two ways of setting your API key when using ``cico``. You can either
provide it on the command line like so::

    cico <command> --api-key <key>

Or by using the ``CICO_API_KEY`` environmental variable::

    export CICO_API_KEY=<key>; cico <command>

Some commands, such as ``cico inventory`` do not require a key to be set.
For more information, please refer to the `Duffy documentation`_.

Retrieving node inventory
~~~~~~~~~~~~~~~~~~~~~~~~~
The ``cico inventory`` command will allow you to retrieve the node inventory.

- If you do not have an API key configured or if you use the ``--all`` argument,
  you will get the list of all nodes.

- If you have an API key configured, you will only get the inventory of nodes
  that are tied to your API key.

Built-in help::

        $ cico help inventory
        usage: cico inventory [-h] [-f {csv,json,table,value,yaml}] [-c COLUMN]
                              [--max-width <integer>] [--noindent]
                              [--quote {all,minimal,none,nonnumeric}] [--all]

        Return a node inventory from the ci.centos.org infrastructure.

        optional arguments:
          -h, --help            show this help message and exit
          --all                 Display all nodes, regardless if an API key is used.

        output formatters:
          output formatter options

          -f {csv,json,table,value,yaml}, --format {csv,json,table,value,yaml}
                                the output format, defaults to table
          -c COLUMN, --column COLUMN
                                specify the column(s) to include, can be repeated

        table formatter:
          --max-width <integer>
                                Maximum display width, 0 to disable

        json formatter:
          --noindent            whether to disable indenting the JSON

        CSV Formatter:
          --quote {all,minimal,none,nonnumeric}
                                when to include quotes, defaults to nonnumeric

Usage::

        $ cico inventory
        Starting new HTTP connection (1): admin.ci.centos.org
        Resetting dropped connection: admin.ci.centos.org
        +---------+---------------+--------------+-----------+------------+---------------+--------------------------------------+--------+------+----------------+--------------+-----------+
        | host_id |   hostname    | ip_address   |  chassis  | used_count | current_state | comment                              | distro | rel  | centos_version | architecture | node_pool |
        +---------+---------------+--------------+-----------+------------+---------------+--------------------------------------+--------+------+----------------+--------------+-----------+
        |     170 | node1.cluster | <obfuscated> | <cluster> |         66 | Deployed      | e0c382aa-8a30-11e5-b2e3-525400ea212d | None   | None | 7              | x86_64       |         0 |
        |      21 | node2.cluster | <obfuscated> | <cluster> |         66 | Deployed      | b54cea7a-8a40-11e5-b2e3-525400ea212d | None   | None | 7              | x86_64       |         0 |
        |      64 | node3.cluster | <obfuscated> | <cluster> |         67 | Deployed      | 3b413756-8967-11e5-b2e3-525400ea212d | None   | None | 7              | x86_64       |         0 |
        +---------+---------------+--------------+-----------+------------+---------------+--------------------------------------+--------+------+----------------+--------------+-----------+

Requesting a node
~~~~~~~~~~~~~~~~~
The ``cico node get`` command will allow you to request one or more nodes.
This command requires an API key to be configured.

Built-in help::

        $ cico help node get
        usage: cico node get [-h] [-f {csv,json,table,value,yaml}] [-c COLUMN]
                             [--max-width <integer>] [--noindent]
                             [--quote {all,minimal,none,nonnumeric}] [--arch <arch>]
                             [--release <release>] [--count <count>]

        Requests nodes from the ci.centos.org infrastructure

        optional arguments:
          -h, --help            show this help message and exit
          --arch <arch>         Requested server architecture. Defaults to x86_64.
          --release <release>   Requested CentOS release. Defaults to 7.
          --count <count>       Requested amount of servers. Defaults to 1.

        output formatters:
          output formatter options

          -f {csv,json,table,value,yaml}, --format {csv,json,table,value,yaml}
                                the output format, defaults to table
          -c COLUMN, --column COLUMN
                                specify the column(s) to include, can be repeated

        table formatter:
          --max-width <integer>
                                Maximum display width, 0 to disable

        json formatter:
          --noindent            whether to disable indenting the JSON

        CSV Formatter:
          --quote {all,minimal,none,nonnumeric}
                                when to include quotes, defaults to nonnumeric

Usage::

        $ cico node get --arch x86_64 --release 7 --count 1
        Starting new HTTP connection (1): admin.ci.centos.org
        Resetting dropped connection: admin.ci.centos.org
        Resetting dropped connection: admin.ci.centos.org
        SSID for these servers: 8fd381ea-8a46-11e5-b2e3-525400ea212d
        +---------+----------------+--------------+---------+------------+---------------+---------+--------+------+----------------+--------------+-----------+
        | host_id |    hostname    |  ip_address  | chassis | used_count | current_state | comment | distro | rel  | centos_version | architecture | node_pool |
        +---------+----------------+--------------+---------+------------+---------------+---------+--------+------+----------------+--------------+-----------+
        |     117 | node4.cluster  | <obfuscated> | cluster |         69 | Ready         | -       | None   | None | 7              | x86_64       |         1 |
        +---------+----------------+--------------+---------+------------+---------------+---------+--------+------+----------------+--------------+-----------+

Releasing a node
~~~~~~~~~~~~~~~~
The ``cico node done`` command will allow you to release all the nodes tied
to a session ID.
This command requires an API key to be configured.

Built-in help::

        $ cico help node done
        usage: cico node done [-h] [-f {csv,json,table,value,yaml}] [-c COLUMN]
                              [--max-width <integer>] [--noindent]
                              [--quote {all,minimal,none,nonnumeric}]
                              <ssid>

        Releases nodes from the ci.centos.org infrastructure for a ssid

        positional arguments:
          <ssid>                SSID of the server pool to release

        optional arguments:
          -h, --help            show this help message and exit

        output formatters:
          output formatter options

          -f {csv,json,table,value,yaml}, --format {csv,json,table,value,yaml}
                                the output format, defaults to table
          -c COLUMN, --column COLUMN
                                specify the column(s) to include, can be repeated

        table formatter:
          --max-width <integer>
                                Maximum display width, 0 to disable

        json formatter:
          --noindent            whether to disable indenting the JSON

        CSV Formatter:
          --quote {all,minimal,none,nonnumeric}
                                when to include quotes, defaults to nonnumeric


Usage::

        $ cico node done 8fd381ea-8a46-11e5-b2e3-525400ea212d
        Starting new HTTP connection (1): admin.ci.centos.org
        Resetting dropped connection: admin.ci.centos.org
        Resetting dropped connection: admin.ci.centos.org
        Released these servers with SSID: 8fd381ea-8a46-11e5-b2e3-525400ea212d
        +---------+---------------+--------------+---------+------------+---------------+--------------------------------------+--------+------+----------------+--------------+-----------+
        | host_id |    hostname   |  ip_address  | chassis | used_count | current_state | comment                              | distro | rel  | centos_version | architecture | node_pool |
        +---------+---------------+--------------+---------+------------+---------------+--------------------------------------+--------+------+----------------+--------------+-----------+
        |     117 | node4.cluster | <obfuscated> | cluster |         69 | Deployed      | 8fd381ea-8a46-11e5-b2e3-525400ea212d | None   | None | 7              | x86_64       |         1 |
        +---------+---------------+--------------+---------+------------+---------------+--------------------------------------+--------+------+----------------+--------------+-----------+

.. _Duffy documentation: https://wiki.centos.org/QaWiki/CI/Duffy
.. _cliff: https://pypi.python.org/pypi/cliff
