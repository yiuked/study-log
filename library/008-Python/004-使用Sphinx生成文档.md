## 使用Sphinx生成文档
1. [简介](#简介 "简介")
1. [安装](#安装 "安装")
1. [使用](#使用 "使用")

### 简介  
`Sphinx`是由`Pocoo Team`这个团队所做的一个文档工具。  
`Sphinx`的用户群很多, 如`Python、OpenCV、Tornado`的文档就是使用它生成的.  
如果要看更多的话可以看下http://sphinx-doc.org/examples.html这里, 很多项目都是它作为文档支持的.  

`Sphinx`的文档是用`reStructedText`所写的,主要是由`docutils`这个作为底层驱动渲染的, 对比`markdown, reStructedText`好像是复杂些.    
当然了, 如果直接看`github`中的文档, 它这两个都支持在线渲染.  

### 安装
基本`Python`安装方法, 下载地址:
https://pypi.python.org/pypi/Sphinx
 ```
python setup.py install
```
即可, 如果遇到依赖包, 一并下载下来再安装.
如果已经安装了`pip, easy_install`,可直接使用以下命令安装则可:
```
pip install -U Sphinx
```

### 使用
在项目文件夹中,执行以下命令:
```
sphinx-quickstart
```
接下来，按提示完成就会生成一系列初始文件.  
`sphinx`的文档以`rst`结尾，在编写完文档后，使用以下命令则可以生成最终的文档.  
```
make html
```
在`_build/html/index.html`中就可以查看效果了  
