### K8S中的 API Server认证

#### 一、认证

- HTTPS证书认证
- HTTP Token认证
- HTTP Base认证



##### 1.1、基于HTTPS证书认证双向认证

![image-20220315224529225](../../../images/typora/image-20220315224529225.png)

#### 二、授权

三种授权策略

##### 2.1 AlwaysDeny

拒绝所有请求

##### 2.2 AlwaysAllow

接收所有请求(默认配置)

##### 2.3 ABAC

(Attribute-Based Access Control)为基于属性的访问控制，表示使用用户配置的授权规则去匹配用户的请求。
我们可以通过设置“访问策略对象”中的如下属性来确定具体的授权行为。
- user（用户名):为字符串类型，该字符串类型的用户名来源于Token文件或基本认证
  文件中的用户名字段的值。
- readonly(只读标识):为布尔类型，当它的值为true时，表明该策略允许GET请求通过。
- resource（资源):为字符串类型，来自于URL的资源，例如“Pods”。
- namespace(命名空间):为字符串类型，表明该策略允许访问某个Namespace 的资源。

例如，我们要实现如下访问控制。

(1) 允许用户alice做任何事情
(2) kubelet只能访问Pod的只读API。
(3) kubelet能读和写Event对象。
(4) 用户bob只能访问myNamespace中的Pod的只读API。则满足上述要求的授权策略文件的内容写法如下:

```json
{ "user" : "alice" }
{ "user" : "kubelet", "resource": "pods", "readonly" : true}
{ "user" : "kubelet", "resource" : "events" }
{ "user" : "bob", "resource": "pods", "readonly": true, "ns": " myNamespace "}
```

#### 三、准入控制

Admission Control配备有一个“准入控制器”的列表，发送给API Server的任何请求都需要通过列表中每个准入控制器的检查，检查不通过，则API Server拒绝此调用请求。

当前可配置的准入控制器如下:

| 控制器名称              | 描述                                                         |
| ----------------------- | ------------------------------------------------------------ |
| AlwaysAdmit             | 允许所有请求                                                 |
| AlwaysPullImages        | 在启动容器之前总是去下载镜像，相当于在每个容器的配置项imagePullPolicy=Always |
| AlwaysDeny              | 禁止所有请求，一般用于测试                                   |
| DenyExecOnPrivileged    | 它会拦截所有想在Privileged Container上执行命令的请求。如果你的集群支持Privileged Container，你又希望限制用户在这些Privileged Container上执行命令，那么强烈推荐你使用它。 |
| **ServiceAccount**      | 这个插件将serviceAccounts实现了自动化，默认启用              |
| **SecurityContextDeny** | 这个插件将使用了SecurityContext的 Pod中定义的选项全部失效。SecurityContext在 Container中定义了操作系统级别的安全设定( uid、gid、capabilities、SELinux 等) |
| **ResourceQuota**       | 用于配额管理目的，作用于Namespace 上，它会观察所有的请求，确保在namespace 上的配额不会超标。推荐在Admission Control参数列表中这个插件排最后一个 |
| **LimitRanger**         | 用于配额管理，作用于Pod 与Container 上，确保Pod 与 Container 上的配额不会超标 |
| NamespaceLifecycle      | 如果尝试在一个不存在的namespace中创建资源对象，则该创建请求将被拒绝。当删除一个namespace时，系统将会删除该namespace中的所有对象，包括Pod、Service等。 |
