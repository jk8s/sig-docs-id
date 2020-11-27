diff --git a/content/en/docs/concepts/storage/persistent-volumes.md b/content/en/docs/concepts/storage/persistent-volumes.md
index f60b90cb3..cf915bfa5 100644
--- a/content/en/docs/concepts/storage/persistent-volumes.md
+++ b/content/en/docs/concepts/storage/persistent-volumes.md
@@ -19,9 +19,6 @@ weight: 20
 
 This document describes the current state of _persistent volumes_ in Kubernetes. Familiarity with [volumes](/docs/concepts/storage/volumes/) is suggested.
 
-
-
-
 <!-- body -->
 
 ## Introduction
@@ -148,7 +145,11 @@ The `Recycle` reclaim policy is deprecated. Instead, the recommended approach is
 
 If supported by the underlying volume plugin, the `Recycle` reclaim policy performs a basic scrub (`rm -rf /thevolume/*`) on the volume and makes it available again for a new claim.
 
-However, an administrator can configure a custom recycler Pod template using the Kubernetes controller manager command line arguments as described [here](/docs/admin/kube-controller-manager/). The custom recycler Pod template must contain a `volumes` specification, as shown in the example below:
+However, an administrator can configure a custom recycler Pod template using
+the Kubernetes controller manager command line arguments as described in the
+[reference](/docs/reference/command-line-tools-reference/kube-controller-manager/).
+The custom recycler Pod template must contain a `volumes` specification, as
+shown in the example below:
 
 ```yaml
 apiVersion: v1
@@ -173,6 +174,47 @@ spec:
 
 However, the particular path specified in the custom recycler Pod template in the `volumes` part is replaced with the particular path of the volume that is being recycled.
 
+### Reserving a PersistentVolume
+
+The control plane can [bind PersistentVolumeClaims to matching PersistentVolumes](#binding) in the
+cluster. However, if you want a PVC to bind to a specific PV, you need to pre-bind them.
+
+By specifying a PersistentVolume in a PersistentVolumeClaim, you declare a binding between that specific PV and PVC.
+If the PersistentVolume exists and has not reserved PersistentVolumeClaims through its `claimRef` field, then the PersistentVolume and PersistentVolumeClaim will be bound.
+
+The binding happens regardless of some volume matching criteria, including node affinity.
+The control plane still checks that [storage class](/docs/concepts/storage/storage-classes/), access modes, and requested storage size are valid.
+
+```yaml
+apiVersion: v1
+kind: PersistentVolumeClaim
+metadata:
+  name: foo-pvc
+  namespace: foo
+spec:
+  storageClassName: "" # Empty string must be explicitly set otherwise default StorageClass will be set
+  volumeName: foo-pv
+  ...
+```
+
+This method does not guarantee any binding privileges to the PersistentVolume. If other PersistentVolumeClaims could use the PV that you specify, you first need to reserve that storage volume. Specify the relevant PersistentVolumeClaim in the `claimRef` field of the PV so that other PVCs can not bind to it.
+
+```yaml
+apiVersion: v1
+kind: PersistentVolume
+metadata:
+  name: foo-pv
+spec:
+  storageClassName: ""
+  claimRef:
+    name: foo-pvc
+    namespace: foo
+  ...
+```
+
+This is useful if you want to consume PersistentVolumes that have their `claimPolicy` set
+to `Retain`, including cases where you are reusing an existing PV.
+
 ### Expanding Persistent Volumes Claims
 
 {{< feature-state for_k8s_version="v1.11" state="beta" >}}
@@ -253,6 +295,16 @@ FlexVolume resize is possible only when the underlying driver supports resize.
 Expanding EBS volumes is a time-consuming operation. Also, there is a per-volume quota of one modification every 6 hours.
 {{< /note >}}
 
+#### Recovering from Failure when Expanding Volumes
+
+If expanding underlying storage fails, the cluster administrator can manually recover the Persistent Volume Claim (PVC) state and cancel the resize requests. Otherwise, the resize requests are continuously retried by the controller without administrator intervention.
+
+1. Mark the PersistentVolume(PV) that is bound to the PersistentVolumeClaim(PVC) with `Retain` reclaim policy.
+2. Delete the PVC. Since PV has `Retain` reclaim policy - we will not lose any data when we recreate the PVC.
+3. Delete the `claimRef` entry from PV specs, so as new PVC can bind to it. This should make the PV `Available`.
+4. Re-create the PVC with smaller size than PV and set `volumeName` field of the PVC to the name of the PV. This should bind new PVC to existing PV.
+5. Don't forget to restore the reclaim policy of the PV.
+
 
 ## Types of Persistent Volumes
 

