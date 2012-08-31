Name:       connman
Summary:    Connection Manager
Version:    1.0
Release:    1
Group:      System/Networking
License:    GPLv2
URL:        http://connman.net/
Source0:    %{name}-%{version}.tar.bz2
Source1:    settings
Source2:    main.conf
Requires:   dbus
Requires:   wpa_supplicant >= 0.7.1
Requires:   bluez
Requires:   ofono
Requires:   systemd
Requires(post):   systemd 
Requires(preun):  systemd
Requires(postun): systemd
BuildRequires:  pkgconfig(libiptc)
BuildRequires:  pkgconfig(xtables)
%ifarch %{ix86}
##BuildRequires:  pkgconfig(libiWmxSdk-0)
%endif
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(libudev) >= 145
##BuildRequires:  openconnect
##BuildRequires:  openvpn
BuildRequires:  iptables-devel
BuildRequires:  pkgconfig(gnutls)


%description
Connection Manager provides a daemon for managing Internet connections
within embedded devices running the Linux operating system.



%package devel
Summary:    Development files for Connection Manager
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
connman-devel contains development files for use with connman.

#%package iwmxsdk
#Summary:    ConnMan plugin for the Intel WiMAX Network Service
#Group:      System/Networking
#Requires:   %{name} = %{version}-%{release}
#Requires:   WiMAX-Network-Service
#
#%description iwmxsdk
#This plugin allows connman to work with WiMAX devices controlled by
#the Intel WiMAX Network Service


%package test
Summary:    Test Scripts for Connection Manager
Group:      Development/Tools
Requires:   %{name} = %{version}-%{release}
Requires:   dbus-python
Requires:   pygobject
Requires:   python-xml

%description test
Scripts for testing Connman and its functionality


%prep
%setup -q -n %{name}-%{version}

%build
%configure --disable-static \
    --enable-ethernet=builtin \
    --enable-wifi=builtin \
    --enable-ofono=builtin \
    --enable-bluetooth=builtin \
    --enable-loopback=builtin \
    --enable-threads \
    --enable-test \
    --with-systemdunitdir=/usr/lib/systemd/system
# disabled for now:
%ifarch %{ix86}
##    --enable-iwmx \
%endif
##    --enable-openconnect=builtin \
##    --enable-openvpn=builtin \

make %{?jobs:-j%jobs}

%install
mkdir -p %{buildroot}%{_sysconfdir}/connman
install -D -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/connman/main.conf

mkdir -p %{buildroot}/usr/lib/systemd/system/network.target.wants
ln -s ../connman.service %{buildroot}/usr/lib/systemd/system/network.target.wants/connman.service

%make_install

install -d -m 700 %{buildroot}/var/lib/connman
install -c -m 600 %{SOURCE1} %{buildroot}/var/lib/connman/settings

%post
systemctl daemon-reload
systemctl restart connman.service
 
%preun
systemctl stop connman.service
 
%postun
systemctl daemon-reload



%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING INSTALL ChangeLog NEWS README
%{_sbindir}/*
#%{_libdir}/%{name}/scripts/*
%config %{_sysconfdir}/dbus-1/system.d/*.conf
%config %{_sysconfdir}/connman/*.conf
/usr/lib/systemd/system/connman.service
/usr/lib/systemd/system/network.target.wants/connman.service
/var/lib/connman/settings


%files devel
%defattr(-,root,root,-)
%doc AUTHORS COPYING INSTALL
%{_includedir}/%{name}/*.h
%{_libdir}/pkgconfig/*.pc

#%files iwmxsdk
#%defattr(-,root,root,-)
#%ifarch %{ix86}
#%{_libdir}/%{name}/plugins/iwmxsdk.so
#%doc COPYING README INSTALL
#%endif

%files test
%defattr(-,root,root,-)
%{_libdir}/%{name}/test/*
