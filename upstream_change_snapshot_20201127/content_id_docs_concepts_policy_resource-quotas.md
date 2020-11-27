diff --git a/content/en/docs/concepts/policy/resource-quotas.md b/content/en/docs/concepts/policy/resource-quotas.md
index 4fb3f17a3..8758603fe 100644
--- a/content/en/docs/concepts/policy/resource-quotas.md
+++ b/content/en/docs/concepts/policy/resource-quotas.md
@@ -13,31 +13,34 @@ there is a concern that one team could use more than its fair share of resources
 
 Resource quotas are a tool for administrators to address this concern.
 
-
-
-
 <!-- body -->
 
 A resource quota, defined by a `ResourceQuota` object, provides constraints that limit
 aggregate resource consumption per namespace.  It can limit the quantity of objects that can
 be created in a namespace by type, as well as the total amount of compute resources that may
-be consumed by resources in that project.
+be consumed by resources in that namespace.
 
 Resource quotas work like this:
 
 - Different teams work in different namespaces.  Currently this is voluntary, but
   support for making this mandatory via ACLs is planned.
-- The administrator creates one `ResourceQuota` for each namespace.
+
+- The administrator creates one ResourceQuota for each namespace.
+
 - Users create resources (pods, services, etc.) in the namespace, and the quota system
-  tracks usage to ensure it does not exceed hard resource limits defined in a `ResourceQuota`.
+  tracks usage to ensure it does not exceed hard resource limits defined in a ResourceQuota.
+
 - If creating or updating a resource violates a quota constraint, the request will fail with HTTP
   status code `403 FORBIDDEN` with a message explaining the constraint that would have been violated.
+
 - If quota is enabled in a namespace for compute resources like `cpu` and `memory`, users must specify
   requests or limits for those values; otherwise, the quota system may reject pod creation.  Hint: Use
   the `LimitRanger` admission controller to force defaults for pods that make no compute resource requirements.
-  See the [walkthrough](/docs/tasks/administer-cluster/quota-memory-cpu-namespace/) for an example of how to avoid this problem.
 
