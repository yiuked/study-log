```shell
#!/bin/bash  
  
if [ "$1" == "" ]; then  
  echo "params 1 is empty,example: model.sh order explore"  
  exit 1  
fi  
  
if [ "$2" == "" ]; then  
  echo "params 2 is empty,example: model.sh order explore"  
  exit 1  
fi  
  
goctl model mysql ddl -c --home ../deploy/goctl -s ../deploy/sql/$1 -d ../app/$2/model
```