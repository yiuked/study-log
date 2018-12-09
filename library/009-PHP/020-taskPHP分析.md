任务列表:config.php中task_list.
任务名:config.php中task_list的key值.
distribute进程：用于调度列表中任务的进程.
worker进程：用于执行列表中的任务,调用方式`php main.php worker "app\tasks\message\WeChatTask" `

缓存:
键值                   键值
listen[任务名]          [true|false] # true为任务启用中，false任务取消
task_worker_[任务名]   任务的基本信息，如时间等
task_exec_[任务名]     待执行队列
task_list              会存储config.php里task_list的所有任务,只保存【任务名】.
close_worker
task_sleep

1.当应用启用时，启动distribute进程,该进程读取【任务列表】，
  将列表中的每条任务存储在`task_worker_[任务名]`中，值为
  ```
    Array
    (
        [timer] => __PHP_Incomplete_Class Object
            (
                [__PHP_Incomplete_Class_Name] => taskphp\Timer
            )

        [task] => __PHP_Incomplete_Class Object
            (
                [__PHP_Incomplete_Class_Name] => app\tasks\invest\InvestBorrowTask
            )

        [skip] => 1
        [run_time] => 1544322402
    )
  ```
  并将【任务名】push到`task_list`列表中,同时将`task_sleep`设置为0。
  接下来distribute进程会进入一个循环的监听状态，检测`task_list`中的任务listen[任务名]是否为true,
  为true的情况下，则将任务下一次要执行的时间与信息推送到task_exec_[任务名]中.

2.在`distribute`进程执行同时，主进程根据传递进的任务,写入`close_worker 值得为 false`，
  同时，将传递进来需要执行的任务写入到listen[任务名]中，值为true，表示该任务需要执行。
  在写入listen[任务名]后，调用popen执行worker进行，执行任务.

3.worker进程在由main进程启用后，进行持续的监听状态，监听listen[任务名]是否为true,为true的情况下，则抛出
task_exec_[任务名]的任务进行执行。
