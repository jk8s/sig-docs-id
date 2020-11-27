diff --git a/content/en/docs/tasks/access-application-cluster/list-all-running-container-images.md b/content/en/docs/tasks/access-application-cluster/list-all-running-container-images.md
index d1e1ba156..3a8983eec 100644
--- a/content/en/docs/tasks/access-application-cluster/list-all-running-container-images.md
+++ b/content/en/docs/tasks/access-application-cluster/list-all-running-container-images.md
@@ -9,15 +9,10 @@ weight: 100
 This page shows how to use kubectl to list all of the Container images
 for Pods running in a cluster.
 
-
-
 ## {{% heading "prerequisites" %}}
 
-
 {{< include "task-tutorial-prereqs.md" >}} {{< version-check >}}
 
-
-
 <!-- steps -->
 
 In this exercise you will use kubectl to fetch all of the Pods
@@ -30,14 +25,14 @@ of Containers for each.
 - Format the output to include only the list of Container image names
   using `-o jsonpath={..image}`.  This will recursively parse out the
   `image` field from the returned json.
-  - See the [jsonpath reference](/docs/user-guide/jsonpath/)
+  - See the [jsonpath reference](/docs/reference/kubectl/jsonpath/)
     for further information on how to use jsonpath.
 - Format the output using standard tools: `tr`, `sort`, `uniq`
   - Use `tr` to replace spaces with newlines
   - Use `sort` to sort the results
   - Use `uniq` to aggregate image counts
 
-```sh
+```shell
 kubectl get pods --all-namespaces -o jsonpath="{..image}" |\
 tr -s '[[:space:]]' '\n' |\
 sort |\
@@ -52,7 +47,7 @@ field within the Pod.  This ensures the correct field is retrieved
 even when the field name is repeated,
 e.g. many fields are called `name` within a given item:
 
-```sh
+```shell
 kubectl get pods --all-namespaces -o jsonpath="{.items[*].spec.containers[*].image}"
 ```
 
@@ -74,7 +69,7 @@ Pod is returned instead of a list of items.
 The formatting can be controlled further by using the `range` operation to
 iterate over elements individually.
 
-```sh
+```shell
 kubectl get pods --all-namespaces -o=jsonpath='{range .items[*]}{"\n"}{.metadata.name}{":\t"}{range .spec.containers[*]}{.image}{", "}{end}{end}' |\
 sort
 ```
@@ -84,7 +79,7 @@ sort
 To target only Pods matching a specific label, use the -l flag.  The
 following matches only Pods with labels matching `app=nginx`.
 
-```sh
+```shell
 kubectl get pods --all-namespaces -o=jsonpath="{..image}" -l app=nginx
 ```
 
@@ -93,7 +88,7 @@ kubectl get pods --all-namespaces -o=jsonpath="{..image}" -l app=nginx
 To target only pods in a specific namespace, use the namespace flag. The
 following matches only Pods in the `kube-system` namespace.
 
-```sh
+```shell
 kubectl get pods --namespace kube-system -o jsonpath="{..image}"
 ```
 
@@ -102,27 +97,14 @@ kubectl get pods --namespace kube-system -o jsonpath="{..image}"
 As an alternative to jsonpath, Kubectl supports using [go-templates](https://golang.org/pkg/text/template/)
 for formatting the output:
 
-
-```sh
+```shell
 kubectl get pods --all-namespaces -o go-template --template="{{range .items}}{{range .spec.containers}}{{.image}} {{end}}{{end}}"
 ```
 
-
-
-
-
-<!-- discussion -->
-
-
-
 ## {{% heading "whatsnext" %}}
 
-
 ### Reference
 
-* [Jsonpath](/docs/user-guide/jsonpath/) reference guide
+* [Jsonpath](/docs/reference/kubectl/jsonpath/) reference guide
 * [Go template](https://golang.org/pkg/text/template/) reference guide
 
-
-
-

