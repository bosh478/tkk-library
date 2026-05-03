---
title: 电子数据司法鉴定实务_郭弘_第5章_Windows系统电子数据鉴定
type: concept
created: 2026-04-29
updated: 2026-04-29
tags: [电子数据鉴定, 司法鉴定, Windows系统鉴定]
source: 〔来源文件不存在〕
source: 〔来源文件不存在〕
source: 〔来源文件不存在〕
sources: 《电子数据司法鉴定实务》郭弘 科学出版社 2025年.md
---

# 第五章 Windows系统电子数据鉴定

## 第节 Windows系统概述

在电数据司法鉴定中，针对个计算机类检材多数安装的是Windows7及后续更新版本，而服务器类检材则多数是WindowsServer2008及后续版本。因此，对于从事电数据的鉴定员，需熟悉Windows操作系统的相关知识,包括Windows常见的痕迹信息和各种志件等。此外，鉴定员也需要熟悉常见的相关痕迹信息的存储及检验分析方法。

## 、常录结构

在开展涉及WindowsVista及更新版本的操作系统鉴定时，应熟悉Windows常的录结构，以便能快速找到相关的涉案数据及文件。

## （）WindowsVista及更新版本常录

操作系统安装录：\Windows

程序安装录:\Program Files或\Program Files(x86)

户配置录:\Users

桌：\Users\<户名>\Desktop

档：\Users\<户名>\Documents

下载：\Users\<户名>\Downloads

图：\Users\<户名>\Pictures

视频：\Users\<户名>\Videos

乐：\Users\<户名>\Music

各类应数据：\Users\<户名>\AppData

回收站：\$Recycle.Bin

Windows事件志:\Windows\System32\Config\winevt\Logs

系统注册表件：\Windows\System32\Config

（）Windows2000/XP常录

操作系统安装录：\Windows

程序安装录:\Program Files或\Program Files(x86)

用户配置录：\Documents and Settings

桌:\Documents andSettings\<户名>\桌

档:\Documents and Settings\<户名>\My Documents

乐：\Documents and Settings\<户名>\My Documents\My Music

图片:\Documents and Settings\<用户名>\My Documents\My Pictures

最近访问文档：\Documents and Settings\<用户名>\Recent

收藏夹：\Documents and Settings\<用户名>\Favorites

发送至：\Documents and Settings\<用户名>\SentTo

Cookies:\Documents and Settings\<用户名>\Cookies

回收站：Recycler(NTFS分区)或 Recycled(FAT 分区）

Windows 事件日志:\Windows\System32\Config

系统注册表文件：\Windows\System32\Config

## 二、磁盘分区格式化机制

从WindowsVista系统开始，用户在Windows系统中对分区进行格式化操作，系统执行的策略与早期的Windows系统不同。如用户取消勾选“快速格式化”的选项，Vista系统将执行正常格式化动作，即对磁盘先进行坏扇区检测，如存在坏扇区，坏扇区将会被记录，其所在的扇区位置将不能用于数据存储。此外，Vista系统将会重建新的文件系统，原有的未分配簇将会全部被清零，相当于数据擦除，因此格式化后的分区中的数据将无法进行恢复。

## 三、卷引导扇区前预留扇区数

在WindowsXP及早期操作系统，用户创建的文件系统（FAT/NTFS)的卷引导记录与分区表（MBR分区表或EBR扩展分区表)之间预留的扇区数为63个。以下案例是在WindowsXP系统下创建的一个磁盘，磁盘总大小为10GB，其中包含1个主分区，3个逻辑分区，如图5-1所示。

![](images/768a0e7e564f2c296a47e5bf106c92dc4b393343c6df4d321d2b5507b692619a.jpg)  
图5-1Windows XPMBR/EBR与卷引导扇区间预留扇区(扇区数63)

在WindowsVista及更新的操作系统，用户创建的文件系统（FAT/NTFS)的卷引导记录与分区表（MBR分区表或EBR扩展分区表）之间预留的扇区数为2048个。以下案例是在Windows10系统下创建的一个磁盘，磁盘总大小为10GB，其中包含1个主分区，3个逻辑分区，如图5-2所示。

![](images/33c6291e21750f59163ac00daede80fac22b2111b3a7239bc15276ecb080d335.jpg)  
图5-2Windows 10 MBR/EBR与卷引导扇区间预留扇区(扇区数2048)

## 四、BitLocker 加密

从WindowsVista和WindowsServer 2008系统版本开始，除了支持原有的EFS加密，Windows 系统新增支持BitLocker加密，可对非系统或系统分区进行全卷加密，进一步提高了数据保护的能力。之后的Windows7系统又进一步增加了BitLocker To Go，支持对优盘及移动硬盘进行数据加密。BitLocker支持使用密码、TPM芯片、智能卡（SmartCard）、USBKey（可用优盘或USB移动存储介质作为载体）及PIN码等多种密钥保护器。

Windows 系统要启用BitLocker加密，需要具备一定的条件，并非所有WindowsVista及后续更新的操作系统均能支持。除了Windows 7专业版外，从Windows Vista至Windows 11 的专业版、企业版及旗舰版均支持BitLocker加密，见表5-1。随着微软Windows系统不断发展，对于内置TPM2.0芯片且支持待机连接模式（Connected Standby)的计算机，如内置的操作系统是Windows Home家庭版，也支持启用基于TPM 的 BitLocker加密，即设备加密(DeviceEncryption) [117]

表5–1 支持 BitLocker 的 Windows 版本
<table><tr><td>操作系统版本</td><td>专业版</td><td>企业版</td><td>旗舰版</td></tr><tr><td>Windows Vista</td><td>支持</td><td>支持</td><td>支持</td></tr><tr><td>Windows 7</td><td>不支持</td><td>支持</td><td>支持</td></tr><tr><td>Windows 8/8.1</td><td>支持</td><td>支持</td><td>支持</td></tr><tr><td>Windows 10</td><td>支持</td><td>支持</td><td>支持</td></tr><tr><td>Windows 11</td><td>支持</td><td>支持</td><td>支持</td></tr></table>

不少用户经常使用BitLocker对非系统分区进加密，直接设置一个密码即可。然而要对Windows系统所在分区进行加密，一般要求计算机有内置的TPM芯片。没有TPM芯片的情况下，Windows 系统默认无法开启BitLocker加密，但可以通过修改组策略来规避这个限制。虽然可以强行开启对系统分区的 BitLocker加密，但每次开机，启动Windows系统前均要输入BitLocker恢复密钥才能正常启动。

首次启用 BitLocker,Windows 系统默认要求备份 BitLocker恢复密钥，通常会生成一个以“BitLocker恢复密钥”和标识符命名的文本文件，文件扩展名为 $\mathrm { T X T _ { o } }$ 在文件保存时用户也可修改其文件名。该文件的内容使用UTF-16LE(即Unicode)编码进行数据存储。该文件中最重要的就是恢复密钥串，它是由48位数字组成，每8位数字一组，使用符号“-”进行分隔，每8位数字均可被11整除，每8位数字大小必须小于216×11（即720896)，如图5-3所示。

![](images/1f23c10f75b780ebb221d6a47481de81a1c1524457190d0a35b006914d64a0df.jpg)  
图5–3 BitLocker 恢复密钥

## 第二节 Windows 注册表分析

## 一、注册表概述

注册表是Windows系统使用的一种集中式分层数据库，常用于存储为一个或多个用户、应用程序和硬件设备配置系统所必需的信息。此外，微软Windows CE 和Windows Mobile 嵌入式及智能机终端操作系统中也均使用注册表来存储相关信息。

对于电子数据司法鉴定而言，鉴定人员可使用鉴定软件，也可手动对Windows系统注册表文件、用户注册表文件及相关注册表文件进行检验并提取相关证据。在商业秘密泄密/窃取、知识产权纠纷、网络攻击事件等案件中，鉴定人员时常需要对Windows 系统中的各类与注册表相关的痕迹信息进行检验，如USB设备使用记录、Windows及第三方应用程序的最近访问文件(MRU)、最近运行的程序记录(UserAssist)、AmCache、ShellBags和打印机配置等。

## 二、注册表存储位置及文件结构

## (一)存储位置

Windows 不同版本存储注册表文件的位置存在差异。表5–2是常见的Windows系统默认的系统注册表、用户注册表文件的列表，可作为开展Windows注册表检验分析的参考。

表5-2 Windows注册表文件存储位置
<table><tr><td>版本</td><td>系统注册表文件存储位置</td><td>用户注册表文件存储位置</td></tr><tr><td>Windows NT</td><td>\WINNT\Windows\System32 \Config</td><td>%SystemRoot%\Profles\&lt;用户名&gt;\NTUSER.DAT</td></tr><tr><td>Windows 2000</td><td>\WINNT\Windows\System32 \Config</td><td>\Documents and Settings\&lt;用户名&gt;\NTUSER.DAT</td></tr><tr><td>Windows XP/2003</td><td>\Windows\System32\Config</td><td>\Documents and Settings\&lt;用户名&gt;\NTUSER.DAT</td></tr><tr><td>Windows Vista~ Windows 11</td><td>\Windows\System32\Config</td><td>\Users\&lt;用户名&gt;\NTUSER.DAT</td></tr></table>

除Windows系统注册表和户注册表件外,部分Windows系统版本将部分注册表信息存储于另外的件中，见表5-3。在开展注册表检验分析时，应留意此部分注册表文件的信息，避免遗漏此部分证据。如涉及需要对ShelBags信息进检验，需对UsrClass.dat进分析并提取相关证据。

表5-3其他Windows相关注册表文件
<table><tr><td>版本</td><td>注册表文件存储位置</td><td>描述</td></tr><tr><td>Windows Vista~ Windows11</td><td>%UserProfile% \AppData \Local \Microsoft \Windows\UsrClass.dat</td><td>包含用户的相关配置信息，如 ShellBags信息，被 虚拟映射为HKCU/Software/Classes</td></tr><tr><td>Windows 7~Windows 11</td><td>%SystemRoot%\AppCompat\ Programs\Amcache.hve</td><td>执行过的应用程序相关信息</td></tr></table>

Windows系统处于开机运状态时，可通过注册表编辑器查看或编辑注册表件中的数据。通过REGEDIT命令可直接打开注册表编辑器，其中的注册表信息是来系统注册表及户注册表件的相关数据，对应关系见表5-4。通常存在多个HKEY前缀命名的注册表录信息。

表5-4注册表配置单元及文件列表
<table><tr><td>注册表配置单元名称 （开机状态）</td><td>注册表文件及相关文件</td><td>描述</td></tr><tr><td>HKEY_LOCAL_MACHINE \SAM</td><td>SAM, Sam.log,Sam.sav</td><td>存储与用户账户、目录服务相关的信息</td></tr><tr><td>\SECURITY</td><td>HKEY_LOCAL_MACHINE SECURITY,Security.log, Security. sav</td><td>存储与安全配置、权限、安全策略相关的信息</td></tr><tr><td>HKEY_LOCAL_MACHINE \SOFTWARE</td><td>SOFTWARE,Software.log， Software.sav</td><td>存储与本地计算机中安装软件相关的信息 （配置）</td></tr><tr><td>\SYSTEM</td><td>HKEY_LOCAL_MACHINE SYSTEM,System.alt，System.不 log, System.sav</td><td>存储与系统配置相关的信息（包括驱动、服 务、系统行为等)</td></tr><tr><td>HKEY_LOCAL_MACHINE \HARDWARE</td><td>无对应的注册表文件</td><td>每次系统启动时都会重新创建此键中的所有 数据，它是易失性数据，在每次系统启动后动 态生成，系统关机时丢弃</td></tr></table>

【靠最業】翁爸学業耕秦聖柔雀背履對，表構黎髮楚蛋菲集整業智寧主孝整彗磷集事等之用，请勿商用，縷，表
<table><tr><td>注册表配置单元名称 (开机状态)</td><td>注册表文件及相关文件</td><td>描述</td></tr><tr><td>HKEY_CURRENT_CONFIG</td><td>SYSTEM,System.alt,System. log, System.sav</td><td>只有HKEY_LOCAL_MACHINE配置单元下的 数据变更会显示在此处</td></tr><tr><td>HKEY_CURRENT_USER</td><td>该键为虚拟的，其数据来自当 前登录用户的NTUSER.DAT</td><td>包含登录用户的用户配置文件，包括环境变 量、桌面设置、网络连接、打印机和应用程序 首选项</td></tr><tr><td>HKEY_USERS</td><td>NTUSER. DAT, NTUSER. DAT. log</td><td>所有用户的配置信息，每个用户的NTUSER. DAT均以SID名称显示在该键的根目录下</td></tr><tr><td>HKEY_CLASSES_ROOT</td><td>该键为虚拟的，其数据来自 HKEY_LOCAL_MACHINE\ Software\Classes</td><td>包含应用程序和文件类型之间的关联(按文 件扩展名)以及对象链接和与COM关联的嵌 入（OLE）注册信息对象和文件类关联数据</td></tr></table>

## （二）注册表的层级及数据类型

注册表的顶级目录一般称之为键/主键/项(Key），子目录称为子键(SubKey)或子项，存储的数据项般称为值（Value），如图5-4所。

![](images/edcfc04d4abb51b1fd9c8d5ef33e463458afd078cfcc8a0f0241b809431a5a5a.jpg)  
图5-4 注册表结构

Windows注册表中的键值使不同的数据类型进存储。Windows注册表常见数据类型见表5-5。其中最为常见的数据类型有REG_SZ、REG_DWORD和REG_BINARY三种类型。

表5-5 注册表数据类型
<table><tr><td>类型</td><td>名称</td><td>描述</td></tr><tr><td>0</td><td>REG_NONE</td><td>无定义值类型</td></tr><tr><td>1</td><td>REG_SZ</td><td>以零结尾的字符串，ANSI或Unicode</td></tr><tr><td>2</td><td>REG_EXPAND_SZ</td><td>包含未扩充的环境变量引用的零结尾的字符串，如%PATH%</td></tr><tr><td>3</td><td>REG_BINARY</td><td>二进制数据，以十六进制符号显示</td></tr><tr><td>4</td><td>REG_DWORD</td><td>32位的数值，有时存储的值也用来表示布尔类型标识，如00为 禁用,01为启用</td></tr><tr><td>5</td><td>REG_DWORD_BIG_ENDIAN</td><td>双字节的值，用来存储BigEndian类型的值</td></tr><tr><td>6</td><td>REG_MULTI_SZ</td><td>零结尾的字符串数组，以2个空字符结束</td></tr><tr><td>7</td><td>REG_QWORD</td><td>64位的数值</td></tr></table>

## 1.注册表配置单元(Hive)

配置单元是注册表中个由键、键及值组成的逻辑组。在电数据鉴定过程中应当熟悉正在运行的操作系统中注册表编辑器的信息与磁盘中对应的注册表文件的映射关系。Windows系统注册表通常包括SAM、SECURITY、SYSTEM和SOFTWARE等注册表件，如图5-5所。

![](images/a16bae21c18080595604f232f20b1b2d928d4a5984a368d4499737919d463a8a.jpg)  
图5-5注册表配置单元(Hive)

## 2.注册表预定义项

注册表中的预定义项是指注册表编辑器中最顶层的项目（如HKEY_CLASSES_ROOT），每个项都是HKEY前缀开头。五预定义项是操作系统在运过程中经常访问的根节点，需要注意的是预定义项存在较多虚拟映射关系。五预定义项中包含的信息实际上都读取来系统注册表（SAM、SECURITY、SYSTEM和SOFTWARE）和户注册表（NTUSER.DAT、USRCLASS.DAT)等件的数据，见表5–6和图5–6。

表5-6 注册表预定义项
<table><tr><td>预定义项</td><td>简写</td><td>描述</td></tr><tr><td>HKEY_CLASSES_ROOT</td><td>HKCR</td><td>包含文件扩展关联信息及OLE数据库，存储在这里的信息可确保使 用Windows资源管理器打开文件时能打开正确的程序</td></tr><tr><td>HKEY_CURRENT_CONFIG</td><td>HKCC</td><td>在启动过程中动态创建，包含系统启动时的硬件相关的配置信息</td></tr><tr><td>HKEY_LOCAL_MACHINE</td><td>HKLM</td><td>包含特定于计算机的配置信息（用于任何用户），如软件，硬件及安全</td></tr><tr><td>HKEY_USERS</td><td>HKU</td><td>包含计算机上的所有以活动方式加载的用户信息和默认配置文件， 默认配置文件决定了没有人登录时，计算机如何响应</td></tr><tr><td>HKEY_CURRENT_USER</td><td>HKCU</td><td>包含登录到系统的当前用户的配置信息,该用户的文件夹、屏幕颜色和 “控制面板”设置都存储在这里。该信息与用户的配置文件相关联</td></tr></table>

![](images/f4cfd7bac4e0104b5c717015c0f56b58e805d5c13c717d0f234618427c49f033.jpg)  
图5-6 预定义项与项的映射关系图

值得注意的是此类信息都是在开机运的Windows系统中使注册表编辑器查看，在实际鉴定过程中，鉴定人员可手工找到注册表文件，直接读取其内部包含的数据。鉴定时直接对磁盘或镜像件中的注册表进分析，离线分析的视与开机状态分析视存在一定差异。

在部分电数据司法鉴定中，鉴定可能在计算机硬盘中发现存在扩展名为REG的件，此类REG件般是户将计算机中的注册表配置导出后的件，或是从其他来源获得的注册表配置件。REG件有其固定的结构，包括注册表编辑器版本信息及键路径、键值名及其数据内容，如图5–7所。

![](images/9846fe2a867b8d9040885b54d562e3b7d951d474717e8b0da255ce51379d3238.jpg)  
图5-7 注册表导出文件(REG文件）

## （三)文件结构

Windows注册表文件并非一个文本文件，更像是一个具有内部自身结构的文件系统。注册表文件包含根键(Key），它就像是文件系统中的根目录，子键(SubKey)类似子目录，而值(Value)类似文件。通常一个根键或子键包含大量的信息。

注册表件结构与件系统结构有很多相似之处。例如NTFS件系统通常有的数据结构，例如主文件分配表(Master FileTable)和属性(Attributes)。注册表文件也包含了自己的数据结构，通常称之为块（Block），分为Regf块和Hbin块。

注册表中的根键(Key)和子键(SubKey)有记录其最后数据修改的时间，在Windows注册表编辑中无法直接查看，借助第三方工具（如Windows Registry Recovery、Registry Explorer）即可查看键的最后写入时间戳的信息，该时间戳为FILETIME类型(8字节,UTC+0:0O),X-WaysForensics或WinHex的数据解释器可以快速解析其对应的日期时间信息，如图5–8所示。

![](images/5e148d806c1c9b4a13d22f06c6320a90fa435ca87568f5f1fed82d3028e527b4.jpg)  
图5-8注册表键的最后写入时间戳

了解注册表文件的结构非常重要，在进行检验分析时可对未分配空间、注册表文件松弛区、页交换文件(Pagefile.sys)或物理内存镜像进手动分析，从中挖掘遗留的相关证据。鉴定员需要能够识别注册表相关数据并对其进解释。

## 三、注册表常见痕迹信息

Windows注册表中包含丰富的系统配置和户设置等信息,这部分信息对于电数据鉴定与司法鉴定来说可能是重要的证据，有助于发现计算机用户的操作为以及操作系统运行过程中发的相关事件的关联信息。

## (一)系统痕迹

Windows系统相关痕迹信息主要与SYSTEM和SOFTWARE注册表件有关。

## 1.系统关机时间

SYSTEM\ControlSet<序号>\Control\Windows\ShutdownTime

（FILETIME期时间格式)

2.外部设备接入及挂载

• SYSTEM\ContolSet<序号>\Enum\USB

（连接计算机的USB设备的相关信息,如HID设备/加密狗,更多详情可参见本章第四节)

