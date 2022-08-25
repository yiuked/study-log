https://dtm.pub/guide/why.html

```
([0-9a-z]+)\s+([0-9a-z]+)\s=\s([0-9]+);([^/]+)(.*)\n
$2 $1 $5\n



@doc "发布二手商品"  
@handler PublishUsed  
post PublishUsed(PublishUsedReq) returns(UsedResp);  
@doc "取消二手商品寄售"

# 将post首字母小写
post ([A-Za-z]{1})
post \L$1