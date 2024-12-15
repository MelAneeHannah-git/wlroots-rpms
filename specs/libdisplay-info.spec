%global _hardened_build 1
%global debug_package %{nil}

Name:           libdisplay-info
Version:        0.1.1
Release:        1%{?dist}
Summary:        EDID and DisplayID library

License:        MIT
URL:            https://gitlab.freedesktop.org/emersion/libdisplay-info
Source0:        %{url}/-/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  pkgconfig
BuildRequires:  hwdata-devel

%description
A library for parsing EDID and DisplayID.

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
    -Dexamples=false \
    -Dtests=false
%meson_build

%install
%meson_install

%files
%license LICENSE
%{_bindir}/di-edid-decode
%{_libdir}/libdisplay-info.so.*

%files devel
%{_includedir}/libdisplay-info
%{_libdir}/libdisplay-info.so
%{_libdir}/pkgconfig/libdisplay-info.pc

%changelog
* Sun Dec 15 2024 Your Name <your.email@domain.com> - 0.1.1-1
- Initial minimal build for container support
- Added di-edid-decode binary to files section
