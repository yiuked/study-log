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