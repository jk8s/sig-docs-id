diff --git a/content/en/docs/concepts/containers/runtime-class.md b/content/en/docs/concepts/containers/runtime-class.md
index d1857f380..6589590bc 100644
--- a/content/en/docs/concepts/containers/runtime-class.md
+++ b/content/en/docs/concepts/containers/runtime-class.md
@@ -138,9 +138,7 @@ table](https://github.com/cri-o/cri-o/blob/master/docs/crio.conf.5.md#crioruntim
   runtime_path = "${PATH_TO_BINARY}"
 ```
 
-See CRI-O's [config documentation][100] for more details.
-
-[100]: https://raw.githubusercontent.com/cri-o/cri-o/9f11d1d/docs/crio.conf.5.md
+See CRI-O's [config documentation](https://raw.githubusercontent.com/cri-o/cri-o/9f11d1d/docs/crio.conf.5.md) for more details.
 
 ## Scheduling
 
@@ -149,7 +147,8 @@ See CRI-O's [config documentation][100] for more details.
 As of Kubernetes v1.16, RuntimeClass includes support for heterogenous clusters through its
 `scheduling` fields. Through the use of these fields, you can ensure that pods running with this
 RuntimeClass are scheduled to nodes that support it. To use the scheduling support, you must have
-the [RuntimeClass admission controller][] enabled (the default, as of 1.16).
+the [RuntimeClass admission controller](/docs/reference/access-authn-authz/admission-controllers/#runtimeclass)
+enabled (the default, as of 1.16).
 
 To ensure pods land on nodes supporting a specific RuntimeClass, that set of nodes should have a
 common label which is then selected by the `runtimeclass.scheduling.nodeSelector` field. The
@@ -165,8 +164,6 @@ by each.
 To learn more about configuring the node selector and tolerations, see [Assigning Pods to
 Nodes](/docs/concepts/scheduling-eviction/assign-pod-node/).
 
-[RuntimeClass admission controller]: /docs/reference/access-authn-authz/admission-controllers/#runtimeclass
-
 ### Pod Overhead
 
 {{< feature-state for_k8s_version="v1.18" state="beta" >}}
@@ -184,9 +181,9 @@ are accounted for in Kubernetes.
 ## {{% heading "whatsnext" %}}
 
 
-- [RuntimeClass Design](https://github.com/kubernetes/enhancements/blob/master/keps/sig-node/runtime-class.md)
-- [RuntimeClass Scheduling Design](https://github.com/kubernetes/enhancements/blob/master/keps/sig-node/runtime-class-scheduling.md)
-- Read about the [Pod Overhead](/docs/concepts/configuration/pod-overhead/) concept
+- [RuntimeClass Design](https://github.com/kubernetes/enhancements/blob/master/keps/sig-node/585-runtime-class/README.md)
+- [RuntimeClass Scheduling Design](https://github.com/kubernetes/enhancements/blob/master/keps/sig-node/585-runtime-class/README.md#runtimeclass-scheduling)
+- Read about the [Pod Overhead](/docs/concepts/scheduling-eviction/pod-overhead/) concept
 - [PodOverhead Feature Design](https://github.com/kubernetes/enhancements/blob/master/keps/sig-node/20190226-pod-overhead.md)
 
 

