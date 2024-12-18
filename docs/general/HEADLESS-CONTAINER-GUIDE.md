# General Headless Container Implementation Guide
## For RHEL-based Systems (AlmaLinux 9.x)

## 1. Prerequisites

### 1.1 System Requirements
```
Base OS: RHEL-based distribution (e.g., AlmaLinux 9.x)
Container Runtime: LXC/LXD compatible
Networking: Static IP capability
GPU: NVIDIA compatible hardware
```

### 1.2 Required Information
```
CONTAINER_NAME="[your-container-name]"
CONTAINER_IP="[your-ip-address]"
GATEWAY_IP="[your-gateway]"
DNS_SERVER="[your-dns]"
DOMAIN="[your-domain]"
REPO_BASE_URL="[your-repo-url]"
```

## 2. Container Setup

### 2.1 Network Configuration
```bash
# Configure static networking
nmcli connection modify eth0 ipv4.method manual
nmcli connection modify eth0 ipv4.addresses ${CONTAINER_IP}/24
nmcli connection modify eth0 ipv4.gateway ${GATEWAY_IP}
nmcli connection modify eth0 ipv4.dns ${DNS_SERVER}
nmcli connection modify eth0 ipv4.dns-search ${DOMAIN}

# Apply configuration
nmcli connection down eth0 && nmcli connection up eth0
```

### 2.2 Package Installation
```bash
# Install Wayland stack
dnf install \
    ${REPO_BASE_URL}/wayland-1.22.0-1.el9.x86_64.rpm \
    ${REPO_BASE_URL}/wayland-client-1.22.0-1.el9.x86_64.rpm \
    ${REPO_BASE_URL}/wayland-cursor-1.22.0-1.el9.x86_64.rpm \
    ${REPO_BASE_URL}/wayland-egl-1.22.0-1.el9.x86_64.rpm

# Install dependencies
dnf install \
    ${REPO_BASE_URL}/libdisplay-info-0.1.1-1.el9.x86_64.rpm \
    ${REPO_BASE_URL}/libseat-0.8.0-1.el9.x86_64.rpm \
    ${REPO_BASE_URL}/wlroots-0.17.1-1.el9.x86_64.rpm

# Install waypipe
dnf install ${REPO_BASE_URL}/waypipe-0.9.2-1.el9.x86_64.rpm
```

## 3. Environment Setup

### 3.1 Device Access
```bash
# Required devices and permissions
/dev/dri/card0         (rw-rw----)
/dev/dri/renderD128    (rw-rw-rw-)
/dev/nvidia0           (rw-rw-rw-)
/dev/nvidiactl         (rw-rw-rw-)
/dev/nvidia-modeset    (rw-rw-rw-)
```

### 3.2 Application User Setup
```bash
# Create application user
APP_USER="[application-user]"
useradd -m ${APP_USER}
usermod -aG video,render ${APP_USER}

# Setup directories
mkdir -p /home/${APP_USER}/Applications
chown -R ${APP_USER}:${APP_USER} /home/${APP_USER}
```

## 4. Application Integration

### 4.1 Application Template
```bash
#!/bin/bash

# Runtime Configuration
export XDG_RUNTIME_DIR=/run/user/$(id -u)
export WAYLAND_DISPLAY=wayland-0

# Wayland Settings
export ELECTRON_ENABLE_WAYLAND=1
export QT_QPA_PLATFORM=wayland
export QT_WAYLAND_DISABLE_WINDOWDECORATION=1

# Application Configuration
APP_NAME="[application-name]"
APP_PATH="/home/${APP_USER}/Applications/${APP_NAME}"

# Launch Application
${APP_PATH}
```

### 4.2 Runtime Directory Setup
```bash
# Create and configure runtime directory
XDG_RUNTIME_DIR=/run/user/$(id -u ${APP_USER})
mkdir -p ${XDG_RUNTIME_DIR}
chmod 700 ${XDG_RUNTIME_DIR}
chown ${APP_USER}:${APP_USER} ${XDG_RUNTIME_DIR}
```

## 5. Wayland Configuration

### 5.1 Socket Management
```bash
# Clear existing sockets
rm -f ${XDG_RUNTIME_DIR}/wayland-*

# Configure waypipe
waypipe \
    --socket=${XDG_RUNTIME_DIR}/wayland-0 \
    --allow-tiled \
    --drm-node=/dev/dri/renderD128 \
    server
```

### 5.2 Environment Variables
Essential environment variables for Wayland applications:
```bash
XDG_RUNTIME_DIR=/run/user/$(id -u)
WAYLAND_DISPLAY=wayland-0
ELECTRON_ENABLE_WAYLAND=1
QT_QPA_PLATFORM=wayland
QT_WAYLAND_DISABLE_WINDOWDECORATION=1
```

## 6. Troubleshooting

### 6.1 Verification Steps
```bash
# Check environment
env | grep -E 'XDG|WAYLAND|DISPLAY'

# Verify socket status
ls -la ${XDG_RUNTIME_DIR}

# Check GPU access
ls -l /dev/dri/
ls -l /dev/nvidia*
```

### 6.2 Common Issues
1. Socket Management:
   - Clean stale sockets
   - Verify ownership and permissions
   - Check waypipe operation

2. Application Launch:
   - Verify environment variables
   - Check file permissions
   - Confirm GPU access

### 6.3 Logging and Debugging
```bash
# Enable verbose waypipe logging
waypipe -d [other-options] server

# Check system logs
journalctl -xe

# Monitor GPU usage
nvidia-smi
```

## 7. Security Considerations

### 7.1 File Permissions
- Runtime directory: 700
- Socket permissions: user only
- Application files: user readable/executable

### 7.2 User Permissions
- Minimal required groups (video, render)
- Application-specific isolation
- No root execution for applications

## 8. Maintenance

### 8.1 Updates
- Test updates in separate container
- Maintain package compatibility
- Document working configurations

### 8.2 Backup
- Configuration files
- Application data
- User settings

## Notes
- Adapt paths and versions to your environment
- Test thoroughly before production use
- Document modifications for your use case
- Consider security implications
