diff --git a/content/en/docs/concepts/services-networking/dual-stack.md b/content/en/docs/concepts/services-networking/dual-stack.md
index aa249566b..234e16dc2 100644
--- a/content/en/docs/concepts/services-networking/dual-stack.md
+++ b/content/en/docs/concepts/services-networking/dual-stack.md
@@ -47,6 +47,7 @@ To enable IPv4/IPv6 dual-stack, enable the `IPv6DualStack` [feature gate](/docs/
 
    * kube-apiserver:
       * `--feature-gates="IPv6DualStack=true"`
+      * `--service-cluster-ip-range=<IPv4 CIDR>,<IPv6 CIDR>`
    * kube-controller-manager:
       * `--feature-gates="IPv6DualStack=true"`
       * `--cluster-cidr=<IPv4 CIDR>,<IPv6 CIDR>`
@@ -97,7 +98,7 @@ On cloud providers which support IPv6 enabled external load balancers, setting t
 
 ## Egress Traffic
 
-The use of publicly routable and non-publicly routable IPv6 address blocks is acceptable provided the underlying {{< glossary_tooltip text="CNI" term_id="cni" >}} provider is able to implement the transport. If you have a Pod that uses non-publicly routable IPv6 and want that Pod to reach off-cluster destinations (eg. the public Internet), you must set up IP masquerading for the egress traffic and any replies. The [ip-masq-agent](https://github.com/kubernetes-incubator/ip-masq-agent) is dual-stack aware, so you can use ip-masq-agent for IP masquerading on dual-stack clusters.
+The use of publicly routable and non-publicly routable IPv6 address blocks is acceptable provided the underlying {{< glossary_tooltip text="CNI" term_id="cni" >}} provider is able to implement the transport. If you have a Pod that uses non-publicly routable IPv6 and want that Pod to reach off-cluster destinations (eg. the public Internet), you must set up IP masquerading for the egress traffic and any replies. The [ip-masq-agent](https://github.com/kubernetes-sigs/ip-masq-agent) is dual-stack aware, so you can use ip-masq-agent for IP masquerading on dual-stack clusters.
 
 ## Known Issues
 

