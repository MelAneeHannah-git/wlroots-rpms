%global _hardened_build 1

Name:           pixman
Version:        0.42.2
Release:        1%{?dist}
Summary:        Pixel manipulation library

License:        MIT
URL:            http://cgit.freedesktop.org/pixman/
Source0:        https://www.cairographics.org/releases/%{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  pkgconfig

%description
Pixman is a pixel manipulation library for X and Cairo.

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
    -Dgtk=disabled \
    -Dlibpng=disabled \
    -Dtests=disabled \
    -Dtimers=false \
    -Dgnuplot=false \
    -Dloongson-mmi=disabled \
    -Dmmx=disabled \
    -Dsse2=disabled \
    -Dssse3=disabled \
    -Dvmx=disabled \
    -Darm-simd=disabled \
    -Dneon=disabled \
    -Da64-neon=disabled \
    -Diwmmxt=disabled \
    -Dmips-dspr2=disabled \
    -Dgnu-inline-asm=disabled \
    -Dtls=disabled \
    -Dopenmp=disabled
%meson_build

%install
%meson_install

%files
%license COPYING
%{_libdir}/libpixman-1.so.*

%files devel
%{_includedir}/pixman-1
%{_libdir}/libpixman-1.so
%{_libdir}/pkgconfig/pixman-1.pc

%changelog
* Sun Dec 15 2024 Your Name <your.email@domain.com> - 0.42.2-1
- Initial minimal build for headless container support
- Disabled all CPU-specific optimizations
