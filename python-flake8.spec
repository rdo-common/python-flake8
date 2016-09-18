%if 0%{?fedora}
%bcond_without python3
%else
%bcond_with python3
%endif

%global modname flake8

Name:             python-%{modname}
Version:          2.5.5
Release:          2%{?dist}
Summary:          Python code checking using pep8 and pyflakes

License:          MIT
URL:              http://pypi.python.org/pypi/%{modname}
Source0:          https://files.pythonhosted.org/packages/source/f/%{modname}/%{modname}-%{version}.tar.gz

BuildArch:        noarch

%description
Flake8 is a wrapper around PyFlakes, pep8, and Ned's McCabe script. It
runs all the tools by launching the single flake8 script, and displays
the warnings in a per-file, merged output.

It also adds a few features: files that contain "# flake8: noqa" are
skipped, lines that contain a "# noqa" comment at the end will not
issue warnings, Git and Mercurial hooks are included, a McCabe
complexity checker is included, and it is extendable through
flake8.extension entry points.

%package -n python2-%{modname}
Summary:        Python code checking using pep8 and pyflakes

Obsoletes:   python-%{modname} < 2.5.1
%{?python_provide:%python_provide python2-%{modname}}

Requires:    python-mccabe >= 0.2.1
Requires:    python-pep8 >= 1.5.7
Requires:    pyflakes >= 0.8.1
Requires:    python-setuptools

BuildRequires:    python2-devel
BuildRequires:    python-nose
BuildRequires:    python-setuptools
BuildRequires:    python-mccabe >= 0.2.1
BuildRequires:    python-pep8 >= 1.5.7
BuildRequires:    pyflakes >= 0.8.1
BuildRequires:    python-mock

%description -n python2-%{modname}
Flake8 is a wrapper around PyFlakes, pep8, and Ned's McCabe script. It
runs all the tools by launching the single flake8 script, and displays
the warnings in a per-file, merged output.

It also adds a few features: files that contain "# flake8: noqa" are
skipped, lines that contain a "# noqa" comment at the end will not
issue warnings, Git and Mercurial hooks are included, a McCabe
complexity checker is included, and it is extendable through
flake8.extension entry points.

%if %{with python3}
%package -n python3-%{modname}
Summary:        Python code checking using pep8 and pyflakes

%{?python_provide:%python_provide python3-%{modname}}

Requires:    python3-setuptools
Requires:    python3-mccabe >= 0.2.1
Requires:    python3-pep8 >= 1.5.7
Requires:    python3-pyflakes >= 0.6.1

BuildRequires:    python3-devel
BuildRequires:    python3-setuptools
BuildRequires:    python3-nose
BuildRequires:    python3-mccabe >= 0.2.1
BuildRequires:    python3-pep8 >= 1.5.7
BuildRequires:    python3-pyflakes >= 0.8.1
BuildRequires:    python3-mock

%description -n python3-%{modname}
Flake8 is a wrapper around PyFlakes, pep8, and Ned's McCabe script. It
runs all the tools by launching the single flake8 script, and displays
the warnings in a per-file, merged output.

It also adds a few features: files that contain "# flake8: noqa" are
skipped, lines that contain a "# noqa" comment at the end will not
issue warnings, Git and Mercurial hooks are included, a McCabe
complexity checker is included, and it is extendable through
flake8.extension entry points.

This is version of the package running with Python 3.
%endif


%prep
%setup -q -n %{modname}-%{version}

# remove bundled egg-info
rm -r flake8.egg-info

# remove requirements from setup.py, handled by rpm.
sed -i '/"pyflakes.*"/d' setup.py
sed -i '/"pep8.*"/d' setup.py
sed -i '/"mccabe .*"/d' setup.py


%build
%py2_build
%if %{with python3}
%py3_build
%endif


%install
# Must do the python3 install first because the scripts in /usr/bin are
# overwritten with every setup.py install (and we want the python2 version
# to be the default for now).
%if %{with python3}
%py3_install
mv %{buildroot}%{_bindir}/flake8 %{buildroot}%{_bindir}/flake8-3
ln -s flake8-3 %{buildroot}%{_bindir}/flake8-%{python3_version}
ln -s flake8-3 %{buildroot}%{_bindir}/python3-flake8  # backwards compat
%endif
%py2_install
ln -s flake8 %{buildroot}%{_bindir}/flake8-2
ln -s flake8-2 %{buildroot}%{_bindir}/flake8-%{python2_version}


%check
%{__python2} setup.py nosetests --verbosity=2
%{?with_python3:%{__python3} setup.py nosetests --verbosity=2}


%files -n python2-%{modname}
%doc README.rst CONTRIBUTORS.txt
%{_bindir}/flake8
%{_bindir}/flake8-2
%{_bindir}/flake8-%{python2_version}
%{_bindir}/%{modname}
%{python_sitelib}/%{modname}*

%if %{with python3}
%files -n python3-%{modname}
%doc README.rst CONTRIBUTORS.txt
%{_bindir}/flake8-3
%{_bindir}/flake8-%{python3_version}
%{_bindir}/python3-flake8
%{python3_sitelib}/%{modname}*
%endif


%changelog
* Sat Sep 17 2016 Ville Skyttä <ville.skytta@iki.fi>
- Add standard versioned names for executable

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.5-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Jun 15 2016 Ville Skyttä <ville.skytta@iki.fi> - 2.5.5-1
- Update to 2.5.5 (rhbz#1346516)

* Fri Feb 12 2016 Ville Skyttä <ville.skytta@iki.fi> - 2.5.4-1
- Update to 2.5.4 (rhbz#1306870)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Jan 31 2016 Ville Skyttä <ville.skytta@iki.fi> - 2.5.2-1
- Update to 2.5.2 (rhbz#1303383)

* Wed Dec 30 2015 Ville Skyttä <ville.skytta@iki.fi> - 2.5.1-1
- Update to 2.5.1 (rhbz#1289545)
- Update to current Fedora Python packaging guidelines

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Mon Nov 02 2015 Matthias Runge <mrunge@redhat.com> - 2.5.0-1
- update to 2.5.0 (rhbz#1275447)

* Mon Oct 26 2015 Ville Skyttä <ville.skytta@iki.fi> - 2.4.1-3
- Update/improve description

* Mon Jul 06 2015 Matthias Runge <mrunge@redhat.com> - 2.4.1-2
- fix FTBFS (rhbz#1239837)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu May 21 2015 Matej Cepl <mcepl@redhat.com> - 2.4.1-1
- update to 2.4.1 (rhbz#1178814)

* Mon Oct 20 2014 Matthias Runge <mrunge@redhat.com> - 2.2.5-1
- update to 2.2.5 (rhbz#1132878)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Wed Apr 09 2014 Matthias Runge <mrunge@redhat.com> - 2.1.0-1
- update to 2.1.0

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