-The name of a `ResourceQuota` object must be a valid
+  See the [walkthrough](/docs/tasks/administer-cluster/manage-resources/quota-memory-cpu-namespace/)
+  for an example of how to avoid this problem.
+
+The name of a ResourceQuota object must be a valid
 [DNS subdomain name](/docs/concepts/overview/working-with-objects/names#dns-subdomain-names).
 
 Examples of policies that could be created using namespaces and quotas are:
@@ -55,15 +58,15 @@ Neither contention nor changes to quota will affect already created resources.
 ## Enabling Resource Quota
 
 Resource Quota support is enabled by default for many Kubernetes distributions.  It is
-enabled when the apiserver `--enable-admission-plugins=` flag has `ResourceQuota` as
+enabled when the API server `--enable-admission-plugins=` flag has `ResourceQuota` as
 one of its arguments.
 
 A resource quota is enforced in a particular namespace when there is a
-`ResourceQuota` in that namespace.
+ResourceQuota in that namespace.
 
 ## Compute Resource Quota
 
-You can limit the total sum of [compute resources](/docs/user-guide/compute-resources) that can be requested in a given namespace.
+You can limit the total sum of [compute resources](/docs/concepts/configuration/manage-resources-containers/) that can be requested in a given namespace.
 
 The following resource types are supported:
 
@@ -73,11 +76,14 @@ The following resource types are supported:
 | `limits.memory` | Across all pods in a non-terminal state, the sum of memory limits cannot exceed this value. |
 | `requests.cpu` | Across all pods in a non-terminal state, the sum of CPU requests cannot exceed this value. |
 | `requests.memory` | Across all pods in a non-terminal state, the sum of memory requests cannot exceed this value. |
+| `hugepages-<size>` | Across all pods in a non-terminal state, the number of huge page requests of the specified size cannot exceed this value. |
+| `cpu` | Same as `requests.cpu` |
+| `memory` | Same as `requests.memory` |
 
 ### Resource Quota For Extended Resources
 
 In addition to the resources mentioned above, in release 1.10, quota support for
-[extended resources](/docs/concepts/configuration/manage-compute-resources-container/#extended-resources) is added.
+[extended resources](/docs/concepts/configuration/manage-resources-containers/#extended-resources) is added.
 
 As overcommit is not allowed for extended resources, it makes no sense to specify both `requests`
 and `limits` for the same extended resource in a quota. So for extended resources, only quota items
@@ -100,8 +106,8 @@ In addition, you can limit consumption of storage resources based on associated
 | Resource Name | Description |
 | --------------------- | ----------------------------------------------------------- |
 | `requests.storage` | Across all persistent volume claims, the sum of storage requests cannot exceed this value. |
-| `persistentvolumeclaims` | The total number of [persistent volume claims](/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims) that can exist in the namespace. |
-| `<storage-class-name>.storageclass.storage.k8s.io/requests.storage` | Across all persistent volume claims associated with the storage-class-name, the sum of storage requests cannot exceed this value. |
+| `persistentvolumeclaims` | The total number of [PersistentVolumeClaims](/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims) that can exist in the namespace. |
+| `<storage-class-name>.storageclass.storage.k8s.io/requests.storage` | Across all persistent volume claims associated with the `<storage-class-name>`, the sum of storage requests cannot exceed this value. |
 | `<storage-class-name>.storageclass.storage.k8s.io/persistentvolumeclaims` | Across all persistent volume claims associated with the storage-class-name, the total number of [persistent volume claims](/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims) that can exist in the namespace. |
 
 For example, if an operator wants to quota storage with `gold` storage class separate from `bronze` storage class, the operator can
@@ -116,12 +122,15 @@ In release 1.8, quota support for local ephemeral storage is added as an alpha f
 | ------------------------------- |----------------------------------------------------------- |
 | `requests.ephemeral-storage` | Across all pods in the namespace, the sum of local ephemeral storage requests cannot exceed this value. |
 | `limits.ephemeral-storage` | Across all pods in the namespace, the sum of local ephemeral storage limits cannot exceed this value. |
+| `ephemeral-storage` | Same as `requests.ephemeral-storage`. |
 
 ## Object Count Quota
 
-The 1.9 release added support to quota all standard namespaced resource types using the following syntax:
+You can set quota for the total number of certain resources of all standard,
+namespaced resource types using the following syntax:
 
-* `count/<resource>.<group>`
+* `count/<resource>.<group>` for resources from non-core groups
+* `count/<resource>` for resources from the core group
 
 Here is an example set of resources users may want to put under object count quota:
 
@@ -135,33 +144,30 @@ Here is an example set of resources users may want to put under object count quo
 * `count/statefulsets.apps`
 * `count/jobs.batch`
 * `count/cronjobs.batch`
-* `count/deployments.extensions`
 
-The 1.15 release added support for custom resources using the same syntax.
+The same syntax can be used for custom resources.
 For example, to create a quota on a `widgets` custom resource in the `example.com` API group, use `count/widgets.example.com`.
 
 When using `count/*` resource quota, an object is charged against the quota if it exists in server storage.
 These types of quotas are useful to protect against exhaustion of storage resources.  For example, you may
-want to quota the number of secrets in a server given their large size.  Too many secrets in a cluster can
-actually prevent servers and controllers from starting!  You may choose to quota jobs to protect against
-a poorly configured cronjob creating too many jobs in a namespace causing a denial of service.
-
-Prior to the 1.9 release, it was possible to do generic object count quota on a limited set of resources.
-In addition, it is possible to further constrain quota for particular resources by their type.
+want to limit the number of Secrets in a server given their large size. Too many Secrets in a cluster can
+actually prevent servers and controllers from starting. You can set a quota for Jobs to protect against
+a poorly configured CronJob. CronJobs that create too many Jobs in a namespace can lead to a denial of service.
 
+It is also possible to do generic object count quota on a limited set of resources.
 The following types are supported:
 
 | Resource Name | Description |
 | ------------------------------- | ------------------------------------------------- |
-| `configmaps` | The total number of config maps that can exist in the namespace. |
-| `persistentvolumeclaims` | The total number of [persistent volume claims](/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims) that can exist in the namespace. |
-| `pods` | The total number of pods in a non-terminal state that can exist in the namespace.  A pod is in a terminal state if `.status.phase in (Failed, Succeeded)` is true.  |
-| `replicationcontrollers` | The total number of replication controllers that can exist in the namespace. |
-| `resourcequotas` | The total number of [resource quotas](/docs/reference/access-authn-authz/admission-controllers/#resourcequota) that can exist in the namespace. |
-| `services` | The total number of services that can exist in the namespace. |
-| `services.loadbalancers` | The total number of services of type load balancer that can exist in the namespace. |
-| `services.nodeports` | The total number of services of type node port that can exist in the namespace. |
-| `secrets` | The total number of secrets that can exist in the namespace. |
+| `configmaps` | The total number of ConfigMaps that can exist in the namespace. |
+| `persistentvolumeclaims` | The total number of [PersistentVolumeClaims](/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims) that can exist in the namespace. |
+| `pods` | The total number of Pods in a non-terminal state that can exist in the namespace.  A pod is in a terminal state if `.status.phase in (Failed, Succeeded)` is true.  |
+| `replicationcontrollers` | The total number of ReplicationControllers that can exist in the namespace. |
+| `resourcequotas` | The total number of ResourceQuotas that can exist in the namespace. |
+| `services` | The total number of Services that can exist in the namespace. |
+| `services.loadbalancers` | The total number of Services of type `LoadBalancer` that can exist in the namespace. |
+| `services.nodeports` | The total number of Services of type `NodePort` that can exist in the namespace. |
+| `secrets` | The total number of Secrets that can exist in the namespace. |
 
 For example, `pods` quota counts and enforces a maximum on the number of `pods`
 created in a single namespace that are not terminal. You might want to set a `pods`
@@ -170,7 +176,7 @@ exhausts the cluster's supply of Pod IPs.
 
 ## Quota Scopes
 
-Each quota can have an associated set of scopes.  A quota will only measure usage for a resource if it matches
+Each quota can have an associated set of `scopes`. A quota will only measure usage for a resource if it matches
 the intersection of enumerated scopes.
 
 When a scope is added to the quota, it limits the number of resources it supports to those that pertain to the scope.
@@ -182,22 +188,60 @@ Resources specified on the quota outside of the allowed set results in a validat
 | `NotTerminating` | Match pods where `.spec.activeDeadlineSeconds is nil` |
 | `BestEffort` | Match pods that have best effort quality of service. |
 | `NotBestEffort` | Match pods that do not have best effort quality of service. |
+| `PriorityClass` | Match pods that references the specified [priority class](/docs/concepts/configuration/pod-priority-preemption). |
 
-The `BestEffort` scope restricts a quota to tracking the following resource: `pods`
+The `BestEffort` scope restricts a quota to tracking the following resource:
+
+* `pods`
 
-The `Terminating`, `NotTerminating`, and `NotBestEffort` scopes restrict a quota to tracking the following resources:
+The `Terminating`, `NotTerminating`, `NotBestEffort` and `PriorityClass`
+scopes restrict a quota to tracking the following resources:
 
+* `pods`
 * `cpu`
-* `limits.cpu`
-* `limits.memory`
 * `memory`
-* `pods`
 * `requests.cpu`
 * `requests.memory`
+* `limits.cpu`
+* `limits.memory`
+
+Note that you cannot specify both the `Terminating` and the `NotTerminating`
+scopes in the same quota, and you cannot specify both the `BestEffort` and
+`NotBestEffort` scopes in the same quota either.
+
+The `scopeSelector` supports the following values in the `operator` field:
+
+* `In`
+* `NotIn`
+* `Exists`
+* `DoesNotExist`
+
+When using one of the following values as the `scopeName` when defining the
+`scopeSelector`, the `operator` must be `Exists`. 
+
+* `Terminating`
+* `NotTerminating`
+* `BestEffort`
+* `NotBestEffort`
+
+If the `operator` is `In` or `NotIn`, the `values` field must have at least
+one value. For example:
+
+```yaml
+  scopeSelector:
+    matchExpressions:
+      - scopeName: PriorityClass
+        operator: In
+        values:
+          - middle
+```
+
+If the `operator` is `Exists` or `DoesNotExist`, the `values` field must *NOT* be
+specified.
 
 ### Resource Quota Per PriorityClass
 
-{{< feature-state for_k8s_version="v1.12" state="beta" >}}
+{{< feature-state for_k8s_version="v1.17" state="stable" >}}
 
 Pods can be created at a specific [priority](/docs/concepts/configuration/pod-priority-preemption/#pod-priority).
 You can control a pod's consumption of system resources based on a pod's priority, by using the `scopeSelector`
@@ -205,6 +249,19 @@ field in the quota spec.
 
 A quota is matched and consumed only if `scopeSelector` in the quota spec selects the pod.
 
+When quota is scoped for priority class using `scopeSelector` field, quota object is restricted to track only following resources:
+
+* `pods`
+* `cpu`
+* `memory`
+* `ephemeral-storage`
+* `limits.cpu`
+* `limits.memory`
+* `limits.ephemeral-storage`
+* `requests.cpu`
+* `requests.memory`
+* `requests.ephemeral-storage`
+
 This example creates a quota object and matches it with pods at specific priorities. The example
 works as follows:
 
@@ -267,7 +324,7 @@ Apply the YAML using `kubectl create`.
 kubectl create -f ./quota.yml
 ```
 
-```shell
+```
 resourcequota/pods-high created
 resourcequota/pods-medium created
 resourcequota/pods-low created
@@ -279,7 +336,7 @@ Verify that `Used` quota is `0` using `kubectl describe quota`.
 kubectl describe quota
 ```
 
-```shell
+```
 Name:       pods-high
 Namespace:  default
 Resource    Used  Hard
@@ -344,7 +401,7 @@ the other two quotas are unchanged.
 kubectl describe quota
 ```
 
-```shell
+```
 Name:       pods-high
 Namespace:  default
 Resource    Used  Hard
@@ -372,13 +429,6 @@ memory      0     20Gi
 pods        0     10
 ```
 
-`scopeSelector` supports the following values in the `operator` field:
-
-* `In`
-* `NotIn`
-* `Exist`
-* `DoesNotExist`
-
 ## Requests compared to Limits {#requests-vs-limits}
 
 When allocating compute resources, each container may specify a request and a limit value for either CPU or memory.
@@ -442,7 +492,7 @@ kubectl create -f ./object-counts.yaml --namespace=myspace
 kubectl get quota --namespace=myspace
 ```
 
-```shell
+```
 NAME                    AGE
 compute-resources       30s
 object-counts           32s
@@ -452,7 +502,7 @@ object-counts           32s
 kubectl describe quota compute-resources --namespace=myspace
 ```
 
-```shell
+```
 Name:                    compute-resources
 Namespace:               myspace
 Resource                 Used  Hard
@@ -468,7 +518,7 @@ requests.nvidia.com/gpu  0     4
 kubectl describe quota object-counts --namespace=myspace
 ```
 
-```shell
+```
 Name:                   object-counts
 Namespace:              myspace
 Resource                Used    Hard
@@ -490,41 +540,40 @@ kubectl create namespace myspace
 ```
 
 ```shell
-kubectl create quota test --hard=count/deployments.extensions=2,count/replicasets.extensions=4,count/pods=3,count/secrets=4 --namespace=myspace
+kubectl create quota test --hard=count/deployments.apps=2,count/replicasets.apps=4,count/pods=3,count/secrets=4 --namespace=myspace
 ```
 
 ```shell
-kubectl create deployment nginx --image=nginx --namespace=myspace
-kubectl scale deployment nginx --replicas=2 --namespace=myspace
+kubectl create deployment nginx --image=nginx --namespace=myspace --replicas=2
 ```
 
 ```shell
 kubectl describe quota --namespace=myspace
 ```
 
-```shell
+```
 Name:                         test
 Namespace:                    myspace
 Resource                      Used  Hard
 --------                      ----  ----
-count/deployments.extensions  1     2
+count/deployments.apps        1     2
 count/pods                    2     3
-count/replicasets.extensions  1     4
+count/replicasets.apps        1     4
 count/secrets                 1     4
 ```
 
 ## Quota and Cluster Capacity
 
-`ResourceQuotas` are independent of the cluster capacity. They are
+ResourceQuotas are independent of the cluster capacity. They are
 expressed in absolute units.  So, if you add nodes to your cluster, this does *not*
 automatically give each namespace the ability to consume more resources.
 
 Sometimes more complex policies may be desired, such as:
 
-  - Proportionally divide total cluster resources among several teams.
-  - Allow each tenant to grow resource usage as needed, but have a generous
-    limit to prevent accidental resource exhaustion.
-  - Detect demand from one namespace, add nodes, and increase quota.
+- Proportionally divide total cluster resources among several teams.
+- Allow each tenant to grow resource usage as needed, but have a generous
+  limit to prevent accidental resource exhaustion.
+- Detect demand from one namespace, add nodes, and increase quota.
 
 Such policies could be implemented using `ResourceQuotas` as building blocks, by
 writing a "controller" that watches the quota usage and adjusts the quota
@@ -535,14 +584,16 @@ restrictions around nodes: pods from several namespaces may run on the same node
 
 ## Limit Priority Class consumption by default
 
-It may be desired that pods at a particular priority, eg. "cluster-services", should be allowed in a namespace, if and only if, a matching quota object exists.
+It may be desired that pods at a particular priority, eg. "cluster-services", 
+should be allowed in a namespace, if and only if, a matching quota object exists.
 
-With this mechanism, operators will be able to restrict usage of certain high priority classes to a limited number of namespaces and not every namespace will be able to consume these priority classes by default.
+With this mechanism, operators are able to restrict usage of certain high
+priority classes to a limited number of namespaces and not every namespace
+will be able to consume these priority classes by default.
 
-To enforce this, kube-apiserver flag `--admission-control-config-file` should be used to pass path to the following configuration file:
+To enforce this, `kube-apiserver` flag `--admission-control-config-file` should be
+used to pass path to the following configuration file:
 
-{{< tabs name="example1" >}}
-{{% tab name="apiserver.config.k8s.io/v1" %}}
 ```yaml
 apiVersion: apiserver.config.k8s.io/v1
 kind: AdmissionConfiguration
@@ -554,34 +605,14 @@ plugins:
     limitedResources:
     - resource: pods
       matchScopes:
-      - scopeName: PriorityClass 
-        operator: In
-        values: ["cluster-services"]
-```
-{{% /tab %}}
-{{% tab name="apiserver.k8s.io/v1alpha1" %}}
-```yaml
-# Deprecated in v1.17 in favor of apiserver.config.k8s.io/v1
-apiVersion: apiserver.k8s.io/v1alpha1
-kind: AdmissionConfiguration
-plugins:
-- name: "ResourceQuota"
-  configuration:
-    # Deprecated in v1.17 in favor of apiserver.config.k8s.io/v1, ResourceQuotaConfiguration
-    apiVersion: resourcequota.admission.k8s.io/v1beta1
-    kind: Configuration
-    limitedResources:
-    - resource: pods
-      matchScopes:
-      - scopeName: PriorityClass 
+      - scopeName: PriorityClass
         operator: In
         values: ["cluster-services"]
 ```
-{{% /tab %}}
-{{< /tabs >}}
 
 Now, "cluster-services" pods will be allowed in only those namespaces where a quota object with a matching `scopeSelector` is present.
 For example:
+
 ```yaml
     scopeSelector:
       matchExpressions:
@@ -590,17 +621,9 @@ For example:
         values: ["cluster-services"]
 ```
 
-See [LimitedResources](https://github.com/kubernetes/kubernetes/pull/36765) and [Quota support for priority class design doc](https://github.com/kubernetes/community/blob/master/contributors/design-proposals/scheduling/pod-priority-resourcequota.md) for more information.
-
-## Example
-
-See a [detailed example for how to use resource quota](/docs/tasks/administer-cluster/quota-api-object/).
-
-
-
 ## {{% heading "whatsnext" %}}
 
-
-See [ResourceQuota design doc](https://git.k8s.io/community/contributors/design-proposals/resource-management/admission_control_resource_quota.md) for more information.
-
-
+- See [ResourceQuota design doc](https://git.k8s.io/community/contributors/design-proposals/resource-management/admission_control_resource_quota.md) for more information.
+- See a [detailed example for how to use resource quota](/docs/tasks/administer-cluster/quota-api-object/).
+- Read [Quota support for priority class design doc](https://github.com/kubernetes/community/blob/master/contributors/design-proposals/scheduling/pod-priority-resourcequota.md).
+- See [LimitedResources](https://github.com/kubernetes/kubernetes/pull/36765)

