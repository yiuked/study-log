## Node内置关键词

**then**
重构前:
```
doAsync1(function () {
  doAsync2(function () {
    doAsync3(function () {})
  })
})
```
重构后:  
```
doAsync1(function () {})
.then(doAsync2(function () {}))
.then(doAsync3(function () {}))
```
**use**
引入中间件
```
//GET请求中间件,引入该中间件后，可处理类似 "?key1=value1&key2=value2" 这类请求
server.use(restify.queryParser());
//POST请求中间件,引入该中间件后，可处理POST请求
//server.use(restify.bodyParser());
```
**on**
