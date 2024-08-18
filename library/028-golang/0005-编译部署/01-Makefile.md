
```shell
.PHONY: all build run web gotool install nginx clean help config  
  
all: gotool build  
  
build:  
make clean  
@if [ ! -f go.mod ];then go mod init gowebsocket;fi  
@if [ ! -d ./deploy ];then mkdir -p ./deploy;fi  
#@go env -w GOPROXY=https://goproxy.cn,direct  
@go mod tidy  
CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -ldflags="-s -w" -o ./deploy/gows ./  
make config  
  
config:  
cp ./config/app.prod.yaml deploy/app.yaml  
  
clean:  
@if [ -f deploy/gows ] ; then rm -rf deploy/gows ; fi  
@if [ -f deploy/app.yaml ] ; then rm -rf deploy/app.yaml ; fi  
  
install:  
make build
```

`.PHONY` 的作用：当我们执行 `make xxx`时，系统轩优化去判断`xxx`是否为当前目录下的一个文件，或者文件夹，如果文件或者文件夹存在时，则会报以下错误:
```
make xxx
make: 'xxx' is up to date.
```
此时，我们就需要用到`.PHONY`,它会告诉系统，`xxx`是`make`命令后的一个参数。