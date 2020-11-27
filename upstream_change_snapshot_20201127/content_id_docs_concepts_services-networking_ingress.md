diff --git a/content/en/docs/concepts/services-networking/ingress.md b/content/en/docs/concepts/services-networking/ingress.md
index 4b6d1f4ab..3977cbc23 100644
--- a/content/en/docs/concepts/services-networking/ingress.md
+++ b/content/en/docs/concepts/services-networking/ingress.md
@@ -7,7 +7,7 @@ weight: 40
 ---
 
 <!-- overview -->
-{{< feature-state for_k8s_version="v1.1" state="beta" >}}
+{{< feature-state for_k8s_version="v1.19" state="stable" >}}
 {{< glossary_definition term_id="ingress" length="all" >}}
 
 
@@ -25,19 +25,30 @@ For clarity, this guide defines the following terms:
 
 ## What is Ingress?
 
-[Ingress](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#ingress-v1beta1-networking-k8s-io) exposes HTTP and HTTPS routes from outside the cluster to
+[Ingress](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#ingress-v1-networking-k8s-io) exposes HTTP and HTTPS routes from outside the cluster to
 {{< link text="services" url="/docs/concepts/services-networking/service/" >}} within the cluster.
 Traffic routing is controlled by rules defined on the Ingress resource.
 
-```none
-    internet
-        |
-   [ Ingress ]
-   --|-----|--
-   [ Services ]
-```
-
-An Ingress may be configured to give Services externally-reachable URLs, load balance traffic, terminate SSL / TLS, and offer name based virtual hosting. An [Ingress controller](/docs/concepts/services-networking/ingress-controllers) is responsible for fulfilling the Ingress, usually with a load balancer, though it may also configure your edge router or additional frontends to help handle the traffic.
+Here is a simple example where an Ingress sends all its traffic to one Service:
+{{< mermaid >}}
+graph LR;
+  client([client])-. Ingress-managed <br> load balancer .->ingress[Ingress];
+  ingress-->|routing rule|service[Service];
+  subgraph cluster
+  ingress;
+  service-->pod1[Pod];
+  service-->pod2[Pod];
+  end
+  classDef plain fill:#ddd,stroke:#fff,stroke-width:4px,color:#000;
+  classDef k8s fill:#326ce5,stroke:#fff,stroke-width:4px,color:#fff;
+  classDef cluster fill:#fff,stroke:#bbb,stroke-width:2px,color:#326ce5;
+  class ingress,service,pod1,pod2 k8s;
+  class client plain;
+  class cluster cluster;
+{{</ mermaid >}}
+
+
+An Ingress may be configured to give Services externally-reachable URLs, load balance traffic, terminate SSL / TLS, and offer name-based virtual hosting. An [Ingress controller](/docs/concepts/services-networking/ingress-controllers) is responsible for fulfilling the Ingress, usually with a load balancer, though it may also configure your edge router or additional frontends to help handle the traffic.
 
 An Ingress does not expose arbitrary ports or protocols. Exposing services other than HTTP and HTTPS to the internet typically
 uses a service of type [Service.Type=NodePort](/docs/concepts/services-networking/service/#nodeport) or
@@ -45,7 +56,7 @@ uses a service of type [Service.Type=NodePort](/docs/concepts/services-networkin
 
 ## Prerequisites
 
-You must have an [ingress controller](/docs/concepts/services-networking/ingress-controllers) to satisfy an Ingress. Only creating an Ingress resource has no effect.
+You must have an [Ingress controller](/docs/concepts/services-networking/ingress-controllers) to satisfy an Ingress. Only creating an Ingress resource has no effect.
 
 You may need to deploy an Ingress controller such as [ingress-nginx](https://kubernetes.github.io/ingress-nginx/deploy/). You can choose from a number of
 [Ingress controllers](/docs/concepts/services-networking/ingress-controllers).
@@ -57,27 +68,11 @@ controllers operate slightly differently.
 Make sure you review your Ingress controller's documentation to understand the caveats of choosing it.
 {{< /note >}}
 
-## The Ingress Resource
+## The Ingress resource
 
 A minimal Ingress resource example:
 
-```yaml
-apiVersion: networking.k8s.io/v1beta1
-kind: Ingress
-metadata:
-  name: test-ingress
-  annotations:
-    nginx.ingress.kubernetes.io/rewrite-target: /
-spec:
-  rules:
-  - http:
-      paths:
-      - path: /testpath
-        pathType: Prefix
-        backend:
-          serviceName: test
-          servicePort: 80
-```
+{{< codenew file="service/networking/minimal-ingress.yaml" >}}
 
 As with all other Kubernetes resources, an Ingress needs `apiVersion`, `kind`, and `metadata` fields.
 The name of an Ingress object must be a valid
@@ -100,75 +95,134 @@ Each HTTP rule contains the following information:
 * An optional host. In this example, no host is specified, so the rule applies to all inbound
   HTTP traffic through the IP address specified. If a host is provided (for example,
   foo.bar.com), the rules apply to that host.
-* A list of paths (for example, `/testpath`), each of which has an associated backend defined with a `serviceName`
-  and `servicePort`. Both the host and path must match the content of an incoming request before the
-  load balancer directs traffic to the referenced Service.
+* A list of paths (for example, `/testpath`), each of which has an associated
+  backend defined with a `service.name` and a `service.port.name` or
+  `service.port.number`. Both the host and path must match the content of an
+  incoming request before the load balancer directs traffic to the referenced
+  Service.
 * A backend is a combination of Service and port names as described in the
-  [Service doc](/docs/concepts/services-networking/service/). HTTP (and HTTPS) requests to the
+  [Service doc](/docs/concepts/services-networking/service/) or a [custom resource backend](#resource-backend) by way of a {{< glossary_tooltip term_id="CustomResourceDefinition" text="CRD" >}}. HTTP (and HTTPS) requests to the
   Ingress that matches the host and path of the rule are sent to the listed backend.
 
-A default backend is often configured in an Ingress controller to service any requests that do not
+A `defaultBackend` is often configured in an Ingress controller to service any requests that do not
 match a path in the spec.
 
-### Default Backend
+### DefaultBackend {#default-backend}
 
-An Ingress with no rules sends all traffic to a single default backend. The default
-backend is typically a configuration option of the [Ingress controller](/docs/concepts/services-networking/ingress-controllers) and is not specified in your Ingress resources.
+An Ingress with no rules sends all traffic to a single default backend. The `defaultBackend` is conventionally a configuration option
+of the [Ingress controller](/docs/concepts/services-networking/ingress-controllers) and is not specified in your Ingress resources.
 
 If none of the hosts or paths match the HTTP request in the Ingress objects, the traffic is
 routed to your default backend.
 
-### Path Types
+### Resource backends {#resource-backend}
 
-Each path in an Ingress has a corresponding path type. There are three supported
-path types:
+A `Resource` backend is an ObjectRef to another Kubernetes resource within the
+same namespace as the Ingress object. A `Resource` is a mutually exclusive
+setting with Service, and will fail validation if both are specified. A common
+usage for a `Resource` backend is to ingress data to an object storage backend
+with static assets.
 
-* _`ImplementationSpecific`_ (default): With this path type, matching is up to
-  the IngressClass. Implementations can treat this as a separate `pathType` or
-  treat it identically to `Prefix` or `Exact` path types.
+{{< codenew file="service/networking/ingress-resource-backend.yaml" >}}
 
-* _`Exact`_: Matches the URL path exactly and with case sensitivity.
+After creating the Ingress above, you can view it with the following command:
+
+```bash
+kubectl describe ingress ingress-resource-backend
+```
 
-* _`Prefix`_: Matches based on a URL path prefix split by `/`. Matching is case
+```
+Name:             ingress-resource-backend
+Namespace:        default
+Address:
+Default backend:  APIGroup: k8s.example.com, Kind: StorageBucket, Name: static-assets
+Rules:
+  Host        Path  Backends
+  ----        ----  --------
+  *
+              /icons   APIGroup: k8s.example.com, Kind: StorageBucket, Name: icon-assets
+Annotations:  <none>
+Events:       <none>
+```
+
+### Path types
+
+Each path in an Ingress is required to have a corresponding path type. Paths
+that do not include an explicit `pathType` will fail validation. There are three
+supported path types:
+
+* `ImplementationSpecific`: With this path type, matching is up to the
+  IngressClass. Implementations can treat this as a separate `pathType` or treat
+  it identically to `Prefix` or `Exact` path types.
+
+* `Exact`: Matches the URL path exactly and with case sensitivity.
+
+* `Prefix`: Matches based on a URL path prefix split by `/`. Matching is case
   sensitive and done on a path element by element basis. A path element refers
   to the list of labels in the path split by the `/` separator. A request is a
   match for path _p_ if every _p_ is an element-wise prefix of _p_ of the
   request path.
-  
-  {{< note >}}
-  If the last element of the path is a substring of the last element in request path, it is not a match (for example: `/foo/bar` matches`/foo/bar/baz`, but does not match `/foo/barbaz`).
-  {{< /note >}}
 
-#### Multiple Matches
+  {{< note >}} If the last element of the path is a substring of the last
+  element in request path, it is not a match (for example: `/foo/bar`
+  matches`/foo/bar/baz`, but does not match `/foo/barbaz`). {{< /note >}}
+
+### Examples
+
+| Kind   | Path(s)                         | Request path(s)               | Matches?                           |
+|--------|---------------------------------|-------------------------------|------------------------------------|
+| Prefix | `/`                             | (all paths)                   | Yes                                |
+| Exact  | `/foo`                          | `/foo`                        | Yes                                |
+| Exact  | `/foo`                          | `/bar`                        | No                                 |
+| Exact  | `/foo`                          | `/foo/`                       | No                                 |
+| Exact  | `/foo/`                         | `/foo`                        | No                                 |
+| Prefix | `/foo`                          | `/foo`, `/foo/`               | Yes                                |
+| Prefix | `/foo/`                         | `/foo`, `/foo/`               | Yes                                |
+| Prefix | `/aaa/bb`                       | `/aaa/bbb`                    | No                                 |
+| Prefix | `/aaa/bbb`                      | `/aaa/bbb`                    | Yes                                |
+| Prefix | `/aaa/bbb/`                     | `/aaa/bbb`                    | Yes, ignores trailing slash        |
+| Prefix | `/aaa/bbb`                      | `/aaa/bbb/`                   | Yes,  matches trailing slash       |
+| Prefix | `/aaa/bbb`                      | `/aaa/bbb/ccc`                | Yes, matches subpath               |
+| Prefix | `/aaa/bbb`                      | `/aaa/bbbxyz`                 | No, does not match string prefix   |
+| Prefix | `/`, `/aaa`                     | `/aaa/ccc`                    | Yes, matches `/aaa` prefix         |
+| Prefix | `/`, `/aaa`, `/aaa/bbb`         | `/aaa/bbb`                    | Yes, matches `/aaa/bbb` prefix     |
+| Prefix | `/`, `/aaa`, `/aaa/bbb`         | `/ccc`                        | Yes, matches `/` prefix            |
+| Prefix | `/aaa`                          | `/ccc`                        | No, uses default backend           |
+| Mixed  | `/foo` (Prefix), `/foo` (Exact) | `/foo`                        | Yes, prefers Exact                 |
+
+#### Multiple matches
 In some cases, multiple paths within an Ingress will match a request. In those
 cases precedence will be given first to the longest matching path. If two paths
 are still equally matched, precedence will be given to paths with an exact path
 type over prefix path type.
 
-## Ingress Class
+## Hostname wildcards
+Hosts can be precise matches (for example “`foo.bar.com`”) or a wildcard (for
+example “`*.foo.com`”). Precise matches require that the HTTP `host` header
+matches the `host` field. Wildcard matches require the HTTP `host` header is
+equal to the suffix of the wildcard rule.
+
+| Host        | Host header       | Match?                                            |
+| ----------- |-------------------| --------------------------------------------------|
+| `*.foo.com` | `bar.foo.com`     | Matches based on shared suffix                    |
+| `*.foo.com` | `baz.bar.foo.com` | No match, wildcard only covers a single DNS label |
+| `*.foo.com` | `foo.com`         | No match, wildcard only covers a single DNS label |
+
+{{< codenew file="service/networking/ingress-wildcard-host.yaml" >}}
+
+## Ingress class
 
 Ingresses can be implemented by different controllers, often with different
 configuration. Each Ingress should specify a class, a reference to an
 IngressClass resource that contains additional configuration including the name
 of the controller that should implement the class.
 
-```yaml
-apiVersion: networking.k8s.io/v1beta1
-kind: IngressClass
-metadata:
-  name: external-lb
-spec:
-  controller: example.com/ingress-controller
-  parameters:
-    apiGroup: k8s.example.com/v1alpha
-    kind: IngressParameters
-    name: external-lb
-```
+{{< codenew file="service/networking/external-lb.yaml" >}}
 
 IngressClass resources contain an optional parameters field. This can be used to
 reference additional configuration for this class.
 
-### Deprecated Annotation
+### Deprecated annotation
 
 Before the IngressClass resource and `ingressClassName` field were added in
 Kubernetes 1.18, Ingress classes were specified with a
@@ -181,7 +235,7 @@ used to reference the name of the Ingress controller that should implement the
 Ingress, the field is a reference to an IngressClass resource that contains
 additional Ingress configuration, including the name of the Ingress controller.
 
-### Default Ingress Class
+### Default IngressClass {#default-ingress-class}
 
 You can mark a particular IngressClass as default for your cluster. Setting the
 `ingressclass.kubernetes.io/is-default-class` annotation to `true` on an
@@ -192,29 +246,29 @@ IngressClass resource will ensure that new Ingresses without an
 If you have more than one IngressClass marked as the default for your cluster,
 the admission controller prevents creating new Ingress objects that don't have
 an `ingressClassName` specified. You can resolve this by ensuring that at most 1
-IngressClasess are marked as default in your cluster.
+IngressClass is marked as default in your cluster.
 {{< /caution >}}
 
 ## Types of Ingress
 
-### Single Service Ingress
+### Ingress backed by a single Service {#single-service-ingress}
 
 There are existing Kubernetes concepts that allow you to expose a single Service
 (see [alternatives](#alternatives)). You can also do this with an Ingress by specifying a
 *default backend* with no rules.
 
-{{< codenew file="service/networking/ingress.yaml" >}}
+{{< codenew file="service/networking/test-ingress.yaml" >}}
 
 If you create it using `kubectl apply -f` you should be able to view the state
 of the Ingress you just added:
 
-```shell
+```bash
 kubectl get ingress test-ingress
 ```
 
 ```
-NAME           HOSTS     ADDRESS           PORTS     AGE
-test-ingress   *         203.0.113.123   80        59s
+NAME           CLASS         HOSTS   ADDRESS         PORTS   AGE
+test-ingress   external-lb   *       203.0.113.123   80      59s
 ```
 
 Where `203.0.113.123` is the IP allocated by the Ingress controller to satisfy
@@ -231,34 +285,29 @@ A fanout configuration routes traffic from a single IP address to more than one
 based on the HTTP URI being requested. An Ingress allows you to keep the number of load balancers
 down to a minimum. For example, a setup like:
 
-```none
-foo.bar.com -> 178.91.123.132 -> / foo    service1:4200
-                                 / bar    service2:8080
-```
+{{< mermaid >}}
+graph LR;
+  client([client])-. Ingress-managed <br> load balancer .->ingress[Ingress, 178.91.123.132];
+  ingress-->|/foo|service1[Service service1:4200];
+  ingress-->|/bar|service2[Service service2:8080];
+  subgraph cluster
+  ingress;
+  service1-->pod1[Pod];
+  service1-->pod2[Pod];
+  service2-->pod3[Pod];
+  service2-->pod4[Pod];
+  end
+  classDef plain fill:#ddd,stroke:#fff,stroke-width:4px,color:#000;
+  classDef k8s fill:#326ce5,stroke:#fff,stroke-width:4px,color:#fff;
+  classDef cluster fill:#fff,stroke:#bbb,stroke-width:2px,color:#326ce5;
+  class ingress,service1,service2,pod1,pod2,pod3,pod4 k8s;
+  class client plain;
+  class cluster cluster;
+{{</ mermaid >}}
 
 would require an Ingress such as:
 
-```yaml
-apiVersion: networking.k8s.io/v1beta1
-kind: Ingress
-metadata:
-  name: simple-fanout-example
-  annotations:
-    nginx.ingress.kubernetes.io/rewrite-target: /
-spec:
-  rules:
-  - host: foo.bar.com
-    http:
-      paths:
-      - path: /foo
-        backend:
-          serviceName: service1
-          servicePort: 4200
-      - path: /bar
-        backend:
-          serviceName: service2
-          servicePort: 8080
-```
+{{< codenew file="service/networking/simple-fanout-example.yaml" >}}
 
 When you create the Ingress with `kubectl apply -f`:
 
@@ -277,8 +326,6 @@ Rules:
   foo.bar.com
                /foo   service1:4200 (10.8.0.90:4200)
                /bar   service2:8080 (10.8.0.91:8080)
-Annotations:
-  nginx.ingress.kubernetes.io/rewrite-target:  /
 Events:
   Type     Reason  Age                From                     Message
   ----     ------  ----               ----                     -------
@@ -291,7 +338,7 @@ When it has done so, you can see the address of the load balancer at the
 Address field.
 
 {{< note >}}
-Depending on the [Ingress controller](/docs/concepts/services-networking/ingress-controllers)
+Depending on the [Ingress controller](/docs/concepts/services-networking/ingress-controllers/)
 you are using, you may need to create a default-http-backend
 [Service](/docs/concepts/services-networking/service/).
 {{< /note >}}
@@ -300,77 +347,50 @@ you are using, you may need to create a default-http-backend
 
 Name-based virtual hosts support routing HTTP traffic to multiple host names at the same IP address.
 
-```none
-foo.bar.com --|                 |-> foo.bar.com service1:80
-              | 178.91.123.132  |
-bar.foo.com --|                 |-> bar.foo.com service2:80
-```
+{{< mermaid >}}
+graph LR;
+  client([client])-. Ingress-managed <br> load balancer .->ingress[Ingress, 178.91.123.132];
+  ingress-->|Host: foo.bar.com|service1[Service service1:80];
+  ingress-->|Host: bar.foo.com|service2[Service service2:80];
+  subgraph cluster
+  ingress;
+  service1-->pod1[Pod];
+  service1-->pod2[Pod];
+  service2-->pod3[Pod];
+  service2-->pod4[Pod];
+  end
+  classDef plain fill:#ddd,stroke:#fff,stroke-width:4px,color:#000;
+  classDef k8s fill:#326ce5,stroke:#fff,stroke-width:4px,color:#fff;
+  classDef cluster fill:#fff,stroke:#bbb,stroke-width:2px,color:#326ce5;
+  class ingress,service1,service2,pod1,pod2,pod3,pod4 k8s;
+  class client plain;
+  class cluster cluster;
+{{</ mermaid >}}
+
 
 The following Ingress tells the backing load balancer to route requests based on
 the [Host header](https://tools.ietf.org/html/rfc7230#section-5.4).
 
-```yaml
-apiVersion: networking.k8s.io/v1beta1
-kind: Ingress
-metadata:
-  name: name-virtual-host-ingress
-spec:
-  rules:
-  - host: foo.bar.com
-    http:
-      paths:
-      - backend:
-          serviceName: service1
-          servicePort: 80
-  - host: bar.foo.com
-    http:
-      paths:
-      - backend:
-          serviceName: service2
-          servicePort: 80
-```
+{{< codenew file="service/networking/name-virtual-host-ingress.yaml" >}}
 
 If you create an Ingress resource without any hosts defined in the rules, then any
 web traffic to the IP address of your Ingress controller can be matched without a name based
 virtual host being required.
 
-For example, the following Ingress resource will route traffic
+For example, the following Ingress routes traffic
 requested for `first.bar.com` to `service1`, `second.foo.com` to `service2`, and any traffic
 to the IP address without a hostname defined in request (that is, without a request header being
 presented) to `service3`.
 
-```yaml
-apiVersion: networking.k8s.io/v1beta1
-kind: Ingress
-metadata:
-  name: name-virtual-host-ingress
-spec:
-  rules:
-  - host: first.bar.com
-    http:
-      paths:
-      - backend:
-          serviceName: service1
-          servicePort: 80
-  - host: second.foo.com
-    http:
-      paths:
-      - backend:
-          serviceName: service2
-          servicePort: 80
-  - http:
-      paths:
-      - backend:
-          serviceName: service3
-          servicePort: 80
-```
+{{< codenew file="service/networking/name-virtual-host-ingress-no-third-host.yaml" >}}
 
 ### TLS
 
 You can secure an Ingress by specifying a {{< glossary_tooltip term_id="secret" >}}
-that contains a TLS private key and certificate. Currently the Ingress only
-supports a single TLS port, 443, and assumes TLS termination. If the TLS
-configuration section in an Ingress specifies different hosts, they are
+that contains a TLS private key and certificate. The Ingress resource only
+supports a single TLS port, 443, and assumes TLS termination at the ingress point
+(traffic to the Service and its Pods is in plaintext).
+If the TLS configuration section in an Ingress specifies different hosts, they are
 multiplexed on the same port according to the hostname specified through the
 SNI TLS extension (provided the Ingress controller supports SNI). The TLS secret
 must contain keys named `tls.crt` and `tls.key` that contain the certificate
@@ -391,27 +411,16 @@ type: kubernetes.io/tls
 Referencing this secret in an Ingress tells the Ingress controller to
 secure the channel from the client to the load balancer using TLS. You need to make
 sure the TLS secret you created came from a certificate that contains a Common
-Name (CN), also known as a Fully Qualified Domain Name (FQDN) for `sslexample.foo.com`.
+Name (CN), also known as a Fully Qualified Domain Name (FQDN) for `https-example.foo.com`.
 
-```yaml
-apiVersion: networking.k8s.io/v1beta1
-kind: Ingress
-metadata:
-  name: tls-example-ingress
-spec:
-  tls:
-  - hosts:
-      - sslexample.foo.com
-    secretName: testsecret-tls
-  rules:
-  - host: sslexample.foo.com
-    http:
-      paths:
-      - path: /
-        backend:
-          serviceName: service1
-          servicePort: 80
-```
+{{< note >}}
+Keep in mind that TLS will not work on the default rule because the
+certificates would have to be issued for all the possible sub-domains. Therefore,
+`hosts` in the `tls` section need to explicitly match the `host` in the `rules`
+section.
+{{< /note >}}
+
+{{< codenew file="service/networking/tls-example-ingress.yaml" >}}
 
 {{< note >}}
 There is a gap between TLS features supported by various Ingress
@@ -421,7 +430,7 @@ controllers. Please refer to documentation on
 platform specific Ingress controller to understand how TLS works in your environment.
 {{< /note >}}
 
-### Loadbalancing
+### Load balancing {#load-balancing}
 
 An Ingress controller is bootstrapped with some load balancing policy settings
 that it applies to all Ingress, such as the load balancing algorithm, backend
@@ -432,10 +441,10 @@ a Service.
 
 It's also worth noting that even though health checks are not exposed directly
 through the Ingress, there exist parallel concepts in Kubernetes such as
-[readiness probes](/docs/tasks/configure-pod-container/configure-liveness-readiness-probes/)
+[readiness probes](/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/)
 that allow you to achieve the same end result. Please review the controller
-specific documentation to see how they handle health checks (
-[nginx](https://git.k8s.io/ingress-nginx/README.md),
+specific documentation to see how they handle health checks (for example:
+[nginx](https://git.k8s.io/ingress-nginx/README.md), or
 [GCE](https://git.k8s.io/ingress-gce/README.md#health-checks)).
 
 ## Updating an Ingress
@@ -478,16 +487,22 @@ spec:
     http:
       paths:
       - backend:
-          serviceName: service1
-          servicePort: 80
+          service:
+            name: service1
+            port:
+              number: 80
         path: /foo
+        pathType: Prefix
   - host: bar.baz.com
     http:
       paths:
       - backend:
-          serviceName: service2
-          servicePort: 80
+          service:
+            name: service2
+            port:
+              number: 80
         path: /foo
+        pathType: Prefix
 ..
 ```
 
@@ -524,16 +539,8 @@ You can achieve the same outcome by invoking `kubectl replace -f` on a modified
 
 ## Failing across availability zones
 
-Techniques for spreading traffic across failure domains differs between cloud providers.
-Please check the documentation of the relevant [Ingress controller](/docs/concepts/services-networking/ingress-controllers) for details. You can also refer to the [federation documentation](https://github.com/kubernetes-sigs/federation-v2)
-for details on deploying Ingress in a federated cluster.
-
-## Future Work
-
-Track [SIG Network](https://github.com/kubernetes/community/tree/master/sig-network)
-for more details on the evolution of Ingress and related resources. You may also track the
-[Ingress repository](https://github.com/kubernetes/ingress/tree/master) for more details on the
-evolution of various Ingress controllers.
+Techniques for spreading traffic across failure domains differ between cloud providers.
+Please check the documentation of the relevant [Ingress controller](/docs/concepts/services-networking/ingress-controllers) for details.
 
 ## Alternatives
 
@@ -547,6 +554,5 @@ You can expose a Service in multiple ways that don't directly involve the Ingres
 ## {{% heading "whatsnext" %}}
 
 * Learn about the [Ingress API](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#ingress-v1beta1-networking-k8s-io)
-* Learn about [Ingress Controllers](/docs/concepts/services-networking/ingress-controllers/)
-* [Set up Ingress on Minikube with the NGINX Controller](/docs/tasks/access-application-cluster/ingress-minikube)
-
+* Learn about [Ingress controllers](/docs/concepts/services-networking/ingress-controllers/)
+* [Set up Ingress on Minikube with the NGINX Controller](/docs/tasks/access-application-cluster/ingress-minikube/)

