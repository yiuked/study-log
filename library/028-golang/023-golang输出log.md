日志输出定位
```
var gormSourceDir string  
  
func init() {  
   _, file, _, _ := runtime.Caller(0)  
   // compatible solution to get gorm source directory with various operating systems  
   gormSourceDir = regexp.MustCompile(`utils.utils\.go`).ReplaceAllString(file, "")  
}

// FileWithLineNum return the file name and line number of the current filefunc FileWithLineNum() string {  
   // the second caller usually from gorm internal, so set i start from 2  
   for i := 2; i < 15; i++ {  
      _, file, line, ok := runtime.Caller(i)  
      if ok && (!strings.HasPrefix(file, gormSourceDir) || strings.HasSuffix(file, "_test.go")) {  
         return file + ":" + strconv.FormatInt(int64(line), 10)  
      }  
   }  
  
   return ""  
}

log.Printf("%v %s%",FileWithLineNum(),"abc")
```