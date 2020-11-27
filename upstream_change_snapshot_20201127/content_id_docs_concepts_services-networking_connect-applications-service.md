diff --git a/content/en/docs/concepts/services-networking/connect-applications-service.md b/content/en/docs/concepts/services-networking/connect-applications-service.md
index 79c605330..402c3c57c 100644
--- a/content/en/docs/concepts/services-networking/connect-applications-service.md
+++ b/content/en/docs/concepts/services-networking/connect-applications-service.md
@@ -15,7 +15,7 @@ weight: 30
 
 Now that you have a continuously running, replicated application you can expose it on a network. Before discussing the Kubernetes approach to networking, it is worthwhile to contrast it with the "normal" way networking works with Docker.
 
-By default, Docker uses host-private networking, so containers can talk to other containers only if they are on the same machine. In order for Docker containers to communicate across nodes, there must be allocated ports on the machine’s own IP address, which are then forwarded or proxied to the containers. This obviously means that containers must either coordinate which ports they use very carefully or ports must be allocated dynamically.
+By default, Docker uses host-private networking, so containers can talk to other containers only if they are on the same machine. In order for Docker containers to communicate across nodes, there must be allocated ports on the machine's own IP address, which are then forwarded or proxied to the containers. This obviously means that containers must either coordinate which ports they use very carefully or ports must be allocated dynamically.
 
 Coordinating port allocations across multiple developers or teams that provide containers is very difficult to do at scale, and exposes users to cluster-level issues outside of their control. Kubernetes assumes that pods can communicate with other pods, regardless of which host they land on. Kubernetes gives every pod its own cluster-private IP address, so you do not need to explicitly create links between pods or map container ports to host ports. This means that containers within a Pod can all reach each other's ports on localhost, and all pods in a cluster can see each other without NAT. The rest of this document elaborates on how you can run reliable services on such a networking model.
 
@@ -133,7 +133,7 @@ about the [service proxy](/docs/concepts/services-networking/service/#virtual-ip
 
 Kubernetes supports 2 primary modes of finding a Service - environment variables
 and DNS. The former works out of the box while the latter requires the
-[CoreDNS cluster addon](http://releases.k8s.io/{{< param "githubbranch" >}}/cluster/addons/dns/coredns).
+[CoreDNS cluster addon](https://releases.k8s.io/{{< param "githubbranch" >}}/cluster/addons/dns/coredns).
 {{< note >}}
 If the service environment variables are not desired (because possible clashing with expected program ones,
 too many variables to process, only using DNS, etc) you can disable this mode by setting the `enableServiceLinks`

