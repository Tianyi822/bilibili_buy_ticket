# B站会员购抢票脚本

## 环境
**python3.10**

## 需要安装的包
```pip install pytest-playwright```
```pip install schedule```

## 预备工作
在命令行中执行以下命令
```playwright install```

这个命令会下载三个浏览器，分别是 Chrome，Firefox 和 WebKit，如果没有特别需求，直接安装 webkit 即可
```playwright install webkit```

国网下载速度会有点慢，自行找办法解决

## 脚本使用教程

config_component 文件夹不要动，没什么需要改的

进入 comic_con 文件夹，按照以下步骤进行操作：
1. 进入 robot.ini 文件，`start_time` 配置修改为开票时间，`process_num` 设置为你需要同时抢的票数，sleep_time 不要动
2. 进入 ticket_config.ini 文件，这个文件我已经配置好，不需要修改，如果修改请按照我给的模板进行修改，`url` 配置为开票页面，`date` 为你网页上的场次选项，`value` 为价格选项，自行改动的话一定不要有错字，要不然小本会失效，空格也不要少不要多！！！
3. 进入 cookie.json 文件，将你的 cookie 数据粘贴进去，获取 cookie 数据方式下面会介绍
4. 进入 run.py 文件，将代码 `ticket_config = Config("comic_con/ticket_config.ini").get_content("beijing_comic_con")` 中的 `beijing_comic_con` 修改为 `bilibili_world` 即刚才在 `ticket_config.ini` 配置文件中方括号括起来的标题
5. 执行 run.py 文件即可

## cookie 数据获取方式

查看这篇博客教程即可（不是我写的，但亲测可用）：https://blog.csdn.net/u010741500/article/details/129455691
cookie-Editor 工具地址：https://chrome.google.com/webstore/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm
**需要科学上网，自行解决**