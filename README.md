# Custom Headless Wlroots RPM Build

This repository contains custom-built RPMs for wlroots and its dependencies, optimized for headless container usage with NVIDIA GPU support.

## Components

All RPMs are built for AlmaLinux 9:

- `wayland-1.22.0`
- `wayland-protocols-1.32`
- `pixman-0.42.2` (with CPU-specific optimizations disabled)
- `libseat-0.8.0`
- `libdisplay-info-0.1.1`
- `wlroots-0.17.1`

## Build Order

Dependencies must be installed in this order:

1. wayland
2. pixman
3. wayland-protocols
4. libseat
5. libdisplay-info
6. wlroots

## Features

- Optimized for headless operation
- NVIDIA GPU support
- Xwayland support enabled
- Minimal build with unnecessary features disabled
- CPU-specific optimizations disabled for container compatibility

## Build Options

### Wayland
- Minimal build with core functionality
- Debug packages disabled

### Pixman
- All CPU-specific optimizations disabled
- Tests and documentation disabled
- GTK demos disabled

### Wayland-protocols
- Minimal installation with required protocols

### Libseat
- Systemd logind support
- Server component disabled
- Examples disabled

### Libdisplay-info
- Examples and tests disabled

### Wlroots
- DRM backend enabled
- Vulkan renderer enabled
- X11 backend disabled
- RDP backend disabled
- Libseat support disabled

## Source Specs

The `specs` directory contains all spec files used to build these RPMs.

## Usage

```bash
# Install in order:
sudo rpm -ivh wayland-1.22.0-1.el9.x86_64.rpm wayland-devel-1.22.0-1.el9.x86_64.rpm
sudo rpm -ivh pixman-0.42.2-1.el9.x86_64.rpm pixman-devel-0.42.2-1.el9.x86_64.rpm
sudo rpm -ivh wayland-protocols-devel-1.32-1.el9.x86_64.rpm
sudo rpm -ivh libseat-0.8.0-1.el9.x86_64.rpm libseat-devel-0.8.0-1.el9.x86_64.rpm
sudo rpm -ivh libdisplay-info-0.1.1-1.el9.x86_64.rpm libdisplay-info-devel-0.1.1-1.el9.x86_64.rpm
sudo rpm -ivh wlroots-0.17.1-1.el9.x86_64.rpm wlroots-devel-0.17.1-1.el9.x86_64.rpm
```

## Notes

- Built on AlmaLinux 9
- Requires NVIDIA GPU drivers
- Requires Xwayland for X11 application support

## License

All components maintain their original licenses. See individual spec files for details.
