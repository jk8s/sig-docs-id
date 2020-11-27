diff --git a/content/en/docs/concepts/workloads/pods/pod-topology-spread-constraints.md b/content/en/docs/concepts/workloads/pods/pod-topology-spread-constraints.md
index 622d6a614..e3a30b3f8 100644
--- a/content/en/docs/concepts/workloads/pods/pod-topology-spread-constraints.md
+++ b/content/en/docs/concepts/workloads/pods/pod-topology-spread-constraints.md
@@ -4,11 +4,21 @@ content_type: concept
 weight: 40
 ---
 
+{{< feature-state for_k8s_version="v1.19" state="stable" >}}
+<!-- leave this shortcode in place until the note about EvenPodsSpread is
+obsolete -->
+
 <!-- overview -->
 
 You can use _topology spread constraints_ to control how {{< glossary_tooltip text="Pods" term_id="Pod" >}} are spread across your cluster among failure-domains such as regions, zones, nodes, and other user-defined topology domains. This can help to achieve high availability as well as efficient resource utilization.
 
-
+{{< note >}}
+In versions of Kubernetes before v1.19, you must enable the `EvenPodsSpread`
+[feature gate](/docs/reference/command-line-tools-reference/feature-gates/) on
+the [API server](/docs/concepts/overview/components/#kube-apiserver) and the
+[scheduler](/docs/reference/generated/kube-scheduler/) in order to use Pod
+topology spread constraints.
+{{< /note >}}
 
 <!-- body -->
 
@@ -274,8 +284,6 @@ There are some implicit conventions worth noting here:
 
 ### Cluster-level default constraints
 
-{{< feature-state for_k8s_version="v1.19" state="beta" >}}
-
 It is possible to set default topology spread constraints for a cluster. Default
 topology spread constraints are applied to a Pod if, and only if:
 

