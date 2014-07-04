Name:           connman
Version:        1.24
Release:        1
License:        GPL-2.0
Summary:        Connection Manager
Url:            http://connman.net
Group:          Network & Connectivity/Connection Management
Source0:        %{name}-%{version}.tar.gz
Source1001:     connman.manifest
BuildRequires: 	systemd
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(libiptc)
BuildRequires:  pkgconfig(xtables)
BuildRequires:  pkgconfig(gnutls)
BuildRequires:  readline-devel
%systemd_requires
Requires:       iptables

%description
Connection Manager provides a daemon for managing Internet connections
within embedded devices running the Linux operating system.

%package test
Summary:        Test Scripts for Connection Manager
Requires:       %{name} = %{version}
Requires:       dbus-python
Requires:       pygobject
Requires:       python-xml

%description test
Scripts for testing Connman and its functionality

%package devel
Summary:        Development Files for connman
Requires:       %{name} = %{version}

%description devel
Header files and development files for connman.

%prep
%setup -q
cp %{SOURCE1001} .

%build
CFLAGS+=" -DTIZEN_EXT"

chmod +x bootstrap
./bootstrap
%configure \
            --enable-threads \
            --enable-client \
            --enable-pacrunner \
            --enable-wifi=builtin \
            --enable-test \
            --enable-loopback \
            --enable-ethernet \
            --with-systemdunitdir=%{_unitdir}

make %{?_smp_mflags}

%install
%make_install

mkdir -p %{buildroot}%{_sysconfdir}/connman
cp src/main.conf %{buildroot}%{_sysconfdir}/connman/main.conf

%install_service network.target.wants connman.service
%install_service multi-user.target.wants connman.service

%post
systemctl daemon-reload
systemctl restart connman.service

%preun
systemctl stop connman.service

%postun
systemctl daemon-reload

%docs_package

%files
%manifest %{name}.manifest
%license COPYING
%{_sbindir}/*
%config %{_sysconfdir}/connman/main.conf
%config %{_sysconfdir}/dbus-1/system.d/*
%{_unitdir}/connman.service
%{_unitdir}/network.target.wants/connman.service
%{_unitdir}/multi-user.target.wants/connman.service

%files test
%manifest %{name}.manifest
%{_libdir}/%{name}/test/*

%files devel
%manifest %{name}.manifest
%{_includedir}/connman/*.h
%{_libdir}/pkgconfig/*.pc

%changelog
