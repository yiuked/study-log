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
如果在运行过程中，提示
```
docker-compose cannot execute binary file
```
请检查docker的版本，可能是docker的版本与compose不一匹配导致，更新一下docker则可。
fig可取代compose
http://www.fig.sh/

#### 合并yaml文件，并启动合并后的内容
```
docker-compose -f 1.yaml -f 2.yaml up -d 2>&1
```
