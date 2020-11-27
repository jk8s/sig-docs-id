diff --git a/content/en/docs/setup/production-environment/container-runtimes.md b/content/en/docs/setup/production-environment/container-runtimes.md
index 77e7bb577..ecaf53c03 100644
--- a/content/en/docs/setup/production-environment/container-runtimes.md
+++ b/content/en/docs/setup/production-environment/container-runtimes.md
@@ -4,411 +4,498 @@ reviewers:
 - bart0sh
 title: Container runtimes
 content_type: concept
-weight: 10
+weight: 20
 ---
 <!-- overview -->
-{{< feature-state for_k8s_version="v1.6" state="stable" >}}
-To run containers in Pods, Kubernetes uses a container runtime. Here are
-the installation instructions for various runtimes.
-
 
+You need to install a
+{{< glossary_tooltip text="container runtime" term_id="container-runtime" >}}
+into each node in the cluster so that Pods can run there. This page outlines
+what is involved and describes related tasks for setting up nodes.
 
 <!-- body -->
 
+This page lists details for using several common container runtimes with
+Kubernetes, on Linux:
 
-{{< caution >}}
-A flaw was found in the way runc handled system file descriptors when running containers.
-A malicious container could use this flaw to overwrite contents of the runc binary and
-consequently run arbitrary commands on the container host system.
-
-Please refer to [CVE-2019-5736](https://access.redhat.com/security/cve/cve-2019-5736) for more
-information about the issue.
-{{< /caution >}}
-
-### Applicability
+- [containerd](#containerd)
+- [CRI-O](#cri-o)
+- [Docker](#docker)
 
 {{< note >}}
-This document is written for users installing CRI onto Linux. For other operating
-systems, look for documentation specific to your platform.
+For other operating systems, look for documentation specific to your platform.
 {{< /note >}}
 
-You should execute all the commands in this guide as `root`. For example, prefix commands
-with `sudo `, or become `root` and run the commands as that user.
+## Cgroup drivers
 
-### Cgroup drivers
+Control groups are used to constrain resources that are allocated to processes.
 
-When systemd is chosen as the init system for a Linux distribution, the init process generates
-and consumes a root control group (`cgroup`) and acts as a cgroup manager. Systemd has a tight
-integration with cgroups and will allocate cgroups per process. It's possible to configure your
-container runtime and the kubelet to use `cgroupfs`. Using `cgroupfs` alongside systemd means
-that there will be two different cgroup managers.
+When [systemd](https://www.freedesktop.org/wiki/Software/systemd/) is chosen as the init
+system for a Linux distribution, the init process generates and consumes a root control group
+(`cgroup`) and acts as a cgroup manager.
+Systemd has a tight integration with cgroups and allocates a cgroup per systemd unit. It's possible
+to configure your container runtime and the kubelet to use `cgroupfs`. Using `cgroupfs` alongside
+systemd means that there will be two different cgroup managers.
 
-Control groups are used to constrain resources that are allocated to processes.
-A single cgroup manager will simplify the view of what resources are being allocated
-and will by default have a more consistent view of the available and in-use resources. When we have
-two managers we end up with two views of those resources. We have seen cases in the field
-where nodes that are configured to use `cgroupfs` for the kubelet and Docker, and `systemd`
-for the rest of the processes running on the node becomes unstable under resource pressure.
+A single cgroup manager simplifies the view of what resources are being allocated
+and will by default have a more consistent view of the available and in-use resources.
+When there are two cgroup managers on a system, you end up with two views of those resources.
+In the field, people have reported cases where nodes that are configured to use `cgroupfs`
+for the kubelet and Docker, but `systemd` for the rest of the processes, become unstable under
+resource pressure.
 
 Changing the settings such that your container runtime and kubelet use `systemd` as the cgroup driver
-stabilized the system. Please note the `native.cgroupdriver=systemd` option in the Docker setup below.
+stabilized the system. To configure this for Docker, set `native.cgroupdriver=systemd`.
 
 {{< caution >}}
-Changing the cgroup driver of a Node that has joined a cluster is highly unrecommended.
+Changing the cgroup driver of a Node that has joined a cluster is strongly *not* recommended.  
 If the kubelet has created Pods using the semantics of one cgroup driver, changing the container
-runtime to another cgroup driver can cause errors when trying to re-create the PodSandbox
-for such existing Pods. Restarting the kubelet may not solve such errors. The recommendation
-is to drain the Node from its workloads, remove it from the cluster and re-join it.
+runtime to another cgroup driver can cause errors when trying to re-create the Pod sandbox
+for such existing Pods. Restarting the kubelet may not solve such errors.
+
+If you have automation that makes it feasible, replace the node with another using the updated
+configuration, or reinstall it using automation.
 {{< /caution >}}
 
-## Docker
+## Container runtimes
 
-On each of your machines, install Docker.
-Version 19.03.11 is recommended, but 1.13.1, 17.03, 17.06, 17.09, 18.06 and 18.09 are known to work as well.
-Keep track of the latest verified Docker version in the Kubernetes release notes.
+{{% thirdparty-content %}}
 
-Use the following commands to install Docker on your system:
+### containerd
 
-{{< tabs name="tab-cri-docker-installation" >}}
-{{% tab name="Ubuntu 16.04+" %}}
+This section contains the necessary steps to use `containerd` as CRI runtime.
+
+Use the following commands to install Containerd on your system:
+
+Install and configure prerequisites:
 
 ```shell
-# (Install Docker CE)
-## Set up the repository:
-### Install packages to allow apt to use a repository over HTTPS
-apt-get update && apt-get install -y \
-  apt-transport-https ca-certificates curl software-properties-common gnupg2
+cat <<EOF | sudo tee /etc/modules-load.d/containerd.conf
+overlay
+br_netfilter
+EOF
+
+sudo modprobe overlay
+sudo modprobe br_netfilter
+
+# Setup required sysctl params, these persist across reboots.
+cat <<EOF | sudo tee /etc/sysctl.d/99-kubernetes-cri.conf
+net.bridge.bridge-nf-call-iptables  = 1
+net.ipv4.ip_forward                 = 1
+net.bridge.bridge-nf-call-ip6tables = 1
+EOF
+
+# Apply sysctl params without reboot
+sudo sysctl --system
 ```
 
+Install containerd:
+
+{{< tabs name="tab-cri-containerd-installation" >}}
+{{% tab name="Ubuntu 16.04" %}}
+
 ```shell
-# Add Docker’s official GPG key:
-curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
+# (Install containerd)
+## Set up the repository
+### Install packages to allow apt to use a repository over HTTPS
+sudo apt-get update && sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common
 ```
 
 ```shell
-# Add the Docker apt repository:
-add-apt-repository \
-  "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
-  $(lsb_release -cs) \
-  stable"
+## Add Docker's official GPG key
+curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key --keyring /etc/apt/trusted.gpg.d/docker.gpg add -
 ```
 
 ```shell
-# Install Docker CE
-apt-get update && apt-get install -y \
-  containerd.io=1.2.13-2 \
-  docker-ce=5:19.03.11~3-0~ubuntu-$(lsb_release -cs) \
-  docker-ce-cli=5:19.03.11~3-0~ubuntu-$(lsb_release -cs)
+## Add Docker apt repository.
+sudo add-apt-repository \
+    "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
+    $(lsb_release -cs) \
+    stable"
 ```
 
 ```shell
-# Set up the Docker daemon
-cat > /etc/docker/daemon.json <<EOF
-{
-  "exec-opts": ["native.cgroupdriver=systemd"],
-  "log-driver": "json-file",
-  "log-opts": {
-    "max-size": "100m"
-  },
-  "storage-driver": "overlay2"
-}
-EOF
+## Install containerd
+sudo apt-get update && sudo apt-get install -y containerd.io
 ```
 
 ```shell
-mkdir -p /etc/systemd/system/docker.service.d
+# Configure containerd
+sudo mkdir -p /etc/containerd
+sudo containerd config default > /etc/containerd/config.toml
 ```
 
 ```shell
-# Restart Docker
-systemctl daemon-reload
-systemctl restart docker
+# Restart containerd
+sudo systemctl restart containerd
 ```
 {{% /tab %}}
 {{% tab name="CentOS/RHEL 7.4+" %}}
 
 ```shell
-# (Install Docker CE)
+# (Install containerd)
 ## Set up the repository
 ### Install required packages
-yum install -y yum-utils device-mapper-persistent-data lvm2
+sudo yum install -y yum-utils device-mapper-persistent-data lvm2
 ```
 
 ```shell
-## Add the Docker repository
-yum-config-manager --add-repo \
-  https://download.docker.com/linux/centos/docker-ce.repo
+## Add docker repository
+sudo yum-config-manager \
+    --add-repo \
+    https://download.docker.com/linux/centos/docker-ce.repo
 ```
 
 ```shell
-# Install Docker CE
-yum update -y && yum install -y \
-  containerd.io-1.2.13 \
-  docker-ce-19.03.11 \
-  docker-ce-cli-19.03.11
+## Install containerd
+sudo yum update -y && sudo yum install -y containerd.io
 ```
 
 ```shell
-## Create /etc/docker
-mkdir /etc/docker
+## Configure containerd
+sudo mkdir -p /etc/containerd
+sudo containerd config default > /etc/containerd/config.toml
 ```
 
 ```shell
-# Set up the Docker daemon
-cat > /etc/docker/daemon.json <<EOF
-{
-  "exec-opts": ["native.cgroupdriver=systemd"],
-  "log-driver": "json-file",
-  "log-opts": {
-    "max-size": "100m"
-  },
-  "storage-driver": "overlay2",
-  "storage-opts": [
-    "overlay2.override_kernel_check=true"
-  ]
-}
-EOF
+# Restart containerd
+sudo systemctl restart containerd
+```
+{{% /tab %}}
+{{% tab name="Windows (PowerShell)" %}}
+```powershell
+# (Install containerd)
+# download containerd
+cmd /c curl -OL https://github.com/containerd/containerd/releases/download/v1.4.0-beta.2/containerd-1.4.0-beta.2-windows-amd64.tar.gz
+cmd /c tar xvf .\containerd-1.4.0-beta.2-windows-amd64.tar.gz
 ```
 
-```shell
-mkdir -p /etc/systemd/system/docker.service.d
+```powershell
+# extract and configure
+Copy-Item -Path ".\bin\" -Destination "$Env:ProgramFiles\containerd" -Recurse -Force
+cd $Env:ProgramFiles\containerd\
+.\containerd.exe config default | Out-File config.toml -Encoding ascii
+
+# review the configuration. depending on setup you may want to adjust:
+# - the sandbox_image (kubernetes pause image)
+# - cni bin_dir and conf_dir locations
+Get-Content config.toml
 ```
 
-```shell
-# Restart Docker
-systemctl daemon-reload
-systemctl restart docker
+```powershell
+# start containerd
+.\containerd.exe --register-service
+Start-Service containerd
 ```
 {{% /tab %}}
 {{< /tabs >}}
 
-If you want the docker service to start on boot, run the following command:
+#### systemd {#containerd-systemd}
+
+To use the `systemd` cgroup driver in `/etc/containerd/config.toml` with `runc`, set
 
-```shell
-sudo systemctl enable docker
+```
+[plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc]
+  ...
+  [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc.options]
+    SystemdCgroup = true
 ```
 
-Refer to the [official Docker installation guides](https://docs.docker.com/engine/installation/)
-for more information.
+When using kubeadm, manually configure the
+[cgroup driver for kubelet](/docs/setup/production-environment/tools/kubeadm/install-kubeadm/#configure-cgroup-driver-used-by-kubelet-on-control-plane-node).
 
-## CRI-O
+### CRI-O
 
-This section contains the necessary steps to install `CRI-O` as CRI runtime.
+This section contains the necessary steps to install CRI-O as a container runtime.
 
 Use the following commands to install CRI-O on your system:
 
 {{< note >}}
 The CRI-O major and minor versions must match the Kubernetes major and minor versions.
-For more information, see the [CRI-O compatiblity matrix](https://github.com/cri-o/cri-o).
+For more information, see the [CRI-O compatibility matrix](https://github.com/cri-o/cri-o).
 {{< /note >}}
 
-### Prerequisites
+Install and configure prerequisites:
 
 ```shell
-modprobe overlay
-modprobe br_netfilter
+sudo modprobe overlay
+sudo modprobe br_netfilter
 
 # Set up required sysctl params, these persist across reboots.
-cat > /etc/sysctl.d/99-kubernetes-cri.conf <<EOF
+cat <<EOF | sudo tee /etc/sysctl.d/99-kubernetes-cri.conf
 net.bridge.bridge-nf-call-iptables  = 1
 net.ipv4.ip_forward                 = 1
 net.bridge.bridge-nf-call-ip6tables = 1
 EOF
 
-sysctl --system
+sudo sysctl --system
 ```
 
 {{< tabs name="tab-cri-cri-o-installation" >}}
 {{% tab name="Debian" %}}
 
-```shell
-# Debian Unstable/Sid
-echo 'deb http://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/Debian_Unstable/ /' > /etc/apt/sources.list.d/devel:kubic:libcontainers:stable.list
-wget -nv https://download.opensuse.org/repositories/devel:kubic:libcontainers:stable/Debian_Unstable/Release.key -O- | sudo apt-key add -
-```
+To install CRI-O on the following operating systems, set the environment variable `OS`
+to the appropriate value from the following table:
 
-```shell
-# Debian Testing
-echo 'deb http://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/Debian_Testing/ /' > /etc/apt/sources.list.d/devel:kubic:libcontainers:stable.list
-wget -nv https://download.opensuse.org/repositories/devel:kubic:libcontainers:stable/Debian_Testing/Release.key -O- | sudo apt-key add -
-```
+| Operating system | `$OS`             |
+| ---------------- | ----------------- |
+| Debian Unstable  | `Debian_Unstable` |
+| Debian Testing   | `Debian_Testing`  |
 
-```shell
-# Debian 10
-echo 'deb http://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/Debian_10/ /' > /etc/apt/sources.list.d/devel:kubic:libcontainers:stable.list
-wget -nv https://download.opensuse.org/repositories/devel:kubic:libcontainers:stable/Debian_10/Release.key -O- | sudo apt-key add -
-```
+<br />
+Then, set `$VERSION` to the CRI-O version that matches your Kubernetes version.
+For instance, if you want to install CRI-O 1.18, set `VERSION=1.18`.
+You can pin your installation to a specific release.
+To install version 1.18.3, set `VERSION=1.18:1.18.3`.
+<br />
 
+Then run
 ```shell
-# Raspbian 10
-echo 'deb http://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/Raspbian_10/ /' > /etc/apt/sources.list.d/devel:kubic:libcontainers:stable.list
-wget -nv https://download.opensuse.org/repositories/devel:kubic:libcontainers:stable/Raspbian_10/Release.key -O- | sudo apt-key add -
-```
+cat <<EOF | sudo tee /etc/apt/sources.list.d/devel:kubic:libcontainers:stable.list
+deb https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/$OS/ /
+EOF
+cat <<EOF | sudo tee /etc/apt/sources.list.d/devel:kubic:libcontainers:stable:cri-o:$VERSION.list
+deb http://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable:/cri-o:/$VERSION/$OS/ /
+EOF
 
-and then install CRI-O:
-```shell
-sudo apt-get install cri-o-1.17
+curl -L https://download.opensuse.org/repositories/devel:kubic:libcontainers:stable:cri-o:$VERSION/$OS/Release.key | sudo apt-key --keyring /etc/apt/trusted.gpg.d/libcontainers.gpg add -
+curl -L https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/$OS/Release.key | sudo apt-key --keyring /etc/apt/trusted.gpg.d/libcontainers.gpg add -
+
+sudo apt-get update
+sudo apt-get install cri-o cri-o-runc
 ```
+
 {{% /tab %}}
 
-{{% tab name="Ubuntu 18.04, 19.04 and 19.10" %}}
+{{% tab name="Ubuntu" %}}
 
+To install on the following operating systems, set the environment variable `OS` to the appropriate field in the following table:
+
+| Operating system | `$OS`             |
+| ---------------- | ----------------- |
+| Ubuntu 20.04     | `xUbuntu_20.04`   |
+| Ubuntu 19.10     | `xUbuntu_19.10`   |
+| Ubuntu 19.04     | `xUbuntu_19.04`   |
+| Ubuntu 18.04     | `xUbuntu_18.04`   |
+
+<br />
+Then, set `$VERSION` to the CRI-O version that matches your Kubernetes version.
+For instance, if you want to install CRI-O 1.18, set `VERSION=1.18`.
+You can pin your installation to a specific release.
+To install version 1.18.3, set `VERSION=1.18:1.18.3`.
+<br />
+
+Then run
 ```shell
-# Configure package repository
-. /etc/os-release
-sudo sh -c "echo 'deb http://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/x${NAME}_${VERSION_ID}/ /' > /etc/apt/sources.list.d/devel:kubic:libcontainers:stable.list"
-wget -nv https://download.opensuse.org/repositories/devel:kubic:libcontainers:stable/x${NAME}_${VERSION_ID}/Release.key -O- | sudo apt-key add -
+cat <<EOF | sudo tee /etc/apt/sources.list.d/devel:kubic:libcontainers:stable.list
+deb https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/$OS/ /
+EOF
+cat <<EOF | sudo tee /etc/apt/sources.list.d/devel:kubic:libcontainers:stable:cri-o:$VERSION.list
+deb http://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable:/cri-o:/$VERSION/$OS/ /
+EOF
+
+curl -L https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/$OS/Release.key | sudo apt-key --keyring /etc/apt/trusted.gpg.d/libcontainers.gpg add -
+curl -L https://download.opensuse.org/repositories/devel:kubic:libcontainers:stable:cri-o:$VERSION/$OS/Release.key | sudo apt-key --keyring /etc/apt/trusted.gpg.d/libcontainers-cri-o.gpg add -
+
 sudo apt-get update
+sudo apt-get install cri-o cri-o-runc
 ```
+{{% /tab %}}
 
+{{% tab name="CentOS" %}}
+
+To install on the following operating systems, set the environment variable `OS` to the appropriate field in the following table:
+
+| Operating system | `$OS`             |
+| ---------------- | ----------------- |
+| Centos 8         | `CentOS_8`        |
+| Centos 8 Stream  | `CentOS_8_Stream` |
+| Centos 7         | `CentOS_7`        |
+
+<br />
+Then, set `$VERSION` to the CRI-O version that matches your Kubernetes version.
+For instance, if you want to install CRI-O 1.18, set `VERSION=1.18`.
+You can pin your installation to a specific release.
+To install version 1.18.3, set `VERSION=1.18:1.18.3`.
+<br />
+
+Then run
 ```shell
-# Install CRI-O
-sudo apt-get install cri-o-1.17
+sudo curl -L -o /etc/yum.repos.d/devel:kubic:libcontainers:stable.repo https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/$OS/devel:kubic:libcontainers:stable.repo
+sudo curl -L -o /etc/yum.repos.d/devel:kubic:libcontainers:stable:cri-o:$VERSION.repo https://download.opensuse.org/repositories/devel:kubic:libcontainers:stable:cri-o:$VERSION/$OS/devel:kubic:libcontainers:stable:cri-o:$VERSION.repo
+sudo yum install cri-o
 ```
+
 {{% /tab %}}
 
-{{% tab name="CentOS/RHEL 7.4+" %}}
+{{% tab name="openSUSE Tumbleweed" %}}
 
 ```shell
-# Install prerequisites
-curl -L -o /etc/yum.repos.d/devel:kubic:libcontainers:stable.repo https://download.opensuse.org/repositories/devel:kubic:libcontainers:stable/CentOS_7/devel:kubic:libcontainers:stable.repo
-curl -L -o /etc/yum.repos.d/devel:kubic:libcontainers:stable:cri-o:{{< skew latestVersion >}}.repo https://download.opensuse.org/repositories/devel:kubic:libcontainers:stable:cri-o:{{< skew latestVersion >}}/CentOS_7/devel:kubic:libcontainers:stable:cri-o:{{< skew latestVersion >}}.repo
+sudo zypper install cri-o
 ```
+{{% /tab %}}
+{{% tab name="Fedora" %}}
 
+Set `$VERSION` to the CRI-O version that matches your Kubernetes version.
+For instance, if you want to install CRI-O 1.18, `VERSION=1.18`.
+
+You can find available versions with:
 ```shell
-# Install CRI-O
-yum install -y cri-o
+sudo dnf module list cri-o
 ```
-{{% /tab %}}
-
-{{% tab name="openSUSE Tumbleweed" %}}
+CRI-O does not support pinning to specific releases on Fedora.
 
+Then run
 ```shell
-sudo zypper install cri-o
+sudo dnf module enable cri-o:$VERSION
+sudo dnf install cri-o
 ```
+
 {{% /tab %}}
 {{< /tabs >}}
 
-### Start CRI-O
+Start CRI-O:
 
 ```shell
-systemctl daemon-reload
-systemctl start crio
+sudo systemctl daemon-reload
+sudo systemctl start crio
 ```
 
 Refer to the [CRI-O installation guide](https://github.com/kubernetes-sigs/cri-o#getting-started)
 for more information.
 
-## Containerd
 
-This section contains the necessary steps to use `containerd` as CRI runtime.
 
-Use the following commands to install Containerd on your system:
+### Docker
 
-### Prerequisites
+On each of your nodes, install Docker CE.
 
-```shell
-cat > /etc/modules-load.d/containerd.conf <<EOF
-overlay
-br_netfilter
-EOF
+The Kubernetes release notes list which versions of Docker are compatible
+with that version of Kubernetes.
 
-modprobe overlay
-modprobe br_netfilter
+Use the following commands to install Docker on your system:
 
-# Setup required sysctl params, these persist across reboots.
-cat > /etc/sysctl.d/99-kubernetes-cri.conf <<EOF
-net.bridge.bridge-nf-call-iptables  = 1
-net.ipv4.ip_forward                 = 1
-net.bridge.bridge-nf-call-ip6tables = 1
-EOF
+{{< tabs name="tab-cri-docker-installation" >}}
+{{% tab name="Ubuntu 16.04+" %}}
 
-sysctl --system
+```shell
+# (Install Docker CE)
+## Set up the repository:
+### Install packages to allow apt to use a repository over HTTPS
+sudo apt-get update && sudo apt-get install -y \
+  apt-transport-https ca-certificates curl software-properties-common gnupg2
 ```
 
-### Install containerd
-
-{{< tabs name="tab-cri-containerd-installation" >}}
-{{% tab name="Ubuntu 16.04" %}}
-
 ```shell
-# (Install containerd)
-## Set up the repository
-### Install packages to allow apt to use a repository over HTTPS
-apt-get update && apt-get install -y apt-transport-https ca-certificates curl software-properties-common
+# Add Docker's official GPG key:
+curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key --keyring /etc/apt/trusted.gpg.d/docker.gpg add -
 ```
 
 ```shell
-## Add Docker’s official GPG key
-curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
+# Add the Docker apt repository:
+sudo add-apt-repository \
+  "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
+  $(lsb_release -cs) \
+  stable"
 ```
 
 ```shell
-## Add Docker apt repository.
-add-apt-repository \
-    "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
-    $(lsb_release -cs) \
-    stable"
+# Install Docker CE
+sudo apt-get update && sudo apt-get install -y \
+  containerd.io=1.2.13-2 \
+  docker-ce=5:19.03.11~3-0~ubuntu-$(lsb_release -cs) \
+  docker-ce-cli=5:19.03.11~3-0~ubuntu-$(lsb_release -cs)
 ```
 
 ```shell
-## Install containerd
-apt-get update && apt-get install -y containerd.io
+# Set up the Docker daemon
+cat <<EOF | sudo tee /etc/docker/daemon.json
+{
+  "exec-opts": ["native.cgroupdriver=systemd"],
+  "log-driver": "json-file",
+  "log-opts": {
+    "max-size": "100m"
+  },
+  "storage-driver": "overlay2"
+}
+EOF
 ```
 
 ```shell
-# Configure containerd
-mkdir -p /etc/containerd
-containerd config default > /etc/containerd/config.toml
+# Create /etc/systemd/system/docker.service.d
+sudo mkdir -p /etc/systemd/system/docker.service.d
 ```
 
 ```shell
-# Restart containerd
-systemctl restart containerd
+# Restart Docker
+sudo systemctl daemon-reload
+sudo systemctl restart docker
 ```
 {{% /tab %}}
 {{% tab name="CentOS/RHEL 7.4+" %}}
 
 ```shell
-# (Install containerd)
+# (Install Docker CE)
 ## Set up the repository
 ### Install required packages
-yum install -y yum-utils device-mapper-persistent-data lvm2
+sudo yum install -y yum-utils device-mapper-persistent-data lvm2
 ```
 
 ```shell
-## Add docker repository
-yum-config-manager \
-    --add-repo \
-    https://download.docker.com/linux/centos/docker-ce.repo
+## Add the Docker repository
+sudo yum-config-manager --add-repo \
+  https://download.docker.com/linux/centos/docker-ce.repo
 ```
 
 ```shell
-## Install containerd
-yum update -y && yum install -y containerd.io
+# Install Docker CE
+sudo yum update -y && sudo yum install -y \
+  containerd.io-1.2.13 \
+  docker-ce-19.03.11 \
+  docker-ce-cli-19.03.11
 ```
 
 ```shell
-## Configure containerd
-mkdir -p /etc/containerd
-containerd config default > /etc/containerd/config.toml
+## Create /etc/docker
+sudo mkdir /etc/docker
 ```
 
 ```shell
-# Restart containerd
-systemctl restart containerd
+# Set up the Docker daemon
+cat <<EOF | sudo tee /etc/docker/daemon.json
+{
+  "exec-opts": ["native.cgroupdriver=systemd"],
+  "log-driver": "json-file",
+  "log-opts": {
+    "max-size": "100m"
+  },
+  "storage-driver": "overlay2",
+  "storage-opts": [
+    "overlay2.override_kernel_check=true"
+  ]
+}
+EOF
 ```
-{{% /tab %}}
-{{< /tabs >}}
 
-### systemd
+```shell
+# Create /etc/systemd/system/docker.service.d
+sudo mkdir -p /etc/systemd/system/docker.service.d
+```
 
-To use the `systemd` cgroup driver, set `plugins.cri.systemd_cgroup = true` in `/etc/containerd/config.toml`.
-When using kubeadm, manually configure the
-[cgroup driver for kubelet](/docs/setup/production-environment/tools/kubeadm/install-kubeadm/#configure-cgroup-driver-used-by-kubelet-on-control-plane-node)
+```shell
+# Restart Docker
+sudo systemctl daemon-reload
+sudo systemctl restart docker
+```
+{{% /tab %}}
+{{< /tabs >}}
 
-## Other CRI runtimes: frakti
+If you want the `docker` service to start on boot, run the following command:
 
-Refer to the [Frakti QuickStart guide](https://github.com/kubernetes/frakti#quickstart) for more information.
+```shell
+sudo systemctl enable docker
+```
 
+Refer to the [official Docker installation guides](https://docs.docker.com/engine/installation/)
+for more information.
 

