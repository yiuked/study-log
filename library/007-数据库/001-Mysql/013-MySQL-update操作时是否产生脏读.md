比如，表名A，字段名为 number，如下的SQL语句:
```
语句1：update A set number=number+ 5 where id=1;
语句2：update A set number=number+ 7 where id=1;
```
假设这两条SQL语句同时被mysql执行，id=1的记录中number字段的原始值为 10，那么是否有可能出现这种情况：

语句1和2因为同时执行，他们得到的number的值都是10，都是在10的基础上分别加5和7，导致最终number被更新为15或17，而不是22？

不会，这个其实就是关系型数据库本身就需要解决的问题。
首先，他们同时被MySQL执行，你的意思其实就是他们是并发执行的，而并发执行的事务在关系型数据库中是有专门的理论支持的-ACID，事务并行等理论，所有关系型数据库实现，包括Oracle，MySQL都需要遵循这个原理。  
简单一点理解就是锁的原理。  
这个时候第一个update会持有id=1这行记录的排它锁，第二个update需要持有这个记录的排它锁的才能对他进行修改，正常的话，第二个update会阻塞，直到第一个update提交成功，他才会获得这个锁，从而对数据进行修改。也就是说，按照关系型数据库的理论，这两个update都成功的话，id=1的number一定会被修改成22。如果不是22，那就是数据库实现的一个严重的bug。  

如果想要深入了解，可能你要预读一下:  

数据库与事务处理  
https://link.zhihu.com/?target=https%3A//book.douban.com/subject/1318221/    

数据库原理  
https://link.zhihu.com/?target=http%3A//blog.jobbole.com/100349/  
英文原文  
https://link.zhihu.com/?target=http%3A//coding-geek.com/how-databases-work/  


作者：李春  
链接：https://www.zhihu.com/question/46733729/answer/128582074  
来源：知乎  
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。  

https://www.zhihu.com/question/46733729/answer/128582074  
