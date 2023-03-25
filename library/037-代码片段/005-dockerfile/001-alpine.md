```
FROM alpine:latest

ENV TZ Asia/Shanghai

RUN apk add tzdata && cp /usr/share/zoneinfo/${TZ} /etc/localtime \
    && echo ${TZ} > /etc/timezone
```

```
FROM golang:1.18 as builder  
  
WORKDIR /go/src  
COPY . .  
  
RUN chmod +x build.sh && ./build.sh  
# chain service images  
FROM alpine:latest as chainapi  
  
LABEL MAINTAINER="womslabs"  
  
WORKDIR /go/src  
  
COPY --from=0 /go/src/deploy/bin/chainapi ./  
COPY --from=0 /go/src/deploy/bin/chainapi.yaml ./config.yaml  
  
ENTRYPOINT ./chainapi -f config.yaml
```