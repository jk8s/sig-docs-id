diff --git a/content/en/docs/concepts/workloads/pods/disruptions.md b/content/en/docs/concepts/workloads/pods/disruptions.md
index 589bde566..78e8b39a4 100644
--- a/content/en/docs/concepts/workloads/pods/disruptions.md
+++ b/content/en/docs/concepts/workloads/pods/disruptions.md
@@ -11,17 +11,14 @@ weight: 60
 <!-- overview -->
 This guide is for application owners who want to build
 highly available applications, and thus need to understand
-what types of Disruptions can happen to Pods.
+what types of disruptions can happen to Pods.
 
-It is also for Cluster Administrators who want to perform automated
+It is also for cluster administrators who want to perform automated
 cluster actions, like upgrading and autoscaling clusters.
 
-
-
-
 <!-- body -->
 
-## Voluntary and Involuntary Disruptions
+## Voluntary and involuntary disruptions
 
 Pods do not disappear until someone (a person or a controller) destroys them, or
 there is an unavoidable hardware or system software error.
@@ -48,7 +45,7 @@ Administrator.  Typical application owner actions include:
 - updating a deployment's pod template causing a restart
 - directly deleting a pod (e.g. by accident)
 
-Cluster Administrator actions include:
+Cluster administrator actions include:
 
 - [Draining a node](/docs/tasks/administer-cluster/safely-drain-node/) for repair or upgrade.
 - Draining a node from a cluster to scale the cluster down (learn about
@@ -68,19 +65,19 @@ Not all voluntary disruptions are constrained by Pod Disruption Budgets. For exa
 deleting deployments or pods bypasses Pod Disruption Budgets.
 {{< /caution >}}
 
-## Dealing with Disruptions
+## Dealing with disruptions
 
 Here are some ways to mitigate involuntary disruptions:
 
-- Ensure your pod [requests the resources](/docs/tasks/configure-pod-container/assign-cpu-ram-container) it needs.
+- Ensure your pod [requests the resources](/docs/tasks/configure-pod-container/assign-memory-resource) it needs.
 - Replicate your application if you need higher availability.  (Learn about running replicated
-[stateless](/docs/tasks/run-application/run-stateless-application-deployment/)
-and [stateful](/docs/tasks/run-application/run-replicated-stateful-application/) applications.)
+  [stateless](/docs/tasks/run-application/run-stateless-application-deployment/)
+  and [stateful](/docs/tasks/run-application/run-replicated-stateful-application/) applications.)
 - For even higher availability when running replicated applications,
