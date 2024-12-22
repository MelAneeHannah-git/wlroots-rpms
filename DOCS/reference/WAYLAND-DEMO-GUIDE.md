# Wayland-Demo Reference Implementation Guide
## Verified Configuration on AlmaLinux 9.x

## 1. Base Configuration

### 1.1 Container Details
```
Name: wayland-demo
Base: AlmaLinux 9.x
IP: 192.168.9.31/24
Gateway: 192.168.9.1
DNS: 192.168.9.22 (schriftstellerin)
Domain: oceanic.local
```

### 1.2 Repository Sources
```
Wayland/Wlroots: https://github.com/MelAneeHannah-git/wlroots-rpms
Waypipe: https://github.com/MelAneeHannah-git/waypipe-almalinux9.rpm
```

## 2. Package Installation

### 2.1 Base Packages
```bash
# Install Wayland packages
dnf install \
    https://github.com/MelAneeHannah-git/wlroots-rpms/raw/main/wayland-1.22.0-1.el9.x86_64.rpm \
    https://github.com/MelAneeHannah-git/wlroots-rpms/raw/main/wayland-client-1.22.0-1.el9.x86_64.rpm \
    https://github.com/MelAneeHannah-git/wlroots-rpms/raw/main/wayland-cursor-1.22.0-1.el9.x86_64.rpm \
    https://github.com/MelAneeHannah-git/wlroots-rpms/raw/main/wayland-egl-1.22.0-1.el9.x86_64.rpm

# Install dependencies
dnf install \
    https://github.com/MelAneeHannah-git/wlroots-rpms/raw/main/libdisplay-info-0.1.1-1.el9.x86_64.rpm \
    https://github.com/MelAneeHannah-git/wlroots-rpms/raw/main/libseat-0.8.0-1.el9.x86_64.rpm \
    https://github.com/MelAneeHannah-git/wlroots-rpms/raw/main/wlroots-0.17.1-1.el9.x86_64.rpm

# Install waypipe
dnf install https://github.com/MelAneeHannah-git/waypipe-almalinux9.rpm/raw/main/RPMS/x86_64/waypipe-0.9.2-1.el9.x86_64.rpm
```

## 3. Network Configuration

### 3.1 Static IP Setup
```bash
nmcli connection modify eth0 ipv4.method manual
nmcli connection modify eth0 ipv4.addresses 192.168.9.31/24
nmcli connection modify eth0 ipv4.gateway 192.168.9.1
nmcli connection modify eth0 ipv4.dns 192.168.9.22
nmcli connection modify eth0 ipv4.dns-search oceanic.local

# Apply changes
nmcli connection down eth0 && nmcli connection up eth0
```

## 4. GPU Configuration

### 4.1 Device Access
```bash
# Verify device access and permissions
ls -l /dev/dri/card0         # Should be rw-rw----
ls -l /dev/dri/renderD128    # Should be rw-rw-rw-
ls -l /dev/nvidia*           # Should be rw-rw-rw-
```

## 5. Application Setup

### 5.1 User Creation
```bash
# Create application user (example: obsidian)
useradd -m obsidian
usermod -aG video,render obsidian

# Create application directories
mkdir -p /home/obsidian/Applications
chown -R obsidian:obsidian /home/obsidian
```

### 5.2 Launch Script
```bash
#!/bin/bash

# Runtime directory setup
export XDG_RUNTIME_DIR=/run/user/$(id -u)
export WAYLAND_DISPLAY=wayland-0

# Wayland/Electron-specific settings
export ELECTRON_ENABLE_WAYLAND=1
export QT_QPA_PLATFORM=wayland
export QT_WAYLAND_DISABLE_WINDOWDECORATION=1

# Path to application
APPIMAGE_PATH="$HOME/Applications/[APP_NAME].AppImage"

# Run application
"$APPIMAGE_PATH"
```

## 6. Verified Environment

### 6.1 Runtime Configuration
```bash
# Runtime directory
XDG_RUNTIME_DIR=/run/user/1000    # For user with UID 1000
WAYLAND_DISPLAY=wayland-0
```

### 6.2 GPU Support
- Verified working with NVIDIA GPU
- DRM/KMS support enabled
- Hardware acceleration available

## 7. Known Working Applications
- Obsidian (Electron-based)
- [Other verified applications to be added]

## 8. Troubleshooting

### 8.1 Common Issues
1. Socket Management:
   - Clear stale sockets: `rm -f $XDG_RUNTIME_DIR/wayland-*`
   - Check socket ownership
   - Verify waypipe operation

2. Application Launch:
   - Verify environment variables
   - Check user permissions
   - Confirm GPU access

### 8.2 Verification Commands
```bash
# Environment check
env | grep -E 'XDG|WAYLAND|DISPLAY'

# Socket check
ls -la $XDG_RUNTIME_DIR

# GPU check
ls -l /dev/dri/
ls -l /dev/nvidia*
```

## Notes
- Configuration tested on AlmaLinux 9.x
- All paths and permissions verified
- Package versions tested and confirmed working
- Based on actual working implementation
