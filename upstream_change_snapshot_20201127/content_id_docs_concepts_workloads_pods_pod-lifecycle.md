diff --git a/content/en/docs/concepts/workloads/pods/pod-lifecycle.md b/content/en/docs/concepts/workloads/pods/pod-lifecycle.md
index d72265faf..3dfa69c5b 100644
--- a/content/en/docs/concepts/workloads/pods/pod-lifecycle.md
+++ b/content/en/docs/concepts/workloads/pods/pod-lifecycle.md
@@ -6,16 +6,61 @@ weight: 30
 
 <!-- overview -->
 
-{{< comment >}}Updated: 4/14/2015{{< /comment >}}
-{{< comment >}}Edited and moved to Concepts section: 2/2/17{{< /comment >}}
-
-This page describes the lifecycle of a Pod.
+This page describes the lifecycle of a Pod. Pods follow a defined lifecycle, starting
+in the `Pending` [phase](#pod-phase), moving through `Running` if at least one
+of its primary containers starts OK, and then through either the `Succeeded` or
+`Failed` phases depending on whether any container in the Pod terminated in failure.
 
+Whilst a Pod is running, the kubelet is able to restart containers to handle some
+kind of faults. Within a Pod, Kubernetes tracks different container
+[states](#container-states) and determines what action to take to make the Pod
+healthy again.
 
+In the Kubernetes API, Pods have both a specification and an actual status. The
+status for a Pod object consists of a set of [Pod conditions](#pod-conditions).
+You can also inject [custom readiness information](#pod-readiness-gate) into the
+condition data for a Pod, if that is useful to your application.
 
+Pods are only [scheduled](/docs/concepts/scheduling-eviction/) once in their lifetime.
+Once a Pod is scheduled (assigned) to a Node, the Pod runs on that Node until it stops
+or is [terminated](#pod-termination).
 
 <!-- body -->
 
+## Pod lifetime
+
+Like individual application containers, Pods are considered to be relatively
+ephemeral (rather than durable) entities. Pods are created, assigned a unique
+ID ([UID](/docs/concepts/overview/working-with-objects/names/#uids)), and scheduled
+to nodes where they remain until termination (according to restart policy) or
+deletion.
+If a {{< glossary_tooltip term_id="node" >}} dies, the Pods scheduled to that node
+are [scheduled for deletion](#pod-garbage-collection) after a timeout period.
+
+Pods do not, by themselves, self-heal. If a Pod is scheduled to a
+{{< glossary_tooltip text="node" term_id="node" >}} that then fails,
+or if the scheduling operation itself fails, the Pod is deleted; likewise, a Pod won't
+survive an eviction due to a lack of resources or Node maintenance. Kubernetes uses a
+higher-level abstraction, called a
+{{< glossary_tooltip term_id="controller" text="controller" >}}, that handles the work of
+managing the relatively disposable Pod instances.
+
+A given Pod (as defined by a UID) is never "rescheduled" to a different node; instead,
+that Pod can be replaced by a new, near-identical Pod, with even the same name if
+desired, but with a different UID.
+
+When something is said to have the same lifetime as a Pod, such as a
+{{< glossary_tooltip term_id="volume" text="volume" >}},
+that means that the thing exists as long as that specific Pod (with that exact UID)
+exists. If that Pod is deleted for any reason, and even if an identical replacement
+is created, the related thing (a volume, in this example) is also destroyed and
+created anew.
+
+{{< figure src="/images/docs/pod.svg" title="Pod diagram" width="50%" >}}
+
+*A multi-container Pod that contains a file puller and a
+web server that uses a persistent volume for shared storage between the containers.*
+
 ## Pod phase
 
 A Pod's `status` field is a
@@ -24,7 +69,7 @@ object, which has a `phase` field.
 
 The phase of a Pod is a simple, high-level summary of where the Pod is in its
 lifecycle. The phase is not intended to be a comprehensive rollup of observations
-of Container or Pod state, nor is it intended to be a comprehensive state machine.
+of container or Pod state, nor is it intended to be a comprehensive state machine.
 
 The number and meanings of Pod phase values are tightly guarded.
 Other than what is documented here, nothing should be assumed about Pods that
@@ -32,190 +77,107 @@ have a given `phase` value.
 
 Here are the possible values for `phase`:
 
-Value | Description
-:-----|:-----------
-`Pending` | The Pod has been accepted by the Kubernetes system, but one or more of the Container images has not been created. This includes time before being scheduled as well as time spent downloading images over the network, which could take a while.
-`Running` | The Pod has been bound to a node, and all of the Containers have been created. At least one Container is still running, or is in the process of starting or restarting.
-`Succeeded` | All Containers in the Pod have terminated in success, and will not be restarted.
-`Failed` | All Containers in the Pod have terminated, and at least one Container has terminated in failure. That is, the Container either exited with non-zero status or was terminated by the system.
-`Unknown` | For some reason the state of the Pod could not be obtained, typically due to an error in communicating with the host of the Pod.
-
-## Pod conditions
-
-A Pod has a PodStatus, which has an array of
-[PodConditions](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#podcondition-v1-core)
-through which the Pod has or has not passed. Each element of the PodCondition
-array has six possible fields:
-
-* The `lastProbeTime` field provides a timestamp for when the Pod condition
-  was last probed.
-
-* The `lastTransitionTime` field provides a timestamp for when the Pod
-  last transitioned from one status to another.
-
-* The `message` field is a human-readable message indicating details
-  about the transition.
-
-* The `reason` field is a unique, one-word, CamelCase reason for the condition's last transition.
-
-* The `status` field is a string, with possible values "`True`", "`False`", and "`Unknown`".
-
-* The `type` field is a string with the following possible values:
-
-  * `PodScheduled`: the Pod has been scheduled to a node;
-  * `Ready`: the Pod is able to serve requests and should be added to the load
-    balancing pools of all matching Services;
-  * `Initialized`: all [init containers](/docs/concepts/workloads/pods/init-containers)
-    have started successfully;
-  * `ContainersReady`: all containers in the Pod are ready.
-
-
-
-## Container probes
-
-A [Probe](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#probe-v1-core) is a diagnostic
-performed periodically by the [kubelet](/docs/admin/kubelet/)
-on a Container. To perform a diagnostic,
-the kubelet calls a
-[Handler](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#handler-v1-core) implemented by
-the Container. There are three types of handlers:
-
-* [ExecAction](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#execaction-v1-core):
-  Executes a specified command inside the Container. The diagnostic
-  is considered successful if the command exits with a status code of 0.
-
-* [TCPSocketAction](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#tcpsocketaction-v1-core):
-  Performs a TCP check against the Container's IP address on
-  a specified port. The diagnostic is considered successful if the port is open.
-
-* [HTTPGetAction](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#httpgetaction-v1-core):
-  Performs an HTTP Get request against the Container's IP
-  address on a specified port and path. The diagnostic is considered successful
-  if the response has a status code greater than or equal to 200 and less than 400.
-
-Each probe has one of three results:
-
-* Success: The Container passed the diagnostic.
-* Failure: The Container failed the diagnostic.
-* Unknown: The diagnostic failed, so no action should be taken.
+Value       | Description
+:-----------|:-----------
+`Pending`   | The Pod has been accepted by the Kubernetes cluster, but one or more of the containers has not been set up and made ready to run. This includes time a Pod spends waiting to be scheduled as well as the time spent downloading container images over the network.
+`Running`   | The Pod has been bound to a node, and all of the containers have been created. At least one container is still running, or is in the process of starting or restarting.
+`Succeeded` | All containers in the Pod have terminated in success, and will not be restarted.
+`Failed`    | All containers in the Pod have terminated, and at least one container has terminated in failure. That is, the container either exited with non-zero status or was terminated by the system.
+`Unknown`   | For some reason the state of the Pod could not be obtained. This phase typically occurs due to an error in communicating with the node where the Pod should be running.
 
-The kubelet can optionally perform and react to three kinds of probes on running
-Containers:
-
-* `livenessProbe`: Indicates whether the Container is running. If
-   the liveness probe fails, the kubelet kills the Container, and the Container
-   is subjected to its [restart policy](#restart-policy). If a Container does not
-   provide a liveness probe, the default state is `Success`.
-
-* `readinessProbe`: Indicates whether the Container is ready to service requests.
-   If the readiness probe fails, the endpoints controller removes the Pod's IP
-   address from the endpoints of all Services that match the Pod. The default
-   state of readiness before the initial delay is `Failure`. If a Container does
-   not provide a readiness probe, the default state is `Success`.
-
-* `startupProbe`: Indicates whether the application within the Container is started.
-   All other probes are disabled if a startup probe is provided, until it succeeds.
-   If the startup probe fails, the kubelet kills the Container, and the Container
-   is subjected to its [restart policy](#restart-policy). If a Container does not
-   provide a startup probe, the default state is `Success`.
-
-### When should you use a liveness probe?
-
-{{< feature-state for_k8s_version="v1.0" state="stable" >}}
-
-If the process in your Container is able to crash on its own whenever it
-encounters an issue or becomes unhealthy, you do not necessarily need a liveness
-probe; the kubelet will automatically perform the correct action in accordance
-with the Pod's `restartPolicy`.
+If a node dies or is disconnected from the rest of the cluster, Kubernetes
+applies a policy for setting the `phase` of all Pods on the lost node to Failed.
 
-If you'd like your Container to be killed and restarted if a probe fails, then
-specify a liveness probe, and specify a `restartPolicy` of Always or OnFailure.
+## Container states
 
-### When should you use a readiness probe?
+As well as the [phase](#pod-phase) of the Pod overall, Kubernetes tracks the state of
+each container inside a Pod. You can use
+[container lifecycle hooks](/docs/concepts/containers/container-lifecycle-hooks/) to
+trigger events to run at certain points in a container's lifecycle.
 
-{{< feature-state for_k8s_version="v1.0" state="stable" >}}
+Once the {{< glossary_tooltip text="scheduler" term_id="kube-scheduler" >}}
+assigns a Pod to a Node, the kubelet starts creating containers for that Pod
+using a {{< glossary_tooltip text="container runtime" term_id="container-runtime" >}}.
+There are three possible container states: `Waiting`, `Running`, and `Terminated`.
 
-If you'd like to start sending traffic to a Pod only when a probe succeeds,
-specify a readiness probe. In this case, the readiness probe might be the same
-as the liveness probe, but the existence of the readiness probe in the spec means
-that the Pod will start without receiving any traffic and only start receiving
-traffic after the probe starts succeeding.
-If your Container needs to work on loading large data, configuration files, or migrations during startup, specify a readiness probe.
+To check the state of a Pod's containers, you can use
+`kubectl describe pod <name-of-pod>`. The output shows the state for each container
+within that Pod.
 
-If you want your Container to be able to take itself down for maintenance, you
-can specify a readiness probe that checks an endpoint specific to readiness that
-is different from the liveness probe.
+Each state has a specific meaning:
 
-Note that if you just want to be able to drain requests when the Pod is deleted,
-you do not necessarily need a readiness probe; on deletion, the Pod automatically
-puts itself into an unready state regardless of whether the readiness probe exists.
-The Pod remains in the unready state while it waits for the Containers in the Pod
-to stop.
+### `Waiting` {#container-state-waiting}
 
-### When should you use a startup probe?
+If a container is not in either the `Running` or `Terminated` state, it is `Waiting`.
+A container in the `Waiting` state is still running the operations it requires in
+order to complete start up: for example, pulling the container image from a container
+image registry, or applying {{< glossary_tooltip text="Secret" term_id="secret" >}}
+data.
+When you use `kubectl` to query a Pod with a container that is `Waiting`, you also see
+a Reason field to summarize why the container is in that state.
 
-{{< feature-state for_k8s_version="v1.16" state="alpha" >}}
+### `Running` {#container-state-running}
 
-If your Container usually starts in more than `initialDelaySeconds + failureThreshold × periodSeconds`, you should specify a startup probe that checks the same endpoint as the liveness probe. The default for `periodSeconds` is 30s.
-You should then set its `failureThreshold` high enough to allow the Container to start, without changing the default values of the liveness probe. This helps to protect against deadlocks.
+The `Running` status indicates that a container is executing without issues. If there
+was a `postStart` hook configured, it has already executed and finished. When you use
+`kubectl` to query a Pod with a container that is `Running`, you also see information
+about when the container entered the `Running` state.
 
-For more information about how to set up a liveness, readiness, startup probe, see
-[Configure Liveness, Readiness and Startup Probes](/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/).
+### `Terminated` {#container-state-terminated}
 
-## Pod and Container status
+A container in the `Terminated` state began execution and then either ran to
+completion or failed for some reason. When you use `kubectl` to query a Pod with
+a container that is `Terminated`, you see a reason, an exit code, and the start and
+finish time for that container's period of execution.
 
-For detailed information about Pod Container status, see
-[PodStatus](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#podstatus-v1-core)
-and
-[ContainerStatus](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#containerstatus-v1-core).
-Note that the information reported as Pod status depends on the current
-[ContainerState](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#containerstatus-v1-core).
+If a container has a `preStop` hook configured, that runs before the container enters
+the `Terminated` state.
 
-## Container States
+## Container restart policy {#restart-policy}
 
-Once Pod is assigned to a node by scheduler, kubelet starts creating containers using container runtime.There are three possible states of containers: Waiting, Running and Terminated. To check state of container, you can use `kubectl describe pod [POD_NAME]`. State is displayed for each container within that Pod.
+The `spec` of a Pod has a `restartPolicy` field with possible values Always, OnFailure,
+and Never. The default value is Always.
 
-* `Waiting`: Default state of container. If container is not in either Running or Terminated state, it is in Waiting state. A container in Waiting state still runs its required operations, like pulling images, applying Secrets, etc. Along with this state, a message and reason about the state are displayed to provide more information.
+The `restartPolicy` applies to all containers in the Pod. `restartPolicy` only
+refers to restarts of the containers by the kubelet on the same node. After containers
+in a Pod exit, the kubelet restarts them with an exponential back-off delay (10s, 20s,
+40s, …), that is capped at five minutes. Once a container has executed for 10 minutes
+without any problems, the kubelet resets the restart backoff timer for that container.
 
-    ```yaml
-   ...
-      State:          Waiting
-       Reason:       ErrImagePull
-   ...
-   ```
+## Pod conditions
 
-* `Running`: Indicates that the container is executing without issues. The `postStart` hook (if any) is executed prior to the container entering a Running state. This state also displays the time when the container entered Running state.
+A Pod has a PodStatus, which has an array of
+[PodConditions](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#podcondition-v1-core)
+through which the Pod has or has not passed:
 
-   ```yaml
-   ...
-      State:          Running
-       Started:      Wed, 30 Jan 2019 16:46:38 +0530
-   ...
-   ```
+* `PodScheduled`: the Pod has been scheduled to a node.
+* `ContainersReady`: all containers in the Pod are ready.
+* `Initialized`: all [init containers](/docs/concepts/workloads/pods/init-containers/)
+  have started successfully.
+* `Ready`: the Pod is able to serve requests and should be added to the load
+  balancing pools of all matching Services.
 
-* `Terminated`:  Indicates that the container completed its execution and has stopped running. A container enters into this when it has successfully completed execution or when it has failed for some reason. Regardless, a reason and exit code is displayed, as well as the container's start and finish time. Before a container enters into Terminated, `preStop` hook (if any) is executed.
+Field name           | Description
+:--------------------|:-----------
+`type`               | Name of this Pod condition.
+`status`             | Indicates whether that condition is applicable, with possible values "`True`", "`False`", or "`Unknown`".
+`lastProbeTime`      | Timestamp of when the Pod condition was last probed.
+`lastTransitionTime` | Timestamp for when the Pod last transitioned from one status to another.
+`reason`             | Machine-readable, UpperCamelCase text indicating the reason for the condition's last transition.
+`message`            | Human-readable message indicating details about the last status transition.
 
-   ```yaml
-   ...
-      State:          Terminated
-        Reason:       Completed
-        Exit Code:    0
-        Started:      Wed, 30 Jan 2019 11:45:26 +0530
-        Finished:     Wed, 30 Jan 2019 11:45:26 +0530
-    ...
-   ```
 
-## Pod readiness {#pod-readiness-gate}
+### Pod readiness {#pod-readiness-gate}
 
 {{< feature-state for_k8s_version="v1.14" state="stable" >}}
 
 Your application can inject extra feedback or signals into PodStatus:
-_Pod readiness_. To use this, set `readinessGates` in the PodSpec to specify
-a list of additional conditions that the kubelet evaluates for Pod readiness.
+_Pod readiness_. To use this, set `readinessGates` in the Pod's `spec` to
+specify a list of additional conditions that the kubelet evaluates for Pod readiness.
 
 Readiness gates are determined by the current state of `status.condition`
-fields for the Pod. If Kubernetes cannot find such a
-condition in the `status.conditions` field of a Pod, the status of the condition
+fields for the Pod. If Kubernetes cannot find such a condition in the
+`status.conditions` field of a Pod, the status of the condition
 is defaulted to "`False`".
 
 Here is an example:
@@ -258,152 +220,228 @@ For a Pod that uses custom conditions, that Pod is evaluated to be ready **only*
 when both the following statements apply:
 
 * All containers in the Pod are ready.
-* All conditions specified in `ReadinessGates` are `True`.
+* All conditions specified in `readinessGates` are `True`.
 
 When a Pod's containers are Ready but at least one custom condition is missing or
-`False`, the kubelet sets the Pod's condition to `ContainersReady`.
+`False`, the kubelet sets the Pod's [condition](#pod-condition) to `ContainersReady`.
 
-## Restart policy
+## Container probes
 
-A PodSpec has a `restartPolicy` field with possible values Always, OnFailure,
-and Never. The default value is Always.
-`restartPolicy` applies to all Containers in the Pod. `restartPolicy` only
-refers to restarts of the Containers by the kubelet on the same node. Exited
-Containers that are restarted by the kubelet are restarted with an exponential
-back-off delay (10s, 20s, 40s ...) capped at five minutes, and is reset after ten
-minutes of successful execution. As discussed in the
-[Pods document](/docs/user-guide/pods/#durability-of-pods-or-lack-thereof),
-once bound to a node, a Pod will never be rebound to another node.
+A [Probe](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#probe-v1-core) is a diagnostic
+performed periodically by the
+[kubelet](/docs/reference/command-line-tools-reference/kubelet/)
+on a Container. To perform a diagnostic,
+the kubelet calls a
+[Handler](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#handler-v1-core) implemented by
+the container. There are three types of handlers:
 
+* [ExecAction](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#execaction-v1-core):
+  Executes a specified command inside the container. The diagnostic
+  is considered successful if the command exits with a status code of 0.
 
-## Pod lifetime
+* [TCPSocketAction](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#tcpsocketaction-v1-core):
+  Performs a TCP check against the Pod's IP address on
+  a specified port. The diagnostic is considered successful if the port is open.
 
-In general, Pods remain until a human or
-{{< glossary_tooltip term_id="controller" text="controller" >}} process
-explicitly removes them.
-The control plane cleans up terminated Pods (with a phase of `Succeeded` or
-`Failed`), when the number of Pods exceeds the configured threshold
-(determined by `terminated-pod-gc-threshold` in the kube-controller-manager).
-This avoids a resource leak as Pods are created and terminated over time.
+* [HTTPGetAction](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#httpgetaction-v1-core):
+  Performs an HTTP `GET` request against the Pod's IP
+  address on a specified port and path. The diagnostic is considered successful
+  if the response has a status code greater than or equal to 200 and less than 400.
 
-There are different kinds of resources for creating Pods:
+Each probe has one of three results:
 
-- Use a {{< glossary_tooltip term_id="deployment" >}},
-  {{< glossary_tooltip term_id="replica-set" >}} or {{< glossary_tooltip term_id="statefulset" >}}
-  for Pods that are not expected to terminate, for example, web servers.
+* `Success`: The container passed the diagnostic.
+* `Failure`: The container failed the diagnostic.
+* `Unknown`: The diagnostic failed, so no action should be taken.
 
-- Use a {{< glossary_tooltip term_id="job" >}}
-  for Pods that are expected to terminate once their work is complete;
-  for example, batch computations. Jobs are appropriate only for Pods with
-  `restartPolicy` equal to OnFailure or Never.
+The kubelet can optionally perform and react to three kinds of probes on running
+containers:
 
-- Use a {{< glossary_tooltip term_id="daemonset" >}}
-  for Pods that need to run one per eligible node.
+* `livenessProbe`: Indicates whether the container is running. If
+   the liveness probe fails, the kubelet kills the container, and the container
+   is subjected to its [restart policy](#restart-policy). If a Container does not
+   provide a liveness probe, the default state is `Success`.
 
-All workload resources contain a PodSpec. It is recommended to create the
-appropriate workload resource and let the resource's controller create Pods
-for you, rather than directly create Pods yourself.
+* `readinessProbe`: Indicates whether the container is ready to respond to requests.
+   If the readiness probe fails, the endpoints controller removes the Pod's IP
+   address from the endpoints of all Services that match the Pod. The default
+   state of readiness before the initial delay is `Failure`. If a Container does
+   not provide a readiness probe, the default state is `Success`.
 
-If a node dies or is disconnected from the rest of the cluster, Kubernetes
-applies a policy for setting the `phase` of all Pods on the lost node to Failed.
+* `startupProbe`: Indicates whether the application within the container is started.
+   All other probes are disabled if a startup probe is provided, until it succeeds.
+   If the startup probe fails, the kubelet kills the container, and the container
+   is subjected to its [restart policy](#restart-policy). If a Container does not
+   provide a startup probe, the default state is `Success`.
+
+For more information about how to set up a liveness, readiness, or startup probe,
+see [Configure Liveness, Readiness and Startup Probes](/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/).
 
-## Examples
+### When should you use a liveness probe?
 
-### Advanced liveness probe example
+{{< feature-state for_k8s_version="v1.0" state="stable" >}}
 
-Liveness probes are executed by the kubelet, so all requests are made in the
-kubelet network namespace.
+If the process in your container is able to crash on its own whenever it
+encounters an issue or becomes unhealthy, you do not necessarily need a liveness
+probe; the kubelet will automatically perform the correct action in accordance
+with the Pod's `restartPolicy`.
 
-```yaml
-apiVersion: v1
-kind: Pod
-metadata:
-  labels:
-    test: liveness
-  name: liveness-http
-spec:
-  containers:
-  - args:
-    - /server
-    image: k8s.gcr.io/liveness
-    livenessProbe:
-      httpGet:
-        # when "host" is not defined, "PodIP" will be used
-        # host: my-host
-        # when "scheme" is not defined, "HTTP" scheme will be used. Only "HTTP" and "HTTPS" are allowed
-        # scheme: HTTPS
-        path: /healthz
-        port: 8080
-        httpHeaders:
-        - name: X-Custom-Header
-          value: Awesome
-      initialDelaySeconds: 15
-      timeoutSeconds: 1
-    name: liveness
-```
+If you'd like your container to be killed and restarted if a probe fails, then
+specify a liveness probe, and specify a `restartPolicy` of Always or OnFailure.
+
+### When should you use a readiness probe?
+
+{{< feature-state for_k8s_version="v1.0" state="stable" >}}
+
+If you'd like to start sending traffic to a Pod only when a probe succeeds,
+specify a readiness probe. In this case, the readiness probe might be the same
+as the liveness probe, but the existence of the readiness probe in the spec means
+that the Pod will start without receiving any traffic and only start receiving
+traffic after the probe starts succeeding.
+If your container needs to work on loading large data, configuration files, or
+migrations during startup, specify a readiness probe.
 
-### Example states
-
-   * Pod is running and has one Container. Container exits with success.
-     * Log completion event.
-     * If `restartPolicy` is:
-       * Always: Restart Container; Pod `phase` stays Running.
-       * OnFailure: Pod `phase` becomes Succeeded.
-       * Never: Pod `phase` becomes Succeeded.
-
-   * Pod is running and has one Container. Container exits with failure.
-     * Log failure event.
-     * If `restartPolicy` is:
-       * Always: Restart Container; Pod `phase` stays Running.
-       * OnFailure: Restart Container; Pod `phase` stays Running.
-       * Never: Pod `phase` becomes Failed.
-
-   * Pod is running and has two Containers. Container 1 exits with failure.
-     * Log failure event.
-     * If `restartPolicy` is:
-       * Always: Restart Container; Pod `phase` stays Running.
-       * OnFailure: Restart Container; Pod `phase` stays Running.
-       * Never: Do not restart Container; Pod `phase` stays Running.
-     * If Container 1 is not running, and Container 2 exits:
-       * Log failure event.
-       * If `restartPolicy` is:
-         * Always: Restart Container; Pod `phase` stays Running.
-         * OnFailure: Restart Container; Pod `phase` stays Running.
-         * Never: Pod `phase` becomes Failed.
-
-   * Pod is running and has one Container. Container runs out of memory.
-     * Container terminates in failure.
-     * Log OOM event.
-     * If `restartPolicy` is:
-       * Always: Restart Container; Pod `phase` stays Running.
-       * OnFailure: Restart Container; Pod `phase` stays Running.
-       * Never: Log failure event; Pod `phase` becomes Failed.
-
-   * Pod is running, and a disk dies.
-     * Kill all Containers.
-     * Log appropriate event.
-     * Pod `phase` becomes Failed.
-     * If running under a controller, Pod is recreated elsewhere.
-
-   * Pod is running, and its node is segmented out.
-     * Node controller waits for timeout.
-     * Node controller sets Pod `phase` to Failed.
-     * If running under a controller, Pod is recreated elsewhere.
+If you want your container to be able to take itself down for maintenance, you
+can specify a readiness probe that checks an endpoint specific to readiness that
+is different from the liveness probe.
 
+{{< note >}}
+If you just want to be able to drain requests when the Pod is deleted, you do not
+necessarily need a readiness probe; on deletion, the Pod automatically puts itself
+into an unready state regardless of whether the readiness probe exists.
+The Pod remains in the unready state while it waits for the containers in the Pod
+to stop.
+{{< /note >}}
 
+### When should you use a startup probe?
 
+{{< feature-state for_k8s_version="v1.18" state="beta" >}}
+
+Startup probes are useful for Pods that have containers that take a long time to
+come into service. Rather than set a long liveness interval, you can configure
+a separate configuration for probing the container as it starts up, allowing
+a time longer than the liveness interval would allow.
+
+If your container usually starts in more than
+`initialDelaySeconds + failureThreshold × periodSeconds`, you should specify a
+startup probe that checks the same endpoint as the liveness probe. The default for
+`periodSeconds` is 30s. You should then set its `failureThreshold` high enough to
+allow the container to start, without changing the default values of the liveness
+probe. This helps to protect against deadlocks.
+
+## Termination of Pods {#pod-termination}
+
+Because Pods represent processes running on nodes in the cluster, it is important to
+allow those processes to gracefully terminate when they are no longer needed (rather
+than being abruptly stopped with a `KILL` signal and having no chance to clean up).
+
+The design aim is for you to be able to request deletion and know when processes
+terminate, but also be able to ensure that deletes eventually complete.
+When you request deletion of a Pod, the cluster records and tracks the intended grace period
+before the Pod is allowed to be forcefully killed. With that forceful shutdown tracking in
+place, the {{< glossary_tooltip text="kubelet" term_id="kubelet" >}} attempts graceful
+shutdown.
+
+Typically, the container runtime sends a TERM signal to the main process in each
+container. Many container runtimes respect the `STOPSIGNAL` value defined in the container
+image and send this instead of TERM.
+Once the grace period has expired, the KILL signal is sent to any remaining
+processes, and the Pod is then deleted from the
+{{< glossary_tooltip text="API Server" term_id="kube-apiserver" >}}. If the kubelet or the
+container runtime's management service is restarted while waiting for processes to terminate, the
+cluster retries from the start including the full original grace period.
+
+An example flow:
+
+1. You use the `kubectl` tool to manually delete a specific Pod, with the default grace period
+   (30 seconds).
+1. The Pod in the API server is updated with the time beyond which the Pod is considered "dead"
+   along with the grace period.
+   If you use `kubectl describe` to check on the Pod you're deleting, that Pod shows up as
+   "Terminating".
+   On the node where the Pod is running: as soon as the kubelet sees that a Pod has been marked
+   as terminating (a graceful shutdown duration has been set), the kubelet begins the local Pod
+   shutdown process.
+   1. If one of the Pod's containers has defined a `preStop`
+      [hook](/docs/concepts/containers/container-lifecycle-hooks/#hook-details), the kubelet
+      runs that hook inside of the container. If the `preStop` hook is still running after the
+      grace period expires, the kubelet requests a small, one-off grace period extension of 2
+      seconds.
+      {{< note >}}
+      If the `preStop` hook needs longer to complete than the default grace period allows,
+      you must modify `terminationGracePeriodSeconds` to suit this.
+      {{< /note >}}
+   1. The kubelet triggers the container runtime to send a TERM signal to process 1 inside each
+      container.
+      {{< note >}}
+      The containers in the Pod receive the TERM signal at different times and in an arbitrary
+      order. If the order of shutdowns matters, consider using a `preStop` hook to synchronize.
+      {{< /note >}}
+1. At the same time as the kubelet is starting graceful shutdown, the control plane removes that
+   shutting-down Pod from Endpoints (and, if enabled, EndpointSlice) objects where these represent
+   a {{< glossary_tooltip term_id="service" text="Service" >}} with a configured
+   {{< glossary_tooltip text="selector" term_id="selector" >}}.
+   {{< glossary_tooltip text="ReplicaSets" term_id="replica-set" >}} and other workload resources
+   no longer treat the shutting-down Pod as a valid, in-service replica. Pods that shut down slowly
+   cannot continue to serve traffic as load balancers (like the service proxy) remove the Pod from
+   the list of endpoints as soon as the termination grace period _begins_.
+1. When the grace period expires, the kubelet triggers forcible shutdown. The container runtime sends
+   `SIGKILL` to any processes still running in any container in the Pod.
+   The kubelet also cleans up a hidden `pause` container if that container runtime uses one.
+1. The kubelet triggers forcible removal of Pod object from the API server, by setting grace period
+   to 0 (immediate deletion).
+1. The API server deletes the Pod's API object, which is then no longer visible from any client.
+
+### Forced Pod termination {#pod-termination-forced}
+
+{{< caution >}}
+Forced deletions can be potentially disruptive for some workloads and their Pods.
+{{< /caution >}}
+
+By default, all deletes are graceful within 30 seconds. The `kubectl delete` command supports
+the `--grace-period=<seconds>` option which allows you to override the default and specify your
+own value.
+
+Setting the grace period to `0` forcibly and immediately deletes the Pod from the API
+server. If the pod was still running on a node, that forcible deletion triggers the kubelet to
+begin immediate cleanup.
+
+{{< note >}}
+You must specify an additional flag `--force` along with `--grace-period=0` in order to perform force deletions.
+{{< /note >}}
+
+When a force deletion is performed, the API server does not wait for confirmation
+from the kubelet that the Pod has been terminated on the node it was running on. It
+removes the Pod in the API immediately so a new Pod can be created with the same
+name. On the node, Pods that are set to terminate immediately will still be given
+a small grace period before being force killed.
+
+If you need to force-delete Pods that are part of a StatefulSet, refer to the task
+documentation for
+[deleting Pods from a StatefulSet](/docs/tasks/run-application/force-delete-stateful-set-pod/).
+
+### Garbage collection of failed Pods {#pod-garbage-collection}
+
+For failed Pods, the API objects remain in the cluster's API until a human or
+{{< glossary_tooltip term_id="controller" text="controller" >}} process
+explicitly removes them.
 
-## {{% heading "whatsnext" %}}
+The control plane cleans up terminated Pods (with a phase of `Succeeded` or
+`Failed`), when the number of Pods exceeds the configured threshold
+(determined by `terminated-pod-gc-threshold` in the kube-controller-manager).
+This avoids a resource leak as Pods are created and terminated over time.
 
 
+## {{% heading "whatsnext" %}}
+
 * Get hands-on experience
   [attaching handlers to Container lifecycle events](/docs/tasks/configure-pod-container/attach-handler-lifecycle-event/).
 
 * Get hands-on experience
-  [Configure Liveness, Readiness and Startup Probes](/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/).
-
-* Learn more about [Container lifecycle hooks](/docs/concepts/containers/container-lifecycle-hooks/).
-
-
+  [configuring Liveness, Readiness and Startup Probes](/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/).
 
+* Learn more about [container lifecycle hooks](/docs/concepts/containers/container-lifecycle-hooks/).
 
+* For detailed information about Pod / Container status in the API, see [PodStatus](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#podstatus-v1-core)
+and
+[ContainerStatus](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#containerstatus-v1-core).

