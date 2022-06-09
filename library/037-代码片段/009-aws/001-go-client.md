```go
func Connect() (*s3.S3, error) {  
  
   creds := credentials.NewStaticCredentials(viper.GetString("aws.access_key_id"), viper.GetString("aws.secret_access_key"), "")  
   _, err := creds.Get()  
   if err != nil {  
      log.Logger.Errorw("bad credentials", zap.Error(err))  
      return nil, err  
   }  
   cfg := aws.NewConfig().  
      WithRegion(viper.GetString("aws.bucket_region")).  
      WithCredentials(creds).  
      WithLogLevel(aws.LogDebugWithHTTPBody) // 打印HTTP日志  
   svc := s3.New(session.New(), cfg)  
  
   return svc, nil  
  
}
```