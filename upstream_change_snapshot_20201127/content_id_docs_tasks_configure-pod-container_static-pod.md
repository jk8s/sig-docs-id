diff --git a/content/en/docs/tasks/configure-pod-container/static-pod.md b/content/en/docs/tasks/configure-pod-container/static-pod.md
index 5189fdb88..cf31d822d 100644
--- a/content/en/docs/tasks/configure-pod-container/static-pod.md
+++ b/content/en/docs/tasks/configure-pod-container/static-pod.md
@@ -14,7 +14,7 @@ without the {{< glossary_tooltip text="API server" term_id="kube-apiserver" >}}
 observing them.
 Unlike Pods that are managed by the control plane (for example, a
 {{< glossary_tooltip text="Deployment" term_id="deployment" >}});
-instead, the kubelet watches each static Pod (and restarts it if it crashes).
+instead, the kubelet watches each static Pod (and restarts it if it fails).
 
 Static Pods are always bound to one {{< glossary_tooltip term_id="kubelet" >}} on a specific node.
 

