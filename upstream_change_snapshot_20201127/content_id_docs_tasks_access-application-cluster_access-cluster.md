diff --git a/content/en/docs/tasks/access-application-cluster/access-cluster.md b/content/en/docs/tasks/access-application-cluster/access-cluster.md
index 39ad8b4b7..7f7432011 100644
--- a/content/en/docs/tasks/access-application-cluster/access-cluster.md
+++ b/content/en/docs/tasks/access-application-cluster/access-cluster.md
@@ -8,9 +8,6 @@ content_type: concept
 
 This topic discusses multiple ways to interact with clusters.
 
-
-
-
 <!-- body -->
 
 ## Accessing for the first time with kubectl
@@ -29,8 +26,9 @@ Check the location and credentials that kubectl knows about with this command:
 kubectl config view
 ```
 
-Many of the [examples](/docs/user-guide/kubectl-cheatsheet) provide an introduction to using
-kubectl and complete documentation is found in the [kubectl manual](/docs/user-guide/kubectl-overview).
+Many of the [examples](/docs/reference/kubectl/cheatsheet/) provide an introduction to using
+kubectl and complete documentation is found in the
+[kubectl manual](/docs/reference/kubectl/overview/).
 
 ## Directly accessing the REST API
 
@@ -151,9 +149,8 @@ certificate.
 
 On some clusters, the apiserver does not require authentication; it may serve
 on localhost, or be protected by a firewall.  There is not a standard
-for this.  [Configuring Access to the API](/docs/reference/access-authn-authz/controlling-access/)
-describes how a cluster admin can configure this.  Such approaches may conflict
-with future high-availability support.
+for this.  [Controlling Access to the API](/docs/concepts/security/controlling-access)
+describes how a cluster admin can configure this.
 
 ## Programmatic access to the API
 
@@ -165,7 +162,7 @@ client libraries.
 * To get the library, run the following command: `go get k8s.io/client-go@kubernetes-<kubernetes-version-number>`, see [INSTALL.md](https://github.com/kubernetes/client-go/blob/master/INSTALL.md#for-the-casual-user) for detailed installation instructions. See [https://github.com/kubernetes/client-go](https://github.com/kubernetes/client-go#compatibility-matrix) to see which versions are supported.
 * Write an application atop of the client-go clients. Note that client-go defines its own API objects, so if needed, please import API definitions from client-go rather than from the main repository, e.g., `import "k8s.io/client-go/kubernetes"` is correct.
 
-The Go client can use the same [kubeconfig file](/docs/concepts/cluster-administration/authenticate-across-clusters-kubeconfig/)
+The Go client can use the same [kubeconfig file](/docs/concepts/configuration/organize-cluster-access-kubeconfig/)
 as the kubectl CLI does to locate and authenticate to the apiserver. See this [example](https://git.k8s.io/client-go/examples/out-of-cluster-client-configuration/main.go).
 
 If the application is deployed as a Pod in the cluster, please refer to the [next section](#accessing-the-api-from-a-pod).
@@ -174,7 +171,7 @@ If the application is deployed as a Pod in the cluster, please refer to the [nex
 
 To use [Python client](https://github.com/kubernetes-client/python), run the following command: `pip install kubernetes`. See [Python Client Library page](https://github.com/kubernetes-client/python) for more installation options.
 
-The Python client can use the same [kubeconfig file](/docs/concepts/cluster-administration/authenticate-across-clusters-kubeconfig/)
+The Python client can use the same [kubeconfig file](/docs/concepts/configuration/organize-cluster-access-kubeconfig/)
 as the kubectl CLI does to locate and authenticate to the apiserver. See this [example](https://github.com/kubernetes-client/python/tree/master/examples).
 
 ### Other languages
@@ -219,7 +216,9 @@ In each case, the credentials of the pod are used to communicate securely with t
 
 The previous section was about connecting the Kubernetes API server.  This section is about
 connecting to other services running on Kubernetes cluster.  In Kubernetes, the
-[nodes](/docs/admin/node), [pods](/docs/user-guide/pods) and [services](/docs/user-guide/services) all have
+[nodes](/docs/concepts/architecture/nodes/),
+[pods](/docs/concepts/workloads/pods/) and
+[services](/docs/concepts/services-networking/service/) all have
 their own IPs.  In many cases, the node IPs, pod IPs, and some service IPs on a cluster will not be
 routable, so they will not be reachable from a machine outside the cluster,
 such as your desktop machine.
@@ -230,7 +229,7 @@ You have several options for connecting to nodes, pods and services from outside
 
   - Access services through public IPs.
     - Use a service with type `NodePort` or `LoadBalancer` to make the service reachable outside
-      the cluster.  See the [services](/docs/user-guide/services) and
+      the cluster.  See the [services](/docs/concepts/services-networking/service/) and
       [kubectl expose](/docs/reference/generated/kubectl/kubectl-commands/#expose) documentation.
     - Depending on your cluster environment, this may just expose the service to your corporate network,
       or it may expose it to the internet.  Think about whether the service being exposed is secure.

