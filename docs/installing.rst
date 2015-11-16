Installing
==========
With pip
~~~~~~~~
Releases of ``python-cicoclient`` are available on PyPi_::

    pip install python-cicoclient

That's it ! There is no extra dependencies or configuration required.

With yum or dnf
~~~~~~~~~~~~~~~
A note on dependencies
----------------------
``python-cicoclient`` was developed as part of an effort to streamline and
simplify consumption of **ci.centos.org** from the `OpenStack RDO project`_.
As such, it's development was heavily influenced by existing OpenStack clients
and thus, share a lot of dependencies which are provided by the official RDO
mirror.

On EL7
------
::

    yum -y install http://rdoproject.org/repos/openstack-liberty/rdo-release-liberty.rpm
    curl -s https://copr.fedoraproject.org/coprs/dmsimard/python-cicoclient/repo/epel-7/dmsimard-python-cicoclient-epel-7.repo |tee /etc/yum.repos.d/python-cicoclient.repo
    yum -y install python-cicoclient

On Fedora
---------
::

    dnf -y install http://rdoproject.org/repos/openstack-liberty/rdo-release-liberty.rpm
    dnf copr enable dmsimard/python-cicoclient
    dnf -y install python-cicoclient

To get started with ``cico``, read the `usage documentation`_.

.. _PyPi: https://pypi.python.org/pypi/python-cicoclient/
.. _OpenStack RDO project: https://www.rdoproject.org/
.. _usage documentation: usage.html
