diff --git a/content/en/docs/concepts/services-networking/ingress-controllers.md b/content/en/docs/concepts/services-networking/ingress-controllers.md
index 33875e363..dcfba66a4 100644
--- a/content/en/docs/concepts/services-networking/ingress-controllers.md
+++ b/content/en/docs/concepts/services-networking/ingress-controllers.md
@@ -22,12 +22,14 @@ Kubernetes as a project currently supports and maintains [GCE](https://git.k8s.i
 
 ## Additional controllers
 
+{{% thirdparty-content %}}
+
 * [AKS Application Gateway Ingress Controller](https://github.com/Azure/application-gateway-kubernetes-ingress) is an ingress controller that enables ingress to [AKS clusters](https://docs.microsoft.com/azure/aks/kubernetes-walkthrough-portal) using the [Azure Application Gateway](https://docs.microsoft.com/azure/application-gateway/overview).
 * [Ambassador](https://www.getambassador.io/) API Gateway is an [Envoy](https://www.envoyproxy.io) based ingress 
   controller with [community](https://www.getambassador.io/docs) or 
   [commercial](https://www.getambassador.io/pro/) support from [Datawire](https://www.datawire.io/).
-* [AppsCode Inc.](https://appscode.com) offers support and maintenance for the most widely used [HAProxy](http://www.haproxy.org/) based ingress controller [Voyager](https://appscode.com/products/voyager). 
-* [AWS ALB Ingress Controller](https://github.com/kubernetes-sigs/aws-alb-ingress-controller) enables ingress using the [AWS Application Load Balancer](https://aws.amazon.com/elasticloadbalancing/).
+* [AppsCode Inc.](https://appscode.com) offers support and maintenance for the most widely used [HAProxy](https://www.haproxy.org/) based ingress controller [Voyager](https://appscode.com/products/voyager). 
+* [AWS Load Balancer Controller](https://github.com/kubernetes-sigs/aws-load-balancer-controller) (formerly known as AWS ALB Ingress Controller) enables ingress using [AWS Elastic Load Balancing](https://aws.amazon.com/elasticloadbalancing/).
 * [Contour](https://projectcontour.io/) is an [Envoy](https://www.envoyproxy.io/) based ingress controller
   provided and supported by VMware.
 * Citrix provides an [Ingress Controller](https://github.com/citrix/citrix-k8s-ingress-controller) for its hardware (MPX), virtualized (VPX) and [free containerized (CPX) ADC](https://www.citrix.com/products/citrix-adc/cpx-express.html) for [baremetal](https://github.com/citrix/citrix-k8s-ingress-controller/tree/master/deployment/baremetal) and [cloud](https://github.com/citrix/citrix-k8s-ingress-controller/tree/master/deployment) deployments.
@@ -44,9 +46,9 @@ Kubernetes as a project currently supports and maintains [GCE](https://git.k8s.i
 * [NGINX, Inc.](https://www.nginx.com/) offers support and maintenance for the
   [NGINX Ingress Controller for Kubernetes](https://www.nginx.com/products/nginx/kubernetes-ingress-controller).
 * [Skipper](https://opensource.zalando.com/skipper/kubernetes/ingress-controller/) HTTP router and reverse proxy for service composition, including use cases like Kubernetes Ingress, designed as a library to build your custom proxy
-* [Traefik](https://github.com/containous/traefik) is a fully featured ingress controller
+* [Traefik](https://github.com/traefik/traefik) is a fully featured ingress controller
   ([Let's Encrypt](https://letsencrypt.org), secrets, http2, websocket), and it also comes with commercial
-  support by [Containous](https://containo.us/services).
+  support by [Traefik Labs](https://traefik.io).
 
 ## Using multiple Ingress controllers
 
@@ -72,4 +74,3 @@ Make sure you review your ingress controller's documentation to understand the c
 * Learn more about [Ingress](/docs/concepts/services-networking/ingress/).
 * [Set up Ingress on Minikube with the NGINX Controller](/docs/tasks/access-application-cluster/ingress-minikube).
 
-

