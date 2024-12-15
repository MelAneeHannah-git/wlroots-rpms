%global _hardened_build 1
%global majorversion 0.17
%global debug_package %{nil}

Name:           wlroots
Version:        0.17.1
Release:        1%{?dist}
Summary:        Modular Wayland compositor library (Headless Build)

License:        MIT
URL:            https://gitlab.freedesktop.org/wlroots/wlroots
Source0:        %{url}/-/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  meson >= 0.58.1
BuildRequires:  ninja-build
BuildRequires:  pkgconfig(libdrm) >= 2.4.113
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols) >= 1.31
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  pkgconfig(wayland-server) >= 1.21
BuildRequires:  pkgconfig(vulkan)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(libinput) >= 1.14.0
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  systemd-devel
BuildRequires:  xorg-x11-server-Xwayland-devel

%description
wlroots is a modular Wayland compositor library that provides backends,
renderers, and features needed to implement a Wayland compositor.
This build is optimized for headless container usage with NVIDIA GPU support.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Development files for %{name}.

%prep
%autosetup -p1

%build
%meson \
    -Dxwayland=enabled \
    -Drenderers=vulkan \
    -Dbackends=drm \
    -Dxcb-errors=disabled \
    -Dexamples=false \
    -Dwerror=false \
    -Dallocators=gbm \
    -Dx11-backend=disabled \
    -Drdp-backend=disabled \
    -Dlibseat=disabled
%meson_build

%install
%meson_install

%files
%license LICENSE
%doc README.md
%{_libdir}/lib%{name}.so.*

%files devel
%{_includedir}/wlr
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Sat Dec 14 2024 Your Name <your.email@domain.com> - 0.17.1-1
- Initial headless package optimized for container usage with NVIDIA GPU support
- Disabled libseat dependency for headless operation
- Fixed meson renderer syntax
