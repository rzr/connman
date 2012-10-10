Name:           connman
Version:        1.15
Release:        1
License:        GPL-2.0
Summary:        Connection Manager
Url:            http://connman.net
Group:          Connectivity/Connection Management
Source0:        %{name}-%{version}.tar.xz
Source10:       40-connman-ntp.list
Source11:       connman-ntp.service
Source1001:     connman.manifest
BuildRequires:  systemd
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(libiptc)
BuildRequires:  pkgconfig(xtables)
BuildRequires:	pkgconfig(gnutls) 
BuildRequires:  openconnect
BuildRequires:  readline-devel
%systemd_requires

%description
Connection Manager provides a daemon for managing Internet connections
within embedded devices running the Linux operating system.

%package plugin-openconnect
Summary:        Openconnect Support for Connman
Group:          Connectivity/Connection Management
Requires:       %{name} = %{version}
Requires:       openconnect

%description plugin-openconnect
Openconnect Support for Connman.

%package test
Summary:        Test Scripts for Connection Manager
Group:          Development/Testing
Requires:       %{name} = %{version}
Requires:       dbus-python
Requires:       python-gobject
Requires:       python-xml

%description test
Scripts for testing Connman and its functionality

%package devel
Summary:        Development Files for connman
Group:          Development/Tools
Requires:       %{name} = %{version}

%description devel
Header files and development files for connman.

%prep
%setup -q
cp %{SOURCE10} .
cp %{SOURCE11} .
cp %{SOURCE1001} .

%build
./bootstrap
%configure \
            --enable-threads \
            --enable-client \
            --enable-pacrunner \
            --enable-wifi=builtin \
            --enable-openconnect \
%if 0%{?enable_connman_features}
            %connman_features \
%endif
            --enable-test \
            --with-systemdunitdir=%{_unitdir}

make %{?_smp_mflags}

%install
%make_install

mkdir -p %{buildroot}/usr/lib/systemd/ntp-units.d
install -m644 40-connman-ntp.list %{buildroot}/usr/lib/systemd/ntp-units.d
install -m644 connman-ntp.service %{buildroot}%{_unitdir}

%install_service network.target.wants connman.service
%install_service network.target.wants connman-ntp.service
%install_service multi-user.target.wants connman.service
%install_service multi-user.target.wants connman-ntp.service

%docs_package 

%files
%license COPYING
%manifest connman.manifest
%{_sbindir}/*
%{_libdir}/connman/plugins/*.so
%{_datadir}/man/*
%config %{_sysconfdir}/dbus-1/system.d/*
%{_unitdir}/connman.service
%{_unitdir}/network.target.wants/connman.service
%{_unitdir}/multi-user.target.wants/connman.service
%{_unitdir}/connman-ntp.service
%{_unitdir}/multi-user.target.wants/connman-ntp.service
%{_unitdir}/network.target.wants/connman-ntp.service
%dir /usr/lib/systemd/ntp-units.d
/usr/lib/systemd/ntp-units.d/40-connman-ntp.list

%files test
%{_libdir}/%{name}/test/*

%files devel
%{_includedir}/connman/*.h
%{_libdir}/pkgconfig/*.pc

%files plugin-openconnect
%{_unitdir}/connman-vpn.service
%{_libdir}/connman/plugins-vpn/openconnect.so
%{_libdir}/connman/scripts/openconnect-script
%{_datadir}/dbus-1/system-services/net.connman.vpn.service

%changelog
