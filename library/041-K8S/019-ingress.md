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

### 三、Ingress Controller
Ingress本身不提供服务，它依赖Ingress Controller，Ingress Controller以Pod的形式部署在Kubernetes集群内，实质上我们无法从外面直接访问，依然要将其暴露出来，暴露方式有几种：

-   通过NodePort形式暴露，前面需接一个负载均衡
-   通过LoadBalancer形式暴露，云产商默认就是这种方式
-   直接在Pod中使用hostport，前面需接一个负载均衡

ingress的实现方式更智能、更友好，相对的配置就略微复杂，它一个IP可以暴露多个应用，支持同域名不同uri，支持证书等功能。

目前Ingress暴露集群内服务的行内公认最好的方式，不过由于其重要地位，世面上有非常多的Ingres Controller，常见的有：

-   Kubernetes Ingress
-   Nginx Ingress
-   Kong Ingress
-   Traefik Ingress
-   HAProxy Ingress
-   Istio Ingress
-   APISIX Ingress

除了上面列举的这些，还有非常多的Ingress Controller，面对如此多的Ingress Controller，我们该如何选择呢？参考的标准是什么？

一般情况下可以从以下几个维度进行判断：

-   支持的协议：是否支持除HTTP(S)之外的协议
-   路由的规则：有哪些转发规则，是否支持正则
-   部署策略：是否支持ab部署、金丝雀部署、蓝绿部署等
-   upstream探针：通过什么机制判定应用程序正常与否，是否有主动和被动检查，重试，熔断器，自定义运行状况检查等解决方案
-   负载均衡算法：支持哪些负载均衡算法，Hash、会话保持、RR、WRR等
-   鉴权方式：支持哪些授权方案？基本，摘要，OAuth，外部身份验证等
-   DDoS防护能力：是否支持基本的限速、白名单等
-   全链路跟踪：能否正常接入全链路监控
-   JWT验证：是否有内置的JSON Web令牌验证，用于对最终应用程序的用户进行验证和验证
-   图像界面：是否需要图形界面
-   定制扩展性：是否方便扩展
-   
[ingress控制器那么多，到底该选哪一个？累觉不爱。 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/302452502)
![[Pasted image 20220606223607.png]]


```
apiVersion: networking.k8s.io/v1 
kind: Ingress
metadata:
  name: nginx-ingress
  namespace: default
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /$2
spec:
  ingressClassName: nginx
  rules:
  - host: 
    http:
      paths:
      - pathType: Prefix
        path: /g(/|$)(.*)
        backend:
          service:
            name: basic-nginx
            port:
              number: 80
      - pathType: Prefix
        path: /a(/|$)(.*)
        backend:
          service:
            name: otel-collector
            port:
              number: 4317
      - pathType: Prefix
        path: /b(/|$)(.*)
        backend:
          service:
            name: otel-collector
            port:
              number: 4318
      - pathType: Prefix
        path: /c(/|$)(.*)
        backend:
          service:
            name: otel-collector
            port:
              number: 8888
```
> - 默认如果指定为 pathType 为 Prefix ，那么 path的路径与访问的资源的路径一至。即当访问 `/a`时会到对应服务下的`/a`目录下找对应的资源
> - ingressClassName的获取访问 `kubectl get ingressclass`


参数文献：

- https://kubernetes.io/zh/docs/concepts/services-networking/ingress/
- https://kubernetes.github.io/ingress-nginx/deploy/#quick-start
- https://blog.csdn.net/qq_39218530/article/details/121374602