•SYSTEM\ControlSet<序号>\Enum\USBSTOR

(连接计算机的USB存储设备的相关信息,如优盘、移动硬盘,更多详情可参见本章第四节)

• SYSTEM\MountedDevices

（曾经连接计算机的存储介质所挂载的盘符及磁盘信息，更多详情可参见本章第四节)

## 3.络配置(TCP/IP)

• SYSTEM\ControlSet<序号>\Services\Tcpip\Parameters\Interfaces\[ keyname]

EnableDHCP（是否使DHCP）

IPAddress(IP地址)

SubnetMask（掩码）

▪ DhcpIPAddress(DHCP IP地址)

▪ DhcpSubnetMask(DHCP掩码）

▪ DhcpServer(DHCP服务器）

▪LeaseObtainedTime（IP租赁获得时间，UNIX期时间格式）

## 4.打印机设置

•SYSTEM\ControlSet<序号>\Control\Print\Printers\[keyname]

■ Name(打印机名称)

Port(打印机端)

Printer Driver（打印机驱动程序)

## 5.安装软件

• SOFTWARE\Microsoft \Windows\CurrentVersion\Uninstall\[keyname]

（通过安装包安装的软件通常会将软件相关信息写到注册表中，控制板中的“添加/删除程序”可通过该键的信息来卸载已安装程序）

▪ DisplayName 显名称

UninstalIString卸载字符串

▪ DisplayVersion 软件版本

■InstalDate安装期

InstallLocation安装录

▪Publisher发布

EstimatedSize预估

## 6.开机自启动软件

• SOFTWARE\Microsoft \Windows\CurrentVersion\Run

• SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce

• SOFTWARE\Microsoft \Windows\CurrentVersion\RunOnceEx

## 7.Windows索引搜索数据库

•Windows XP操作系统：

%systemdrive% \Documents and Settings \All Users \Application Data\Microsoft \Search\

Data\Applications\Windows\Windows.edb

•Windows7及更新操作系统版本：

%systemdrive%\ProgramData\Microsoft \Search\Data\Applications\Windows\Windows.edb

%systemdrive%\ProgramData \Microsoft\Search\Data\Applications\Windows\GatherLogs\ SystemIndex

## （二）用户痕迹

Windows用户痕迹相关信息主要存在于用户配置文件夹中，此外，相关配置信息与NTUSER.DAT和UsrClass.dat等注册表文件相关。

1.Windows 内置浏览器痕迹信息

• IE 6–7: %USERPROFILE%\LocalSettings\History\History.IE5

• IE 8 −9: %USERPROFILE%\AppData\Local\Microsoft \Windows\History\History.IE5

• IE 10-11 及Win10+版本：

• % USERPROFILE%\AppData\Local \Microsoft \Windows \WebCache\WebCacheV \*.dat

•工输网址信息：NTUSER.DAT\Software\Microsoft \Internet Explorer\TypedURLs

2.用户搜索关键词

· NTUSER.DAT\Software\Microsoft \Windows\CurrentVersion\Explorer\WordWheelQuery（Windows7及以上版本系统适用）

3.缩略图缓存

• %USERPROFILE%\AppData\Local\Microsoft \Windows\Explorer

4.网络映射历史记录

• NTUSER.DAT\SOFTWARE\Microsoft \Windows\CurrentVersion \Explorer\Map Network Drive MRU

5.远程桌面连接(Terminal Client)

• NTUSER.DAT\Software \Microsoft \Terminal Server Client \Default

6.墙纸( Wall Paper)

• NTUSER.DAT\Software \Microsoft \Windows\CurrentVersion \Explorer\Wallpaper\MRU

7.用户配置文件夹定义

• NTUSER.DAT\Software \Microsoft \Windows\CurrentVersion \Explorer\User Shell Folders

## (三)其他注册表相关痕迹信息

Windows系统痕迹及用户痕迹均包含来注册表的各种信息，多数鉴定软件可自动解析系统痕迹信息和用户痕迹信息。在开展电子数据司法鉴定中，可能会遇到有些涉案的痕迹信息存储于注册表，而鉴定软件却无法解析，就要求鉴定人员需具备一定的研究能力，查阅书籍、刊物或其他文献，也可搭建测试环境进模拟实验并进验证总结出注册表中记录的相关痕迹信息。

## 四、Windows 注册表鉴定

## (一)Windows 内置工具分析

对于涉案的计算机磁盘或镜像文件进行注册表鉴定，可以使用Windows内置工具进行分析。首先将要分析的注册表文件复制到指定目录，然后运行注册表编辑器，选中HKEY_LOCAL_MACHINE。从菜单“文件”选择“加载配置单元”，即可对注册表文件进行内容查看。该方式无法提取和分析删除的注册表信息。此外，也可通过菜单中的“卸载配置单元”将已加载的配置单元卸载。

## (二)辅助工具分析

除了Windows 内置工具，也可使用辅助分析工具分析注册表，例如 Registry Explorer 支持恢复删除的注册表信息，其搜索能力甚至超越众多鉴定软件。Registry Explorer支持批量添加多个注册表配置单元文件，且可以自动恢复删除的注册表信息。该工具还内置了鉴定常用的书签，直接选择要查看的注册表信息即可直接跳转到对应的注册表位置。

在电子数据鉴定过程中，特别是不清楚键值存在哪个注册表文件时，鉴定人员可直接加载所有系统注册表文件及多个用户的注册表文件（NTUSER.DAT），然后对所有注册表文件进行全局搜索。Registry Explorer 支持根据键(Key)、值名称(Value name)、值数据(Value Data)及值残留数据(Value Slack)等属性进行常规关键词及正则表达式搜索。此外，还可以根据注册表键或值的最后写时间戳属性进过滤。

鉴定人员通常还可以使用商业鉴定软件，如 EnCase Forensic、FTK、X-Ways Forensics等进行注册表的鉴定。

## 第三节 文件打开记录痕迹分析

## 一、快捷方式文件

## (一)快捷方式文件概述

快捷方式文件也称作链接文件，扩展名是“Ink”，主要有三种来源：分别是用户手动创建、应用程序安装后自动生成、用户打开文件/文件夹自动生成。快捷方式文件中包含了大量信息，是Windows鉴定中重要的分析对象，主要包括：

• 目标文件的大小

• 目标件创建时间、修改时间和访问时间

• 目标文件的完整路径

•所在分区存储介质类型(可移动或不可移动)

•所在分区卷序列号

●打开标件时卡MAC地址

• 计算机名

## (二)快捷方式文件工作机制

默认情况下，当双击或者通过软件中的“打开”对话框来打开文件或文档，在Recent文件夹中都会生成一个快捷方式文件（文件扩展名为.lnk），见表5–7。

表5–7 Windows不同版本快捷方式存储路径
<table><tr><td>操作系统版本</td><td>快捷方式文件存储路径</td></tr><tr><td>Windows 2000/XP/2003</td><td>%UserProfile% \Recent</td></tr><tr><td>Windows Vista/Windows 7/8/10</td><td>%UserProfile%\AppData\Roaming\Microsoft\Windows\Recent</td></tr></table>

Windows7操作系统默认在开始菜单中不显示“最近使的项”列表，通过修改系统设置即可在Windows 开始菜单中显示。需要注意的是，即使没有勾选该选项，操作系统也始终会生成快捷方式文件。

Windows 8和Windows 10 操作系统在开始菜单中均没有“最近使用的项目”。在Windows10系统的资源管理器界面“快速访问”中可以找到“最近使用的文件”，从中可发现该用户最近打开过的件列表，从而了解用户对件操作的活动情况。

快捷式件的路径信息中包含了盘符信息，但这并不能用来关联具体的分区或存储设备，因为盘符的分配并不是固定的，同一个盘符在不同时间可能会分配给不同的分区。但快捷方式文件中的卷序列号可以确定具体的分区。卷序列号在格式化时生成，具有唯一性且正常情况下不会变化。而卷序列号又可以与存储设备的相关信息进关联。

快捷方式文件有明显的签名特征，前20字节固定为\x4C\x00\x00\x00\x01\x14\x02\x00\x00\x00\x00\x00\xC0\x00\x00\x00\x00\x00\x00\x46，且文件比较小，一般都小于4KB，部分甚至小于1KB。对于NTFS文件系统，小于1KB 的文件属于常驻文件，文件内容保存在\$MFT文件中，文件被删除后，很长时间内不会被覆盖，恢复的概率很大。大于1KB的快捷方式文件，签名恢复的成功率也非常高。

## (三)快捷方式文件检验

通过鉴定工具可自动检验和分析快捷方式文件（.LNK），并解析其内嵌的元数据信息，常用的工具有取证大师取证神探、X-Ways Forensics、Magnet Axiom 及Windows File Analyzer(免费工具），分析过程如图5-9和图5–10所示。

![](images/f7ff78d8500bb9da2aa3d6e81ec3a18d84c82167850ea3a22de7fd61b8765472.jpg)  
图5–9取证大师解析快捷方式文件

## 二、最近打开的项目

Windows 操作系统本身及许多应用程序记录了“最近打开的项目”（Most RecentlyUsed，简称MRU)。Windows操作系统及应用软件将MRU历史记录在注册表中，在注册表的键名经常带有“MRU”的关键词。

多数鉴定工具对常见的MRU信息都能进行提取和解析。如解析Windows系统通用对话框中“最近打开保存文档”主要来自注册表；而“最近访问的文档”的数据源主要来跳转列表和快捷式件，注册表中RecentDocs键中的打开档列表并未列其中。鉴定人员可简单通过查看鉴定结果中解析出的内容对应的来源文件来判断鉴定结果对应的数据源。如需提取完整MRU信息，可能需要手动分析更多存储于注册表中的信息。作为电子数据鉴定人员，不能完全依赖鉴定工具的解析能力，需要了解各种MRU信息的存储位置及解码方法。目前大部分MRU信息都是明文存储，多数可以直接查看其内容。

![](images/ceb6804906357a4776ef1699892be6fc31f708684d9315efaa2ecc8c3ef2c7c2.jpg)  
图5-10 WFA 鉴定工具分析 LNK快捷方式文件

NirSoft工具集中的RecentFilesView支持解析注册表中的部分MRU信息（如最近打开、保存及访问的档），其主要数据来源是对Recent件夹中的快捷式件及NTUSER.DAT注册表中的对话框最近打开/保存的档。默认情况下允许该具针对所在计算机的系统录及用户注册表进行分析，也可通过按F9键进入“AdvancedOptions（高级选项）”手动指定Recent文件夹及用户注册表文件（NTUSER.DAT)的位置，进行文件的离线解析，如图5–11所示。

## (一)最近打开的文档

Windows系统针对不同的户会记录其打开过的档(不包含可执程序）。最近打开的档主要是指户注册表NTUSER.DAT中记录的RecentDocs的信息，其存储位置为NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\Explorer\RecentDocs。默认注册表中根据文件扩展名记录户打开的件列表，并记录了打开件的次序。

## （二）对话框打开/保存/访问的件

除系统内置的工具外，第三方软件也可直接通过WindowsAPI接口直接调用文件打开及保存的对话框窗口，通过该窗口来读取或保存文件的内容。主要的MRU痕迹信息与OpenSaveMRU或OpenSavePIDMRU有关，如图5-12所示。子键“\*”记录了所有类型的件

![](images/1c1a8cec6424c5e5903371522a16468e2029941adcd3e271872e8cc6b3c514c7.jpg)  
图5– 11 RecentFilesView 解析的 MRU记录

打开及保存记录，其他子键则只记录对应扩展名的记录。MRU记录没有使用明文字符串记录信息，其格式是PIDL。

• NTUSER.DAT\Software \Microsoft \Windows \CurrentVersion \Explorer \ComDlg32\OpenSaveMRU (Windows 2000/XP/2003)

• NTUSER.DAT\Software \Microsoft \Windows \CurrentVersion \Explorer \ComDlg32\OpenSavePIDMRU（Vista及以上系统)

![](images/bdf756a50ea471543510227ee1834fa271bf0df391fc54538715ab5060d8451c.jpg)  
图5– 12 Windows 7 系统中的MRU 记录

## （三）微软Office应用最近打开项目

微软Office软件包含常见的Word、Excel、PowerPoint、Visio和Access组件，这些组件应用程序打开件后均会记录曾经打开过的件完整路径和最后打开期时间，同时也记录曾经打开过的件夹信息。此外，如计算机用户使用的是Office 365账户登录，Office应用程序记录的最近打开件信息所在的注册表位置将会有所不同。

最近打开文件项目以“Item+数字”命名，值为字符串型。例如：[F00000000][T01D94E4B849CC2C0][O00000000]\*C:\Users\henry\Desktop\技术白皮书.docx，其中[T01D94E4B849CC2C0]是打开该文件的最后日期时间，T代表“时间”,01D94E4B849CC2C0为FILETIME数据类型（Big Endian)对应的十六进制字符串，如图5– 13所示，通过DCode工具进行时间转换，经过实际测试验证，可解析出正确的时间信息，如图5-14所示。

![](images/45aba7eccbfd36f1e906d2a4647df5c1cf2f6dddf9d7e2d6920c7eee3a533180.jpg)  
图5 – 13 Word 的 File MRU 记录

![](images/922404c8b867f26b51fe6c7f75292344a6dbd0cac592659e4385e81267658f5b.jpg)  
图5-14使用DCode解码FILETIME时间数据

微软Office办公软件及相关组件的最近打开项信息均存储于户注册表NTUSER.DAT文件中，其对应的注册表内部路径见表5-8。注册表中的路径包含了Office的内部版本号。

表5-8微软Office常见应用程序最近打开项目记录
<table><tr><td>Office应用程序</td><td>最近打开项目记录 (注册表路径)</td></tr><tr><td>Word最近打开文件</td><td>NTUSER.DAT\SOFTWARE\Microsoft\Office\&lt;内部版本号&gt;\Word\File MRU NTUSER.DAT\SOFTWARE\Microsoft \Office\&lt;内部版本号&gt;\Word\UserMRU \&lt;UserID&gt;\File MRU (Office 365)</td></tr><tr><td>Word最近打开文件夹</td><td>NTUSER.DAT\SOFTWARE\Microsoft\Office\&lt;内部版本号&gt;\Word\Place MRU NTUSER.DAT\SOFTWARE\Microsoft\Office\&lt;内部版本号&gt;\Word\User MRU \&lt;UserID&gt;\Place MRU (Office 365)</td></tr><tr><td>Excel最近打开文件</td><td>NTUSER.DAT\SOFTWARE\Microsoft\Office\&lt;内部版本号&gt;\Excel\File MRU NTUSER.DAT\SOFTWARE\Microsoft \Office\&lt;内部版本号&gt;\Excel\User MRU \&lt;UserID&gt;\File MRU (Office 365)</td></tr><tr><td>Excel 最近打开文件夹</td><td>NTUSER.DAT\SOFTWARE\Microsoft\Office\&lt;内部版本号&gt;\Excel\Place MRU NTUSER.DAT\SOFTWARE\Microsoft \Ofice\&lt;内部版本号&gt;\Excel\UserMRU \&lt;UserID&gt;\Place MRU (Office 365)</td></tr><tr><td>PowerPoint最近打开文件</td><td>NTUSER.DAT\SOFTWARE\Microsoft \Office\&lt;内部版本号&gt;\PowerPoint \ File MRU NTUSER.DAT\SOFTWARE\Microsoft\Office\&lt;内部版本号&gt;\PowerPoint \User MRU\&lt;UserID&gt;\File MRU (Office 365)</td></tr><tr><td>PowerPoint最近打开文 件夹</td><td>NTUSER.DAT\SOFTWARE\Microsoft \Office\&lt;内部版本号&gt;\PowerPoint \ Place MRU NTUSER.DAT\SOFTWARE\Microsoft\Office\&lt;内部版本号&gt;\PowerPoint\User MRU\&lt;UserID&gt;\Place MRU (Office 365)</td></tr><tr><td>Visio最近打开文件</td><td>NTUSER.DAT\SOFTWARE\Microsoft \Office\&lt;内部版本号&gt;\Visio\File MRU NTUSER.DAT\SOFTWARE\Microsoft\Office\&lt;内部版本号&gt;\Visio \User MRU \&lt;UserID&gt;\File MRU (Office 365)</td></tr><tr><td>Visio 最近打开文件夹</td><td>NTUSER.DAT\SOFTWARE\Microsoft\Office\&lt;内部版本号&gt;\Visio\Place MRU NTUSER.DAT\SOFTWARE\Microsoft \Office\&lt;内部版本号&gt;\PowerPoint\User MRU\&lt;UserID&gt;\Place MRU (Office 365)</td></tr><tr><td>Access最近打开文件</td><td>NTUSER.DAT\SOFTWARE\Microsoft\Office\&lt;内部版本号&gt;\Access\FileMRU NTUSER.DAT\SOFTWARE\Microsoft \Office\&lt;内部版本号&gt;\Access \User MRU\&lt;UserID&gt;\File MRU (Office 365)</td></tr><tr><td>Access 最近打开文件夹</td><td>NTUSER. DAT\SOFTWARE\Microsoft\Office\&lt;内部版本号&gt;\Access\ Place MRU NTUSER.DAT\SOFTWARE\Microsoft \Office\&lt;内部版本号&gt;\Access \User MRU\&lt;UserID&gt;\Place MRU (Office 365)</td></tr></table>

## （四）WPSOffice最近打开件记录

金山WPSOffice主要有WPS（字处理）、ET（表格）、WPP（演示文稿）、PDF等组件组成，每个组件都是独的程序，分别记录打开过的件列表以及打开件的期时间。用户注册表文件NTUSER.DAT中，可找到Kingsoft\Office\<版本号>\<程序名缩写>\RecentFiles\Sequence，该键中记录了所有打开过的档的名称及期时间（UnixEpoch时间格式），如图5-15所示。此外，在子键files和filebak中也有打开件的完整名称和路径。部分应用（如PDF、WPS)和LastPos的子键记录每个档最后的编辑位置，如图5–16所示。

![](images/6ce51ce26e88935d8d5b645be4bf8fa7a2fbd92aadbf0fe4e7b8ef2258ed4dcf.jpg)  
图5-15注册表中WPS的MRU记录

![](images/8537782fd7475892b1336030848425cfae7b47910c4eb58cd1012d001722c300.jpg)  
图5-16WPSOffice应用程序记录的最后位置及编辑位置

WPSOffice与微软Office有较多相似之处，它同样在注册表件中记录了WPSOffice各组件最近打开件列表信息，见表5–9。

