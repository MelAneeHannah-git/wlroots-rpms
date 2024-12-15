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

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconfig

%description devel
Development files for %{name}.

%prep
%autosetup -p1

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

%files
%license COPYING
%{_libdir}/libwayland-*.so.*

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
* Sun Dec 15 2024 Your Name <your.email@domain.com> - 1.22.0-1
- Initial minimal build for headless container support
- Added proper pkgconfig file handling

