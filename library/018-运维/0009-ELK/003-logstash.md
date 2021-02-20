```
input{}, 
filter{},
output{}
```

## 输入

```
input{}
```



## 过滤器

- grok
- date
- mutate
- geoip
- json
- split
- useragent
- key-value
- ruby
- metrics



**grok**

Grok 是 Logstash 最重要的插件。你可以在 grok 里预定义好命名正则表达式，在稍后(grok参数或者其他正则表达式里)引用它。 

```
filter{
	grok {
		match => {
		// 127.0.0.1 - - [20/Oct/2020:23:45:57 +0800] "GET /EC/07/1B163A66812A5E98B1E117E8AD4AFA5EEAFB HTTP/1.1" 404 286
		"message" => "%{IPV4:ip} .* \[%{DATA:timestamp}\] \"%{WORD:method} %{URIPATHPARAM:request_uri} .*\/%{DATA:http_version}\" %{NUMBER:status_code} %{NUMBER:lenght}"
		}
	}
}
# 自定义正则，格式：(?<custom_feild>(.*)) 其中`<custom_feild>` 为字段，`(.*)`为字段对应的正则
.*\[(?<custom_feild>(.*))\].*
```

grok中如果有多咱日志类型，可以为match设置多个匹配，传递参数时需要传递一个包含偶数个数的数组，如下:

```
    grok {
        match => [
            "message","%{IPV4:ip} - \[%{DATA:timestamp}\] \"%{WORD:method} %{URIPATHPARAM:request_uri} HTTP\/%{DATA:http_version} %{NUMBER:status_code} %{NOTSPACE:duration} %{NUMBER:lenght}\" \"%{GREEDYDATA:agent}\" \"%{GREEDYDATA:error}\"",
            "message","\[%{DATA:timestmp}\] %{DATA:source} \[%{NOTSPACE:drution}\] \[%{BASE10NUM:rows}\] %{GREEDYDATA:sql}"
        ]
    }
```



[grom格式在线测试](https://www.5axxw.com/tools/v2/grok.html)

**date**

*date* 插件可以用来转换你的日志记录中的时间字符串，变成 `LogStash::Timestamp` 对象，然后转存到 `@timestamp` 字段里。**outputs/elasticsearch 中常用的 `%{+YYYY.MM.dd}` 这种写法必须读取 `@timestamp` 数据，所以一定不要直接删掉这个字段保留自己的字段，而是应该用 filters/date 转换后删除自己的字段！**

```
date {
	 match => ["timestamp", "dd/MMM/yyyy:HH:mm:ss Z"]
	 remove_field => [stimestamp] # 删除原字段
}
```



## 输出

```
output{
    elasticsearch{
        hosts => "http://localhost:9200"
        index => "logstash-apache"
    }
    stdout{}
}
```



## 启动

```
.\logstash -e "input{stdin{}} output{stdout{}}"
.\logstash -f ..\config\test.yml -t // 测试配置文件是否正确
```

