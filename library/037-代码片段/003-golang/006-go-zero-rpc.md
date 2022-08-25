```shell
#!/bin/bash  
  
read -r -d '' tpl <<-EOF  
syntax = "proto3";  
  
package pb;  
  
option go_package = "./pb";  
  
message IdReq{  
  int64 id = 1;}  
  
message UserInfoReply{  
  int64 id = 1;  string name = 2;  string number = 3;  string gender = 4;}  
  
service user {  
  rpc getUser(IdReq) returns(UserInfoReply);}  
EOF  
  
if [ "$1" == "" ]; then  
  echo -e "if you want to generate rpc project,example: ./rpc.sh explore"  
  echo "if you want to generate rpc file example? Y(Yes)/N(No):"  
  # shellcheck disable=SC2162  
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
  storageDir="../app/$moduleName/cmd/rpc/pb"  
  if [ ! -f "$storageDir" ]; then  
    mkdir -p "$storageDir"  
  fi  
  echo "$tpl">"$storageFile/$moduleName.proto"  
  echo "Done"  
  exit  
fi  
  
set -x  
protoDir="../app/$1/cmd/rpc/pb"  
  
# shellcheck disable=SC2164  
cd "$protoDir"  
goctl rpc protoc "$1.proto" --go_out=.. --go-grpc_out=.. --zrpc_out=..  
set +x
```