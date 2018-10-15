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
