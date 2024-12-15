%global _hardened_build 1
%global debug_package %{nil}

Name:           libseat
Version:        0.8.0
Release:        1%{?dist}
Summary:        Seat management library

License:        MIT
URL:            https://git.sr.ht/~kennylevinsen/seatd
Source0:        https://git.sr.ht/~kennylevinsen/seatd/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  pkgconfig
BuildRequires:  systemd-devel

%description
libseat is a universal seat management library that allows applications
to use whatever seat management is available on the system.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconfig

%description devel
Development files for %{name}.

%prep
%autosetup -p1 -n seatd-%{version}

%build
%meson \
    -Dexamples=disabled \
    -Dserver=disabled \
    -Dlibseat-logind=systemd \
    -Dman-pages=disabled
%meson_build

%install
%meson_install

%files
%license LICENSE
%{_libdir}/libseat.so.*

%files devel
%{_includedir}/libseat.h
%{_libdir}/libseat.so
%{_libdir}/pkgconfig/libseat.pc

%changelog
* Sun Dec 15 2024 Your Name <your.email@domain.com> - 0.8.0-1
- Initial minimal build for container support
