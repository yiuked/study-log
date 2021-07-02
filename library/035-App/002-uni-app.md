### 一、开发环境

* HBuilderX：[官方IDE下载地址](https://www.dcloud.io/hbuilderx.html)

### 二、运行调试

* 真机运行：连接手机，开启USB调试，进入uni-app项目，点击工具栏的运行 -> 真机运行 -> 选择运行的设备，即可在该设备里面体验uni-app。

  ![image-20210702144753283](../../../images/typora/image-20210702144753283.png)

  > 如手机无法识别，请点击菜单运行-运行到手机或模拟器-真机运行常见故障排查指南。 注意目前开发App也需要安装微信开发者工具。

### 三、正式打包

#### 1. 云端打包

在HBuilderX工具栏，点击发行，选择原生app-云端打包，如下图：

![image-20210702144902424](../../../images/typora/image-20210702144902424.png)

https://ask.dcloud.net.cn/article/37979

#### 2. Xcode与Android Studio打包

在 HBuilderX 发行菜单里找到本地打包菜单，生成离线打包资源，然后参考离线打包文档操作：https://nativesupport.dcloud.net.cn/AppDocs/README。

离线打包需要环境：

* Android Studio / Xcode

* App离线SDK

* [申请Appkey](https://nativesupport.dcloud.net.cn/AppDocs/usesdk/appkey)



ERROR: Cannot query the value of this provider because it has no value available.



ERROR: This version of the Android Support plugin for IntelliJ IDEA (or Android Studio) cannot open this project, please retry with version 4.1 or newer.
