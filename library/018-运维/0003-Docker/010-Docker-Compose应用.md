### Docker compose 应用
#### 安装
Mac下，如果安装了docker则需要再安装了，默认已集成了compose,
centos下安装docker-compose:
```
yum install docker-compose
```

#### 操作
如果修改了docker-compose.yml文件，需要运行`docker-compose down`后，再运行`docker-compose up -d`来进行重构。

#### 问题
1. 如果在运行过程中，提示

```
docker-compose cannot execute binary file
```
请检查docker的版本，可能是docker的版本与compose不一匹配导致，更新一下docker则可。
fig可取代compose
http://www.fig.sh/

2. 如何容器运行后，马上退出

   ```
   tty: true
   stdin_open: true
   ```

   



#### 合并yaml文件，并启动合并后的内容
```
docker-compose -f 1.yaml -f 2.yaml up -d 2>&1
```

* 模板

  ```
  version: '2.2'
  
  networks:
      ocot:
  
  services:
      api.core:
          container_name: api.core
          image: centos:centos7
          volumes:
           - /root/core/api:/var/api
          environment:
           - SET_CONTAINER_TIMEZONE=true
           - CONTAINER_TIMEZONE=Asia/Shanghai
          environment:
           - TZ=Asia/Shanghai
          working_dir: /var/api
          command: ./ocot web
          ports:
           - 9080:8080
          networks:
           - ocot
          restart: always
      api.order:
          container_name: api.order
          image: centos:centos7
          volumes:
           - /root/core/api:/var/api
          environment:
           - SET_CONTAINER_TIMEZONE=true
           - CONTAINER_TIMEZONE=Asia/Shanghai
          environment:
           - TZ=Asia/Shanghai
          working_dir: /var/api
          command: ./ocot order
          networks:
           - ocot
          restart: always
  
  ```






* 在docker-compose中配置日志:

```
version: '2.2'

networks:
    pms:

services:
    pms_api:
        container_name: pms_api
        image: centos:latest
        logging:
                driver: json-file
                options:
                        max-size: 1g
        volumes:
         - /home/www/pms/api:/var/api
        environment:
         - SET_CONTAINER_TIMEZONE=true
         - CONTAINER_TIMEZONE=Asia/Shanghai
        environment:
         - TZ=Asia/Shanghai
        working_dir: /var/api
        command: ./ocot web
        ports:
         - 9083:9080
        networks:
         - pms

```