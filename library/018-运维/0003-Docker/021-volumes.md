```yaml
version: '2'

services:
  mariadb:
    image: docker.io/bitnami/mariadb:10.6
    environment:
      # ALLOW_EMPTY_PASSWORD is recommended only for development.
      - ALLOW_EMPTY_PASSWORD=yes
      - MARIADB_USER=bn_prestashop
      - MARIADB_DATABASE=bitnami_prestashop
    ports:
      - '33061:3306'
    volumes:
      - 'mariadb_data:/bitnami/mariadb'

  prestashop:
    image: docker.io/bitnami/prestashop:8
    ports:
      - '8025:8080'
    environment:
      - PRESTASHOP_HOST=localhost
      - PRESTASHOP_DATABASE_HOST=mariadb
      - PRESTASHOP_DATABASE_PORT_NUMBER=3306
      - PRESTASHOP_DATABASE_USER=bn_prestashop
      - PRESTASHOP_DATABASE_NAME=bitnami_prestashop
      # ALLOW_EMPTY_PASSWORD is recommended only for development.
      - ALLOW_EMPTY_PASSWORD=yes
    volumes:
      - 'prestashop_data:/bitnami/prestashop'
    depends_on:
      - mariadb

volumes:
  mariadb_data:
    driver: local
  prestashop_data:
    driver: local
```
上示例中，指定在本地创建了两个存储桶：
```yaml
volumes:
  mariadb_data:
    driver: local
  prestashop_data:
    driver: local
```
可以通过以下命令来查询已创建的`volume`
```
docker volume ls
```
如果想要查看存储的位置
```
docker volume inspect ps8_prestashop_data
```

指定存储路径
```
volumes:
  mariadb_data:
    driver: local
    driver_opts:
      type: none
      device: /path/on/host
      o: bind
  prestashop_data:
    driver: local
    driver_opts:
      type: none
      device: /path/on/host
      o: bind

```