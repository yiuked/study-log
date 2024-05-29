```go
package main  
  
import webview "github.com/webview/webview_go"  
  
func main() {  
   // 创建一个新的WebView实例  
   debug := true  
   w := webview.New(debug)  
   defer w.Destroy()  
  
   // 设置窗口标题和尺寸  
   w.SetTitle("直播间")  
   w.SetSize(600, 1000, webview.HintNone)  
  
   // 加载指定的URL  
   w.Navigate("https://www.example.com")  
  
   // 运行WebView  
   w.Run()  
}
```

如果是Mac下打包windows程序，需要先安装 mingw-w64
```shell
brew install mingw-w64
CGO_ENABLED=1 CC=x86_64-w64-mingw32-gcc CXX=x86_64-w64-mingw32-g++ GOOS=windows GOARCH=amd64 go build -ldflags="-H windowsgui" -o test.exe main.go
```

`-ldflags="-H windowsgui"` 不加这项，打包时会出现一个控制台窗口


mac下如果有控制台窗口：
```shell
go install github.com/machinebox/appify@latest
appify your_app your_app_name
```