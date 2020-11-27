diff --git a/content/en/docs/concepts/cluster-administration/networking.md b/content/en/docs/concepts/cluster-administration/networking.md
index 29044be25..184b40c8d 100644
--- a/content/en/docs/concepts/cluster-administration/networking.md
+++ b/content/en/docs/concepts/cluster-administration/networking.md
@@ -12,14 +12,11 @@ understand exactly how it is expected to work.  There are 4 distinct networking
 problems to address:
 
 1. Highly-coupled container-to-container communications: this is solved by
-   [pods](/docs/concepts/workloads/pods/pod/) and `localhost` communications.
+   {{< glossary_tooltip text="Pods" term_id="pod" >}} and `localhost` communications.
 2. Pod-to-Pod communications: this is the primary focus of this document.
 3. Pod-to-Service communications: this is covered by [services](/docs/concepts/services-networking/service/).
 4. External-to-Service communications: this is covered by [services](/docs/concepts/services-networking/service/).
 
-
-
-
 <!-- body -->
 
 Kubernetes is all about sharing machines between applications.  Typically,
@@ -82,6 +79,8 @@ as an introduction to various technologies and serves as a jumping-off point.
 The following networking options are sorted alphabetically - the order does not
 imply any preferential status.
 
+{{% thirdparty-content %}}
+
 ### ACI
 
 [Cisco Application Centric Infrastructure](https://www.cisco.com/c/en/us/solutions/data-center-virtualization/application-centric-infrastructure/index.html) offers an integrated overlay and underlay SDN solution that supports containers, virtual machines, and bare metal servers. [ACI](https://www.github.com/noironetworks/aci-containers) provides container networking integration for ACI. An overview of the integration is provided [here](https://www.cisco.com/c/dam/en/us/solutions/collateral/data-center-virtualization/application-centric-infrastructure/solution-overview-c22-739493.pdf).
@@ -93,7 +92,7 @@ Thanks to the "programmable" characteristic of Open vSwitch, Antrea is able to i
 
 ### AOS from Apstra
 
-[AOS](http://www.apstra.com/products/aos/) is an Intent-Based Networking system that creates and manages complex datacenter environments from a simple integrated platform.  AOS leverages a highly scalable distributed design to eliminate network outages while minimizing costs.
+[AOS](https://www.apstra.com/products/aos/) is an Intent-Based Networking system that creates and manages complex datacenter environments from a simple integrated platform.  AOS leverages a highly scalable distributed design to eliminate network outages while minimizing costs.
 
 The AOS Reference Design currently supports Layer-3 connected hosts that eliminate legacy Layer-2 switching problems.  These Layer-3 hosts can be Linux servers (Debian, Ubuntu, CentOS) that create BGP neighbor relationships directly with the top of rack switches (TORs).  AOS automates the routing adjacencies and then provides fine grained control over the route health injections (RHI) that are common in a Kubernetes deployment.
 
@@ -101,7 +100,7 @@ AOS has a rich set of REST API endpoints that enable Kubernetes to quickly chang
 
 AOS supports the use of common vendor equipment from manufacturers including Cisco, Arista, Dell, Mellanox, HPE, and a large number of white-box systems and open network operating systems like Microsoft SONiC, Dell OPX, and Cumulus Linux.
 
-Details on how the AOS system works can be accessed here: http://www.apstra.com/products/how-it-works/
+Details on how the AOS system works can be accessed here: https://www.apstra.com/products/how-it-works/
 
 ### AWS VPC CNI for Kubernetes
 
@@ -115,7 +114,7 @@ Additionally, the CNI can be run alongside [Calico for network policy enforcemen
 [Azure CNI](https://docs.microsoft.com/en-us/azure/virtual-network/container-networking-overview) is an [open source](https://github.com/Azure/azure-container-networking/blob/master/docs/cni.md) plugin that integrates Kubernetes Pods with an Azure Virtual Network (also known as VNet) providing network performance at par with VMs. Pods can connect to peered VNet and to on-premises over Express Route or site-to-site VPN and are also directly reachable from these networks. Pods can access Azure services, such as storage and SQL, that are protected by Service Endpoints or Private Link. You can use VNet security policies and routing to filter Pod traffic. The plugin assigns VNet IPs to Pods by utilizing a pool of secondary IPs pre-configured on the Network Interface of a Kubernetes node.
 
 Azure CNI is available natively in the [Azure Kubernetes Service (AKS)] (https://docs.microsoft.com/en-us/azure/aks/configure-azure-cni).
- 
+
 
 ### Big Cloud Fabric from Big Switch Networks
 
@@ -123,7 +122,11 @@ Azure CNI is available natively in the [Azure Kubernetes Service (AKS)] (https:/
 
 With the help of the Big Cloud Fabric's virtual pod multi-tenant architecture, container orchestration systems such as Kubernetes, RedHat OpenShift, Mesosphere DC/OS & Docker Swarm will be natively integrated alongside with VM orchestration systems such as VMware, OpenStack & Nutanix. Customers will be able to securely inter-connect any number of these clusters and enable inter-tenant communication between them if needed.
 
-BCF was recognized by Gartner as a visionary in the latest [Magic Quadrant](http://go.bigswitch.com/17GatedDocuments-MagicQuadrantforDataCenterNetworking_Reg.html). One of the BCF Kubernetes on-premises deployments (which includes Kubernetes, DC/OS & VMware running on multiple DCs across different geographic regions) is also referenced [here](https://portworx.com/architects-corner-kubernetes-satya-komala-nio/).
+BCF was recognized by Gartner as a visionary in the latest [Magic Quadrant](https://go.bigswitch.com/17GatedDocuments-MagicQuadrantforDataCenterNetworking_Reg.html). One of the BCF Kubernetes on-premises deployments (which includes Kubernetes, DC/OS & VMware running on multiple DCs across different geographic regions) is also referenced [here](https://portworx.com/architects-corner-kubernetes-satya-komala-nio/).
+
+### Calico
+
+[Calico](https://docs.projectcalico.org/) is an open source networking and network security solution for containers, virtual machines, and native host-based workloads. Calico supports multiple data planes including: a pure Linux eBPF dataplane, a standard Linux networking dataplane, and a Windows HNS dataplane. Calico provides a full networking stack but can also be used in conjunction with [cloud provider CNIs](https://docs.projectcalico.org/networking/determine-best-networking#calico-compatible-cni-plugins-and-cloud-provider-integrations) to provide network policy enforcement.
 
 ### Cilium
 
@@ -135,7 +138,7 @@ addressing, and it can be used in combination with other CNI plugins.
 
 ### CNI-Genie from Huawei
 
-[CNI-Genie](https://github.com/Huawei-PaaS/CNI-Genie) is a CNI plugin that enables Kubernetes to [simultaneously have access to different implementations](https://github.com/Huawei-PaaS/CNI-Genie/blob/master/docs/multiple-cni-plugins/README.md#what-cni-genie-feature-1-multiple-cni-plugins-enables) of the [Kubernetes network model](https://github.com/kubernetes/website/blob/master/content/en/docs/concepts/cluster-administration/networking.md#the-kubernetes-network-model) in runtime. This includes any implementation that runs as a [CNI plugin](https://github.com/containernetworking/cni#3rd-party-plugins), such as [Flannel](https://github.com/coreos/flannel#flannel), [Calico](http://docs.projectcalico.org/), [Romana](http://romana.io), [Weave-net](https://www.weave.works/products/weave-net/).
+[CNI-Genie](https://github.com/Huawei-PaaS/CNI-Genie) is a CNI plugin that enables Kubernetes to [simultaneously have access to different implementations](https://github.com/Huawei-PaaS/CNI-Genie/blob/master/docs/multiple-cni-plugins/README.md#what-cni-genie-feature-1-multiple-cni-plugins-enables) of the [Kubernetes network model](/docs/concepts/cluster-administration/networking/#the-kubernetes-network-model) in runtime. This includes any implementation that runs as a [CNI plugin](https://github.com/containernetworking/cni#3rd-party-plugins), such as [Flannel](https://github.com/coreos/flannel#flannel), [Calico](https://docs.projectcalico.org/), [Romana](https://romana.io), [Weave-net](https://www.weave.works/products/weave-net/).
 
 CNI-Genie also supports [assigning multiple IP addresses to a pod](https://github.com/Huawei-PaaS/CNI-Genie/blob/master/docs/multiple-ips/README.md#feature-2-extension-cni-genie-multiple-ip-addresses-per-pod), each from a different CNI plugin.
 
@@ -155,13 +158,18 @@ tables to provide per-instance subnets to each host (which is limited to 50-100
 entries per VPC). In short, cni-ipvlan-vpc-k8s significantly reduces the
 network complexity required to deploy Kubernetes at scale within AWS.
 
+### Coil
+
+[Coil](https://github.com/cybozu-go/coil) is a CNI plugin designed for ease of integration, providing flexible egress networking.
+Coil operates with a low overhead compared to bare metal, and allows you to define arbitrary egress NAT gateways for external networks.
+
 ### Contiv
 
-[Contiv](https://github.com/contiv/netplugin) provides configurable networking (native l3 using BGP, overlay using vxlan,  classic l2, or Cisco-SDN/ACI) for various use cases. [Contiv](http://contiv.io) is all open sourced.
+[Contiv](https://github.com/contiv/netplugin) provides configurable networking (native l3 using BGP, overlay using vxlan,  classic l2, or Cisco-SDN/ACI) for various use cases. [Contiv](https://contiv.io) is all open sourced.
 
 ### Contrail / Tungsten Fabric
 
-[Contrail](http://www.juniper.net/us/en/products-services/sdn/contrail/contrail-networking/), based on [Tungsten Fabric](https://tungsten.io), is a truly open, multi-cloud network virtualization and policy management platform. Contrail and Tungsten Fabric are integrated with various orchestration systems such as Kubernetes, OpenShift, OpenStack and Mesos, and provide different isolation modes for virtual machines, containers/pods and bare metal workloads.
+[Contrail](https://www.juniper.net/us/en/products-services/sdn/contrail/contrail-networking/), based on [Tungsten Fabric](https://tungsten.io), is a truly open, multi-cloud network virtualization and policy management platform. Contrail and Tungsten Fabric are integrated with various orchestration systems such as Kubernetes, OpenShift, OpenStack and Mesos, and provide different isolation modes for virtual machines, containers/pods and bare metal workloads.
 
 ### DANM
 
@@ -242,7 +250,7 @@ traffic to the internet.
 
 ### Kube-router
 
-[Kube-router](https://github.com/cloudnativelabs/kube-router) is a purpose-built networking solution for Kubernetes that aims to provide high performance and operational simplicity. Kube-router provides a Linux [LVS/IPVS](http://www.linuxvirtualserver.org/software/ipvs.html)-based service proxy, a Linux kernel forwarding-based pod-to-pod networking solution with no overlays, and iptables/ipset-based network policy enforcer.
+[Kube-router](https://github.com/cloudnativelabs/kube-router) is a purpose-built networking solution for Kubernetes that aims to provide high performance and operational simplicity. Kube-router provides a Linux [LVS/IPVS](https://www.linuxvirtualserver.org/software/ipvs.html)-based service proxy, a Linux kernel forwarding-based pod-to-pod networking solution with no overlays, and iptables/ipset-based network policy enforcer.
 
 ### L2 networks and linux bridging
 
@@ -252,8 +260,8 @@ Note that these instructions have only been tried very casually - it seems to
 work, but has not been thoroughly tested.  If you use this technique and
 perfect the process, please let us know.
 
-Follow the "With Linux Bridge devices" section of [this very nice
-tutorial](http://blog.oddbit.com/2014/08/11/four-ways-to-connect-a-docker/) from
+Follow the "With Linux Bridge devices" section of
+[this very nice tutorial](https://blog.oddbit.com/2014/08/11/four-ways-to-connect-a-docker/) from
 Lars Kellogg-Stedman.
 
 ### Multus (a Multi Network plugin)
@@ -274,7 +282,7 @@ Multus supports all [reference plugins](https://github.com/containernetworking/p
 
 ### Nuage Networks VCS (Virtualized Cloud Services)
 
-[Nuage](http://www.nuagenetworks.net) provides a highly scalable policy-based Software-Defined Networking (SDN) platform. Nuage uses the open source Open vSwitch for the data plane along with a feature rich SDN Controller built on open standards.
+[Nuage](https://www.nuagenetworks.net) provides a highly scalable policy-based Software-Defined Networking (SDN) platform. Nuage uses the open source Open vSwitch for the data plane along with a feature rich SDN Controller built on open standards.
 
 The Nuage platform uses overlays to provide seamless policy-based networking between Kubernetes Pods and non-Kubernetes environments (VMs and bare metal servers). Nuage's policy abstraction model is designed with applications in mind and makes it easy to declare fine-grained policies for applications.The platform's real-time analytics engine enables visibility and security monitoring for Kubernetes applications.
 
@@ -292,17 +300,9 @@ stateful ACLs, load-balancers etc to build different virtual networking
 topologies.  The project has a specific Kubernetes plugin and documentation
 at [ovn-kubernetes](https://github.com/openvswitch/ovn-kubernetes).
 
-### Project Calico
-
-[Project Calico](http://docs.projectcalico.org/) is an open source container networking provider and network policy engine.
-
-Calico provides a highly scalable networking and network policy solution for connecting Kubernetes pods based on the same IP networking principles as the internet, for both Linux (open source) and Windows (proprietary - available from [Tigera](https://www.tigera.io/essentials/)).  Calico can be deployed without encapsulation or overlays to provide high-performance, high-scale data center networking.  Calico also provides fine-grained, intent based network security policy for Kubernetes pods via its distributed firewall.
-
-Calico can also be run in policy enforcement mode in conjunction with other networking solutions such as Flannel, aka [canal](https://github.com/tigera/canal), or native GCE, AWS or Azure networking.
-
 ### Romana
 
-[Romana](http://romana.io) is an open source network and security automation solution that lets you deploy Kubernetes without an overlay network. Romana supports Kubernetes [Network Policy](/docs/concepts/services-networking/network-policies/) to provide isolation across network namespaces.
+[Romana](https://romana.io) is an open source network and security automation solution that lets you deploy Kubernetes without an overlay network. Romana supports Kubernetes [Network Policy](/docs/concepts/services-networking/network-policies/) to provide isolation across network namespaces.
 
 ### Weave Net from Weaveworks
 
@@ -312,13 +312,8 @@ Weave Net runs as a [CNI plug-in](https://www.weave.works/docs/net/latest/cni-pl
 or stand-alone.  In either version, it doesn't require any configuration or extra code
 to run, and in both cases, the network provides one IP address per pod - as is standard for Kubernetes.
 
-
-
 ## {{% heading "whatsnext" %}}
 
-
 The early design of the networking model and its rationale, and some future
-plans are described in more detail in the [networking design
-document](https://git.k8s.io/community/contributors/design-proposals/network/networking.md).
-
-
+plans are described in more detail in the
+[networking design document](https://git.k8s.io/community/contributors/design-proposals/network/networking.md).

