diff --git a/content/en/docs/tasks/run-application/horizontal-pod-autoscale-walkthrough.md b/content/en/docs/tasks/run-application/horizontal-pod-autoscale-walkthrough.md
index 2c00e4aa7..49009e126 100644
--- a/content/en/docs/tasks/run-application/horizontal-pod-autoscale-walkthrough.md
+++ b/content/en/docs/tasks/run-application/horizontal-pod-autoscale-walkthrough.md
@@ -11,39 +11,37 @@ weight: 100
 
 <!-- overview -->
 
-Horizontal Pod Autoscaler automatically scales the number of pods
+Horizontal Pod Autoscaler automatically scales the number of Pods
 in a replication controller, deployment, replica set or stateful set based on observed CPU utilization
 (or, with beta support, on some other, application-provided metrics).
 
 This document walks you through an example of enabling Horizontal Pod Autoscaler for the php-apache server.
-For more information on how Horizontal Pod Autoscaler behaves, see the 
+For more information on how Horizontal Pod Autoscaler behaves, see the
 [Horizontal Pod Autoscaler user guide](/docs/tasks/run-application/horizontal-pod-autoscale/).
 
 ## {{% heading "prerequisites" %}}
 
-
 This example requires a running Kubernetes cluster and kubectl, version 1.2 or later.
-[metrics-server](https://github.com/kubernetes-incubator/metrics-server/) monitoring needs to be deployed in the cluster
-to provide metrics via the resource metrics API, as Horizontal Pod Autoscaler uses this API to collect metrics. The instructions for deploying this are on the GitHub repository of [metrics-server](https://github.com/kubernetes-incubator/metrics-server/), if you followed [getting started on GCE guide](/docs/setup/production-environment/turnkey/gce/),
-metrics-server monitoring will be turned-on by default.
-
-To specify multiple resource metrics for a Horizontal Pod Autoscaler, you must have a Kubernetes cluster
-and kubectl at version 1.6 or later.  Furthermore, in order to make use of custom metrics, your cluster
-must be able to communicate with the API server providing the custom metrics API. Finally, to use metrics
-not related to any Kubernetes object you must have a Kubernetes cluster at version 1.10 or later, and
-you must be able to communicate with the API server that provides the external metrics API.
+[Metrics server](https://github.com/kubernetes-sigs/metrics-server) monitoring needs to be deployed
+in the cluster to provide metrics through the [Metrics API](https://github.com/kubernetes/metrics).
+Horizontal Pod Autoscaler uses this API to collect metrics. To learn how to deploy the metrics-server,
+see the [metrics-server documentation](https://github.com/kubernetes-sigs/metrics-server#deployment).
+
+To specify multiple resource metrics for a Horizontal Pod Autoscaler, you must have a
+Kubernetes cluster and kubectl at version 1.6 or later. To make use of custom metrics, your cluster
+must be able to communicate with the API server providing the custom Metrics API.
+Finally, to use metrics not related to any Kubernetes object you must have a
+Kubernetes cluster at version 1.10 or later, and you must be able to communicate
+with the API server that provides the external Metrics API.
 See the [Horizontal Pod Autoscaler user guide](/docs/tasks/run-application/horizontal-pod-autoscale/#support-for-custom-metrics) for more details.
 
-
-
 <!-- steps -->
 
-## Run & expose php-apache server
+## Run and expose php-apache server
 
-To demonstrate Horizontal Pod Autoscaler we will use a custom docker image based on the php-apache image.
-The Dockerfile has the following content:
+To demonstrate Horizontal Pod Autoscaler we will use a custom docker image based on the php-apache image. The Dockerfile has the following content:
 
-```
+```dockerfile
 FROM php:5-apache
 COPY index.php /var/www/html/index.php
 RUN chmod a+rx index.php
@@ -51,7 +49,7 @@ RUN chmod a+rx index.php
 
 It defines an index.php page which performs some CPU intensive computations:
 
-```
+```php
 <?php
   $x = 0.0001;
   for ($i = 0; $i <= 1000000; $i++) {
@@ -66,11 +64,12 @@ using the following configuration:
 
 {{< codenew file="application/php-apache.yaml" >}}
 
-
 Run the following command:
+
 ```shell
 kubectl apply -f https://k8s.io/examples/application/php-apache.yaml
 ```
+
 ```
 deployment.apps/php-apache created
 service/php-apache created
@@ -90,6 +89,7 @@ See [here](/docs/tasks/run-application/horizontal-pod-autoscale/#algorithm-detai
 ```shell
 kubectl autoscale deployment php-apache --cpu-percent=50 --min=1 --max=10
 ```
+
 ```
 horizontalpodautoscaler.autoscaling/php-apache autoscaled
 ```
@@ -99,10 +99,10 @@ We may check the current status of autoscaler by running:
 ```shell
 kubectl get hpa
 ```
+
 ```
 NAME         REFERENCE                     TARGET    MINPODS   MAXPODS   REPLICAS   AGE
 php-apache   Deployment/php-apache/scale   0% / 50%  1         10        1          18s
-
 ```
 
 Please note that the current CPU consumption is 0% as we are not sending any requests to the server
@@ -114,11 +114,7 @@ Now, we will see how the autoscaler reacts to increased load.
 We will start a container, and send an infinite loop of queries to the php-apache service (please run it in a different terminal):
 
 ```shell
-kubectl run -it --rm load-generator --image=busybox /bin/sh
-
-Hit enter for command prompt
-
-while true; do wget -q -O- http://php-apache; done
+kubectl run -i --tty load-generator --rm --image=busybox --restart=Never -- /bin/sh -c "while sleep 0.01; do wget -q -O- http://php-apache; done"
 ```
 
 Within a minute or so, we should see the higher CPU load by executing:
@@ -126,10 +122,10 @@ Within a minute or so, we should see the higher CPU load by executing:
 ```shell
 kubectl get hpa
 ```
+
 ```
 NAME         REFERENCE                     TARGET      MINPODS   MAXPODS   REPLICAS   AGE
 php-apache   Deployment/php-apache/scale   305% / 50%  1         10        1          3m
-
 ```
 
 Here, CPU consumption has increased to 305% of the request.
@@ -138,6 +134,7 @@ As a result, the deployment was resized to 7 replicas:
 ```shell
 kubectl get deployment php-apache
 ```
+
 ```
 NAME         READY   UP-TO-DATE   AVAILABLE   AGE
 php-apache   7/7      7           7           19m
@@ -161,6 +158,7 @@ Then we will verify the result state (after a minute or so):
 ```shell
 kubectl get hpa
 ```
+
 ```
 NAME         REFERENCE                     TARGET       MINPODS   MAXPODS   REPLICAS   AGE
 php-apache   Deployment/php-apache/scale   0% / 50%     1         10        1          11m
@@ -169,6 +167,7 @@ php-apache   Deployment/php-apache/scale   0% / 50%     1         10        1
 ```shell
 kubectl get deployment php-apache
 ```
+
 ```
 NAME         READY   UP-TO-DATE   AVAILABLE   AGE
 php-apache   1/1     1            1           27m
@@ -180,8 +179,6 @@ Here CPU utilization dropped to 0, and so HPA autoscaled the number of replicas
 Autoscaling the replicas may take a few minutes.
 {{< /note >}}
 
-
-
 <!-- discussion -->
 
 ## Autoscaling on multiple metrics and custom metrics
@@ -244,8 +241,8 @@ There are two other types of metrics, both of which are considered *custom metri
 object metrics.  These metrics may have names which are cluster specific, and require a more
 advanced cluster monitoring setup.
 
-The first of these alternative metric types is *pod metrics*.  These metrics describe pods, and
-are averaged together across pods and compared with a target value to determine the replica count.
+The first of these alternative metric types is *pod metrics*.  These metrics describe Pods, and
+are averaged together across Pods and compared with a target value to determine the replica count.
 They work much like resource metrics, except that they *only* support a `target` type of `AverageValue`.
 
 Pod metrics are specified using a metric block like this:
@@ -261,11 +258,11 @@ pods:
 ```
 
 The second alternative metric type is *object metrics*. These metrics describe a different
-object in the same namespace, instead of describing pods. The metrics are not necessarily
+object in the same namespace, instead of describing Pods. The metrics are not necessarily
 fetched from the object; they only describe it. Object metrics support `target` types of
 both `Value` and `AverageValue`.  With `Value`, the target is compared directly to the returned
 metric from the API. With `AverageValue`, the value returned from the custom metrics API is divided
-by the number of pods before being compared to the target. The following example is the YAML
+by the number of Pods before being compared to the target. The following example is the YAML
 representation of the `requests-per-second` metric.
 
 ```yaml
@@ -423,7 +420,8 @@ we can use `kubectl describe hpa`:
 ```shell
 kubectl describe hpa cm-test
 ```
-```shell
+
+```
 Name:                           cm-test
 Namespace:                      prom
 Labels:                         <none>
@@ -478,8 +476,7 @@ We will create the autoscaler by executing the following command:
 ```shell
 kubectl create -f https://k8s.io/examples/application/hpa/php-apache.yaml
 ```
+
 ```
 horizontalpodautoscaler.autoscaling/php-apache created
 ```
-
-

