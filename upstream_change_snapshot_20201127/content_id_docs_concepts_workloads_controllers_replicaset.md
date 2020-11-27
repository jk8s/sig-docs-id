diff --git a/content/en/docs/concepts/workloads/controllers/replicaset.md b/content/en/docs/concepts/workloads/controllers/replicaset.md
index ef2a069ca..ba0270b57 100644
--- a/content/en/docs/concepts/workloads/controllers/replicaset.md
+++ b/content/en/docs/concepts/workloads/controllers/replicaset.md
@@ -5,7 +5,7 @@ reviewers:
 - madhusudancs
 title: ReplicaSet
 content_type: concept
-weight: 10
+weight: 20
 ---
 
 <!-- overview -->
@@ -233,7 +233,7 @@ A ReplicaSet also needs a [`.spec` section](https://git.k8s.io/community/contrib
 
 ### Pod Template
 
-The `.spec.template` is a [pod template](/docs/concepts/workloads/Pods/pod-overview/#pod-templates) which is also
+The `.spec.template` is a [pod template](/docs/concepts/workloads/pods/#pod-templates) which is also
 required to have labels in place. In our `frontend.yaml` example we had one label: `tier: frontend`.
 Be careful not to overlap with the selectors of other controllers, lest they try to adopt this Pod.
 
@@ -245,9 +245,10 @@ For the template's [restart policy](/docs/concepts/workloads/Pods/pod-lifecycle/
 The `.spec.selector` field is a [label selector](/docs/concepts/overview/working-with-objects/labels/). As discussed
 [earlier](#how-a-replicaset-works) these are the labels used to identify potential Pods to acquire. In our
 `frontend.yaml` example, the selector was:
-```shell
+
+```yaml
 matchLabels:
-	tier: frontend
+  tier: frontend
 ```
 
 In the ReplicaSet, `.spec.template.metadata.labels` must match `spec.selector`, or it will
@@ -295,7 +296,7 @@ curl -X DELETE  'localhost:8080/apis/apps/v1/namespaces/default/replicasets/fron
 Once the original is deleted, you can create a new ReplicaSet to replace it.  As long
 as the old and new `.spec.selector` are the same, then the new one will adopt the old Pods.
 However, it will not make any effort to make existing Pods match a new, different pod template.
-To update Pods to a new spec in a controlled way, use a 
+To update Pods to a new spec in a controlled way, use a
 [Deployment](/docs/concepts/workloads/controllers/deployment/#creating-a-deployment), as ReplicaSets do not support a rolling update directly.
 
 ### Isolating Pods from a ReplicaSet
@@ -340,7 +341,7 @@ kubectl autoscale rs frontend --max=10 --min=3 --cpu-percent=50
 [`Deployment`](/docs/concepts/workloads/controllers/deployment/) is an object which can own ReplicaSets and update
 them and their Pods via declarative, server-side rolling updates.
 While ReplicaSets can be used independently, today they're  mainly used by Deployments as a mechanism to orchestrate Pod
-creation, deletion and updates. When you use Deployments you don’t have to worry about managing the ReplicaSets that
+creation, deletion and updates. When you use Deployments you don't have to worry about managing the ReplicaSets that
 they create. Deployments own and manage their ReplicaSets.
 As such, it is recommended to use Deployments when you want ReplicaSets.
 
@@ -350,7 +351,7 @@ Unlike the case where a user directly created Pods, a ReplicaSet replaces Pods t
 
 ### Job
 
-Use a [`Job`](/docs/concepts/jobs/run-to-completion-finite-workloads/) instead of a ReplicaSet for Pods that are expected to terminate on their own
+Use a [`Job`](/docs/concepts/workloads/controllers/job/) instead of a ReplicaSet for Pods that are expected to terminate on their own
 (that is, batch jobs).
 
 ### DaemonSet

