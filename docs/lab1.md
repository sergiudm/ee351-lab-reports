# Lab1实验报告：Raspberry Pi系统安装与SSH、VNC服务
## 一、实验介绍
本实验旨在指导用户如何使用SD卡格式化工具和官方的Raspberry Pi Imager软件进行树莓派操作系统的安装，并学习如何通过SSH和VNC实现对树莓派的远程管理。此过程包括了从准备SD卡到设置初始配置，再到实现安全的远程连接的所有步骤。

## 二、实验原理
- 系统安装：通过使用SD Formmater工具来格式化SD卡，确保其处于最佳状态以接收新的操作系统镜像；使用Raspberry Pi Imager或Win32DiskImager等工具将下载的操作系统镜像写入SD卡。
- SSH：Secure Shell是一种网络协议，它允许数据在两个网络实体之间加密传输，可以用于远程登录、执行命令等功能。
- VNC：Virtual Network Computing是一个图形桌面共享系统，它允许一台计算机远程控制另一台计算机。VNC Viewer是客户端软件，它能够连接到启用了VNC服务器的树莓派并显示其桌面环境。

## 三、实验步骤
- 使用SD Formmater格式化SD卡。
- 使用Raspberry Pi Imager选择并安装所需版本的操作系统。
- 在SD卡中编辑config.txt文件，根据显示器分辨率添加必要的启动参数。
- 硬件接线完成后插入SD卡，开启树莓派电源。
- 设置语言和地区信息，配置新密码（可选）。
- 开启SSH和VNC服务，获取树莓派IP地址。
- 使用Putty、MobaXterm或其他SSH客户端连接至树莓派。
- 使用VNC Viewer连接至树莓派桌面环境，或者通过安装xrdp服务使用Windows远程桌面连接。