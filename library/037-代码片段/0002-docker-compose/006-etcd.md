```
version: '2'  
  
networks:  
  app-tier:  
    driver: bridge  
  
services:  
  etcd:  
    image: 'bitnami/etcd:3.4.18'  
    container_name: etcd  
    environment:  
      - ALLOW_NONE_AUTHENTICATION=no  // 启用密码验证
      - ETCD_ROOT_PASSWORD=123456     // 设置root密码为123456
	  								  // 当有集群时，向外广播自己的地址 
      - ETCD_ADVERTISE_CLIENT_URLS=http://127.0.0.1:2379 
    ports:  
      - 2379:2379  
      - 2380:2380  
    networks:  
      - app-tier  
  
  etcdkeeper:  
    image: 'evildecay/etcdkeeper:v0.7.6'  
    container_name: etcdkeeper  
    ports:  
      - 2388:8080  
    networks:  
      - app-tier  
    depends_on:  
      - etcd
```