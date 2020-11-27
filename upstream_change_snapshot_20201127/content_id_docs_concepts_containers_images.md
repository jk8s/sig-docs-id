diff --git a/content/en/docs/concepts/containers/images.md b/content/en/docs/concepts/containers/images.md
index a01e8d84f..be25fd4e1 100644
--- a/content/en/docs/concepts/containers/images.md
+++ b/content/en/docs/concepts/containers/images.md
@@ -19,8 +19,6 @@ before referring to it in a
 
 This page provides an outline of the container image concept.
 
-
-
 <!-- body -->
 
 ## Image names
@@ -49,7 +47,7 @@ to roll back to a working version.
 Instead, specify a meaningful tag such as `v1.42.0`.
 {{< /caution >}}
 
-## Updating Images
+## Updating images
 
 The default pull policy is `IfNotPresent` which causes the
 {{< glossary_tooltip text="kubelet" term_id="kubelet" >}} to skip
@@ -63,13 +61,13 @@ you can do one of the following:
 
 When `imagePullPolicy` is defined without a specific value, it is also set to `Always`.
 
-## Multi-architecture Images with Manifests
+## Multi-architecture images with image indexes
 
-As well as providing binary images, a container registry can also serve a [container image manifest](https://github.com/opencontainers/image-spec/blob/master/manifest.md). A manifest can reference image manifests for architecture-specific versions of an container. The idea is that you can have a name for an image (for example: `pause`, `example/mycontainer`, `kube-apiserver`) and allow different systems to fetch the right binary image for the machine architecture they are using.
+As well as providing binary images, a container registry can also serve a [container image index](https://github.com/opencontainers/image-spec/blob/master/image-index.md). An image index can point to multiple [image manifests](https://github.com/opencontainers/image-spec/blob/master/manifest.md) for architecture-specific versions of a container. The idea is that you can have a name for an image (for example: `pause`, `example/mycontainer`, `kube-apiserver`) and allow different systems to fetch the right binary image for the machine architecture they are using.
 
 Kubernetes itself typically names container images with a suffix `-$(ARCH)`. For backward compatibility, please generate the older images with suffixes. The idea is to generate say `pause` image which has the manifest for all the arch(es) and say `pause-amd64` which is backwards compatible for older configurations or YAML files which may have hard coded the images with suffixes.
 
-## Using a Private Registry
+## Using a private registry
 
 Private registries may require keys to read images from them.  
 Credentials can be provided in several ways:
@@ -88,7 +86,7 @@ Credentials can be provided in several ways:
 
 These options are explaind in more detail below.
 
-### Configuring Nodes to authenticate to a Private Registry
+### Configuring nodes to authenticate to a private registry
 
 If you run Docker on your nodes, you can configure the Docker container
 runtime to authenticate to a private container registry.
@@ -96,7 +94,7 @@ runtime to authenticate to a private container registry.
 This approach is suitable if you can control node configuration.
 
 {{< note >}}
-Kubernetes as only supports the `auths` and `HttpHeaders` section in Docker configuration.
+Default Kubernetes only supports the `auths` and `HttpHeaders` section in Docker configuration.
 Docker credential helpers (`credHelpers` or `credsStore`) are not supported.
 {{< /note >}}
 
@@ -129,7 +127,7 @@ example, run these on your desktop/laptop:
       - for example, to test this out: `for n in $nodes; do scp ~/.docker/config.json root@"$n":/var/lib/kubelet/config.json; done`
 
 {{< note >}}
-For production clusers, use a configuration management tool so that you can apply this
+For production clusters, use a configuration management tool so that you can apply this
 setting to all the nodes where you need it.
 {{< /note >}}
 
@@ -180,7 +178,7 @@ template needs to include the `.docker/config.json` or mount a drive that contai
 All pods will have read access to images in any private registry once private
 registry keys are added to the `.docker/config.json`.
 
-### Pre-pulled Images
+### Pre-pulled images
 
 {{< note >}}
 This approach is suitable if you can control node configuration.  It
@@ -199,7 +197,7 @@ This can be used to preload certain images for speed or as an alternative to aut
 
 All pods will have read access to any pre-pulled images.
 
-### Specifying ImagePullSecrets on a Pod
+### Specifying imagePullSecrets on a Pod
 
 {{< note >}}
 This is the recommended approach to run containers based on images
@@ -208,7 +206,7 @@ in private registries.
 
 Kubernetes supports specifying container image registry keys on a Pod.
 
-#### Creating a Secret with a Docker Config
+#### Creating a Secret with a Docker config
 
 Run the following command, substituting the appropriate uppercase values:
 
@@ -261,14 +259,14 @@ EOF
 This needs to be done for each pod that is using a private registry.
 
 However, setting of this field can be automated by setting the imagePullSecrets
-in a [ServiceAccount](/docs/user-guide/service-accounts) resource.
+in a [ServiceAccount](/docs/tasks/configure-pod-container/configure-service-account/) resource.
 
 Check [Add ImagePullSecrets to a Service Account](/docs/tasks/configure-pod-container/configure-service-account/#add-imagepullsecrets-to-a-service-account) for detailed instructions.
 
 You can use this in conjunction with a per-node `.docker/config.json`.  The credentials
 will be merged.
 
-## Use Cases
+## Use cases
 
 There are a number of solutions for configuring private registries.  Here are some
 common use cases and suggested solutions.

