## Request详解
关于`request`,在入口文件`index.php`就能很轻易找到它的踪迹，相对于其它的组件，`request`
相对来说是比较独立的存在的组件。
```
$response = $kernel->handle(
    $request = Illuminate\Http\Request::capture()
);
```

`Request` 定义在 `Illuminate\Http\Request.php`中，从定义的源码中，可以知道，它是继承的`Symfony`
框架的`Request`,并在此基础进进行了进一步的扩展.
```
class Request extends SymfonyRequest implements Arrayable, ArrayAccess{

}
```
