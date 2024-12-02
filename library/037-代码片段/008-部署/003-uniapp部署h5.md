```shell
#!/bin/zsh  
  
project="www.abc.com"  
  
if [ -d ./unpackage/deploy ];then  
  rm -rf ./unpackage/deploy/*  
else  
  mkdir -p ./unpackage/deploy;  
fi  
  
/Applications/HBuilderX.app/Contents/MacOS/cli publish --platform h5 --project cihaishop  
res=$?  
if [ $res -ne 0 ];then  
  echo "编译失败"  
  exit 1  
fi  
  
cp -r ./unpackage/dist/build/web ./unpackage/deploy/h5/  
echo "编译成功"  
  
tar -czvf ./unpackage/deploy/h5.tar.gz -C ./unpackage/deploy h5  
echo "打包成功"  
rm -rf ./unpackage/deploy/h5  
  
scp ./unpackage/deploy/h5.tar.gz root@cihai520.com:/www/wwwroot/$project/system/runtime/  
res=$?  
if [ $res -ne 0 ];then  
  echo "上传失败"  
  exit 1  
fi  
  
ssh root@cihai520.com << eeooff  
cd /www/wwwroot/$project/system/runtime/  
tar -zxvf h5.tar.gz  
rm -f h5.tar.gz  
rm -rf /www/wwwroot/$project/public_html/h5  
cp -r h5 /www/wwwroot/$project/public_html  
rm -rf h5  
eeooff
```