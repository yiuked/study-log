
创建Chrome扩展程序的React和TypeScript是一种结合了这两种技术的开发方法。下面是一些基本步骤：

1. 首先，确保您已经安装了Node.js和npm（Node包管理器）。

2. 使用Create React App工具创建一个新的React项目。您可以在终端中运行以下命令：
```
npx create-react-app my-extension --template typescript
```
这将创建一个名为"my-extension"的新文件夹，并在其中初始化一个React项目。

3. 进入项目文件夹：
```
cd my-extension
```

4. 更新manifest.json文件
```json
{
   "name": "my-extension",
   "description": "The power of React and TypeScript for building interactive Chrome extensions",
   "version": "1.0",
   "manifest_version": 3,
   "action": {
       "default_popup": "index.html",
       "default_title": "Open the popup"
   },
   "icons": {
       "16": "logo192.png",
       "48": "logo192.png",
       "128": "logo192.png"
   }
}
```
> 字段注解：
>- name：扩展程序的名称
>- description：扩展程序的描述
>- version：扩展程序的当前版本
>- manifest_version：我们项目中要使用的清单格式的版本
> - action：动作允许您自定义在Chrome工具栏上显示的按钮，这些按钮通常会触发一个带有扩展程序界面的弹出窗口。在我们的例子中，我们定义了我们希望我们的按钮启动一个带有我们的index.html内容的弹出窗口，该文件托管了我们的应用程序。
>- icons：扩展程序图标集合

5. 在项目文件夹中创建一个名为"public"的新文件夹。在该文件夹中，创建一个名为"manifest.json"的文件，用于描述您的扩展程序的配置和权限。您可以参考Chrome官方文档了解更多关于manifest.json的信息。

6. 在项目文件夹中，运行以下命令来构建您的扩展程序：
```
npm run build
```
这将在项目文件夹中创建一个"build"文件夹，其中包含了构建后的扩展程序文件。

7. 打开Chrome浏览器，进入扩展程序管理页面（chrome://extensions/）。

8. 在扩展程序管理页面的右上角，打开"开发者模式"。

9. 点击"加载已解压的扩展程序"，选择您的项目文件夹中的"build"文件夹。

10. 现在，您的扩展程序应该已经加载并可用了。

最后，如果需要发布到应用商店，需要注册开发账号，注册需要绑定信用卡，并支付$5。
注册地址：
https://chrome.google.com/webstore/devconsole/register?hl=zh-CN