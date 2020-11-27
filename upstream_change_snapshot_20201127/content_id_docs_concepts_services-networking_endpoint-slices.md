diff --git a/content/en/docs/concepts/services-networking/endpoint-slices.md b/content/en/docs/concepts/services-networking/endpoint-slices.md
index 7c66ce007..b028139c1 100644
--- a/content/en/docs/concepts/services-networking/endpoint-slices.md
+++ b/content/en/docs/concepts/services-networking/endpoint-slices.md
@@ -3,7 +3,7 @@ reviewers:
 - freehan
 title: EndpointSlices
 content_type: concept
-weight: 15
+weight: 35
 ---
 
 
@@ -23,7 +23,9 @@ Endpoints.
 
 The Endpoints API has provided a simple and straightforward way of
 tracking network endpoints in Kubernetes. Unfortunately as Kubernetes clusters
-and Services have gotten larger, limitations of that API became more visible.
+and {{< glossary_tooltip text="Services" term_id="service" >}} have grown to handle and
+send more traffic to more backend Pods, limitations of that original API became
+more visible.
 Most notably, those included challenges with scaling to larger numbers of
 network endpoints.
 
@@ -37,11 +39,12 @@ platform for additional features such as topological routing.
 ## EndpointSlice resources {#endpointslice-resource}
 
 In Kubernetes, an EndpointSlice contains references to a set of network
