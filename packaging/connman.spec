%bcond_with     connman_openconnect
%bcond_with     connman_ntp

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
BuildRequires:  pkgconfig(gnutls)
%if %{with connman_openconnect}
BuildRequires:  openconnect
%endif
BuildRequires:  readline-devel
%systemd_requires

%description
Connection Manager provides a daemon for managing Internet connections
within embedded devices running the Linux operating system.

%if %{with connman_openconnect}
%package plugin-openconnect
Summary:        Openconnect Support for Connman
Requires:       %{name} = %{version}
Requires:       openconnect

%description plugin-openconnect
Openconnect Support for Connman.
%endif

%package test
Summary:        Test Scripts for Connection Manager
Requires:       %{name} = %{version}
Requires:       dbus-python
Requires:       python-gobject
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
./bootstrap
%configure \
            --enable-threads \
            --enable-client \
            --enable-pacrunner \
            --enable-wifi=builtin \
%if %{with connman_openconnect}
            --enable-openconnect \
%endif
            --enable-test \
            --with-systemdunitdir=%{_unitdir}

make %{?_smp_mflags}

%install
%make_install

%if %{with connman_ntp}
mkdir -p %{buildroot}/usr/lib/systemd/ntp-units.d
install -m644 %{SOURCE10} %{buildroot}/usr/lib/systemd/ntp-units.d
install -m644 %{SOURCE11} %{buildroot}%{_unitdir}
%install_service network.target.wants connman-ntp.service
%install_service multi-user.target.wants connman-ntp.service
%endif

%install_service network.target.wants connman.service
%install_service multi-user.target.wants connman.service

%docs_package

%files
%license COPYING
%manifest connman.manifest
%{_sbindir}/*
%{_libdir}/connman/plugins/*.so
%config %{_sysconfdir}/dbus-1/system.d/*
%{_unitdir}/connman.service
%{_unitdir}/network.target.wants/connman.service
%{_unitdir}/multi-user.target.wants/connman.service
%if %{with connman_ntp}
%dir /usr/lib/systemd/ntp-units.d
%{_unitdir}/connman-ntp.service
%{_unitdir}/multi-user.target.wants/connman-ntp.service
%{_unitdir}/network.target.wants/connman-ntp.service
/usr/lib/systemd/ntp-units.d/40-connman-ntp.list
%endif

%files test
%{_libdir}/%{name}/test/*

%files devel
%{_includedir}/connman/*.h
%{_libdir}/pkgconfig/*.pc

%if %{with connman_openconnect}
%files plugin-openconnect
%{_unitdir}/connman-vpn.service
%{_libdir}/connman/plugins-vpn/openconnect.so
%{_libdir}/connman/scripts/openconnect-script
%{_datadir}/dbus-1/system-services/net.connman.vpn.service
%endif

%changelog