表5-9WPS应用程序及对应的最近打开文件记录(注册表路径)
<table><tr><td>WPS应用程序</td><td>最近打开文件记录（注册表路径）</td></tr><tr><td>WPS字处理最近打开 文件</td><td>NTUSER.DAT\SOFTWARE\kingsof \Office\版本\wps\RecentFiles\files 最近打开文件列表 NTUSER.DAT\SOFTWARE\kingsoft \Office\版本\wps\RecentFiles\filesbak 最近打开文件列表（备份） NTUSER. DAT\\SOFTWARE\kingsoft \Office\版本\wps\RecentFiles\Sequence</td></tr><tr><td>ET表格最近打开文件</td><td>NTUSER.DAT\SOFTWARE\kingsoft \Office\版本\et\RecentFiles\files 最近打开文件列表 NTUSER.DAT\SOFTWARE\kingsoft \Office\版本\et\RecentFiles\filesbak 最近打开文件列表（备份） NTUSER.DAT\\SOFTWARE\kingsoft \Office\版本\et \RecentFiles\Sequence 最近打开文件的时间戳（UnixEpoch时间格式）</td></tr><tr><td>WPP 演示文稿最近打 开文件</td><td>NTUSER.DAT\SOFTWARE\kingsoft \Office\版本\wpp\RecentFiles\files 最近打开文件列表 NTUSER.DAT\SOFTWARE\kingsoft\Office\版本\wpp\RecentFiles\filesbak 最近打开文件列表(备份） NTUSER.DAT\\SOFTWARE\kingsoft\Office\版本\wpp\RecentFiles\Sequence 最近打开文件的时间戳(Unix Epoch时间格式)</td></tr><tr><td>WPS PDF最近打开 文件</td><td>NTUSER.DAT\SOFTWARE\kingsoft \Office\版本\pdf\RecentFiles\files 最近打开文件列表 NTUSER.DAT\SOFTWARE\kingsoft\Office\版本\pdf\RecentFiles\filesbak 最近打开文件列表（备份） NTUSER.DAT\\SOFTWARE\kingsoft \Office\版本\pdf\RecentFiles\Sequence 最近打开文件的时间戳（UnixEpoch时间格式） NTUSER.DAT\\SOFTWARE\kingsoft\Office\版本\pdf\RecentFiles\LastPos 最近打开文件的编辑位置信息</td></tr></table>

## (五）系统内置应最近打开项

除了以上Windows系统常见MRU信息外,系统内置的画图、运命令（Run）、媒体播放器播放记录等均有对应的注册表记录。

（1）画图（Paint）最近打开件：SOFTWARE\Microsoft\Windows\CurrentVersion\Applets\Paint\Recent File List

(2）最近运行过的命令：NTUSER.DAT\Software\Microsoft \Windows\CurrentVersion\Explorer\ RunMRU

(3）媒体播放文件（Media Player)打开/保存的件夹：NTUSER.DAT\Software\Microsoft\ MediaPlayer\Player\Settings\SaveAsDir 或OpenDir

播放件列表：NTUSER.DAT\Software\Microsoft\MediaPlayer\Player\RecentFileList

## （六）其他第三软件最近打开项

（1）Foxit福昕PDF最近打开文件/文件夹：NTUSER.DAT\SOFTWARE\Foxit Software\FoxitPhantom<版本号>\MRU\FileMRU

(2）WinRAR最近打开文件列表：NTUSER.DAT\SOFTWARE\Foxit Software\Foxit Phantom<版本号>\MRU\PlaceMRU

(3）WinRAR最近打开件列表：NTUSER.DAT\SOFTWARE\WinRAR\ArcHistory

（4）加密软件容器挂载列表：NTUSER.DAT\Software\Jetico\BestCrypt\Recently Mounted Containers

## 三、跳转列表

跳转件是特定应程序打开过的最近件的列表记录。每个程序都有个对应的列表。即使Recent件夹中的快捷式件被删除或应程序被卸载删除后,该痕迹信息特别有用，可直观了解用户行为活动。

跳转列表件分为两种类型：

•Automatic（自动）：系统自动弹出此类跳转列表，它记录了文件使用的相关信息，并将该信息存储于标件，与于打开该件的程序进关联。

•Custom（定义）：该跳转列表由各应程序维护，可提供与程序菜单或定义分类相关的任务列表。

所有程序的跳转列表数据存储于户配置件夹中：%UserProfile%\AppData\Roaming\Microsoft\Windows\Recent，文件夹中的Automatic Destinations 和CustomDestinations 文件夹分别存储了Automatic（动)和Custom（定义)两种类型的跳转件的数据件，其件的命名分别是 ID.automaticDestinations-ms 和 ID.customDestinations-ms。

每一种应用程序都有自己的文件名，也称为跳转列表编号（JumpListID），可能既有AutomaticDestinations-ms，也有CustomDestination-ms文件。通过用文本编辑器查看每一个文件，可以判断文件链接至程序的跳转列表条目。经研究发现，下列程序将它们最近打开项目的数据存储于以下位置：

• 28c8b86deab549a1.customDestinations-ms -- Internet Explorer 8 跳转列表

•1b4dd67f29cb1962.automaticDestinations-ms--Windows资源管理器跳转列表

●9b9cdc69c1c24e2b.automaticDestinations-ms--记事本最近打开的件

•9b9cdc69c1c24e2b.customDestinations-ms--保存户动固定的记事本相关记录

跳转列表中的应用ID为16位的十六进制字符串，由于应用程序的路径经过非标准的CRC64算法计算得到。由于应用ID和应用路径有关，所以不同版本的应用对应的跳转列表ID相同，同一个跳转列表ID，也可能对应某个应用的不同版本。即使是完全相同的应用，安装在不同路径也会产不同的应ID。

github.com在其GitHub上公布了数百条跳转列表ID及对应的应用，国内hustrong.com公布了部分本应的跳转列表ID。常见的应ID见表5-10。

表5-10常见跳转列表应用ID
<table><tr><td>应用ID</td><td>应用</td><td>来源</td></tr><tr><td>5F7B5F1E01B83767</td><td>Windows快速访问</td><td>github.com</td></tr><tr><td>F01B4D95CF55D32A</td><td>Windows 资源管理器</td><td>github.com</td></tr><tr><td>A8C43EF36DA523B1</td><td>Microsoft Office Word 2003</td><td>github.com</td></tr><tr><td>75D01B5B7DF0D177</td><td>Microsoft Office Excel 2003</td><td>hustrong.com</td></tr><tr><td>C1441AD09A3298E8</td><td>Microsoft Office PowerPoint 2003</td><td>hustrong.com</td></tr><tr><td>ADECFB853D77462A</td><td>Microsoft Office Word 2007</td><td>github.com</td></tr><tr><td>B2122DC4CD78DA12</td><td>Microsoft Office Word 2007</td><td>hustrong.com</td></tr><tr><td>631BF9274CB983CF</td><td>Microsoft Office Word 2007</td><td>hustrong.com</td></tr><tr><td>CDF30B95C55FD785</td><td>Microsoft Office Excel 2007</td><td>github.com</td></tr><tr><td>108CB4A6150F18AF</td><td>Microsoft Office Excel 2007 x86</td><td>hustrong.com</td></tr><tr><td>F5AC5390B9115FDB</td><td>Microsoft Office PowerPoint 2007 x64</td><td>hustrong.com</td></tr><tr><td>A7BD71699CD38D1C</td><td>Microsoft Office Word 2010x86</td><td>github.com</td></tr><tr><td>44A3621B32122D64</td><td>Microsoft Office Word 2010x64</td><td>github.com</td></tr><tr><td>9839AEC31243A928</td><td>Microsoft Office Excel 2010x86</td><td>github.com</td></tr><tr><td>6E855C85DE07BC6A</td><td>Microsoft Office Excel 2010×64</td><td>github.com</td></tr><tr><td>9C7CC110FF56D1BD</td><td>Microsoft Office PowerPoint 2010x86</td><td>github.com</td></tr><tr><td>5F6E7BC0FB699772</td><td>Microsoft Office PowerPoint 2010x64</td><td>github.com</td></tr><tr><td>A4A5324453625195</td><td>Microsoft Office Word 2013 x86</td><td>github.com</td></tr><tr><td>47BB2136FDA3F1ED</td><td>Microsoft Ofice Word 2013</td><td>hustrong.com</td></tr><tr><td>F0275E8685D95486</td><td>Microsoft Office Excel 2013 x86</td><td>github.com</td></tr><tr><td>69BACC0499D41C04</td><td>Microsoft Office Excel 2013</td><td>hustrong.com</td></tr><tr><td>8FDB062F1E486CAC</td><td>Microsoft Office PowerPoint 2013</td><td>github.com</td></tr><tr><td>4293E440AD719476</td><td>Word 2016 x64</td><td>hustrong.com</td></tr><tr><td>A18DF73203B0340E</td><td>Microsoft Office Word 2016</td><td>github.com</td></tr><tr><td>FB3B0DBFEE58FAC8</td><td>Microsoft Office Word 2016/2019 x64</td><td>hustrong.com</td></tr><tr><td>B2122DC4CD78DA12</td><td>Microsoft Office Word 2016 x32</td><td>hustrong.com</td></tr><tr><td>BEB8BC0EF1324736</td><td>Microsoft Office Excel 2016x64</td><td>hustrong.com</td></tr><tr><td>B8AB77100DF80AB2</td><td>Microsoft Office Excel 2016/2019 x64</td><td>hustrong.com</td></tr><tr><td>D00655D2AA12FF6D</td><td>Microsoft Ofice PowerPoint 2016/2019x64</td><td>hustrong.com</td></tr><tr><td>7821F5BF3954ED50</td><td>PowerPoint 2016 x64</td><td>hustrong.com</td></tr><tr><td>BEF1F793523AF548</td><td>WPS文字2013/2016/2019</td><td>hustrong.com</td></tr><tr><td>647A64F80B1EAE05</td><td>WPS表格2013/2016/2019</td><td>hustrong.com</td></tr><tr><td>42938BE9A7126430</td><td>WPS演示2013/2016/2019</td><td>hustrong.com</td></tr><tr><td>579438F135536AEC</td><td>WPS Office 2019</td><td>hustrong.com</td></tr><tr><td>8A461F82E9EB4102</td><td>福昕阅读器</td><td>hustrong.com</td></tr><tr><td>A0C14AF241D40144</td><td>福昕 PDF阅读器</td><td>hustrong.com</td></tr><tr><td>3E9850346F375D41</td><td>福昕高级PDF编辑器</td><td>hustrong.com</td></tr><tr><td>D38A3EA7EC79FBED</td><td>Libreffice文本文档</td><td>hustrong.com</td></tr><tr><td>83DD64E7FA560BD5</td><td>LibreOffice 电子表格</td><td>hustrong.com</td></tr><tr><td>ECD1A5E2C3AF9C46</td><td>LibreOffice 演示文稿</td><td>hustrong.com</td></tr><tr><td>4D939776340F1D18</td><td>OpenOffice文本文档</td><td>hustrong.com</td></tr><tr><td>E7F34DEE82980C52</td><td>OpenOffice 电子表格</td><td>hustrong.com</td></tr><tr><td>C62FFFF28DBF17E9</td><td>Everything</td><td>hustrong.com</td></tr><tr><td>E9A39DFBA105EA23</td><td>FastStone Image Viewer</td><td>hustrong.com</td></tr></table>

续表

<table><tr><td>应用ID</td><td>应用</td><td>来源</td></tr><tr><td>588CEA7E4ABED698</td><td>Adobe Acrobat DC</td><td>hustrong.com</td></tr><tr><td>DE48A32EDCBE79E4</td><td>Adobe Acrobat Reader DC</td><td>hustrong.com</td></tr><tr><td>70FFD305907C983B</td><td>7-Zip</td><td>hustrong.com</td></tr><tr><td>4D991BAF44C72AF0</td><td>360阅读</td><td>hustrong.com</td></tr><tr><td>12DC1EA8E34B5A06</td><td>Windows 画图</td><td>hustrong.com</td></tr><tr><td>473AFB3847A021B4</td><td>Ultralso</td><td>hustrong.com</td></tr><tr><td>46F433176BC0B3D2</td><td>WinRAR x64</td><td>github.com</td></tr><tr><td>FB32DC162D479E3E</td><td>SumatraPDF</td><td>hustrong.com</td></tr><tr><td>F70B2DC8FC5D6A00</td><td>Xmind</td><td>hustrong.com</td></tr><tr><td>7DCD2FB1ACAD3C7E</td><td>QQ 播放器</td><td>hustrong.com</td></tr><tr><td>3A3AE9C3837E4147</td><td>腾讯视频</td><td>hustrong.com</td></tr><tr><td>83618AA7531263CB</td><td>暴风影音</td><td>hustrong.com</td></tr><tr><td>298A6B8701438FDA</td><td>CAJViewer 7.2</td><td>hustrong.com</td></tr><tr><td>930CF1DD2266E2CB</td><td>DB Browser for SQLite x64</td><td>hustrong.com</td></tr><tr><td>AE97C4551971CBE</td><td>DB Browser for SQLite x32</td><td>hustrong.com</td></tr><tr><td>A53CDC88DBEDA586</td><td>360 压缩</td><td>hustrong.com</td></tr><tr><td>AE6DF75DF512BD06</td><td>微软 Groove 音乐</td><td>hustrong.com</td></tr><tr><td>469E4A7982CEA4D4</td><td>Windows 写字板</td><td>github.com</td></tr><tr><td>9B9CDC69C1C24E2B</td><td>Windows 记事本</td><td>github.com</td></tr><tr><td>BAACB5294867B833</td><td>Notepad++x64</td><td>hustrong.com</td></tr><tr><td>E70D383B15687E37</td><td>Notepad++x32</td><td>hustrong.com</td></tr><tr><td>9D1F905CE5044AEE</td><td>旧版 Edge 浏览器</td><td>github.com</td></tr><tr><td>188F5EC9D11DED56</td><td>Edge 浏览器</td><td>hustrong.com</td></tr><tr><td>632339B8EC6BCF8E</td><td>Google Chrome</td><td>hustrong.com</td></tr><tr><td>1A89D1BEFE8E90E3</td><td>Adobe Acrobat Distiller Pro XI</td><td>hustrong.com</td></tr><tr><td>1BC9BBBE61F14501</td><td>OneNote</td><td>hustrong.com</td></tr><tr><td>23646679AACCFAEO</td><td>Adobe Reader</td><td>hustrong.com</td></tr><tr><td>26753C97EA000ECD</td><td>LibreOffice</td><td>hustrong.com</td></tr><tr><td>290532160612E071</td><td>WinRAR</td><td>hustrong.com</td></tr><tr><td>31E8AC6B0784ED7D</td><td>Foxit Reader</td><td>hustrong.com</td></tr><tr><td>8208F866DA3E7833</td><td>迅雷</td><td>hustrong.com</td></tr></table>

customDestinations-ms 及automaticDestinations-ms文件本质是OLE复合文件，相当于一个容器，内部每条记录均为一个快捷方式文件。使用复合文件查看器打开跳转列表文件，可以明显查看每条记录均具有快捷方式文件的签名（\x4C\x00\x00\x00\x01\x14\x02\x00\x00\x00\x00\x00\xC0\x00\x00\x00\x00\x00\x00\x46)，如图5-17所示。

![](images/6747b489d3c629a4120c2e73b53155eef7d74ba2c5dd6f42ac33740484e58cfe.jpg)  
图5–17跳转列表文件内部实际是快捷方式文件

X-WaysForensics执行“进行卷快照”功能后，可直接从跳转列表文件中解析出快捷方式文件，如图5-18和图5-19所示。

![](images/6b53842145d17ae00f812216c4c8d9328eb8d05000599697980bbf504551b388.jpg)  
图5– 18 X-Ways Forensics 解析的跳转列表

跳转列表文件是一种OLE（Object Linking and Embedded）文件，与FAT文件系统并不相同。跳转列表文件包含了两个主要部分：目标列表(DestList)和链接文件本身。目标列表是跳转列表中所有项目的简要清单列表，包括路径、日期时间及每个项目的编号。通过该方式可方便找到具体的项目。跳转文件中还存在一个与每个文件对应的详细信息条目，包含与链接文件相同的信息内容。大多数鉴定工具支持跳转列表文件内容解析，但是解析结果存在差异，鉴定人员也可使用免费工具JumpList Explorer（EricZimmerman工具集）、JumpListsView（Nirsoft工具集）来进行跳转文件的数据解析。

<table><tr><td></td><td rowspan=1 colspan=1>Target attributes</td><td rowspan=1 colspan=1>A</td></tr><tr><td></td><td rowspan=1 colspan=1>Target file size</td><td rowspan=1 colspan=1>0</td></tr><tr><td></td><td rowspan=1 colspan=1>Show Window</td><td rowspan=1 colspan=1>SW NORMAL</td></tr><tr><td></td><td rowspan=1 colspan=1>Target created</td><td rowspan=1 colspan=1>2023-05-04,14:11:26+8</td></tr><tr><td></td><td rowspan=1 colspan=1>Last written</td><td rowspan=1 colspan=1>2023-05-04,14:11:26+8</td></tr><tr><td></td><td rowspan=1 colspan=1>Last accessed</td><td rowspan=1 colspan=1>2023-05-04,14:11:26+8</td></tr><tr><td></td><td rowspan=1 colspan=1>ID List</td><td rowspan=1 colspan=1>Desktop\C:AIM_MODIFIED.txtC=2023-05-0406:11:28</td></tr><tr><td></td><td rowspan=1 colspan=1>Volume type</td><td rowspan=1 colspan=1>Fixed</td></tr><tr><td></td><td rowspan=1 colspan=1>Volume serial</td><td rowspan=1 colspan=1>0x80E1A015</td></tr><tr><td></td><td rowspan=1 colspan=1>Volume name</td><td></td></tr><tr><td></td><td rowspan=1 colspan=1>Local path</td><td rowspan=1 colspan=1>C:AIM_MODIFIED.txt</td></tr><tr><td></td><td rowspan=1 colspan=1>PROPERTYSTORAGE</td><td rowspan=1 colspan=1>[9F4C2855-9F79-4B39-A8D0-E1D42DE1D5F3}</td></tr><tr><td></td><td rowspan=1 colspan=1>Size</td><td rowspan=1 colspan=1>17</td></tr><tr><td></td><td rowspan=1 colspan=1>propID</td><td rowspan=1 colspan=1>7</td></tr><tr><td></td><td rowspan=1 colspan=1>Host name</td><td rowspan=1 colspan=1>strong-pc</td></tr><tr><td></td><td rowspan=1 colspan=1>Volume ID</td><td rowspan=1 colspan=1>[A5B60206-3508-404B-8BEF-FCB5A39C43E9}</td></tr><tr><td></td><td rowspan=1 colspan=1>Object ID</td><td rowspan=1 colspan=1>{8D4E493F-EA42-11ED-97A9-F75B38309C84}</td></tr><tr><td></td><td rowspan=1 colspan=1>MAC Address</td><td rowspan=1 colspan=1>F75B38309C84</td></tr><tr><td></td><td rowspan=1 colspan=1>Timestamp</td><td rowspan=1 colspan=1>2023-05-04,14:11:47+8,Seq6057</td></tr><tr><td rowspan=1 colspan=3>4                                                                                                                  b</td></tr></table>

图5– 19X-Ways Forensics 解析的跳转列表中的快捷方式文件

Windows7系统默认启用跳转列表，默认每个应用程序只会显示最后的10个文件项目。通过任务栏及开始菜单的属性可进行禁用。虽然只显示最后10条，但是在跳转列表文件中记录还有更多。

Windows 8和Windows 10系统下跳转列表也是默认启用的。在Windows 10中，目标列表的二进制结构已经有了小变化，因此导致部分鉴定工具查看跳转列表文件出现一些问题。目标列表和链接件仍然可以使复合件查看器或多数鉴定具进查看。

## 四、时间线

TimeLine(时间线)是Windows101803版本引入的新功能，也有人将其称为“时间轴”。该功能记录最近30天的活动，例如浏览过的网页、打开过的文件。时间线相关信息保存在ActivitiesCache.db 文件中，路径为“%LOCALAPPDATA%\ConnectedDevicesPlatform\L.%USERNAME%\ActivitiesCache.db"”或“%LOCALAPPDATA%\ConnectedDevicesPlatform\<CID>\ActivitiesCache.db",前者是本地账户保存时间线数据的位置，后者是在线账户保存时间线数据的位置。如果系统中存在多个用户，会存在多个ActivitiesCache.db 文件。目前常见的鉴定工具均可解析时间线痕迹。

ActivitiesCache.db是SQLite 数据，可直接使用 DB Browser for SQLite 等工具进行查看。但需要注意的是，如果ActivitiesCache.db同目录中存在“ActivitiesCache.db-shm”和“ActivitiesCache.db-wal”文件，需要将“ActivitiesCache.db"、“ActivitiesCache.db-shm"和“ActivitiesCache.db-wal”导出到同目录再使用SQLite工具进行分析，否则数据可能不完整。

ActivitiesCache.db有7张表，重要信息主要位于Activity表中。Activity 表主要字段及含义如下：

•Id：活动记录的二进制的唯一标识，共16位。

• AppId：可查看对应的应用程序。

• AppActivityId：可解析上网记录从

• StartTime：活动开始时间，Unix Epoch 时间戳。

• EndTime：活动结束时间，Unix Epoch 时间戳。

● ExpirationTime：活动过期时间，Unix Epoch 时间戳，一般是时间开始后的30天。过期的事件将不在时间线中显示。

•Payload：可解析事件除时间外的大部分属性，例如显示的标题、应用程序、网页URL或文件路径等。

使用 DBBrowser forSQLite 等工具可对ActivitiesCache.db数据库文件进行分析，如图5-20所示。

![](images/3f66d1299c96f473784e415bdec53df17c2422824306da31ac5872c1e4c11e5d.jpg)  
图5– 20 使用 DB Browser for SQLite 解析 ActivitiesCache.db

由于时间线功能只显示最近三十天的活动信息，过期的记录一般会被删除，如操作不当可能会覆盖掉时间线痕迹。如果使用仿真的方法查看Windows中的时间线痕迹，建议将虚拟机的时间调整为上次正常关机时间。

## 五、缩略图

为了加快图片的预览速度，操作系统一般会保存图片的缩略图。在Windows 2000系统下，对于NTFS文件系统的分区，当用户以缩略图视图查看图片所在的目录后，每张图片会生成ADS保存缩略图；对于FAT文件系统，当用户以缩略图视图查看存在图片的目录后，该目录中会生成一个带有隐藏和系统属性的Thumbs.db，该文件中包含了图片文件的缩

略图。

在WindowsXP 操作系统中，如果文件夹设置中未勾选“不缓存缩略图”，无论是NTFS分区还是FAT32分区，用户以缩略图视图查看包含图片的目录后，该目录中会生成一个带有隐藏属性的 Thumbs.db 来保存缩略图。

WindowsVista及更高版本的系统中，缩略图集中保存在“%LOCALAPPDATA%\Microsoft\Windows\Explorer\”目录下，文件名为“thumbcache_\*.db”。当用户使用UNC路径访问包含图片的文件夹时，WindowsVista及更高版本的系统依然会在对应的文件夹中生成Thumbs.dlb保存缩略图。UNC路径以双反斜杠(\V)开头，接着是主机名或IP 地址，然后是共享名，再后是目录路径，不同部分用反斜杠隔开。UNC 路径最常见的场景是访问SMB共享目录，用户也可通过UNC路径访问本地数据，例如用户需要访问C盘根目录，则在文件资源管理器中输入“\\127.0.0.1\C \$\”或“\\localhost\C \$\”即可。

早期的Thumbs.db 中不仅包含图像的缩略图，还包含文件的文件名、修改时间以及带盘符的完整路径。Windows XP 中的 Thumbs.db 中包含缩略图、文件名以及文件的修改时间，而Windows Vista 及更高版本的系统生成的 Thumbs.db 仅包含缩略图信息。Thumbcache 文件中除了缩略图信息外，其他信息对于电子数据鉴定来说价值相对较小。

免费工具ThumbsViewer 可解析各种版本的Thumbs.db，如图5–21所示；免费工具Thumbcache Viewer可解析各种 thumbcache 缩略图，如图5–22 所示。这两个工具无论是从数据库文件中解析的缩略图数量，还是解析的元数据，实际效果比常见的鉴定软件更好。

![](images/254b22a448ed1e920d6d43ff81c761a404fd1e46baac2e36ab666e59354a685c.jpg)  
图5– 21 使用 Thumbs Viewer 解析 Thumbs.db

![](images/33fb7d641fb3e043ae41bcf21b9975d1f874f3ba540ba5f71b1f74e6a1c0033b.jpg)  
图5 – 22 使用 Thumbcache Viewer 解析 thumbcache \* .db

## 第四节 USB 设备使用记录分析

## 一、USB设备概述

在电子数据鉴定领域，USB设备，特别是USB存储设备的使用痕迹是重要的分析对象。USB设备的使用痕迹分布在注册表、事件日志等诸多位置。Windows除记录最近使用的文件外，也记录一些设备的使用操作记录。USB设备（如加密狗、优盘、移动硬盘、智能手机等)在与计算机进行连接时，系统将会识别USB设备，并在注册表中生成相关的关键信息。

