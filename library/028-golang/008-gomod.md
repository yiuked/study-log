参数解析
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
