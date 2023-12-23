## 项目部署  
  
> 服务器需要先安装docker、docker-compose，并启动mysql、redis、nginx服务。  
> 准备工作，需要先添加公钥到服务器的authorized_keys文件中，才能进行免密登录。如果登录失败，检测/Users/你的账号/.ssh/known_hosts中是否存在服务器的记录，如果存在，删除即可。  
> 需要在服务器数据目录创建项目名称的目录，如：/data/域名  
  
### 1.创建项目配置文件  
```  
make object  
```  
根据提示输入域名、admin api端口号、app api的端口号。输入后，会在config目录下生成项目的配置文件。可以调整当中的内容。项目配置文件存在时，不会再次生成。  
项目配置文件列表如下：  
```  
域名  
├── docker.admin.yaml # admin api的配置文件  
├── docker.app.yaml # app api的配置文件  
├── docker-compose.yaml # docker compose配置文件  
├── cert # 存放证书，需要手动复制到该目录  
└── nginx.conf # nginx配置文件  
```  
  
### 2.编译可执行文件  
与 #创建项目配置文件 不分先后，执行编译后，会在deploy目录下生成可执行文件与ui静态文件。  
```  
make install  
```  
执行后的目录结构如下：  
```  
deploy  
├──api  
├────adm  
├────app  
├──ui  
├────admui  
├────pcui  
└────wx  
```  
注：  
- 单独编译api可执行文件，需要安装go环境，执行`make api`即可。  
- 单独编译UI，需要安装nodejs，执行`make ui`即可（nodejs 18版本）。  
  
### 3.打包上传  
该阶段会将项目配置文件、可执行文件、ui静态文件打包上传到服务器。需要提前配置好服务器的ssh免密登录。  
```  
./update.sh <domain>  
```  
  
#### 3.1 打包上传时需要修改文件  
```  
./update.sh <domain> stop  
```  
stop 期间，还没有进行zip打包，可以修改文件。修改完成后，执行任意键进行文件打包与上传。  
  
#### 3.2 版本回退  
```  
./update.sh <domain> rollback <version>  
```  
version为版本号，可以查看packages目录下的版本号，选择回退的版本号。  
  
#### 3.3 只打包不上传  
```  
./update.sh <domain> pre  
```  
该命令会在packages目录下生成版本号目录，但是不会上传到服务器。  
  
## 常见问题  
### 1.在编译pcui时报错  
```  
...  
Error: error:0308010C:digital envelope routines::unsupported  
at new Hash (node:internal/crypto/hash:71:19)  
at Object.createHash (node:crypto:133:10)  
...  
```  
出现这个问题，是因为nodejs版本过低，或者过高，目前测试nodejs16版本可以。在项目的package.json中。我添加如下内容：  
```  
"scripts": {  
"serve": "export NODE_OPTIONS=--openssl-legacy-provider && vue-cli-service serve --mode development",  
"build": "export NODE_OPTIONS=--openssl-legacy-provider && vue-cli-service build --mode production",  
"lint": "vue-cli-service lint"  
},  
```  
注意，我测试时在linux下，nodejs18版本时，通过export命令设置NODE_OPTIONS，可以解决问题。但是在nodejs16版本下，不需要设置NODE_OPTIONS，直接执行vue-cli-service命令即可。  
windows可能不支持export命令，可以直接在命令行中执行：  
```  
set NODE_OPTIONS=--openssl-legacy-provider  
```  
也可以切换nodejs版本，使用nvm管理nodejs版本，切换到nodejs16,然后重试。


### shell 脚本 
```
#!/bin/bash  
  
host="$1"  
remotedir="/data/$1/"  
serviceName="${host//./_}"  
  
if [ "$1" == "" ]; then  
echo "please enter host,eg:www.example.com"  
exit 1  
fi  
  
if [ ! -d "config/$1" ]; then  
echo "config/$1 not exists"exit 1  
fi  
  
export LC_CTYPE="en_US.UTF-8"  
result=$(ssh root@$host "if [ ! -d $remotedir ]; then echo 0; else echo 1; fi")  
if [ "$result" -eq 0 ]; then  
echo "remote directory[$remotedir] not exists"  
exit 1  
else  
echo "remote directory[$remotedir] check accepted"  
fi  
  
function upload_zip() {  
echo "[step4] upload zip file ..."  
scp -r $1 root@$host:$remotedir  
  
filez=$(basename $1)  
echo "filez:$filez"  
# shellcheck disable=SC2087  
ssh root@$host <<eeooff  
  
# print ssh info  
cd $remotedir  
echo "================= Login ssh success, start update ... ================"  
echo "[ssh] Current path:"  
pwd  
echo "========= Files list ============="  
ls -ahl  
echo "=================================="  
  
# stop docker compose  
if [ -d "production" ]; then  
echo "[ssh] stop docker compose ..."  
cd production  
docker compose -p $serviceName down  
if [ $? -eq 0 ]; then  
echo "[ssh] docker compose -p $serviceName down success"  
cd ..  
rm -rf production  
else  
echo "[ssh] docker compose -p $serviceName down error"  
exit 1  
fi  
fi  
  
# unzip and move files  
echo "[ssh] unzip $filez ..."  
mkdir production  
unzip -q $filez -d production  
mv production/*/* production/  
  
# start docker compose  
cd production  
echo "[ssh] start docker compose ..."  
docker compose -p $serviceName up -d 2>&1  
  
# update nginx cert  
if [ -n "\$(ls -A cert/)" ]; then  
echo "[ssh] update nginx cert ..."  
if [ ! -d /etc/nginx/cert ]; then  
mkdir -p /etc/nginx/cert  
fi  
  
cp cert/* /etc/nginx/cert/  
fi  
  
# update nginx config  
if [ -f "$host.conf" ]; then  
echo "[ssh] update nginx config ..."  
cp $host.conf /etc/nginx/conf.d  
  
nginx -t  
if [ $? -eq 0 ]; then  
service nginx reload  
else  
echo -e "[ssh]\e[31mNginx check error\e[0m"  
fi  
fi  
eeooff  
}  
  
if [ "$2" == "rollback" ]; then  
echo "start rollback ..."  
if [ "$3" == "" ]; then  
echo "please enter version,eg:www.example.com rollback <1bede1-210801>"  
exit 1  
fi  
  
upload_zip "packages/$1/$3.zip"  
exit 0  
fi  
  
  
hash=$(git rev-parse --short=6 HEAD)  
time=$(date +%y%m%d)  
output="${hash}-${time}"  
package="packages/$1/$output"  
zipfile="$output.zip"  
  
echo "[step1] mkdir $package ..."if [ -f "packages/$1/$zipfile" ]; then  
echo "packages/$1/$zipfile is exist,continue will overwrite it,continue? [y/n]"read -r input  
if [ "$input" != "y" ]; then  
exit 1  
fi  
fi  
  
if [ ! -d "$package" ]; then  
set -x  
mkdir -p "$package"  
set +x  
else  
echo "$package is exist,continue will overwrite it,continue? [y/n]"read -r input  
if [ "$input" != "y" ]; then  
exit 1  
fi  
set -x  
rm -rf "$package"  
mkdir -p "$package"  
set +x  
fi  
  
echo "[step2] copy files ..."  
set -x  
cp -r deploy/* "packages/$1/$output"  
cp config/"$1"/docker.admin.yaml "$package/api/adm/"  
cp config/"$1"/docker.app.yaml "$package/api/app/"  
cp config/"$1"/docker-compose.yaml "$package/"  
cp config/"$1"/"$1".conf "$package/$1.conf"  
cp -r config/"$1"/cert "$package/cert"  
# shellcheck disable=SC2038  
find $package/ui/admui/static -name "*.js"|xargs sed -i '' 's/wwwexampletplcom/'"$1"'/g'  
# shellcheck disable=SC2038  
find $package/ui/pcui/static -name "*.js"|xargs sed -i '' 's/wwwexampletplcom/'"$1"'/g'  
# shellcheck disable=SC2038  
find $package/ui/wx/dist -name "*.js" |xargs sed -i '' 's/demo.tonyhr.cn/'"$1"'/g'  
set +x  
  
if [ "$2" == "stop" ]; then  
echo "waiting need change files,finished? [any key continue]"  
read -r input  
elif [ "$2" == "pre" ]; then  
exit 0  
fi  
  
echo "[step3] zip files ..."  
cd "packages/$1/" || exit 1  
# zip deploy files  
zip -q -r "$zipfile" "$output/"  
echo "info:zip finished"  
  
rm -rf "$output"  
  
# shellcheck disable=SC2218  
upload_zip "$zipfile"
```

