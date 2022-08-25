Makefile
```
.PHONY: all build run gotool install clean help  
  
BINARY_NAME=ossapi  
GO_FILE:=main.go  
  
all: gotool build  
  
build:  
   @if [ ! -f go.mod ];then go mod init aws_upload;fi  
   @go env -w GOPROXY=https://goproxy.cn,direct  
   @go mod tidy  
   CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o ${BINARY_NAME}  ${GO_FILE}  
  
run:  
   @go run ./  
  
gotool:  
   go fmt ./  
   go vet ./  
  
install:  
   make build  
  
  
clean:  
   @if [ -f ${BINARY_NAME} ] ; then rm ${BINARY_NAME} ; fi
```

shell
```
#!/bin/bash  
  
set -x  
docker run -v $(pwd):/go/src golang:1.18 sh -c "cd /go/src && make install"  
set +x
```