在%windir%\System32\Config\SYSTEM注册表中记录Windows 系统中插入过的USB设备。通过鉴定软件或注册表工具查看SYSTEM 注册表文件，找到 ControlSet<ID>\Enum\USB及 ControlSet<ID>\Enum\USBSTOR。

## 二、USB设备注册表痕迹

## (一)设备型号及序列号

Widnows操作系统会自动记录USB设备连接的相关信息，将其存储于注册表SYSTEM文件中，该文件通常默认位于%windir%\System32\Config文件夹中。使用鉴定软件解析注册表文件SYSTEM的内容，可找到USB设备相关注册表信息的存储位置（\ControlSet<ID>\Enum\)。USB设备一般可分为两种类型，一种是不可存储数据的设备（如USB接口的键盘、鼠标、加密狗等），另一种是数据存储设备（光盘、优盘、移动硬盘及智能手机等）。不可存储数据的设备的注册表信息存储于\ControlSet<ID>\Enum\USB，可存储数据的设备的注册表信息存储于\ControlSet<ID>\Enum\USBSTOR,其中USBSTOR是 USB STORAGE的缩写，如图5–23所示。

![](images/8131f5802bc934da9ddbf27cb699436d6b39abf3d7c6ff9a9d23b5e7100f8770.jpg)  
图5-23 注册表USBSTOR 键保存的USB 存储设备信息

USB存储设备连接计算机后，会在USBSTOR 键下生成一个设备类ID，设备类ID形如“Disk&Ven_Kingston&Prod_DataTraveler_3.0&Rev_"。部分字段含义如下：

•Disk：该设备是一个USB存储介质，而不是不可存储的设备(如加密狗)

• CdRom：该设备是一个光盘存储介质

•Ven：Vendor厂商的缩写

•Prod：Product产品型号的缩写

•Rev:Revision 修订版缩写

设备类ID键的创建时间一般被认为是对应USB存储设备第一次连接计算机的时间。设备类ID注册表键有一个子键，名称中包含了设备的序列号。图5–24中Kingston DataTraveler3设备的序列号为“E0D55EA53550F45068A50D81”。需要注意的是，如果序列号第二位是“&”符号，说明该序列号是Windows随机生成的，设备本身并没有唯一的序列号。

在\ControlSet<ID>\Enum\USBSTOR\<USB 设备>\<序列号>\Device Parameters \Partmgr下，还保存着DiskId字段，如图5-24 所示，此字段可以用来关联其他位置的USB 痕迹。此外，该位置还保存着分区表相关信息。

![](images/429dd3e23bf08f9144e103e5735cea3fd25a205bdbaf33605bafc1c9ec19c68c.jpg)  
图5- 24 USBSTOR中保存的DiskId信息

除USBSTOR 键外，DevicesClasses键也记录了USB设备的型号、序列号等信息，如图5–25所示。该注册表键的具体位置为“\ControlSet<ID>\Control\DeviceClasses\{53F56307-B6BF-

11D0-94F2-00A0C91EFB8B}√”。上述注册表路径中的“53F56307-B6BF-11D0-94F2-  
00A0C91EFB8B”是磁盘的类GUID[9]。

![](images/4b9157e9e0abb9ef4ee59cfd144952e89a137a9fad7922326f470cf9b40b3ae6.jpg)  
图5-25 注册表 DeviceClasses键

## (二)挂载的盘符

注册表SYSTEM文件中的“MountedDevices”保存了盘符最后关联的分区信息，如果同设备再次连接计算机，且该盘符没有被其他设备占用的情况下，会优先分配上次使用过的盘符。MountedDevices 中保存的记录均以 REG_BINARY数据类型进行存储，其中含有\DosDevices的项目对应的值的前4个字节（十六进制值)为磁盘签名，第5个至第12个字节为卷在物理磁盘中的偏移位置，将此8个字节长度的数据转化为十进制后即卷的头部在物理磁盘中的偏移字节数，可使用RegistryViewer直接查看，如图5–26所示。

![](images/1ec52177c70a93b1375e93f35cf06299e6ce718b753481e6397af11c1ea21834.jpg)  
图5–26 MountedDevices中 USB 设备相关的记录

计算机鉴定工具在添加证据文件后可自动准确解析出磁盘中分区分配的盘符，有助于鉴定人员分析如快捷方式文件中包含的盘符与实际分区的对应关系，如图5-27所示。

注册表SOFTAWARE文件中的“\Microsoft \Windows Portable Devices”保存了包含USB存储设备在内的便携设备的FriendlyName，设备友好名称可能是分配的盘符，也可能是卷标。相关记录的路径中包含了设备型号及序列号信息，如图5–28所。

![](images/18dbaaa0c5923e07d9b797a16103465a60aa4a86f8dba801f307a5a222edc7ab.jpg)  
图5-27 取证神探动解析分区对应的盘符信息

![](images/06a5173b22fa08ea1bf6492cc32c7ca52f9dd0b0bfc440f9593292f451a9c0e1.jpg)  
图5-28 WPD注册表键中USB设备分配的盘符

## (三)卷标

WPD注册表键中包含了卷的相关信息，鉴定员可检验出计算机曾经接的USB存储设备的卷标信息，如图5–29所。

![](images/e355bd981481ad28db937964e249a863940e18dfc3ce3c182d33c91f468039ca.jpg)  
图5-29 WPD注册表键中的卷标信息

## (四)卷序列号

卷序列号（Volume Serial Number，简称VSN)是Windows 操作系统在格式化后给卷分配的唯一性标识。在Windows Vista 及 Windows 7 中，ReadyBoost 功能会在注册表中生成 EMDMgmt键，该键的具体位置为注册表文件Software 中的“\Microsoft\WindowsNT\CurrentVersion\EMDMgmt”。每个USB存储设备会在该键下生成一个子键，子键名称中除了包含型号、序列号等信息，还会包含一个十进制的卷序列号。

图5-30为2012年司法鉴定科学研究院能力验证检材中的注册表截图。图中高亮的注册表键，记录了一个序列号为“0902100000000000778262176”的ADATA优盘，十进制的卷序列号为“3565576558”，换算成十六进制则是D486616E。

![](images/6fd777e4a0bd42191d7d04a1da767272ef35397a21b9761d6807f8792515f6c3.jpg)  
图5-30注册表 EMDMgmt键中的卷序列号

检材中的快捷方式文件“4D5D1281-0000000A.Ink”显示用户打开过“E：\新建文件夹（2）\篡改\4D5D1281-0000000A.eml”，该文件所在分区的卷序列号为D486616E。结合“HKLM\SYSTEM\MountedDevices\”可知盘符E对应序列号为“09021000000000000778262176”的USB设备。以上信息正好与EMDMgmt键中的记录相吻合，如图5–31和图5–32所示。

![](images/50acdcbf00f92e6aab517682b9953d0eef30cc3afd7ab67317e2e33edb0b4619.jpg)  
图5–31 X-Ways Forensics解析快捷方式文件

## 三、USB设备安装日志

SetupAPI会记录设备的加载过程。在Windows 2000/2003/XP 中，对应的日志文件为“%systemroot% \setupapi.log"，在Windows Vista 到Windows 11 系统中，对应的日志文件为“%

![](images/19be59ca813abb316b2fd903fb9b7b8dac3ca938f183e961eb5a6065fd7a9b47.jpg)  
图5-32使X-WaysForensics注册表查看器查看曾经挂载的设备

systemroot%\INF\setupapi.dev.log”。USB设备次连接计算机时，会在SetupAPI志中产相关的记录，这些记录是USB设备次连接时间的重要依据。

## 四、USB设备事件志

在Windows 7系统中，事件志Microsoft-Windows-DriverFrameworks-UserMode%4Operational.evtx中会有系列的事件记录USB设备的连接及断开连接的过程。

当USB设备连接到计算机，会产ID为2100、2003、2004、2006的记录，它们的事件来源均为“DriverFrameworks-UserMode”，般可以将ID为2003的记录作为USB设备连接的记录。ID为2003的记录中包含设备的型号及序列号等信息，如图5-33所①。

![](images/2bdff97841fe09cde4f31282b630b49abfa74f2b814ffe31ee60ca9ff266d5e9.jpg)  
图5-33 Windows7系统中USB存储设备连接的事件日志

当USB设备从计算机上断开连接，会成ID为2100、2102的记录，事件来源均为“DriverFrameworks-UserMode”，般可以将ID为2102的记录作为USB设备断开连接的标志。需要注意的是，并每次USB连接记录都会对应产条断开连接的记录。ID为2102的记录，如图5-34所。

![](images/63e5b013f3dc707a2cab3bbf91de630f04e44cfc88e69599c78dad0483e2944e.jpg)  
图5-34 Windows7系统中USB设备断开连接的事件志

在Windows 10及Windows11系统中,Microsoft-Windows-DriverFrameworks-UserMode%4Operational.evtx志不复存在,但有新的事件志记录了USB存储设备每次的连接及断开连接的事件,其中最重要的是分区诊断志，对应的志件为“Microsoft-Windows-Partition%4Diagnostic.evtx”。

分区诊断志记录了系统发现的新的分区的信息，包括内置硬盘分区和USB存储设备分区的相关信息。前Windows10/11中分区诊断志中所有的事件来源均为“Partition”，事件ID均为“1006”，如图5-35所示。

![](images/76a8d7515d0cc2fb043018acd7eb1296e6bef17a4ce0f8e6131601d7dbd0b29e.jpg)  
图5-35 Windows10系统中的分区诊断志

分区诊断志中记录了设备的详细参数信息,但这些信息在Windows事件查看器的“常规”视图中法查看，需在“详细信息”视图进查看。主要字段及其含义见表5-11。

表5-11 详细信息
<table><tr><td>字段</td><td>含义</td><td>备注</td></tr><tr><td>DiskNumber</td><td>磁盘号</td><td>与磁盘管理器(diskmgmt.msc)中查看的磁盘号一致</td></tr><tr><td>IsSystemCritical</td><td>是否是系统分区</td><td>“true”代表系统分区,“false”代表非系统分区</td></tr><tr><td>BytesPerSector</td><td>每扇区字节数</td><td></td></tr><tr><td>Capacity</td><td>磁盘容量</td><td>单位为字节，注意不是分区容量</td></tr><tr><td>Manufacturer</td><td>制造商</td><td>部分记录此字段为空</td></tr><tr><td>Model</td><td>型号</td><td></td></tr><tr><td>Revision</td><td>固件版本</td><td></td></tr><tr><td>SerialNumber</td><td>序列号</td><td>NVMe 协议的磁盘此字段不准</td></tr><tr><td>ParentId</td><td>父系ID</td><td>此字段中包含设备使用的协议，例如PCI或USB</td></tr></table>

使EventLogExplorer动解析2022年能验证(2022SF-CNAS026)镜像computer.E01中的分区诊断志，如图5–36所。

![](images/3ddf191e5071b68b693fee76b8c6c3dc2c909a7c0b7826295317e5a0a44019a1.jpg)  
图5-36 使EventLogExplorer解析分区诊断志

## 第五节 程序运行痕迹分析

Windows系统运过程中，对使用频率的应用程序进记录，包括应用程序名称、路径、运次数、最后次执时间等信息。记录的信息存在于注册表中的UserAssist键中。

用户注册表文件NTUSER.DAT记录用户的各种配置信息，通过鉴定软件或注册表具打开该文件，找到“\SOFTWARE\MICROSOFT\WINDOWS\CURRENTVERSION\EXPLORER\UserAssist”。Windows系统中的应用程序运行记录保存于UserAssist下的两个GUID命名的子键中，不同的操作系统版本有所不同，见表5-12。

表5-12注册表中UserAssist键信息
<table><tr><td>子键名称(GUID)</td><td>记录信息</td><td>备注</td></tr><tr><td>5E6AB780-7743-11CF-A12B-00AA004AE837}</td><td>Internet Toolbar</td><td>Windows XP版本</td></tr><tr><td>{75048700-EF1F-11D0-9888-006097DEACF9}</td><td>Active Desktop</td><td>Windows XP版本</td></tr><tr><td>{CEBFF5CD-ACE2-4F4F-9178-9926F41749EA}</td><td></td><td>Vista以上版本</td></tr><tr><td>{F4E57C4B-2036-45FO-A9AB-443BCFE33D9F}</td><td></td><td>Vista 以上版本</td></tr></table>

Vista以上操作系统使用的GUID子键名称均固定有两个，分别为{CEBFF5CD-ACE2-4F4F-9178-9926F41749EA}和{F4E57C4B-2036-45F0-A9AB-443BCFE33D9F}。在 X-WaysForensics注册表查看器中浏览UserAssist记录时，可直接对数据进解码。

## 一、Prefetch 预读文件

Windows引入了预读文件（Prefetch)加速程序加载及启动速度的机制。预读文件在启动过程中通过将数据和程序的代码页载入内存，从而实现程序的快速加载。

在系统及程序启动过程中，预读文件用于跟踪调用文件，该文件存储于%WINDOWS%\Prefetch目录。文件名是以应用程序名加上横线及文件路径的哈希值对应的十六进制，并以PF作为文件扩展名，如图5-37所示。

![](images/5206c2e0c2f119d2ba57f41e19104f88ca408f6526977a1da153f568c14477e6.jpg)  
图5–37 Windows Prefetch文件

Prefetch预读文件的文件头部签名为：

Windows XP: 11 00 00 00 53 43 43 41 0F 00 00 00

• Windows Vista/7: 17 00 00 00 53 43 43 41 00 00 00

• Windows 8: 1A 00 00 00 53 43 43 11 00 00 00

• Windows 10/11: 4D 41 4D 04

## (）WindowsXP版本预读件

在电子数据鉴定中，预读文件可用于分析应用程序的执情况，包括最后运行时间及运次数。WindowsXP系统的Prefetch预读件结构见表5-13。

表5-13 WindowsXP预读件(PF)件结构
<table><tr><td colspan="2">字 节</td><td rowspan="2">数据</td><td rowspan="2">格式</td></tr><tr><td>偏移量</td><td>长度</td></tr><tr><td>0x04</td><td>4</td><td>头部特征字</td><td>SCCA</td></tr><tr><td>0x10</td><td>60</td><td>应用程序名称</td><td>Unicode</td></tr><tr><td>0x78</td><td>8</td><td>最后运行日期</td><td>FILETIME</td></tr><tr><td>0x90</td><td>4</td><td>执行次数</td><td>十六进制(HEX)</td></tr></table>

