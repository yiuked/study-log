console.cloud.google.com
1.创建项目 93625
2.启用google play android api deveploer
3.创建OAuth(域名+测试账号)
4.创建凭证(OAuth客户端ID+域名)

google play console
1.设置->应用完整性->google cloud项目->(项目创建后可能会延迟生效)
2.关联Oauth客户端ID


1.获取code,code永久保留
https://accounts.google.com/o/oauth2/auth?scope=https://www.googleapis.com/auth/androidpublisher&response_type=code&access_type=offline&redirect_uri=https://applive.top&client_id=152661117043-2o1g2s5vhtb24vnn4f4jg5s466fjjfsg.apps.googleusercontent.com
用开发者账号登录授权

2.回跳地址(通过回调地址获取到code)
https://applive.top/?code=4/0AX4XfWg4h9OQmKT6D-UHjPCMaGCeHCVOlCCi6SHxO-CXc1n3gsqEVPJFrqUylgaTSkBQXA&scope=https://www.googleapis.com/auth/androidpublisher

4.通过code获取refreshtoken与accesstoken
### 获取token
POST https://accounts.google.com/o/oauth2/token
Content-Type: application/json

{
  "grant_type": "authorization_code",
  "code": "4/0AX4XfWigGeVNiLIKjwDLf6-QjxlZy4H7S9oEiibCv5T6WVHhPIv8neMeJmlUHOW37k2HwQ",
  "client_id": "33696707861-hb1ma1jrv4ufj98dp6rgm8vb22dkj8mo.apps.googleusercontent.com",
  "client_secret": "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",
  "redirect_uri": "https://applive.top"
}

5.


https://applive.top/?code=4/0AX4XfWiWx9GStO4mhiz3KMyVmVv-5s7Q-S4eOzSzQCnOubAFTd6gEcnbqSswzY0Hi_HtjQ&scope=https://www.googleapis.com/auth/androidpublisher