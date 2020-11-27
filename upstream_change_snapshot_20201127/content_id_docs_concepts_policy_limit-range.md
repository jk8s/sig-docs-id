diff --git a/content/en/docs/concepts/policy/limit-range.md b/content/en/docs/concepts/policy/limit-range.md
index 5b670d38a..8158b7843 100644
--- a/content/en/docs/concepts/policy/limit-range.md
+++ b/content/en/docs/concepts/policy/limit-range.md
@@ -8,13 +8,10 @@ weight: 10
 
 <!-- overview -->
 
-By default, containers run with unbounded [compute resources](/docs/user-guide/compute-resources) on a Kubernetes cluster.
+By default, containers run with unbounded [compute resources](/docs/concepts/configuration/manage-resources-containers/) on a Kubernetes cluster.
 With resource quotas, cluster administrators can restrict resource consumption and creation on a {{< glossary_tooltip text="namespace" term_id="namespace" >}} basis.
 Within a namespace, a Pod or Container can consume as much CPU and memory as defined by the namespace's resource quota. There is a concern that one Pod or Container could monopolize all available resources. A LimitRange is a policy to constrain resource allocations (to Pods or Containers) in a namespace.
 
-
-
-
 <!-- body -->
 
 A _LimitRange_ provides constraints that can:
@@ -54,11 +51,8 @@ there may be contention for resources. In this case, the Containers or Pods will
 
 Neither contention nor changes to a LimitRange will affect already created resources.
 
-
-
 ## {{% heading "whatsnext" %}}
 
-
 Refer to the [LimitRanger design document](https://git.k8s.io/community/contributors/design-proposals/resource-management/admission_control_limit_range.md) for more information.
 
 For examples on using limits, see:
@@ -68,7 +62,5 @@ For examples on using limits, see:
 - [how to configure default CPU Requests and Limits per namespace](/docs/tasks/administer-cluster/manage-resources/cpu-default-namespace/).
 - [how to configure default Memory Requests and Limits per namespace](/docs/tasks/administer-cluster/manage-resources/memory-default-namespace/).
 - [how to configure minimum and maximum Storage consumption per namespace](/docs/tasks/administer-cluster/limit-storage-consumption/#limitrange-to-limit-requests-for-storage).
-- a [detailed example on configuring quota per namespace](/docs/tasks/administer-cluster/quota-memory-cpu-namespace/).
-
-
+- a [detailed example on configuring quota per namespace](/docs/tasks/administer-cluster/manage-resources/quota-memory-cpu-namespace/).
 

