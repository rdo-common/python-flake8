%if 0%{?fedora} > 12 
%bcond_without python3
%else
%bcond_with python3
%endif

%global modname flake8

Name:             python-%{modname}
Version:          2.0
Release:          5%{?dist}
Summary:          Code checking using pep8 and pyflakes

Group:            Development/Languages
License:          MIT
URL:              http://pypi.python.org/pypi/%{modname}
Source0:          http://pypi.python.org/packages/source/f/%{modname}/%{modname}-%{version}.tar.gz

BuildArch:        noarch
BuildRequires:    python2-devel
BuildRequires:    python-nose
BuildRequires:    python-setuptools
BuildRequires:    python-mccabe >= 0.2
BuildRequires:    python-pep8 >= 1.4.3
BuildRequires:    pyflakes >= 0.6.1
Requires:    python-mccabe >= 0.2
Requires:    python-pep8 >= 1.4.3
Requires:    pyflakes >= 0.6.1
Requires:    python-setuptools
%if %{with python3}
BuildRequires:    python3-devel
BuildRequires:    python3-setuptools
BuildRequires:    python3-nose
BuildRequires:    python3-mccabe >= 0.2
BuildRequires:    python3-pep8 >= 1.4.3
BuildRequires:    python3-pyflakes >= 0.6.1
%endif

%description
Flake8 is a wrapper around these tools:

- PyFlakes - pep8 - Ned's McCabe script

Flake8 runs all tools by launching the single 'flake8' script, but ignores
pep8 and PyFlakes extended options and just uses defaults. It displays the
warnings in a per-file, merged output.

It also adds a few features:

- files that contains with this header are skipped::

# flake8: noqa

- lines that contains a "# NOQA" comment at the end will not issue a
warning. - a Mercurial hook.

- a McCabe complexity checker.


%if %{with python3}
%package -n python3-%{modname}
Summary:        Code checking using pep8 and pyflakes
Group:          Development/Languages

Requires:    python3-setuptools
Requires:    python3-mccabe >= 0.2
Requires:    python3-pep8 >= 1.4.3
Requires:    python3-pyflakes >= 0.6.1

%description -n python3-%{modname}
Flake8 is a wrapper around these tools:

- PyFlakes - pep8 - Ned's McCabe script

Flake8 runs all tools by launching the single 'flake8' script, but ignores
pep8 and PyFlakes extended options and just uses defaults. It displays the
warnings in a per-file, merged output.

It also adds a few features:

- files that contains with this header are skipped::

# flake8: noqa

- lines that contains a "# NOQA" comment at the end will not issue a
warning. - a Mercurial hook.

- a McCabe complexity checker.

This is version of the package running with Python 3.

%endif


%prep
%setup -q -n %{modname}-%{version}

#sed -i -e '/^#!\s*\/.*bin\/.*python/d' flake8/pep8.py
#chmod -x flake8/pep8.py

%if %{with python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'

%endif


%build
%{__python2} setup.py build

%if %{with python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif

%install
unset PYTHONPATH
rm -rf %{buildroot}
# Must do the python3 install first because the scripts in /usr/bin are
# overwritten with every setup.py install (and we want the python2 version
# to be the default for now).
%if %{with python3}
pushd %{py3dir}
    %{__python3} setup.py install -O1 --skip-build --root %{buildroot}
    mv %{buildroot}%{_bindir}/flake8 %{buildroot}%{_bindir}/python3-flake8
popd
%endif

%{__python2} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT


%check
%{__python2} setup.py nosetests --verbosity=2
%if %{with python3}
%{__python3} setup.py nosetests --verbosity=2
%endif

%files
%doc README.rst CONTRIBUTORS.txt

%{_bindir}/%{modname}
%{python_sitelib}/%{modname}*

%if %{with python3}
%files -n python3-%{modname}
%doc README.rst CONTRIBUTORS.txt
%{_bindir}/python3-flake8
%{python3_sitelib}/%{modname}*
%endif


%changelog
* Thu Jan 02 2014 Matthias Runge <mrunge@redhat.com> - 2.0-5
- add missing requires to pep8, python-mccabe and pyflakes (rhbz#1046955)

* Mon Nov 18 2013 Matthias Runge <mrunge@redhat.com> - 2.0-4
- use __python2 instead of __python
- add CONTRIBUTORS.txt to py3 docs

* Tue Nov 05 2013 Matthias Runge <mrunge@redhat.com> - 2.0-3
- minimal spec cleanup, fix one rpmlint warning

* Sat Sep 08 2012 Matej Cepl <mcepl@redhat.com> - 1.4-2
- Update .spec file according to ongoing packaging review.

* Tue Jul 10 2012 Matej Cepl <mcepl@redhat.com> - 1.4-1
- initial package for Fedora

