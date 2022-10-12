```plain
redis:
image: 'redis:4-alpine'
command: redis-server --requirepass yourpassword
ports:
- '6379:6379'
```