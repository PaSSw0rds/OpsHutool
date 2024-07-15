# 运维基线
在做运维的时候，经常会需要做漏扫和等保合规，目前有很多工具可以对服务器进行基线扫描，例如最著名的OpenSCAP，他是一个对服务器进行基线扫描的开源工具。
> OpenSCAP (OSCAP) is an open-source utility that can use a SCAP Security Guide (SSG) profile as a basis for testing security compliance. You can use the OSCAP utilities with Oracle Linux to automate compliance testing.

但遗憾的是，目前上还没有出现扫描后并自动修复的工具，基本上都是人工修改，或者仅支持服务器刚部署完成的时候使用（因为长时无人维护的服务器可能配置不一，不适用单体的修改）。
这个项目的命名参考了 JAVA 著名开源工具类项目 [Hutool](https://doc.hutool.cn/) ，希望帮助所有苦逼的运维和实施脱离苦海。

项目处于全新开发阶段，由于我的个人主要使用的语言是JAVA，对于Python的开发并不熟悉，可能会有非常多的BUG，**请只在虚拟机上测试**。也欢迎有想要实现的功能给我留言。


## 使用方法

克隆项目，执行 `setup/startup.sh` 。

## 项目架构
```
.
├─setup						# 项目主目录
│  └─rpm					# 必要的安装依赖
└─venv						# ansible 项目目录（暂无使用）
    ├─env					# ansible 环境
    ├─inventory				# ansible 清单
    └─project				# ansible 任务
```

## 更新日志
· 2024-07-15    编写README.md
