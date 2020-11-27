diff --git a/content/en/docs/concepts/workloads/controllers/statefulset.md b/content/en/docs/concepts/workloads/controllers/statefulset.md
index 4f8429d66..acdb68165 100644
--- a/content/en/docs/concepts/workloads/controllers/statefulset.md
+++ b/content/en/docs/concepts/workloads/controllers/statefulset.md
@@ -8,7 +8,7 @@ reviewers:
 - smarterclayton
 title: StatefulSets
 content_type: concept
-weight: 40
+weight: 30
 ---
 
 <!-- overview -->
@@ -141,6 +141,18 @@ As each Pod is created, it gets a matching DNS subdomain, taking the form:
 `$(podname).$(governing service domain)`, where the governing service is defined
 by the `serviceName` field on the StatefulSet.
 
+Depending on how DNS is configured in your cluster, you may not be able to look up the DNS
+name for a newly-run Pod immediately. This behavior can occur when other clients in the
+cluster have already sent queries for the hostname of the Pod before it was created.
+Negative caching (normal in DNS) means that the results of previous failed lookups are
+remembered and reused, even after the Pod is running, for at least a few seconds.
+
+If you need to discover Pods promptly after they are created, you have a few options:
+
+- Query the Kubernetes API directly (for example, using a watch) rather than relying on DNS lookups.
+- Decrease the time of caching in your Kubernetes DNS provider (typically this means editing the config map for CoreDNS, which currently caches for 30 seconds).
+
+
 As mentioned in the [limitations](#limitations) section, you are responsible for
 creating the [Headless Service](/docs/concepts/services-networking/service/#headless-services)
 responsible for the network identity of the pods.
@@ -188,7 +200,7 @@ The StatefulSet should not specify a `pod.Spec.TerminationGracePeriodSeconds` of
 
 When the nginx example above is created, three Pods will be deployed in the order
 web-0, web-1, web-2. web-1 will not be deployed before web-0 is
-[Running and Ready](/docs/user-guide/pod-states/), and web-2 will not be deployed until
+[Running and Ready](/docs/concepts/workloads/pods/pod-lifecycle/), and web-2 will not be deployed until
 web-1 is Running and Ready. If web-0 should fail, after web-1 is Running and Ready, but before
 web-2 is launched, web-2 will not be launched until web-0 is successfully relaunched and
 becomes Running and Ready.
@@ -278,5 +290,3 @@ StatefulSet will then begin to recreate the Pods using the reverted template.
 * Follow an example of [deploying Cassandra with Stateful Sets](/docs/tutorials/stateful-application/cassandra/).
 * Follow an example of [running a replicated stateful application](/docs/tasks/run-application/run-replicated-stateful-application/).
 
-
-

