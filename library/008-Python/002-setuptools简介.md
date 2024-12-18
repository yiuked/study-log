### setuptools简介
`setuptools` 是 `Python Enterprise Application Kit（PEAK）` 的一个副项目，它是一组`Python`的`distutilsde`工具的增强工具（适用于`Python 2.3.5`以上的版本，`64`位平台则适用于 `Python 2.4` 以上的版本），可以让程序员更方便的创建和发布 `Python` 包，特别是那些对其它包具有依赖性的状况。    
经常接触`Python`的同学可能会注意到，当需要安装第三方`python`包时，可能会用到`easy_install`命令。`easy_install`是由`PEAK(Python Enterprise Application Kit)`开发的`setuptools`包里带的一个命令，所以使用`easy_install`实际上是在调用`setuptools`来完成安装模块的工作。  
`Perl` 用户比较熟悉 `CPAN`，而 `Ruby` 用户则比较熟悉 `Gems`；引导 `setuptools` 的 `ez_setup` 工具和随之而生的扩展后的 `easy_install` 与 `“Cheeseshop”（Python Package Index，也称为 “PyPI”）`一起工作来实现相同的功能。它可以很方便的让您自动下载，编译，安装和管理`Python`包。  
