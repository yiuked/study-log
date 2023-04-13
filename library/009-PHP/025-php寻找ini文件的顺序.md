### PHP5按照以下顺序依次查找PHP.ini：
1. PHPIniDir (Apache 2 module only)
2. 注册表键值：HKEY_LOCAL_MACHINE—SOFTWARE—PHPIniFilePath
3. 环境变量:%PHPRC%
4. PHP5的目录 (for CLI), 或者web服务器目录(for SAPI modules)
5. Windows目录(C:\windows or C:\winnt) 
所以如果是Apache + PHP5的话可以使用 PHPIniDir 指定php5的配置文件php.ini的路径。

如在httpd.conf：
### 以apache的模块方式运行php
LoadModule php4_module /apache/php/sapi/php4apache.dll
PHPINIDir /apache/php/php.ini
wamp 装好无法访问phpmyadmin:
