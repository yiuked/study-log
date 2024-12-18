
服务端代码
```go
func (a *DeviceApi) GetRunDeviceAttribute(c *gin.Context) {  
   c.Writer.Header().Set("Content-Type", "text/event-stream")  
   c.Writer.Header().Set("Cache-Control", "no-cache")  
   c.Writer.Header().Set("Connection", "keep-alive")  
  
   var once sync.Once  
   deviceId := c.Query("deviceId")  
   employeeId := utils2.GetEmployeeId(c)  
   ident := fmt.Sprintf("sse:device:state:%s:%d", deviceId, employeeId)  
  
   currentChan := make(chan []byte)  
  
   cleanUp := func() {  
      once.Do(func() {  
         close(currentChan)  
         delete(global.SSE, ident)  
         fmt.Println("清理资源，关闭通道")  
      })  
   }  
   defer cleanUp()  
  
   // 确保上一个通道被关闭  
   if prevChan, ok := global.SSE[ident]; ok {  
      close(prevChan)  
      delete(global.SSE, ident)  
   }  
  
   // 首次从redis获取数据  
   prefix := fmt.Sprintf("sse:device:state:%s", deviceId)  
   if global.GvaRedis != nil {  
      msg := global.GvaRedis.Get(context.Background(), prefix).Val()  
      if msg != "" {  
         msgStr := fmt.Sprintf("data:%s\n\n", msg)  
         c.Writer.Write([]byte(msgStr))  
         c.Writer.Flush()  
      } else {  
         c.Writer.Write([]byte("data:\n\n"))  
         c.Writer.Flush()  
      }  
   }  
  
   global.SSE[ident] = currentChan  
   timeoutDuration := 120 * time.Second  
   timer := time.NewTimer(timeoutDuration)  
  
   for {  
      select {  
      case data := <-currentChan: // 从通道中读取数据  
         msgStr := fmt.Sprintf("data:%s\n\n", data)  
         c.Writer.Write([]byte(msgStr))  
         c.Writer.Flush()  
  
         if !timer.Stop() {  
            <-timer.C  
         }  
         timer.Reset(timeoutDuration)  
      case <-timer.C:  
         global.GvaLog.Error("sse连接超时")  
         cleanUp()  
         return  
      case <-c.Request.Context().Done():  
         global.GvaLog.Error("sse客户端断开连接")  
         cleanUp()  
         return  
      }  
   }  
}
```
客户端代码：
```ts
function createEventSource(url, options, success, fail) {  
    // 中间件逻辑，例如检查 token 或添加全局参数  
    const params = new URLSearchParams(options).toString();  
    const token = localStorage.getItem('token')  
    const fullUrl = process.env.REACT_APP_BASE_URL + url + `?x-token=${token}&${params}`;  
  
    const eventSource = new EventSource(fullUrl);  
    eventSource.onmessage = (event) => {  
        console.log('Message from server:', event.data);  
        if (success) {  
            success(event.data)  
        }  
    };  
  
    // 监听自定义事件  
    eventSource.addEventListener("customEvent", function (event) {  
        console.log("接收到自定义事件:", event);  
    });  
  
    // 监听打开事件  
    eventSource.onopen = function () {  
        console.log("SSE 连接已打开");  
    };  
  
    eventSource.onerror = (error) => {  
        console.error('SSE Error:', error);  
        eventSource.close(); // 发生错误时关闭连接  
        if (fail) {  
            fail(error)  
        }  
    };  
  
    return eventSource;  
}  
  
export const getRunDeviceAttribute = (deviceId, callback, errorCallback) => {  
    // 创建 EventSource 连接  
    return createEventSource('/device/getRunDeviceAttribute', {  
        deviceId: deviceId,  
    }, callback, errorCallback);  
}
```

nginx配置
```shell
location / {
    proxy_pass   http://127.0.0.1:8611;

    # 超时设置，适配长连接
    proxy_connect_timeout 600;
    proxy_send_timeout 600;
    proxy_read_timeout 600;
    send_timeout 600;

    # 关键配置
    proxy_http_version 1.1;          # 强制使用 HTTP/1.1 支持持久连接
    proxy_buffering off;             # 禁用 Nginx 缓冲，实时传输数据
    proxy_cache off;                 # 禁用缓存
    chunked_transfer_encoding on;    # 支持分块传输
    add_header Cache-Control 'no-cache';  # 禁止客户端缓存
    proxy_set_header Connection '';  # 清空 Connection 头部，保持长连接
}
```