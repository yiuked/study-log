#### 安装  
下载地址:http://www.sublimetext.com/  

#### 插件下载
package control  
https://packagecontrol.io/   

#### 配置  
1. 显示左侧文件栏  
你直接打开`sublime text`程序，然后点击`file->open folder`打开你要显示的目录就行.  
2. 显示小菜单导航  
`View ->Side Bar ->Show Side Bar`  
3. 添加删除空白行
`ctrl+shift+p`  或者在 `preferences` 的 `package controll` 里 搜索 `install package`
打开安装面板后，搜索  
`DeleteBlankLines`  
安装成功后，在 `edit->line` 就能看到删除空白行的选项了.  


#### 扩展
##### 1.运行PHP程序
1. 将php添加到环境变量中  
2. 打开`sublime->tools->build system->new build system`  
写入以下内容:
```
{
    "cmd": ["php", "$file"],
    "file_regex": "php$",
    "selector": "source.php"
}
```
保存到默认路径：`php.sublie-build`  
3. 打开php文件，按ctrl+b 运行

##### 2.整合xdebug
安装`xdebug client`注意，是带`client`的  
要使用`Xdebug`必须将要调度的内容保存为项目  
然后设置项目文件  
```
{
	"folders":
	[
		{
			"path": "/Users/apple/Documents/httpd/"
		}
	],
	"settings":
  	{
	    "xdebug": {
	  		"path_mapping": {},   
	  		"url": "http://127.0.0.1/index.php",
	  		"super_globals": true,
	  		"close_on_stop": true,
	  		"port": 9000   
	    }
  	}
}
```
然后配置`firefox`的`easy debug`,在`sublime` 的`tools`里可以看到`Xdebug`选项。  
