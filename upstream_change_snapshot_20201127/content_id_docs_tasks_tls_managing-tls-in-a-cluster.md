diff --git a/content/en/docs/tasks/tls/managing-tls-in-a-cluster.md b/content/en/docs/tasks/tls/managing-tls-in-a-cluster.md
index 5098d353d..62e5cfc9c 100644
--- a/content/en/docs/tasks/tls/managing-tls-in-a-cluster.md
+++ b/content/en/docs/tasks/tls/managing-tls-in-a-cluster.md
@@ -76,11 +76,16 @@ cat <<EOF | cfssl genkey - | cfssljson -bare server
     "192.0.2.24",
     "10.0.34.2"
   ],
-  "CN": "my-pod.my-namespace.pod.cluster.local",
+  "CN": "system:node:my-pod.my-namespace.pod.cluster.local",
   "key": {
     "algo": "ecdsa",
     "size": 256
-  }
+  },
+  "names": [
+    {
+      "O": "system:nodes"
+    }
+  ]
 }
 EOF
 ```
@@ -109,12 +114,13 @@ command:
 
 ```shell
 cat <<EOF | kubectl apply -f -
-apiVersion: certificates.k8s.io/v1beta1
+apiVersion: certificates.k8s.io/v1
 kind: CertificateSigningRequest
 metadata:
   name: my-svc.my-namespace
 spec:
   request: $(cat server.csr | base64 | tr -d '\n')
+  signerName: kubernetes.io/kubelet-serving
   usages:
   - digital signature
   - key encipherment
@@ -125,10 +131,10 @@ EOF
 Notice that the `server.csr` file created in step 1 is base64 encoded
 and stashed in the `.spec.request` field. We are also requesting a
 certificate with the "digital signature", "key encipherment", and "server
-auth" key usages. We support all key usages and extended key usages listed
-[here](https://godoc.org/k8s.io/api/certificates/v1beta1#KeyUsage)
-so you can request client certificates and other certificates using this
-same API.
+auth" key usages, signed by the `kubernetes.io/kubelet-serving` signer.
+A specific `signerName` must be requested.
+View documentation for [supported signer names](/docs/reference/access-authn-authz/certificate-signing-requests/#signers)
+for more information.
 
 The CSR should now be visible from the API in a Pending state. You can see
 it by running:

