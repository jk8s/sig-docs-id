diff --git a/content/en/docs/concepts/services-networking/add-entries-to-pod-etc-hosts-with-host-aliases.md b/content/en/docs/concepts/services-networking/add-entries-to-pod-etc-hosts-with-host-aliases.md
index 05a6a8bc8..8eee03bf9 100644
--- a/content/en/docs/concepts/services-networking/add-entries-to-pod-etc-hosts-with-host-aliases.md
+++ b/content/en/docs/concepts/services-networking/add-entries-to-pod-etc-hosts-with-host-aliases.md
@@ -5,27 +5,28 @@ reviewers:
 title: Adding entries to Pod /etc/hosts with HostAliases
 content_type: concept
 weight: 60
+min-kubernetes-server-version: 1.7
 ---
 
-{{< toc >}}
 
 <!-- overview -->
-Adding entries to a Pod's /etc/hosts file provides Pod-level override of hostname resolution when DNS and other options are not applicable. In 1.7, users can add these custom entries with the HostAliases field in PodSpec.
 
-Modification not using HostAliases is not suggested because the file is managed by Kubelet and can be overwritten on during Pod creation/restart.
+Adding entries to a Pod's `/etc/hosts` file provides Pod-level override of hostname resolution when DNS and other options are not applicable. You can add these custom entries with the HostAliases field in PodSpec.
+
+Modification not using HostAliases is not suggested because the file is managed by the kubelet and can be overwritten on during Pod creation/restart.
 
 
 <!-- body -->
 
-## Default Hosts File Content
+## Default hosts file content
 
-Let's start an Nginx Pod which is assigned a Pod IP:
+Start an Nginx Pod which is assigned a Pod IP:
 
 ```shell
-kubectl run nginx --image nginx --generator=run-pod/v1
+kubectl run nginx --image nginx
 ```
 
-```shell
+```
 pod/nginx created
 ```
 
@@ -35,7 +36,7 @@ Examine a Pod IP:
 kubectl get pods --output=wide
 ```
 
-```shell
+```
 NAME     READY     STATUS    RESTARTS   AGE    IP           NODE
 nginx    1/1       Running   0          13s    10.200.0.4   worker0
 ```
@@ -46,7 +47,7 @@ The hosts file content would look like this:
 kubectl exec nginx -- cat /etc/hosts
 ```
 
-```none
+```
 # Kubernetes-managed hosts file.
 127.0.0.1	localhost
 ::1	localhost ip6-localhost ip6-loopback
@@ -60,43 +61,44 @@ fe00::2	ip6-allrouters
 By default, the `hosts` file only includes IPv4 and IPv6 boilerplates like
 `localhost` and its own hostname.
 
-## Adding Additional Entries with HostAliases
+## Adding additional entries with hostAliases
 
-In addition to the default boilerplate, we can add additional entries to the
-`hosts` file to resolve `foo.local`, `bar.local` to `127.0.0.1` and `foo.remote`,
-`bar.remote` to `10.1.2.3`, we can by adding HostAliases to the Pod under
+In addition to the default boilerplate, you can add additional entries to the
+`hosts` file.
+For example: to resolve `foo.local`, `bar.local` to `127.0.0.1` and `foo.remote`,
+`bar.remote` to `10.1.2.3`, you can configure HostAliases for a Pod under
 `.spec.hostAliases`:
 
 {{< codenew file="service/networking/hostaliases-pod.yaml" >}}
 
-This Pod can be started with the following commands:
+You can start a Pod with that configuration by running:
 
 ```shell
-kubectl apply -f hostaliases-pod.yaml
+kubectl apply -f https://k8s.io/examples/service/networking/hostaliases-pod.yaml
 ```
 
-```shell
+```
 pod/hostaliases-pod created
 ```
 
-Examine a Pod IP and status:
+Examine a Pod's details to see its IPv4 address and its status:
 
 ```shell
 kubectl get pod --output=wide
 ```
 
-```shell
+```
 NAME                           READY     STATUS      RESTARTS   AGE       IP              NODE
 hostaliases-pod                0/1       Completed   0          6s        10.200.0.5      worker0
 ```
 
-The `hosts` file content would look like this:
+The `hosts` file content looks like this:
 
 ```shell
 kubectl logs hostaliases-pod
 ```
 
-```none
+```
 # Kubernetes-managed hosts file.
 127.0.0.1	localhost
 ::1	localhost ip6-localhost ip6-loopback
@@ -111,19 +113,18 @@ fe00::2	ip6-allrouters
 10.1.2.3	foo.remote	bar.remote
 ```
 
-With the additional entries specified at the bottom.
+with the additional entries specified at the bottom.
 
-## Why Does Kubelet Manage the Hosts File?
+## Why does the kubelet manage the hosts file? {#why-does-kubelet-manage-the-hosts-file}
 
-Kubelet [manages](https://github.com/kubernetes/kubernetes/issues/14633) the
+The kubelet [manages](https://github.com/kubernetes/kubernetes/issues/14633) the
 `hosts` file for each container of the Pod to prevent Docker from
 [modifying](https://github.com/moby/moby/issues/17190) the file after the
 containers have already been started.
 
-Because of the managed-nature of the file, any user-written content will be
-overwritten whenever the `hosts` file is remounted by Kubelet in the event of
-a container restart or a Pod reschedule. Thus, it is not suggested to modify
-the contents of the file.
-
-
+{{< caution >}}
+Avoid making manual changes to the hosts file inside a container.
 
+If you make manual changes to the hosts file,
+those changes are lost when the container exits.
+{{< /caution >}}

