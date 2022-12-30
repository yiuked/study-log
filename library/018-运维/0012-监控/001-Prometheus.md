### 整合 gin
```go
package middleware  
  
import (  
   "github.com/gin-gonic/gin"  
   "github.com/prometheus/client_golang/prometheus")  
  
var httpRequestCount = prometheus.NewCounterVec(  
   prometheus.CounterOpts{  
      Name: "http_request_count",  
      Help: "http request count",  
   },  
   []string{"endpoint"},  
)  
  
func init() {  
   prometheus.MustRegister(httpRequestCount)  
}  
  
func Prometheus() gin.HandlerFunc {  
   return func(c *gin.Context) {  
      httpRequestCount.WithLabelValues(c.Request.RequestURI).Inc()  
      c.Next()  
   }  
}
```

gin 中加入
```go
Router.GET("/metrics", func(c *gin.Context) {  
   promhttp.Handler().ServeHTTP(c.Writer, c.Request)  
})  
Router.Use(middleware.Prometheus())
```