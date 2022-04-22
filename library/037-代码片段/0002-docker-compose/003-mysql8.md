```
  mysql:
    image: mysql/mysql-server:8.0.28
#    image: mysql/mysql-server:5.7.37
    container_name: mysql
    environment:
      # 时区上海
      TZ: Asia/Shanghai
      # root 密码
      MYSQL_ROOT_PASSWORD: root
    ports:
      - 3306:3306
    volumes:
      # 数据挂载
      - ./data/mysql/data:/var/lib/mysql
      # 日志
    command:
      # 将mysql8.0默认密码策略 修改为 原先 策略 (mysql8.0对其默认策略做了更改 会导致密码无法匹配)
      --default-authentication-plugin=mysql_native_password
      --character-set-server=utf8mb4
      --collation-server=utf8mb4_general_ci
      --explicit_defaults_for_timestamp=true
      --lower_case_table_names=1
    privileged: true
    restart: always
    networks:
      - womapi_net
```

