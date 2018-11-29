Name:             python-cicoclient
Version:          0.4.4
Release:          1%{?dist}
Summary:          Client interfaces to admin.ci.centos.org

License:          ASL 2.0
URL:              https://github.com/CentOS/%{name}
Source0:          https://pypi.io/packages/source/P/%{name}/%{name}-%{version}.tar.gz

BuildArch:        noarch

BuildRequires:    git
BuildRequires:    python2-devel
BuildRequires:    python-cliff
BuildRequires:    python-pbr
BuildRequires:    python-requests
BuildRequires:    python-setuptools
BuildRequires:    python-simplejson
BuildRequires:    python-six

# Work around an old version of python-sphinx_rtd_theme in CBS
BuildRequires:    fontawesome-fonts-web

Requires:         python-cliff >= 1.14.0
Requires:         python-pbr >= 1.6
Requires:         python-requests >= 2.5.2
Requires:         python-simplejson
Requires:         python-six >= 1.9.0

%description
python-cicoclient is a client, library, and a CLI interface that can be used to
communicate with the ci.centos.org infrastructure provisioning system: Duffy.

%package doc
Summary:          Documentation for python-cicoclient

BuildRequires:    python-sphinx
BuildRequires:    python-sphinx_rtd_theme
# python-sphinx_rtd_theme missing dependency https://bugzilla.redhat.com/show_bug.cgi?id=1282297
BuildRequires:    fontawesome-fonts-web

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
%{__python2} setup.py build

%install
%{__python2} setup.py install --skip-build --root %{buildroot}

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
%{python2_sitelib}/cicoclient
%{python2_sitelib}/*.egg-info
%{_mandir}/man1/cico.1*

%files doc
%license LICENSE
%doc html

%changelog
* Thu Nov 29 2018 brian@bstinson.com - 0.4.4-1
- Fixup the default flavor for ansible

* Apr 05 2018 brian@bstinson.com 0.4.2-1
- Build for multiarch support

* Tue Aug 23 2016 brian@bstinson.com 0.3.9-1
- Build in the CentOS infrastructure tags

