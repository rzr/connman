Name:           connman
Version:        1.9
Release:        1
License:        GPL-2.0
Summary:        Connection Manager
Url:            http://connman.net
Group:          System/Networking
Source0:        %{name}-%{version}.tar.xz
Source1001:     packaging/connman.manifest
Patch0:		dbus.patch
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(libiptc)
BuildRequires:  pkgconfig(xtables)
BuildRequires:	pkgconfig(gnutls) 
BuildRequires:  readline-devel
Requires:       systemd
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd

%description
Connection Manager provides a daemon for managing Internet connections
within embedded devices running the Linux operating system.

%package test
Summary:        Test Scripts for Connection Manager
Group:          Development/Tools
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
%patch0 -p1


%build
cp %{SOURCE1001} .
./bootstrap
%configure \
            --enable-threads \
            --enable-wifi=builtin \
%if 0%{?enable_connman_features}
            %connman_features \
%endif
            --enable-test \
            --with-systemdunitdir=%{_unitdir}

make %{?_smp_mflags}

%install
%make_install

mkdir -p %{buildroot}%{_unitdir}/network.target.wants
ln -s ../connman.service %{buildroot}%{_unitdir}/network.target.wants/connman.service

%install_service multi-user.target.wants connman.service

%files
%manifest connman.manifest
%{_sbindir}/*
#%{_libdir}/connman/plugins/*.so
#%{_datadir}/dbus-1/services/*
%{_sysconfdir}/dbus-1/system.d/*
#%{_sysconfdir}/connman/main.conf
#%{_sysconfdir}/dbus-1/system.d/*.conf
%{_unitdir}/connman.service
%{_unitdir}/network.target.wants/connman.service
%{_unitdir}/multi-user.target.wants/connman.service
%files test
%{_libdir}/%{name}/test/*


%files devel
%{_includedir}/connman/*.h
%{_libdir}/pkgconfig/*.pc
