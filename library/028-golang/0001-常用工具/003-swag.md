生成文档工具

``` go
type CustomerID struct {  
   ID uint `json:"id" form:"id" binding:"required"` // 用户ID  
}

// FindCustomer 用id查询Customer  
// @Tags Customer  
// @Summary 用id查询Customer  
// @Security ApiKeyAuth  
// @accept application/json  
// @Produce application/json  
// @Param data body coreReq.CustomerID true "用id查询Customer"  
// @Success 200 {object} response.Response{data=model.Customer}  "详情"  
// @Router /customer/findCustomer [get]  
func (customerApi *CustomerApi) FindCustomer(c *gin.Context) {  
   var customer coreReq.CustomerID  
   err := c.ShouldBindQuery(&customer)  
   if err != nil {  
      response.FailWithMessage(err.Error(), c)  
      return  
   }  
   if recustomer, err := customerService.GetCustomer(customer.ID); err != nil {  
      global.GVA_LOG.Error("查询失败!", zap.Error(err))  
      xer, boo := err.(*xerr.XError)  
      if !boo {  
         response.FailWithMessage("查询失败", c)  
      } else {  
         response.FailWithMessage(fmt.Sprintf("查询失败：%s", xer.OutErr), c)  
      }  
   } else {  
      response.OkWithData(gin.H{"recustomer": recustomer}, c)  
   }  
}
```

有时候有些类型不好生成如`database.SqlNullString`、`datatypes.JSON` 可以通过以下方法处理
`.swaggo`:

```
// Replace all NullInt64 with int
replace database/sql.NullInt64 int

// Don't include any fields of type database/sql.NullString in the swagger docs
skip    database/sql.NullString
```
示例
```
// 替换类型  
replace preorder/admin/server/model/core/response.DinnerJson preorder/common/model.Dinner
```

忽略某个字段
```
type Account struct {
    ID   string    `json:"id"`
    Name string     `json:"name"`
    Ignored int     `swaggerignore:"true"`
}
```