diff --git a/content/en/docs/concepts/workloads/controllers/replicationcontroller.md b/content/en/docs/concepts/workloads/controllers/replicationcontroller.md
index 2cc828494..fa481fb3f 100644
--- a/content/en/docs/concepts/workloads/controllers/replicationcontroller.md
+++ b/content/en/docs/concepts/workloads/controllers/replicationcontroller.md
@@ -10,7 +10,7 @@ feature:
     Restarts containers that fail, replaces and reschedules containers when nodes die, kills containers that don't respond to your user-defined health check, and doesn't advertise them to clients until they are ready to serve.
 
 content_type: concept
-weight: 20
+weight: 90
 ---
 
 <!-- overview -->
@@ -23,9 +23,6 @@ A _ReplicationController_ ensures that a specified number of pod replicas are ru
 time. In other words, a ReplicationController makes sure that a pod or a homogeneous set of pods is
 always up and available.
 
-
-
-
 <!-- body -->
 
 ## How a ReplicationController Works
@@ -126,7 +123,7 @@ A ReplicationController also needs a [`.spec` section](https://git.k8s.io/commun
 
 The `.spec.template` is the only required field of the `.spec`.
 
-The `.spec.template` is a [pod template](/docs/concepts/workloads/pods/pod-overview/#pod-templates). It has exactly the same schema as a [pod](/docs/concepts/workloads/pods/pod/), except it is nested and does not have an `apiVersion` or `kind`.
+The `.spec.template` is a [pod template](/docs/concepts/workloads/pods/#pod-templates). It has exactly the same schema as a {{< glossary_tooltip text="Pod" term_id="pod" >}}, except it is nested and does not have an `apiVersion` or `kind`.
 
 In addition to required fields for a Pod, a pod template in a ReplicationController must specify appropriate
 labels and an appropriate restart policy. For labels, make sure not to overlap with other controllers. See [pod selector](#pod-selector).
@@ -134,7 +131,7 @@ labels and an appropriate restart policy. For labels, make sure not to overlap w
 Only a [`.spec.template.spec.restartPolicy`](/docs/concepts/workloads/pods/pod-lifecycle/#restart-policy) equal to `Always` is allowed, which is the default if not specified.
 
 For local container restarts, ReplicationControllers delegate to an agent on the node,
-for example the [Kubelet](/docs/admin/kubelet/) or Docker.
+for example the [Kubelet](/docs/reference/command-line-tools-reference/kubelet/) or Docker.
 
 ### Labels on the ReplicationController
 
@@ -214,7 +211,7 @@ The ReplicationController makes it easy to scale the number of replicas up or do
 
 The ReplicationController is designed to facilitate rolling updates to a service by replacing pods one-by-one.
 
-As explained in [#1353](http://issue.k8s.io/1353), the recommended approach is to create a new ReplicationController with 1 replica, scale the new (+1) and old (-1) controllers one by one, and then delete the old controller after it reaches 0 replicas. This predictably updates the set of pods regardless of unexpected failures.
+As explained in [#1353](https://issue.k8s.io/1353), the recommended approach is to create a new ReplicationController with 1 replica, scale the new (+1) and old (-1) controllers one by one, and then delete the old controller after it reaches 0 replicas. This predictably updates the set of pods regardless of unexpected failures.
 
 Ideally, the rolling update controller would take application readiness into account, and would ensure that a sufficient number of pods were productively serving at any given time.
 
@@ -239,11 +236,11 @@ Pods created by a ReplicationController are intended to be fungible and semantic
 
 ## Responsibilities of the ReplicationController
 
-The ReplicationController simply ensures that the desired number of pods matches its label selector and are operational. Currently, only terminated pods are excluded from its count. In the future, [readiness](http://issue.k8s.io/620) and other information available from the system may be taken into account, we may add more controls over the replacement policy, and we plan to emit events that could be used by external clients to implement arbitrarily sophisticated replacement and/or scale-down policies.
+The ReplicationController simply ensures that the desired number of pods matches its label selector and are operational. Currently, only terminated pods are excluded from its count. In the future, [readiness](https://issue.k8s.io/620) and other information available from the system may be taken into account, we may add more controls over the replacement policy, and we plan to emit events that could be used by external clients to implement arbitrarily sophisticated replacement and/or scale-down policies.
 
-The ReplicationController is forever constrained to this narrow responsibility. It itself will not perform readiness nor liveness probes. Rather than performing auto-scaling, it is intended to be controlled by an external auto-scaler (as discussed in [#492](http://issue.k8s.io/492)), which would change its `replicas` field. We will not add scheduling policies (for example, [spreading](http://issue.k8s.io/367#issuecomment-48428019)) to the ReplicationController. Nor should it verify that the pods controlled match the currently specified template, as that would obstruct auto-sizing and other automated processes. Similarly, completion deadlines, ordering dependencies, configuration expansion, and other features belong elsewhere. We even plan to factor out the mechanism for bulk pod creation ([#170](http://issue.k8s.io/170)).
+The ReplicationController is forever constrained to this narrow responsibility. It itself will not perform readiness nor liveness probes. Rather than performing auto-scaling, it is intended to be controlled by an external auto-scaler (as discussed in [#492](https://issue.k8s.io/492)), which would change its `replicas` field. We will not add scheduling policies (for example, [spreading](https://issue.k8s.io/367#issuecomment-48428019)) to the ReplicationController. Nor should it verify that the pods controlled match the currently specified template, as that would obstruct auto-sizing and other automated processes. Similarly, completion deadlines, ordering dependencies, configuration expansion, and other features belong elsewhere. We even plan to factor out the mechanism for bulk pod creation ([#170](https://issue.k8s.io/170)).
 
-The ReplicationController is intended to be a composable building-block primitive. We expect higher-level APIs and/or tools to be built on top of it and other complementary primitives for user convenience in the future. The "macro" operations currently supported by kubectl (run, scale) are proof-of-concept examples of this. For instance, we could imagine something like [Asgard](http://techblog.netflix.com/2012/06/asgard-web-based-cloud-management-and.html) managing ReplicationControllers, auto-scalers, services, scheduling policies, canaries, etc.
+The ReplicationController is intended to be a composable building-block primitive. We expect higher-level APIs and/or tools to be built on top of it and other complementary primitives for user convenience in the future. The "macro" operations currently supported by kubectl (run, scale) are proof-of-concept examples of this. For instance, we could imagine something like [Asgard](https://techblog.netflix.com/2012/06/asgard-web-based-cloud-management-and.html) managing ReplicationControllers, auto-scalers, services, scheduling policies, canaries, etc.
 
 
 ## API Object
@@ -257,8 +254,8 @@ API object can be found at:
 ### ReplicaSet
 
 [`ReplicaSet`](/docs/concepts/workloads/controllers/replicaset/) is the next-generation ReplicationController that supports the new [set-based label selector](/docs/concepts/overview/working-with-objects/labels/#set-based-requirement).
-It’s mainly used by [`Deployment`](/docs/concepts/workloads/controllers/deployment/) as a mechanism to orchestrate pod creation, deletion and updates.
-Note that we recommend using Deployments instead of directly using Replica Sets, unless you require custom update orchestration or don’t require updates at all.
+It's mainly used by [Deployment](/docs/concepts/workloads/controllers/deployment/) as a mechanism to orchestrate pod creation, deletion and updates.
+Note that we recommend using Deployments instead of directly using Replica Sets, unless you require custom update orchestration or don't require updates at all.
 
 
 ### Deployment (Recommended)
@@ -271,7 +268,7 @@ Unlike in the case where a user directly created pods, a ReplicationController r
 
 ### Job
 
-Use a [`Job`](/docs/concepts/jobs/run-to-completion-finite-workloads/) instead of a ReplicationController for pods that are expected to terminate on their own
+Use a [`Job`](/docs/concepts/workloads/controllers/job/) instead of a ReplicationController for pods that are expected to terminate on their own
 (that is, batch jobs).
 
 ### DaemonSet
@@ -283,6 +280,6 @@ safe to terminate when the machine is otherwise ready to be rebooted/shutdown.
 
 ## For more information
 
-Read [Run Stateless AP Replication Controller](/docs/tutorials/stateless-application/run-stateless-ap-replication-controller/).
+Read [Run Stateless Application Deployment](/docs/tasks/run-application/run-stateless-application-deployment/).
 
 