-endpoints. The EndpointSlice controller automatically creates EndpointSlices
-for a Kubernetes Service when a {{< glossary_tooltip text="selector"
-term_id="selector" >}} is specified. These EndpointSlices will include
-references to any Pods that match the Service selector. EndpointSlices group
-network endpoints together by unique Service and Port combinations.
+endpoints. The control plane automatically creates EndpointSlices
+for any Kubernetes Service that has a {{< glossary_tooltip text="selector"
+term_id="selector" >}} specified. These EndpointSlices include
+references to all the Pods that match the Service selector. EndpointSlices group
+network endpoints together by unique combinations of protocol, port number, and
+Service name.  
 The name of a EndpointSlice object must be a valid
 [DNS subdomain name](/docs/concepts/overview/working-with-objects/names#dns-subdomain-names).
 
@@ -71,15 +74,18 @@ endpoints:
       topology.kubernetes.io/zone: us-west2-a
 ```
 
-By default, EndpointSlices managed by the EndpointSlice controller will have no
-more than 100 endpoints each. Below this scale, EndpointSlices should map 1:1
-with Endpoints and Services and have similar performance.
+By default, the control plane creates and manages EndpointSlices to have no
+more than 100 endpoints each. You can configure this with the
+`--max-endpoints-per-slice`
+{{< glossary_tooltip text="kube-controller-manager" term_id="kube-controller-manager" >}}
+flag, up to a maximum of 1000.
 
-EndpointSlices can act as the source of truth for kube-proxy when it comes to
+EndpointSlices can act as the source of truth for
+{{< glossary_tooltip term_id="kube-proxy" text="kube-proxy" >}} when it comes to
 how to route internal traffic. When enabled, they should provide a performance
 improvement for services with large numbers of endpoints.
 
-### Address Types
+### Address types
 
 EndpointSlices support three address types:
 
@@ -87,55 +93,66 @@ EndpointSlices support three address types:
 * IPv6
 * FQDN (Fully Qualified Domain Name)
 
-### Topology
+### Topology information {#topology}
 
 Each endpoint within an EndpointSlice can contain relevant topology information.
 This is used to indicate where an endpoint is, containing information about the
 corresponding Node, zone, and region. When the values are available, the
-following Topology labels will be set by the EndpointSlice controller:
+control plane sets the following Topology labels for EndpointSlices:
 
 * `kubernetes.io/hostname` - The name of the Node this endpoint is on.
-* `topology.kubernetes.io/zone` - The zone this endpoint is in. 
+* `topology.kubernetes.io/zone` - The zone this endpoint is in.
 * `topology.kubernetes.io/region` - The region this endpoint is in.
 
 The values of these labels are derived from resources associated with each
 endpoint in a slice. The hostname label represents the value of the NodeName
 field on the corresponding Pod. The zone and region labels represent the value
-of the labels with the same names on the corresponding Node. 
+of the labels with the same names on the corresponding Node.
 
 ### Management
 
-By default, EndpointSlices are created and managed by the EndpointSlice
-controller. There are a variety of other use cases for EndpointSlices, such as
-service mesh implementations, that could result in other entities or controllers
-managing additional sets of EndpointSlices. To ensure that multiple entities can
-manage EndpointSlices without interfering with each other, a
-`endpointslice.kubernetes.io/managed-by` label is used to indicate the entity
-managing an EndpointSlice. The EndpointSlice controller sets
-`endpointslice-controller.k8s.io` as the value for this label on all
-EndpointSlices it manages. Other entities managing EndpointSlices should also
-set a unique value for this label.
+Most often, the control plane (specifically, the endpoint slice
+{{< glossary_tooltip text="controller" term_id="controller" >}}) creates and
+manages EndpointSlice objects. There are a variety of other use cases for
+EndpointSlices, such as service mesh implementations, that could result in other
+entities or controllers managing additional sets of EndpointSlices.
+
+To ensure that multiple entities can manage EndpointSlices without interfering
+with each other, Kubernetes defines the
+{{< glossary_tooltip term_id="label" text="label" >}}
+`endpointslice.kubernetes.io/managed-by`, which indicates the entity managing
+an EndpointSlice.
+The endpoint slice controller sets `endpointslice-controller.k8s.io` as the value
+for this label on all EndpointSlices it manages. Other entities managing
+EndpointSlices should also set a unique value for this label.
 
 ### Ownership
 
-In most use cases, EndpointSlices will be owned by the Service that it tracks
-endpoints for. This is indicated by an owner reference on each EndpointSlice as
-well as a `kubernetes.io/service-name` label that enables simple lookups of all
-EndpointSlices belonging to a Service.
+In most use cases, EndpointSlices are owned by the Service that the endpoint
+slice object tracks endpoints for. This ownership is indicated by an owner
+reference on each EndpointSlice as well as a `kubernetes.io/service-name`
+label that enables simple lookups of all EndpointSlices belonging to a Service.
 
-## EndpointSlice Controller
+### EndpointSlice mirroring
 
-The EndpointSlice controller watches Services and Pods to ensure corresponding
-EndpointSlices are up to date. The controller will manage EndpointSlices for
-every Service with a selector specified. These will represent the IPs of Pods
-matching the Service selector.
+In some cases, applications create custom Endpoints resources. To ensure that
+these applications do not need to concurrently write to both Endpoints and
+EndpointSlice resources, the cluster's control plane mirrors most Endpoints
+resources to corresponding EndpointSlices.
 
-### Size of EndpointSlices
+The control plane mirrors Endpoints resources unless:
 
-By default, EndpointSlices are limited to a size of 100 endpoints each. You can
-configure this with the `--max-endpoints-per-slice` {{< glossary_tooltip
-text="kube-controller-manager" term_id="kube-controller-manager" >}} flag up to
-a maximum of 1000.
+* the Endpoints resource has a `endpointslice.kubernetes.io/skip-mirror` label
+  set to `true`.
+* the Endpoints resource has a `control-plane.alpha.kubernetes.io/leader`
+  annotation.
+* the corresponding Service resource does not exist.
+* the corresponding Service resource has a non-nil selector.
+
+Individual Endpoints resources may translate into multiple EndpointSlices. This
+will occur if an Endpoints resource has multiple subsets or includes endpoints
+with multiple IP families (IPv4 and IPv6). A maximum of 1000 addresses per
+subset will be mirrored to EndpointSlices.
 
 ### Distribution of EndpointSlices
 
@@ -145,8 +162,8 @@ different target port numbers for the same named port, requiring different
 EndpointSlices. This is similar to the logic behind how subsets are grouped
 with Endpoints.
 
-The controller tries to fill EndpointSlices as full as possible, but does not
-actively rebalance them. The logic of the controller is fairly straightforward:
+The control plane tries to fill EndpointSlices as full as possible, but does not
+actively rebalance them. The logic is fairly straightforward:
 
 1. Iterate through existing EndpointSlices, remove endpoints that are no longer
    desired and update matching endpoints that have changed.
@@ -154,7 +171,7 @@ actively rebalance them. The logic of the controller is fairly straightforward:
    fill them up with any new endpoints needed.
 3. If there's still new endpoints left to add, try to fit them into a previously
    unchanged slice and/or create new ones.
-   
+
 Importantly, the third step prioritizes limiting EndpointSlice updates over a
 perfectly full distribution of EndpointSlices. As an example, if there are 10
 new endpoints to add and 2 EndpointSlices with room for 5 more endpoints each,
@@ -172,15 +189,20 @@ In practice, this less than ideal distribution should be rare. Most changes
 processed by the EndpointSlice controller will be small enough to fit in an
 existing EndpointSlice, and if not, a new EndpointSlice is likely going to be
 necessary soon anyway. Rolling updates of Deployments also provide a natural
-repacking of EndpointSlices with all pods and their corresponding endpoints
+repacking of EndpointSlices with all Pods and their corresponding endpoints
 getting replaced.
 
+### Duplicate endpoints
 
+Due to the nature of EndpointSlice changes, endpoints may be represented in more
+than one EndpointSlice at the same time. This naturally occurs as changes to
+different EndpointSlice objects can arrive at the Kubernetes client watch/cache
+at different times. Implementations using EndpointSlice must be able to have the
+endpoint appear in more than one slice. A reference implementation of how to
+perform endpoint deduplication can be found in the `EndpointSliceCache`
+implementation in `kube-proxy`.
 
 ## {{% heading "whatsnext" %}}
 
-
-* [Enabling EndpointSlices](/docs/tasks/administer-cluster/enabling-endpointslices)
+* Learn about [Enabling EndpointSlices](/docs/tasks/administer-cluster/enabling-endpointslices)
 * Read [Connecting Applications with Services](/docs/concepts/services-networking/connect-applications-service/)
-
-

