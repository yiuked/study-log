### KMS命令激活Office2016方法
1. 首先查看Office2016安装目录在哪里，如果是默认安装，没有修改路径，是在C:\Program Files\Microsoft Office\Office16目录下，64位系统装32位office路径是C:\Program Files (x86)\Microsoft Office\Office16，具体路径还得自行查看；

2. 接着右键点击开始图标，选择【Windows PowerShell(管理员)】，或者【命令提示符(管理员)】；

3. 打开命令提示符，复制这个命令，在命令窗口鼠标右键，会自动粘贴，按回车进入office2016安装路径，如果你不是在这个目录，需手动修改，目录错误，后面就无法执行激活操作；

4. 接着复制下面这个命令，在命令窗口鼠标右键自动粘贴命令，按回车执行，安装office2016专业增强版密钥，如果提示无法找到脚本文件，说明第3步打开的路径错误；

   cscript ospp.vbs /inpkey:XQNVK-8JYDB-WJ9W3-YJ8YR-WFG99

   【Office Professional Plus 2016：XQNVK-8JYDB-WJ9W3-YJ8YR-WFG99】

   【Office Standard 2016：JNRGM-WHDWX-FJJG3-K47QV-DRTFM】

5. 接着复制这个命令，右键自动粘贴，按回车执行，设置kms服务器；

   cscript ospp.vbs /sethst:kms.03k.org
   
6. 最后执行这个命令，按回车激活office2016；

   cscript ospp.vbs /act
   
7. 如果要查询office2016激活状态，执行这个命令。

   cscript ospp.vbs /dstatus