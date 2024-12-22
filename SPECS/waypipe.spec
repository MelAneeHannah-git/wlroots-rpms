Name:           waypipe
Version:        0.9.2
Release:        1%{?dist}
Summary:        A network transparency daemon for Wayland
License:        MIT
URL:            https://gitlab.freedesktop.org/mstoeckl/waypipe
Source0:        %{url}/-/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  meson >= 0.47.0
BuildRequires:  ninja-build
BuildRequires:  pkgconfig
BuildRequires:  wlroots-devel >= 0.17.1
BuildRequires:  wayland-devel >= 1.22.0
BuildRequires:  wayland-protocols-devel >= 1.32
BuildRequires:  libdrm-devel
BuildRequires:  mesa-libgbm-devel
BuildRequires:  libzstd-devel
BuildRequires:  systemtap-sdt-devel
BuildRequires:  lz4-devel

Requires:       wlroots >= 0.17.1
Requires:       wayland >= 1.22.0
Requires:       libdrm
Requires:       mesa-libgbm
Requires:       libzstd
Requires:       lz4

%description
Waypipe is a proxy for Wayland clients, with the aim of supporting behavior
analogous to ssh -X. In conjunction with a general-purpose compression
program, like lz4, zstd, or others, it can optimize the amount of data
transmitted over the remote connection.

This build includes DMABUF and ZSTD support, and is optimized for headless
container usage with NVIDIA GPU support.

%prep
%autosetup -n waypipe-v%{version}-db328a8984382a4b985c4e4a3b69b11ad1e078a0 -p1

%build
%meson \
    -Dwith_dmabuf=auto \
    -Dwith_vaapi=disabled \
    -Dwith_video=disabled \
    -Dwith_systemtap=true \
    -Dbuild_c=true \
    -Dbuild_rs=false

%meson_build

%install
%meson_install

%files
%license COPYING
%doc README.md CONTRIBUTING.md
%{_bindir}/waypipe
%{_mandir}/man1/waypipe.1*

%changelog
* Mon Dec 16 2024 Builder <builder@example.com> - 0.9.2-1
- Initial package build with headless container support
- Enabled DMABUF and ZSTD support
- Built with C implementation (not Rust)
- Configured for NVIDIA GPU support
- Based on verified build configuration
- Added lz4 support
