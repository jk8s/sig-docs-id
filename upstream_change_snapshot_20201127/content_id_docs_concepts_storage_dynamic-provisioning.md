diff --git a/content/en/docs/concepts/storage/dynamic-provisioning.md b/content/en/docs/concepts/storage/dynamic-provisioning.md
index dc82e5c2c..bedd431dc 100644
--- a/content/en/docs/concepts/storage/dynamic-provisioning.md
+++ b/content/en/docs/concepts/storage/dynamic-provisioning.md
@@ -33,7 +33,7 @@ from the API group `storage.k8s.io`. A cluster administrator can define as many
 that provisioner when provisioning.
 A cluster administrator can define and expose multiple flavors of storage (from
 the same or different storage systems) within a cluster, each with a custom set
-of parameters. This design also ensures that end users don’t have to worry
+of parameters. This design also ensures that end users don't have to worry
 about the complexity and nuances of how storage is provisioned, but still
 have the ability to select from multiple storage options.
 
@@ -85,8 +85,8 @@ is deprecated since v1.6. Users now can and should instead use the
 this field must match the name of a `StorageClass` configured by the
 administrator (see [below](#enabling-dynamic-provisioning)).
 
-To select the “fast” storage class, for example, a user would create the
-following `PersistentVolumeClaim`:
+To select the "fast" storage class, for example, a user would create the
+following PersistentVolumeClaim:
 
 ```yaml
 apiVersion: v1

