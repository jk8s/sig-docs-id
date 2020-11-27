diff --git a/content/en/docs/concepts/services-networking/dns-pod-service.md b/content/en/docs/concepts/services-networking/dns-pod-service.md
index 9d88019e3..1a55acf3d 100644
--- a/content/en/docs/concepts/services-networking/dns-pod-service.md
+++ b/content/en/docs/concepts/services-networking/dns-pod-service.md
@@ -68,10 +68,19 @@ of the form `auto-generated-name.my-svc.my-namespace.svc.cluster-domain.example`
 
 ### A/AAAA records
 
-Any pods created by a Deployment or DaemonSet have the following
-DNS resolution available:
+In general a pod has the following DNS resolution:
 
-`pod-ip-address.deployment-name.my-namespace.svc.cluster-domain.example.`
+`pod-ip-address.my-namespace.pod.cluster-domain.example`.
+
+For example, if a pod in the `default` namespace has the IP address 172.17.0.3,
+and the domain name for your cluster is `cluster.local`, then the Pod has a DNS name:
+
+`172-17-0-3.default.pod.cluster.local`.
+
+Any pods created by a Deployment or DaemonSet exposed by a Service have the
+following DNS resolution available:
+
+`pod-ip-address.deployment-name.my-namespace.svc.cluster-domain.example`.
 
 ### Pod's hostname and subdomain fields
 
@@ -157,6 +166,24 @@ pointing to the Pod's IP address. Also, Pod needs to become ready in order to ha
 record unless `publishNotReadyAddresses=True` is set on the Service.
 {{< /note >}}
 
+### Pod's setHostnameAsFQDN field {#pod-sethostnameasfqdn-field}
+
+{{< feature-state for_k8s_version="v1.19" state="alpha" >}}
+
+**Prerequisites**: The `SetHostnameAsFQDN` [feature gate](/docs/reference/command-line-tools-reference/feature-gates/)
+must be enabled for the
+{{< glossary_tooltip text="API Server" term_id="kube-apiserver" >}}
+
+When a Pod is configured to have fully qualified domain name (FQDN), its hostname is the short hostname. For example, if you have a Pod with the fully qualified domain name `busybox-1.default-subdomain.my-namespace.svc.cluster-domain.example`, then by default the `hostname` command inside that Pod returns `busybox-1` and  the `hostname --fqdn` command returns the FQDN.
+
+When you set `setHostnameAsFQDN: true` in the Pod spec, the kubelet writes the Pod's FQDN into the hostname for that Pod's namespace. In this case, both `hostname` and `hostname --fqdn` return the Pod's FQDN.
+
+{{< note >}}
+In Linux, the hostname field of the kernel (the `nodename` field of `struct utsname`) is limited to 64 characters.
+
+If a Pod enables this feature and its FQDN is longer than 64 character, it will fail to start. The Pod will remain in `Pending` status (`ContainerCreating` as seen by `kubectl`) generating error events, such as Failed to construct FQDN from pod hostname and cluster domain, FQDN `long-FQDN` is too long (64 characters is the max, 70 characters requested). One way of improving user experience for this scenario is to create an [admission webhook controller](/docs/reference/access-authn-authz/extensible-admission-controllers/#admission-webhooks) to control FQDN size when users create top level objects, for example, Deployment.
+{{< /note >}}
+
 ### Pod's DNS Policy
 
 DNS policies can be set on a per-pod basis. Currently Kubernetes supports the
@@ -182,7 +209,7 @@ following pod-specific DNS policies. These policies are specified in the
 
 {{< note >}}
 "Default" is not the default DNS policy. If `dnsPolicy` is not
-explicitly specified, then “ClusterFirst” is used.
+explicitly specified, then "ClusterFirst" is used.
 {{< /note >}}
 
 
@@ -276,4 +303,3 @@ The availability of Pod DNS Config and DNS Policy "`None`" is shown as below.
 
 For guidance on administering DNS configurations, check
 [Configure DNS Service](/docs/tasks/administer-cluster/dns-custom-nameservers/)
-

