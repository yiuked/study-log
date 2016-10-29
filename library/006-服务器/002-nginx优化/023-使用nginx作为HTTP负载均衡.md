1. 介绍

在许多应用中，负载平衡是一种常用的技术来优化利用资源最大化吞吐量，减少等待时间，并确保容错。

可以使用nginx的作为一种非常高效的HTTP负载平衡器，将流量分配到多个应用服务器上提高性能，可扩展性和高可用性。
2. 负载均衡方法

nginx支持下面几种负载均衡机制：

    round-robin：轮询。以轮询方式将请求分配到不同服务器上
    least-connected：最少连接数。将下一个请求分配到连接数最少的那台服务器上
    ip-hash ：基于客户端的IP地址。散列函数被用于确定下一个请求分配到哪台服务器上

3. 负载均衡默认配置

nginx负载均衡最简单的配置如下：
http {
    upstream myapp1 {
        server srv1.example.com;
        server srv2.example.com;
        server srv3.example.com;
    }
 
    server {
        listen 80;
 
        location / {
            proxy_pass http://myapp1;
        }
    }
}

在上面的例子中，srv1，srv2，srv3运行着相同的应用程序。如果没有特别指定负载均衡方法默认是以轮询方式。所有的请求被代理到服务组myapp1，然后nginx负载均衡的分发请求。

nginx反向代理实现包括下面这些负载均衡HTTP、HTTPS、FastCGI、uwsgi，SCGI和memcached。

要配置HTTPS的负载均衡，只需使用“https”开头的协议。

当要设置FastCGI，uwsgi，SCGI，或者memcached的负载平衡，分别使用fastcgi_pass，uwsgi_pass，scgi_pass和memcached_pass指令。
4. 最少连接负载均衡

在一些要求需要更长的时间才能完成的应用情况下， 最少连接可以更公平地控制应用程序实例的负载。使用最少连接负载均衡，nginx不会向负载繁忙的服务器上分发请求，而是将请求分发到负载低的服务器上。

配置如下：
upstream myapp1 {
       least_conn;
       server srv1.example.com;
       server srv2.example.com;
       server srv3.example.com;
   }
5. 会话持久性

以轮询或最少连接的负载均衡算法，每个后续的客户端的请求，可以潜在地分配给不同的服务器上，并不能保证相同的客户端请求将总是指向同一服务器上。

这对于有会话信息的应用场景下，会有问题的。一般的做法是需要将session信息共享，如使用memcache来存放session。

如果将客户端的会话“粘性”或总是试图选择一个特定的服务器，也是可以的。负载均衡的ip-hash机制就可以实现。

配置如下：
upstream myapp1 {
    ip_hash;
    server srv1.example.com;
    server srv2.example.com;
    server srv3.example.com;
}
6. 加权负载均衡

可以使用权重来进一步控制影响nginx负载均衡算法。

在上面的例子中，都没有配置权重，这意味着所有指定的服务器都被视为同样的。

当指定的服务器的权重参数，权重占比为负载均衡决定的一部分。权重大负载就大。

配置如下：
upstream myapp1 {
        server srv1.example.com weight=3;
        server srv2.example.com;
        server srv3.example.com;
    }

这种情况下，每5个新的请求将被分布如下：3请求将被引导到SRV1，一个请求将去SRV2，另一个请求去srv3。
7. 后端健康检测

nginx反向代理包含内置的或第三方扩展来实现服务器健康检测的。如果后端某台服务器响应失败，nginx会标记该台服务器失效，在特定时间内，请求不分发到该台上。

max_fails指令设置在fail_timeout期间内连续的失败尝试。 默认情况下，max_fails为1。如果被设置为0，该服务器的健康检测将禁用。

fail_timeout参数还定义了多长时间服务器将被标记为失败。在fail_timeout后，服务器还是failed，nginx将检测该服务器是否存活，如果探测成功，将标记为活的。
8. 内容延伸

upstream模块内容: http://nginx.org/en/docs/http/ngx_http_upstream_module.html#server

应用负载均衡：http://nginx.com/products/application-load-balancing/

应用健康检测：http://nginx.com/products/application-health-checks/

活动监视：http://nginx.com/products/live-activity-monitoring/

更加详细的负载均衡配置：http://nginx.com/blog/load-balancing-with-nginx-plus/

http://nginx.com/blog/load-balancing-with-nginx-plus-part2/