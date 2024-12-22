%global _hardened_build 1

Name:           wayland
Version:        1.22.0
Release:        1%{?dist}
Summary:        Wayland Compositor Infrastructure
License:        MIT
URL:            https://wayland.freedesktop.org/
Source0:        %{url}/releases/%{name}-%{version}.tar.xz

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  expat-devel
BuildRequires:  libffi-devel
BuildRequires:  libxml2-devel
BuildRequires:  pkgconfig

%description
Wayland is a protocol for a compositor to talk to its clients.
This build is optimized for headless container usage.

# Client package
%package client
Summary:        Wayland client library
Provides:       libwayland-client = %{version}-%{release}
Provides:       libwayland-client%{?_isa} = %{version}-%{release}
Conflicts:      libwayland-client < %{version}-%{release}
%description client
Library for implementing Wayland clients.

# Cursor package
%package cursor
Summary:        Wayland cursor library
Provides:       libwayland-cursor = %{version}-%{release}
Provides:       libwayland-cursor%{?_isa} = %{version}-%{release}
Conflicts:      libwayland-cursor < %{version}-%{release}
Requires:       %{name}-client%{?_isa} = %{version}-%{release}
%description cursor
Libraries for handling cursors in Wayland clients.

# EGL package
%package egl
Summary:        Wayland EGL library
Provides:       libwayland-egl = %{version}-%{release}
Provides:       libwayland-egl%{?_isa} = %{version}-%{release}
Conflicts:      libwayland-egl < %{version}-%{release}
Requires:       %{name}-client%{?_isa} = %{version}-%{release}
%description egl
Libraries for handling EGL in Wayland clients.

# Server package
%package server
Summary:        Wayland server library
Provides:       libwayland-server = %{version}-%{release}
Provides:       libwayland-server%{?_isa} = %{version}-%{release}
Conflicts:      libwayland-server < %{version}-%{release}
%description server
Library for implementing Wayland servers.

# Development package
%package devel
Summary:        Development files for %{name}
Requires:       %{name}-client%{?_isa} = %{version}-%{release}
Requires:       %{name}-cursor%{?_isa} = %{version}-%{release}
Requires:       %{name}-egl%{?_isa} = %{version}-%{release}
Requires:       %{name}-server%{?_isa} = %{version}-%{release}
Requires:       pkgconfig
%description devel
Development files for %{name}.

%prep
%autosetup -n %{name}-%{version} -p1

%build
%meson \
    -Dlibraries=true \
    -Dscanner=true \
    -Dtests=false \
    -Ddocumentation=false \
    -Ddtd_validation=false

%meson_build

%install
%meson_install

%files server
%license COPYING
%{_libdir}/libwayland-server.so.*

%files client
%license COPYING
%{_libdir}/libwayland-client.so.*

%files cursor
%license COPYING
%{_libdir}/libwayland-cursor.so.*

%files egl
%license COPYING
%{_libdir}/libwayland-egl.so.*

%files devel
%{_bindir}/wayland-scanner
%{_includedir}/wayland-*.h
%{_libdir}/libwayland-*.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/aclocal/wayland-scanner.m4
%dir %{_datadir}/wayland
%{_datadir}/wayland/wayland-scanner.mk
%{_datadir}/wayland/wayland.dtd
%{_datadir}/wayland/wayland.xml

%changelog
* Mon Dec 17 2024 Builder <builder@example.com> - 1.22.0-1
- Added proper Provides declarations for system compatibility
- Split packages with proper dependencies
- Optimized for headless container usage
