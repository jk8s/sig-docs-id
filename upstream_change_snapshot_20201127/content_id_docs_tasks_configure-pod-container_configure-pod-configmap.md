diff --git a/content/en/docs/tasks/configure-pod-container/configure-pod-configmap.md b/content/en/docs/tasks/configure-pod-container/configure-pod-configmap.md
index 42eff59db..2824cce64 100644
--- a/content/en/docs/tasks/configure-pod-container/configure-pod-configmap.md
+++ b/content/en/docs/tasks/configure-pod-container/configure-pod-configmap.md
@@ -532,7 +532,7 @@ This functionality is available in Kubernetes v1.6 and later.
 
 ## Use ConfigMap-defined environment variables in Pod commands
 
-You can use ConfigMap-defined environment variables in the `command` section of the Pod specification using the `$(VAR_NAME)` Kubernetes substitution syntax.
+You can use ConfigMap-defined environment variables in the `command` and `args` of a container using the `$(VAR_NAME)` Kubernetes substitution syntax.
 
 For example, the following Pod specification
 

