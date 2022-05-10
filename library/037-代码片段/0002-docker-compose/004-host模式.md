针对特定端口设置为`host`模式
```
version: '3'  
  
services:  
  html:  
    image: nginx:latest  
    container_name: html  
    restart: always  
    privileged: true  
    ports:  
      - target: 80  
        published: 9211  
        mode: host  
    volumes:  
      - ./build:/usr/share/nginx/html  
      - ./deploy/nginx/conf.d:/etc/nginx/conf.d  
      - ./deploy/nginx/log:/var/log/nginx
```
	  
将整个容器设置为`host`模式
```
version: '3'  
  
services:  
  html:  
    image: nginx:latest  
    container_name: html  
    restart: always  
    privileged: true 
	network_mode: host
    volumes:  
      - ./build:/usr/share/nginx/html  
      - ./deploy/nginx/conf.d:/etc/nginx/conf.d  
      - ./deploy/nginx/log:/var/log/nginx
```
> `host`模式下整机所有端口都会暴露，不需要再进行`ports`指定