执次数是指应程序曾经运过的次数，如果程序是作为操作系统启动过程的部分，那么该执次数不会更新。因此执次数的准确性只适于般的第三应程序，不适于系统启动过程相关的程序。

PF件包含了程序启动前10秒过程访问的件及件夹的信息记录。对程序启动前10秒访问的件及件夹的分析可能很有帮助，有助于发现隐藏件夹、对应的户账号信息或了解程序是否从外部存储介质运。

## (）Vista/Windows7版本预读件

WindowsVista和Windows7操作系统也同样存在预读件，然预读件(PF)的内部结构有些轻微的变化，主要体现在偏移位置差异，见表5-14。

表5-14 WindowsVista/Windows 7预读文件(PF)文件结构
<table><tr><td colspan="2">字节</td><td rowspan="2">数据</td><td rowspan="2">格式</td></tr><tr><td>偏移量</td><td>长度</td></tr><tr><td>0x04</td><td>4</td><td>头部特征字</td><td>SCCA</td></tr><tr><td>0x10</td><td>60</td><td>应用程序名称</td><td>Unicode</td></tr><tr><td>0x80</td><td>8</td><td>最后运行日期</td><td>FILETIME</td></tr><tr><td>0x98</td><td>4</td><td>执行次数</td><td>十六进制(HEX)</td></tr></table>

## （三）Windows8及以上版本的预读件

Windows8及以上操作系统版本持保存多达1024个独的预读件。个程序可以有多个预读件,例如，程序从个件夹移动到另个件夹，那么就会成不同的预读件。预读件结构也有了较的变化，新的件结构允许存储程序的最后8次运时间。

当新的期时间条增加到预读件中时，程序的执次数才会增加。旦程序执次数达到10,Windows8系统将周期性地更新期时间及执次数，见表5-15。

表5–15 Windows 8 预读文件结构
<table><tr><td colspan="2">字节</td><td rowspan="2">数据</td><td rowspan="2">格式</td></tr><tr><td>偏移量</td><td>长度</td></tr><tr><td>0x04</td><td>4</td><td>头部特征字</td><td>SCCA</td></tr><tr><td>0x10</td><td>60</td><td>应用程序名称</td><td>Unicode</td></tr><tr><td>0x80</td><td>8</td><td>最后运行日期</td><td>FILETIME</td></tr><tr><td>0x88</td><td>8</td><td>倒数第 2 次运行日期</td><td>FILETIME</td></tr><tr><td>0x90</td><td>8</td><td>倒数第 3 次运行日期</td><td>FILETIME</td></tr><tr><td>0x98</td><td>8</td><td>倒数第 4 次运行日期</td><td>FILETIME</td></tr><tr><td>0xA0</td><td>8</td><td>倒数第5 次运行日期</td><td>FILETIME</td></tr><tr><td>0xA8</td><td>8</td><td>倒数第 6 次运行日期</td><td>FILETIME</td></tr><tr><td>0xB0</td><td>8</td><td>倒数第7 次运行日期</td><td>FILETIME</td></tr><tr><td>0xB8</td><td>8</td><td>倒数第8次运行日期</td><td>FILETIME</td></tr><tr><td>0x98</td><td>4</td><td>执行次数</td><td>十六进制(HEX)</td></tr></table>

## （四)Windows 10 版本预读文件

从Windows10开始，系统使用的预读文件内部采用了压缩机制。从鉴定角度讲，该变化不会影响预读功能，但会导致工具无法查看预读文件内容。Windows10 预读文件存储的位置、扩展名均不变，但预读文件头部变为了\x4D\x41\x4D\x04。

Prefetch文件中保存文件的运行次数、每次的运行时间、最后一次运行时加载的相关文件以及对应的加载时间，此外，Prefetch文件中还保存应用程序所在分区的卷序列号。不同鉴定软件对 Prefetch文件的解析程度不一。X-Ways Forensics 和取证大师等鉴定软件对预读文件解析均较为全面。此外，也可使用Nirsoft 工具集中的WinPrefetchView、Eric Zimmerman工具集中的PECmd 等免费工具查看Windows10的预读文件。

Prefetch 预读文件中可能包含用户访问的文件，由于Windows 10开始Prefetch 文件是压缩的，无法通过关键字搜索的方法搜索到Prefetch文件内部的文件记录，这些痕迹需要用户手动检查。

## 二、ShimCache

ShimCache也被称为AppCompatCache，是WindowsXP引入的一个应用程序兼容性数据库组件。在WindowsXP系统中，ShimCache位于注册表文件SYSTEM 中的“\ControlSet<序号>\Control\Session Manager\AppCompatibility"，在 Windows Vista 至 Windows 11 系统中，ShimCache位于注册表文件SYSTEM中的“ControlSet<序号>\Control\Session Manager\AppCompatCache"

ShimCache中记录了应用程序的完整路径信息以及记录最后更新时间。需要注意的是，ShimCache记录并不意味着应用定被执过，因为磁盘中所有的应用程序在执前就被添加到 ShimCache 中。ShimCache 记录条数有限，达到最大条数后会滚动覆盖较早的记录。在Windows XP 中,ShimCache 最多保存96 条记录，Vista 至Windows 11 系统中 ShimCache 最多保存1024条记录。目前支持解析ShimCache 痕迹的鉴定软件不多，可使用Magnet Axiom、X-Ways Forensics 及 ArtiFast 等鉴定软件进行分析。

## 三、AmCache

在Windows 7 系统中， RecentFileCache. bcf 文件(% SystemRoot%\appcompat\ ProgramsiRecentFileCache.bef)被用来记录应用程序的兼容性情况，该文件从Windows8开始被替换为Amcache.hve(%SystemRoot%\appcompat\Programs\RecentFileCache.bcf)[12]，该文件为注册表文件格式，可采用注册表查看器或常规鉴定软件进行分析。

Amcache.hve中保存着可执行文件的完整路径、大小、文件修改时间、SHA-1值以及版本号等程序元数据。需要注意的是，AmCache只能证明某应用程序曾经存在过，但并不能证明该应用被执过。

对Amcache.hve文件进行分析，发现曾存在应用程序“C：\Program Files\7-Zip\7z.exe”，大小为545280字节，文件SHA-1为“E4E4D66639097862A59410DECF5DB146CEAA5D19”，软件版本为22.00，如图5–38所示。

![](images/9cb792469f4a282cc7911588686d17f1ed1fc042d89578e3e732620559c3eb42.jpg)  
图5–38 使用X-Ways Forensics 注册表查看器直接查看AmCache

Magnet AXIOM鉴定软件，对Windows 系统AmCache 的痕迹解析较为完整全面，包含快捷方式信息、程序信息及设备信息等，如图5–39所示。

## 四、SRUM(系统资源使用监控)

SRUM(System Resource Usage Monitor）是Windows8引入的功能，旨在监控应用程序、服务以及网络连接的相关情况，是诊断策略服务(Diagnostic Policy Service，即 DSP）的一部分，数据保存在“%SystemRoot%\System32\sru\SRUDB.dat"”。

![](images/bb2e2d93d75b6c3624f6c4ad742eee7895d9d436972c0df6bcae08ff555cd4c6.jpg)  
图5-39 AXIOM解析出的AmCache痕迹信息

SRUDB.dat是ESE数据库，各表的数据来源保存在注册表“HKLM\SOFTWARE\Microsoft\WindowsNT\CurrentVersion\SRUM\Extensions\”中,如图5–40所,不同的系统会略有差异。

![](images/9b0d731003b1a64c15f280f8abd26e946f182f0905237d34a3aff75b9ea6d8b4.jpg)  
图5-40 注册表中的SRUM相关数据

SRUDB.dat中的数据并实时记录，是每时以及系统关机时写，临时数据保存在注册表等位置。SRUDB.dat可以免费具ESEDatabaseView打开，但该具查看信息并不是很直观。MagnetAXIOM商业鉴定软件则可较好地解析SRUM数据。

SRUDB.dat中的应程序资源使记录价值较,因为记录着所有在系统中运过的应程序，即使部分应程序已经被清除。

## 五、BAM/DAM

BAM和DAM分别是“Windows Background Activity Moderator”和“Windows Background/

DesktopActivity Moderator”的缩写，是Windows 10 开始引入的包含应用执行记录的痕迹，在注册表中的位置分别为“HKLM\SYSTEM\CurrentControlSet\Services\bam\State\UserSettings\<用户 SID>"和“HKLM\SYSTEM\CurrentControlISet\Services\dam\State\UserSettings\<用户 SID>"。

BAM/DAM中记录了各用户最近运过的应用程序的完整路径以及最后运时间。鉴定员可使用鉴定软件工分析BAM/DAM在注册表中保存的信息，检验执过的应用程序记录，如图5-41所示。

![](images/0bac5134c68dfe43ad191efedaa9ea44384d1d6dfc74fd9ddcf7a467deda3aa6.jpg)  
图5–41使用X-Ways Forensics 注册表查看器查看BAM记录

## 第六节 日志分析

Windows 操作系统在运行过程中会产生大量的日志信息，如Windows 事件日志（EventLog)、NTFS日志、Windows 服务器系统的 IIS日志、FTP日志、Exchange Server 邮件服务器日志、MS SQL Server 的数据库日志等。不管是 PC还是服务器中，Windows事件日志都存在，也是电子数据鉴定中的重要分析项目。此外还有其他相关的日志，如新设备接入产生的日志(setupapi.dev.log)等。此外，还有系统内置软件及第三方软件（如杀毒软件)等均可能在磁盘中保存相关的日志文件。

## 一、Windows 事件日志

## (一)Windows 事件日志概述

事件是统一由Windows的事件日志服务（Windows Event LogService)来统一收集和存储。它存储了来自各种数据源的信息记录，常称之为“事件日志”。事件日志为操作系统及关联的应用程序提供了一种标准化、集中式地记录重要软件及硬件信息的方法。事件日志提供了丰富的历史信息，可帮助发现系统或安全问题，此外还可以对被入侵的系统进行部分虚拟现场的还原，掌握黑客入侵系统的相关痕迹及时间点[118]。

## (二)Windows 事件日志版本

Windows事件日志基本目前可分为：EVT和EVTX文件格式。

## (三)Windows 事件日志数据存储及相关特征

Windows2000/XP/2003Server等操作系统采用EVT格式存储事件日志，其默认存储位置为：%SystemRoot%\System32\Config。

Windows事件日志类别主要包括系统（System）、安全性(Security）、应用程序（Application)及部分自定义日志。系统内置的三个事件日志文件默认大小均为512KB，如大于512KB时，默认系统将覆盖超过7天的日志记录。事件日志记录了错误、失败、成功、信息及警告事件，常见的Windows事件日志文件存储位置可见表5–16。

表5–16常见Windows 事件日志类别
<table><tr><td>事件类别</td><td>描述</td><td>存储位置及文件名</td></tr><tr><td>系统</td><td>包含系统进程、设备磁盘活动等。事件记录了设备驱动 无法正常启动或停止，硬件失败，重复IP地址，系统进 程的启动、停止及暂停等行为</td><td>%System Root% \System32\Config\ SysEvent.evt</td></tr><tr><td>安全性</td><td>包含安全性相关的事件，如用户权限变更、登录及注销、9 文件及文件夹访问、打印等信息</td><td>%System Root%\System32\Config\ SecEvent.evt</td></tr><tr><td>应用程序</td><td>包含操作系统安装的应用程序软件相关的事件。事件 日志包括了错误、警告及任何应用程序需要报告的信 息，应用程序开发人员可以决定记录哪些信息</td><td>%System Root%\System32\Config\ AppEvent.evt</td></tr><tr><td>自定义</td><td>在Windows Server服务器中一般还存在目录服务、DNS 服务及文件复制服务等事件日志记录</td><td>%System Root% \System32\Config\</td></tr></table>

微软从WindowsVista操作系统开始采用全新的 EVTX 格式。新版事件日志的文件结构、日志类型及日志存储位置均发生较大的变化，见表5–17。默认的事件日志存储位置为：%SystemRoot%\System32\winevt\Logs。

表5– 17 Windows 事件日志文件(EVTX)
<table><tr><td>类型</td><td>事件类别</td><td>描述</td><td>文件名</td></tr><tr><td rowspan="3">Windows日志</td><td>系统</td><td>包含系统进程、设备磁盘活动等。事件记录了设备 驱动无法正常启动或停止，硬件失败，重复IP地 址，系统进程的启动、停止及暂停等行为</td><td>System.evtx</td></tr><tr><td>安全</td><td>包含安全性相关的事件，如用户权限变更、登录及Security.evtx 注销、文件及文件夹访问、打印等信息</td><td></td></tr><tr><td>应用程序</td><td>包含操作系统安装的应用程序软件相关的事件。事Application. 件日志包括了错误、警告及任何应用程序需要报告 的信息，应用程序开发人员可以决定记录哪些信息</td><td>evtx</td></tr><tr><td>应用程序及 服务日志</td><td>Microsoft</td><td>Microsoft 文件夹下包含了200 多个微软内置的事件日 详见日志存储 志分类，只有部分类型默认启用记录功能，如远程桌面 客户端连接（TerminalServices-ClientActiveXCore）、无 线网络（WLAN-AutoConfig）、有线网络（Wired- AutoConfig）、设备安装（UserPnp）等相关日志</td><td>目录对应文件</td></tr><tr><td rowspan="3">应用程序和 服务日志</td><td>Microsoft Office Alerts</td><td>微软Office应用程序（包括Word/Excel/PowerPoint 等）的各种警告信息，其中包含用户对文档操作过 程中出现的各种行为，记录有文件名、路径等信息</td><td>OAlerts.evtx</td></tr><tr><td>Windows PowerShell</td><td>Windows自带的 PowerShell应用的日志信息</td><td>Windows PowerShell.evtx</td></tr><tr><td>Internet Explorer</td><td>IE浏览器应用程序的日志信息，默认未启用，需要 通过组策略进行配置</td><td>Internet Explorer.evtx</td></tr></table>

WindowsVista及以上版本的Windows事件日志有较大的变化。通过系统自带的事件日志查看器查看其分为“Windows志”和“应程序和服务志”两类。Windows志中包含早期版本原有的系统、安全和应程序等,还新增设置及已转发事件（默认禁)志。应程序和服务志是个新分类，主要包含了系统内置的各种应程序和服务产的志。

系统内置的三个核心日志文件默认大小均为20480KB（即20MB），超过20480KB时，默认系统将优先覆盖过期的志记录。其他应用程序和服务志多数最大件默认为1028KB，超过最限制后也优先覆盖过期的志记录。因此，在电数据鉴定过程中有时会遇到案发期间的志无法在现有的事件志文件中找到，需要通过对磁盘分区的未分配空间进恢复，最大限度地找到相关的日志文件的数据段。

此外，操作系统还支持接收远程计算机的Windows事件日志数据，因此，在鉴定过程中，还需要注意待鉴定的计算机硬盘中存储的志件是否为本机的志数据。

## (四)事件日志查看与鉴定

## 1.事件日志文件内容查看

事件日志文件通常可采用商业化鉴定工具直接进行分析，如EnCaseForensic、FTK、X-Ways Forensics等。多数鉴定软件均持EVT和EVTX两种文件格式，可直接加载进行分析。此外,也可采Windows系统带的事件志查看器或第三方免费的鉴定辅助具（如EventLog Explorer)来进行数据的查看与分析。

## 2.常见的Windows 事件的分析

Windows事件志中记录的信息中，关键的要素包含事件级别、记录时间、事件来源、事件ID、事件描述、涉及的用户、计算机、操作代码及任务类别等。其中事件ID与操作系统版本有关，同类事件在不同操作系统中的事件ID不完全相同，最大的差异主要体现在第一版(EVT)和第二版(EVTX)的事件日志，因此在鉴定过程中需特别注意，在使用事件ID进行过滤搜索时，需要考虑到操作系统版本的差异，如表5–18和表5–19所示。

