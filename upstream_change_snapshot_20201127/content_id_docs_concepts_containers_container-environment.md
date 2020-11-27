diff --git a/content/en/docs/concepts/containers/container-environment.md b/content/en/docs/concepts/containers/container-environment.md
index a57ac2181..7ec28e97b 100644
--- a/content/en/docs/concepts/containers/container-environment.md
+++ b/content/en/docs/concepts/containers/container-environment.md
@@ -28,7 +28,7 @@ The Kubernetes Container environment provides several important resources to Con
 
 The *hostname* of a Container is the name of the Pod in which the Container is running.
 It is available through the `hostname` command or the
-[`gethostname`](http://man7.org/linux/man-pages/man2/gethostname.2.html)
+[`gethostname`](https://man7.org/linux/man-pages/man2/gethostname.2.html)
 function call in libc.
 
 The Pod name and namespace are available as environment variables through the
@@ -51,7 +51,7 @@ FOO_SERVICE_PORT=<the port the service is running on>
 ```
 
 Services have dedicated IP addresses and are available to the Container via DNS,
-if [DNS addon](http://releases.k8s.io/{{< param "githubbranch" >}}/cluster/addons/dns/) is enabled. 
+if [DNS addon](https://releases.k8s.io/{{< param "githubbranch" >}}/cluster/addons/dns/) is enabled. 
 
 
 

