diff --git a/content/en/docs/concepts/architecture/control-plane-node-communication.md b/content/en/docs/concepts/architecture/control-plane-node-communication.md
index 925f14d17..2e7235a89 100644
--- a/content/en/docs/concepts/architecture/control-plane-node-communication.md
+++ b/content/en/docs/concepts/architecture/control-plane-node-communication.md
@@ -21,7 +21,7 @@ This document catalogs the communication paths between the control plane (really
 Kubernetes has a "hub-and-spoke" API pattern. All API usage from nodes (or the pods they run) terminate at the apiserver (none of the other control plane components are designed to expose remote services). The apiserver is configured to listen for remote connections on a secure HTTPS port (typically 443) with one or more forms of client [authentication](/docs/reference/access-authn-authz/authentication/) enabled.
 One or more forms of [authorization](/docs/reference/access-authn-authz/authorization/) should be enabled, especially if [anonymous requests](/docs/reference/access-authn-authz/authentication/#anonymous-requests) or [service account tokens](/docs/reference/access-authn-authz/authentication/#service-account-tokens) are allowed.
 
-Nodes should be provisioned with the public root certificate for the cluster such that they can connect securely to the apiserver along with valid client credentials. For example, on a default GKE deployment, the client credentials provided to the kubelet are in the form of a client certificate. See [kubelet TLS bootstrapping](/docs/reference/command-line-tools-reference/kubelet-tls-bootstrapping/) for automated provisioning of kubelet client certificates.
+Nodes should be provisioned with the public root certificate for the cluster such that they can connect securely to the apiserver along with valid client credentials. A good approach is that the client credentials provided to the kubelet are in the form of a client certificate. See [kubelet TLS bootstrapping](/docs/reference/command-line-tools-reference/kubelet-tls-bootstrapping/) for automated provisioning of kubelet client certificates.
 
 Pods that wish to connect to the apiserver can do so securely by leveraging a service account so that Kubernetes will automatically inject the public root certificate and a valid bearer token into the pod when it is instantiated.
 The `kubernetes` service (in all namespaces) is configured with a virtual IP address that is redirected (via kube-proxy) to the HTTPS endpoint on the apiserver.
@@ -46,10 +46,10 @@ These connections terminate at the kubelet's HTTPS endpoint. By default, the api
 
 To verify this connection, use the `--kubelet-certificate-authority` flag to provide the apiserver with a root certificate bundle to use to verify the kubelet's serving certificate.
 
-If that is not possible, use [SSH tunneling](/docs/concepts/architecture/master-node-communication/#ssh-tunnels) between the apiserver and kubelet if required to avoid connecting over an
+If that is not possible, use [SSH tunneling](#ssh-tunnels) between the apiserver and kubelet if required to avoid connecting over an
 untrusted or public network.
 
-Finally, [Kubelet authentication and/or authorization](/docs/admin/kubelet-authentication-authorization/) should be enabled to secure the kubelet API.
+Finally, [Kubelet authentication and/or authorization](/docs/reference/command-line-tools-reference/kubelet-authentication-authorization/) should be enabled to secure the kubelet API.
 
 ### apiserver to nodes, pods, and services
 

