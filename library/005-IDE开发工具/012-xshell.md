- Xshell、Xftp 5、6 解决“要继续使用此程序,您必须应用最新的更新或使用新版本

修改安装目录下的nslicense.dll

1. 用二进制编辑器（UltraEdit、notepad++的HEX-Editor插件）打开Xshell/Xftp安装目录下的nslicense.dll
2. 搜索
`7F 0C 81 F9 80 33 E1 01 0F 86 80`
替换为：
`7F 0C 81 F9 80 33 E1 01 0F 83 80`
3. 保存退出即可

注：直接打开nslincense.dll可能没有编辑权限，可以copy一份到其他地方，然后进行修改，再将修改后的dll文件替换掉Xshell、Xftp安装目录下的dll

本文适用于Xsehll、Xftp 5，也适用于Xshell、Xftp 6，5和6的区别仅仅在于：
版本5的十六进制串为：`7F 0C 81 F9 80 33 E1 01 0F 86 80`，
版本6的十六进制串为：`7F 0C 81 F9 80 33 E1 01 0F 86 81`，但不影响。