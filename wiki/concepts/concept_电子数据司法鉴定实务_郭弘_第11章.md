---
title: 电子数据司法鉴定实务_郭弘_第11章_虚拟化技术的应用与鉴定
type: concept
created: 2026-04-29
updated: 2026-04-29
tags: [电子数据鉴定, 司法鉴定, 虚拟化鉴定]
source: 〔来源文件不存在〕
source: 〔来源文件不存在〕
source: 〔来源文件不存在〕
sources: 《电子数据司法鉴定实务》郭弘 科学出版社 2025年.md
---

# 第十一章 虛拟化技术的应用与鉴定

## 第一节 虚拟化技术概述

虚拟化是计算机科学中个技术概念，本质是将计算机资源通过虚拟化技术分割为若相互独立的虚拟计算机资源，以实现资源的共享复用和安全隔离。计算机系统从高层至低层可依次划分为应用程序层、操作系统层、硬件层，在每一层上都可以进虚拟化。

应用程序层虚拟化典型例子是编程语虚拟机，例如Java虚拟机（Java virtual machine，JVM)可虚拟出运行Java程序的虚拟体系结构，将Java程序代码编译成其虚拟体系结构的字节码，再由JVM运时翻译成机器语进执，从而可实现Java语的跨平台。

操作系统层虚拟化是将操作系统内核虚拟化，为户提供多个相互隔离的操作执环境。这些操作执环境对于使用它的户来看就像一台真实的计算机，有独的网络、件系统、库函数和系统设置等。在不同具体技术实现中，这些执环境称呼不同，例如容器(container)、虚拟化引擎(virtualization engine， VE)等。

硬件层虚拟化可实现对整个计算机系统的虚拟，将硬件资源由专门管理器管理，从而可将多个物理计算机资源合并，或将一台物理计算机资源虚拟出多台虚拟计算机系统。每台虚拟的计算机系统都有独的虚拟CPU、内存和IV/O设备。

随着云计算技术的快速发展和广泛应用，支撑云计算的虚拟化技术（virtualizationtechnology,VT)分关键,前较流的虚拟化有硬件层虚拟化的虚拟机技术和操作系统层虚拟化的容器技术。本章将主要探讨虚拟机和容器有关的鉴定技术。

## 一、虚拟机技术

## (一)什么是虚拟机

虚拟机技术与仿真技术有些类似，但不同的是虚拟机技术可在同硬件平台上虚拟出多台虚拟设备，在不同虚拟设备上可同时运多个不同的操作系统。实现虚拟机技术的关键是加个中间层。从实现式看，中间层的实现可采纯软件式,即在主机操作系统之上部署虚拟机软件，完全由该软件负责将物理机虚拟出多个虚拟机，每个虚拟机都具有完整的计算机应用环境；也可采用硬件辅助虚拟化技术，即在支持VT技术的硬件层上，由虚拟机监视器（virtual machine monitor,VMM)或虚拟管理器（Hypervisor)负责处理器、内存和I/O的虚拟化，以及对虚拟机的控制和硬件访问的干预。

利用虚拟机技术虚拟出的虚拟计算机系统，包括应用程序和操作系统，称为虚拟机（virtual machine，VM)，也称为客户机（guest machine）。而虚拟出VM的设备称为主机或宿主机(hostmachine)。对于使用户，使虚拟机与使用物理计算机没有什么区别。

## (二)虚拟机技术分类

## 1.按照实现结构进行分类

按照虚拟机实现结构的不同，即Hypervisor的结构层次不同，可以分为1型(TYPE1)虚拟管理器和2型（TYPE2）虚拟管理器。

其中1型虚拟管理器，也称为裸机管理器，它直接运行在宿主机物理硬件上，而不依赖底层操作系统，因而更加高效和安全。由于这类管理器本身像一个轻量级操作系统，创建和管理虚拟机一般需要通过控制台远程连接到服务器进行。

2型虚拟管理器，也称宿主机型管理器，它安装在宿主机的现有操作系统上，一定程度上依赖现有操作系统进虚拟化和资源管理。由于这类管理器运在宿主机操作系统之上，宿主机操作系统和虚拟机运本身要占用定资源，因而在性能上易导致延迟，资源易被浪费且宿主机操作系统的安全缺陷和漏洞也会直接威胁虚拟机的安全，如图11-1所示。

![](images/31abf273cec024417f521171176e27343d0dac079b8e6bba74907e755eff7da5.jpg)  
图11-1虚拟管理器的2 种类型

## 2.按照产品类型和应用场景分类

前,市场上虚拟机产品类型很多,按照产品类型和应场景的不同,可将较流的虚拟机技术产品分为以下几种：VMware Workstation/Fusion/Player、VMware vSphere/ESXi、OracleVM VirtualBox、KVM、Red Hat Virtualization、Microsoft Hyper-V、Parallels Desktop、CitrixXenServer/Xen等。

## （三）常见虚拟机实现方法

虚拟机实现虚拟化涉及CPU、内存和外设的虚拟化。CPU虚拟化包括三种式，分别为全虚拟化、半虚拟化和硬件辅助虚拟化。全虚拟化式调用CPU指令时必须通过封装解码转换为调用主机OS指令，进而通过内核调用CPU指令。半虚拟化方式中客户机内核被修改过，系统调用时可直接对CPU调用。而硬件辅助虚拟化方式CPU指令多了-1环，此时0环为虚拟机内核，当虚拟机系统调用时，会调用0环特权指令，进而再转换为调用-1环特权指令。内存虚拟化引入了三种地址：机器地址、虚拟物理地址、虚拟地址，通过VMM实现地址之间的映射。硬盘、显卡等IV/0外设虚拟化也有不同虚拟化解决方案，例如，硬盘可通过划分不同区域供不同虚拟机访问实现虚拟化、显卡通过提供虚拟缓冲设备实现虚拟化等。

## 二、容器虚拟化技术

## (一)什么是容器虚拟化

虚拟机技术虽然可通过制作虚拟机镜像轻松迁移，不用担迁移部署出错或者环境不致等问题，但在创建环境、部署应用、应用的移植性等方面都很烦琐，通过操作系统层虚拟化技术可较好实现各种环境的灵活迁移和部署。容器虚拟化，又称容器技术，就是操作系统层的虚拟化技术，前发展已经成熟，它通过对计算机系统资源的隔离和灵活调度，提供应用程序完整的运环境。

## 1.容器基础技术

容器技术最重要的功能是实现隔离和保护。前流的容器技术都是基于chroot、namespace、cgroups等技术来实现的。

(1) chroot chroot可改变程序执时的root录位置。通过切换进程及其子进程的root录，使得进程法访问录外的件，起到隔离作。但仅使chroot法隔离进程、络等资源。

(2)Namespace Namespace,称为“命名空间”或“名称空间”,来实现对Linux内核资源的隔离。使用命名空间后每个进程都具有独的系统运环境，包括主机名、网络协议栈、件系统等。命名空间关键特征是使进程相互隔离。

