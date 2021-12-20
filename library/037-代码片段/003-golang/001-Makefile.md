`Makefile`文件内容:

```shell
.PHONY: all build run gotool install clean help

BINARY_NAME=srv_api
BIN_DIR=../../bin/
LAN_FILE=.go
GO_FILE:=${BINARY_NAME}${LAN_FILE}

all: gotool build

build:
	CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o ${BINARY_NAME}  ${GO_FILE}

run:
	@go run ./

gotool:
	go fmt ./
	go vet ./

install:
	make build
	mv ${BINARY_NAME} ${BIN_DIR}

clean:
	@if [ -f ${BINARY_NAME} ] ; then rm ${BINARY_NAME} ; fi


```

> .PHONY 的作用,当目录下如在诸如`clear` `build` `all` `gotool` 等文件时,会导致程序中断退出,通过`.PHONY`可以有效的避免此类问题.

