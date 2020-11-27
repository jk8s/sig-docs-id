diff --git a/content/en/docs/concepts/workloads/pods/init-containers.md b/content/en/docs/concepts/workloads/pods/init-containers.md
index 6e67a9e0c..5c92f0742 100644
--- a/content/en/docs/concepts/workloads/pods/init-containers.md
+++ b/content/en/docs/concepts/workloads/pods/init-containers.md
@@ -28,8 +28,8 @@ Init containers are exactly like regular containers, except:
 * Init containers always run to completion.
 * Each init container must complete successfully before the next one starts.
 
-If a Pod's init container fails, Kubernetes repeatedly restarts the Pod until the init container
-succeeds. However, if the Pod has a `restartPolicy` of Never, Kubernetes does not restart the Pod.
+If a Pod's init container fails, the kubelet repeatedly restarts that init container until it succeeds. 
+However, if the Pod has a `restartPolicy` of Never, and an init container fails during startup of that Pod, Kubernetes treats the overall Pod as failed.
 
 To specify an init container for a Pod, add the `initContainers` field into
 the Pod specification, as an array of objects of type

