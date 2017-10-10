Spring AOP(面向方面编程)框架，用于在模块化方面的横切关注点。简单得说，它只是一个拦截器拦截一些过程，例如，当一个方法执行，Spring AOP 可以劫持一个执行的方法，在方法执行之前或之后添加额外的功能。
在Spring AOP中，有 4 种类型通知(advices)的支持：
1. 通知(Advice)之前 - 该方法执行前运行 `MethodBeforeAdvice`
2. 通知(Advice)返回之后 – 运行后，该方法返回一个结果 `AfterReturningAdvice`
3. 通知(Advice)抛出之后 – 运行方法抛出异常后，`ThrowsAdvic`
4. 环绕通知 – 环绕方法执行运行，结合以上这三个通知 `MethodInterceptor`。  
通常，开发过程中，人们会选择实现环绕通知。
