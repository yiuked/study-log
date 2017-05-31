# Laravel中的API认证（Passport）
>1. [第一章节](#第一章节 "第一章节")
	1. [安装](#安装 "安装")
	1. [配置文件准备](#配置文件准备 "配置文件准备")
	1. [配置命令准备:](#配置命令准备: "配置命令准备:")
1. [第二章节](#第二章节 "第二章节")
	1. [authorization_code 模式](#authorization_code模式 "authorization_code 模式")

## 第一章节
### 安装
要使用`Passport`，首先，我们得安装安装:
```
composer require laravel/passport
```
### 配置文件准备
  1. 接下来，在配置文件 `config/app.php` 的 `providers` 数组中注册 `Passport` 服务提供者:
  ```
  ...
  Illuminate\Auth\AuthServiceProvider::class, //放在此命令后，否则会出现什么奇奇怪怪的问题
  Laravel\Passport\PassportServiceProvider::class,
  ...
  ```

  2. 添加 `Laravel\Passport\HasApiTokens` `trait` 到 `App\User` 模型:
  ```php
  namespace App;

  use Laravel\Passport\HasApiTokens;
  use Illuminate\Notifications\Notifiable;
  use Illuminate\Foundation\Auth\User as Authenticatable;

  class User extends Authenticatable
  {
      use HasApiTokens, Notifiable;
  }
  ```
  3. 在 `AuthServiceProvider` 的 `boot` 方法中调用 `Passport::routes` 方法:
  ```php
  namespace App\Providers;

  use Laravel\Passport\Passport;
  use Illuminate\Support\Facades\Gate;
  use Illuminate\Foundation\Support\Providers\AuthServiceProvider as ServiceProvider;

  class AuthServiceProvider extends ServiceProvider
  {
      /**
       * The policy mappings for the application.
       *
       * @var array
       */
      protected $policies = [
          'App\Model' => 'App\Policies\ModelPolicy',
      ];

      /**
       * Register any authentication / authorization services.
       *
       * @return void
       */
      public function boot()
      {
          $this->registerPolicies();

          Passport::routes();
      }
  }
  ```
  4. 在配置文件 `config/auth.php` 中，需要设置 `api` 认证 `guard` 的 `driver` 选项为 `passport`.
  ```php
  'guards' => [
      'web' => [
          'driver' => 'session',
          'provider' => 'users',
      ],

      'api' => [
          'driver' => 'passport',
          'provider' => 'users',
      ],
  ],
  ```

### 配置命令准备:
```
php artisan migrate               # 生成Passport数据表

php artisan passport:install      
# 该命令相当于执行以下三个个命令，
# php artisan passport:keys         // 生成 Passport 需要的加密 keys 文件存储在 /storage/ 目录下
# php artisan passport:client --password // 生成 `personal_access_client` 两种客户端类型的client_id与secret
# php artisan passport:client --personal // 生成 `password_client`两种客户端类型的client_id与secret

# 如果你是想测试 授权码模式（authorization code），那么，执行下面这个命令，来成生一个client_id与secret是必不可少的.
php artisan passport:client       # 根据向导生成用户的 client ID 和 secret（仅用于开发环境下）
```

`Passport` 默认注册了以下路由.
```
| POST     | oauth/authorize                         | \Laravel\Passport\Http\Controllers\ApproveAuthorizationController@approve  | web,auth     |
| GET|HEAD | oauth/authorize                         | \Laravel\Passport\Http\Controllers\AuthorizationController@authorize       | web,auth     |
| DELETE   | oauth/authorize                         | \Laravel\Passport\Http\Controllers\DenyAuthorizationController@deny        | web,auth     |
| POST     | oauth/clients                           | \Laravel\Passport\Http\Controllers\ClientController@store                  | web,auth     |
| GET|HEAD | oauth/clients                           | \Laravel\Passport\Http\Controllers\ClientController@forUser                | web,auth     |
| DELETE   | oauth/clients/{client_id}               | \Laravel\Passport\Http\Controllers\ClientController@destroy                | web,auth     |
| PUT      | oauth/clients/{client_id}               | \Laravel\Passport\Http\Controllers\ClientController@update                 | web,auth     |
| GET|HEAD | oauth/personal-access-tokens            | \Laravel\Passport\Http\Controllers\PersonalAccessTokenController@forUser   | web,auth     |
| POST     | oauth/personal-access-tokens            | \Laravel\Passport\Http\Controllers\PersonalAccessTokenController@store     | web,auth     |
| DELETE   | oauth/personal-access-tokens/{token_id} | \Laravel\Passport\Http\Controllers\PersonalAccessTokenController@destroy   | web,auth     |
| GET|HEAD | oauth/scopes                            | \Laravel\Passport\Http\Controllers\ScopeController@all                     | web,auth     |
| POST     | oauth/token                             | \Laravel\Passport\Http\Controllers\AccessTokenController@issueToken        | throttle     |
| POST     | oauth/token/refresh                     | \Laravel\Passport\Http\Controllers\TransientTokenController@refresh        | web,auth     |
| GET|HEAD | oauth/tokens                            | \Laravel\Passport\Http\Controllers\AuthorizedAccessTokenController@forUser | web,auth     |
| DELETE   | oauth/tokens/{token_id}                 | \Laravel\Passport\Http\Controllers\AuthorizedAccessTokenController@destroy | web,auth     |
```
生成以下数据表:
```
oauth_access_tokens
oauth_auth_codes
oauth_clients
oauth_personal_access_clients
oauth_refresh_tokens
```

## 第二章节
在进行第二章节前，你必须搞清楚这些内容，`Passport`是一套基于`oauth2.0`的验证方式，它保留`oauth2.0`中的几种认证模式:
五、客户端的授权模式

客户端必须得到用户的授权（authorization grant），才能获得令牌（access token）。OAuth 2.0定义了四种授权方式。
>授权码模式（authorization code）  
>简化模式（implicit）  
>密码模式（resource owner password credentials）  
>客户端模式（client credentials）  

### 授权码模式 （authorization code）
该模式其实比较常见，我们在登录美团、滴滴等应用时，
可以选择第三方微信、QQ、支付宝等方式登录，授权过程会跳转到微信或者QQ等相应的应用上授权后再返回美团、滴滴等应用。
我在web.php中添加了以下代码，已便进行测试
```php
Route::get('/redirect', function () {
    $query = http_build_query([
        'client_id' => '4', # client_id并非user id,当我们在前面执行`php artisan passport:client`在`oauth_clients`中生成数据并取其id则可。
        'redirect_uri' => 'http://cike.app:8000/auth/callback', # 在`php artisan passport:client`执行此命令时，会要求用户输入此链接，请确保一至。
        'response_type' => 'code',# 固定值
        'scope' => '*',
    ]);

    return redirect('http://cike.app:8000/oauth/authorize?'.$query);
});
Route::get('/auth/callback', function (\Illuminate\Http\Request $request) {
    // 此处的code会存入认证服务器的oauth_auth_code表，第三方应用拿到code后，则可使用code向认证服务器申请token
    $http = new GuzzleHttp\Client;
    $response = $http->post('http://cike.app/oauth/token', [  # 我的环境是基于vagrant,服务器开放80端口，对外映射为8000，此处请求是服务器对自己发起，因此不需要添加8000端口。
        'form_params' => [
            'grant_type' => 'authorization_code', # 固定值
            'client_id' => '4', # 保持与前面的client_id一至
            'client_secret' => 'mG1fwkO5A2TXJxmGQk7UQ1IdvAGLRdiXQ4oEDgBq', `在`oauth_clients`中生成的secret值
            'redirect_uri' => 'http://cike.app:8000/auth/callback',
            'code' => $request->get('code'),
        ],
    ]);

    $token = json_decode((string) $response->getBody(), true);
    // 刷新token
    $http = new GuzzleHttp\Client;
    $response = $http->post('http://your-app.com/oauth/token', [
        'form_params' => [
            'grant_type' => 'refresh_token',
            'refresh_token' => $token->access_token,
            'client_id' => '4',
            'client_secret' => 'mG1fwkO5A2TXJxmGQk7UQ1IdvAGLRdiXQ4oEDgBq',
            'scope' => '',
        ],
    ]);
});
```
以上完整实列，亲测可以正常获取到token值。
> code 值消费一次后则失效。  
> 无论是code还是token，认证服务器上不会保留，真实数据，仅保留一通过加密后的字符串ID。  

### 密码模式（resource owner password credentials）  
当我们在开发自己

>简化模式（implicit）  
>客户端模式（client credentials）  
