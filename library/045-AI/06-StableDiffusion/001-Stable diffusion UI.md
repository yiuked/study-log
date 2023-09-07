启动时报以下错误
```
RuntimeError: "LayerNormKernelImpl" not implemented for 'Half'
```
> 运行时加下`./webui.sh --precision full --no-half` 参数