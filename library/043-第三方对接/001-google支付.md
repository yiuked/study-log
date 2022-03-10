### 一 账户配置

#### console.cloud.google.com
1. 创建新项目
2. 在库中启用`google play android api deveploer`
3. 创建OAuth(注意填写域名与测试账号)
4. 创建凭证,选择OAuth客户端ID(注意填写域名)

####　google play console
1.设置->应用完整性->google cloud项目进行项目关联(项目创建后可能会延迟生效)
2.关联Oauth客户端ID

### 二 获取基础信息

1. 获取`code`,`code`永久保留

   ```
   https://accounts.google.com/o/oauth2/auth?scope=https://www.googleapis.com/auth/androidpublisher&response_type=code&access_type=offline&redirect_uri=https://example.com&client_id=192661117043-2o1g2s5vhtb24vnn4f4jg5s466fjafsef.apps.googleusercontent.com
   ```

   > 需要用开发者账号登录授权,授权成功后会回跳到`redirect_uri`地址,注意获取其中的`code`,`code`一旦获取到可作为配置文件进行保留
   >
   > 回跳地址如下:
   >
   > ```
   > https://applive.top/?code=4/0AX4XfWg4h9OQmKT6D-UHjPCMaGCeHCVOlCCi6SHxO-CXc1n3gsqEVabcdefg&scope=https://www.googleapis.com/auth/androidpublisher
   > ```
   >
   > 

2. 通过code获取refreshtoken与accesstoken

    ```
    ### 获取
    POST https://accounts.google.com/o/oauth2/token
    Content-Type: application/json
    
    {
      "grant_type": "authorization_code",
      "code": "4/0AX4XfWg4h9OQmKT6D-UHjPCMaGCeHCVOlCCi6SHxO-CXc1n3gsqEVabcdefg",
      "client_id": "192661117043-2o1g2s5vhtb24vnn4f4jg5s466fjafsef.apps.googleusercontent.com",
      "client_secret": "GOCSPX-abcedfg",
      "redirect_uri": "https://applive.top"
    }
    ### 返回
    {
      "access_token": "ya29.A0ARrdaM-FMv7iJwQffJtdaaiDYl7WLFhkUC-bjTgYR5FGuzLmhbUErE-WKDgweeQHIiD6cbQDV659S3-PM4XLXLYrh6QZ",
      "expires_in": 3599,
      "refresh_token": "1//0euzzZ8jG170ICgYIARAAGA4SNwF-L9IrRdEJUNlhlq0SVnovVLiQI74GAAOKyawM1VD",
      "scope": "https://www.googleapis.com/auth/androidpublisher",
      "token_type": "Bearer"
    }
    ```

### 三 集成

1. 功能实现(查询订单)

    ```
    ### 查询订单
    GET https://androidpublisher.googleapis.com/androidpublisher/v3/applications/{包名}/purchases/products/{产品id}/tokens/{消费token}?access_token={access_token}
    
    ```

