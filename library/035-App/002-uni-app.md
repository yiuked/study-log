# uni-app

相关文档：
[离线打包教程](https://nativesupport.dcloud.net.cn/AppDocs/usesdk/appkey.html)
[微信开放平台创建移动应用获取签名](https://developers.weixin.qq.com/doc/oplatform/Downloads/Android_Resource.html)

### 一、开发环境

* HBuilderX：[官方IDE下载地址](https://www.dcloud.io/hbuilderx.html)

### 二、运行调试

* 真机运行：连接手机，开启USB调试，进入uni-app项目，点击工具栏的运行 -> 真机运行 -> 选择运行的设备，即可在该设备里面体验uni-app。

  ![image-20210702144753283](../../../images/typora/image-20210702144753283.png)

  > 如手机无法识别，请点击菜单运行-运行到手机或模拟器-真机运行常见故障排查指南。 注意目前开发App也需要安装微信开发者工具。

### 三、正式打包

#### 1. 云端打包

在HBuilderX工具栏，点击发行，选择原生app-云端打包:

* 高峰期打包不时间不确定性
* HBuilderX 自身没带模拟器只能采用真机调试

https://ask.dcloud.net.cn/article/37979





#### 2.Android Studio打包

* 模拟器
* 随时可以打包，速度快



##### 2.1 安装

Android Studio http://www.android-studio.org/



在 HBuilderX 发行菜单里找到本地打包菜单，生成离线打包资源，然后参考离线打包文档操作：https://nativesupport.dcloud.net.cn/AppDocs/README。

离线打包需要环境：

* Android Studio / Xcode

  > http://www.android-studio.org/

* App离线SDK

  > https://nativesupport.dcloud.net.cn/AppDocs/usesdk/android

* [申请Appkey](https://nativesupport.dcloud.net.cn/AppDocs/usesdk/appkey)

  > https://nativesupport.dcloud.net.cn/AppDocs/usesdk/appkey
  

##### 3生成证书

```shell

# 生成keystore文件
keytool -genkey -v -keystore abc.keystore -alias abc -keyalg RSA -keysize 2048 -validity 100000

# 计算sha1值
keytool -list -v -keystore abc.keystore -alias abc

keytool -list -v -keystore cihai_mxsd.keystore -alias cihai_mxsd
```


- HBuilderX中标准真机运行基座使用的是DCloud申请HBuilder应用的AppID等信息，仅用于体验微信登录功能
- 配置参数需提交云端打包后才能生效，真机运行时请使用[自定义调试基座](https://ask.dcloud.net.cn/article/35115)


#### 微信登录
需要在开放平台创建移动应用
```js
uni.login({
	provider: 'weixin',
	onlyAuthorize: true,
```
onlyAuthorize 默认为 false,返回code,如果设置为true，必须前台传SECRET

### FAQ
1. Installed Build Tools revision 30.0.3 is corrupted. Remove and install again using the SDK Manager.
   > Languages&Frameworks > Android SDK > SDK Tools 中删除30.0.3重新安装一下

2. Uniapp默认的基座是使用的是unapp官方的appid和AppSecret，需要使用自己的重新打包基座。
3. 
4. 调用微信登录返回以下错误
```json
   {
   "errMsg":"login:fail 业务参数配置缺失,http://ask.dcloud.net.cn/article/282",
   "errCode":-7,
   "code":-7
   }
```
修改以下文件：app/src/main/AndroidManifest.xml，Oauth中的微信登录和分享用的都是以下配置
```xml
<!-- 微信分享 配置begin -->  
<meta-data  
    android:name="WX_SECRET"  
    android:value="xx" />  
<meta-data  
    android:name="WX_APPID"  
    android:value="xx" />
<activity  
    android:name="[改为applicationid,重要！！].wxapi.WXEntryActivity"  
    android:exported="true"  
    android:label="@string/app_name"  
    android:launchMode="singleTop">  
    <intent-filter>        <action android:name="android.intent.action.VIEW" />  
  
        <category android:name="android.intent.category.DEFAULT" />  
  
        <data android:scheme="wxfe66e9c99c84d0ce" />  
    </intent-filter></activity>    
```

5. 微信登录时自定义基座报以下错误
```json
	{
    "errMsg": "login:fail Unable to send",
    "errCode": -100,
    "code": -100,
    "innerCode": -3
}
```
找到 `app/src/main/java`目录下的`WXEntryActivity`和`WXPayEntryActivity`,包名路径要改成applicationid

6.  HbuilderX中，自定义基座存放的路径为 `unpackage/debug/anroid_debug.apk`，文件名和路径名不要改。
7. 支付宝接入BUG汇集：https://open.alipay.com/portal/forum/post/60501039
8. 支付宝接入错误查询：https://opensupport.alipay.com/support/diagnostic-tools/b3b501fd-a442-4dee-8b3f-e5f5edcc6d6e
















































ERROR: Cannot query the value of this provider because it has no value available.
ERROR: This version of the Android Support plugin for IntelliJ IDEA (or Android Studio) cannot open this project, please retry with version 4.1 or newer.
.\emulator.exe -avd test1 -dns-server 114.114.114.114
echo 1> /proc/sys/net/ipv6/conf/wlan0/disable_ipv6
