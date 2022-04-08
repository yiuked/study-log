## Ingress

### 一、概述

通常情况下，Service 和 Pod 的 IP 仅可在集群内部访问。集群外部的请求需要通过负载均衡转发到 Service 在 Node 上暴露的 NodePort 上，然后再由 kube-proxy 通过边缘路由器 (edge router) 将其转发给相关的 Pod 或者丢弃。K8s的Pod和Service需要通过NodePort或者loadBlance把服务暴露到外， 但是随着微服务的增多。管理会变得越来越麻烦，比如端口分配、日志采集等。能不能对所有的服务进行统一转发、管理呢？通过Ingress便可以完成。它有以下功能：

- 基于http-header 的路由
- 基于 path 的路由
- 单个ingress 的 timeout
- 请求速率limit
- rewrite 规则

### 二、组成

Ingress 主要分为两部分：

- Ingress Controller 是流量的入口，是一个实体软件， 一般是Nginx 和 Haproxy 。

- Ingress 描述具体的路由规则。



参数文献：

- https://kubernetes.io/zh/docs/concepts/services-networking/ingress/