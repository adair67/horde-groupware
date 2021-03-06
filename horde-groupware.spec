# TODO
# - lighttpd support
# - make it use system Kronolith, Turba, Nag and Mnemo.
# - system PEAR packages
#   instead of the bundled ones.
%define	_hordeapp groupware
#define	_snap	2005-08-01
%define	_rc		rc1
%define	_rel	0.1
%include	/usr/lib/rpm/macros.php
Summary:	Browser based collaboration suite
Summary(pl.UTF-8):	Oparte na przeglądarce narzędzie do pracy grupowej
Name:		horde-%{_hordeapp}
Version:	1.2
Release:	%{?_rc:0.%{_rc}.}%{?_snap:0.%(echo %{_snap} | tr -d -).}%{_rel}
License:	GPL v2
Group:		Applications/WWW
#Source0:	ftp://ftp.horde.org/pub/horde-groupware/horde-groupware-%{version}.tar.gz
Source0:	http://ftp.horde.org/pub/horde-groupware/horde-groupware-%{version}-%{_rc}.tar.gz
# Source0-md5:	5d6dcc1855277a099762943ad3fedc8f
#Source1:	%{name}.conf
#Patch0: %{name}-prefs.patch
URL:		http://horde.org/groupware/
BuildRequires:	rpm-php-pearprov >= 4.0.2-98
BuildRequires:	rpmbuild(macros) >= 1.264
BuildRequires:	tar >= 1:1.15.1
Requires:	apache(mod_access)
#Requires:	horde >= 3.0
Requires:	webapps
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoreq	'pear(Horde.*)'

%define		hordedir	/usr/share/horde
#define		_appdir		%{hordedir}/%{_hordeapp}
%define		_appdir		%{_datadir}/%{_hordeapp}
%define		_webapps	/etc/webapps
%define		_webapp		horde-%{_hordeapp}
%define		_sysconfdir	%{_webapps}/%{_webapp}

%description
Horde Groupware is a free, enterprise ready, browser based
collaboration suite. Users can manage and share calendars, contacts,
tasks and notes with the standards compliant components from the Horde
Project.

Horde Groupware bundles the separately available applications
Kronolith, Turba, Nag and Mnemo.

The Horde Project writes web applications in PHP and releases them
under the GNU Public License. For more information (including help
with Webmail) please visit <http://www.horde.org/>.

%description -l pl.UTF-8
Horde Groupware Webmail Edition to darmowe, gotowe do zastosowań
produkcyjnych narzędzie do pracy grupowej. Użytkownicy mogą zarządzać
i współdzielić kalendarze, kontakty, zadania i notatki przy użyciu
zgodnych ze standardem komponentów z projektu Horde.

Horde Groupware jest opakowaniem aplikacji dostępnych samodzielnie:
Kronolith, Turba, Nag i Mnemo.

Projekt Horde tworzy aplikacje WWW w PHP i wydaje je na licencji GNU
General Public License. Więcej informacji (włącznie z pomocą dla
Webmail) można znaleźć na stronie <http://www.horde.org/>.

%prep
%setup -qcT -n %{?_snap:%{_hordeapp}-%{_snap}}%{!?_snap:%{_hordeapp}-%{version}%{?_rc:-%{_rc}}}
tar zxf %{SOURCE0} --strip-components=1

rm -f {,*/}.htaccess
for i in config/*.dist; do
	mv $i config/$(basename $i .dist)
done
# considered harmful (horde/docs/SECURITY)
rm test.php

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir}/docs}

cp -a *.php $RPM_BUILD_ROOT%{_appdir}
cp -a config/* $RPM_BUILD_ROOT%{_sysconfdir}
echo '<?php ?>' > $RPM_BUILD_ROOT%{_sysconfdir}/conf.php
touch $RPM_BUILD_ROOT%{_sysconfdir}/conf.php.bak
cp -a lib locale templates themes $RPM_BUILD_ROOT%{_appdir}
cp -a docs/CREDITS $RPM_BUILD_ROOT%{_appdir}/docs

ln -s %{_sysconfdir} $RPM_BUILD_ROOT%{_appdir}/config
%if 0
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ ! -f %{_sysconfdir}/conf.php.bak ]; then
	install /dev/null -o root -g http -m660 %{_sysconfdir}/conf.php.bak
fi

%if 0
%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}
%endif

%files
%defattr(644,root,root,755)
%doc README docs/* scripts
%dir %attr(750,root,http) %{_sysconfdir}
%if 0
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%endif
%attr(660,root,http) %config(noreplace) %{_sysconfdir}/conf.php
%attr(660,root,http) %config(noreplace) %ghost %{_sysconfdir}/conf.php.bak
%attr(640,root,http) %config(noreplace) %{_sysconfdir}/[!c]*.php
%attr(640,root,http) %{_sysconfdir}/conf.xml

%dir %{_appdir}
%{_appdir}/*.php
%{_appdir}/config
%{_appdir}/docs
%{_appdir}/lib
%{_appdir}/locale
%{_appdir}/templates
%{_appdir}/themes
