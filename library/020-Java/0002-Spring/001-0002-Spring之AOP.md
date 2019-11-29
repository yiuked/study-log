### AOP概述
Spring AOP(面向方面编程)框架，用于在模块化方面的横切关注点。简单得说，它只是一个拦截器拦截一些过程，例如，当一个方法执行，Spring AOP 可以劫持一个执行的方法，在方法执行之前或之后添加额外的功能。
在Spring AOP中，有 4 种类型通知(advices)的支持：
1. 通知(Advice)之前 - 该方法执行前运行 `MethodBeforeAdvice`
2. 通知(Advice)返回之后 – 运行后，该方法返回一个结果 `AfterReturningAdvice`
3. 通知(Advice)抛出之后 – 运行方法抛出异常后，`ThrowsAdvic`
4. 环绕通知 – 环绕方法执行运行，结合以上这三个通知 `MethodInterceptor`。  
通常，开发过程中，人们会选择实现环绕通知。

### AOP实列
实现一个AOP实列:
```
import org.aspectj.lang.JoinPoint;
import org.aspectj.lang.annotation.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;
import org.springframework.web.context.request.RequestContextHolder;
import org.springframework.web.context.request.ServletRequestAttributes;


import javax.servlet.http.HttpServletRequest;

@Aspect # 1.加入Aspect注解
@Component # 2.加入Component注解
public class HttpAspect {
    private final static Logger logger = LoggerFactory.getLogger(HttpAspect.class);

    # 3.加入Before注解，在controller前执行；Before的参数:execution(public * com.example.server.controller.*.*(..)表明拦截哪些控制器
    @Before("execution(public * com.example.server.controller.*.*(..))")
    public void processBefore(JoinPoint joinPoint) {
      logger.info("System controller running...");
    }

    @Before("common()")
    public void processBefore(JoinPoint joinPoint) {
        ServletRequestAttributes requestAttributes = (ServletRequestAttributes) RequestContextHolder.getRequestAttributes();
        HttpServletRequest httpServletRequest = requestAttributes.getRequest();

        logger.info("url={},length={},ip={},method={},class={},params={}",
                httpServletRequest.getRequestURI(),
                httpServletRequest.getContentLength(),
                httpServletRequest.getRemoteAddr(),
                httpServletRequest.getMethod(),
                joinPoint.getClass(),
                joinPoint.getArgs()
                );
    }

    # 6.调用统一的拦截方法
    @After("common()")
    public void processAfter() {
        logger.info("Process controller after.");
    }

    # 4.拦截的控制器可能用于多个场景，为了防止代码重复，可以通过@Pointcut方法定义一个统一的拦截方法
    @Pointcut("execution(public * com.example.server.controller.*.*(..))")
    public void common() {

    }

    # 7.@AfterReturning可以对Controller的返回值进行拦截
    @AfterReturning(returning = "object", pointcut = "common()")
    public void responseBefore(Object object) {
        logger.info("Response={}",object);
    }
}

```
