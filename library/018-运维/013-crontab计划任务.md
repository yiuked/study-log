## Crontab计划任务详解
#### 在创建计划任务的时候，如果想以某一个特定的用户去执行应该如何操作.
```
crontab: invalid option -- 'h'
crontab: usage error: unrecognized option
Usage:
 crontab [options] file
 crontab [options]
 crontab -n [hostname]

Options:
 -u <user>  定义用户
 -e         编辑用户任务
 -l         列出用户计划任务
 -r         删除计划任务
 -i         prompt before deleting
 -n <host>  set host in cluster to run users' crontabs
 -c         get host in cluster to run users' crontabs
 -s         selinux context
 -x <mask>  enable debugging

Default operation is replace, per 1003.2
```
如果想为`www`用户创建一个任务
```
crontab -u www -e
```
如果不使用`-u www`的情况下，默认是创建在`root`用户下，程序以`root`用户执行。
创建成功后，如果需要查看某一个用户的任务是否创建成功。
```
crontab -u www -l
```
#### 命令格式说明：
```
* * * * * command
| | | | |- 星期 (取值范围0 - 6)
| | | |- 月份 （取值范围1-12）
| | |- 日期 （取值范围1-31）
| |- 小时 (取值范围0-23)
|- 分钟（取值范围0-59）
```
> 星号(\*)：代表所有可能的值，例如month字段如果是星号，则表示在满足其它字段的制约条件后每月都执行该命令操作。  
> 逗号(,)：可以用逗号隔开的值指定一个列表范围，例如，"1,2,5,7,8,9"  
> 中杠(-)：可以用整数之间的中杠表示一个整数范围，例如"2-6"表示"2,3,4,5,6"    
> 正斜线(/)：可以用正斜线指定时间的间隔频率，例如"0-23/2"表示每两小时执行一次。同时正斜线可以和星号一起使用，例如*/10，如果用在minute字段，表示每十分钟执行一次。  

#### 使用实例

1. 每1分钟执行一次 `command`
```
  * * * * * command
```
2. 每小时的第3和第15分钟执行  
```
  3,15 * * * * command
```
3. 在上午8点到11点的第3和第15分钟执行
```
  3,15 8-11 * * * command
```
4. 每隔两天的上午8点到11点的第3和第15分钟执行
```
  3,15 8-11 */2 * * command
```
5. 每个星期一的上午8点到11点的第3和第15分钟执行
```
  3,15 8-11 * * 1 command
```
6. 每晚的21:30重启smb
```
30 21 * * * /etc/init.d/smb restart
```
7. 每月1、10、22日的4 : 45重启smb
```
  45 4 1,10,22 * * /etc/init.d/smb restart
```
8. 每周六、周日的1 : 10重启smb
```
  10 1 * * 6,0 /etc/init.d/smb restart
```
9. 每天18 : 00至23 : 00之间每隔30分钟重启smb
```
  0,30 18-23 * * * /etc/init.d/smb restart
```
10. 每星期六的晚上11 : 00 pm重启smb
```
  0 23 * * 6 /etc/init.d/smb restart
```
11. 每一小时重启smb
```
  * */1 * * * /etc/init.d/smb restart
```
12. 晚上11点到早上7点之间，每隔一小时重启smb
```
  23-7/1 * * * /etc/init.d/smb restart
```
14. 每月的4号与每周一到周三的11点重启smb
```
  0 11 4 * mon-wed /etc/init.d/smb restart
```
15. 一月一号的4点重启smb
```
  0 4 1 jan * /etc/init.d/smb restart
```

16. 每小时执行`/etc/cron.hourly`目录内的脚本
```
  01   *   *   *   *     root run-parts /etc/cron.hourly
```
> run-parts这个参数了，如果去掉这个参数的话，后面就可以写要运行的某个脚本名，而不是目录名了

#### 后记
在crontab中如果调用shell文件时,可能会出现这种情况，正常执行shell文件没有任何问题，但是
添加到crontab中时，死活不执行，或者只执行部分，关于这个问题产生的原因为：  
shell文件在用户自主输入时与crontab执行时的环境变量不一样，可以通过:
```
$ env
```
来显示当前系统的环境变量，再到shell文件添加env日志:
```
env >> test.log
```
通过对比查看是缺少了哪些环境变量，找到后，可以在shell文件中添加:
```
PATH=$PTAH:[缺少的目录]
```

### 当PHP文件中引require时，提示文件找不到？
如果计划任务是这么写的
```
* * * * * php /var/php/cron.php
```
其中`cron.php`中通过require引入关联路径文件
```
<?php
require "../config/config.php";
```
那么你很可能会得到一个错误的信息，就是config.php文件找不到。
脚本会把根目录`/`当成当前路径，以`/`为中心进行关联，因此找不到文件。
此时，需要在执行脚本前进入到文件所在路径
```
* * * * * cd /var/php && php /var/php/cron.php
```