### Makefile
```
.PHONY: all build run gotool install ui admui pcui wx api object clean help  
  
all: gotool build  
  
build:  
make clean  
make api  
make ui  
  
api:  
@if [ ! -d ./deploy/api/adm ];then mkdir -p ./deploy/api/adm;fi  
@if [ ! -d ./deploy/api/app ];then mkdir -p ./deploy/api/app;fi  
cd ./api && CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -ldflags="-s -w" -o ../deploy/api/adm/admapi ./admin/server/  
cd ./api && CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -ldflags="-s -w" -o ../deploy/api/app/appapi ./app/server/  
  
ui:  
make admui  
make pcui  
make wx  
  
admui:  
if [ ! -d ./deploy/ui ];then mkdir -p ./deploy/ui;fi  
if [ -d ./deploy/ui/admui ];then rm -rf ./deploy/ui/admui;fi  
mkdir ./deploy/ui/admui  
cd ./ui/admui && yarn build  
cp -r ./ui/admui/build/* ./deploy/ui/admui  
  
pcui:  
if [ ! -d ./deploy/ui ];then mkdir -p ./deploy/ui;fi  
if [ -d ./deploy/ui/pcui ];then rm -rf ./deploy/ui/pcui;fi  
mkdir ./deploy/ui/pcui  
cd ./ui/pcui && yarn build  
cp -r ./ui/pcui/dist/* ./deploy/ui/pcui  
  
wx:  
if [ ! -d ./deploy/ui ];then mkdir -p ./deploy/ui;fi  
if [ -d ./deploy/ui/wx ];then rm -rf ./deploy/ui/wx;fi  
mkdir ./deploy/ui/wx  
cd ./ui/wx && yarn build:mp-weixin  
cp -r ./ui/wx/dist ./deploy/ui/wx  
  
object:  
@echo "Enter object domain:"  
@read -r objectName && \  
export objectName=$$objectName; \  
echo "Enter admin api port:"; \  
read -r adminPort && \  
export adminPort=$$adminPort; \  
echo "Enter app api port:"; \  
read -r appPort && \  
export appPort=$$appPort; \  
echo "\nenv info => domain:$$objectName adminPort:$$adminPort appPort:$$appPort" && \  
if [ ! -d ./config/$$objectName ];then mkdir -p ./config/$$objectName;fi && \  
cp ./api/admin/server/config.docker.yaml ./config/$$objectName/docker.admin.yaml && \  
cp ./api/app/server/config.docker.yaml ./config/$$objectName/docker.app.yaml && \  
cp ./api/docker-compose.yaml ./config/$$objectName/docker-compose.yaml && \  
cp ./nginx/nginx.conf ./config/$$objectName/$$objectName.conf && \  
cd ./config/$$objectName && \  
if [ ! -d ./cert ];then mkdir cert;fi && \  
echo "\nfile created success!" && \  
ls -l && \  
`sed -i '' 's/{DOMAIN}/'"$$objectName"'/g' docker.admin.yaml docker.app.yaml $$objectName.conf docker-compose.yaml` && \  
`sed -i '' 's/{ADM_PORT}/'"$$adminPort"'/g' docker.admin.yaml docker.app.yaml $$objectName.conf docker-compose.yaml` && \  
`sed -i '' 's/{APP_PORT}/'"$$appPort"'/g' docker.admin.yaml docker.app.yaml $$objectName.conf docker-compose.yaml`  
  
install:  
make build  
  
clean:  
@if [ -d deploy/api ] ; then rm -rf deploy/api ; fi  
@if [ -d deploy/ui ] ; then rm -rf deploy/ui ; fi
```