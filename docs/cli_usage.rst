Usage
=====
In order to be able to use ``cico``, you need to use it from a location that
has network connectivity to the administrative endpoint, by default this is
``http://admin.ci.centos.org:8080/``.

Built-in help
~~~~~~~~~~~~~
``cico`` comes built-in with powerful CLI help that explains available commands,
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

If you have installed ``python-cicoclient`` from a RPM repository, you can also
access the complete documentation with ``man cico``.

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
- You can also provide a SSID to only return hosts matching this specific SSID.

Built-in help::

        $ cico help inventory
        usage: cico inventory [-h] [-f {csv,json,table,value,yaml}] [-c COLUMN]
                              [--max-width <integer>] [--noindent]
                              [--quote {all,minimal,none,nonnumeric}]
                              [--ssid <ssid>]

        Returns a node inventory from the ci.centos.org infrastructure.

        optional arguments:
          -h, --help            show this help message and exit
          --ssid <ssid>         Only return nodes matching the provided ssid.

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
        +----+------------+-------------+----------+----------+--------+------+-----+--------+---------+------+--------------+------------+
        | id | hostname   | ip          | comment  | state    | distro | rel  | ver | arch   | chassis | pool | console_port | used_count |
        +----+------------+-------------+----------+----------+--------+------+-----+--------+---------+------+--------------+------------+
        | 12 | n1.cluster | 172.19.3.1  | e90b20b8 | Deployed | None   | None | 7   | x86_64 | cluster |    0 |         2110 |        102 |
        |  2 | n2.cluster | 172.19.3.2  | ea32338c | Deployed | None   | None | 7   | x86_64 | cluster |    0 |         2010 |        141 |
        +----+------------+-------------+----------+----------+--------+------+-----+--------+---------+------+--------------+------------+

        $ cico inventory --ssid e90b20b8
        +----+------------+-------------+----------+----------+--------+------+-----+--------+---------+------+--------------+------------+
        | id | hostname   | ip          | comment  | state    | distro | rel  | ver | arch   | chassis | pool | console_port | used_count |
        +----+------------+-------------+----------+----------+--------+------+-----+--------+---------+------+--------------+------------+
        | 12 | n1.cluster | 172.19.3.1  | e90b20b8 | Deployed | None   | None | 7   | x86_64 | cluster |    0 |         2110 |        102 |
        +----+------------+-------------+----------+----------+--------+------+-----+--------+---------+------+--------------+------------+

        $ cico inventory -f value -c hostname -c ip -c comment
        n1.cluster 172.19.3.1 e90b20b8
        n2.cluster 172.19.3.2 ea32338c

        $ cico inventory -f json
        [
          {
            "comment": "e90b20b8",
            "ver": "7",
            "ip": "172.19.3.1",
            "hostname": "n1.cluster",
            "state": "Deployed",
            "chassis": "cluster",
            "used_count": 102,
            "rel": null,
            "console_port": 2110,
            "arch": "x86_64",
            "id": 12,
            "pool": 0,
            "distro": null
          },
          {
            "comment": "ea32338c",
            "ver": "7",
            "ip": "172.19.3.2",
            "hostname": "n2.cluster",
            "state": "Deployed",
            "chassis": "cluster",
            "used_count": 141,
            "rel": null,
            "console_port": 2010,
            "arch": "x86_64",
            "id": 2,
            "pool": 0,
            "distro": null
          }
        ]

        $ cico inventory -f yaml
        - arch: x86_64
          chassis: cluster
          comment: e90b20b8
          console_port: 2110
          distro: null
          hostname: n1.cluster
          id: 12
          ip: 172.19.3.1
          pool: 0
          rel: null
          state: Deployed
          used_count: 102
          ver: '7'
        - arch: x86_64
          chassis: cluster
          comment: ea32338c
          console_port: 2010
          distro: null
          hostname: n2.cluster
          id: 2
          ip: 172.19.3.2
          pool: 0
          rel: null
          state: Deployed
          used_count: 141
          ver: '7'

Requesting nodes
~~~~~~~~~~~~~~~~
The ``cico node get`` command will allow you to request one or more nodes.
This command requires an API key to be configured.

Built-in help::

        $ cico help node get
        usage: cico node get [-h] [-f {csv,json,table,value,yaml}] [-c COLUMN]
                             [--max-width <integer>] [--noindent]
                             [--quote {all,minimal,none,nonnumeric}] [--arch <arch>]
                             [--release <release>] [--count <count>]
                             [--retry-count <count>] [--retry-interval <seconds>]

        Requests nodes from the ci.centos.org infrastructure

        optional arguments:
          -h, --help            show this help message and exit
          --arch <arch>         Requested server architecture. Defaults to x86_64.
          --release <release>   Requested CentOS release. Defaults to 7.
          --count <count>       Requested amount of servers. Defaults to 1.
          --retry-count <count>
                                Amount of retries to do in case of failure. Defaults
                                to 1.
          --retry-interval <seconds>
                                Wait between subsequent retries. Defaults to 10
                                (seconds).

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

        $ cico node get --arch x86_64 --release 7 --count 1 --retry-count 2 --retry-interval 30
        +----+------------+-------------+----------+----------+--------+------+-----+--------+---------+------+--------------+------------+
        | id | hostname   | ip          | comment  | state    | distro | rel  | ver | arch   | chassis | pool | console_port | used_count |
        +----+------------+-------------+----------+----------+--------+------+-----+--------+---------+------+--------------+------------+
        | 12 | n1.cluster | 172.19.3.1  | e90b20b8 | Deployed | None   | None | 7   | x86_64 | cluster |    0 |         2110 |        102 |
        +----+------------+-------------+----------+----------+--------+------+-----+--------+---------+------+--------------+------------+

Releasing nodes
~~~~~~~~~~~~~~~
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

        $ cico node done e90b20b8
        +----+------------+-------------+----------+----------+--------+------+-----+--------+---------+------+--------------+------------+
        | id | hostname   | ip          | comment  | state    | distro | rel  | ver | arch   | chassis | pool | console_port | used_count |
        +----+------------+-------------+----------+----------+--------+------+-----+--------+---------+------+--------------+------------+
        | 12 | n1.cluster | 172.19.3.1  | e90b20b8 | Deployed | None   | None | 7   | x86_64 | cluster |    0 |         2110 |        102 |
        +----+------------+-------------+----------+----------+--------+------+-----+--------+---------+------+--------------+------------+

.. _Duffy documentation: https://wiki.centos.org/QaWiki/CI/Duffy
.. _cliff: https://pypi.python.org/pypi/cliff
