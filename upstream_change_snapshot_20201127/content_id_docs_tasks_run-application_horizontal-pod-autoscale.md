diff --git a/content/en/docs/tasks/run-application/horizontal-pod-autoscale.md b/content/en/docs/tasks/run-application/horizontal-pod-autoscale.md
index f84744cdd..ff16a13e7 100644
--- a/content/en/docs/tasks/run-application/horizontal-pod-autoscale.md
+++ b/content/en/docs/tasks/run-application/horizontal-pod-autoscale.md
@@ -15,7 +15,7 @@ weight: 90
 
 <!-- overview -->
 
-The Horizontal Pod Autoscaler automatically scales the number of pods
+The Horizontal Pod Autoscaler automatically scales the number of Pods
 in a replication controller, deployment, replica set or stateful set based on observed CPU utilization (or, with
 [custom metrics](https://git.k8s.io/community/contributors/design-proposals/instrumentation/custom-metrics-api.md)
 support, on some other application-provided metrics). Note that Horizontal
@@ -45,16 +45,16 @@ obtains the metrics from either the resource metrics API (for per-pod resource m
 or the custom metrics API (for all other metrics).
 
 * For per-pod resource metrics (like CPU), the controller fetches the metrics
-  from the resource metrics API for each pod targeted by the HorizontalPodAutoscaler.
+  from the resource metrics API for each Pod targeted by the HorizontalPodAutoscaler.
   Then, if a target utilization value is set, the controller calculates the utilization
   value as a percentage of the equivalent resource request on the containers in
-  each pod.  If a target raw value is set, the raw metric values are used directly.
+  each Pod.  If a target raw value is set, the raw metric values are used directly.
   The controller then takes the mean of the utilization or the raw value (depending on the type
-  of target specified) across all targeted pods, and produces a ratio used to scale
+  of target specified) across all targeted Pods, and produces a ratio used to scale
   the number of desired replicas.
 
-  Please note that if some of the pod's containers do not have the relevant resource request set,
-  CPU utilization for the pod will not be defined and the autoscaler will
+  Please note that if some of the Pod's containers do not have the relevant resource request set,
+  CPU utilization for the Pod will not be defined and the autoscaler will
   not take any action for that metric. See the [algorithm
   details](#algorithm-details) section below for more information about
   how the autoscaling algorithm works.
@@ -65,7 +65,7 @@ or the custom metrics API (for all other metrics).
 * For object metrics and external metrics, a single metric is fetched, which describes
   the object in question. This metric is compared to the target
   value, to produce a ratio as above. In the `autoscaling/v2beta2` API
-  version, this value can optionally be divided by the number of pods before the
+  version, this value can optionally be divided by the number of Pods before the
   comparison is made.
 
 The HorizontalPodAutoscaler normally fetches metrics from a series of aggregated APIs (`metrics.k8s.io`,
@@ -265,12 +265,12 @@ APIs, cluster administrators must ensure that:
 
 * The corresponding APIs are registered:
 
-   * For resource metrics, this is the `metrics.k8s.io` API, generally provided by [metrics-server](https://github.com/kubernetes-incubator/metrics-server).
+   * For resource metrics, this is the `metrics.k8s.io` API, generally provided by [metrics-server](https://github.com/kubernetes-sigs/metrics-server).
      It can be launched as a cluster addon.
 
    * For custom metrics, this is the `custom.metrics.k8s.io` API.  It's provided by "adapter" API servers provided by metrics solution vendors.
      Check with your metrics pipeline, or the [list of known solutions](https://github.com/kubernetes/metrics/blob/master/IMPLEMENTATIONS.md#custom-metrics-api).
-     If you would like to write your own, check out the [boilerplate](https://github.com/kubernetes-incubator/custom-metrics-apiserver) to get started.
+     If you would like to write your own, check out the [boilerplate](https://github.com/kubernetes-sigs/custom-metrics-apiserver) to get started.
 
    * For external metrics, this is the `external.metrics.k8s.io` API.  It may be provided by the custom metrics adapters provided above.
 
@@ -319,7 +319,7 @@ For instance if there are 80 replicas and the target has to be scaled down to 10
 then during the first step 8 replicas will be reduced. In the next iteration when the number
 of replicas is 72, 10% of the pods is 7.2 but the number is rounded up to 8. On each loop of
 the autoscaler controller the number of pods to be change is re-calculated based on the number
-of current replicas. When the number of replicas falls below 40 the first policy_(Pods)_ is applied
+of current replicas. When the number of replicas falls below 40 the first policy _(Pods)_ is applied
 and 4 replicas will be reduced at a time.
 
 `periodSeconds` indicates the length of time in the past for which the policy must hold true.
@@ -328,7 +328,7 @@ allows at most 10% of the current replicas to be scaled down in one minute.
 
 The policy selection can be changed by specifying the `selectPolicy` field for a scaling
 direction. By setting the value to `Min` which would select the policy which allows the
-smallest change in the replica count. Setting the value to `Disabled` completely disabled
+smallest change in the replica count. Setting the value to `Disabled` completely disables
 scaling in that direction.
 
 ### Stabilization Window
@@ -405,8 +405,9 @@ behavior:
       periodSeconds: 60
 ```
 
-To allow a final drop of 5 pods, another policy can be added and a selection
-strategy of minimum:
+To ensure that no more than 5 Pods are removed per minute, you can add a second scale-down
+policy with a fixed size of 5, and set `selectPolicy` to minimum. Setting `selectPolicy` to `Min` means
+that the autoscaler chooses the policy that affects the smallest number of Pods:
 
 ```yaml
 behavior:
@@ -418,7 +419,7 @@ behavior:
     - type: Pods
       value: 5
       periodSeconds: 60
-    selectPolicy: Max
+    selectPolicy: Min
 ```
 
 ### Example: disable scale down
@@ -432,7 +433,14 @@ behavior:
     selectPolicy: Disabled
 ```
 
+## Implicit maintenance-mode deactivation
 
+You can implicitly deactivate the HPA for a target without the
+need to change the HPA configuration itself. If the target's desired replica count
+is set to 0, and the HPA's minimum replica count is greater than 0, the HPA 
+stops adjusting the target (and sets the `ScalingActive` Condition on itself
+to `false`) until you reactivate it by manually adjusting the target's desired
+replica count or HPA's minimum replica count.
 
 ## {{% heading "whatsnext" %}}
 
@@ -440,5 +448,3 @@ behavior:
 * Design documentation: [Horizontal Pod Autoscaling](https://git.k8s.io/community/contributors/design-proposals/autoscaling/horizontal-pod-autoscaler.md).
 * kubectl autoscale command: [kubectl autoscale](/docs/reference/generated/kubectl/kubectl-commands/#autoscale).
 * Usage example of [Horizontal Pod Autoscaler](/docs/tasks/run-application/horizontal-pod-autoscale-walkthrough/).
-
-

