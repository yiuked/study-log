### 参数解析
```
download    download modules to local cache (下载module到本地cache))
edit        edit go.mod from tools or scripts (编辑go.mod文件)
graph       print module requirement graph (打印模块依赖图))
init        initialize new module in current directory (在当前目录初始化一个新的module)
tidy        add missing and remove unused modules (添加缺失的module,删除未使用的module)
vendor      make vendored copy of dependencies (将依赖复制到vendor下)
verify      verify dependencies have expected content (验证依赖项是否具有预期的内容)
why         explain why packages or modules are needed (解释为什么需要软件包或模块)
```


阿里云Go Module代理仓库服务
```
https://mirrors.aliyun.com/goproxy/
```
### 使用帮助
1. 使用go1.11以上版本并开启go module机制
2. 导出GOPROXY环境变量
```
export GOPROXY=https://mirrors.aliyun.com/goproxy/
```


### 依赖文件分布
首先要知道，mod 模式下安装的依赖包都存放在`$GOPATH/pkg/mod`目录下，
在 mod 模式下导入第三方包时会去`$GOPATH/pkg/mod`目录下加载，
而不是普通模式下的`$GOPATH/src | project/vendor`目录。

mod模式是否开启由环境变量 GO111MODULE 决定，GO111MODULE 环境变量有三个值：`on,auto（默认值）,off`。
> on：强制开启mod模式，此模式下不会去 $GOPATH/src，project/vendor 下加载第三方依赖包，只会去$GOPATH/pkg/mod下载加载。  
> auto：如果项目在 $GOPATH/src下，则转为普通模式，否则，转为mod模式。  
> off：关闭mod模式，转为普通的$GOPATH/src，project/vendor模式。  

### 代理设置
1. 在Go 1.13中，我们可以通过GOPROXY来控制代理
设置GOPROXY代理：
```
go env-w GOPROXY=https://goproxy.cn,direct
```

2. 设置GOPRIVATE来跳过私有库，比如常用的Gitlab或Gitee，中间使用逗号分隔：
```
go env -w GOPRIVATE=*.gitlab.com,*.gitee.com
```

3. 如果在运行go mod vendor时，提示`Get https://sum.golang.org/lookup/xxxxxx: dial tcp 216.58.200.49:443: i/o timeout`，则是因为Go 1.13设置了默认的`GOSUMDB=sum.golang.org`，这个网站是被墙了的，用于验证包的有效性，可以通过如下命令关闭：
```
go env -w GOSUMDB=off
```

4. 私有仓库自动忽略验证可以设置 `GOSUMDB="sum.golang.google.cn"`， 这个是专门为国内提供的sum 验证服务。
```
go env -w GOSUMDB="sum.golang.google.cn"
go env -w GOSUMDB="sum.golang.org"
```
-w 标记 要求一个或多个形式为 NAME=VALUE 的参数， 并且覆盖默认的设置
