docker compose 的 redis 模板：
```plain
  redis:
    container_name: redis
    image: redis
    command: 'redis-server --requirepass 123456'
    volumes:
      - ./redis:/data
      - /etc/timezone:/etc/timezone
      - /etc/localtime:/etc/localtime
      - type: bind
        source: /usr/share/zoneinfo/PRC
        target: /usr/share/zoneinfo/PRC
    environment:
      - SET_CONTAINER_TIMEZONE=true
      - CONTAINER_TIMEZONE=Asia/Shanghai
    ports:
      - 6379:6379
    restart: always
```