表5–18常见Windows事件类型及说明
<table><tr><td>类型</td><td>日志文件名</td><td>事件分类</td><td>事件ID</td><td>说明</td></tr><tr><td rowspan="2">用户登 录注销</td><td>Microsoft-Windows-</td><td>收到登录通知</td><td>1</td><td>系统收到用户登录请求</td></tr><tr><td>User Profile Service% 40perational.evtx</td><td>完成处理登录通知</td><td>2 统</td><td>系统完成登录处理，即用户成功登录系</td></tr><tr><td>类型</td><td>日志文件名</td><td>事件分类</td><td>事件IⅢ</td><td>说明</td></tr><tr><td rowspan="4">用户登</td><td rowspan="4">Microsoft-Windows- User Profle Service%</td><td>收到注销通知</td><td>3</td><td>系统收到用户注销请求</td></tr><tr><td>完成处理注销通知</td><td>4</td><td>系统完成用户注销处理，即用户在系统 中成功注销</td></tr><tr><td>用户配置注册表文件 加载</td><td>5</td><td>加载用户注册表文件NTUSER.DAT及 UsrClass.dat</td></tr><tr><td>加载用户配置文件夹</td><td>67</td><td>本地配置文件夹（UserProfile）配置加</td></tr><tr><td rowspan="2">系统时 间修改</td><td>System.evtx</td><td>修改系统时间操作</td><td></td><td>数据来源必须是 Kernel-General,通常 生成两条记录,其中一条日志记录了原 有系统时间及变更后的系统时间，并记 录系统更改原因为“更改原因：应用程 序或系统组件更改了时间”。另一条记 录则是对系统时间精准度调整(纳秒 级)，只取最后系统时间纳秒数值前三</td></tr><tr><td>Security.evtx</td><td>修改系统时间操作</td><td>4616</td><td>位(做四舍五入) 通常生成两条记录，其中一条日志记录 了系统时间修改相关的账号名、安全 ID、进程ID、进程名称与路径、原有系 统时间及变更后的系统时间等信息。 另一条记录则是对系统时间精准度调 整(纳秒级)，只取最后系统时间纳秒 数值前三位(做四舍五入)</td></tr><tr><td rowspan="6">无线网 络自动 配置</td><td rowspan="3">WLAN-AutoConfig% 40perational.evtx</td><td>启动无线网络自动连 接配置</td><td>8000</td><td>自动配置服务已开始连接无线网络，记 录无线网卡名称及原有保存的无线网 络SSID名称</td></tr><tr><td>成功接入原有保存的 无线网络</td><td>8001</td><td>自动配置服务已成功连接到无线网络</td></tr><tr><td>开始无线网络关联</td><td>11000</td><td>已开始无线网络关联，信息包括无线网 卡名称、本地网卡MAC地址及原有保 存的无线网络SSID名称等信息</td></tr><tr><td rowspan="4"></td><td>无线网络关联成功</td><td>11001</td><td>无线网络关联成功</td></tr><tr><td>无线安全功能已启动</td><td>11010</td><td>无线安全功能已启动</td></tr><tr><td>无线安全功能成功</td><td>11005</td><td>无线安全功能成功</td></tr><tr><td>Microsoft-Windows- 网络已连接</td><td>10000</td><td colspan="2">网络已连接</td></tr><tr><td>40perational.evtx System.evtx</td><td>NetworkProfile% 网络已断开连接</td><td></td><td>10001 网络已断开连接</td><td>来源 DriverFrameworks-UserMode，正在</td></tr><tr><td>即插即 用设备</td><td></td><td>以用户模式安装驱动 程序包</td><td></td><td>设备安装使用用户模式驱动程序框架 版本的驱动程序，包含设备厂商、品牌 及序列号 SN 等信息</td></tr><tr><td>类型</td><td>日志文件名</td><td>事件分类</td><td>事件ID</td><td>说明</td></tr><tr><td rowspan="4">即插即 用设备 Microsoft-Windows- Kernel-PnP% 4Configuration.evtx</td><td>System.evtx</td><td>已成功安装驱动程序 包</td><td>10100</td><td>来源 DriverFrameworks-UserMode，已成 功安装驱动程序包</td></tr><tr><td rowspan="3"></td><td>为USB 存储介质加载 INF驱动程序</td><td>20001</td><td>来源UserPnp,记录设备实例信息，含设 备厂商、品牌及序列号 SN 等信息</td></tr><tr><td>为USB 介质添加磁盘 服务</td><td>20003</td><td>来源UserPnp,记录设备实例信息，含设 备厂商、品牌及序列号SN等信息</td></tr><tr><td>设备已配置 设备已启动</td><td>400 410</td><td>已配置设备，如为USB设备准备驱动程序 已启动设备</td></tr><tr><td rowspan="5">远程桌 面连接</td><td rowspan="5">Microsoft-Windows- TerminalServices- RDPClient% 4Operational.evtx</td><td>设备需要进一步安装 正在尝试连接到服务器</td><td>430</td><td>设备需要进一步安装</td></tr><tr><td>已成功连接到服务器</td><td>1024 1025</td><td>记录远程终端服务器的IP地址 已成功连接到服务器</td></tr><tr><td>已断开服务器连接</td><td>1026</td><td>已断开服务器连接</td></tr><tr><td>已使用会话连接到服 务</td><td>1027</td><td>已使用会话连接到域，记录的信息含有 远程服务器的计算机名（并非用户输入</td></tr><tr><td>SSL加密通信检测 远程登录用户名 1029</td><td>1028</td><td>该信息，而是客户端自动获取远程服务 器的计算机名并将其记录） 服务器支持SSL加密通信是否支持 记录远程登录使用的用户名经过 SHA256及Base64转换，记录内容如</td></tr><tr><td rowspan="3">远程终 端服务 访问</td><td rowspan="3">Microsoft-Windows- TerminalServices- LocalSessionManager% 4Operational.evtx 会话重新连接成功</td><td>会话登录成功</td><td></td><td>Base64 (SHA256(UserName）） = WAlZ81aqzLQmoWEfQivmPQwJxIm/ XQcDjplQdjznr5E=-</td></tr><tr><td>已收到 Shell启动通知</td><td>21 22</td><td>远程终端服务：会话登录成功 远程终端服务：已收到 Shell启动通知</td></tr><tr><td>会话注销成功 会话已断开连接</td><td>23 24</td><td>远程终端服务：会话注销成功 远程终端服务：会话已断开连接</td></tr></table>

表5-19常见Windows账户相关事件及说明 [121]
<table><tr><td>事件ID</td><td>说 明</td></tr><tr><td>528</td><td>用户成功登录计算机</td></tr><tr><td>529</td><td>用户使用系统未知的用户名登录，或已知用户使用错误的密码登录</td></tr><tr><td>530</td><td>用户账户在许可的时间范围外登录</td></tr><tr><td>531</td><td>用户使用已禁用账户登录</td></tr><tr><td>532</td><td>用户使用过期账户登录</td></tr><tr><td>533</td><td>不允许用户登录计算机</td></tr><tr><td>534</td><td>用户使用不许可的登录类型(如网络、交互、远程交互)进行登录</td></tr><tr><td>535</td><td>指定账户的密码已过期</td></tr><tr><td>536</td><td>Net Logon 服务未处于活动状态</td></tr><tr><td>537</td><td>登录由于其他原因而失败</td></tr><tr><td>538</td><td>用户注销</td></tr><tr><td>539</td><td>试图登录时账户已被锁定。此事件表示攻击失败并导致账户被锁定</td></tr><tr><td>540</td><td>网络登录成功</td></tr><tr><td>682</td><td>用户重新连接了已断开的终端服务会话</td></tr><tr><td>683</td><td>用户在未注销的情况下断开终端服务会话</td></tr></table>

## 3.EVT事件日志文件结构

EVT事件志件是种进制格式的件，件头部签名为六进制300000004C664C65(LfLe)，如图5-42所示。全新的事件志件，默认情况下，事件志记录均按顺序进存储，每条记录均有的记录结构特征(LfLe）。

<table><tr><td rowspan=1 colspan=1>SysEvent.Evt</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td rowspan=1 colspan=2>offset</td><td rowspan=1 colspan=16>0 1 2 3 4 5 6 7  8 9 A B C D E F</td><td rowspan=1 colspan=4>ANSI ASCII</td></tr><tr><td rowspan=1 colspan=2>00000000</td><td rowspan=1 colspan=12>300000004C664C65 01000000</td><td rowspan=1 colspan=4>01000000</td><td rowspan=1 colspan=4>0  IfLe</td></tr><tr><td rowspan=1 colspan=2>00000010</td><td rowspan=1 colspan=3>300000</td><td rowspan=1 colspan=2>0028</td><td rowspan=1 colspan=1>65</td><td rowspan=1 colspan=1>01</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>F4</td><td rowspan=1 colspan=1>01</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>01</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=2>0000</td><td rowspan=1 colspan=4>0  (eo</td></tr><tr><td rowspan=1 colspan=2>00000020</td><td rowspan=1 colspan=3>000001</td><td rowspan=1 colspan=2>0008</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>80</td><td rowspan=1 colspan=1>3A</td><td rowspan=1 colspan=1>09</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>30</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=2>0000</td><td rowspan=1 colspan=4>e: 0</td></tr><tr><td rowspan=1 colspan=2>00000030</td><td rowspan=1 colspan=3>co0000</td><td rowspan=1 colspan=2>004C</td><td rowspan=1 colspan=1>66</td><td rowspan=1 colspan=1>4C</td><td rowspan=1 colspan=1>65</td><td rowspan=1 colspan=1>01</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>7A</td><td rowspan=1 colspan=1>80</td><td rowspan=1 colspan=2>8D54</td><td rowspan=1 colspan=4>à  LfLe   ze T</td></tr><tr><td rowspan=1 colspan=2>00000040</td><td rowspan=1 colspan=3>7A808D</td><td rowspan=1 colspan=1>54</td><td rowspan=1 colspan=1>79</td><td rowspan=1 colspan=1>17</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>80</td><td rowspan=1 colspan=1>04</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>04</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=2>0000</td><td rowspan=1 colspan=4>z€Ty e</td></tr><tr><td rowspan=1 colspan=2>00000050</td><td rowspan=1 colspan=3>000000</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>62</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>62</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=2>0000</td><td rowspan=1 colspan=4>b       b</td></tr><tr><td rowspan=1 colspan=2>00000060</td><td rowspan=1 colspan=3>000000</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>BA</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>45</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>76</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>65</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=2>6E00</td><td rowspan=1 colspan=4>0   EVen</td></tr><tr><td rowspan=1 colspan=2>00000070</td><td rowspan=1 colspan=3>74004C</td><td rowspan=1 colspan=2>006F</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>67</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>4D</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>41</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=2>4300</td><td rowspan=1 colspan=4>tL。g</td></tr><tr><td rowspan=1 colspan=2>00000080</td><td rowspan=1 colspan=3>480049</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>4E</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>45</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>4E</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>41</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>4D</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=2>4500</td><td rowspan=1 colspan=4>HTNEN     E</td></tr><tr><td rowspan=1 colspan=2>00000090</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=2>0035</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>2E</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>30</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>31</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>2E</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=2>3200</td><td rowspan=1 colspan=4>5     1     2</td></tr><tr><td rowspan=1 colspan=2>000000A0</td><td rowspan=1 colspan=1>36</td><td rowspan=1 colspan=2>0030</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>30</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>53</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>65</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>72</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=2>7600</td><td rowspan=1 colspan=4>600          V</td></tr><tr><td rowspan=1 colspan=2>000000B0</td><td rowspan=1 colspan=1>69</td><td rowspan=1 colspan=2>0063</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>65</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>50</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=2>6100</td><td rowspan=1 colspan=1>63</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=2>6B00</td><td rowspan=1 colspan=4>iCe          k</td></tr><tr><td rowspan=1 colspan=2>000000CO</td><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=2>0033</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>55</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>6E</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=2>6900</td><td rowspan=1 colspan=1>70</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=2>7200</td><td rowspan=1 colspan=4>3          P上</td></tr><tr><td rowspan=1 colspan=2>000000D0</td><td rowspan=1 colspan=1>6E</td><td rowspan=1 colspan=2>0063</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>65</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>73</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>73</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=2>6E00</td><td rowspan=1 colspan=1>72</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=2>2000</td><td rowspan=1 colspan=4>。Cess。r</td></tr><tr><td rowspan=1 colspan=2>000000E0</td><td rowspan=1 colspan=1>46</td><td rowspan=1 colspan=2>0072</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>65</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>65</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=2>0000</td><td rowspan=1 colspan=1>co</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=2>0000</td><td rowspan=1 colspan=4>Eree    à</td></tr><tr><td rowspan=1 colspan=2>000000F0</td><td rowspan=1 colspan=1>68</td><td rowspan=1 colspan=2>0000</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>4C</td><td rowspan=1 colspan=1>66</td><td rowspan=1 colspan=1>4C</td><td rowspan=1 colspan=1>65</td><td rowspan=1 colspan=1>02</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=2>0000</td><td rowspan=1 colspan=1>7A</td><td rowspan=1 colspan=1>80</td><td rowspan=1 colspan=1>8D</td><td rowspan=1 colspan=1>54</td><td rowspan=1 colspan=3>h  IfLe</td><td rowspan=1 colspan=1>2ET</td></tr><tr><td rowspan=1 colspan=2>00000100</td><td rowspan=1 colspan=1>7A</td><td rowspan=1 colspan=2>808D</td><td rowspan=1 colspan=1>54</td><td rowspan=1 colspan=1>75</td><td rowspan=1 colspan=1>17</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>80</td><td rowspan=1 colspan=1>04</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=3>ze Tu e</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=2>00000110</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=2>0000</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>62</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>62</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=3>b</td><td rowspan=1 colspan=1>b</td></tr><tr><td rowspan=1 colspan=2>00000120</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=2>0000</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>62</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>45</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>76</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>65</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>6E</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>b</td><td rowspan=1 colspan=1>E</td><td rowspan=1 colspan=1>0n</td></tr><tr><td rowspan=1 colspan=2>00000130</td><td rowspan=1 colspan=1>74</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>4C</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>6F</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>67</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>4D</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>41</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>43</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>tL</td><td rowspan=1 colspan=1>。</td><td rowspan=1 colspan=1>g</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=2>00000140</td><td rowspan=1 colspan=1>48</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>49</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>4E</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>45</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>4E</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>41</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>4D</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>45</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>HI</td><td rowspan=1 colspan=1>N</td><td rowspan=1 colspan=2>NENAME</td></tr><tr><td rowspan=1 colspan=2>00000150</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>68</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>EO</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>4C</td><td rowspan=1 colspan=1>66</td><td rowspan=1 colspan=2>4C65</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=3>h  à  LfLe</td></tr><tr><td rowspan=1 colspan=2>00000160</td><td rowspan=1 colspan=1>03</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>6D</td><td rowspan=1 colspan=1>80</td><td rowspan=1 colspan=1>8D</td><td rowspan=1 colspan=1>54</td><td rowspan=1 colspan=1>8B</td><td rowspan=1 colspan=1>80</td><td rowspan=1 colspan=1>8D</td><td rowspan=1 colspan=1>54</td><td rowspan=1 colspan=1>02</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=2>0640</td><td rowspan=1 colspan=4>me T&lt;€    @</td></tr><tr><td rowspan=1 colspan=2>00000170</td><td rowspan=1 colspan=1>04</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>02</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>6E</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>4D</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>67</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>5E</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=2>0000</td><td rowspan=6 colspan=4>nMgへ0   žseI   a     MACMEce</td></tr><tr><td rowspan=1 colspan=2>00000180</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>30</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=2>0000</td><td rowspan=1 colspan=1>9E</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=2>0000</td></tr><tr><td rowspan=1 colspan=2>00000190</td><td rowspan=1 colspan=1>53</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>65</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>72</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>69</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>61</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=2>6c00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=2>4D00</td></tr><tr><td rowspan=1 colspan=2>000001A0</td><td rowspan=1 colspan=1>41</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>43</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>48</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>49</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>4E</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=2>4500</td><td rowspan=1 colspan=1>4E</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=2>4100</td></tr><tr><td rowspan=1 colspan=2>000001B0</td><td rowspan=1 colspan=1>4D</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>45</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>5c</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>44</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=2>6500</td><td rowspan=1 colspan=1>76</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=2>6900</td></tr><tr><td rowspan=1 colspan=2>000001C0</td><td rowspan=1 colspan=3>630065</td><td rowspan=1 colspan=2>005C</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>53</td><td rowspan=1 colspan=2>00 65</td><td rowspan=1 colspan=3>007200</td><td rowspan=1 colspan=4>69006100</td></tr></table>

图5-42 EVT事件志件签名及记录特征

当志件超出最限制时，系统将会删除较早的志记录，因此，志记录也将出现不连续存储的情况，同一个记录分散在不同的扇区位置，连续存储的事件志记录结构如图5-43所示。

![](images/6f11ceea95013757dfb38731f4ba85c5b517de9408f68f73744710a50a1a2a22.jpg)  
图5-43 非连续存储的事件志记录结构

当操作系统重新安装（如格式化后进系统安装），通常可先根据件系统元数据信息进数据恢复（如基于\$MFT、录项特征信息）。如件系统元数据信息已被覆盖，那么还可基于EVT事件志记录的特征进数据恢复。如HarlanCarvey编写的LfLe事件志恢复具(下载地址：https://github.com/keydet89/Tools），可对未分配空间、内存镜像件进事件志记录的挖掘恢复。

## 4.EVTX事件日志文件结构

EVTX事件志件是WindowsVista及更版本系统使的事件志格式。EVTX件结构见表5-20,块（Chunk)结构见表5-21，事件记录结构见表5-22。

表5-20 EVTX事件日志文件结构
<table><tr><td>偏移量</td><td>大小</td><td>值</td><td>描</td><td>述</td></tr><tr><td>0</td><td>8</td><td>&quot;ElfFilelx00&quot;</td><td>签名</td><td></td></tr><tr><td>8</td><td>8</td><td></td><td>首个块(Chunk)号</td><td></td></tr><tr><td>16</td><td>8</td><td></td><td>最后块（Chunk）号</td><td></td></tr><tr><td>24</td><td>8</td><td></td><td>下一记录标识符</td><td></td></tr><tr><td>32</td><td>4</td><td>128</td><td>头部大小</td><td></td></tr><tr><td>36</td><td>2</td><td></td><td>小版本</td><td></td></tr><tr><td>38</td><td>2</td><td></td><td>大版本</td><td></td></tr><tr><td>40</td><td>2</td><td>4096</td><td>头部块大小(chunk 数据偏移）</td><td></td></tr><tr><td>42</td><td>2</td><td></td><td>块(Chunk)数量</td><td></td></tr><tr><td>44</td><td>76</td><td></td><td>未知</td><td></td></tr><tr><td>120</td><td>4</td><td></td><td>文件标记flag(1为Dirty状态、2为完整)</td><td></td></tr><tr><td>124</td><td>4</td><td></td><td>校验和(Checksum)</td><td></td></tr><tr><td>128</td><td>3968</td><td></td><td>未知</td><td></td></tr></table>

表5-21 EVTX件内部的块(Chunk)结构
<table><tr><td>偏移量</td><td>大小</td><td>值</td><td>述</td></tr><tr><td>0</td><td>8</td><td>&quot;ElfChnk\x00&quot;</td><td>签名（Signature）</td></tr><tr><td>8</td><td>8</td><td></td><td>首个事件记录号</td></tr><tr><td>16</td><td>8</td><td></td><td>最后一个事件记录号</td></tr><tr><td>24</td><td>8</td><td></td><td>首个事件记录识别标识</td></tr><tr><td>32</td><td>8</td><td></td><td>最后一个事件识别标识</td></tr><tr><td>40</td><td>4</td><td>128</td><td>头部大小(指针数据的偏移)</td></tr><tr><td>44</td><td>4</td><td></td><td>最后一条事件记录数据偏移（该偏移量是相 对于块头的起始位置）</td></tr><tr><td>48</td><td>4</td><td></td><td>块中自由空间偏移(该偏移量是相对于块头 的起始位置)</td></tr><tr><td>52</td><td>4</td><td></td><td>事件记录校验和（事件记录数据的CRC32值）</td></tr><tr><td>56</td><td>64</td><td></td><td>未知</td></tr><tr><td>120</td><td>4</td><td></td><td>未知</td></tr><tr><td>124</td><td>4</td><td></td><td>校验和(块的前 120 字节及字节 128 至512 的 数据的CRC32 校验值)</td></tr></table>

表5-22 EVTX文件内部的事件记录结构
<table><tr><td>偏移量</td><td>大小</td><td>值</td><td>描 述</td></tr><tr><td>0</td><td>4</td><td>&quot;\x2a\x2a\x00\x00&quot;</td><td>签名（Signature）</td></tr><tr><td>4</td><td>4</td><td></td><td>大小(事件记录的大小，包括签名和大小)</td></tr><tr><td>8</td><td>8</td><td></td><td>事件记录标识符(ID)</td></tr><tr><td>16</td><td>8</td><td></td><td>最后写入的日期时间(FILETIME)</td></tr><tr><td>24</td><td>…</td><td></td><td>事件记录内容（二进制XML)</td></tr></table>

## 5.事件日志鉴定注意事项

Windows操作系统默认没有提供删除特定日志记录的功能，仅提供删除所有日志的操作功能。然而，内置的事件日志查看器提供了对选定的事件日志记录进行保存的功能，因此，用户完全可以仅保留指定的事件记录信息，并将其另存为新的事件志件。此外，也存在些第三具可直接从事件志中删除指定记录。

在电子数据真实性鉴定中，有时需要对事件日志的完整性进行检验分析，鉴定是否存在伪造的痕迹。鉴定员可对志件中的事件记录编号(EventRecordID)进完整性检查，如检查事件记录编号是否连续、是否缺失特定编号的记录等。通过事件志记录编号的连续性也可发现操作系统中事件发后真实的先后顺序。

在使Windows带的事件查看器对志件分析时，默认使“常规”标签页，然有些特定的情况下，也时常需要使“详细信息”标签页中的“XM视图”或“友好视图”来查看更多详细信息。通过该视图可查看有些在事件志记录列表中法查看的信息，如事件志记录编号（即EventRecordID），如图5–44所。

![](images/655b313c48044b71dfd26294332f3a46f582ec4cbe2cd526c9a92ca299d797f9.jpg)  
图5-44 事件志记录编号查看方法

Windows事件志记录列表视图在户没有对任何列进排序操作前，默认是按其事件志记录编号(即EventRecordID)来排序的。对某案例中Windows事件志件进分析，通过事件志记录编号连续性检查，发现事件志记录编号1775的事件记录存在缺失，如图5–45所,因此该事件志件完整性存在问题，存在伪造的可能。

![](images/9014a927d0901093c7d8a7e7b56911b1e98cf82b03b42810c1c19261c2f98cd3.jpg)  
图5-45 事件日志记录编号缺失的发现

默认情况下，事件日志记录编号是自动连续增加，不会出现个别记录编号缺失。值得注意的是，当Windows系统用户对操作系统进行大版本升级时，操作系统可能会重新初始化事件日志记录编号。

通过对Windows事件日志的鉴定，鉴定人员可对操作系统、应用程序、服务及设备等操作行为记录及时间进行回溯，在一些安全事件调查取证及电子数据司法鉴定中（如非法入侵鉴定、企业内部数据泄密等），借助事件日志中记录的信息，可顺利开展相关电子数据的司法鉴定工作。

## 二、NTFS文件系统日志

NTFS是Windows 2000操作系统及后续版本最常使用的文件系统。在分区格式化为NTFS后，文件系统会自动生成一系列的“内部文件”或“元文件”，此类文件均带有\$前缀，在Windows系统中无法查看内部文件，可使用鉴定软件查看。NTFS文件系统内部包含两个重要的日志文件：\$UsnJrnl和\$Logfile，可为鉴定人员提供分区中文件的历史操作记录信息。

从Windows 7 操作系统开始，NTFS文件系统均引入了USN日志机制。该日志文件记录了NTFS分区中文件的创建、重命名、内容变更及删除等重要操作。因此，NTFS文件系统的日志对于电子数据鉴定来说是一个宝藏，它可分析系统用户、远程控制者或入侵者对磁盘分区操作行为进行全面的记录，包括时间戳、文件或文件夹名及操作原因等信息。

## (一)USN日志

## 1.\$USNJrnl 日志概述

\$UsnJrnl文件在每个NTFS分区根目录下的 \$Extend 中可以找到。在不同的鉴定软件（如EnCase、FTKImager)中查看的方式有些差异，如图5–46和图5–47所示。

![](images/ccc9852732c44a7966228a61774aaa8517fa87da1dd498f8ac286756da74adf1.jpg)  
图5– 46 EnCase Forensic 查看 \$Usnjrnl 日志

![](images/0aa504d5d6b14791e85f80ebbcccb02b92c2cbf7051a41374d74a0493618f3ed.jpg)  
图5–47 FTK Imager查看\$Usnjrnl志

## 2.\$UsnJrnl志文件结构

\$UsnJrnl志件包含两个属性信息，可简单理解为它是由\$MAX和\$J两个件组成，见表5-23。

表5-23 \$USNJRNL志件说明
<table><tr><td>文件名称</td><td>说 明</td></tr><tr><td>$MAX</td><td>记录元数据变化的日志，文件大小为32字节</td></tr><tr><td rowspan="5">$J</td><td>记录文件变化的日志，$J文件的特点：</td></tr><tr><td>●每条记录有USN(Update Sequence Number，更新序号）信息</td></tr><tr><td>● 记录顺序是由USN 决定</td></tr><tr><td>●USN 即 $J 属性中记录的偏移值</td></tr><tr><td>●USN信息也会在MFT记录的$STANDARD_INFORMATION属性进行记录</td></tr></table>

\$MAX件记录的信息较少，该件大为32字节，记录固定的信息，件结构见表5-24，其包含的内容如图5-48所示。

表5-24 \$MAX文件结构
<table><tr><td>偏移</td><td>长度</td><td>存储信息</td><td>详情</td></tr><tr><td>0x00</td><td>8</td><td>最大大小（Maximum Size)</td><td>日志数据的最大大小限制</td></tr><tr><td>0x08</td><td>8</td><td>分配大小（Allocation Size)</td><td>当新日志数据保存时分配的空间大小</td></tr><tr><td>0x10</td><td>8</td><td>USN编号（USN ID)</td><td>$UsnJrnl文件的创建时间</td></tr><tr><td>0x18</td><td>8</td><td>最小有效 USN值（Lowest Valid USN)</td><td>当前记录中最小的 USN 值，鉴定人员可以 访问$J 属性中的第一条记录的起始位置</td></tr></table>

