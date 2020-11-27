diff --git a/content/en/docs/tasks/configure-pod-container/assign-memory-resource.md b/content/en/docs/tasks/configure-pod-container/assign-memory-resource.md
index 79bc2b86b..7afb3cb24 100644
--- a/content/en/docs/tasks/configure-pod-container/assign-memory-resource.md
+++ b/content/en/docs/tasks/configure-pod-container/assign-memory-resource.md
@@ -21,7 +21,7 @@ but is not allowed to use more memory than its limit.
 Each node in your cluster must have at least 300 MiB of memory.
 
 A few of the steps on this page require you to run the
-[metrics-server](https://github.com/kubernetes-incubator/metrics-server)
+[metrics-server](https://github.com/kubernetes-sigs/metrics-server)
 service in your cluster. If you have the metrics-server
 running, you can skip those steps.
 

