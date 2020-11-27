diff --git a/content/en/docs/concepts/architecture/cloud-controller.md b/content/en/docs/concepts/architecture/cloud-controller.md
index 9a731b684..d97fc94a4 100644
--- a/content/en/docs/concepts/architecture/cloud-controller.md
+++ b/content/en/docs/concepts/architecture/cloud-controller.md
@@ -23,7 +23,7 @@ mechanism that allows different cloud providers to integrate their platforms wit
 
 ## Design
 
-![Kubernetes components](/images/docs/components-of-kubernetes.png)
+![Kubernetes components](/images/docs/components-of-kubernetes.svg)
 
 The cloud controller manager runs in the control plane as a replicated set of processes
 (usually, these are containers in Pods). Each cloud-controller-manager implements

