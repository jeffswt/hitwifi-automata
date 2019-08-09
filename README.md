
# HITWiFi: Automata

![2B小姐姐赛高](./assets/banner.png)

后台自动连接哈工大校园网的脚本。

<del>威海校区表示极度舒适（自带自动连接功能）。</del>

如果你觉得好用请推荐给周围的人。

记得在页面右上角留颗 Star！务必！务必！务必！（逃

<del>Star 是我生活的动力 ↗</del>

## 功能

  - 显示当前网络连接状态（准实时更新）
  - 多语言支持（看起来tql）
  - 一键配置校园网账号
  - 一键连接工大校园网
  - 一键登出工大校园网（敢问谁会用这个功能）
  - 识别到账号退出自动重连校园网
  - 自动重连功能可暂停
  - 在非校园网环境下不贸然登录校园网
  - 多次登陆失败后自动暂停自动重连功能
  - **不明文存储密码！**
    **不明文存储密码！**
    **不明文存储密码！**
    <del>实名举报某 bzoj 不开 HTTPS 还明文传输密码</del>
    <del>你们俩不要笑；对，poj 和 hduoj，就是你们俩</del>
  - 2B 小姐姐赛高

## 安装

伸手党请看下一节（记得 star）↓

首先你需要有 [Python](https://www.python.org/downloads/)。

然后把需要的依赖装好就行了。

```bash
git clone https://github.com/jeffswt/hitwifi-automata.git
pip install -r requirements.txt
```

然后双击 `hitwa.pyw` 会提醒你选择语言、输入用户名密码，就开始自动连接啦！

当然之后你也可以在任务栏菜单里面更改设置。

也可以创建一个指向 `hitwa.pyw` 的快捷方式放到桌面上。

## 下载

到 [Release](https://github.com/jeffswt/hitwifi-automata/releases/latest) 里面下载最新版本 `hitwa.exe`。

配置用户名密码方式同上 ↑

直接点那个程序就行了，然后它在关机前就会自动连接校园网

## Todo

 - [x] 后台挂机，自动断线重连
 - [ ] 自动配置开机自启动
 - [ ] 适配移动端（不存在的
 - [ ] 直接要求加上无感认证，然后本项目自动终结（

## Contributing

Open to pull requests.

## License

Licensed under MIT License.
