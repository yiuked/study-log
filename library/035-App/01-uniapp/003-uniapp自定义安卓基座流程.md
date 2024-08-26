#### 1、创建应用
前往：https://dev.dcloud.net.cn/pages/app/list 创建uniapp应用，创建成功后:
##### 1.1 在 `/manifest.json` 文件中个性appid:
```json
{
    "name" : "MX_shop",
    "appid" : "__UNI__CCABC***",
```
##### 1.2 创建安卓打包证书
```shell
# 生成keystore文件
keytool -genkey -v -keystore abc.keystore -alias abc -keyalg RSA -keysize 2048 -validity 100000

# 转成PKCS12密钥
keytool -importkeystore -srckeystore cihai_shop.keystore -destkeystore cihai_shop.keystore -deststoretype pkcs12

# 计算sha1、sha2的值
keytool -list -v -keystore abc.keystore -alias abc
```
获得sha1和sha2的值后，在以下路径中创建平台安卓平台信息：
```
应用管理 》我的应用 》各平台信息 》新增
```
##### 1.3 获得离线打包key
```
应用管理 》我的应用 》各平台信息 》创建离线打包Key
```

#### 2、生成打包资源
```
菜单栏 》发行 》原生APP-本地打包 》生成本地APP打包资源
```

#### 3、下载SDK
下载地址：https://nativesupport.dcloud.net.cn/AppDocs/download/android.html
一定要下载和你当前使用的HbuilderX版本一致的

##### 4、配置项目
##### 4.1、修改build.gradle
文件路径：app/build.gradle
```kotlin
defaultConfig {  
    applicationId "com.example.app1" // 修改点1：应用包名  
    minSdkVersion 21  
    targetSdkVersion 28  
    versionCode 1  
    versionName "1.0"  
    multiDexEnabled true  
    ndk {  
        abiFilters 'x86', 'armeabi-v7a', 'arm64-v8a'  
    }  
    manifestPlaceholders = [  
            "apk.applicationId"     : "com.example.app1",  // 修改点2：应用包名  
    ]  
    compileOptions {  
        sourceCompatibility JavaVersion.VERSION_1_8  
        targetCompatibility JavaVersion.VERSION_1_8  
    }  
}  
signingConfigs {  
    config {  
        keyAlias 'example'                   // 修改点3：证书别名  
        keyPassword '123456'                 // 修改点4：证书密码  
        storeFile file('example.keystore')   // 修改点5：证书文件  
        storePassword '123456'               // 修改点6：存储密码  
        v1SigningEnabled true  
        v2SigningEnabled true  
    }  
}
```

##### 4.2 修改AndroidManifest.xml
文件中的配置信息会被打包到基座文件中
文件路径：app/src/main/AndroidManifest.xml
```xml

<meta-data  
    android:name="WX_SECRET"  
    android:value="34c6**********cf" />  
<meta-data  
    android:name="WX_APPID"  
    android:value="wx********ce" />  
<!-- 微信分享 配置begin -->    
<activity  
    android:name="com.example.shop.wxapi.WXEntryActivity"  
    android:exported="true"  
    android:label="@string/app_name"  
    android:launchMode="singleTop">  
    <intent-filter>        
	    <action android:name="android.intent.action.VIEW" />
        <category android:name="android.intent.category.DEFAULT" />  
        <data android:scheme="wx********ce" />  
    </intent-filter>
</activity>  
<!-- 微信分享 配置 end -->  
<!-- 微信支付配置 start -->
<activity  
    android:name="com.example.shop.wxapi.WXPayEntryActivity"  
    android:exported="true"  
    android:launchMode="singleTop" />
...
<meta-data  
    android:name="dcloud_appkey"  
    android:value="**********" />
```

##### 4.3、修改 dcloud_control.xml
文件路径：app/src/main/assets/data/dcloud_control.xml
```xml
<apps>  
    <app appid="__UNI__XXXX" appver=""/>  
</apps>
```

##### 4.4、更新图标与启动图
```
ls app/src/main/res/drawable-xxhdpi
icon.png      # 图标
push.png      # 推送图标
splash.png    # 启动图
```

##### 4.5、修改APP名称
文件路径：app/src/main/res/values/strings.xml
```xml
<hbuilder debug="true" syncDebug="true">  
<apps>  
    <app appid="__UNI__xxx" appver=""/>  
</apps>  
</hbuilder>
```
https://ask.dcloud.net.cn/article/35482

#### 5、准备打包文件
HuiderX中打包好的资源包，一般路径为：
```
unpackage/resources/__UNI__B05E216/www
```
复制到安卓项目中，路径为：
```shell
app/src/main/assets/apps/__UNI__XXX/www
```


## 签名生成工具

用于获取安装到手机的第三方应用签名的apk包。点击下载 [签名生成工具](https://res.wx.qq.com/wxdoc/dist/assets/media/Gen_Signature_Android.e481f889.zip)