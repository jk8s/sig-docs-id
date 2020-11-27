diff --git a/content/en/docs/tasks/administer-cluster/dns-custom-nameservers.md b/content/en/docs/tasks/administer-cluster/dns-custom-nameservers.md
index 9fb0452dd..437e58f39 100644
--- a/content/en/docs/tasks/administer-cluster/dns-custom-nameservers.md
+++ b/content/en/docs/tasks/administer-cluster/dns-custom-nameservers.md
@@ -50,7 +50,7 @@ and more. For more information, see [DNS for Services and Pods](/docs/concepts/s
 If a Pod's `dnsPolicy` is set to `default`, it inherits the name resolution
 configuration from the node that the Pod runs on. The Pod's DNS resolution
 should behave the same as the node.
-But see [Known issues](/docs/tasks/debug-application-cluster/dns-debugging-resolution/#known-issues).
+But see [Known issues](/docs/tasks/administer-cluster/dns-debugging-resolution/#known-issues).
 
 If you don't want this, or if you want a different DNS config for pods, you can
 use the kubelet's `--resolv-conf` flag.  Set this flag to "" to prevent Pods from

