## Controller的使用

1. 使用`Controller`必须添加注解
```
@Controller
public class DemoController{
  ...
}
```

2. `RestController`的使用
```
@RestController
public class DemoController{
  ...
}
```

3. `RequestMapping`类型
```
#给类添加一个总体roule
@RequestMapping("/index")
#给方法添加一个roule
@RequestMapping(value = "/hello", method = RequestMethod.GET)
#给方法添加多处roule
@RequestMapping(value = {"/hello", "demo"}, method = RequestMethod.GET)
```

4. 获取请求参数  


```java
@PathVariable
#通过/product/xxx传参数
@RequestMapping(value = "/product1/{name}", method = RequestMethod.GET)
public String product1(@PathVariable("name") String name) {
    return "Product1:" + name;
}

#通过?name=xxx传参数
@RequestMapping(value = "/product", method = RequestMethod.GET)
public String product(@PathVariable("name") String name) {
    return "Product:" + name;
}


@RequestParam
@RequestParam(value="username", required = false, defaultValue = 0)
value 请求字段名
required 是否居必传
defaultValue 默认值

@GetMapping
@GetMapping("/product")
对注解进行了有效的缩写，它等同于
@RequestMapping(value = "/product", method = RequestMethod.GET)
当然还有
@PostMapping
@PutMapping
...
```
