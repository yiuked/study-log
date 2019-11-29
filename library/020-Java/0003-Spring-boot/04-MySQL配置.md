## MySQL配置指南

* 在`build.gradel`或者`pox.xml`中引入依赖包:

```
dependencies {
  ...
	compile('mysql:mysql-connector-java')
}

```

* 在`application.yml`中配置数据库连接方式.

```
spring:
  datasource:
    driver-class-name: com.mysql.jdbc.Driver
    url: jdbc:mysql://127.0.0.1:3306/demo
    username: root
    password: ""
  jpa:
    hibernate:
      ddl-auto: update
      show-sql: true
```


* 通常采用JPA对MYSQL进行操作，因此

```
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;

@Entity
public class Girl {
    @Id
    @GeneratedValue
    private Integer girlId;
    private String username;

    public Girl() {
    }

    public Integer getGirlId() {
        return girlId;
    }

    public void setGirlId(Integer girlId) {
        this.girlId = girlId;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }
}
```
* 需要创建一个继承`JpaRepository`的接口  

```
import org.springframework.data.jpa.repository.JpaRepository;
interface GirlRepository extends JpaRepository<Girl, Integer> {}
```

* 控制器中调用

```
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController
public class GirlController {

    @Autowired
    private GirlRepository girlRepository;

    @GetMapping("/girls")
    public List<Girl> getGirlList() {
        return girlRepository.findAll();
    }
}

```
