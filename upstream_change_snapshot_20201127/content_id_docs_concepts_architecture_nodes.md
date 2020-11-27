diff --git a/content/en/docs/concepts/architecture/nodes.md b/content/en/docs/concepts/architecture/nodes.md
index 516e4eb6d..337b2107f 100644
--- a/content/en/docs/concepts/architecture/nodes.md
+++ b/content/en/docs/concepts/architecture/nodes.md
@@ -23,8 +23,6 @@ The [components](/docs/concepts/overview/components/#node-components) on a node
 {{< glossary_tooltip text="container runtime" term_id="container-runtime" >}}, and the
 {{< glossary_tooltip text="kube-proxy" term_id="kube-proxy" >}}.
 
-
-
 <!-- body -->
 
 ## Management
@@ -100,7 +98,7 @@ You can modify Node objects regardless of the setting of `--register-node`.
 For example, you can set labels on an existing Node, or mark it unschedulable.
 
 You can use labels on Nodes in conjunction with node selectors on Pods to control
-scheduling. For example, you can to constrain a Pod to only be eligible to run on
+scheduling. For example, you can constrain a Pod to only be eligible to run on
 a subset of the available nodes.
 
 Marking a node as unschedulable prevents the scheduler from placing new pods onto
@@ -195,7 +193,7 @@ The node lifecycle controller automatically creates
 The scheduler takes the Node's taints into consideration when assigning a Pod to a Node.
 Pods can also have tolerations which let them tolerate a Node's taints.
 
-See [Taint Nodes by Condition](/docs/concepts/configuration/taint-and-toleration/#taint-nodes-by-condition)
+See [Taint Nodes by Condition](/docs/concepts/scheduling-eviction/taint-and-toleration/#taint-nodes-by-condition)
 for more details.
 
 ### Capacity and Allocatable {#capacity}
@@ -263,7 +261,7 @@ a Lease object.
 
 #### Reliability
 
- In most cases, node controller limits the eviction rate to
+ In most cases, the node controller limits the eviction rate to
 `--node-eviction-rate` (default 0.1) per second, meaning it won't evict pods
 from more than 1 node per 10 seconds.
 
@@ -339,6 +337,5 @@ for more information.
 * Read the [API definition for Node](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#node-v1-core).
 * Read the [Node](https://git.k8s.io/community/contributors/design-proposals/architecture/architecture.md#the-kubernetes-node)
   section of the architecture design document.
-* Read about [taints and tolerations](/docs/concepts/configuration/taint-and-toleration/).
-* Read about [cluster autoscaling](/docs/tasks/administer-cluster/cluster-management/#cluster-autoscaling).
+* Read about [taints and tolerations](/docs/concepts/scheduling-eviction/taint-and-toleration/).
 

