diff --git a/content/en/docs/concepts/storage/volume-snapshots.md b/content/en/docs/concepts/storage/volume-snapshots.md
index a6cc12208..a93ea27e0 100644
--- a/content/en/docs/concepts/storage/volume-snapshots.md
+++ b/content/en/docs/concepts/storage/volume-snapshots.md
@@ -31,6 +31,8 @@ A `VolumeSnapshot` is a request for snapshot of a volume by a user. It is simila
 
 `VolumeSnapshotClass` allows you to specify different attributes belonging to a `VolumeSnapshot`. These attributes may differ among snapshots taken from the same volume on the storage system and therefore cannot be expressed by using the same `StorageClass` of a `PersistentVolumeClaim`.
 
+Volume snapshots provide Kubernetes users with a standardized way to copy a volume's contents at a particular point in time without creating an entirely new volume. This functionality enables, for example, database administrators to backup databases before performing edit or delete modifications.
+
 Users need to be aware of the following when using this feature:
 
 * API Objects `VolumeSnapshot`, `VolumeSnapshotContent`, and `VolumeSnapshotClass` are {{< glossary_tooltip term_id="CustomResourceDefinition" text="CRDs" >}}, not part of the core API.
@@ -94,14 +96,14 @@ using the attribute `volumeSnapshotClassName`. If nothing is set, then the defau
 
 For pre-provisioned snapshots, you need to specify a `volumeSnapshotContentName` as the source for the snapshot as shown in the following example. The `volumeSnapshotContentName` source field is required for pre-provisioned snapshots.
 
-```
+```yaml
 apiVersion: snapshot.storage.k8s.io/v1beta1
 kind: VolumeSnapshot
 metadata:
   name: test-snapshot
 spec:
   source:
-        volumeSnapshotContentName: test-content
+    volumeSnapshotContentName: test-content
 ```
 
 ## Volume Snapshot Contents
@@ -152,6 +154,4 @@ You can provision a new volume, pre-populated with data from a snapshot, by usin
 the *dataSource* field in the `PersistentVolumeClaim` object.
 
 For more details, see
-[Volume Snapshot and Restore Volume from Snapshot](/docs/concepts/storage/persistent-volumes/#volume-snapshot-and-restore-volume-from-snapshot-support).
-
-
+[Volume Snapshot and Restore Volume from Snapshot](/docs/concepts/storage/persistent-volumes/#volume-snapshot-and-restore-volume-from-snapshot-support).
\ No newline at end of file

