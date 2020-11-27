diff --git a/content/en/docs/concepts/workloads/pods/podpreset.md b/content/en/docs/concepts/workloads/pods/podpreset.md
index f77e34a3f..9cbb7bdff 100644
--- a/content/en/docs/concepts/workloads/pods/podpreset.md
+++ b/content/en/docs/concepts/workloads/pods/podpreset.md
@@ -1,7 +1,7 @@
 ---
 reviewers:
 - jessfraz
-title: Pod Preset
+title: Pod Presets
 content_type: concept
 weight: 50
 ---
@@ -32,20 +32,20 @@ specific service do not need to know all the details about that service.
 
 In order to use Pod presets in your cluster you must ensure the following:
 
-1.  You have enabled the API type `settings.k8s.io/v1alpha1/podpreset`. For
-    example, this can be done by including `settings.k8s.io/v1alpha1=true` in
-    the `--runtime-config` option for the API server. In minikube add this flag
-    `--extra-config=apiserver.runtime-config=settings.k8s.io/v1alpha1=true` while
-    starting the cluster.
-1.  You have enabled the admission controller `PodPreset`. One way to doing this
-    is to include `PodPreset` in the `--enable-admission-plugins` option value specified
-    for the API server. In minikube, add this flag
-    
-    ```shell
-    --extra-config=apiserver.enable-admission-plugins=NamespaceLifecycle,LimitRanger,ServiceAccount,DefaultStorageClass,DefaultTolerationSeconds,NodeRestriction,MutatingAdmissionWebhook,ValidatingAdmissionWebhook,ResourceQuota,PodPreset
-    ```
-    
-    while starting the cluster.
+1. You have enabled the API type `settings.k8s.io/v1alpha1/podpreset`. For
+   example, this can be done by including `settings.k8s.io/v1alpha1=true` in
+   the `--runtime-config` option for the API server. In minikube add this flag
+   `--extra-config=apiserver.runtime-config=settings.k8s.io/v1alpha1=true` while
+   starting the cluster.
+1. You have enabled the admission controller named `PodPreset`. One way to doing this
+   is to include `PodPreset` in the `--enable-admission-plugins` option value specified
+   for the API server. For example, if you use Minikube, add this flag:
+
+   ```shell
+   --extra-config=apiserver.enable-admission-plugins=NamespaceLifecycle,LimitRanger,ServiceAccount,DefaultStorageClass,DefaultTolerationSeconds,NodeRestriction,MutatingAdmissionWebhook,ValidatingAdmissionWebhook,ResourceQuota,PodPreset
+   ```
+
+   while starting your cluster.
 
 ## How it works
 
@@ -64,31 +64,28 @@ When a pod creation request occurs, the system does the following:
    modified by a `PodPreset`. The annotation is of the form
    `podpreset.admission.kubernetes.io/podpreset-<pod-preset name>: "<resource version>"`.
 
-Each Pod can be matched by zero or more Pod Presets; and each `PodPreset` can be
-applied to zero or more pods. When a `PodPreset` is applied to one or more
-Pods, Kubernetes modifies the Pod Spec. For changes to `Env`, `EnvFrom`, and
-`VolumeMounts`, Kubernetes modifies the container spec for all containers in
-the Pod; for changes to `Volume`, Kubernetes modifies the Pod Spec.
+Each Pod can be matched by zero or more PodPresets; and each PodPreset can be
+applied to zero or more Pods. When a PodPreset is applied to one or more
+Pods, Kubernetes modifies the Pod Spec. For changes to `env`, `envFrom`, and
+`volumeMounts`, Kubernetes modifies the container spec for all containers in
+the Pod; for changes to `volumes`, Kubernetes modifies the Pod Spec.
 
 {{< note >}}
 A Pod Preset is capable of modifying the following fields in a Pod spec when appropriate:
-- The `.spec.containers` field.
-- The `initContainers` field (requires Kubernetes version 1.14.0 or later).
+- The `.spec.containers` field
+- The `.spec.initContainers` field
 {{< /note >}}
 
-### Disable Pod Preset for a Specific Pod
+### Disable Pod Preset for a specific pod
 
 There may be instances where you wish for a Pod to not be altered by any Pod
-Preset mutations. In these cases, you can add an annotation in the Pod Spec
+preset mutations. In these cases, you can add an annotation in the Pod's `.spec`
 of the form: `podpreset.admission.kubernetes.io/exclude: "true"`.
 
 
 
 ## {{% heading "whatsnext" %}}
 
-
 See [Injecting data into a Pod using PodPreset](/docs/tasks/inject-data-application/podpreset/)
 
 For more information about the background, see the [design proposal for PodPreset](https://git.k8s.io/community/contributors/design-proposals/service-catalog/pod-preset.md).
-
-

