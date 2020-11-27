diff --git a/content/en/docs/reference/glossary/volume.md b/content/en/docs/reference/glossary/volume.md
index 2076378bb..22cebca91 100755
--- a/content/en/docs/reference/glossary/volume.md
+++ b/content/en/docs/reference/glossary/volume.md
@@ -6,15 +6,15 @@ full_link: /docs/concepts/storage/volumes/
 short_description: >
   A directory containing data, accessible to the containers in a pod.
 
-aka: 
+aka:
 tags:
 - core-object
 - fundamental
 ---
  A directory containing data, accessible to the {{< glossary_tooltip text="containers" term_id="container" >}} in a {{< glossary_tooltip term_id="pod" >}}.
 
-<!--more--> 
+<!--more-->
 
 A Kubernetes volume lives as long as the Pod that encloses it. Consequently, a volume outlives any containers that run within the Pod, and data in the volume is preserved across container restarts.
 
-See [storage](https://kubernetes.io/docs/concepts/storage/) for more information.
+See [storage](/docs/concepts/storage/) for more information.

