%define debug_package %{nil}
%define selinux_variants mls targeted
%define selinux_policyver 3.14.3

Name:           coredns
Version:        1.12.0
Release:        1%{?dist}
Summary:        DNS server with minimal plugins for container environment

License:        Apache-2.0
URL:            https://github.com/coredns/coredns
Source0:        https://github.com/coredns/coredns/archive/v%{version}.tar.gz
Source1:        Corefile
Source2:        coredns.service

BuildRequires:  golang >= 1.20
BuildRequires:  git
BuildRequires:  systemd-rpm-macros
BuildRequires:  make
BuildRequires:  selinux-policy-devel
BuildRequires:  checkpolicy
BuildRequires:  policycoreutils

Requires(pre):  shadow-utils
Requires(post): systemd
Requires(post): policycoreutils
Requires(preun): systemd
Requires(postun): systemd
Requires: policycoreutils, libselinux-utils
Requires(post): selinux-policy-base >= %{selinux_policyver}

%description
CoreDNS is a DNS server that chains plugins. This build includes only the
essential plugins needed for container name resolution.

%prep
%autosetup

%build
export CGO_ENABLED=1
export GOFLAGS="-buildmode=pie -trimpath"
export LDFLAGS="-linkmode=external -compressdwarf=false"
make GOFLAGS="${GOFLAGS}" LDFLAGS="${LDFLAGS}"

%install
# Create directories
install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_sysconfdir}/coredns/zones
install -d %{buildroot}%{_localstatedir}/log/coredns
install -d %{buildroot}%{_unitdir}

# Install binary
install -p -m 755 coredns %{buildroot}%{_sbindir}/coredns

# Install config file
install -p -m 640 %{SOURCE1} %{buildroot}%{_sysconfdir}/coredns/Corefile

# Install systemd service file
install -p -m 644 %{SOURCE2} %{buildroot}%{_unitdir}/coredns.service

%pre
getent group coredns >/dev/null || groupadd -r coredns
getent passwd coredns >/dev/null || \
    useradd -r -g coredns -d %{_sysconfdir}/coredns -s /sbin/nologin \
    -c "CoreDNS DNS server" coredns

%post
%systemd_post coredns.service

# SELinux contexts
semanage port -a -t dns_port_t -p tcp 53 2>/dev/null || :
semanage port -a -t dns_port_t -p udp 53 2>/dev/null || :
restorecon -R %{_sysconfdir}/coredns || :
restorecon -R %{_sbindir}/coredns || :
restorecon -R %{_localstatedir}/log/coredns || :

# Set file contexts
semanage fcontext -a -t bin_t %{_sbindir}/coredns || :
semanage fcontext -a -t etc_t "%{_sysconfdir}/coredns(/.*)?" || :
semanage fcontext -a -t var_log_t "%{_localstatedir}/log/coredns(/.*)?" || :

%preun
%systemd_preun coredns.service

%postun
%systemd_postun_with_restart coredns.service
if [ $1 -eq 0 ] ; then  # Package removal
    semanage port -d -t dns_port_t -p tcp 53 2>/dev/null || :
    semanage port -d -t dns_port_t -p udp 53 2>/dev/null || :
    semanage fcontext -d -t bin_t %{_sbindir}/coredns || :
    semanage fcontext -d -t etc_t "%{_sysconfdir}/coredns(/.*)?" || :
    semanage fcontext -d -t var_log_t "%{_localstatedir}/log/coredns(/.*)?" || :
fi

%files
%license LICENSE
%doc README.md
%attr(755,root,root) %{_sbindir}/coredns
%dir %attr(750,coredns,coredns) %{_sysconfdir}/coredns
%dir %attr(750,coredns,coredns) %{_sysconfdir}/coredns/zones
%config(noreplace) %attr(640,coredns,coredns) %{_sysconfdir}/coredns/Corefile
%attr(644,root,root) %{_unitdir}/coredns.service
%dir %attr(750,coredns,coredns) %{_localstatedir}/log/coredns

%changelog
* Sun Mar 17 2024 Oceanic Cloud Infrastructure Team <admin@oceanic.cloud> - 1.12.0-1
- Initial package with minimal plugins for container DNS
- Added SELinux contexts and RHEL-specific configurations
- Fixed file declarations and permissions