-spread applications across racks (using
-[anti-affinity](/docs/user-guide/node-selection/#inter-pod-affinity-and-anti-affinity-beta-feature))
-or across zones (if using a
-[multi-zone cluster](/docs/setup/multiple-zones).)
+  spread applications across racks (using
+  [anti-affinity](/docs/user-guide/node-selection/#inter-pod-affinity-and-anti-affinity-beta-feature))
+  or across zones (if using a
+  [multi-zone cluster](/docs/setup/multiple-zones).)
 
 The frequency of voluntary disruptions varies.  On a basic Kubernetes cluster, there are
 no voluntary disruptions at all.  However, your cluster administrator or hosting provider
@@ -90,58 +87,58 @@ of cluster (node) autoscaling may cause voluntary disruptions to defragment and
 Your cluster administrator or hosting provider should have documented what level of voluntary
 disruptions, if any, to expect.
 
-Kubernetes offers features to help run highly available applications at the same
-time as frequent voluntary disruptions.  We call this set of features
-*Disruption Budgets*.
 
-
-## How Disruption Budgets Work
+## Pod disruption budgets
 
 {{< feature-state for_k8s_version="v1.5" state="beta" >}}
 
-An Application Owner can create a `PodDisruptionBudget` object (PDB) for each application.
-A PDB limits the number of pods of a replicated application that are down simultaneously from
-voluntary disruptions.  For example, a quorum-based application would
+Kubernetes offers features to help you run highly available applications even when you
+introduce frequent voluntary disruptions.
+
+As an application owner, you can create a PodDisruptionBudget (PDB) for each application.
+A PDB limits the number of Pods of a replicated application that are down simultaneously from
+voluntary disruptions. For example, a quorum-based application would
 like to ensure that the number of replicas running is never brought below the
 number needed for a quorum. A web front end might want to
 ensure that the number of replicas serving load never falls below a certain
 percentage of the total.
 
 Cluster managers and hosting providers should use tools which
-respect Pod Disruption Budgets by calling the [Eviction API](/docs/tasks/administer-cluster/safely-drain-node/#the-eviction-api)
-instead of directly deleting pods or deployments.  Examples are the `kubectl drain` command
-and the Kubernetes-on-GCE cluster upgrade script (`cluster/gce/upgrade.sh`).
+respect PodDisruptionBudgets by calling the [Eviction API](/docs/tasks/administer-cluster/safely-drain-node/#the-eviction-api)
+instead of directly deleting pods or deployments.
 
-When a cluster administrator wants to drain a node
-they use the `kubectl drain` command.  That tool tries to evict all
-the pods on the machine.  The eviction request may be temporarily rejected,
-and the tool periodically retries all failed requests until all pods
-are terminated, or until a configurable timeout is reached.
+For example, the `kubectl drain` subcommand lets you mark a node as going out of
+service. When you run `kubectl drain`, the tool tries to evict all of the Pods on
+the Node you're taking out of service. The eviction request that `kubectl` submits on
+your behalf may be temporarily rejected, so the tool periodically retries all failed
+requests until all Pods on the target node are terminated, or until a configurable timeout
+is reached.
 
 A PDB specifies the number of replicas that an application can tolerate having, relative to how
 many it is intended to have.  For example, a Deployment which has a `.spec.replicas: 5` is
 supposed to have 5 pods at any given time.  If its PDB allows for there to be 4 at a time,
-then the Eviction API will allow voluntary disruption of one, but not two pods, at a time.
+then the Eviction API will allow voluntary disruption of one (but not two) pods at a time.
 
 The group of pods that comprise the application is specified using a label selector, the same
 as the one used by the application's controller (deployment, stateful-set, etc).
 
-The "intended" number of pods is computed from the `.spec.replicas` of the pods controller.
-The controller is discovered from the pods using the `.metadata.ownerReferences` of the object.
+The "intended" number of pods is computed from the `.spec.replicas` of the workload resource
+that is managing those pods. The control plane discovers the owning workload resource by
+examining the `.metadata.ownerReferences` of the Pod.
 
 PDBs cannot prevent [involuntary disruptions](#voluntary-and-involuntary-disruptions) from
 occurring, but they do count against the budget.
 
 Pods which are deleted or unavailable due to a rolling upgrade to an application do count
-against the disruption budget, but controllers (like deployment and stateful-set)
-are not limited by PDBs when doing rolling upgrades -- the handling of failures
-during application updates is configured in the controller spec.
-(Learn about [updating a deployment](/docs/concepts/workloads/controllers/deployment/#updating-a-deployment).)
+against the disruption budget, but workload resources (such as Deployment and StatefulSet)
+are not limited by PDBs when doing rolling upgrades. Instead, the handling of failures
+during application updates is configured in the spec for the specific workload resource.
 
-When a pod is evicted using the eviction API, it is gracefully terminated (see
-`terminationGracePeriodSeconds` in [PodSpec](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#podspec-v1-core).)
+When a pod is evicted using the eviction API, it is gracefully
+[terminated](/docs/concepts/workloads/pods/pod-lifecycle/#pod-termination), honoring the
+`terminationGracePeriodSeconds` setting in its [PodSpec](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#podspec-v1-core).)
 
-## PDB Example
+## PodDisruptionBudget example {#pdb-example}
 
 Consider a cluster with 3 nodes, `node-1` through `node-3`.
 The cluster is running several applications.  One of them has 3 replicas initially called
@@ -272,4 +269,6 @@ the nodes in your cluster, such as a node or system software upgrade, here are s
 
 * Learn more about [draining nodes](/docs/tasks/administer-cluster/safely-drain-node/)
 
+* Learn about [updating a deployment](/docs/concepts/workloads/controllers/deployment/#updating-a-deployment)
+  including steps to maintain its availability during the rollout.
 

