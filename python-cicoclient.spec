%if 0%{?rhel} && 0%{?rhel} < 8
%bcond_without python2
%bcond_with python3
%else
%bcond_with python2
%bcond_without python3
%endif

Name:             python-cicoclient
Version:          0.4.7
Release:          1%{?dist}
Summary:          Client interfaces to admin.ci.centos.org

License:          ASL 2.0
URL:              https://github.com/CentOS/%{name}
Source0:          https://pypi.io/packages/source/p/%{name}/%{name}-%{version}.tar.gz

BuildArch:        noarch

BuildRequires:    git

%if %{with python2}
BuildRequires:    python2-devel
BuildRequires:    python-cliff
BuildRequires:    python-pbr
BuildRequires:    python-requests
BuildRequires:    python-setuptools
BuildRequires:    python-six
%endif
%if %{with python3}
BuildRequires:    python3-devel
#BuildRequires:    python3-cliff
BuildRequires:    python3-pbr
BuildRequires:    python3-requests
BuildRequires:    python3-setuptools
BuildRequires:    python3-six
%endif

%if %{with python2}
Requires:         python-cliff >= 1.14.0
Requires:         python-pbr >= 1.6
Requires:         python-requests >= 2.5.2
Requires:         python-six >= 1.9.0
%endif
%if %{with python3}
Requires:         python3-cliff >= 1.14.0
Requires:         python3-pbr >= 1.6
Requires:         python3-requests >= 2.5.2
Requires:         python3-six >= 1.9.0
%endif

%description
python-cicoclient is a client, library, and a CLI interface that can be used to
communicate with the ci.centos.org infrastructure provisioning system: Duffy.

%package doc
Summary:          Documentation for python-cicoclient

%if %{with python2}
BuildRequires:    python-sphinx
BuildRequires:    python-sphinx_rtd_theme
%endif
%if %{with python3}
BuildRequires:    python3-sphinx
BuildRequires:    python3-sphinx_rtd_theme
%endif

Requires:         %{name} = %{version}-%{release}

%description      doc
python-cicoclient is a client, library, and a CLI interface that can be used to
communicate with the ci.centos.org infrastructure provisioning system: Duffy.

This package contains auto-generated documentation.

%prep
%setup -q -n %{name}-%{version}

# Requirements are handled by packaging
rm -f requirements.txt test-requirements.txt

%build
%if %{with python2}
%{__python2} setup.py build
%endif
%if %{with python3}
%py3_build
%endif

%install
%if %{with python2}
%{__python2} setup.py install --skip-build --root %{buildroot}
%endif
%if %{with python3}
%py3_install
%endif

export PYTHONPATH="$( pwd ):$PYTHONPATH"
sphinx-build -b html docs html
sphinx-build -b man docs man

install -p -D -m 644 man/python-cicoclient.1 %{buildroot}%{_mandir}/man1/cico.1

# Fix hidden-file-or-dir warnings
rm -rf html/.doctrees html/.buildinfo

%files
%license LICENSE
%doc README.rst
%{_bindir}/cico
%if %{with python2}
%{python2_sitelib}/cicoclient
%{python2_sitelib}/*.egg-info
%endif
%if %{with python3}
%{python3_sitelib}/cicoclient
%{python3_sitelib}/*.egg-info
%endif
%{_mandir}/man1/cico.1*

%files doc
%license LICENSE
%doc html

%changelog
* Fri Oct 22 2021 Evgeni Golov - 0.4.7-1
- Update to 0.4.7

* Tue Oct 19 2021 arrfab@centos.org - 0.4.6-1
- Bumped to 0.4.6 for 9-stream support

* Tue Oct 29 2019 brian@bstinson.com - 0.4.5-1
- Add CentOS 8 and 8-Stream

* Thu Nov 29 2018 brian@bstinson.com - 0.4.4-1
- Fixup the default flavor for ansible

* Thu Apr 05 2018 brian@bstinson.com 0.4.2-1
- Build for multiarch support

* Tue Aug 23 2016 brian@bstinson.com 0.3.9-1
- Build in the CentOS infrastructure tags