![](images/aa08c8f991d57938bc4948f04c9c1ae0609f674ff71542db23a43b08fc0306b5.jpg)  
图5-48 \$MAX文件十六进制查看

\$J件对于电数据鉴定有较的价值，其记录了NTFS分区中对象的创建、重命名、删除、件属性变化等与相关操作记录。\$J属性件中的志记录是可变的，默认是连续存储机制。件前部默认是以零填充的稀疏区域（SparseArea）。

<table><tr><td rowspan=1 colspan=1>稀疏区域(Sparse Area)</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>日志记录</td><td rowspan=1 colspan=1>日志记录</td><td rowspan=1 colspan=1>日志记录</td><td rowspan=1 colspan=1>日志记录</td></tr></table>

采该结构的原因是操作系统要保持志数据占的总空间为固定。

新志记录般是从\$J件尾部开始添加；

•如果要添加的记录总超过“分配（AllocationSize）”，操作系统就认定整个志数据超过了“最（MaximumSize）”；

•如果整个志数据超过了“最（MaximumSize）”，\$J件前半部分将以零式填充。

因此，\$J文件的逻辑大小将持续增长，但是保存的实际数据占用的空间却是固定长度。常见的志数据为0x20000\~0x23FFFFF。\$J属性件结构[119],如图5-49所,详细件结构及说明见表5–25。

<table><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>6</td><td rowspan=1 colspan=1>7</td><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1>9</td><td rowspan=1 colspan=1>a</td><td rowspan=1 colspan=1>b</td><td rowspan=1 colspan=1>c</td><td rowspan=1 colspan=1>d</td><td rowspan=1 colspan=1>e</td><td rowspan=1 colspan=1>f</td></tr><tr><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=4>record length</td><td rowspan=1 colspan=2>majorversion</td><td rowspan=1 colspan=2>minorversion</td><td rowspan=1 colspan=8>file reference number</td></tr><tr><td rowspan=1 colspan=1>10</td><td rowspan=1 colspan=8>parent file reference number</td><td rowspan=1 colspan=8>usn</td></tr><tr><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=8>timestamp</td><td rowspan=1 colspan=4>reason</td><td rowspan=1 colspan=4>source info</td></tr><tr><td rowspan=1 colspan=1>30</td><td rowspan=1 colspan=4>security info</td><td rowspan=2 colspan=12>security info            file attributes      file length  file name           nameoffset(name continuation)</td></tr><tr><td rowspan=1 colspan=1>40:</td><td></td><td></td><td></td><td></td></tr></table>

图5-49 \$J属性件结构图

表5-25 \$J文件结构及说明
<table><tr><td>偏移</td><td>长度</td><td>存储信息</td></tr><tr><td>0x00</td><td>4</td></tr><tr><td>2 大版本(Major Version)</td><td>记录大/长度（RecordLength）</td></tr><tr><td>0x04 0x06 2</td><td>小版本（Minor Version）</td></tr><tr><td>0x08 8</td><td>MFT参考号（MFT Reference Number)</td></tr><tr><td>0x10 8</td><td>父级MFT参考号（Parent MFT Reference</td></tr><tr><td>Number) 0x18</td><td></td></tr><tr><td>8 usN 时间戳（TimeStamp-FILETIME）</td><td>更新序号（Update Sequence Number) 事件时间（UTC+0)</td></tr><tr><td>0x20 8 0x28</td><td>事件变更的标记</td></tr><tr><td>4 原因标记（Reason Flag）</td><td></td></tr><tr><td>0x2C 4 0x30</td><td>源信息（Source Information） 4 安全ID (Security ID)</td></tr><tr><td>0x34</td><td>4</td></tr><tr><td></td><td>文件属性（File Atributes)</td></tr><tr><td>0x38 2</td><td>文件名大小（Size of Filename）</td></tr><tr><td>文件名偏移（Offset of Filename）</td><td>0x3A 2 0x3C</td></tr><tr><td>N 文件名（Filename)</td><td></td></tr></table>

\$J件中的原因标记(ReasonFlag）的常见数值及说明，如图5–50所。通过原因标记可以分析件被覆盖、件/件夹被删除、件/件夹重命名等常见件操作事件。

<table><tr><td rowspan=1 colspan=1>Flag</td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=1 colspan=1>0×01</td><td rowspan=1 colspan=1>The file was overwritten.</td></tr><tr><td rowspan=1 colspan=1>$0×02</td><td rowspan=1 colspan=1>The file or directory was added to</td></tr><tr><td rowspan=1 colspan=1>0×04</td><td rowspan=1 colspan=1>The file or directory was truncated.</td></tr><tr><td rowspan=1 colspan=1>0×10</td><td rowspan=1 colspan=1>The named data streams for a file is overwritten.</td></tr><tr><td rowspan=1 colspan=1>0x20</td><td rowspan=1 colspan=1>A named data streams for the file were added.</td></tr><tr><td rowspan=1 colspan=1>0×40</td><td rowspan=1 colspan=1>A named data streams for the fle was truncated</td></tr><tr><td rowspan=1 colspan=1>0×100</td><td rowspan=1 colspan=1>The file or directory was created for the first time.</td></tr><tr><td rowspan=1 colspan=1>0x200</td><td rowspan=1 colspan=1>The file or directory was deleted.</td></tr><tr><td rowspan=1 colspan=1>0x×400</td><td rowspan=1 colspan=1>The file&#x27;s or directory&#x27;s extended attributes were changed.</td></tr><tr><td rowspan=1 colspan=1>0×800</td><td rowspan=1 colspan=1>The access rights to the file or directory was changed.</td></tr><tr><td rowspan=1 colspan=1>0×1000</td><td rowspan=1 colspan=1>The file or directory was renamed.(previous name)</td></tr><tr><td rowspan=1 colspan=1>0x2000</td><td rowspan=1 colspan=1>The file or directory was renamed.(new name)</td></tr><tr><td rowspan=1 colspan=1>0×4000</td><td rowspan=1 colspan=1>A user changed the FILE_ATTRIBUTE_NOT_CONTENT_INDEXED atribute.</td></tr><tr><td rowspan=1 colspan=1>0×8000</td><td rowspan=1 colspan=1>A user has either changed one or more file or directory atributes or one or more time stamps.</td></tr><tr><td rowspan=1 colspan=1>0x10000</td><td rowspan=1 colspan=1>A hard link was added to or removed from the file or directory</td></tr><tr><td rowspan=1 colspan=1>0×20000</td><td rowspan=1 colspan=1>The compression state of the file or directory was changed from or to compressed.</td></tr><tr><td rowspan=1 colspan=1>0×40000</td><td rowspan=1 colspan=1>The fle or directory was encrypted or decrypted.</td></tr><tr><td rowspan=1 colspan=1>0×80000</td><td rowspan=1 colspan=1>The object identifer of the file or directory was changed.</td></tr><tr><td rowspan=1 colspan=1>0×100000</td><td rowspan=1 colspan=1>Therearconi iectoshsiaseie</td></tr><tr><td rowspan=1 colspan=1>0×20000</td><td rowspan=1 colspan=1>A named stream has been added to or removed from the file, or a named stream has been renamed.</td></tr><tr><td rowspan=1 colspan=1>0x800000000</td><td rowspan=1 colspan=1>The file or directory was dosed.</td></tr></table>

图5-50 原因标记(ReasonFlag)数值及说明

## 3.\$UsnJrnl日志文件分析

前鉴定软件中直接持\$UsnJrnl件分析的有X-WaysForensics和取证神探等工具，有些取证从业员基于EnCase平台编写了\$UsnJrml志记录解析的脚本。市上还有不少鉴定软件尚未持\$UsnJrml志的数据解析。此外,也可使第三免费具(如NTFSLogTracker)。

## (）\$Logfile 志

## 1.\$Logfile 文件概述

NTFS是种基于事务的件系统，在对任何个件系统中的件进写操作时，它都会记录每次写操作的志[120]。记录NTFS件系统产的事务的件为\$Logfile。事务是种每步都必须执的磁盘操作。在NTFS件系统中泛使回写缓存机制，因此\$Logfile特别重要。

## 2.\$Logfile文件分析

志分析具“NTFSLogTracker”持对NTFS志（\$Logfile及\$UsnJrnl)的分析，提供可

视化的界,操作较简便。志分析之前通常要求鉴定员将\$Logfile、\$UsnJrnl（\$J件）、\$MFT等件导出，如要对未分配空间中的USN志进分析，还需将未分配簇以件式导出。

NTFSLogTracker启动后,选择已导出的\$Logfile、\$J及\$MFT件后,选择“Parse”，然后设置SQLiteDB数据库件的存储路径及件名后，即可动解析两个志件的所有记录，如图5-51。

![](images/218dadfade88c9a7b440f26a2abb11cb4396e2b0494142c156dfb694128e6d08.jpg)  
图5-51 选择日志文件及\$MFT所在位置

## 三、其他志

除Windows事件志、IIS志外，还有FTP志、操作系统相关志和应程序志等。由于鉴定软件可能未能动解析出相关应程序志，因此有些志需鉴定员在电数据鉴定过程中需要针对性地进行数据提取和手工分析。

## （一）远程控制软件志

应程序志(如远程控制软件、杀毒软件)在些案件中可能发挥越来越多地重要作，其中远程控制软件常见的有TeamViewer、向葵及ToDesk等。以下志及相关件的存储位置部分采星号表，表路径或件名并固定名称。其中ProgramFiles\*可能包括Program Files或 Program Files(x86)。

## 1.TeamViewer软件志及相关信息

• TeamViewer连接志

\Program Files \*\TeamViewer\connections \*.txt

•TeamViewer应志

\Program Files \* \TeamViewer\TeamViewer \*_Logfile \*.log

•TeamViewer配置件

\%UserProfile%\AppData\Roaming\TeamViewer\MRU\RemoteSupport\

2.向日葵软件日志及相关信息

•志件

\Program Files \* \Oray\SunLogin\SunloginClient \log\ \*.log

•配置件

\Program Files \* \Oray\SunLogin\SunloginClient\config.ini

•向葵Lite版志件

\ProgramData\Oray \SunloginClientLite \Iog

• 向日葵 Lite 版配置文件

```batch
\% UserProfile%\AppData\Roaming\Oray \SunloginClientLite
```

• 传输文件

\%UserProfile% \Documents \Sunlogin Files

3.ToDesk 软件日志及相关信息

•\Program Files \* \ToDesk\Logs

•\% UserProfile%\AppData\Local\ToDesk\Logs

•\ProgramData\ToDesk_Lite\Logs(ToDesk Lite 版日志文件)

## (二)杀毒软件日志

Windows系统安装的杀毒软件在运行过程中也会记录相关日志，如文件扫描日志、可疑程序日志等。本节以360杀毒软件的日志为例。360杀毒软件在Windows系统平台的安装及使用普及率高。在系统或程序运行过程中出现的一些异常行为、文件扫描、可疑文件的上传等均有相关日志记录。

360杀毒软件的日志存储位置为：C:\Program Files\360\360sd\Log。日志目录进行分类存储，包含以下多个文件夹：

• CpuOverLog：CPU处理器过载志

• CpuOverLog_t：CPU处理器过载相关日志

•FileUploadLog：可疑文件上传日志

•PopWndTrackerLog：弹窗程序追踪志(针对弹窗告等程序安全检测，包含)

• ProcessHistoryLog：进程历史记录志

•RealtimeProtectLog：实时保护志(含程序件完整路径及名称、MD5哈希等)

• UpdateLog：更新日志

• VirusScanLog：病毒扫描日志

• WebAdLog：页广告志

## 第七节 计算机物理内存获取与分析

## 一、计算机物理内存概述

计算机物理内存一般指的是随机存取存储器(Random AccessMemory，简称 RAM)。内存是一种易失性存储载体，保存处理器主动访问和存储的代码和数据，是一个临时的数据交换空间。大多数的计算机的内存属于一种动态 RAM(DRAM)。它是动态变化的，因其利用了电容器在充电和放电状态间的差异来存储数据的比特位。为了维持电容器的状态，动态内存必须周期性刷新，这也是内存控制器最典型的任务[123]。

## (一)物理内存数据的价值

操作系统及各种应用软件经常需要与内存进行数据交互，此外由于内存空间有限，因此计算机系统可能将内存中的数据缓存到磁盘中。内存中有大量的各类数据，结构化及非结构化数据。通过对物理内存镜像可提取有价值的数据。常见有价值的数据，包含以下内容：

•进程列表(包括恶意程序进程、Rootkit隐藏进程等)

●动态链接库(当前系统或程序加载的动态链接库)

●打开件列表(当前系统打开的件列表)

•网络连接(当前活动的网络连接)

• \$MFT记录(常驻文件均可以直接提取恢复）

●注册表(部分注册表信息，包括系统注册表和用户注册表文件)

•加密密钥或密码（如Windows 账户密码 Hash、BitLocker/TrueCrypt/VeraCrypt等全盘加密或加密容器的恢复密钥等）

● 聊天记录(如QQ聊天记录段)

•互联网访问(上记录URL地址、网页缓存及InPrivate隐私模式访问数据等)

●电邮件(如网页邮件缓存页面)

●图及文档等(尚未保存到磁盘中的图、文档等件)

## （二）页交换文件

Windows引入页交换文件(Pagefile.sys)来协助内存数据的交换。Pagefile.sys用于存储从物理内存中转移过来的数据。要获得一个正在运行的系统的活动全貌或快照，通常除分析物理内存中的数据，还需对Pagefile.sys进行分析。

Windows系统开始支持页交换文件Pagefile.sys的加密。可使用futil命令行查询页交换文件是否加密，如图5-52和图5-53所示。

![](images/c0a09b5028680cab83f8061e5ddd33305b8886d3cca1eabe9d52aecb477c6978.jpg)  
图5-52启用页交换文件加密

![](images/4dc92cc080c18750d8d62385f1bbf587e68cb6e4f82f96b3ce9e138eb6db8599.jpg)  
图5-53查询页交换文件加密状态

## (三)休眠文件

Hiberfil.sys是当系统休眠时，Windows将物理内存的数据写磁盘生成的一个文件。当系统进入休眠状态后，网络连接将会中断。当系统重新加电时，hiberfil.sys文件中的数据重新回写到物理内存中，这也使得从休眠状态恢复到原始状态变得相当快。

该文件采用了Xpress算法（带霍夫曼Huffman及LZ编码）。文件头部通常包含“hibr”、“HIBR”、“wake”或“WAKE”等特征。操作系统从休眠状态恢复后，文件头部被清零。清零后的件头部可能导致些鉴定软件无法分析。

要对hiberfil.sys进行分析，要求鉴定工具可将休眠文件中的数据解压为原生数据并进行数据解析。Matieu Suiche 的 Windows Memory Toolkit 工具 hibr2bin.exe 支持将休眠文件转为原生转储文件。

当鉴定人员在现场要制作Windows操作系统的物理内存镜像时，可能由于内存镜像工具不兼容操作系统导致无法获取物理内存数据。当无法成功制作物理内存镜像时，可让系统进休眠模式，从而用变通的方式获得物理内存中的数据。

## 二、计算机物理内存获取与鉴定

## (一)物理内存镜像获取

内存鉴定(MemoryForensics)通常指对计算机及相关设备运时的物理内存中存储的临时数据进获取与分析，提取有价值的数据。内存是操作系统及各种软件交换数据的区域，数据易丢失。常见物理内存获取法：冷启动攻击、基于线或雷电接的直接内存访问获取及内存获取软件具。

不同的操作系统需要到不同的物理内存获取具，Windows操作系统平台持内存获取的常见工具有：

•DumpIt（早期版本名为Win32dd）

•Belkasoft RAMCapturer

•  Magnet RAM Capture

• Winpmem

• EnCase Imager

• FTK Imager

Windows操作系统平台下的Dumplt是个简单易的计算机内存镜像获取具。通常可将该工具存放在大容量移动硬盘或优盘中，可在正在运Windows系统的平台直接运，根据提进操作即可，如图5–54所。

![](images/9c4efc1f6a3f99a789489f9d46a2c6afc56e46ce570f877c8b73a1473553ce0b.jpg)  
图5-54 在Windows系统的平台运

## （二）物理内存鉴定分析

Windows操作系统获取出的物理内存镜像需使用专门的内存分析工具。常见的内存分析工具有Volatility、Rekall、MagnetAxiom、Forensic Toolkit等，可解析出常见的基本信息，包括进程信息、络连接、加载的DLL件及注册表加载信息等。

Volatility Framework是个完全开放的内存分析具集，基于GNUGPL2许可，以python语进编写。Volatility是款开源免费具，可进内存数据的级分析，此外由于代码开源的特点，遇到一些无法解决的问题时，还可对源代码进行修改或扩展功能。

Volatility持的内存镜像格式：

●原始物理内存镜像格式

•EWF格式

•Windows32位及64位系统崩溃转储件

●Windows32位及64位系统休眠件（Windows7及早期版本)

