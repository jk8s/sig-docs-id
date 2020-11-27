diff --git a/content/en/docs/tasks/run-application/force-delete-stateful-set-pod.md b/content/en/docs/tasks/run-application/force-delete-stateful-set-pod.md
index e706c6179..cda469f21 100644
--- a/content/en/docs/tasks/run-application/force-delete-stateful-set-pod.md
+++ b/content/en/docs/tasks/run-application/force-delete-stateful-set-pod.md
@@ -37,13 +37,23 @@ You can perform a graceful pod deletion with the following command:
 kubectl delete pods <pod>
 ```
 
-For the above to lead to graceful termination, the Pod **must not** specify a `pod.Spec.TerminationGracePeriodSeconds` of 0. The practice of setting a `pod.Spec.TerminationGracePeriodSeconds` of 0 seconds is unsafe and strongly discouraged for StatefulSet Pods. Graceful deletion is safe and will ensure that the Pod [shuts down gracefully](/docs/concepts/workloads/pods/pod-lifecycle/#pod-termination) before the kubelet deletes the name from the apiserver.
-
-Kubernetes (versions 1.5 or newer) will not delete Pods just because a Node is unreachable. The Pods running on an unreachable Node enter the 'Terminating' or 'Unknown' state after a [timeout](/docs/admin/node/#node-condition). Pods may also enter these states when the user attempts graceful deletion of a Pod on an unreachable Node. The only ways in which a Pod in such a state can be removed from the apiserver are as follows:
-
-   * The Node object is deleted (either by you, or by the [Node Controller](/docs/admin/node)).<br/>
-   * The kubelet on the unresponsive Node starts responding, kills the Pod and removes the entry from the apiserver.<br/>
-   * Force deletion of the Pod by the user.
+For the above to lead to graceful termination, the Pod **must not** specify a
+`pod.Spec.TerminationGracePeriodSeconds` of 0. The practice of setting a
+`pod.Spec.TerminationGracePeriodSeconds` of 0 seconds is unsafe and strongly discouraged
+for StatefulSet Pods. Graceful deletion is safe and will ensure that the Pod
+[shuts down gracefully](/docs/concepts/workloads/pods/pod-lifecycle/#pod-termination)
+before the kubelet deletes the name from the apiserver.
+
+Kubernetes (versions 1.5 or newer) will not delete Pods just because a Node is unreachable.
+The Pods running on an unreachable Node enter the 'Terminating' or 'Unknown' state after a
+[timeout](/docs/concepts/architecture/nodes/#node-condition).
+Pods may also enter these states when the user attempts graceful deletion of a Pod
+on an unreachable Node.
+The only ways in which a Pod in such a state can be removed from the apiserver are as follows:
+
+* The Node object is deleted (either by you, or by the [Node Controller](/docs/concepts/architecture/nodes/)).
+* The kubelet on the unresponsive Node starts responding, kills the Pod and removes the entry from the apiserver.
+* Force deletion of the Pod by the user.
 
 The recommended best practice is to use the first or second approach. If a Node is confirmed to be dead (e.g. permanently disconnected from the network, powered down, etc), then delete the Node object. If the Node is suffering from a network partition, then try to resolve this or wait for it to resolve. When the partition heals, the kubelet will complete the deletion of the Pod and free up its name in the apiserver.
 

