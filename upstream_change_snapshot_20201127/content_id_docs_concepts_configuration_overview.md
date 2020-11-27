diff --git a/content/en/docs/concepts/configuration/overview.md b/content/en/docs/concepts/configuration/overview.md
index 744034f8e..5882ce95d 100644
--- a/content/en/docs/concepts/configuration/overview.md
+++ b/content/en/docs/concepts/configuration/overview.md
@@ -73,7 +73,7 @@ A desired state of an object is described by a Deployment, and if changes to tha
 
 ## Container Images
 
-The [imagePullPolicy](/docs/concepts/containers/images/#updating-images) and the tag of the image affect when the [kubelet](/docs/admin/kubelet/) attempts to pull the specified image.
+The [imagePullPolicy](/docs/concepts/containers/images/#updating-images) and the tag of the image affect when the [kubelet](/docs/reference/command-line-tools-reference/kubelet/) attempts to pull the specified image.
 
 - `imagePullPolicy: IfNotPresent`: the image is pulled only if it is not already present locally.
 

