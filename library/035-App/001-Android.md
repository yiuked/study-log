### 1、安卓API怎么选？


Android Studio 右边只显示gradle的几个数据
> Settle》Experimental》Gradle》Configure all Gradle tasks during Gradle Sync(this can make Gradle Sync slower) 把这一栏选上就行了

```


dependencies {
# 新创建拉activity默认会引用 activity:1.8.0的库，该库要求JAVA 61 既JAVA17版本，如果你用的# JAVA1.8，会得到这么一个错误“Unsupported class file major version 61”，你可以升级
# JAVA17或者降级引用的库

//    implementation 'androidx.appcompat:appcompat:1.7.0'  
//    implementation 'com.google.android.material:material:1.12.0'  
//    implementation 'androidx.activity:activity:1.8.0'  
//    implementation 'androidx.constraintlayout:constraintlayout:2.1.4'
	...
	implementation 'androidx.appcompat:appcompat:1.2.0'  
	implementation 'com.google.android.material:material:1.4.0'  
	implementation 'androidx.activity:activity:1.2.0'  
	implementation 'androidx.constraintlayout:constraintlayout:2.1.0'
	...
}
```
### **Major Version 和 Java 版本对应关系**

每个 Java 版本都有一个对应的 major version，它是 `.class` 文件的一个字段，表示编译该文件时使用的 Java 版本。这个版本信息帮助 Java 虚拟机（JVM）和其他工具识别和处理 `.class` 文件。。以下是常见 Java 版本和其对应的 major version：

- **Java 1.0**: Major Version 45
- **Java 1.1**: Major Version 45
- **Java 1.2**: Major Version 46
- **Java 1.3**: Major Version 47
- **Java 1.4**: Major Version 48
- **Java 5**: Major Version 49
- **Java 6**: Major Version 50
- **Java 7**: Major Version 51
- **Java 8**: Major Version 52
- **Java 9**: Major Version 53
- **Java 10**: Major Version 54
- **Java 11**: Major Version 55
- **Java 12**: Major Version 56
- **Java 13**: Major Version 57
- **Java 14**: Major Version 58
- **Java 15**: Major Version 59
- **Java 16**: Major Version 60
- **Java 17**: Major Version 61