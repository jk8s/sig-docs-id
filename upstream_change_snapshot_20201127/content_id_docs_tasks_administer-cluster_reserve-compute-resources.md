diff --git a/content/en/docs/tasks/administer-cluster/reserve-compute-resources.md b/content/en/docs/tasks/administer-cluster/reserve-compute-resources.md
index 4f00675c3..b6249f50e 100644
--- a/content/en/docs/tasks/administer-cluster/reserve-compute-resources.md
+++ b/content/en/docs/tasks/administer-cluster/reserve-compute-resources.md
@@ -39,22 +39,7 @@ the kubelet command line option `--reserved-cpus` to set an
 
 ## Node Allocatable
 
-```text
-      Node Capacity
----------------------------
-|     kube-reserved       |
-|-------------------------|
-|     system-reserved     |
-|-------------------------|
-|    eviction-threshold   |
-|-------------------------|
-|                         |
-|      allocatable        |
-|   (available for pods)  |
-|                         |
-|                         |
----------------------------
-```
+![node capacity](/images/docs/node-capacity.svg)
 
 `Allocatable` on a Kubernetes node is defined as the amount of compute resources
 that are available for pods. The scheduler does not over-subscribe

