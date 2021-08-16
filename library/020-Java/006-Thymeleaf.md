- ```
  th:field // 需要配合 th:object
  th:value // 直接取对象值
  ${#numbers.formatDecimal(user.blance, 1, 2)} // 格式化输出
  ```

- SpringBoot+Thyemelaf开发环境正常，打包jar发到服务器就报错Template might not exist or might not be accessible

  > 引用模板文件时把 "/" 前缀去掉
  >
  > ```
  > private String prefix = "/account/fee";
  > 改成
  > private String prefix = "account/fee";
  > ```
  >
  > 
  >
  > 还有页面中使用了th:include语法的，
  >
  > ```
  > th:include="/xxx/xxx"
  > 前端的/去掉，
  > th:include="xxx/xxx"
  > ```