命名空间有不同的类型，每个都有其不同的特征。前持的主要有以下6种：①MountNamespace(挂载命名空间）;②Network Namespace（络命名空间）;③ IPCNamespace（interprocess communication namespace， IPC命名空间）； PID Namespace（process IDnamespace,PID命名空间);⑤UTS Namespace(UNIX Time-Sharing Namespace,UTS 命名空间）;⑥UserNamespace（用户命名空间）。

(3) Cgroups Cgroups是LinuxControlGroups的缩写，即控制组。通过控制组可以限制每组的进程的资源使用，包括CPU、内存、磁盘I/O和网络带宽资源等。通过监控配置的控制组，可拒绝控制组访问某些资源，也可在运行的系统上动态地重新配置控制组，从而实现对资源使用的细粒度控制。

## 2.容器运行时

容器运时（container runtime）是容器进程运和管理的具。常见具有lxc,runc、Imctfy、cri-o、docker(containerd）、rkt等。lxc（LinuxContainer）为用户提供工具集使用和管理lxc容器，实现轻量级的虚拟化;runc是由docker和容器开放接（open container interface，OCI)创建的开源项目，实现了容器启停、资源隔离等功能;lmctfy是Google发布的一个开源版本的Linux容器系统;cri-o是RedHat最早开发的项目。Containerd提供了较完整的容器功能，包括容器镜像传输和存储、容器执和管理、存储和络等。rkt是CoreOS公司发起的项目，提供了验证、下载、查询镜像，创建、运行和管理容器等功能。这些工具功能各有侧重，运行时可分为低层级(LowLevel)和层级（HighLevel）两类。低层级运时负责创建、运和管理容器。而层级运行时则要实现更多的功能，包括为容器准备必要的环境，对镜像进操作和管理，创建容器的网络等，可通过调用低层级的运时来启动容器。

## 3.容器规范

容器化前已成为现代软件基础设施的基础，由于Kubernetes容器技术涵盖了架构、研发、部署、运维等软件开发全流程，是一个基于容器技术的集群部署与管理系统。国内的阿里云、腾讯云、华为云等容器云平台均基于开源的Kubernetes构建。此处仅介绍Kubernetes持的容器规范。 0百用

（1）OCI规范（容器开放接口规范） OCI是由Docker,Google,CoreOS等多家公司于2015年共同成的项，并由Linux基会进管理，致于容器格式和运时制定个开放的业化标准。容器实际上有两种状态：静和运。在静状态下，个容器是个或组保存在磁盘上的件。这些被称为容器镜像（containerimage）或容器仓库（containerrepository）。当启动容器时，容器引擎会解压所需的件和元数据，然后把它们交给Linux内核。启动个容器如同启动个正常的Linux进程，需要对Linux内核进API调，该API调用通常会启动额外的隔离并挂载容器镜像中的件副本。一旦运，容器就只是一个Linux进程。容器启动的过程，以及磁盘上镜像的格式，都是由标准进行定义和管理的。前OCI包括两个标准：容器运时标准(runtime spec)和容器镜像标准(imagespec)。

1）runtime spec OCI运时标准对容器的配置、执环境和命周期进了规范。容器的配置信息存储在件config.json中，该件放在容器件系统包(filesystem bundle)根录，来详细说明创建容器的相关信息，包括实现对容器的标准操作所需的元数据,例如,要运的流程、要注入的环境变量、要使用沙箱的特征等。

2）image spec 容器镜像格式较多,如docker、LXD,为了增强互操作性,需要符合特定标准。OCI的容器镜像标准定义了OCI镜像标准，包括个镜像清单(image manifest)、个可选的镜像索引（image index）、一组件系统层（filesystem layer）和个配置（configuration）组成，其标是创建可互操作的具，于构建、移动和准备容器镜像的运。

其中ImageManifest清单件是组成个容器image的组件描述档;Image Index是镜像索引，是可选的，是指向不同的manifests和descriptors的列表。Image Layout是镜像布局，指镜像的内容布局，Filesystem Layer是件系统层，指个容器件系统的“变化集合”。ImageConfiguration是配置件，如应参数、环境等信息。

(2）CRI规范(container runtimeinterface，容器运行时接口规范） CRI是kubernetes推出的运时接，旨在通过统的接与各个容器引擎之间进互动,从隔离各个容器引擎之间的差异。为了与OCI进兼容,kubernetes还推出了CRI-O，它是CRI和OCI之间沟通的座桥梁，可便更多符合OCI标准的容器运时，接kubernetes进集成使。

(3）CNI(container networkinterface，容器网络接口） CNI是Google和CoreOS主导制定的容器网络标准，规范定义了种供管理员定义络配置的格式、容器运时向络插件发出请求的协议、基于提供的配置执插件的过程、插件将功能委托给其他插件的过程、插件将其结果返回到运时的数据类型等内容。CNI本身并不关心代码，它只关心容器的网络连接和删除容器时删除分配的资源。

(4) CSI(container storage interface，容器存储接口） CSI用于提供存储资源，由kubernetes、Mesos、Docker等社区成员联合制定的个业标准接规范，旨在将任意存储系统暴露给容器化应用程序。

## （）容器与虚拟机区别

容器是将操作系统的资源有效地划分为个一个孤的组，可在组之间更好地平衡有效利资源的技术。与虚拟机技术相主要区别有以下点不同：

## 1.虚拟化层次不同

容器和虚拟机都能将CPU、内存、磁盘和络等系统单资源虚拟化并表示为多个资源供使用，但容器和虚拟机的虚拟化层次不同。虚拟机将整个计算机虚拟化到硬件层，而容器只虚拟化操作系统级别以上的软件层。图11-2是容器和虚拟机虚拟化层次不同的意图。

![](images/cb29b836907f9c37a4596e70212ee13fc7684ca2e2793bc24d1c3f71526daa64.jpg)  
图 11-2容器和虚拟化层次差异

## 2.适应环境不同

容器是在主机上本地运行，并与其他容器共享主机的操作系统内核，在主机中以进程形式运行，而每一个虚拟机均具有自己的独立客户端操作系统，其内核可与主机操作系统不同。与虚拟机相比，容器占用更少的内存、启动快捷、迁移方便。虚拟机由于有自己独立的操作系统，适应性更强，从安全性角度看，虚拟机的隔离更加彻底安全。

当然，容器和虚拟机也可结合使用，可在虚拟机上运行容器，此时容器主机就是虚拟机。

## 第二节 虚拟机鉴定

## 一、虚拟机鉴定难点与方法

## (一)虚拟机鉴定难点

## 1.虚拟机发现较为困难

对虚拟机进行鉴定的前提是要找到各虚拟机对应的硬盘文件（或分区)和其他相关信息。由于各虚拟机相关数据存储目录用户可自定义，当虚拟机软件被卸载或者相关配置信息被删除后，要找到系统中对应的虚拟机将变得困难。要搜索所有的虚拟机信息，可利用虚拟硬盘的特殊格式，通过搜索技术在主机的所有硬盘中去分析和查找。采用全盘搜索技术能够较好地发现隐藏的、被删除的客户机数据，但前提是在鉴定时需要有这方面的意识。

## 2.虚拟机状态确定较为重要

虚拟机系统与主机系统不同的是，虚拟机是可复制和移动的，在本地主机中存在的客户机不一定是在本机上创建和最初使用的。因而需要确定虚拟机创建的时间，以及所使用的虚拟硬盘是否在本地最初创建。如果是从他人电脑中复制而来，在调查案件时应重点关注虚拟机创建以后虚拟硬盘中数据变化情况。

除关注虚拟硬盘数据状态外，虚拟机是否处于开机状态也是在鉴定中需要考量的问题。通常情况下，可通过生成快照的方式对当前状态进程固定。

## 3.时间关系可能更加复杂

虚拟机有独的时间系统，有一些日志记录的时间信息是相对于主机时间的偏移信息，无论是主机的时间修改变化，还是客户机系统的时间变化都可能影响电数据信息的准确性并增加案件还原的难度。因在调查分析证据前，对主机系统时间是否准确、是否调整过时间、客户机系统时间是否准确、是否调整过时间等信息进分析,是解决时间错乱引起分析困难的必要步骤。

## 4.虚拟机损坏和被删除的恢复问题

当虚拟机完好时，通过复制虚拟机便可进动态仿真分析。但虚拟硬盘件即使出现极的差错，分析时都可能存在困难。此时应根据不同的场景，采不同的案进分析。例如，可对虚拟硬盘格式进转换以便现有鉴定软件能够识别和分析，但应考虑转换前后数据内容的差异点。必要时，还需要通过动分析法进纠错或分析。

## （二）虚拟机鉴定的程序和方法

不同的鉴定场景，对虚拟机鉴定关注点是不同的，因而具体程序和方法也存在差异，以下按照常见情形阐述虚拟机鉴定程序和方法：

## 1.虚拟机全局配置件和环境数据的提取和固定

在对虚拟机分析前，先要判断提取和固定数据的范围，需要对主机和虚拟机软件全局配置信息进分析，并根据需要进提取固定。包括主机中虚拟机列表、各虚拟机的基本信息、主机的时间信息、时间变动情况、主机中与虚拟机软件和虚拟机有关的系统志、虚拟软件志等。

## 2.开机状态下虚拟机状态的固定

当虚拟机在开机状态时，可通过快照法或者开机状态下提取内存等易失性数据提取法进数据固定。

## 3.各虚拟机数据的固定

对虚拟机数据固定内容包括虚拟机所有的志信息、快照信息、虚拟硬盘数据信息、内存信息等。般情况下直接对相关件进复制固定便可。

## 4.动态和静态分析相结合方法分析

当提取固定好虚拟机数据后，需要对提取和固定的数据进一步进分析。对虚拟机数据的分析宜采动态分析和静态分析相结合法进。由于虚拟机内部数据的鉴定与各虚拟机操作系统和应密切相关，不同系统其技术点和法均不同,具体如何鉴定请参阅相关章节的分析。本章仅就虚拟机有关数据进分析，不涉及虚拟机系统内部数据的鉴定。

虚拟机动态分析可通过配置相似的虚拟机环境直接运后进分析，而虚拟机静态分析则是直接对虚拟硬盘文件和虚拟机内存镜像进分析，它与传统硬盘和内存镜像的鉴定方法和具均相同。但鉴定软件有可能对某些虚拟硬盘件格式法有效识别，此时需要通过虚拟机管理工具或第三方软件将虚拟硬盘件格式转换为可分析的虚拟硬盘格式再进分析。转换后丢失的信息如果需要进步分析，则可通过分析法进分析。

## （三）删除或损坏虚拟机分析

虚拟机如果被删除，需要通过搜索和恢复技术将其进恢复，然后再进行分析。如果虚拟机硬盘件数据有损坏，可通过以下两种方案进分析：第一种案是直接对损坏虚拟硬盘进静态分析，从中搜索和恢复出可以识别的有效数据;第种案是尝试对虚拟硬盘进修复，如果损坏较小，可通过格式修复后使得鉴定软件或者虚拟机管理软件能够识别，通过转换具转换后再进分析。

对损坏虚拟机分析基础是了解虚拟机硬盘件格式和结构，关于各虚拟机硬盘件的结构将在各虚拟机鉴定部分进分析。

## （四）加密虚拟机分析

虚拟机如果被加密，对应的虚拟硬盘数据也会被加密，不仅无法直接访问虚拟机，也无法通过鉴定软件对虚拟硬盘进行分析，需要先对其破解，等清除密码后再进行分析。

多数虚拟机软件均有设置加密的选项。在VMwareWorkstation软件中，可通过虚拟机设置中“选项”下的“访问控制”进设置;在ParallersDesktop软件中，可在配置时通过“安全性”下的“使用密码加密”选项进加密；在VirtualBox软件中，可通过“常规”下的“虚拟机加密”来选择加密的算法。

除此之外，还可直接通过虚拟机管理命令具进虚拟机的加密，以VirtualBox为例，加密个未加密的虚拟机可使如下命令格式：

VBoxManage encryptvm <uuid>I <vmname> setencryption -new-password <filename>I- -   
cipher <cipher-ID> --new-password-id <ID>

其中,filename是指存储密码的件，也可使用“-表示通过命令提示符输;--cipher选项指定加密方法，支持AES-128或AES-256;-new-password-id是可选项，用来指定密码标识符，当虚拟机有多个密码时此来正确识别。

要对加密虚拟机进破解，需要了解其加密方法，并选择相应的破解方法。需要注意的是，随着虚拟机软件版本的更新，其加密方法可能也会随之改变或更新。根据相关资料的查阅，前虚拟机VMware使AES-128加密算法，使10000轮的PBKDF-SHA1哈希值来从密码中得出加密密钥。Parallels使AES-128CBC算法来加密数据，加密密钥通过MD5哈希函数的两次迭代得出。VirtualBox加密算法可选择AES-XTS128-PLAIN64或AES–XTS256-PLAIN64，而加密密钥采用了SHA-256哈希函数，哈希迭代次数取决于AES加密密钥的长度，可达120万次哈希迭代值。

对于加密虚拟机的破解，通常采用字典攻击或者暴力破解的方式进，能否破解及破解所需时间，依赖加密算法的强度、字典、破解的设备等多种因素。破解的基本方法如下：

1）选择字典攻击或暴力破解对应的件。通常，选择虚拟机文件夹里较小的文件，对于VMware,选择.vmx文件;对于Parallels,选择config.pvs文件;对于VirtualBox选择.vbox文件。

2）选择相应的持软件或者编写相关的代码。例如，ElcomsoftDistributedPasswordRecoveryV.4.45密码破解软件支持VMware、Paralls、VirtualBox加密虚拟机的密码破解；另外在Github上也有破解加密虚拟机的相关代码，对于.vmx件可使用axcheron/pyvmx-cracker（htps://github.com/axcheron/pyvmx-cracker）；对于.vbox文件可以使用sinfocol/vboxdie-cracker(https://github.com/sinfocol/vboxdie-cracker)进行破解。

3）搭建环境或安装软件、进破解。

## 二、常见虚拟机鉴定

## (一)VMware鉴定

## 1.vmware虚拟机主要文件信息

（1）志件 虚拟机主录下有件名为vmware或者虚拟机名称开头的志件，如vmware.log,vmware-0.log等。该志件为虚拟机的调试志件，记录了虚拟机运的志，通过该志可发现件创建、USB接、户为时间、主机操作系统基本信息等。

（2）虚拟机配置文件 扩展名为.vmx的件是Vmware workstation虚拟机配置件，其包含了CPU、内存、硬盘等硬件配置信息。另外扩展名为.vmxf的件是附加配置件。.vmx件可直接通过记事本查看其内容。如果虚拟机被加密，.vmx件内容也会被加密。

（3）虚拟磁盘文件 扩展名为.vmdk的件是虚拟硬盘件，记录了操作系统全部相关数据。通常.vmdk件存储在虚拟机主录，但也可以放在其他录。在鉴定时要根据虚拟机.vmx配置件进分析。关于VMDK虚拟硬盘件的硬盘结构请查看本章第四节中的介绍。

虚拟硬盘可以是单个vmdk件，也可以是拆分的多个件。单个件虚拟硬盘的件名通常为vmname.vmdk,其中vmname为虚拟机名称。如果虚拟机包含多个虚拟硬盘，则名称通常为vmname-#.vmdk，其中#为数字。当虚拟硬盘在创建时不具有固定大小，且拆分为多个件时，即拆分为2GB小的件，通常虚拟硬盘名称为vmname.vmdk、vmname-s001.vmdk、vmname-s002.vmdk、vmname-s003.vmdk ...…,其中vname-s###.vmdk（注：#代表0—9的数字，下同)是实际存储硬盘数据的，具有2GB大小的拆分件。如果创建虚拟硬盘采用了预分配形式，则硬盘名称常为vname-f###.vmdk的形式。

对于VMDK件来说，如果是未破坏或未加密的，可使用能够识别vmdk件的鉴定软件直接加载进行分析，也可通过挂载软件挂载为硬盘后，通过鉴定软件进行分析。挂载的方法有很多，可利VmwareWorkstation的映射功能或者Vmware-Mount等具挂载或映射虚拟硬盘。

（4）虚拟机内存文件 扩展名为.vmem的件是虚拟机内存件，包含了操作系统内核数据结构、进程、线程、堆中的数据，以及用户有关的数据如用户输入的密码、聊天信息等敏感信息；正常情况下虚拟机关机后，vmem文件就会消失；但虚拟机的系统处在挂起状态时，该件会保留在本地。另外对虚拟机进快照时，也会成对应的.vmem内存件。

对VMware虚拟机内存的分析，使用较新版的volatility可直接进解析，而不需要进转储。若要转储后进分析，可使volatility的raw2dmp插件进转换。

(5）快照件 扩展名为.vmsd和.vmsn的件来记录快照信息、元数据和状态。多次快照虚拟机后，其仅成个.vmsd件，每次快照均有个对应的.vmsn件。

快照件名般以“虚拟机名-snapshot#”为名称，其中.vmsn件来存储当前使的快照状态，记录了当前快照的元数据。而.vmsd文件记录了虚拟机快照有关信息和元数据，UID编号、快照文件名、快照注释、执行快照的虚拟硬盘文件和快照总数等。初始大小为0字节，随着快照数的增加持续增。另外，每个快照均有个对应的.vmem内存件。

（6）挂起状态文件 虚拟机挂起状态时，也有两个相关联的文件，一个为扩展名为.vmss的件，个扩展名为.vmem的件。前者记录虚拟机处于已挂起状态的信息件，后者记录内存的件。件名般形如“虚拟机名-###.vmem”和“虚拟机名-###.vmss”

（7）其他文件还有一些件，在鉴定中一般关注较少。扩展名为.nvram的文件，该文件记录虚拟机BIOS状态信息。以.lck结尾的录，该录是虚拟机系统在开机时动创建的，每个目录下均有若干以扩展名.lck结尾的件，其目的是锁定vmx的件夹，在虚拟机关机后会动删除。但如果虚拟机异常退出，这些件依然保留。

## 2.虚拟机在主机中配置和日志

在进虚拟机鉴定时，需要了解虚拟机所在主机的状态，包括时区、操作系统信息以及虚拟机是否在本机运、何时运等有关信息，此时需要利虚拟机所在主机中记录的相关信息进分析。在Windows10系统中，除了对Windows志、注册表、Prefetch等传统鉴定信息分析外，具有定价值的虚拟机配置和志信息还有以下处：

(1）temp录下的志件 在windows系统的temp录下，有虚拟机安装运时的有关信息，例如可通过件分析主机的时区信息、虚拟机运的时间、主机运信息，这些对某些案件鉴定有定帮助，其位置常为“C:\Windows\Temp\vmware-SYSTEM”。

（2）Roaming录下的客户机列表信息 通常在户的AppData\Roaming\Vmware录下存储客户机的列表信息，即虚拟机打开后左侧“库”栏的客户机列表信息。

(3）其他 当虚拟机开启vmwaretools时，在虚拟机和主机之间拖拉件时，有可能会留下操作痕迹，即使原件已经被删除。例如从主机到Linux虚拟机拖拉件时，在户家录的“.cache/vmware/drag_and_drop”下会形成痕迹。

## (二)ESXi鉴定

ESXi是vSphere配置、创建、运虚拟机的平台，是vSphere鉴定的主要对象。对其鉴定主要包括对ESXi主机的有关志件、平台虚拟机信息以及各虚拟机的鉴定。

## 1.ESXi主机日志文件

要对ESXi主机的有关活动情况进分析，需通过主机中的日志信息进分析，ESXi主要志件如表11-1所。

表11-1 ESXi主机主要日志件
<table><tr><td>名称</td><td>位置</td><td>主要内容</td></tr><tr><td>身份验证子系统日志</td><td>/var/log/auth.log</td><td>包含本地系统身份认证相关的所有事件（注：可 以通过登录到vmware ESXi控制台查看，也可固定 后分析查看，下同）</td></tr><tr><td>DHCP客戶端日志</td><td>/var/log/dhclient.log</td><td>记录DHCP客户端服务，包括发现、解决租赁请求 和更新信息</td></tr><tr><td>ESX更新日志</td><td>/var/log/esxupdate.log</td><td>记录ESXi补丁安装和更新信息</td></tr><tr><td>Fault Tolerance 管理代理日志/var/log/fdm.log</td><td></td><td>vSphere High Availability 日志</td></tr><tr><td>主机代理日志</td><td>/var/log/hostd.log</td><td>包含代理程序管理和配置ESXi主机及其虚拟机 的信息</td></tr><tr><td>ESXi Shell活动日志</td><td>/var/log/shell.log</td><td>该日志包含了键入 ESXi Shell 的所有命令和 Shell 事件记录</td></tr><tr><td>系统引导日志</td><td>/var/log/sysboot.log</td><td></td></tr><tr><td>常规系统日志</td><td>/var/log/syslog.log</td><td>该日志记录了所有常规消息</td></tr><tr><td>vMotion身份验证守护进程 日志</td><td>/var/log/vmauthd.log</td><td></td></tr><tr><td>VMkernel 设备管理日志</td><td>/var/log/vmkdevmgr.log</td><td></td></tr><tr><td>VMkernel子系统中的日志</td><td>/var/log/vmkernel.log</td><td>记录ESXi活动和与虚拟机有关的活动，包括设备 发现、存储和联网设备和驱动程序事件以及虚拟 机启动等</td></tr><tr><td></td><td>VMkernel 事件守护进程日志/var/log/vmkeventd.log</td><td></td></tr><tr><td>VMkernel警告日志</td><td>/var/log/ vmkwarning.log</td><td>记录警告日志消息的摘要</td></tr><tr><td>VMware 监测守护进程日志</td><td>/var/log/vobd.log</td><td></td></tr><tr><td>vCenter代理日志</td><td>/var/log/vpxa.log</td><td>记录与vCenterServer通信的代理有关信息</td></tr></table>

通过VsphereESXi客户端工具，可连接到服务器。例如，通过浏览器输入服务器地址，登录后便可对服务器进行管理。点击“监控”，通过“日志”“事件”“任务”等信息可分析ESXi服务器的活动情况。

## 2.虚拟机客户机主要文件信息

通过Vsphere ESXi创建的虚拟机客户机目录下文件与VMwareWorkstation创建的虚拟机客户机目录大体相似。通过浏览器直接连接ESXi虚拟机，便可通过WEB管理服务器管理虚拟机和存储资源。通过点击“存储”，选择对应的虚拟机录，该录下存储有配置件、虚拟机志件、快照信息和虚拟硬盘件等内容，信息与vmware workstation类似。

## 3.虚拟机的导出方法

如果要对虚拟机内数据进鉴定分析，可通过数据存储浏览器将对应录下的所有件都下载后进行分析。也可通过虚拟机的导出功能将虚拟机导出后，对虚拟机进行分析。ESXi导出虚拟机的方法为：在虚拟机关闭的前提下，选择需要导出的虚拟机，鼠标右键弹出菜单后，选择“导出”功能，再选择导出的“文件”便可下载虚拟机进行分析。需要注意的是，如果需要对快照状态等进分析，直接下载虚拟机整个目录下件为相对较佳的选择。

## (三)VirtualBox鉴定

## 1.VirtualBox主要文件信息

Oracle VM VirtualBox目前支持Windows、Linux、macOS和 Solaris 等平台，创建虚拟机后，包括些配置件、虚拟硬盘和快照等信息，另外VirtualBox还会建一些全局配置信息。在不同操作系统中，这些文件的具体位置可能有所不同。在Windows系统中，默认情况下客户机主目录是Windows系统库Shell32.dll的 SHGetFolderPath函数返回的位置，一般为C：\Users\[username]。表11–2 所列内容是在Windows环境下，与VirtualBox鉴定相关的证据信息。

表11-2Windows 环境下VirtualBox虚拟机相关证据信息与位置
<table><tr><td>证据类别</td><td>默认目录位置</td><td>主要证据信息</td><td>备注</td></tr><tr><td>信息</td><td>程序安装目录C:\Program Files（x86) \Oracle \VirtualBox</td><td>在程序安装目录内包含虚拟机运 行相关的各种.dll文件、驱动、模 板等文件，在对DLL注入和恶意 软件有关案件调查时，VirtualBox 有可能成为攻击目标，此时该目 录下文件将是调查关注点之一</td><td>安装时程序的目录 可修改</td></tr><tr><td>信息</td><td>VirtualBox全局 C:\Users\[username] \.VirtualBox</td><td>有关VirtualBox虚拟机的环境信 息和日志等</td><td>[username]指用户名</td></tr><tr><td>虚拟机相关信C：\Users\username] 息</td><td>\VirtualBox VMS</td><td>各客户虚拟机信息，包含客户机 的配置文件、虚拟硬盘、快照和日 志等文件</td><td>创建客户机目录在创 建时可通过 VirtualBox Management 进行任意 设置</td></tr><tr><td>和日志信息</td><td>宿主机注册表Windows：注册表与系统日志与VirtualBox 运行有关的日志可 Linux：系统日志</td><td>通过主机系统日志进一步分析</td><td></td></tr></table>

## （1）关于VirtualBox虚拟机目录的证据信息

1）.vbox件 在虚拟机录下有扩展名为.vbox和.vbox-prev的件，其中.vbox扩展名件是虚拟机的配置件，是XML格式，包含虚拟机的软硬件配置信息。.vbox-prev扩展名的件是历史版本的vbox配置件，起到备份的作。

2）.vdi件 扩展名为.vdi的件是VirtualBox默认格式的虚拟硬盘件，件名称和格式都在.vbox配置文件中指定。VirtualBox除支持.vdi格式的VDI虚拟硬盘外，还持VMware的VMDK虚拟硬盘件、微软的VHD虚拟硬盘件、苹果的HDD虚拟硬盘件。关于VDI硬盘分析参见“VDI件结构”部分的分析。

3）志文件 每次VBox启动，都会产生一个log（志）文件，其扩展名为.log或形于.log.1、.log.2、.log.3等历史记录志文件。通过志文件可分析虚拟机的启动时间、访问的资源、宿主机的有关信息，以及运行的时长等。

4）快照文件VirtualBox可以生成快照，快照文件夹下包括扩展名为.sav的文件和扩展名为.vdi的快照件。在对快照件进分析时，需要结合快照VDI件和主VDI以及存在父子关系的快照VDI进分析。主VDI和快照VDI之间的关系可通过文件头进分析。在VDI文件头中，有字段自身UUID和上一个快照的UUID，通过这些信息可分析出主VDI和各快照VDI之间的关系，如图11-3所示。

![](images/2ffb644dd29ba1305778ea0696bde23f7bf2d7280c9ee5a1363113a5f23cbe73.jpg)  
图11-3快照VDI的链条分析

上图快照件在其.vdi件内记录了VDI链的上一个.vdi件的UUID号，其上一个件是主文件。当快照比较多时，这种链条比较复杂，必须先把它们之间依赖关系分析清楚，才能进一步分析。当需要对某个快照进行静态分析时，可根据上述VDI之间的联系，通过虚拟硬盘格式转换具先转换为单一的虚拟硬盘件，然后再进分析。快照件进合并法有很多，例如，可通过删除快照的方法，将快照数据合并到文件中；可通过在当前状态下导出虚拟机转换为虚拟硬盘格式进行分析，还可通过复制虚拟硬盘的方式将快照虚拟硬盘及父盘合并到一个新虚拟硬盘中。

5）内存信息 在快照或挂起时，虚拟机的内存信息也保存了，可通过恢复到特定快照状态，通过VBoxManager的debugvm命令dump虚拟机的完整物理内存，然后通过volatility的vboxinfo插件进分析。或者直接通过内存提取具固定内存后再通过volatility等具进分析。

## （2）关于VirtualBox的全局信息

1）selectorwindow.log 该志记录了VirtualBox内带具的操作信息，当虚拟环境的存储介质或络发变化时，事件将记该志。

2）VBoxSVC.txtVBoxSVC.txt是VirtualBox服务进程的志信息，记录了VirtualBox虚拟化事件的志，通过该志可分析主机信息、主机操作系统信息、主机中的进程ID、虚拟机创建的相关信息。

3）VirtualBox.xml与VirtualBox.xml-prev VirtualBox.xml是关于VirtualBox应程序的当前配置信息,VirtualBox.xml-prev是其前次的历史配置信息。通过VirtualBox.Xml可分析出VirtualBox中的虚拟机列表信息，包括虚拟机UUID和虚拟机的路径信息。除此之外，本件还记录络信息、DHCP服务器信息等。

## 2.VDI文件结构与恢复

VDI件包括两部分信息：部分是元数据信息，部分是硬盘数据信息。元数据信息占0x200000个字节。其中元数据信息最关键的是前512个字节，其主要内容如表11-3所示。

表11-3 OracleVDI件头信息
<table><tr><td>偏移量</td><td>内容</td><td>说明</td></tr><tr><td>0x00-0x27</td><td>ASCII字符文件头</td><td>以ASCII字符形式表示的头部信息，占28个字节，通常为 “&lt;&lt;&lt;Oracle VM VirtualBox Disk Image &gt;&gt;&gt;”，不同版本的 VirtualBox其信息内容略有不同</td></tr><tr><td>0x40-0x43</td><td>文件签名信息</td><td>4个字节，固定为“7F10 DA BE”（注：VDI文件采用小头序形 式编码)</td></tr><tr><td>0×44-0x47</td><td>VDI的版本信息</td><td>记录版本号,01000100表示版本号为1.1</td></tr><tr><td>0x48-0x4B</td><td>头部大小</td><td>4 个字节表示头部大小，默认为0x190</td></tr><tr><td>0x4C-0x4F</td><td>镜像类型</td><td>镜像类型有以下几种： 1 = Dynamic 2=Static 4=Snapshot</td></tr><tr><td>0x50-0x53</td><td>镜像标志</td><td>通常为0</td></tr><tr><td>0x54-0x153</td><td>镜像描述</td><td>通常为0</td></tr><tr><td>0x154-0x157</td><td>虚拟硬盘前 Block 数量</td><td>记录虚拟硬盘开始前的块数量，块大小为512 字节</td></tr><tr><td>0x158-0x15B</td><td>数据偏移</td><td>记录虚拟硬盘开始的偏移量，默认为00002000，即偏移为 0x200000字节</td></tr><tr><td>0x168-0x16B</td><td>扇区大小</td><td>默认512字节，即默认为00 02 00 00</td></tr><tr><td>0x170-0x177</td><td>硬盘大小</td><td>以字节数为单位表示硬盘大小</td></tr><tr><td>0x178-0x17B</td><td>Block大小</td><td>字节数</td></tr><tr><td>0x17C−0x17F</td><td>Block附加数据</td><td></td></tr><tr><td>0x180-0x183</td><td>HDD的 block数量</td><td>VDI块的数量</td></tr><tr><td>0x184-0x187</td><td>分配的块数</td><td>指有数据的所有block 的数量</td></tr><tr><td>0x188-0x197</td><td>VDI 的UUID</td><td>VDI自己的UUID</td></tr><tr><td>0x198-0x1A7</td><td>最近一个快照的UUID</td><td>之前的一个快照的UUID</td></tr><tr><td>0X1A8-0X1B7</td><td>前一个LINK的UUID</td><td>链上的前一个VDI的UUID</td></tr><tr><td>0X1B8-0X1C7</td><td>父UUID</td><td>VDI硬盘的数据实际存放在0x200000偏移之后</td></tr></table>

目前，大多数鉴定软件可直接识别VMDK文件，但仅有一部分鉴定软件可识别分析VDI硬盘文件。分析VDI软件时，可通过手动分析方法对硬盘的元数据进行分析，然后利用VirtualBox管理器的硬盘格式转换功能将其转换为VMDK件后进加载分析。

转换命令格式如下：

## VBoxManage.exe clonehd [sourcehd] [ targethd] --format vmdk

其中，[sourcehd]为转换前VDI硬盘的路径和文件名，[targethd]为转换后VMDK硬盘的路径和文件名。转换 vmdk文件后，再通过VMware中vmware-vdiskmanager工具进行转换，以便导入到VMware虚拟机。

## vmware-vdiskmanager.exe - [source.vmdk] -t 0 [target.vmdk]

其中，该命令-r表示硬盘格式的转换，-t表示转换后的硬盘类型，其后可接0\~6的数字。这些数字表示意义如下：0表示单个大小可增长的虚拟硬盘格式，1表示分割为若干2GB文件的大可增长的虚拟硬盘，2表示预分配的虚拟硬盘，3表示预分配的分割为若2GB件的虚拟硬盘，4表示预分配的ESX虚拟硬盘，5为流媒体优化的压缩硬盘，6为精简配置的虚拟硬盘ESX3.x及以上版本。

当VDI格式出错或者需要恢复数据时，可结合专VDI具进分析和恢复，以辅助解决部分鉴定软件无法处理的问题。

## (四)Hyper-V鉴定

## 1. Hyper-V主要文件信息

当创建一个虚拟机时，虚拟机的存储位置可自定义，默认位置为“C：\ProgramData\Microsoft\Windows\Hyper-V"，当选择创建虚拟硬盘时，默认位置一般为“C:\virtualDisk”，检查点（注：Hyper-V中检查点概念与vmware虚拟机中的快照概念类似)位置也可进单独设置，一般位置为“C：\ProgramData\Microsoft\Windows\Hyper-V"。需要注意的是不同类型的Hyper-V和不同版本的Hyper-V相关文件存储路径是不同的，有些存放在一个卷或目录下，有些可能分开存储，但主要件类别和内容基本相同的。

在Hyper-V主目录中有一个文件“data.vmcx”，该文件为Hyper-V虚拟机的全局配置信息，在VirtualMachines录中般存放虚拟机客户机的配置和运状态信息。在Snapshots件夹中存放的是Hyper-V检查点的有关信息。

(1).vmcx文件 VMCX（Virtual Machine Configuration）件指虚拟机配置件。论是主录下(data.vmcx)还是虚拟机或快照录下均有扩展名为.vmcx的件，该件内容是虚拟机配置信息或运时捕获的虚拟机配置信息。与VMware等虚拟机的配置件不同，较新版本的Hyper-V成的.vmcx件是进制格式的，不能通过记事本直接查看其信息。

(2).vmrs文件 VMRS件是Hyper-V虚拟机运时的状态数据，通常为活动RAM的大小。

(3).vmgs文件 记录客户机状态数据的件,在预计虚拟机将被持久化和多次重启的情况下，需要该件。

（4）虚拟硬盘文件 Hyper-V使的虚拟硬盘是VHD，它有两种类型.VHD和.VHDX。VHD是I旧版本虚拟硬盘格式,VHDX是新版本的虚拟硬盘格式,能提供VHD更好的性能与容错能，WindowsServer2012以来便直存在。当创建检查点后，会成.AVHD或.AVHDX扩展名的件，主要来存储检查点后新写的数据。

## 2.Hyper-V虚拟机的导出方法

将Hyper-V虚拟机导出后再对虚拟机内部数据进静态或动态分析是常见的分析法。Hyper-V虚拟机可通过Powershell提供的命令进导出，也可通过Hyper-V管理器GUI界进导出。图11-4是通过PowerShell导出的法。主要采Export-VM命令，可-name指定虚拟机名称，-path选项指定导出位置，导出指定的虚拟机，也可通过“Get-VMIExport-VM”命令导出所有注册的虚拟机。

![](images/109663112f752d074d8f39312dd79e3f54f8ffe330f058d4621bd1ccb6177be2.jpg)  
图11-4 通过Export-VM命令导出虚拟机

图11-5是通过Hyper-V管理器导出的法。选择想要导出的虚拟机，右键选择“导出”，在导出虚拟机对话框选择导出件的位置,便可导出虚拟机。

![](images/234eede81a7dab05ba6fe0e5559771a56997104a705c9c1eefc2852c728219e4.jpg)  
图11-5Hyper-V虚拟机导出

导出后，在导出录建了以虚拟机名称命名的件夹。在该件夹下包含三个录，分别是Snapshots、Virtual HardDisks、VirtualMachines，分别保存了检查点、虚拟硬盘、虚拟机配

置和运行时状态等数据。

## 3.Hyper-V虚拟机配置信息和日志分析

(1) data.vmcx data.vmcx件记录了关于所有注册虚拟机的基本信息。对于没有注册的虚拟机，对其vmcx文件分析可通过导到Hyper-V进分析，但这会改变Hyper-V的注册虚拟机信息。

(2）各虚拟机的vmcx文件 每个虚拟机录下都有个vmcx件，该件是进制件，记录了虚拟机配置的相关信息，可通过管理端直接查看虚拟机配置信息。如果要在鉴定设备上分析vmcx件，可将虚拟机导鉴定环境中的Hyper-V进分析，也可通过PowerShell中Get-VM、Set-VM、Export-VM、Import-VM 等命令结合分析。

(3) 虚拟机日志文件分析 Windows应用和服务日志中有若干Hyper-V有关事件志，主要日志文件包括 Microsoft-Windows-Hyper-V-Compute-Admin. evtx、Microsoft-Windows-Hyper-V-Compute-Operational. evtx、Microsoft-Windows-Hyper-V-Config-Admin. evtx、Microsoft-Windows-Hyper-V-Config-Operational. evtx、Microsoft-Windows-Hyper-V-Guest-Drivers% 4Admin.evtx、Microsoft-Windows-Hyper-V-Hypervisor-Admin. evtx、Microsoft-Windows-Hyper-V-Hypervisor-Operational.evtx、Microsoft-Windows-Hyper-V-StorageVSP-Admin.evtx、Microsoft-Windows-Hyper-V-VID-Admin. evtx、Microsoft-Windows-Hyper-V-VMMS-Admin. evtx、Microsoft-Windows-Hyper-V-VMMS-Networking. evtx、Microsoft-Windows-Hyper-V-VMMS-Operational. evtx、Microsoft-Windows-Hyper-V-VMMS-Storage. evtx、Microsoft-Windows-Hyper-V-VmSwitch-Operational. evtx、Microsoft-Windows-Hyper-V-Worker-Admin.evtx、Microsoft-Windows-Hyper-V-Worker-Operational.evtx 等。

## 4.VHDX结构分析

微软的虚拟硬盘格式早期为VHD，是一种以文件来表示硬盘镜像的格式，支持固定大小硬盘和动态小硬盘两种类型。WindowsServer2012为Hyper-V3.0引了名为VHDX的新虚拟磁盘格式，其存储容量I旧的VHD格式得多，而且它还能在电源故障期间提供数据损坏保护，并优化动态磁盘(dynamicdisk）和差异化磁盘(diferencingdisk）的结构对齐，以防止扇区物理磁盘的性能下降。VHDX前持三种类型的虚拟硬盘：固定(fixed)虚拟硬盘、动态(dynamic)虚拟硬盘和差异化(differencing）虚拟硬盘。固定虚拟硬盘文件大小固定，不会随着数据的添加或删除而增长或缩小。动态虚拟硬盘其大是动态变化的，随着更多的数据被写，该件通过分配更多的空间动态地增加，直设定的有效载荷上限。差异化虚拟硬盘，记录与虚拟硬盘文件相比的差异部分块，当读取特定磁盘偏移量数据时，先通过最新的子虚拟硬盘上寻找，如果未找到数据，便从父虚拟硬盘上搜索，通过这种方式一直遍历。VHDX文件包括三个部分：头部、非重叠对象和空闲空间。其中，头部始终在文件头部、对象和空闲空间位置可相互交叠，对顺序没有特别要求，唯一的限制是所有对象在件中都要求1MB对齐，其布局如图11-6所示。

![](images/8adf86f8274ab5fbadc3eae791c79e0bc2c416e3b36790759cc44f19e965deb6.jpg)  
图11-6VHDX文件的布局实例

除了头部结构（Header）以外，前在VHDX件中定义的结构还包括块分配表（BlockAllocationTable,BAT）、元数据区域（MetadataRegion）、志（Log）、有效载荷块（PayloadBlocks)和扇区位图块(Sector Bitmap）。

(1）头部结构 头部结构包括5个项，分别是件类型识别符、两个头(Header)结构、两个区域表(RegionTable），每个项为64K，其布局如图11-7所。

<table><tr><td colspan="6">0KB 64KB 128KB 192KB 256KB 320KB 1MB</td></tr><tr><td>FileType Identifier</td><td>Header 1</td><td>Header 2</td><td>Region Table1</td><td>Region Table2</td><td>Reserved</td></tr></table>

图11-7 VHDX头部结构的布局

通过VHDX头部结构中的Header可判断Log位置和，通过RegionTable可定位BAT、MetadataRegion的位置。VHDX的整个逻辑布局如图11-8所。

![](images/ed70e0abeab2df7583c7e4299cd81fa8d6003cec88428d448bde11d3904bfee8.jpg)  
图11-8 VHDX的逻辑布局

件类型识别符包含件签名信息和创建者信息。签名为“0x7668647866696c65”，对应的ASCII字符为“vhdxfile”。在0x20000偏移处记录了vhdx的创建信息。

头部结构中的两个Header在同时刻只能有个是激活状态,此时该头部信息可进更新。在Header有个8字节的序列号(SequenceNumber)字段，仅当本Header有效且其序列号于另外个Header的序列号时，该Header才是当前有效的。在Header中还有个16字节的FileWriteGuid和16字节的DataWriteGuid字段，当VHDX件发更改，包括系统元数据、户元数据和志等信息发更改时，FileWriteGuid都会进更新，将会成新的独的GUID值。但DataWriteGuid字段仅有户可见数据发改变时才进更新，例如数据块在件内的移动不会改变其值，但虚拟磁盘大小、块数据发生变化会引起其变化。Header还记录了LogGuid、版本、小（Loglength）、位置（偏移量LogOffset），如图11-9所示。 【善雅集】对电子责料不主张任何权利，仅供公众及法律从业者、学生等法 完学习之用，请勿商用。

头部结构的Region表记录了件内部对象的标识符和位置信息，包括4字节签名、4字节校验和、4字节条数,4字节保留、16字节的Guid、8字节的件偏移信息、4字节的长度信息和是否必须等信息。记录已知 Regions包括 BAT 和Metadata Region，其GUID分别为2dc27766-f623-4200-9d64-115e9bfd4a08、8b7ca206-4790-4b9a-b8fe-575f050f886e，BAT偏移0x300000,metadata偏移0x200000,如图 11–10、图11–11、图11–12 所示。

<table><tr><td>Offset</td><td>0 1</td><td>2</td><td>3</td><td>4</td><td>5</td><td>6</td><td>7</td><td>8</td><td></td><td>9</td><td>A</td><td>B</td><td>C</td><td>D</td><td>E</td><td>F</td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>00000FFFO</td><td>000000</td><td></td><td>00</td><td>00</td><td></td><td>00</td><td>00</td><td>00</td><td></td><td>00</td><td></td><td>00</td><td>00</td><td></td><td>00</td><td>00</td><td></td><td>00</td><td>00</td><td>00</td><td></td><td></td><td></td><td></td></tr><tr><td>000010000</td><td>68 65 61 64 93</td><td></td><td></td><td></td><td></td><td>D5</td><td></td><td>5F</td><td>65</td><td></td><td>10</td><td></td><td>品</td><td></td><td>0</td><td>00</td><td></td><td>00</td><td>0</td><td></td><td>00</td><td></td><td>00</td><td>headlo_e...</td></tr><tr><td>000010010</td><td>E4</td><td>OD</td><td>BO</td><td>88</td><td>42</td><td>F1</td><td></td><td>34</td><td>45</td><td></td><td>95</td><td></td><td>1C</td><td>02</td><td></td><td>67</td><td></td><td>4F</td><td></td><td>2D</td><td>61</td><td></td><td>F4</td><td></td></tr><tr><td>000010020</td><td>9F</td><td>CD</td><td>06</td><td>E4</td><td>5C</td><td>91</td><td></td><td>C4</td><td></td><td>46</td><td>AB</td><td></td><td>9C</td><td>59</td><td></td><td>8F</td><td></td><td>1A</td><td>B2</td><td></td><td>70</td><td></td><td>E6</td><td>a.IBn4EI..g0-aδ If.a\AF《IY..²p</td></tr><tr><td>000010030</td><td></td><td></td><td></td><td></td><td>0</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>00</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>000010040</td><td>品 </td><td></td><td></td><td>0</td><td></td><td>00</td><td></td><td></td><td></td><td>0</td><td></td><td>0</td><td></td><td>0</td><td></td><td>0</td><td></td><td>0</td><td>0</td><td></td><td>0</td><td></td><td></td><td></td></tr><tr><td></td><td>品 品 -- --</td><td>01</td><td>--</td><td>品 --</td><td>0 --</td><td>品 -</td><td>-</td><td>10 --</td><td>0</td><td>--</td><td>品</td><td>--</td><td>--</td><td>10 -</td><td>-</td><td>--</td><td></td><td>0</td><td>品 -</td><td></td><td>0</td><td></td><td>0</td><td></td></tr><tr><td>Offset</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>-</td><td>--</td><td>--</td><td></td><td></td></tr><tr><td>00001FFF0</td><td>0</td><td>1</td><td>2</td><td>3</td><td></td><td>4</td><td>5</td><td></td><td>6</td><td>7</td><td></td><td>8</td><td></td><td>9</td><td>A$</td><td></td><td>B</td><td>C$</td><td></td><td>D</td><td>E</td><td></td><td>F</td><td></td></tr><tr><td></td><td>00000000</td><td></td><td></td><td></td><td>00</td><td></td><td>00</td><td>00</td><td></td><td>00</td><td></td><td>00</td><td>00</td><td></td><td>00</td><td></td><td>00</td><td></td><td>00</td><td>00</td><td></td><td></td><td>0000</td><td></td></tr><tr><td>000020000</td><td>68 65</td><td></td><td>61</td><td>64</td><td>E4</td><td></td><td>49</td><td>A7</td><td></td><td></td><td>E7</td><td>11</td><td>00</td><td></td><td>00</td><td></td><td>00</td><td>00</td><td></td><td>00</td><td></td><td>00</td><td>00</td><td></td></tr><tr><td>000020010</td><td>E4 OD</td><td>BO</td><td></td><td>88</td><td>42</td><td></td><td>F1</td><td>34</td><td></td><td></td><td>45</td><td>95</td><td>1C</td><td></td><td>02</td><td></td><td>67</td><td>4F</td><td></td><td>2D</td><td></td><td>61</td><td>F4</td><td></td></tr><tr><td>000020020</td><td>9F CD</td><td>06</td><td></td><td>E4</td><td>5C</td><td></td><td>91</td><td>C4</td><td></td><td></td><td>46</td><td></td><td>AB 9C</td><td></td><td>59</td><td></td><td>8F</td><td>1A</td><td></td><td>B2</td><td></td><td>70</td><td>E6</td><td>log offset 0x100000</td></tr><tr><td>000020030</td><td>品 0</td><td>品</td><td></td><td>品</td><td>0</td><td></td><td>品</td><td></td><td></td><td></td><td>品</td><td>0</td><td>品</td><td></td><td>00</td><td></td><td>0</td><td>0</td><td></td><td>品</td><td></td><td></td><td>0000</td><td></td></tr><tr><td>000020040</td><td>0 0</td><td>01</td><td></td><td>0</td><td></td><td>0</td><td>0</td><td></td><td>10</td><td>0</td><td></td><td></td><td></td><td>□000</td><td>10</td><td></td><td>00</td><td>00</td><td></td><td>品</td><td></td><td>0</td><td>0</td><td></td></tr><tr><td>000020050</td><td>0</td><td>品 品</td><td></td><td>0</td><td></td><td>品</td><td>品</td><td></td><td>00</td><td>0</td><td></td><td></td><td></td><td>000000</td><td></td><td></td><td>00</td><td></td><td></td><td>0</td><td></td><td>0</td><td></td><td></td></tr></table>

图11–9 Head结构

<table><tr><td rowspan=1 colspan=1>Offset</td><td rowspan=1 colspan=10>0 1 2 3 4 5 6 7  8 9 A BC$ D EF</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>00002FFF0</td><td rowspan=1 colspan=10>0000000000000000 0000000000000000</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>000030000</td><td rowspan=1 colspan=10>□265 6769AE8C6BC6 02000品00000</td><td rowspan=1 colspan=1>regi@lkE..</td></tr><tr><td rowspan=1 colspan=1>000030010</td><td rowspan=1 colspan=10>6677C22D23F642 9D64115E9BFD4A08</td><td rowspan=1 colspan=1>fwA-#o.B.d.^IyJ.</td></tr><tr><td rowspan=1 colspan=1>000030020</td><td rowspan=1 colspan=10>03000品00 010000100000</td><td rowspan=4 colspan=1>…….....$|I.GIK,bW_..In</td></tr><tr><td rowspan=1 colspan=1>000030030</td><td rowspan=1 colspan=10>06A27C8B90479A4B B8FE575F05OF886E</td></tr><tr><td rowspan=1 colspan=1>000030040</td><td rowspan=1 colspan=10>0200品0品0 00100001品000</td></tr><tr><td rowspan=1 colspan=1>000030050</td><td rowspan=1 colspan=10>00000品000 000品00</td></tr><tr><td rowspan=1 colspan=1>Offset</td><td rowspan=1 colspan=10>0 1 2 3 4 5 67  8 9A$B C D EF</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>00003FFF0</td><td rowspan=1 colspan=10>0000000000000000 0000000000000000</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>000040000</td><td rowspan=1 colspan=7>72656769AE8C6BC6 02</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>0000000000</td><td rowspan=1 colspan=1>regi@IkE..</td></tr><tr><td rowspan=1 colspan=1>000040010</td><td rowspan=1 colspan=2>6677C22D</td><td rowspan=1 colspan=5>23F6品42 9D</td><td rowspan=1 colspan=1>64</td><td rowspan=1 colspan=1>11</td><td rowspan=1 colspan=1>5E9BFD4A08</td><td rowspan=1 colspan=1>fwA-#o.B.d.^IyJ.</td></tr><tr><td rowspan=1 colspan=1>000040020</td><td rowspan=1 colspan=2>品品300</td><td rowspan=1 colspan=3>00</td><td rowspan=1 colspan=2>品 </td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>10</td><td rowspan=1 colspan=1>品01品品0</td><td rowspan=1 colspan=1>.0..</td></tr><tr><td rowspan=1 colspan=1>000040030</td><td rowspan=1 colspan=1>06A27C</td><td rowspan=1 colspan=1>8B</td><td rowspan=1 colspan=1>90</td><td rowspan=1 colspan=2>479A</td><td rowspan=1 colspan=1>4B</td><td rowspan=1 colspan=1>B8</td><td rowspan=1 colspan=1>FE</td><td rowspan=1 colspan=1>57</td><td rowspan=1 colspan=1>5F05OF886E</td><td rowspan=1 colspan=1>.$|I.GIK,bW_..In</td></tr><tr><td rowspan=1 colspan=1>000040040</td><td rowspan=1 colspan=1>00020</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>10</td><td rowspan=1 colspan=1>0001000</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>000040050</td><td rowspan=1 colspan=1>品品0</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=3>品</td><td rowspan=1 colspan=2>0 品</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>品</td><td rowspan=1 colspan=1>0000</td><td rowspan=2 colspan=1></td></tr><tr><td rowspan=1 colspan=1>000040060</td><td rowspan=1 colspan=1>0.0.0</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=3>品%</td><td rowspan=1 colspan=2>g 8</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>e</td><td rowspan=1 colspan=1>gg00 00 00</td></tr></table>

图11– 10 两 Regions部分的数据内容

<table><tr><td>Offset</td><td>0</td><td>1</td><td>2</td><td>3</td><td></td><td>4</td><td>5</td><td>6 7</td><td></td><td>8</td><td>9</td><td>A</td><td>B</td><td>C</td><td>D</td><td>E F</td><td></td><td></td></tr><tr><td>000200000</td><td>6D</td><td>65</td><td>74</td><td>61</td><td></td><td>64</td><td>61</td><td>74 61</td><td></td><td></td><td>品</td><td>05</td><td></td><td>00</td><td>00</td><td>0</td><td>0</td><td>metadata.</td></tr><tr><td>000200010</td><td>回</td><td>品</td><td></td><td></td><td>品</td><td></td><td></td><td>0000</td><td></td><td></td><td></td><td>品</td><td></td><td>品</td><td>品</td><td>000</td><td>D</td><td></td></tr><tr><td>000200020</td><td>37</td><td>67</td><td>A1</td><td>CA</td><td></td><td>36</td><td>FA</td><td>43</td><td>4D</td><td>B3</td><td>B6</td><td>33</td><td>F0</td><td>AA</td><td>44</td><td>E7</td><td>6B</td><td>7giE6uCM338aDgk</td></tr><tr><td>000200030</td><td>品</td><td>0</td><td>01</td><td>品</td><td></td><td>08</td><td></td><td>00 </td><td></td><td>04</td><td>品</td><td></td><td>品</td><td>0</td><td>品</td><td>品</td><td>品 :</td><td></td></tr><tr><td>000200040</td><td>24</td><td>42</td><td>A5</td><td>2F</td><td></td><td>1B</td><td>CD</td><td>76</td><td>48</td><td>B2</td><td>11</td><td>5D</td><td>BE</td><td>D8</td><td>3B</td><td>F4</td><td>B8</td><td>$B￥/.IvH2.]x0；δ，</td></tr><tr><td>000200050</td><td>08</td><td>品</td><td>01</td><td>品</td><td></td><td>08</td><td>品</td><td>品</td><td></td><td>06</td><td>品</td><td>品</td><td></td><td>0</td><td>品</td><td>品</td><td>品</td><td></td></tr><tr><td>000200060</td><td>1D</td><td>BF</td><td>41</td><td>81</td><td></td><td>6F</td><td>A9</td><td>09</td><td>47</td><td>BA</td><td>47</td><td>F2</td><td>33</td><td>A8</td><td>FAAB</td><td></td><td>5F</td><td>.cA.o@.GΩGò3&quot;ú《_</td></tr><tr><td>000200070</td><td>10</td><td>品</td><td>01</td><td>品</td><td></td><td>04</td><td>0</td><td>0</td><td>0</td><td>06</td><td>品</td><td></td><td>品</td><td>0</td><td>品</td><td>品</td><td>品</td><td></td></tr><tr><td>000200080</td><td>C7</td><td>48</td><td>A3</td><td>CD</td><td></td><td>5D</td><td>44</td><td>71</td><td>44</td><td>9C</td><td>C9</td><td>E9</td><td>88</td><td>52</td><td>51</td><td>C5</td><td>56</td><td>CHEf1DqDIEeIRQAV</td></tr><tr><td>000200090</td><td>14</td><td>品</td><td>01</td><td>0</td><td></td><td>04</td><td>00</td><td>00</td><td></td><td>06</td><td></td><td>品</td><td>品</td><td>00</td><td>0</td><td>品</td><td>品</td><td></td></tr><tr><td>0002000A0</td><td>AB</td><td>12</td><td>CA</td><td>BE</td><td></td><td>E6</td><td>B2</td><td>23</td><td>45</td><td>93</td><td>EF</td><td>C3</td><td>09</td><td>EO</td><td>0</td><td>C7</td><td>46</td><td>《.Ex²#EIiA.à.CF</td></tr><tr><td>0002000B0</td><td>1800</td><td></td><td>01</td><td>00</td><td></td><td>10</td><td>00</td><td></td><td></td><td>0600</td><td></td><td></td><td></td><td>00</td><td>00</td><td></td><td>0000</td><td></td></tr><tr><td>0002000C0</td><td>AB12</td><td></td><td>CA</td><td>BE</td><td></td><td>E6B2</td><td></td><td>23</td><td>45</td><td>93EF</td><td></td><td>C3</td><td>09</td><td>E000</td><td></td><td></td><td>C746</td><td>《.Ex2#EiA.a.CF</td></tr><tr><td>0002000Dn</td><td></td><td>1800</td><td></td><td>g</td><td></td><td>10</td><td></td><td></td><td></td><td>06 00</td><td></td><td>品品</td><td></td><td></td><td>品</td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr></table>

图11– 11 Metadata的数据内容

<table><tr><td>Offset</td><td>0</td><td>1</td><td>2</td><td>3</td><td>4</td><td>5</td><td>6</td><td>7</td><td>8</td><td>9</td><td>$A}$</td><td>B</td><td>C</td><td>D</td><td></td><td>F</td></tr><tr><td>000300000</td><td></td><td>06 00</td><td>40</td><td>00</td><td>00</td><td>00</td><td>00</td><td>00</td><td>06 00</td><td>40</td><td>04</td><td>00</td><td>00</td><td>00</td><td>00 D</td><td>.@... @</td></tr><tr><td>000300010</td><td>00</td><td>00</td><td>00</td><td>00</td><td>00</td><td>00</td><td>00 00</td><td>00</td><td>00</td><td>00</td><td>00</td><td>00</td><td>00</td><td>00</td><td>00 .</td><td></td></tr><tr><td>000300020</td><td>06</td><td>00</td><td>40</td><td>06</td><td>00</td><td>00</td><td>00</td><td>00</td><td>06 00</td><td>40</td><td>6A</td><td>01</td><td>00</td><td>00</td><td>00</td><td>..@.. @j</td></tr><tr><td>000300030</td><td>06</td><td>00</td><td>40</td><td>6C</td><td>01</td><td>00</td><td>00 00</td><td></td><td>06 00</td><td>40</td><td>6E</td><td>01</td><td>00</td><td>00</td><td>00</td><td>..@1.. @n</td></tr><tr><td>000300040</td><td>06</td><td>00</td><td>40</td><td>70</td><td>01</td><td>00</td><td>00 00</td><td></td><td>06 00</td><td>40</td><td>90</td><td>01</td><td>00</td><td>00</td><td>00</td><td>..@p. .... .@</td></tr><tr><td>000300050</td><td>06</td><td>00</td><td>40</td><td>92</td><td>01</td><td>00</td><td>00 00</td><td></td><td>06 00</td><td>40</td><td>94</td><td>01</td><td>00</td><td>00</td><td>00</td><td>.@&#x27;.</td></tr><tr><td>000300060</td><td>06</td><td>00</td><td>40</td><td>08</td><td>00</td><td>00</td><td>00 00</td><td></td><td>00 00</td><td>00</td><td>00</td><td>00</td><td>00</td><td>00</td><td>00</td><td>..@..</td></tr><tr><td>000300070</td><td>00</td><td>00</td><td>00</td><td>00</td><td>00</td><td>00</td><td>00</td><td>00</td><td>00 00</td><td>00</td><td>00</td><td>00</td><td>00</td><td>00</td><td>00</td><td></td></tr><tr><td>000300080</td><td>00</td><td>00</td><td>00</td><td>00</td><td>00</td><td>00</td><td>00</td><td>00</td><td>00 00</td><td>00</td><td>00</td><td>00</td><td>00</td><td>00</td><td>00</td><td>...</td></tr><tr><td>000300090</td><td>00</td><td>00</td><td>00</td><td>00</td><td>00</td><td>00</td><td>00</td><td>00</td><td>00 00</td><td>00</td><td>00</td><td>00</td><td>00</td><td>00</td><td></td><td>·</td></tr><tr><td>0003000A0</td><td>06</td><td>00</td><td>40</td><td>OA</td><td>00</td><td>00</td><td>00</td><td>00</td><td>00 00</td><td>00</td><td>00</td><td>00</td><td>00</td><td>00</td><td>00</td><td>: ..@.</td></tr><tr><td>0003000B0</td><td>00</td><td>00</td><td>00</td><td>00</td><td>00</td><td>00</td><td>00</td><td>00</td><td>00</td><td>00 00</td><td>00</td><td>00</td><td>00</td><td>00</td><td>00</td><td></td></tr><tr><td>0003000C0</td><td>00</td><td>00</td><td>00</td><td>00</td><td>00</td><td>00</td><td>00</td><td>00</td><td>00</td><td>00 00</td><td>00</td><td>00</td><td>00</td><td>00</td><td>00</td><td>.</td></tr><tr><td>0003000D0</td><td>00</td><td>00</td><td>00</td><td>0</td><td>00</td><td>00</td><td>00</td><td>00</td><td>00</td><td>00 00</td><td>00</td><td>00</td><td>00</td><td>00</td><td>00 00</td><td>:</td></tr><tr><td>0003000E0</td><td>06</td><td>00</td><td>40</td><td>OC</td><td>00</td><td>00</td><td>00</td><td>00</td><td>00</td><td>00 00</td><td>00</td><td>00</td><td>00</td><td>00</td><td>00</td><td>: ..@</td></tr><tr><td>0003000F0</td><td>00</td><td>00</td><td>00</td><td>00</td><td>00</td><td>00</td><td>00</td><td>00</td><td>00</td><td>00 00</td><td>00</td><td>00</td><td>00</td><td>0</td><td>00</td><td></td></tr><tr><td>000300100</td><td>06</td><td>00</td><td>40</td><td>OE</td><td>00</td><td>00</td><td>00</td><td>00</td><td>02</td><td>00 00</td><td>00</td><td>00</td><td>00</td><td>00</td><td>00</td><td>..@.</td></tr><tr><td>000300110</td><td>02</td><td>00</td><td>00</td><td>00</td><td>00</td><td>00</td><td>00</td><td>00</td><td>00</td><td>00 00</td><td>00</td><td>00</td><td>00</td><td>00</td><td>00</td><td></td></tr><tr><td>000300120</td><td>06</td><td>00</td><td>40</td><td>10</td><td>00</td><td>00</td><td>00</td><td>00</td><td>00</td><td>00 00</td><td>00</td><td>00</td><td>00</td><td>00</td><td>00</td><td>..@.</td></tr><tr><td>000300130</td><td></td><td>00</td><td>00</td><td>00</td><td>00</td><td>00</td><td>00</td><td>00</td><td>0000</td><td>00</td><td>00</td><td>00</td><td>00</td><td>00</td><td></td><td></td></tr><tr><td>a000a04</td><td>00</td><td>00 00</td><td>00</td><td>6</td><td>00</td><td>00</td><td>00</td><td>00</td><td>00</td><td>00</td><td>0o 0</td><td>p</td><td>0 00</td><td>a0</td><td>00 00</td><td></td></tr></table>

图11-12 BAT记录的数据内容

(2）载荷块(Payload Blocks) VHDX中有两种类型的块，种是有效载荷块，记录虚拟磁盘载荷数据；种是扇区位图块(SectorBitmap），记录部分扇区位图信息。在BAT中记录了块的位置信息（块在件中的偏移），它由系列8字节值的数组组成。有效载荷块和扇区位图块偏移信息是按规律排列的,扇区位图块紧跟在个chunk后,每个chunk由若载荷块组成。如果chunk率是4,BAT记录的信息如图11-13所。

<table><tr><td rowspan=1 colspan=10>PB有效载荷块条SB扇区位图块条目</td></tr><tr><td rowspan=1 colspan=1>PB0</td><td rowspan=1 colspan=1>PB1</td><td rowspan=1 colspan=1>PB2</td><td rowspan=1 colspan=1>PB3</td><td rowspan=1 colspan=1>SB0</td><td rowspan=1 colspan=1>PB5</td><td rowspan=1 colspan=1>PB6</td><td rowspan=1 colspan=1>PB7</td><td rowspan=1 colspan=1>SB1</td><td rowspan=1 colspan=1></td></tr></table>

图11-13 BAT布局实例

通过查找BAT的有效载荷块，便可定位磁盘的每个数据块，其逻辑结构如图11–14所示。

![](images/c2bfa13e06399e852a63aeb0f95ab8dc5ae1ed2880ce62a2405906d06286851b.jpg)  
图11-14通过BAT定位数据

## 5.Hyper-V虚拟磁盘和合并方法

Hyper-V检查点对应的虚拟磁盘仅记录差异信息，对磁盘数据进分析可选择将磁盘合并后进。对Hyper-V虚拟磁盘进合并，先通过Hyper-V管理器提供的检查磁盘功能确定虚拟磁盘之间的依赖关系,通过点击“检查磁盘”,选择要分析的差异虚拟磁盘,将会弹出该磁盘属性，显示该磁盘的父级关系，进一步点击右下角的“检查父级”，依次查下去，直到没有显示父级。

再通过Hyper-V管理器提供的编辑磁盘功能合并虚拟磁盘。先将涉及的虚拟磁盘备份。然后点击“编辑磁盘”功能，通过向导步步选择“AVHDX虚拟磁盘”“合并”“合并到父虚拟磁盘”，最后，该虚拟磁盘将合并到父虚拟磁盘，再依次通过编辑磁盘工具将新合并虚拟磁盘合并到其磁盘，直差异虚拟磁盘全部被合并。

## (五)Parallels Desktop鉴定

## 1. Parallels Desktop主要文件信息

通过ParallelsDesktop创建虚拟机后，默认情况下会在当前户录的Parallels录下成个扩展名为.pvm的包件。对Parallels客户机进分析可通过复制固定该包，然后在鉴定分析平台进一步分析。查看该包件，其中有若干录和件，是Parallels虚拟机的主要件内容。

(1) config.pvs config·pvs是Parallels虚拟机的配置件，是以XML格式存储的。它有个树形结构，虚拟机的配置参数值存储在树的叶节点中，并按照功能分组。XML树的根元素是ParallelsVirtualMachine，它的直接子元素如表11-4所示。

表11–4 ParallelsVirtualMachine 的直接子元素
<table><tr><td colspan="2">元素 内容描述</td></tr><tr><td>AppVersion</td><td>包括 Parallels Destop的版本号和创建号</td></tr><tr><td>ValidRc</td><td>Parallels内部使用</td></tr><tr><td>Identification</td><td>包含识别主机上的虚拟机参数，包括虚拟机名称、UUID、文件位置和其他信息</td></tr><tr><td>Security</td><td>包含虚拟机的安全设置，这些设置由Parallels Desktop 内部使用</td></tr><tr><td>Settings</td><td>配置信息主要部分，包含虚拟机的一般配置参数、启动和关闭选项、运行选项、 Parallels Tools 选项等</td></tr><tr><td>Hardware</td><td>包含定义虚拟机硬件的参数，包括CPU、内存、磁盘驱动器、显卡、网络适配器、声卡、 USB等</td></tr><tr><td>InstalledSoftware</td><td>Parallels内部使用</td></tr></table>

在Identification元素中，VmUuid记录了虚拟机的UUID，ServerUuid记录了主机的UUID，VmFilesLocation记录了虚拟机的件位置，VmUptimeStartDateTime记录了虚拟机最后次启动的期和时间，VmUptimeInSeconds记录了虚拟机最后次启动后运的时间。

在Settings元素中,General组参数定义了客户机操作系统的类型、版本等信息，Startup组参数定义了自启动式、开机顺序、窗模式等信息，Shutdown组参数定义了关机的有关选项信息，Runtime组参数定义了虚拟机运时的有关选项信息。

(2）.app包 .app包记录了Parallels应包名、版本号、唯标识符等信息，解包后有个contents录,录下有若件和录。

(3).mem文件 .mem扩展名结尾的件是包含Parallels虚拟机的内存转储信息的件。

(4).hdd包 .hdd包存储了虚拟磁盘有关信息。解包后目录下有一个件名为DiskDescription.xml件,该件记录了虚拟机磁盘件的有关信息，包括快照对应的虚拟磁盘数据，以及快照磁盘之间的子关系等信息。而磁盘镜像的实际数据存储在.hds文件中。

(5）快照 Snapshot包记录的是虚拟机快照信息。其中.pvc件和.pvi件是XML格式的文件，记录了快照时虚拟机的基本信息，包括快照时间、虚拟机名称、虚拟机UUID、共享目录、HDD等信息。.sav件包含了虚拟机的状态,mem件包含了虚拟机内存转储信息。

## 2.虚拟机日志

在每个客户机PVM包解包后的根目录下有一个Parallels.log文件，该件记录了虚拟机运行情况和相关事件。通过该日志可分析软件信息、虚拟机路径、状态、快照情况，以及USB设备接入等信息。

## 3.其他日志

在虚拟录下还有个statistic.log件记录了虚拟机状态变化情况。除此之外,mac系统志可能还记录了parallels软件运信息，可能在某些案件鉴定中需要关注。

## （六）其他

## 1.Xen虚拟机鉴定要点

对xenserver中存储、虚拟机等信息的分析需要借助XenCenter管理平台，通过XenCenter可清晰地查阅xenserver中的虚拟机、存储等情况。当需要对特定虚拟机进分析时,也可使虚拟机的导出功能，导出后进步进分析。如果要对服务器进磁盘克隆，可制作E01镜像或DD镜像。Xen虚拟机不同于Vmware等虚拟机，其虚拟磁盘不对应虚拟磁盘件，而是对应分区。

## 2.Kvm虚拟机鉴定要点

KVM虚拟机配置文件是以扩展名为.xml的文件，默认情况下放在/etc/libvirt目录下，虚拟磁盘件、快照和内存等数据默认情况下在/var/lib/libvirt录。

可使命令“virshlist-all”命令对KVM虚拟机信息进查询，包括停运的虚拟机信息，磁盘文件默认情况下扩展名.qcow2,内存文件为.save，快照（实际仅快照虚拟机信息）.xml件。如果鉴定软件不能识别.qcow2格式件，又需要离线分析.qcow2件时，可利qemu-img具对虚拟硬盘进转换后再进分析。

KVM的虚拟机的志信息默认情况下在/var/log/libvirt/qemu录下以虚拟机客户机名称为件名的log件中。另外，virsh-manager运志在用户目录下的.cache录下，例如root 用户/root/.cache/virsh-manager目录下的virsh-manager.log。有关libvirtd 运行和qemu模拟器启动情况的有关信息可以通过syslog.log等系统志件进检索分析。对KVM虚拟机内部的分析，可先导出虚拟机客户机再进分析。

## 第三节 虚拟容器鉴定

## 一、虚拟容器鉴定难点与方法

## (一)虚拟容器鉴定难点

## 1.涉及分布式环境

容器技术与云计算密切相关，它是支撑云计算的核心技术之一。通过容器技术，能够方便地支持微服务架构的应用，实现快速部署，快速迭代。这种微服务架构本质上也是分布式架构，在该架构下每个业务模块都作为独项开发并将其称为个服务，微服务的拆分粒度更。在产环境中，分布式架构往往涉及多台物理位置不同的计算机来共同承载业务。这种分布式环境疑加了电数据鉴定的难度。

传统鉴定由于可以接触物理设备，因而可采取断网、查封扣押等措施，并通过制作位对位硬盘镜像和内存镜像进实验室分析。在分布式环境中，物理设备很难接触，容器状态也容易变化，通过关机式鉴定不仅不可，而且由于容器和组件之间不断相互通信、一旦服务停止或者虚拟网络、存储等服务出现故障，都会使鉴定变得艰难。很大程度上鉴定需要依赖云服务提供商的云基础设施环境。

## 2.架构复杂、实现技术众多

容器与容器编排相关技术和实现案众多，与容器技术相关概念和对象也常多。例如，在dockers中涉及镜像、容器、网络、存储卷等对象，在K8s涉及集群、节点、部署、复制集、pod、服务、存储卷、标签、注解等。有一些类似概念在不同技术实现中可能还存在差异。因此在鉴定中，如果不能对容器及相关技术的整体架构做全面的了解，在鉴定中可能没有清晰头绪，或者遗漏重要信息。

由于架构复杂、服务众多，集群的组件之间不断相互通信、在分析问题、追踪问题的根源方常困难，在鉴定前期有必要收集尽可能多的有关案件发时集群状态的信息。

## 3.对鉴定及时性要求高

容器及相关技术部署快速，但同时相关数据也容易被销毁，相较于传统鉴定，虚拟容器涉及的鉴定对及时性要求可能更。如果不能及时对案件现场采取必要措施，嫌疑通过简单的操作更容易销毁鉴定关键数据而难以被恢复或被发现。

## （二）虚拟容器鉴定的程序和方法

针对容器和集群的鉴定可按以下程序和法进：

## 1.了解虚拟容器技术有关架构、集群、节点和容器有关信息

在鉴定前，可根据案件相关情况了解待鉴定事项可能涉及的云计算技术和内容。通过委托提供的资料信息，可对被鉴定系统涉及的技术有个致的认识。

在远程鉴定时，首先应判断采用的技术、使用了何种架构，涉及的集群信息、集群的状态，以及集群有关的节点和容器信息。

## 2.根据不同场景，选择合适的数据提取固定方案，并对相关数据进一步进行分析

在了解虚拟容器技术有关架构后,根据不同架构和案件需求,对相应的件或虚拟存储介质进固定或分析。例如，是否需要对节点计算机或虚拟机制作镜像，是否要对容器进快照，有关配置件是否需要打包固定、持久性存储数据是否固定等。

## 二、常见虚拟容器鉴定

## (—)docker鉴定

## 1.docker体系结构

docker前采的是客户端/服务器架构，包括客户端和服务端两核组件,同时通过镜像仓库来存储镜像。客户端和服务器可运在同台设备上，也可通过socket或者RESTfulAPI来进通信。其基本架构如图11-15所。

![](images/1feb4d4e0f2f309113c7576a99e7ca03be983cc3e1b0a38a0b2bb6d6d4df3d6e.jpg)  
图11-15 docker的体系结构

## 2.docker容器鉴定常见方法

对docker容器鉴定也包括两种法，一种是容器运状态下的动态鉴定；一种是容器静状态下的离线鉴定。当在鉴定环境中进分析时，可结合静态和动态分析法进容器、镜像和存储的分析。

## 3.docker动态鉴定常用命令

docker客户端提供了一组管理命令，对某个资源进行集中管理，包括快照、配置、容器、镜像、络、节点、插件、服务、服务栈、集群、系统、密钥和挂载卷等。对docker进动态鉴定时，通常包括对系统信息、容器、镜像、存储、络等的鉴定。

（1）系统基本信息 对docker信息系统、docker中容器的状态、镜像历史、事件信息的分析是最常见的分析内容。与系统信息相关的命令如表115所。

表11-5 系统信息检查常见命令
<table><tr><td>类别</td><td>命 令</td><td>说明</td></tr><tr><td rowspan="5">系统信息</td><td>docker info</td><td>显示docker系统信息，包括docker客户端信息，服务端的版本、容器数 量与运行状态、镜像数据、存储驱动、日志格式等基本信息</td></tr><tr><td>docker version</td><td>显示docker版本信息，包括客户端docker引擎版本、服务端docker引 擎版本等信息</td></tr><tr><td>docker logs</td><td>获取特定容器的日志信息，其命令格式如下（其中CONTAINER指容器 名称或者容器ID，下同）： docker logs[OPTIONS]CONTAINER</td></tr><tr><td>docker history</td><td>显示特定镜像的历史，其命令格式如下（其中IMAGE指镜像名称或者</td></tr><tr><td></td><td>镜像ID，下同）： docker history [OPTIONS]IMAGE</td></tr><tr><td></td><td>docker events</td><td>获取来自服务器的实时事件</td></tr><tr><td></td><td>docker inspect</td><td>查看镜像、容器、网络、卷等docker对象的详细信息，其命令格式如下： docker inspect[OPTIONS]NAME|ID [NAMEIID..]</td></tr></table>

(2）容器信息检查不当对某个特定容器进检查时，需要分析容器的基本情况，必要时还要将容器中相关件导出分析,相关检查命令如表11–6所。

表11-6 docker容器信息检查相关命令
<table><tr><td>类别</td><td>命 令</td><td>说 明</td></tr><tr><td></td><td>docker ps</td><td>列出正在运行容器信息。如果加上-a选项则列出所有的容器，包括 已经停止运行的容器</td></tr><tr><td rowspan="7">容器信息类</td><td>docker inspect</td><td>检查特定容器信息</td></tr><tr><td>CONTAINER docker port</td><td>容器端口映射查看，其命令格式如下： docker port CONTAINER [PRIVATE_PORT[/PROTO]]</td></tr><tr><td>docker cp</td><td>容器和主机间进行文件或者目录复制。其格式如下：</td></tr><tr><td></td><td>docker cp[OPTIONSCONTAINER:SRC_PATH DEST_PATH或者 docker cp [OPTIONS]SRC_PATHI- CONTAINER: DEST_PATH</td></tr><tr><td>docker diff</td><td>检查容器文件系统目录和文件的变化</td></tr><tr><td>docker attach</td><td>docker diff CONTAINER 连接正在运行中的容器，其命令格式如下：</td></tr><tr><td>docker start/stop/</td><td>docker attach [OPTIONS]CONTAINER 启动、停止和重启一个或者多个容器，其命令格式如下：</td></tr><tr><td></td><td>restart docker export</td><td>docker start|stop|restart [OPTIONS]CONTAINER [CONTAINER...] 将一个容器的文件系统导出为一个tar归档文件，其命令格式如下： docker export [OPTIONS]CONTAINER</td></tr></table>

(3）镜像信息检查 在进鉴定分析时，有时需要对镜像进分析，对镜像件归档、对容器快照件系统进分析，有关命令如表117所。

表11-7 镜像信息检查有关命令
<table><tr><td>类别</td><td>命 令</td><td>说 明</td></tr><tr><td rowspan="5">镜像信息类</td><td>docker images</td><td>查看本地镜像，使用-a选项会列出本地所有镜像，含中间镜像层。命 令格式如下： docker images [OPTIONS][REPOSITORY[:TAG]]</td></tr><tr><td>docker inspect IMAGE</td><td>检查镜像的详细信息</td></tr><tr><td>docker save</td><td>docker save：将指定镜像保存成tar归档文件。 docker save [OPTIONS]IMAGE [IMAGE..]</td></tr><tr><td>docker load</td><td>-0：输出到的文件 dockerload：导入使用docker save命令导出的镜像</td></tr><tr><td>docker import</td><td>-i：指定导入的文件 docker import：从归档文件中创建镜像。 docker import [OPTIONS]file|URLI- [REPOSITORY[ :TAG]]</td></tr></table>

(4)存储类信息检查 当需要对存储卷信息进行检查时，可使用表11–8所示的命令。

表11-8存储卷信息检查有关命令
<table><tr><td>类别</td><td>命 令</td><td>说 明</td></tr><tr><td rowspan="3">存储信息类</td><td>docker volume ls</td><td>列出存储卷，命令格式如下： docker volume Is [ OPTIONS]</td></tr><tr><td>docker</td><td>检查一个或多个存储卷的详细信息，命令格式如下：</td></tr><tr><td>volumes inspect</td><td>docker volume inspect [OPTIONS] VOLUME [ VOLUME...]</td></tr></table>

(5)网络信息检查 网络信息检查相关命令见表11-9所示。

表11-9网络信息检查有关命令
<table><tr><td>类别</td><td>命 令</td><td>说 明</td></tr><tr><td>网络信息类 inpect</td><td>docker networks Is docker network</td><td>列出网络。格式：docker network Is[OPTIONS] 显示一个或多个网络的详细信息，格式如下：</td></tr></table>

（6）主机系统日志在对docker容器进行分析时，有时要检查主机有关日志，包括docker服务运行情况、docker服务产生的有关日志等。日志一般存储在/var/log目录下，可使用cat和jounalctl命令查看相关日志。

## 4.docker 主要配置文件分析

docker默认的存储位置为/var/lib/docker，主要包括containers、image、overlay2、volumes、network、swarm 等子目录。containers目录为存放容器信息的目录，在该目录下是以容器id为目录名称的子目录，存放各容器的信息。在每一个容器目录下，主要有hosts、hostname、config.v2.json、hostconfig.json、resolv.conf 文件和以.log扩展名结尾的日志文件。var/lib/docker目录下的 Image目录存放的是本地镜像信息。在 image/overlay2目录下有distribution、imagedb、layerdb三个目录和repositories.json文件。repositories.json 中存储了本地所有镜像列表信息。network目录存放的是网络信息，在files子目录下有local-kv.db文件，该文件用来存储一些网络配置信息。volumes目录存放的是卷数据信息。overlay2目录存放的是镜像管理数据，该目录名是以存储驱动命名的，不同存储驱动目录名不同。对其分析详见本节docker存储分析。swarm目录存放的是docker容器编排有关信息。详见本节docker swarm 集群分析。

(1)hostconfig.json 容器目录下hostconfig.json记录了容器端口映射、卷驱动等信息，它与config.v2.json两个文件是容器的主要配置文件。

(2) config.v2.json config.v2.json记录了容器的配置信息，如图11-16所示。

## 5.docker容器日志文件分析

docker容器的目录下有以log扩展名结尾的志文件，该文件是容器日志信息，可对其直接查看分析。

## 6.docker 存储分析

docker容器有两类存储机制，一种由存储驱动（StorageDriver）实现的联合文件系统（UnionFS），种是以外部挂载的卷（volume）和绑定挂载（bindingmount）等实现的持久存储。通常，存储驱动实现的是容器内部的存储，用于存储应用程序本身，而卷存储实现的是容器的外部存储，于持久化保存应程序产的数据。

![](images/6530479bd28a7181b3cd9c8540efcc4185dbfba459bf74eb388cd0e747202926.jpg)  
图11-16 config.v2.json

联合件系统可将多个录内容联合挂载到个根录，录的物理位置是分开的。因通过它可把只读的镜像层和可读写的容器层的件系统进合并。当对只读件系统进修改时,将修改保存在可写件系统当中，实现写复制功能。联合件系统的分层结构有利于镜像和容器的创建、共享和分发，实现多层数据的叠加，并对外提供统的视图，图11–17是docker分层。

![](images/874b4494ccb7ba038ff43320261a818d251d9d5af28d2f5b46c387fbcb38298c.jpg)  
图11-17 UnionFS分层存储示例

docker引擎可使联合件系统的多种变体，例如AUFS、OverlayFS、Btrfs、BFS和DeviceMapper等件系统。上述件系统都是存储驱动实现的，主要有aufs、overlay、overlay2、devicemapper、btrfs、zfs、vfs等。

在ubuntu、centos、debian和fedora等Linux系统中，前overlay2是docker选的存储驱动，以下仅以overlay2存储驱动为例，介绍docker存储有关的鉴定知识。

(1）overlay2结构 OverlayFS可在台Linux主机上将两个录分层,并将它们作为个单的录呈现。这些录被称为层，统呈现的过程被称为联合挂载(unionmount)。图11-18是docker官技术档展的docker镜像与容器如何分层以及如何与OverlayFS映射的。其中底层录称为lowerdir,即图中镜像层,层录称为upperdir,即图中容器,对外暴露的统视图录称为merged,即容器的挂载点。

![](images/ccabce62b857e44d74f5d6c00f73b022a901948569eaa767db64e5d3d41fe1dc.jpg)  
图11-18 docker结构与OverlayFS结构的映射

其中，镜像的顶层是overlay中的lowerdir,是只读的。容器的新录是upperdir,是可写的。当容器层要修改file2时，在容器层成可写的file2件,如果件没有改变，则不需要在容器层成对应件。在合并时，如果镜像层与容器层存在相同件时，则忽略镜像层件，最终对外形成统视图的“merged”层。

overlay存储驱动镜像层只能挂载层,要实现多层镜像,需要借助硬链接等形式实现共享，overlay2存储驱动本持多达128个OverlayFS层。在实现式上,overlay2通过每层增加lower件,通过该件记录所有底层的信息。图11-19是overlay2的录层次结构。

![](images/812c0fef185bd9f79d6063625c8abe9624d812d1b7c9971709c6dd81b53d3be8.jpg)  
图11-19 overlay2的录层次结构

上图是通过tree命令显示的/var/lib/docker/overlay2的录层次，在该录下是各层的目录和以写字母“1”命名的录，它包含符号链接，指向每层的diff录。在每层录下，分别包括diff、link、lower、work等录或件(其中有个录仅有diff,link,没有lower)。

每一层的diff目录包含了该层的实际内容；每一层都有一个link文件，其内容是链接，实际指向diff目录（记录1目录的链接)；除了最底层没有lower文件外，每一层都有一个lower文件，该文件包含了该层的更底层的软链接名称和顺序。而work是联合文件系统的内部工作文件。

如果创建了容器,则在overlay2录下多出了容器层,容器层的下级录较镜像层多个merged目录，该目录是overlay2存储驱动的直接挂载点，对容器的任何修改都会反映到该目录中。在静态分析时需要对此目录进关注。

查询容器运行时overlay2存储驱动的挂载，可使用“mountIgrep overlay2”命令进行。如图11-20所示。

![](images/d5ba9c30d29405fe1f07d3af81e34d47b9436b0cc9b5c6ed4312f65a3fe835c7.jpg)  
图11– 20 overlay2 存储驱动的挂载

（2）卷与绑定挂载的分析为了确保容器停止后文件持久化存储，常见的方案是通过卷和绑定挂载进行。卷本质上是docker主机上的文件和目录，可挂载到容器的文件系统。

通过卷可使得容器之间共享数据，当容器被删除时，卷依然存在，存储在卷中的任何数据都会保留。如果容器被停止使用或者被删除，而卷没有显式被删除，可通过调查卷的数据发现线索和信息。调查当前卷的情况可使用“docker volumes lIs”和“docker volumes inspect”。

设置容器的卷或绑定挂载时，通过使用-v或-mount,-v由三个字段组成，用冒号字符（：)隔开。在绑定挂载的情况下，第一个字段是主机上文件或目录的路径；第二个字段是在容器中被挂载的路径；第三个字段是可选的，是一个用逗号分隔的选项列表，如ro。而-mount则由逗号隔开的多个键值对组成，每个键值对由一个<key>=<value>元组组成。表11−10为mount常见选项。

表11- 10 mount常见选项
<table><tr><td>mount 选项</td><td>取值</td><td>含 义</td></tr><tr><td>Type键</td><td>volume bind tmpfs</td><td>卷使用volume 绑定挂载为bind tmpfs是临时挂载，是基于内存的文件系统，存储的是非持久或敏感信</td></tr><tr><td>Source键</td><td>可以空</td><td>息，是临时性的，也不能在容器之间共享 挂载的源。命名卷为卷名，匿名卷则省略</td></tr><tr><td>Desitination键</td><td></td><td>挂载的目的地</td></tr><tr><td>Readonly</td><td>可以无</td><td>ro为只读</td></tr></table>

（3）卷容器卷容器是一种特殊的容器，它通过挂载卷或者绑定挂载创建容器，专门供其他容器使用。其他容器在使用时通过-volumes-from选项就可使用该卷容器的挂载。在调

本书的版权及著作权等部归于出版社及作者查鉴定时，与容器调查鉴定方法类似。 仅供公众及法律从业者、学生等法学研究学习之用，请勿商用。

## 7. docker-compose

docker容器本占资源极少，般每个容器中只运个服务。当个项包含多个服务时，为每个服务单独构建镜像构建容器较为烦琐。通过docker-compose可同时部署多个服务，实现对docker容器集群的快速编排。docker-compose只需要在docker-compose.yml模板件,定义配置多个容器之间的关系,然后只需要个命令就能同时启动/关闭这些容器。

docker-compose是以项进管理的,它将项分解成不同的服务,这些服务最终通过容器实例的形式运。docker-py是调docker API的软件包,docker-compose通过它来实现与docker引擎的连接。整个体系结构如图11-21所。

![](images/6f4889b6d50f015360769e8ee33ceeee5984d87e916f101e4745bad07fe74e19.jpg)  
图11-21 docker-compose的体系结构

在对docker compose进鉴定时，需要对docker-compose的配置件（默认docker-compose.yml或docker-compose.yaml)进分析,若涉及使dockerfile定义应程序环境,也要相应地进分析。

dockercompose的主配置件采YAML格式,由很多节和键值对组成，默认的件名为docker-compose.yml,来定义整个应程序，包括版本（version）、服务（service）、络(networks）、卷(volumes)等。

标准compose包括version、services、networks和volumes四个环节。在services节下可定义若服务名，每个服务名下通常包括image、bulid、depends_on、networks、volumes等健，再往下层可定义选项，最后的层级是具体值。networks节定义络,并可由services节下的networks健引本节定义的络。volumes节定义卷，并可由services节下的volumes健引本节定义的命名卷。

与鉴定有定关系的键值信息如表11-11所。

表11-11 docker-compose配置件部分信息表
<table><tr><td>序号</td><td>节</td><td>键(key)</td><td>说 明</td></tr><tr><td rowspan="8"></td><td rowspan="8">services</td><td>image: build:</td><td>image字段指定容器启动使用的镜像 build用于定义构建镜像的配置，如果同时定义了image，则compose</td></tr><tr><td>context: dockerfile:</td><td>会构建镜像并将其名称命名为image字段定义的名称 context定义构建上下文路径、dockerfile制定Dockerfile,args定义</td></tr><tr><td>args: Buildno:</td><td>参数</td></tr><tr><td>depends_on</td><td>容器间依赖、启动先后顺序问题</td></tr><tr><td>network_mode</td><td>指定网络模式，常见的有bridge、host、none、service:、container:</td></tr><tr><td>networks</td><td>指定要加入的网络，引用networks节中定义的网络</td></tr><tr><td>volumes:</td><td>定义数据卷：例如以下指定的</td></tr><tr><td></td><td>volumes: -db_data:/var/lib/mysql</td></tr><tr><td rowspan="9">2</td><td rowspan="9">networks</td><td></td><td></td></tr><tr><td>driver</td><td>定义驱动</td></tr><tr><td>driver_opts ipam</td><td>以键值形式表示的选项列表 定义ⅡPAM 配置。以下是一个例子：</td></tr><tr><td></td><td>ipam:</td></tr><tr><td></td><td>driver:default config:</td></tr><tr><td></td><td>- subnet:172.28.0.0/16 gateway:172.28.5.254</td></tr><tr><td></td><td>上面例子driver自定义驱动,config分别定义了CIDR子网和网关</td></tr><tr><td></td><td>Volumes节中的条目可以为空，此时docker配置默认的驱动。也可 以通过driver、driver_opts字段进行配置</td></tr><tr><td>external</td><td>用于设置卷是否在compose外部创建。external为true则compose</td></tr><tr><td rowspan="2">3 volumes</td><td rowspan="2"></td><td>不会创建该卷。例如，下面实例表示data是已经存在的，compose</td></tr><tr><td>不会创建 volumes:</td></tr></table>

对docker-compose进动态分析时，常使的命令见表11-12所。

表11-12 镜像信息检查有关命令
<table><tr><td>类别</td><td>命 令</td><td>说 明</td></tr><tr><td>docker-</td><td>docker compose ls</td><td>查看当前运行的项目，-a选项则包括停止的项目，通过该命令可分析 项目名称、运行的状态，以及该项目对应的配置文件，命令格式如下： docker compose Is [OPTIONS]</td></tr><tr><td>compose</td><td>docker compose config</td><td>解析并显示当前项目的配置信息。格式如下： docker compose config [OPTIONS][SERVICE...]</td></tr><tr><td rowspan="3">docker- compose</td><td>docker compose ps</td><td>列出一个compose项目的容器，包括当前状态和暴露的端口。格式如下： docker compose ps[OPTIONS][SERVICE...]</td></tr><tr><td>docker compose images</td><td>列出所创建容器的镜像列表，格式如下： docker compose images [OPTIONS][SERVICE...]</td></tr><tr><td>docker compose logs</td><td>查看容器的输出日志，格式如下： docker compose logs [OPTIONS][SERVICE..]</td></tr></table>

## 8.docker集群

docker通过引swarm模式来实现集群管理。swarm是由多个引擎组成的个整体，swarm集群是由多台以swarm模式运的物理主机或虚拟机组成,它们在集群充当管理节点或者作节点。通过集群可使多节点协同作，实现可性、负载均衡和并处理。节点分为管理节点(manager)和作节点(worker)两类，前者于swarm集群的管理,dockerswarm命令都在管理节点执,后者负责在其上执管理节点下发的服务(service）。管理节点也可有多个，但只有个管理节点可成为leader,leader是通过raft协议实现。

对dockerswarm集群进鉴定时，需要先了解dockerswarm的状态，了解集群节点和服务等有关信息。通常在动态分析时，可采取以下命令查看信息，见表1113所。

表11-13dockerswarm集群调查常命令
<table><tr><td>序号</td><td>命 令</td><td>说 明</td></tr><tr><td>1</td><td>docker node ls</td><td>docker node ls:查看当前集群中的节点信息</td></tr><tr><td>2</td><td>docker service ls</td><td>docker service Is：查看当前集群中的服务信息</td></tr><tr><td>3</td><td></td><td>docker service inspect docker service inspect 服务名称：查看某个服务的详情</td></tr><tr><td>4</td><td>docker service ps</td><td>docker service ps服务名称：查看某个服务名称的容器信息。如果某个服 务有多个容器会有多条信息</td></tr><tr><td>5</td><td>docker service logs</td><td>docker service logs服务名称：查看某个服务的日志信息</td></tr><tr><td>6</td><td>docker stack config</td><td>查看 docker 集群最近的配置文件,格式如下： docker stack config [OPTIONS]</td></tr><tr><td>7</td><td>docker stack Is</td><td>查看编排服务</td></tr></table>

dockerswarm还可使yml配置件,使“docker stack”进部署。例如,“docker stackdeploy-cyml件编排服务名称”是指按照yml件的配置部署swarm栈。通过这种式进配置时，需要检查最近（严格来说应是案件发时)的次配置信息,提取yml件并对其分析。

## (二）K8s鉴定

## 1.Kubernetes体系架构

Kubernetes,简称K8s,是个由云原计算基（the CloudNative Computing Foundation，

CNCF)托管的、开源的容器编排引擎，用来对容器化应用进自动化部署、缩扩和管理。

Kubernetes使集群(Cluster)来运组成系统的各种作负载，当部署了个Kubernetes就得到了一个集群。一个Kubernetes 集群由一组称为“节点”（Node)的工作机器组成，在这些机器上可运行容器化应用程序。每个集群至少有一个工作节点（WorkerNode)。根据官方文档资料,Kubernetes集群的核心组件如图11-22所示。

![](images/11c4bc10736a84823a8f148b58f45a3f988a11b8a24555c8ec2094fa95b0305a.jpg)  
图11–22 Kubernetes 集群的核心组件

## (1)Kubernetes 组件

1）控制平面组件(controlplane components）控制平面组件对集群进行全局决策以及检测和响应集群事件，例如，调度、启动新pod 等。可在集群中的任何机器上运行，但通常所有控制平面组件都安装在单独的一台机器上，且不在该台机器上运用户容器。

a)Kube API 服务器(kube-apiserver) Kube API服务器是 Kubernetes 控制平面的前端，用来提供Kubernetes RESTAPI服务。是Kubernetes对所有资源进行增加、删除、修改、查询的唯一入口。kube-apiserver具有水平伸缩性，可通过部署更多的实例进行扩展。例如，可通过运行多个kube-apiserver实例，在这些实例之间平衡流量。

b）etcdKubernetes集群使etcd存储整个集群的状态。etcd是个致的分布式键值存储。

c)Kube 调度器(kube-scheduler) Kube调度器负责将 Pod 调度到节点中。调度决策需要考虑的因素包括个人和集体资源需求、软硬件与政策约束、亲和与反亲和性规范、数据定位、作负载间的扰和最后期限。

d）Kube控制器管理器(kube-controller-manager) Kube控制器管理器是各种控制器的集合，它们都被编译成一个二进制文件，在一个进程中运行。这些控制器的类型包括节点控制器(Node controller)、工作控制器（Job controller)、EndpointSlice 控制器（EndpointSlice controller)和 ServiceAccount 控制器(ServiceAccount controller)。

e)云控制器管理器(cloud-controller-manager）云控制器管理器是嵌入了云特有的控制逻辑，可把集群连接到云提供商的API。

2）节点组件（NodeComponents） 节点组件于维护运中的pod并为Kubernetes提供运行时环境。

a）kubelet负责Pod对应容器的创建、启动、停等任务。

b）kube-proxy kube-proxy是个络代理，在集群的每个节点上运，实现了Kubernetes服务概念的部分。kube-proxy维护节点上的络规则。这些络规则允许从集群内部或外部的络会话与户的Pod进络通信。kube-proxy使操作系统的数据包过滤层（如果有且可的）。否则,kube-proxy会转发流量。

c）容器运时（containerruntime） 容器运时是负责运容器的软件。Kubernetes持containerd、CRI-O,以及KubernetesCRI（容器运时接）的任何其他实现。

(2）kubernetes对象 kubernetes对象是kubernetes系统中的持久实体，可来表集群的状态。旦创建了对象,Kubernetes系统就会不断地作以确保这个对象存在。论是创建、修改还是删除对象都需要使KubernetesAPI,当使kubectl命令界时,CLI也会进必要的KubernetesAPI调。常见的kubernetes对象如表11-14所。

表11– 14 常见的 kubernetes 对象
<table><tr><td>类别</td><td>名称</td></tr><tr><td>资源对象</td><td>Pod、ReplicaSet、ReplicationController、Deployment、StatefulSet、DaemonSet、Job、CronJob、 HorizontalPodAutoscaling</td></tr><tr><td>配置对象</td><td>Node,Namespace,Service、Secret, ConfigMap、Ingress,Label,ThirdPartyResource、ServiceAccount</td></tr><tr><td>存储对象</td><td>Volume,Persistent Volume</td></tr><tr><td></td><td>策略对象SecurityContext、ResourceQuota、LimitRange</td></tr></table>

1）对象规范和状态(object spec and status）乎每个Kubernetes对象都包含对象规范(object spec)和对象状态(object status)这两个嵌套的对象字段来管理对象的配置。对象规范，描述的是对象的期望(desired)状态，在创建对象时进设置。对象状态，描述的是对象的当前状态，由Kubernetes系统及其组件来提供和更新。Kubernetes控制平持续地、主动地管理每个对象的实际状态以匹配所需状态。例如：在Kubernetes中,Deployment对象可表集群上运的个应程序。创建Deployment时，假设设置Deployment spec运三个副本（期望状态)。Kubernetes系统会读取部署规范并启动所需应程序的三个实例。当实例中任何个失败了(状态更改）,Kubernetes系统会通过更正来响应规范和状态之间的差异,在这种情况下便会启动个替换实例。

2）描述Kubernetes对象 当在Kubernetes中创建对象时,要提供描述期望状态的对象规范以及该对象有关的些基本信息（例如名称）。当KubernetesAPI创建对象（直接或通过kubectl)时，API请求必须将该信息作为JSON包含在请求正中。通常是以.yaml格式件提供，kubectl在发出API请求时会将它转换为JSON。 勿商用。

表11-15是一个示例.yaml文件（application/deployment.yaml），显示Kubernetes部署时对象的规范，有关规范更详尽和具体内容可查阅kubernetes规范件。

表11-15 yaml文件部署示例  
```yaml
apiVersion :apps/v1
kind: Deployment
metadata:
name: nginx-deployment
spec:
selector:
matchLabels:
app:nginx
replicas :2 # tells deployment to run 2 pods matching the template
template:
metadata:
labels:
app:nginx
spec:
containers:
-name:nginx
image:nginx:1.14.2
ports:
-containerPort:80
```

其中，apiVersion表Kubernetes API的版本,kind表创建对象的类型;metadata为元数据，例如name、UID、namespace等信息来唯标识对象;spec描述的是期望对象处于什么状态。当定义好规范后，可通过类似于“kubectlapply-fdeployment.yaml”的命令创建对象。

3）个主要kubernetes对象 Kubernetes资源和对象概念和术语较多,本书不赘述，相关术语请参阅Kubernetes的官站（https://kubernetes.io）。与鉴定相关度较的kubernetes对象主要有以下个：

a）node 安装节点组件负责维护运中的pod的主机或者虚拟机称为节点或者作节点。安装控制平组件专门负责调度的主机或虚拟机也称为主节点。

b）pod pod是kubernetes的最重要概念之,它是其作单元,包含个或者多个容器，pod中的所有容器都具有相同的IP地址和端空间，每个pod都有个唯的ID。

c）service 在pod被销毁和重建过程中，IP地址不总是稳定和可依赖的，这需要通过Service(服务)来解决。服务是逻辑上组pod,提供了种访问这些pod的策略,这些策略常被称为微服务，这组pod能够被service访问，通过服务较容易实现应用的服务发现和负载均衡。

d）volume 提供数据的持久化存储,跟pod有致的命周期。常见的数据卷类型有emptyDir、hostPathnfs、iscsi、secret等。

其中,emptDir是创建个空录挂载到容器中，pod删除后，录内数据也被删除,适于持久化的存储;hostPath则将节点上某已存在的录挂载到Pod中,Pod退出后节点上的数据保留;nfs、iscsi是使用对应协议的网络存储，属于持久化存储;secret来传递敏感信息，是基于内存的tmpfs。除此之外，还有awsElasticBlockStore、gccPersistentDisk、AzureFileVolume等众多的数据卷类型。

e）Namespace 命名空间，来实现虚拟化。

f) Replicaset在kubernetes 中， pod 可能随时发生故障，通过 Replicaset 实现 pod 失败后的重新生成。当pod调度到某个节点上运行时，保证其按指定的副本个数正常运行，当副本数不足时，则通过Replicaset创建；当超过指定的副本个数时，则终止某些pod。

g)Deployment管理pod或副本集。

h）DaemonSet管理长期运于后台的应用。

i）StatefulSet管理带有状态的应用，某些应用需要关心pod 的状态，一旦pod发生故障，kubernetes 会创建同一命名的pod，并挂载原来的存储，以便实现pod中应用继续进行。

## 2.kubernetes 鉴定基本思路

对kubernetes进行鉴定时，首先要对集群架构进行调查，根据集群对应的架构和服务情况、案件情况等信息确定要提取和固定数据的范围、位置、方法，例如，是否需要对所有节点进行全盘镜像，还是仅需要对主节点或者某个应用所产生的数据进行提取和固定。其次，根据案件的不同情况，对提取和固定的镜像、数据、日志、配置信息等进一步进静态和动态分析。当确定了集群的整体架构、服务和数据位置后相关鉴定的方法，与docker的鉴定并无太大的不同，以下仅就日志、配置、节点、pod的鉴定进行简要分析：

(1）日志和配置文件鉴定动态鉴定分析时，需要对 kubernetes的集群架构进行调查，可利用 kebectl 命令行工具进行分析，根据调查案件的需求dump 相关配置信息。通常 kubectl的格式：kubectl [command][TYPE][NAME][flags]。其中 comand是命令、TYPE 是资源类型，NAME是指资源名称，flags是标志。与鉴定紧密相关的命令见表11-16所示。

表11–16 kubectl 动态分析涉及的命令
<table><tr><td>序号</td><td>命 令</td><td>说 明</td></tr><tr><td></td><td>kubectl cluster-info</td><td>显示集群中控制平面和服务的端点信息。如果要dump信息到文件，可以使 用dump，格式如下： kubectl cluster-info dump --namespaces default , kube-system --output-directory =/ path/to/cluster-state 此条命令是指将指定的一组命名空间（default和kube-system命名空间）的 集群信息dump到/path/to/cluster-state目录（注：--namespaces指定命名空 间，此表其他命令此选项均相同，不一一说明)。 该命令还会转储集群中所有pod 的日志；这些日志根据命名空间和pod 名称</td></tr><tr><td>2</td><td>kubectl config</td><td>转储到不同的目录。 kubeconfig 有关的命令，格式是kubectl config SUBCOMMAND，与鉴定相关主 要有以下几个： (1）显示当前上下文 kubectl config current-context (2）列出kubeconfig中定义的所有集群 kubectl config get-clusters (3)列出kubeconfig中的所有上下文 kubectl config get-contexts (4)显示kubeconfig中定义的用户 kubectl config get-users</td></tr><tr><td>3</td><td>kubectl api-resources</td><td>列出kubectl支持的所有资源类型</td></tr><tr><td>4</td><td>kubectl get</td><td>显示一个或多个资源，资源类型包括nodes、services、pods、deployment 等被 kubectl 支持的任何资源，使用实例如下： （1）列出命名空间中的所有服务 kubectl get services （2）列出所有命名空间中的所有pods kubectl get pods -all-namespaces （3）列出当前命名空间中的所有pod,并提供更多详细信息 kubectl get pods -o wide (4)列出一个特定的部署 kubectl get deployment my-dep</td></tr><tr><td>5</td><td>kubectl describe</td><td>列出某个或某组资源的详细信息。其命令格式为： kubectl describe(-f FILENAME|TYPE [NAME_PREFIX |-l label|TYPE/ NAME) 例如： （1）列出所有pod详细信息 kubectl describe pods （2）列出所有node详细信息 kubectl describe nodes （3）列出所有名称空间pv详细信息</td></tr><tr><td>6</td><td>kubectl logs</td><td>kubectl describe pv --al-namespaces 显示POD 中容器的日志信息，格式如下： kubectl logs[-f][-p](POD |TYPE/NAME)[-c CONTAINER]</td></tr><tr><td>7</td><td>kubectl version</td><td>打印当前上下文的客户和服务器版本信息</td></tr><tr><td>8</td><td>kubectl cp</td><td>文件复制命令，格式为： kubectl cp&lt;file-spec-src&gt;&lt;file-spec-dest&gt; 例如： 将/tmp/foo从 pod复制到本地的/tmp/bar上</td></tr></table>

静态分析要根据所提取的镜像或所提取数据的范围和内容进分析，除了对动态分析导出的对象配置信息、持久化存储数据进分析外，还可重点关注系统中的相关配置件和志件，常见件有：与部署、服务、存储等对象有关的yml件、pod和容器运的志文件。 雅 ，请勿商用

(2）节点分析 了解集群架构基本信息后，可根据不同案件需要就重点关注的内容进分析,如持久化存储数据,并确定提取固定数据的范围，固定相关数据后便可按照传统鉴定方法进行进一步分析。如果要对节点计算机或虚拟机进更加完整的分析，则需要对节点计算机进镜像。鉴定人员通常面对的是云主机，此时可通过以下几种途径进鉴定：如果有管理云资源的户账号，则可利云服务提供商提供的功能进鉴定。例如，对阿云主机镜像可利其提供的快照功能进镜像;如果有云主机root户账号密码，也可直接进dd镜像，并利用ftp进行下载，但耗时较长。

通过云服务提供商提供的功能进节点镜像时，其格式可能是qcow2，为了能够使鉴定软件识别或者仿真分析，可通过qemu先转换成vmdk格式。如果需要仿真分析再进步根据虚拟仿真环境确定是否需要再进转换。将qcow2转换为vmdk虚拟磁盘的命令格式为："qemu-img convert -p -f qcow2 -O vmdk .\from.qcow2 .\to.vmdk"。其中qemu-img 是 qemu 的镜像格式转换具,from.qcow2是提取的qcow2镜像，to.vmdk是转换后的vmdk镜像。

(3）pod和容器鉴定 对pod和容器的鉴定类似于对docker容器的鉴定,尤其要注意对持久化存储所产的数据、secrets、configmap等进分析,但对于存储式的不同、部署的服务类型不同、案件性质不同，鉴定关注的内容均可能存在差异。

## 第四节 虚拟化技术在鉴定中的应用

作为项新兴技术,虚拟化技术在电数据鉴定中也有着重要作。利虚拟化技术可在仿真环境下分析电子数据证据;通过建虚拟化平台实验室还可改变传统单机系统分析中不易协同作、不灵活便的缺点,提鉴定团队的合作效率、增强安全可靠性、便于鉴定环境的扩展。本节仅就仿真应予以介绍。

## 一、计算机系统仿真

## (一)计算机系统仿真方法

## 1.利用磁盘镜像进行仿真的一般过程

在电数据司法鉴定中，当获取了涉案计算机的EO1镜像或DD镜像时，可通过专业的鉴定仿真软件进仿真，也可利用虚拟化软件手动进仿真。专业仿真软件，如弘连的眼仿真鉴定软件、美亚的电子数据仿真系统，一般都持各类磁盘物理镜像、分区物理镜像和虚拟机磁盘的仿真，且一般都加入了用户密码自动重置的功能，因而使用起来较为方便，但其底层也是利虚拟化技术。有时对些特殊镜像使专业鉴定仿真软件分析偶尔会出错法正常仿真，此时需要对鉴定镜像进分析并动仿真。由于专业鉴定仿真软件使较为简单，本部分仅就如何利通虚拟机软件进系统仿真予以介绍。动仿真计算机系统通常需要经过以下三个阶段：

（1）准备阶段 在准备阶段主要是通过对鉴定镜像的分析，确定镜像是否包含操作系统分区，是全盘镜像还是分区镜像，检材系统是哪一种操作系统等信息，同时对虚拟机仿真时采用哪一种虚拟硬盘类型作出选择。

(2)仿真系统创建和排错 当确定了镜像的操作系统类型，可利用虚拟机管理软件创建虚拟机，在创建过程中，要对操作系统、CPU、内存、网络等进行选择，同时还要选择硬盘接口类型、虚拟磁盘类型、对应文件或设备等。在仿真过程中，可能因为设置错误、配置错误而出现各种报错，此时还需要进一步排错。例如，虚拟机磁盘找不到错误、虚拟磁盘被

占错误等。

(3）系统户密码破解和绕过 启动操作系统后,到登录界时,通常需要输户名和密码才能进系统。如果不知道被鉴定计算机的户名和密码，还需要进步进破解或者绕过。

## 2.vmdk虚拟磁盘的结构

不同虚拟机持的虚拟磁盘件格式不同,常见的有vmdk、vhd、vhdx、ova、ovf、qcow2等。在进行系统仿真时，需要选择虚拟机支持的格式，vmdk是实务中较常使用的虚拟磁盘格式，下以vmdk虚拟磁盘格式为例进介绍。

（1）vmdk虚拟磁盘布局 vmdk虚拟磁盘可由单个件包含的存储构成，也可由多个较件的集合组成的存储构成。虚拟磁盘件所有磁盘空间可在虚拟磁盘创建时分配，也可动态按需分配，即只在需要时才增长空间以容纳新数据。

vmdk虚拟磁盘个本描述符(textdescriptor)描述了虚拟磁盘中的数据布局。这个描述符可作为个单独的件保存，也可作为部分嵌到虚拟磁盘数据件中。

在未对虚拟机进快照前，个虚拟磁盘只由基本磁盘(baselink)组成。如果对虚拟机进快照，虚拟磁盘则包括baselink和delta链接(deltalink）。delta链接记录了客户操作系统写磁盘的变化。多次拍摄快照可能有多个delta链接与个特定的baselink相关联，如图11-23所。

每个link都是由个或多个区块(extent)组成，个区块是指个物理存储区域,通常是个件，其结构如图11–24所。

![](images/939c4b44e5a3b7f0a84a71b3f75dd6a2021c381f3fe343654eb819d788e9a237.jpg)  
图11-23 虚拟磁盘组成实例

![](images/dc6fcb0e7d7da029e9ce2e3b20872d383510a4cd9371d71476a4b4188c39b056.jpg)  
图11-24 多个区块组成个link

(2）文本描述符 vmdk虚拟磁盘本描述符由三个部分组成（注：有的由四部分组成）：第一部分为描述符头（header），包括version、encoding、CID、isNativeSnapshot、createType等信息，其主要含义如表1117所。

表11-17 虚拟磁盘描述符头主要字段含义
<table><tr><td>序号</td><td>字段</td><td>主要含义</td></tr><tr><td>1</td><td>version</td><td>版本信息，默认1</td></tr><tr><td>2</td><td>CID</td><td>随机的 32 位数字，表示内容ID，用来标 识 link</td></tr><tr><td>3</td><td>parentCID</td><td>父link的CID值。每个link都有CID和 parentCID,parentCID用来标识其link。 如果是baselink,其父link是Oxffff</td></tr></table>

续表

<table><tr><td>序号</td><td>字段</td><td>主要含义</td><td>备注</td></tr><tr><td>4</td><td>createType</td><td>表示虚拟磁盘的类型，可以是下列类型 之一： •monolithicSparse ● vmfsSparse monolithicFlat • vmfs twoGbMaxExtentSparse twoGbMaxExtentFlat • fullDevice •vmfsRaw • partitionedDevice • vmfsRawDeviceMap</td><td>monolithic表示虚拟磁盘的数据存 储在一个单一文件中 Sparse表示存储为稀疏方式，即虚 拟磁盘为可增长磁盘 Flat表示虚拟磁盘为预分配磁盘 所需所有空间在被创建时就被分 配了 twoGbMaxExtent表示虚拟磁盘的数 据存储由多个小文件集合组成 vmfs表示ESX服务器虚拟磁盘 fullDevice、vmfsRaw和partitionedDevice 用于虚拟机直接使用物理磁盘</td></tr><tr><td>5</td><td></td><td>• vmfsPassthroughRawDeviceMap • streamOptimized</td><td>在计算机系统仿真鉴定时，主要涉 及monolithicFlat、fullDevice等类型</td></tr><tr><td>6</td><td>parentfileNamefint</td><td>父磁盘路径和文件名信息 编码。ESI虚拟机磁盘文件常见字段，</td><td></td></tr><tr><td>7</td><td>encoding isNativeSnapshot</td><td>用来指定编码，如CTF-8 是否本地快照。ESI虚拟机磁盘文件常</td><td></td></tr></table>

第部分是区块(extent)描述部分，由或多组成，每描述了个区块。从虚拟机的度来看，是从偏移量为0的位置开始将这些区块列举出来。每包括五个部分，分别描述了访问权限、扇区数、区块类型、件名、偏移量等信息。

访问权限，可取值为：RW、RDONLY或NOACCESS，分别表读写、只读或不可访问。

扇区数是指该区块的，每扇区数为512字节。

区块类型，可能值为：FLAT、SPARSE、ZERO、VMFS、VMFSSPARSE、VMFSRDM或VMFSRAW。其中物理磁盘、分区和包含FLAT的磁盘类型,都使FLAT。ZERO表字节内容都为0的扇区。

件名是区块相对于描述符位置的路径和件名称。如果虚拟磁盘描述符头是fullDevice、partitionedDevice等物理设备，则件名必须指向SCSI或IDE等设备。

以下是若区块描述信息的例,如图11-25所。

![](images/5c63e3671d7c6bffd26de0a937c18c9e560f664e67016cddecc3c1a19d58d9d8.jpg)  
图11-25 VMDK的区块描述实例

第三部分是改变追踪文件，对于version为1的vmdk，没有这一部分。在ESXi虚拟机中此部分来指定改变追踪件。该件保存从上次快照以来的虚拟机所发变化的数据块信息。其格式如下：

# Change Tracking File

changeTrackPath = "vm_name-ctk.vmdk"

最后一部分是磁盘数据库信息，存储了虚拟磁盘的其他信息。每一行是一个条目，每个条目格式如下：ddb.<NameOfEntry>="<value of entry>"。条目用来指定适配器类型、CHS 等信息。适配器类型可以是IDE、Buslogic、lsilogic、legacyESX等。下面是某个vmdk文件的磁盘数据库信息，如图11-26 所示。

![](images/217d045904719419092a53b7bbbaefb19e2e448120aba392d2978c538f683c2a.jpg)  
图11-26 VMDK 磁盘数据库信息

## 3.磁盘镜像转换虚拟磁盘的方法

(1)E01 镜像挂载为物理磁盘生成 vmdk 方法通常鉴定镜像为 E01 镜像或者 dd 镜像，可将镜像挂载后，通过指定挂载后的物理设备来创建虚拟机。挂载后可利用虚拟机的功能自动创建 vmdk文件，创建的vmdk文件描述符头的createType 为“fullDevice”，区块描述信息也指向该物理设备。

(2)E01 等镜像直接转换为虚拟磁盘的方法通过专业鉴定工具或者第三方工具，可直接或间接将 E01或dd镜像文件转换为vmdk 文件。例如，可通过Arsenal Image Mouter 将磁盘镜像挂载后、再利用其“save as a new image fle”功能转换为虚拟磁盘镜像。如果没有直接转换工具，可先使用FTK Imager等镜像工具将 E01镜像转换为dd镜像，再通过虚拟机提供的磁盘转换功能进行转换。

(3)dd 镜像间接转换为虚拟磁盘的方法如果鉴定镜像为dd 镜像文件，还可通过记事本构建一个vmdk的区块描述符文件，不需要磁盘数据转换，只要将区块信息指向dd 镜像的磁盘文件进行仿真。如果dd镜像文件不是完整的磁盘镜像，还可利用vmdk 磁盘的区块信息组合，组成一个新的磁盘进行仿真。

在手动构建vmdk文件时，在描述符头信息里将createType 指定为“monolithicFlat”，在第二部分区块描述信息里设置一行extent信息，将磁盘访问模式指定为RW，指定磁盘的总扇区数，指定磁盘对应的dd文件名称，注意dd文件应放在vmdk文件同目录下，指定读写的起始位置便可。表11–18是构建的 vmdk文件的实例。

```toml
# Disk DescriptorFile
version= 1
encoding= "GBK"
CID=ff87efc2
parentcdD=f
isNativeSnapshot ="no"
createType="monolithicFlat"
#Extent description
RW117231408FLAT"case2016.001"0
#The Disk Data Base
#DDB
ddb.adapterType = "lsilogic"
ddb.geometry.biosCylinders ="116301"
ddb.geometry.biosHeads = "16"
ddb.geometry.biosSectors = "63"
ddb.geometry.cylinders = "116301"
ddb.geometry.heads = "16"
ddb.geometry.sectors ="63"
ddb.longContentID="ba88af43b8a24e018e8df5b4ff87efc2"
ddb.uuid= "60 00 C2 9d 01 33 d1 a7-2f cb5c 01 08 d8 85 72"
ddb.virtualHWVersion="11"
```

## 4.基于vmware的计算机系统仿真实例

下以E01镜像进系统仿真为例，介绍完整的过程和注意事项：先，使ArsenalImageMounter挂载E01镜像。挂载后信息如图11-27所。

![](images/9c16b945a992d458b7c70065f03262e71b288c9ccf7f2166029f719408be66fd.jpg)  
图11-27 挂载后磁盘设备信息

E01镜像挂载完成后，接着创建虚拟机。通过“新建虚拟机向导”予以设置。第1步，选“定义”;第2步,虚拟机硬件兼容性,按默认设置;第3步,安装来源,选“稍后安装操作系统”;第4步,选择操作系统,选“Linux”“ubuntu”（这步操作系统信息，可通过分析镜像确定操作系统类型，选择错误一般情况下对仿真结果影响不大）；第5步，命名虚拟机，按需求填写名称和路径；第6步，处理器配置，根据情况填写，本例填写1个CPU,2个核心；第7步，虚拟机内存，根据情况填写，本例设置4G大小;第8步，网络类型，本例设置为NAT;第9步，I/0控制器类型，按默认LSILogical;第10步，磁盘类型，按默认SCSI;第11步,选择磁盘,选择“使物理磁盘”;第12步，选择物理磁盘，根据前述的挂载后磁盘设备信息为PhysicalDrive4,选择“PhysicalDrive4”。第13步,指定磁盘件,按默认,本例为“e01emulator.vmdk”;第14步，完成，如图11–28所。

![](images/78ba573a1ce5f48e27a50497ffcf8658e5f267f82fc007a00e7602f5b7db4e78.jpg)  
图11-28 完成状态虚拟机基本信息

完成虚拟机创建后，e0lemulator.vmdk件已经创建完成，启动虚拟机便可。其中e01emulator.vmdk件内容如图11-29所。

![](images/6e9689230444699baf73959d6611b7140cb0805874b99d980abc321bdbebaa64.jpg)  
图11-29 创建后VMDK件

启动虚拟机后，进系统登录界面，接下来需要对系统用户的令进重置才可登录，破解法见本节()的内容。

## （二）系统密码破解方法

在进系统仿真时，需要对操作系统户令进破解。如果仅为了仿真分析，则只需要通过安全模式或单户模式进密码重置便可。但如果希望通过分析户令规律进其他令的关联分析时，则需要对密码口令进暴力破解以便发现用户使用的真实令。

## 1.Windows系统密码破解方法

针对Windows系统开机时的密码，可通过重置、破解和绕过等法解决。在进仿真鉴定时，一般采用重置系统密码法较为简捷。

由于Windows户和密码存储在注册表SAM中，可进安全模式重置户密码（例如，通过命令“NETUSERadministrator123456”将administrator户密码重置为123456），还可通过替换方法将已知密码的加密信息替换SAM表中对应的加密密码，也可通过暴力破解方法分析出系统的户名和密码。下以第三具为例介绍重置密码法：

图11-30为通过启动光盘启动系统，利PCUnlocker具重置密码的例。

![](images/9f8b17ec9fd37bc4f3e0aa8cc84159ed7aeb5ca6b459c5aa61002e6a23b23693.jpg)  
图11-30 使用PCUnlocker重置Windows密码

除以上思路外，还可使SAMinside等软件暴破解密码。针对运中的Windows，可通过漏洞利技术绕过、重置和破解密码，但在仿真鉴定中般不采。

## 2.Linux系统密码破解法

(1)root 密码重置方法 Linux系统鉴定较常采用重置法修改root用户的密码。通过单户模式可直接修改Linux系统密码，需要注意的是当系统启selinux安全机制时，需要selinux放以使重置密码效。

下以centos为例，介绍密码重置法。在Linux启动时按e进启动菜单的编辑，在图11-31中Linux内核加载末尾修改和追加相应的命令和参数。具体如下：

![](images/be7cb08ea303fed88db556072b39f90ca4fbfedd022d1e69f562c5c0b86f444e.jpg)  
图11-31修改内核加载参数

第1步：进入救援或者单用户模式，使根目录可读写。方法1是在图中红色标记行末尾追加“rd.break”参数进救援模式后，使用“mount -o remount,rw/sysroot”修改/sysroot的挂载式为rw，使“chroot/sysroot”改变系统的参考根录位置;法2是在图中红标记末尾追加 $\mathrm { \dot { \bar { \iota } } i n i t { = } / b i n / s h } ^ { \prime \prime }$ 进单用户模式后，使用“mount-oremount,rw/”修改挂载方式为rw;方法3是在图中红标记末尾追加 $\mathrm { \ddot { \Delta } i n i t { = } / b i n / s h \vec { \Delta } ^ { \mathrm { \prime \prime } } }$ ,同时将该“ro”修改为“rw”进单用户模式。

第2步，使passwd命令修改root户的密码。

第3步，通过使用“touch/.autorelabel”来使SELinux放策略。

第4步,退出重启。执“exec/sbin/init”或输两次exit退出并动重启。

(2）root密码破解方法 除重置密码外，也可通过暴破解的法获得root户的密码。其思路是从etc/shadow文件找到加密的口令信息，利用hashcat等破解工具进行破解，但此法在仿真鉴定中效率相对较低，较少采。

## 3.macOS系统密码破解方法

采用重置密码方法进入MacOS系统较为方便，例如，准备Mac的安装光盘或者镜像，在VMware虚拟机中选择“打开电源时进固件”,选择从光盘引导系统，当进安装界面时，不点击“继续”，而是选择菜单“实用具”下的“终端”，进终端后，键“resetpassword”,将弹出修改密码界,再根据向导完成修改便可重置户密码。

## 二、移动终端仿真

## (一)移动终端仿真方法

在电子数据鉴定中，对移动终端仿真是指通过获取的证据镜像，对其进行仿真分析，避免直接操作移动设备引起设备状态的变化，可更加直观地分析电子数据。在实务中，较少采用此方法，因为一方面需要ROOT手机后才能获取完整镜像，另一方面大多数案件通过静态分析便可满足鉴定的需求。从理论上说，移动终端仿真与PC的仿真在程序和法上类似，但前虚拟化软件对安卓、苹果各类机持有限，直接对鉴定镜像进动态分析较为困难。但利机模拟器，仍可有限地对机系统中应进仿真分析。例如仅对机应用和重要数据有关的分区进提取，然后尝试重建对应机模拟器中磁盘分区表和替换data等相关分区数据实现动态分析，以使仿真环境所关应和数据接近原系统情况。

## （二）APP应用程序仿真方法

相较于移动终端仿真，对APP应用程序的动态分析更为常见。APP应用程序在PC上进行开发时，开发人员会使用模拟器来分析其开发的APP应用程序，以便了解上架前它是如何运的。对于鉴定人员来说，使用虚拟机运的模拟器进仿真分析，可了解APP应用程序的运行情况，是否存在恶意行为，还可对APP网络连接服务器情况进行检测。从理论上说，对APP应用仿真分为两种情形，一种情况是仅对APP应用程序进行仿真分析；另一种情况是对应用程序现有状态包括数据继续进分析。后种情况除提取应用程序外，还需要通过技术方法将应用程序数据进行提取和替换。采用后一种方法时，可以较直观的方法观看应用程序的数据呈现。除了在虚拟机中安装APP应用程序外，还需要删除APP应用下的数据，并替换为通过鉴定得到的data件夹下对应应的数据。

当需要对APP进功能动态分析时，需要搭建特定环境后再进仿真，前很多取证公司提供了商用软件可对APP直接进行仿真分析，这些工具能够大量减少分析的工作量。但也存在很多情况，可能还需要自已定制分析环境进分析。

在对APP应用仿真分析时，通常要定制日志的记录方式和数据包捕获方式。要定制日志记录，例如希望记录APP应用访问本地电话具体过程、发送短信、发送邮件的内容，或者监控API调的情况等，则需要先对定制模拟器系统镜像进替换。希望抓取APP应访问络的数据包，则需要搭建抓包的环境。定制系统前主要针对安卓系统，需对操作系统内核进改造，在鉴定领域目前尚处于理论研究阶段，但也有一些初步研究成果。

搭建网络抓包环境较为常见，本节仅对常见的抓包环境进简述。要进行抓包，首先要下载手机模拟器、下载数据包捕获工具；其次，对抓包工具和模拟器进行网络设置，如设置代理，使机的数据包均能被抓包工具捕获;再次，针对https流量无法解析情况，则应设置相应的证书等内容;最后，针对APP可能检测代理、root、虚拟机等环境而不能触发程序运或数据包发送的情况，进行相应的处理，以使关心的数据包能够被捕获。

本部分仅以fiddler数据包工具为例，简要介绍机APP分析的环境搭建过程：

手机模拟器和 fiddler安装，略。

Fiddler和模拟器代理的设置。在fiddler的tools菜单的“options”子菜单的“connections”选项卡中设置监听端（如7777），将“Allow remote computers to connect”勾选。在机模拟器中，选择连接的网络，设置代理服务器（假设fiddler所在主机 ip地址为192.168.1.6，可将ip地址和端口分别设置为192.168.1.6、7777)，如图11-32所示。

![](images/80420f43cc46f49880c3123628f431af230293ed4c078ac3d9190b85e33f2bb2.jpg)  
图11-32模拟器网络设置代理服务器

为了捕获分析https数据包，还应对tools菜单的“Options”菜单的“HTTPS”选项卡中“CaptureHTTPSCONNECTS”和“Decrypt HTTPStraffic”两个选项卡进勾选,如图11–33所。同时将证书导出到桌（ExportRootCertificate toDesktop）以便安装到机模拟器，并将该证书拖进机模拟器中进安装（注：如果模拟器不持证书导需要先转换，再安装为系统证书），如图11–34所示。

![](images/3a25cfeafb0205944d87ed118fb8b994c5e522db5443584168110d0dbaf747b6.jpg)  
图11-33 https 捕获设置

![](images/55cad82d275d3aff08f11e6cbee4e1c9a2d38762ad5f958ccd884cc11a80655b.jpg)  
图11-34 模拟器中安装证书

有些APP有防抓包的检测机制，则需要根据不同场景进环境搭建。有些APP使okhttp框架设置代理不系统代理，或者检测到代理设置后不触发数据包的发送,此时常见思路之一是不通过应用层设置代理，直接在络层设置端转发。例如，利ProxyDroid绕过APP代理检测，安装postern配置VPN代理等。

另种APP防抓包机制是SSL绑定（SSLPinning）和双向认证机制（two-waySSLauthentication),这种场景下通信使了专属证书,前者应程序会对证书特征进检测，不通过检测，应用程序不会将请求发送到服务器；后者客户端和服务器都使用证书认证。对于SSLPinning根据实现法不同，又分为三种情况，分别为证书绑定（CertificatePinning）、公钥绑定(PublicKeyPinning）和哈希绑定（HashPinning）。针对此种抓包限制，常见的应对法是通过逆向和hooking技术抓证书并将其安装于抓包具。例如,针对证书绑定检测可在Xposed框架下使JustTrustme具、通过Frida进objection绕过等进抓包。

除此之外，在逆向分析APP应用程序时，还需要对些防逆向的机制进绕过和规避，例如,root环境、虚拟机环境检测等。针对APP鉴定内容请参阅相关章节的论述。

## 第五节 小 结

本章主要介绍虚拟化技术，主要就Vmware、ESXi、VirtualBox、Hyper-V、ParallelsDesktop、Kvm、Xen等虚拟机中与鉴定有关的电数据有哪些、如何对其鉴定，以及docker、Kubernetes等容器有关技术如何进鉴定进了分析,同时对利虚拟化技术进操作系统和APP仿真的法也进了简要介绍。通过本章学习，希望读者能够了解虚拟机化技术的有关原理、常见虚拟机技术、docker和Kubernetes的基础架构等。

![](images/74bc78f4ab4d8638afa537a55c812cfab042d78d70c0ba0457e6a3cb828d09d6.jpg)

## · 思考题

1.虚拟机技术有哪些不同实现方法?

2.如何在系统中发现隐藏或被删除的虚拟机?

3.简述加密虚拟机破解的具体方法。

4.docker容器如何被发现和鉴定?

5.在Kubernetes 环境下，如何提取与案件相关的证据？

6.如何利用虚拟机软件进行系统仿真?

## 相关

（相关法条和概念待补充）
