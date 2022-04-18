## Ingress

### 一、概述

通常情况下，Service 和 Pod 的 IP 仅可在集群内部访问。集群外部的请求需要通过负载均衡转发到 Service 在 Node 上暴露的 NodePort 上，然后再由 kube-proxy 通过边缘路由器 (edge router) 将其转发给相关的 Pod 或者丢弃。K8s的Pod和Service需要通过NodePort或者loadBlance把服务暴露到外， 但是随着微服务的增多。管理会变得越来越麻烦，比如端口分配、日志采集等。能不能对所有的服务进行统一转发、管理呢？通过Ingress便可以完成。它有以下功能：

- 基于http-header 的路由
- 基于 path 的路由
- 单个ingress 的 timeout
- 请求速率limit
- rewrite 规则

工作原理图：

![Nginx Ingress工作原理](..\..\images\041\8-200910161P9135.gif)

![clipboard.png](..\..\images\041\ingress-2.jpg)

### 二、组成原理

Nginx Ingress 由资源对象 Ingress、Ingress 控制器、Nginx 三部分组成，Ingress 控制器用以将 Ingress 资源实例组装成 Nginx 配置文件（nginx.conf），并重新加载 Nginx 使变更的配置生效。当它监听到 Service 中 Pod 变化时通过动态变更的方式实现 Nginx 上游服务器组配置的变更，无须重新加载 Nginx 进程。工作原理如下图所示。

- Ingress，一组基于域名或 URL 把请求转发到指定 Service 实例的访问规则，是 Kubernetes 的一种资源对象，Ingress 实例被存储在对象存储服务 etcd 中，通过接口服务被实现增、删、改、查的操作。
- Ingress 控制器（Ingress controller），用以实时监控资源对象 Ingress、Service、End-point、Secret（主要是 TLS 证书和 Key）、Node、ConfigMap 的变化，自动对 Nginx 进行相应的操作。
- Nginx，实现具体的应用层负载均衡及访问控制。



参数文献：

- https://kubernetes.io/zh/docs/concepts/services-networking/ingress/
- https://kubernetes.github.io/ingress-nginx/deploy/#quick-start