# Review Request: http://bugzilla.redhat.com/432139

Name:           kiconedit
Version:        4.3.3
Release:        1%{?dist}
Summary:        An icon editor

Group:          Applications/Publishing
License:        GPLv2+
URL:            http://www.kde.org
Source0:        ftp://ftp.kde.org/pub/kde/stable/%{version}/src/extragear/%{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  kdelibs4-devel >= 4
BuildRequires:  cmake
BuildRequires:  desktop-file-utils
BuildRequires:  gettext

%{?_kde4_macros_api:Requires: kde4-macros(api) = %{_kde4_macros_api} }
Requires: kdelibs4 >= %{version}

%description
KIconEdit is designed to help create icons for 
KDE using the standard icon palette.


%prep
%setup -q


%build

mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde4} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
rm -rf %{buildroot}

make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

%find_lang %{name}
HTML_DIR=$(kde4-config --expandvars --install html)
if [ -d %{buildroot}${HTML_DIR} ]; then
for lang_dir in %{buildroot}${HTML_DIR}/* ; do
  if [ -d ${lang_dir} ]; then
    lang=$(basename ${lang_dir})
    echo "%lang(${lang}) ${HTML_DIR}/${lang}/%{name}/" >> %{name}.lang
  fi
done
fi


%check
desktop-file-validate %{buildroot}%{_datadir}/applications/kde4/%{name}.desktop


%clean
rm -rf %{buildroot}


%post
touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
  update-desktop-database -q &> /dev/null
  touch --no-create %{_datadir}/icons/hicolor &> /dev/null
  gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
fi

%posttrans
update-desktop-database -q &> /dev/null
gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING COPYING.DOC NEWS
%{_kde4_bindir}/kiconedit
%{_kde4_appsdir}/kiconedit/
%{_kde4_datadir}/applications/kde4/kiconedit.desktop
%{_kde4_iconsdir}/hicolor/*/*/*


%changelog
* Thu Nov 05 2009 Sebastian Vahl <svahl@fedoraproject.org> - 4.3.3-1
- 4.3.3

* Tue Sep 01 2009 Sebastian Vahl <svahl@fedoraproject.org> - 4.3.1-1
- 4.3.1

* Tue Aug 04 2009 Than Ngo <than@redhat.com> - 4.3.0-1
- 4.3.0

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun 10 2009 Sebastian Vahl <fedora@deadbabylon.de> 4.2.4-1
- 4.2.4

* Mon May 11 2009 Rex Dieter <rdieter@fedoraproject.org> 4.2.3-2
- fix %%_docdir/HTML/<lang> ownership

* Fri May 08 2009 Rex Dieter <rdieter@fedoraproject.org> 4.2.3-1
- 4.2.3
- optimize scriptlets

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 23 2009 Than Ngo <than@redhat.com> - 4.2.0-1
- 4.2.0

* Mon Nov 17 2008 Rex Dieter <rdieter@fedoraproject.org> 4.1.3-2
- scriptlet, dependency fixes

* Sun Nov 09 2008 Sebastian Vahl <fedora@deadbabylon.de> 4.1.3-1
- 4.1.3

* Fri Oct 03 2008 Rex Dieter <rdieter@fedoraproject.org> 4.1.2-1
- 4.1.2

* Fri Aug 29 2008 Than Ngo <than@redhat.com> 4.1.1-1
- 4.1.1

* Thu Aug 28 2008 Sebastian Vahl <fedora@deadbabylon.de> 4.1.0-1
- 4.1 (final)

* Mon May 26 2008 Than Ngo <than@redhat.com> 4.0.80-1
- 4.1 beta 1

* Thu Apr 03 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0.3-2
- rebuild (again) for the fixed %%{_kde4_buildtype}

* Mon Mar 31 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0.3-1
- update to 4.0.3
- rebuild for NDEBUG and _kde4_libexecdir

* Tue Mar 04 2008 Sebastian Vahl <fedora@deadbabylon.de> 4.0.2-1
- new upstream version: 4.0.2

* Thu Feb 14 2008 Sebastian Vahl <fedora@deadbabylon.de> 4.0.1-2
- remove reference to KDE 4 in summary

* Fri Feb 08 2008 Sebastian Vahl <fedora@deadbabylon.de> 4.0.1-1
- new upstream version: 4.0.1

* Fri Jan 25 2008 Sebastian Vahl <fedora@deadbabylon.de> 4.0.0-1
- Initial version of kde-4.0.0 version
