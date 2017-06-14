## 介绍
一个完整的基于Docker的PHP开发环境。  
它包含了封装好的Dokcer镜像，以及配置文件，为我们提供一个完整的PHP开发环境。  

## 概述
如何快速的安装 `NGINX`, `PHP`, `Composer`, `MySQL`, `Redis` 以及 `Beanstalkd`:  
1. 克隆`laradoc`到你的`PHP`项目内:  
```shell
git clone https://github.com/Laradock/laradock.git
```

2. 进入 `laradock` 目录，并将 `env-example` 更名为 `.env`.
```shell
cp env-example .env
```

3. 启动容器
```shell
docker-compose up -d nginx mysql redis beanstalkd
```
