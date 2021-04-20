```
POST http://example.com/upload
Content-Type: multipart/form-data; boundary=WebAppBoundary

Name
--WebAppBoundary
Content-Disposition: form-data; name="data"; filename="test.jpg"
Content-Type: multipart/form-data

<D:\v\test.jpg
--WebAppBoundary--
```

## Content-type

内容类型，一般是指网页中存在的Content-Type，用于定义网络文件的类型和网页的编码，决定浏览器将以什么形式、什么编码读取这个文件。
文件扩展名与 Content-type 的对应关系，参见 [http://tool.oschina.net/commons]

## Content-Disposition

Content-disposition 是 MIME 协议的扩展，MIME 协议指示 MIME 用户代理如何显示附加的文件。
当 IE 浏览器接收到头时，它会激活文件下载对话框，它的文件名框自动填充了头中指定的文件名。
Content-Disposition 就是当用户想把请求所得的内容存为一个文件的时候提供一个默认的文件名。

示例：

```
Content-Disposition: inline
Content-Disposition: attachment
Content-Disposition: attachment; filename="filename.jpg"
```