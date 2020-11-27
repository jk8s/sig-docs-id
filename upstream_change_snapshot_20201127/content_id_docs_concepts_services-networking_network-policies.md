diff --git a/content/en/docs/concepts/services-networking/network-policies.md b/content/en/docs/concepts/services-networking/network-policies.md
index 774d7b780..7d417e4df 100644
--- a/content/en/docs/concepts/services-networking/network-policies.md
+++ b/content/en/docs/concepts/services-networking/network-policies.md
@@ -10,12 +10,12 @@ weight: 50
 
 <!-- overview -->
 
-If you want to control traffic flow at the IP address or port level (OSI layer 3 or 4), then you might consider using Kubernetes NetworkPolicies for particular applications in your cluster.  NetworkPolicies are an application-centric construct which allow you to specify how a {{< glossary_tooltip text="pod" term_id="pod">}} is allowed to communicate with various network "entities" (we use the word "entity" here to avoid overloading the more common terms such as "endpoints" and "services", which have specific Kubernetes connotations) over the network. 
+If you want to control traffic flow at the IP address or port level (OSI layer 3 or 4), then you might consider using Kubernetes NetworkPolicies for particular applications in your cluster.  NetworkPolicies are an application-centric construct which allow you to specify how a {{< glossary_tooltip text="pod" term_id="pod">}} is allowed to communicate with various network "entities" (we use the word "entity" here to avoid overloading the more common terms such as "endpoints" and "services", which have specific Kubernetes connotations) over the network.
 
 The entities that a Pod can communicate with are identified through a combination of the following 3 identifiers:
 
 1. Other pods that are allowed (exception: a pod cannot block access to itself)
-2. Namespaces that are allowed 
+2. Namespaces that are allowed
 3. IP blocks (exception: traffic to and from the node where a Pod is running is always allowed, regardless of the IP address of the Pod or the node)
 
 When defining a pod- or namespace- based NetworkPolicy, you use a {{< glossary_tooltip text="selector" term_id="selector">}} to specify what traffic is allowed to and from the Pod(s) that match the selector.
@@ -219,14 +219,14 @@ When the feature gate is enabled, you can set the `protocol` field of a NetworkP
 You must be using a {{< glossary_tooltip text="CNI" term_id="cni" >}} plugin that supports SCTP protocol NetworkPolicies.
 {{< /note >}}
 
-# What you CAN'T do with network policies (at least, not yet)
+## What you can't do with network policies (at least, not yet)
 
 As of Kubernetes 1.20, the following functionality does not exist in the NetworkPolicy API, but you might be able to implement workarounds using Operating System components (such as SELinux, OpenVSwitch, IPTables, and so on) or Layer 7 technologies (Ingress controllers, Service Mesh implementations) or admission controllers.  In case you are new to network security in Kubernetes, its worth noting that the following User Stories cannot (yet) be implemented using the NetworkPolicy API.  Some (but not all) of these user stories are actively being discussed for future releases of the NetworkPolicy API.
 
 - Forcing internal cluster traffic to go through a common gateway (this might be best served with a service mesh or other proxy).
 - Anything TLS related (use a service mesh or ingress controller for this).
 - Node specific policies (you can use CIDR notation for these, but you cannot target nodes by their Kubernetes identities specifically).
-- Targeting of namespaces or services by name (you can, however, target pods or namespaces by their{{< glossary_tooltip text="labels" term_id="label" >}}, which is often a viable workaround).
+- Targeting of namespaces or services by name (you can, however, target pods or namespaces by their {{< glossary_tooltip text="labels" term_id="label" >}}, which is often a viable workaround).
 - Creation or management of "Policy requests" that are fulfilled by a third party.
 - Default policies which are applied to all namespaces or pods (there are some third party Kubernetes distributions and projects which can do this).
 - Advanced policy querying and reachability tooling.

