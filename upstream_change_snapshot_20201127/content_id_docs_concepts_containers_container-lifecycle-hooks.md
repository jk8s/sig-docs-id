diff --git a/content/en/docs/concepts/containers/container-lifecycle-hooks.md b/content/en/docs/concepts/containers/container-lifecycle-hooks.md
index 386e4d00b..fa74d9422 100644
--- a/content/en/docs/concepts/containers/container-lifecycle-hooks.md
+++ b/content/en/docs/concepts/containers/container-lifecycle-hooks.md
@@ -30,7 +30,7 @@ There are two hooks that are exposed to Containers:
 
 `PostStart`
 
-This hook executes immediately after a container is created.
+This hook is executed immediately after a container is created.
 However, there is no guarantee that the hook will execute before the container ENTRYPOINT.
 No parameters are passed to the handler.
 
@@ -38,11 +38,11 @@ No parameters are passed to the handler.
 
 This hook is called immediately before a container is terminated due to an API request or management event such as liveness probe failure, preemption, resource contention and others. A call to the preStop hook fails if the container is already in terminated or completed state.
 It is blocking, meaning it is synchronous,
-so it must complete before the call to delete the container can be sent.
+so it must complete before the signal to stop the container can be sent.
 No parameters are passed to the handler.
 
 A more detailed description of the termination behavior can be found in
-[Termination of Pods](/docs/concepts/workloads/pods/pod/#termination-of-pods).
+[Termination of Pods](/docs/concepts/workloads/pods/pod-lifecycle/#pod-termination).
 
 ### Hook handler implementations
 
@@ -56,7 +56,8 @@ Resources consumed by the command are counted against the Container.
 ### Hook handler execution
 
 When a Container lifecycle management hook is called,
-the Kubernetes management system executes the handler in the Container registered for that hook. 
+the Kubernetes management system execute the handler according to the hook action,
+`exec` and `tcpSocket` are executed in the container, and `httpGet` is executed by the kubelet process.
 
 Hook handler calls are synchronous within the context of the Pod containing the Container.
 This means that for a `PostStart` hook,
@@ -64,10 +65,21 @@ the Container ENTRYPOINT and hook fire asynchronously.
 However, if the hook takes too long to run or hangs,
 the Container cannot reach a `running` state.
 
-The behavior is similar for a `PreStop` hook.
-If the hook hangs during execution,
-the Pod phase stays in a `Terminating` state and is killed after `terminationGracePeriodSeconds` of pod ends.
-If a `PostStart` or `PreStop` hook fails,
+`PreStop` hooks are not executed asynchronously from the signal
+to stop the Container; the hook must complete its execution before
+the signal can be sent.
+If a `PreStop` hook hangs during execution,
+the Pod's phase will be `Terminating` and remain there until the Pod is
+killed after its `terminationGracePeriodSeconds` expires.
+This grace period applies to the total time it takes for both
+the `PreStop` hook to execute and for the Container to stop normally.
+If, for example, `terminationGracePeriodSeconds` is 60, and the hook
+takes 55 seconds to complete, and the Container takes 10 seconds to stop
+normally after receiving the signal, then the Container will be killed
+before it can stop normally, since `terminationGracePeriodSeconds` is
+less than the total time (55+10) it takes for these two things to happen.
+
+If either a `PostStart` or `PreStop` hook fails,
 it kills the Container.
 
 Users should make their hook handlers as lightweight as possible.
@@ -121,4 +133,3 @@ Events:
 * Get hands-on experience
   [attaching handlers to Container lifecycle events](/docs/tasks/configure-pod-container/attach-handler-lifecycle-event/).
 
-

