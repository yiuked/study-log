```shell
#!/bin/bash  
  
read -r -d '' tpl <<-EOF  
type (  
    LoginReq {        Username string \`json:"username"\`        Password string \`json:"password"\`    }  
    LoginReply {        Id           int64 \`json:"id"\`        Name         string \`json:"name"\`        Gender       string \`json:"gender"\`        AccessToken  string \`json:"accessToken"\`        AccessExpire int64 \`json:"accessExpire"\`        RefreshAfter int64 \`json:"refreshAfter"\`    })  
  
// 如果需要包含外部的api文件  
// import (  
//  "types/request.api"  
//  "types/response.api"  
// )  
  
service user-api {  
    @handler login    post /user/login (LoginReq) returns (LoginReply)}  
EOF  
  
if [ "$1" == "" ]; then  
  echo -e "if you want to generate api project,example: ./api.sh explore"  
  echo "if you want to generate module api? Y(Yes)/N(No):"  
  read handelAction  
  # shellcheck disable=SC1068  
  handelActions=$(echo "$handelAction" | tr A-Z a-z)  
  if [ "$handelActions" == "n" ]; then  
    echo "exit"  
    exit 0  
  fi  
  echo "put module name:"  
  # shellcheck disable=SC2162  
  read moduleName  
  if [ "$moduleName" == "" ]; then  
    echo "module name is require"  
    exit 0  
  fi  
  storageDir="../app/$moduleName/cmd/api/desc"  
  if [ ! -f "$storageDir" ]; then  
    mkdir -p "$storageDir"  
  fi  
  echo "$tpl">"$storageFile/$moduleName.api"  
  echo "Done"  
  exit  
fi  
  
goctl api go -api "../app/$1/cmd/api/desc/$1.api" -dir "../app/$1/cmd/api/"
```