•VMware保存状态件(.vmss)及快照件(.vmsn)

•HPAK格式(FastDump)

QEMU内存转储件

在Windows系统平台下，有两种式可运Volatility具。第种是独安装Python运环境，再下载Volatility源代码执命令;第种为下载Volatility独Windows程序（须另外安装和配置Python环境）。前Volatility分为两个版本，分别是V2和V3版，本书以V2.6.1版本为例，该工具可通过GitHub站点（htps：//github.com/volatilityfoundation/volatility)进行下载。

## Volatility常命令行参数：

•-h查看相关参数及帮助说明

•--info查看相关模块名称及持的Windows版本

•-f指定要打开的内存镜像件及路径

⚫-d开启调试模式

•-v开启显详细信息模式(verbose)

表5-26为Volatility常命令范例可供鉴定员参考，如需了解更加详细的volatility功能，可查看其帮助信息。

表5-26Volatility常用命令范例
<table><tr><td colspan="2">功能 参考命令行及参数</td></tr><tr><td>查看进程列表</td><td>volatility.exe -f Win7_SP1_x86.vmem --profile=Win7SP1x86 pslist</td></tr><tr><td>查看进程列表(树形)</td><td>volatility.exe -f Win7_SP1_x86.vmem --profile=Win7SP1x86 pstree</td></tr><tr><td>查看进程列表（psx视图）</td><td>volatility.exe -f Win7_SP1_x86.vmem --profile=Win7SP1x86 psxview</td></tr><tr><td>查看网络通讯连接</td><td>volatility.exe-f Win7_SP1_x86.vmem--profile=Win7SP1x86netscan</td></tr><tr><td>查看加载的动态链接库</td><td>volatility.exe -f Win7_SP1_x86.vmem -profile=Win7SP1x86dllist</td></tr><tr><td>查看 SSDT表</td><td>volatility.exe-f Win7_SP1_x86.vmem--profile=Win7SP1x86 ssdt</td></tr><tr><td>查看UserAssist痕迹</td><td>volatility.exe -f Win7_SP1_x86.vmem --profile=Win7SP1x86 userassist</td></tr><tr><td>查看 ShimCache痕迹</td><td>volatility.exe -f Win7_SP1_x86.vmem--profile=Win7SP1x86 shimcache</td></tr><tr><td>查看ShellBags</td><td>volatility.exe -f Win7_SP1_x86.vmem --profile= Win7SP1x86 shellbags</td></tr><tr><td>查看服务列表</td><td>volatility.exe-f Win7_SP1_x86.vmem--profile=Win7SP1x86svcscan</td></tr><tr><td>查看Windows账户 hash</td><td>volatility.exe -f Win7_SP1_x86.vmem --profile= Win7SP1x86 hashdump</td></tr><tr><td>查看最后关机时间</td><td>volatility.exe-fWin7_SP1_x86.vmem --profile=Win7SP1x86 shutdowntime</td></tr><tr><td>查看IE历史记录</td><td>volatility.exe -f Win7_SP1_x86.vmem profile= Win7SP1x86 iehistory</td></tr><tr><td>提取注册表数据</td><td>volatility.exe -f Win7_SP1_x86.vmem--profile= Win7SP1x86dumpregistry</td></tr><tr><td>解析MFT记录</td><td>volatility.exe -f Win7_SP1_x86.vmem --profile=Win7SP1x86 mftparser</td></tr><tr><td>导出 MFT 记录</td><td>volatility.exe-f Win7_SP1_x86.vmem--profile= Win7SP1x86mftparser --output-</td></tr><tr><td>获取TrueCrypt密钥信息</td><td>file=mftverbose.txt-Dmftoutput volatility.exe -f Win7_SP1_x86.vmem -profile= Win7SP1x86 truecryptmaster</td></tr><tr><td>获取 TrueCrypt 密码信息</td><td>volatility.exe-f Win7_SP1_x86.vmem--profile=Win7SP1x86 truecryptpassphrase</td></tr></table>

查看系统进程列表，如图5-55所。

•参考命令：volatility.exe -f Win7_SP1_x86.vmem --profile=Win7SP1x86 pslist

![](images/32c8fe75a0a9553a69b74785b0e7b7bb5eb9e3471d505d3ddfe9ea7744f0fd1d.jpg)  
图5-55 查看系统进程列表

查看络通讯连接信息，如图5–56所。

•参考命令：volatility.exe -f Win7_SP1_x86.vmem -profile=Win7SP1x86 netscan

![](images/0486e1def75abb7323e2e12130f31c226785644fced8406add3dacb78853592f.jpg)  
图5-56 查看络通讯连接信息

提取内存中的注册表信息，如图5-57所。

·参考命令：volatility.exe -f Win7_SP1_x86.vmem -profile=Win7SP1x86 dumpregistry

![](images/842ae0833ddd63655e2ad175167c1ae13fc73ebefeaa515d88067091d9bed170.jpg)  
图5-57 内存中的注册表信息提取

提取内存中的MFT记录信息，如图5–58所。

•参考命令：volatility.exe -f Win7_SP1_x86.vmem --profile=Win7SP1x86 mftparser

![](images/e6adf28146e02df125d1c723cc869e2f61d095d05e3d7d6daf04da7e75ddd0c2.jpg)  
图5-58 内存中的MFT记录信息提取

导出内存中的MFT记录数据，如图5-59所。

•参考命令：volatility.exe -f Win7_SP1_x86.vmem profile=Win7SP1x86 mftparser --output-file = mftverbose.txt -D mftoutput

![](images/d03d658b5ea88e42ecb0a6f7292a508278118f9161550dfa494fac3dd672023a.jpg)  
图5-59 MFT记录中的常驻文件的导出

## 第八节 其他痕迹信息

## 一、回收站分析

## (一)回收站概述

默认情况下，用户删除文件的操作并不会将文件直接从文件系统中删除，而是移动到“回收站”，当用户清空回收站后，文件才从文件系统中删除。

回收站是一个虚拟的“文件夹”，将各分区临时删除的文件集中展示出来，在此处用户可查看原始文件的大小、删除时间、原始路径等信息。但回收站中文件的名称并不是在磁盘中真实的名称。移动到回收站中的文件会统一保存在各分区特定的目录下。

## (二)INFO2 文件及其结构分析

对于WindowsXP系统，回收站目录是各分区下的“RECYCLER\<当前用户SID>\”(NTFS文件系统)或“Recycled”（FAT32文件系统）目录中，文件移动到回收站后，会被重命名，而删除时间、文件大小（物理大小）、原始路径（中文版WindowsXP中为GBK编码）则保存在同目录的INFO2文件中。

INFO2是二进制文件，无法直接预览，但可使用鉴定软件进行解析，如图5-60所示。INFO2中记录的文件大小是物理大小而非逻辑大小，所以回收站中显示的文件大小永远是文件所在分区簇大小的整数倍。另一方面，随着回收站的不断操作，INFO2文件会反复更改，所以非常容易在文件残留区中留下之前移动到回收站中文件的记录，必要时鉴定人员应该对INFO2文件的残留区进行手动分析。

![](images/1cbbe15fe6d99e32427fcf8ea334e06e39a62b939837bfca045e1fabb94ac2f4.jpg)  
图5 – 60 X-Ways Forensics 解析 Windows XP 回收站

## (三)\$I和\$R 文件结构及分析

从WindowsVista 系统开始，回收站内部机制发生较大的变化。在Vista及更高版本的系统中，文件移动到回收站后，会移动到对应分区下的“\$RECYCLE.BIN\<当前用户SID>\”（NTFS文件系统）或“\$RECYCLE.BIN”（FAT32、exFAT文件系统）目录并重命名，新文件名扩展名不变，名称以“\$R”开头，接下来是6个随机字符（以下简称“\$R件”），同时创建个与之对应的以“\$I”开头的文件（以下简称“\$I文件”）。同一对\$R文件和\$I文件除文件开头不同，名称其余部分完全致。\$I件中保存了件的(逻辑）、删除时间及删除前的路径(UTF–16LE编码)等信息，如图5-61所示。

![](images/de0cce1f1eeb551fd00686a6953fc13f7ddaf77ba9dfa6a0afc8ab68e5f3a2a7.jpg)  
图5–61 Windows 11 回收站 \$I文件

\$I文件结构如下：

·前八字节为版本信息，WindowsVista到Windows10均为“0100000000000000”，Windows11为“0200 00 000000 00 00”。

·第9到第16字节是文件大小信息，小端字节序存储的十六进制数，单位为字节。图5–61中的“2781010000000000”即为十六进制“18127”，对应的进制为“98599”，即被删除的文件小为98599字节。

●第17到第24字节是文件移动到回收站的时间，时间戳格式是filetime，小端字节序存储。图5-61中的“30FD9330AC63D901”对应的UTC时间为“2023-03-3108:38:38”。

•Windows11，第25字节到第28字节为文件删除前路径的字符数，第29字节到文件结尾为文件删除前的路径，字符编码为UTF–16BE；对于WindowsVista到Windows8.1，从第25字节到件结尾为件删除前的路径，字符编码为UTF-16BE。

Windows 10之前系统中的\$I文件，文件大小固定为544字节，Windows10、Windows11系统中的\$I件大小不固定，主要取决于对应件的原始路径长度。

\$I件有明显的特征信息，可使签名恢复尝试从未分配空间中恢复数据。由于\$I对于NTFS件系统，不同户移动到回收站中的件暂存在与件所在分区对应的以户SID命名的录中。所以户在回收站中只能查看删除的件,清空回收站也只会将各分区回收站录SID件夹中的数据删除。因此，如果用户在计算机中将部分件移动到了回收站但未清空回收站，后续重新安装了操作系统，则之前移动到回收站中的件将不再可见，且法通过清空回收站的式从件系统中删除以释放空间。如果户使在某电脑上将NTFS件系统的移动硬盘中移动了部分件到回收站，则后续在其他计算机中将法查看这些件，且法通过清空回收站的式从件系统中删除以释放空间。

## 二、卷影快照分析

## (一)卷影快照概述

卷影快照(Volume Shadow Copy)是Windows 操作系统的一项技术，可在NTFS或 ReFS文件系统中创建文件或卷的快照，用以备份数据或访问被占用的文件。卷影快照服务最早在WindowsXP中引入，但只能创建临时快照，用于访问被占用的文件。在Windows Server 2003中，卷影快照服务可用来创建持久的快照。

卷影快照数据保存在分区根目录名为“SystemVolume Information”的子目录中，该目录具有系统和隐藏属性。2020年能力验证检材镜像PLEXTOR PX-128M5Pro.e01分区2 中的三个卷影快照数据，快照对应的时间点分别为2020-05-2811:49:42、2020-06-0510:23:19和2020-06-0511：25:01，如图5-62所示。

![](images/be1171e991ae418bf5e0aa47dc46398d1f24eeedc06ae14ef2a0d7f6456389aa.jpg)  
图5–62 System Volume Information 目录中的卷影快照数据

在WindowsVista及Windows 7系统中，在文件资源管理器中分区的右击菜单中可查看“还原以前的版本”的选项，会列出此分区存在的卷影快照，点击“打开”，以UNC路径直接访问卷影快照中的数据。

微软在Windows8中取消了文件资源管理器中“还原以前的版本”的选项，虽然在Windows10中又恢复了此选项，但无法从这里查看卷影快照数据。

## (二)卷影快照分析方法

## 1.使用内置命令 vssadmin 进行挂载

在命令提示符中，管理员权限下使用“vssadmin list shadows”命令可查看系统中的卷影快照列表。如果想查看指定分区的卷影快照列表，可添加/for 参数，例如“vssadmin list shadows/for=C：”可查看C：\的所有卷影快照，如图5-63所示。

![](images/cba12476a89738f9ffe3c8dea050fb4a95b414d2e6767f920a21941944f32bd5.jpg)  
图5-63使用vssadmin命令查卷影快照列表

“mklink”是创建链接（包括软连接及硬链接）的命令，使mklink命令可以将卷影快照连接到本地录。例如我们可以使“mklink/dC：\vsc\\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy1\”命令将图5-63中2020-5-2811:49:42的卷影快照链接到“C：\vsc”录,接下来就可以通过件资源管理器直接访问，,如图5-64所。

![](images/0e4bd271055687a5d3b68427aca43dd73f17594b687bfd4a4cc3cc50a48a9b73.jpg)  
图5-64 使mklink命令将卷影快照链接到本地录

## 2.使用鉴定软件解析卷影快照信息

在Windows系统运状态下，鉴定软件可通过SMFT读取所有的件可直接解析出整个分区在卷影快照时间点的状态,从绕过件系统的权限访问限制。使鉴定软件解析2020年能验证检材镜像PLEXTORPX-128M5Pro.e01分区2的卷影快照,解析了Administrator户录的数据，如图5–65所。

卷影快照中的数据，除常规件外，还包含注册表、事件志等的历史版本。以2020年能验证检材镜像PLEXTORPX-128M5Pro.e01为例，如图5-66所，分区2中当前的\$UsnJrnl志，最早的记录是2020-05-2919:45:22,卷影快照中的\$UsnJrnl志，最早的记录是2020-05-2810:17:03，最晚的记录是2020-05-2811:49:42，如图5-67所示。

![](images/43d1542d782653917d1df42e874fda5caa3dabc74d451296b2a017a820859e46.jpg)  
图5-65 使用取证神探解析卷影快照

<table><tr><td>一分区</td><td>文件</td><td></td><td>预览</td><td>详细</td><td>缩略图</td><td>时间轴 图例说明 RAW 文本 </td></tr><tr><td>Timestanp</td><td>Change type</td><td></td><td>FileID</td><td>Attributes</td><td>Filename</td></tr><tr><td></td><td>19:45:22</td><td>+8</td><td>Data 98426,2</td><td>A</td><td>INSTALLAGENT.EXE-2CA93386.pf</td></tr><tr><td>2020-05-29, 2020-05-29,</td><td>19:45:25</td><td>+8</td><td>Temporary</td><td>92253,38</td><td>A speedmem2.hg-journal</td></tr><tr><td>2020-05-29,</td><td>19:45:25</td><td>+8</td><td>Data 98860,4</td><td>A</td><td>galaxy2.dat</td></tr><tr><td>2020-05-29,</td><td>19:45:25</td><td>+8</td><td>Data</td><td>106389,22 A</td><td>SOGOUEXPLORER.EXE-C02C7C9F.pf</td></tr><tr><td>2020-05-29,</td><td>19:45:30</td><td>+8</td><td>Data</td><td>98084,3</td><td>SHA lastalivel.dat</td></tr><tr><td>2020-05-29,</td><td>19:46:21</td><td>+8</td><td>Data 90754,1</td><td>SHA</td><td>ntuser.dat.LOG2</td></tr><tr><td>2020-05-29,</td><td>19:46:21</td><td>+8</td><td>Data 104043,1</td><td>SHA</td><td>ntuser. dat.LOG2</td></tr><tr><td>2020-05-29,</td><td>19:46:30</td><td>+8</td><td>Data 90030,3</td><td>SHA</td><td>lastalive0.dat</td></tr><tr><td>2020-05-29,</td><td>19:47:04</td><td>+8</td><td>Data</td><td>104931,12 A</td><td>Data_2020_05_29.dat</td></tr><tr><td>2020-05-29,</td><td>19:47:04</td><td>+8</td><td>Data Data</td><td>90014,8 A 104934,10</td><td>MIndex.dat</td></tr><tr><td>2020-05-29,</td><td>19:47:04 19:47:08</td><td>+8 +8</td><td>Data 98860,4</td><td>A A</td><td>CIndex_2020_05_29.dat</td></tr><tr><td>2020-05-29,</td><td>19:47:08</td><td>+8</td><td>Data 89503,1</td><td>A</td><td>galaxy2.dat</td></tr><tr><td>2020-05-29,</td><td>19:47:08</td><td>+8</td><td>Data 98860.4</td><td>A</td><td>system</td></tr><tr><td>2020-05-29.</td><td>19:47:08</td><td>+8</td><td>Data</td><td>87353,2 A</td><td>galaxy2. dat</td></tr><tr><td>2020-05-29, 2020-05-29.</td><td>19.47.08</td><td>+8</td><td>Dat.a</td><td>85832.1 A</td><td>software SECITRTTY</td></tr><tr><td>4</td><td></td><td></td><td></td><td></td><td></td></tr><tr><td colspan="6">\PLEXTORPX-128M5Pro,分区2\SExtend\SUsnJrnl:$J</td></tr></table>

图5–66 PLEXTOR PX-128M5Pro.e01分区2中的\$UsnJrnl志

![](images/6be7b93d5e0285546094435f4f6e380fc3315a25de5ad4cc0f74315e82ec47df.jpg)  
图5-67 PLEXTORPX-128M5Pro.e01分区2卷影快照中的\$UsnJrnl志

## 第九节  结

在Windows系统的电数据鉴定中,先需了解常见的Windows系统版本、件系统、录结构及各种Windows常见痕迹信息及其所在位置。其次，要熟悉注册表的动鉴定，掌握主流的鉴定软件或注册表分析工具的使用，具备独立研究和分析注册表信息的能力。

Windows的常见系统痕迹涵盖了件打开记录痕迹、USB设备使记录、程序运痕迹、浏览器分析、计算机内存镜像分析、志分析、回收站分析及卷影快照分析等。

随着Windows系统的不断更新，鉴定员在对Window系统进检验鉴定时，现有的计算机鉴定具可能法动提取鉴定要求所需的关键信息，因此，鉴定员需具备Windows鉴定的常见知识点和独开展研究新型痕迹信息或相关鉴定分析所需的技能。

![](images/82436d4fa8a0d712bb982602be239ad520337f150f8a9acbccfe8cdbef3c4cae.jpg)

## ·思考题

1.WindowsVista及更版本的系统的事件日志默认存储的位置是什么?

2.WindowsVista及更高版本的系统中，回收站对应的名称是什么？

3.Windows10/11系统中对某个NTFS卷进行格式化（非快速格式化)，请问该卷原有保存的文件是否可以进行恢复?

4.Windows系统中Prefetch件夹中以pf文件扩展名命名的件记录了哪些信息？

5.Windows系统用户使用蓝牙方式传输文件到外部设备，在哪个痕迹信息中可以找到有关证据？

## 相关

（相关法条和概念待补充）
