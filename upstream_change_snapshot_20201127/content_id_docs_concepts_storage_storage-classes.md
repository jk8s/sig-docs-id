diff --git a/content/en/docs/concepts/storage/storage-classes.md b/content/en/docs/concepts/storage/storage-classes.md
index a16baf46b..e6846c7ea 100644
--- a/content/en/docs/concepts/storage/storage-classes.md
+++ b/content/en/docs/concepts/storage/storage-classes.md
@@ -15,8 +15,6 @@ This document describes the concept of a StorageClass in Kubernetes. Familiarity
 with [volumes](/docs/concepts/storage/volumes/) and
 [persistent volumes](/docs/concepts/storage/persistent-volumes) is suggested.
 
-
-
 <!-- body -->
 
 ## Introduction
@@ -96,7 +94,7 @@ run, what volume plugin it uses (including Flex), etc. The repository
 [kubernetes-sigs/sig-storage-lib-external-provisioner](https://github.com/kubernetes-sigs/sig-storage-lib-external-provisioner)
 houses a library for writing external provisioners that implements the bulk of
 the specification. Some external provisioners are listed under the repository
-[kubernetes-incubator/external-storage](https://github.com/kubernetes-incubator/external-storage).
+[kubernetes-sigs/sig-storage-lib-external-provisioner](https://github.com/kubernetes-sigs/sig-storage-lib-external-provisioner).
 
 For example, NFS doesn't provide an internal provisioner, but an external
 provisioner can be used. There are also cases when 3rd party storage
@@ -168,11 +166,11 @@ A cluster administrator can address this issue by specifying the `WaitForFirstCo
 will delay the binding and provisioning of a PersistentVolume until a Pod using the PersistentVolumeClaim is created.
 PersistentVolumes will be selected or provisioned conforming to the topology that is
 specified by the Pod's scheduling constraints. These include, but are not limited to, [resource
-requirements](/docs/concepts/configuration/manage-compute-resources-container),
+requirements](/docs/concepts/configuration/manage-resources-containers/),
 [node selectors](/docs/concepts/scheduling-eviction/assign-pod-node/#nodeselector),
 [pod affinity and
 anti-affinity](/docs/concepts/scheduling-eviction/assign-pod-node/#affinity-and-anti-affinity),
-and [taints and tolerations](/docs/concepts/configuration/taint-and-toleration).
+and [taints and tolerations](/docs/concepts/scheduling-eviction/taint-and-toleration).
 
 The following plugins support `WaitForFirstConsumer` with dynamic provisioning:
 
@@ -244,7 +242,7 @@ parameters:
 ```
 
 * `type`: `io1`, `gp2`, `sc1`, `st1`. See
-  [AWS docs](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSVolumeTypes.html)
+  [AWS docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSVolumeTypes.html)
   for details. Default: `gp2`.
 * `zone` (Deprecated): AWS zone. If neither `zone` nor `zones` is specified, volumes are
   generally round-robin-ed across all active zones where Kubernetes cluster
@@ -256,7 +254,7 @@ parameters:
 * `iopsPerGB`: only for `io1` volumes. I/O operations per second per GiB. AWS
   volume plugin multiplies this with size of requested volume to compute IOPS
   of the volume and caps it at 20 000 IOPS (maximum supported by AWS, see
-  [AWS docs](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSVolumeTypes.html).
+  [AWS docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSVolumeTypes.html).
   A string is expected here, i.e. `"10"`, not `10`.
 * `fsType`: fsType that is supported by kubernetes. Default: `"ext4"`.
 * `encrypted`: denotes whether the EBS volume should be encrypted or not.
@@ -417,6 +415,21 @@ This internal provisioner of OpenStack is deprecated. Please use [the external c
 
 ### vSphere
 
+There are two types of provisioners for vSphere storage classes: 
+
+- [CSI provisioner](#csi-provisioner): `csi.vsphere.vmware.com`
+- [vCP provisioner](#vcp-provisioner): `kubernetes.io/vsphere-volume`
+
+In-tree provisioners are [deprecated](/blog/2019/12/09/kubernetes-1-17-feature-csi-migration-beta/#why-are-we-migrating-in-tree-plugins-to-csi). For more information on the CSI provisioner, see [Kubernetes vSphere CSI Driver](https://vsphere-csi-driver.sigs.k8s.io/) and [vSphereVolume CSI migration](/docs/concepts/storage/volumes/#csi-migration-5).
+
+#### CSI Provisioner {#vsphere-provisioner-csi}
+
+The vSphere CSI StorageClass provisioner works with Tanzu Kubernetes clusters. For an example, refer to the [vSphere CSI repository](https://raw.githubusercontent.com/kubernetes-sigs/vsphere-csi-driver/master/example/vanilla-k8s-file-driver/example-sc.yaml).
+
+#### vCP Provisioner 
+
+The following examples use the VMware Cloud Provider (vCP) StorageClass provisioner.  
+
 1. Create a StorageClass with a user specified disk format.
 
     ```yaml
@@ -686,7 +699,7 @@ provisioner: kubernetes.io/portworx-volume
 parameters:
   repl: "1"
   snap_interval:   "70"
-  io_priority:  "high"
+  priority_io:  "high"
 
 ```
 
@@ -695,7 +708,7 @@ parameters:
 * `repl`: number of synchronous replicas to be provided in the form of
   replication factor `1..3` (default: `1`) A string is expected here i.e.
   `"1"` and not `1`.
-* `io_priority`: determines whether the volume will be created from higher
+* `priority_io`: determines whether the volume will be created from higher
   performance or a lower priority storage `high/medium/low` (default: `low`).
 * `snap_interval`: clock/time interval in minutes for when to trigger snapshots.
   Snapshots are incremental based on difference with the prior snapshot, 0
@@ -821,4 +834,3 @@ Delaying volume binding allows the scheduler to consider all of a Pod's
 scheduling constraints when choosing an appropriate PersistentVolume for a
 PersistentVolumeClaim.
 
-

