1. 为文件或者目录建立软连接.
在 `D:\wwwroot\tools\` 目录下创建`D:\php\vendor`文件夹的软链接，名称保持为`vendor`
命令：
```
  mklink /D D:\wwwroot\tools\vendor D:\php\vendor
```
>Note：/D 不能少，不加表示创建文件的软链接而不是文件夹
