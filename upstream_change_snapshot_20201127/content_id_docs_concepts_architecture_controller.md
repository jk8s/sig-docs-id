diff --git a/content/en/docs/concepts/architecture/controller.md b/content/en/docs/concepts/architecture/controller.md
index 547a624a9..d6897d297 100644
--- a/content/en/docs/concepts/architecture/controller.md
+++ b/content/en/docs/concepts/architecture/controller.md
@@ -92,9 +92,18 @@ Controllers that interact with external state find their desired state from
 the API server, then communicate directly with an external system to bring
 the current state closer in line.
 
-(There actually is a controller that horizontally scales the
-nodes in your cluster. See
-[Cluster autoscaling](/docs/tasks/administer-cluster/cluster-management/#cluster-autoscaling)).
+(There actually is a [controller](https://github.com/kubernetes/autoscaler/)
+that horizontally scales the nodes in your cluster.)
+
+The important point here is that the controller makes some change to bring about
+your desired state, and then reports current state back to your cluster's API server.
+Other control loops can observe that reported data and take their own actions.
+
+In the thermostat example, if the room is very cold then a different controller
+might also turn on a frost protection heater. With Kubernetes clusters, the control
+plane indirectly works with IP address management tools, storage services,
+cloud provider APIS, and other services by
+[extending Kubernetes](/docs/concepts/extend-kubernetes/) to implement that.
 
 ## Desired versus current state {#desired-vs-current}
 
@@ -113,9 +122,9 @@ useful changes, it doesn't matter if the overall state is or is not stable.
 As a tenet of its design, Kubernetes uses lots of controllers that each manage
 a particular aspect of cluster state. Most commonly, a particular control loop
 (controller) uses one kind of resource as its desired state, and has a different
-kind of resource that it manages to make that desired state happen. For example, 
+kind of resource that it manages to make that desired state happen. For example,
 a controller for Jobs tracks Job objects (to discover new work) and Pod objects
-(to run the Jobs, and then to see when the work is finished). In this case 
+(to run the Jobs, and then to see when the work is finished). In this case
 something else creates the Jobs, whereas the Job controller creates Pods.
 
 It's useful to have simple controllers rather than one, monolithic set of control
@@ -140,7 +149,7 @@ the {{< glossary_tooltip term_id="kube-controller-manager" >}}. These
 built-in controllers provide important core behaviors.
 
 The Deployment controller and Job controller are examples of controllers that
-come as part of Kubernetes itself (“built-in” controllers).
+come as part of Kubernetes itself ("built-in" controllers).
 Kubernetes lets you run a resilient control plane, so that if any of the built-in
 controllers were to fail, another part of the control plane will take over the work.
 
@@ -154,8 +163,7 @@ controller does.
 
 ## {{% heading "whatsnext" %}}
 
-* Read about the [Kubernetes control plane](/docs/concepts/#kubernetes-control-plane)
-* Discover some of the basic [Kubernetes objects](/docs/concepts/#kubernetes-objects)
+* Read about the [Kubernetes control plane](/docs/concepts/overview/components/#control-plane-components)
+* Discover some of the basic [Kubernetes objects](/docs/concepts/overview/working-with-objects/kubernetes-objects/)
 * Learn more about the [Kubernetes API](/docs/concepts/overview/kubernetes-api/)
 * If you want to write your own controller, see [Extension Patterns](/docs/concepts/extend-kubernetes/extend-cluster/#extension-patterns) in Extending Kubernetes.
-

