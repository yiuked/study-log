## 使用amWiki构建自己的文档系统

### 安装 amWiki
amWiki 可以同时在 Atom 编辑器和 nodejs npm 的命令行两个平台工作，两个平台的工作相互独立，但所创建的文库却可以相互共用  
（PS：对这两个平台的依赖都是编辑需求而不是服务器需求，amWiki 创建的文库是纯静态 html，可以布置到任意服务器）

#### 作为 Atom 插件安装
1. 下载 Github 开源文本编辑器 [Atom](https://atom.io/ "Atom官网")，并安装  
2. 安装 Atom 插件 amWiki，并在完成后重启 Atom
    - 前往 Github 的 [amWiki版本发布页](https://github.com/TevinLi/amWiki/releases) 下载最新版压缩包，解压到 C:\Users\Administrator\.atom\packages，并将文件夹名 `amWiki-1.x.x` 改为 `amWiki`
    - 或者，Atom 菜单，File -> Setting -> Install -> 搜索 `amWiki` -> 找到 amWiki 并  Install
    - 或者，在 cmd 或终端中命令：`apm install amWiki`（_第三字母 W 大写_）
3. 在 Atom 菜单，File -> `Add Project Folder` 添加一个项目文件夹
4. 在此文件夹下创建一个名为 `config.json` 的文件
5. 在 Atom 菜单，amWiki轻文库 -> 通过“config.json”创建新文库

#### 作为 nodejs 全局模块安装
1. 下载 [nodejs](https://nodejs.org/) 并安装
2. 执行命令： `npm install -g amwiki`（_第三字母 w 小写_）
3. cd 到某个文件夹，通过命令 `amwiki create` 创建文库
4. 通过命令 `amwiki help` 查看帮助
--------------------------------------------------------------------------------
> 以上是amWiki作者官方的安装说明，github地址:https://github.com/TevinLi/amWiki
