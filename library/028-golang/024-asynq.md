https://github.com/hibiken/asynq#command-line-tool

```
go install github.com/hibiken/asynq/tools/asynq
```

```
asynq task run --queue=default --id=taskid --uri 127.0.0.1:6379  
```

taskid 可以通过`asynq dash`来获取