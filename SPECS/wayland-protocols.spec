%global _hardened_build 1
%global debug_package %{nil}

Name:           wayland-protocols
Version:        1.32
Release:        1%{?dist}
Summary:        Wayland protocols that add functionality not available in the core protocol

License:        MIT
URL:            https://wayland.freedesktop.org/
Source0:        https://gitlab.freedesktop.org/wayland/%{name}/-/releases/%{version}/downloads/%{name}-%{version}.tar.xz

BuildRequires:  gcc
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  pkgconfig
BuildRequires:  wayland-devel

%description
wayland-protocols contains Wayland protocols that add functionality not
available in the Wayland core protocol. Such protocols either add
completely new functionality, or extend the functionality of some other
protocol either in Wayland core, or some other protocol in
wayland-protocols.

%package devel
Summary:        Wayland protocols that add functionality not available in the core protocol
Requires:       pkgconfig

%description devel
wayland-protocols contains Wayland protocols that add functionality not
available in the Wayland core protocol.

%prep
%autosetup -p1

%build
%meson
%meson_build

%install
%meson_install

%files devel
%license COPYING
%doc README.md
%{_datadir}/pkgconfig/wayland-protocols.pc
%{_datadir}/wayland-protocols/

%changelog
* Sun Dec 15 2024 Your Name <your.email@domain.com> - 1.32-1
- Initial build for headless container support
- Disabled debug package generation
