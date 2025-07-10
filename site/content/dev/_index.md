---
title: "自研插件"
date: 2019-12-10T13:07:14+08:00
draft: false
weight: 3
featured_image: '/images/bg_qq_sponsor.png'
---


服务器使用自定义插件 **OrzMC** 来辅助维护服务器运营，非通用插件

---

插件包含的功能如下:

1. 新手进入服务器后会自动获得一本新手指南，并打开阅读

1. 使用 **/guide** 命令也可以打开新手指南
    
1. 使用 **/tpbow** 玩家可获得传送弓, 传送弓可以传送玩家到箭落地的位置

1. 禁用了非可驯服实体的传送，防止 **/tp @e ~ ~ ~** 类似命令的误操作

    下面是未被禁止传送的实体：
    
    - 末影人(EnderMan)
    - 盔甲架(ArmorStand)
    - 潜影盒(Shulker)
    
1. 禁用了TNT, 并且有玩家放置或点燃TNT时会全服公告，并在放置时发消息到玩家群

1. QQ群上下线提醒功能，使用了 **[NapCatQQ][NapCatQQ]** 服务实现

1. QQBot登录：[QQBot](https://qqbot.jokerhub.cn)
1. 国内MCS管理面板：[MCSManager][MCSManager]


[NapCatQQ]: <https://napcat.napneko.icu/>
[go-cqhttp]: <https://docs.go-cqhttp.org/>
[MCSManager]: <http://mcs.jokerhub.cn:23333/>
