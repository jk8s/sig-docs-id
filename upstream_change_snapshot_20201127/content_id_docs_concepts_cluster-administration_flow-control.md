diff --git a/content/en/docs/concepts/cluster-administration/flow-control.md b/content/en/docs/concepts/cluster-administration/flow-control.md
index 26fc1194d..f40a86bab 100644
--- a/content/en/docs/concepts/cluster-administration/flow-control.md
+++ b/content/en/docs/concepts/cluster-administration/flow-control.md
@@ -162,6 +162,31 @@ are built in and may not be overwritten:
   that only matches the `catch-all` FlowSchema will be rejected with an HTTP 429
   error.
 
+## Health check concurrency exemption
+
+The suggested configuration gives no special treatment to the health
+check requests on kube-apiservers from their local kubelets --- which
+tend to use the secured port but supply no credentials.  With the
+suggested config, these requests get assigned to the `global-default`
+FlowSchema and the corresponding `global-default` priority level,
+where other traffic can crowd them out.
+
+If you add the following additional FlowSchema, this exempts those
+requests from rate limiting.
+
+{{< caution >}}
+
+Making this change also allows any hostile party to then send
+health-check requests that match this FlowSchema, at any volume they
+like.  If you have a web traffic filter or similar external security
+mechanism to protect your cluster's API server from general internet
+traffic, you can configure rules to block any health check requests
+that originate from outside your cluster.
+
+{{< /caution >}}
+
+{{< codenew file="priority-and-fairness/health-for-strangers.yaml" >}}
+
 ## Resources
 The flow control API involves two kinds of resources.
 [PriorityLevelConfigurations](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#prioritylevelconfiguration-v1alpha1-flowcontrol-apiserver-k8s-io)
@@ -303,15 +328,20 @@ to get a mapping of UIDs to names for both FlowSchemas and
 PriorityLevelConfigurations.
 
 ## Observability
+
+### Metrics
+
 When you enable the API Priority and Fairness feature, the kube-apiserver
 exports additional metrics. Monitoring these can help you determine whether your
 configuration is inappropriately throttling important traffic, or find
 poorly-behaved workloads that may be harming system health.
 
-* `apiserver_flowcontrol_rejected_requests_total` counts requests that
-  were rejected, grouped by the name of the assigned priority level,
-  the name of the assigned FlowSchema, and the reason for rejection.
-  The reason will be one of the following:
+* `apiserver_flowcontrol_rejected_requests_total` is a counter vector
+  (cumulative since server start) of requests that were rejected,
+  broken down by the labels `flowSchema` (indicating the one that
+  matched the request), `priorityLevel` (indicating the one to which
+  the request was assigned), and `reason`.  The `reason` label will be
+  have one of the following values:
     * `queue-full`, indicating that too many requests were already
       queued,
     * `concurrency-limit`, indicating that the
@@ -320,23 +350,72 @@ poorly-behaved workloads that may be harming system health.
     * `time-out`, indicating that the request was still in the queue
       when its queuing time limit expired.
 
-* `apiserver_flowcontrol_dispatched_requests_total` counts requests
-  that began executing, grouped by the name of the assigned priority
-  level and the name of the assigned FlowSchema.
-
-* `apiserver_flowcontrol_current_inqueue_requests` gives the
-  instantaneous total number of queued (not executing) requests,
-  grouped by priority level and FlowSchema.
-
-* `apiserver_flowcontrol_current_executing_requests` gives the instantaneous
-  total number of executing requests, grouped by priority level and FlowSchema.
-
-* `apiserver_flowcontrol_request_queue_length_after_enqueue` gives a
-  histogram of queue lengths for the queues, grouped by priority level
-  and FlowSchema, as sampled by the enqueued requests.  Each request
-  that gets queued contributes one sample to its histogram, reporting
-  the length of the queue just after the request was added.  Note that
-  this produces different statistics than an unbiased survey would.
+* `apiserver_flowcontrol_dispatched_requests_total` is a counter
+  vector (cumulative since server start) of requests that began
+  executing, broken down by the labels `flowSchema` (indicating the
+  one that matched the request) and `priorityLevel` (indicating the
+  one to which the request was assigned).
+
+* `apiserver_current_inqueue_requests` is a gauge vector of recent
+  high water marks of the number of queued requests, grouped by a
+  label named `request_kind` whose value is `mutating` or `readOnly`.
+  These high water marks describe the largest number seen in the one
+  second window most recently completed.  These complement the older
+  `apiserver_current_inflight_requests` gauge vector that holds the
+  last window's high water mark of number of requests actively being
+  served.
+
+* `apiserver_flowcontrol_read_vs_write_request_count_samples` is a
+  histogram vector of observations of the then-current number of
+  requests, broken down by the labels `phase` (which takes on the
+  values `waiting` and `executing`) and `request_kind` (which takes on
+  the values `mutating` and `readOnly`).  The observations are made
+  periodically at a high rate.
+
+* `apiserver_flowcontrol_read_vs_write_request_count_watermarks` is a
+  histogram vector of high or low water marks of the number of
+  requests broken down by the labels `phase` (which takes on the
+  values `waiting` and `executing`) and `request_kind` (which takes on
+  the values `mutating` and `readOnly`); the label `mark` takes on
+  values `high` and `low`.  The water marks are accumulated over
+  windows bounded by the times when an observation was added to
+  `apiserver_flowcontrol_read_vs_write_request_count_samples`.  These
+  water marks show the range of values that occurred between samples.
+
+* `apiserver_flowcontrol_current_inqueue_requests` is a gauge vector
+  holding the instantaneous number of queued (not executing) requests,
+  broken down by the labels `priorityLevel` and `flowSchema`.
+
+* `apiserver_flowcontrol_current_executing_requests` is a gauge vector
+  holding the instantaneous number of executing (not waiting in a
+  queue) requests, broken down by the labels `priorityLevel` and
+  `flowSchema`.
+
+* `apiserver_flowcontrol_priority_level_request_count_samples` is a
+  histogram vector of observations of the then-current number of
+  requests broken down by the labels `phase` (which takes on the
+  values `waiting` and `executing`) and `priorityLevel`.  Each
+  histogram gets observations taken periodically, up through the last
+  activity of the relevant sort.  The observations are made at a high
+  rate.
+
+* `apiserver_flowcontrol_priority_level_request_count_watermarks` is a
+  histogram vector of high or low water marks of the number of
+  requests broken down by the labels `phase` (which takes on the
+  values `waiting` and `executing`) and `priorityLevel`; the label
+  `mark` takes on values `high` and `low`.  The water marks are
+  accumulated over windows bounded by the times when an observation
+  was added to
+  `apiserver_flowcontrol_priority_level_request_count_samples`.  These
+  water marks show the range of values that occurred between samples.
+
+* `apiserver_flowcontrol_request_queue_length_after_enqueue` is a
+  histogram vector of queue lengths for the queues, broken down by
+  the labels `priorityLevel` and `flowSchema`, as sampled by the
+  enqueued requests.  Each request that gets queued contributes one
+  sample to its histogram, reporting the length of the queue just
+  after the request was added.  Note that this produces different
+  statistics than an unbiased survey would.
     {{< note >}}
     An outlier value in a histogram here means it is likely that a single flow
     (i.e., requests by one user or for one namespace, depending on
@@ -346,14 +425,17 @@ poorly-behaved workloads that may be harming system health.
     to increase that PriorityLevelConfiguration's concurrency shares.
     {{< /note >}}
 
-* `apiserver_flowcontrol_request_concurrency_limit` gives the computed
-  concurrency limit (based on the API server's total concurrency limit and PriorityLevelConfigurations'
-  concurrency shares) for each PriorityLevelConfiguration.
-
-* `apiserver_flowcontrol_request_wait_duration_seconds` gives a histogram of how
-  long requests spent queued, grouped by the FlowSchema that matched the
-  request, the PriorityLevel to which it was assigned, and whether or not the
-  request successfully executed.
+* `apiserver_flowcontrol_request_concurrency_limit` is a gauge vector
+  holding the computed concurrency limit (based on the API server's
+  total concurrency limit and PriorityLevelConfigurations' concurrency
+  shares), broken down by the label `priorityLevel`.
+
+* `apiserver_flowcontrol_request_wait_duration_seconds` is a histogram
+  vector of how long requests spent queued, broken down by the labels
+  `flowSchema` (indicating which one matched the request),
+  `priorityLevel` (indicating the one to which the request was
+  assigned), and `execute` (indicating whether the request started
+  executing).
     {{< note >}}
     Since each FlowSchema always assigns requests to a single
     PriorityLevelConfiguration, you can add the histograms for all the
@@ -361,13 +443,71 @@ poorly-behaved workloads that may be harming system health.
     requests assigned to that priority level.
     {{< /note >}}
 
-* `apiserver_flowcontrol_request_execution_seconds` gives a histogram of how
-  long requests took to actually execute, grouped by the FlowSchema that matched the
-  request and the PriorityLevel to which it was assigned.
-
-
-
-
+* `apiserver_flowcontrol_request_execution_seconds` is a histogram
+  vector of how long requests took to actually execute, broken down by
+  the labels `flowSchema` (indicating which one matched the request)
+  and `priorityLevel` (indicating the one to which the request was
+  assigned).
+
+### Debug endpoints
+
+When you enable the API Priority and Fairness feature, the kube-apiserver serves the following additional paths at its HTTP[S] ports.
+
+- `/debug/api_priority_and_fairness/dump_priority_levels` - a listing of all the priority levels and the current state of each.  You can fetch like this:
+  ```shell
+  kubectl get --raw /debug/api_priority_and_fairness/dump_priority_levels
+  ```
+  The output is similar to this:
+  ```
+  PriorityLevelName, ActiveQueues, IsIdle, IsQuiescing, WaitingRequests, ExecutingRequests,
+  workload-low,      0,            true,   false,       0,               0,
+  global-default,    0,            true,   false,       0,               0,
+  exempt,            <none>,       <none>, <none>,      <none>,          <none>,
+  catch-all,         0,            true,   false,       0,               0,
+  system,            0,            true,   false,       0,               0,
+  leader-election,   0,            true,   false,       0,               0,
+  workload-high,     0,            true,   false,       0,               0,
+  ```
+
+- `/debug/api_priority_and_fairness/dump_queues` - a listing of all the queues and their current state.  You can fetch like this:
+  ```shell
+  kubectl get --raw /debug/api_priority_and_fairness/dump_queues
+  ```
+  The output is similar to this:
+  ```
+  PriorityLevelName, Index,  PendingRequests, ExecutingRequests, VirtualStart,
+  workload-high,     0,      0,               0,                 0.0000,
+  workload-high,     1,      0,               0,                 0.0000,
+  workload-high,     2,      0,               0,                 0.0000,
+  ...
+  leader-election,   14,     0,               0,                 0.0000,
+  leader-election,   15,     0,               0,                 0.0000,
+  ```
+
+- `/debug/api_priority_and_fairness/dump_requests` - a listing of all the requests that are currently waiting in a queue.  You can fetch like this:
+  ```shell
+  kubectl get --raw /debug/api_priority_and_fairness/dump_requests
+  ```
+  The output is similar to this:
+  ```
+  PriorityLevelName, FlowSchemaName, QueueIndex, RequestIndexInQueue, FlowDistingsher,       ArriveTime,
+  exempt,            <none>,         <none>,     <none>,              <none>,                <none>,
+  system,            system-nodes,   12,         0,                   system:node:127.0.0.1, 2020-07-23T15:26:57.179170694Z,
+  ```
+  
+  In addition to the queued requests, the output includes one phantom line for each priority level that is exempt from limitation.
+
+  You can get a more detailed listing with a command like this:
+  ```shell
+  kubectl get --raw '/debug/api_priority_and_fairness/dump_requests?includeRequestDetails=1'
+  ```
+  The output is similar to this:
+  ```
+  PriorityLevelName, FlowSchemaName, QueueIndex, RequestIndexInQueue, FlowDistingsher,       ArriveTime,                     UserName,              Verb,   APIPath,                                                     Namespace, Name,   APIVersion, Resource, SubResource,
+  system,            system-nodes,   12,         0,                   system:node:127.0.0.1, 2020-07-23T15:31:03.583823404Z, system:node:127.0.0.1, create, /api/v1/namespaces/scaletest/configmaps,
+  system,            system-nodes,   12,         1,                   system:node:127.0.0.1, 2020-07-23T15:31:03.594555947Z, system:node:127.0.0.1, create, /api/v1/namespaces/scaletest/configmaps,
+  ```
+  
 ## {{% heading "whatsnext" %}}
 
 

