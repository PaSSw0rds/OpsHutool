# 运维基线
在做运维的时候，经常会需要做漏扫和等保合规，目前有很多工具可以对服务器进行基线扫描，例如最著名的OpenSCAP，他是一个对服务器进行基线扫描的开源工具。
> OpenSCAP (OSCAP) is an open-source utility that can use a SCAP Security Guide (SSG) profile as a basis for testing security compliance. You can use the OSCAP utilities with Oracle Linux to automate compliance testing.

毫无疑问的是，OSCAP 是目前最好的基线扫描并提供修复建议和生成修复脚本的工具，本工具**不指望也不能够**能够替代该开源工具。本项目核心仅仅是为了自己偷懒，能在未来维护上保持服务器安全基线一致，减少人工的机械操作。

这个项目的命名参考了 JAVA 著名开源工具类项目 [Hutool](https://doc.hutool.cn/) ，希望帮助所有苦逼的运维和实施脱离苦海。

项目处于全新开发阶段，由于我的个人主要使用的语言是JAVA，对于Python的开发并不熟悉，可能会有非常多的BUG，**请只在虚拟机上测试**。也欢迎有想要实现的功能给我留言。

## 基线标准

1. 通用操作系统保护配置文件《Protection Profile for General Purpose Operating Systems》由美国国家信息保护技术中心（简称NIAP）撰写。 
   - https://commoncriteria.github.io/pp/operatingsystem/operatingsystem.html
   - https://github.com/commoncriteria/operatingsystem
2. SSG 基线《OSPP - Protection Profile for General Purpose Operating Systems》
   - https://static.open-scap.org/ssg-guides/ssg-rhel7-guide-ospp.html
   - https://static.open-scap.org/ssg-guides/ssg-fedora-guide-ospp.html
3. 《GB/T 28448-2019 信息安全技术 网络安全等级保护测评要求》
   - https://openstd.samr.gov.cn/bzgk/gb/newGbInfo?hcno=BAFB47E8874764186BDB7865E8344DAF
   - https://nic.usc.edu.cn/info/1107/1727.htm

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
- 2024-07-15    编写README.md
