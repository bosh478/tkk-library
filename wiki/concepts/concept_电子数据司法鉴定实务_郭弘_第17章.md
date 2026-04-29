---
title: 电子数据司法鉴定实务_郭弘_第17章_电子数据恢复
type: concept
created: 2026-04-29
updated: 2026-04-29
tags: [电子数据鉴定, 司法鉴定, 电子数据恢复]
sources: [["《电子数据司法鉴定实务》郭弘 科学出版社 2025年.md"]]
---

# 第十七章 电子数据恢复

## 第一节 概 述

## 一、数据恢复应用概述

在信息技术高速发展的今天，数据已经成为任何企业或个人的核心资产。但是，数据安全问题也日益突出，如何保证数据的安全性和完整性，成为各行业都需要面对的重要问题。在实际操作中，由于不可预知的因素，数据丢失的情况时有发生。因此，数据恢复技术的应用也变得越来越重要。

数据恢复技术在安全领域的不同层级和场景下具有不同的含义，常见应场景包括应急响应环节下基于灾备的数据恢复，以及数据丢失后基于存储介质的数据恢复。应急响应环节下的数据恢复,是指在络安全事件发后,通过切换主备系统或数据源等措施来保障业务的连续性，其对象是企业的数据资产。而数据丢失后基于存储介质的数据恢复，是指在数据存储介质面临损坏、误操作、病毒攻击等情况下，采用相对应的技术手段，重建或找回丢失的数据文件。

在司法鉴定实务活动中，面向存储介质的数据恢复是提取固定数据信息的基础，也是数据分析和功能检验的前置，次全的数据恢复可以从存储介质中提取到量的关联和碎信息，为后续的调查分析奠定基础。因此，面向存储介质的数据恢复在司法鉴定领域得到度重视,针对不同存储介质的发展变化,相应的理论体系、技术法和具软件等也在不断更新。本章节以存储介质的数据恢复为重点，分别讲述不同存储介质的软硬件特性、数据恢复的基础原理，以及不同层级下常用的数据恢复方法和工具软件。

## 二、数据存储和数据恢复原理概述

目前，在实际应用领域，数据存储的基础原理主要分为磁、光、电三大类，分别对应磁存储介质、光存储介质和电存储介质三种。其中，磁存储介质是将数字信号磁化后保存在磁性镀膜上，最早的磁带、软盘以及目前常见的机械硬盘均为此类存储介质。机械硬盘根据规格尺寸、接类型、盘转速等不同指标特性泛适于不同的应场景,在商业环境中具有极的适例。前机械硬盘的最单盘容量已超过20TB，且随着艺优化还在不断突破极限。光存储介质核心是利用激光照射介质，通过改变介质性状以实现数据存储，读取信息时则利用定向光束扫描存储介质表，通过检测激光反射量以转化有效信息。光盘是最常见的光存储介质，包括CD、DVD、蓝光等不同类型。相比磁存储介质，光存储介质成本较低，但单盘容量已达上限，主要适用在特定场景领域。电存储介质基于半导体技术，主要通过电子电路以二进制式储存数据信息，近年随着芯技术突破得到迅猛发展。常见的电存储介质包括闪存盘（又称优盘或U盘）、存储卡(SD、TF等）和固态硬盘（SSD)等，随着芯业快速发展，电存储介质成本不断降低，形态各异、接繁多，在个消费领域占飞速提升。

磁、光、电三类存储介质各自的特点突出，使用场景也有较大不同，但总体来说，磁存储介质技术更为成熟，安全性更高，多用来存储大型数据集和重要数据，电存储介质发展迅速，在数据交换和个消费市场有较占，光存储介质由于单盘容量限制等原因使用场景逐步缩小，目前多用于数据备份等用途。根据实际应用占比，本章节内容主要针对磁存储介质和电存储介质，包括机械硬盘、固态硬盘等。这两类存储介质对应产品的技术封装较完整，数据恢复的可操作性也比较。

在行业实践中，数据恢复所解决的问题一般分为物理故障和逻辑故障。物理故障是指存储介质本身发生硬件损坏，无法正常运转、识别或存取数据，比如电路故障、磁头和电机故障、盘划伤等。逻辑故障是指与件系统相关的数据丢失问题，比如分区调整、格式化、件删除等操作导致的件丢失。这两类故障是依据对应的技术处理层级不同进划分，但从存储介质产品技术封装与应用的角度，完整的数据存储实现要分为三个层级，分别为物理层、固件层和逻辑层。其中，物理层和固件层联系相对紧密，可以理解为固件层是逻辑层调用物理层所必需的驱动控制层。在实际应用中，存储介质受到外力影响产生损坏的情况下，物理层故障和固件层故障可能会伴生出现，相应的恢复过程也需要同步调试，这就对应了物理故障恢复。逻辑层相对独立，在底层数据可正常访问的前提下，主要研究数据管理算法，进而在数据丢失、损坏时，通过逆向定位进行数据重组，以实现数据信息的可读与复现，这对应了逻辑故障恢复。

为便于理解数据恢复的基础原理，先从数据应用的度来观察数据的存放管理和检索使用过程。数据信息本身是一种虚拟的数字信号，其存储必须依附于特定的物理介质。在物理层，虚拟的数据信息以电磁信号的性质依附于某一种物理介质，存储介质作为一个容器对这些电磁信号的表现介质进运管理，以保证数据信号的电磁转换和正常识别。固件层对物理层所有资源进行统一管理，形成标准接口为逻辑层的数据读写提供服务，以解决底层电磁信号同计算机层面的级制信号对照关系。逻辑层则在此基础上进数据空间的规划使，构建多样化的操作系统和件系统进数据管理。数据恢复技术就是以此为基础，通过逆向操作的式逐一理清各层级的运原理和标准定义，进在出现意外情况导致系统功能失效时，通过人工介来重建不同层级的预设功能，以实现数据重现的目的。

基于上述分析，数据恢复的本质，就是对不同原理的存储介质单元进行分层研究，理解其物理层、固件层和逻辑层的功能实现原理，结合逆向分析和比照验证等手段，在相应层级的功能失效或数据损坏的情况下，手动进行数据重建，挽救重要数据信息。目前，在物理层，数据恢复的基础研究内容包括机械原理、数字电路等，解决的主要问题有磁头损坏、电机故障、PCB板故障等；在固件层，则主要研究面向硬件的驱动程序，解决的主要问题有固件解析、回写和主控程序读写等，固件层的研究由于面临技术垄断、知识产权保护等原因，多以应用案的形式存在;在逻辑层，研究的内容更加多样化，包括操作系统、文件系统、应用系统等，且随着应用需求的变化在不断拓展,常见的逻辑层问题包括误删除、分区错误、误格式化、病毒破坏等种种原因。

## 三、数据恢复常见法和软硬件设备

数据恢复的重点是对不同介质、不同层级的识别与重建，本节基于业实践应，整理数据恢复领域常见的技术法和软硬件具。

在物理层，常见的故障类型可能包括电源组件故障、PCB板故障、磁头损坏、电机损坏、盘划伤等，其典型的数据恢复方法包括同等组件替换、特种清洁、开盘热交换等。上述恢复方法属于机械维修的范畴，对员动能力要求较，业中尚缺乏标准的维修具和操作流程。其中，在特种清洁方面，针对烧、水浸和粉尘等不同场景，根据附着物和介质类型不同，主流存储介质产厂商提出了若干清洁溶液配案，为推动相关问题解决奠定了基础。

在固件层，常见的故障类型包括物理故障引起的伴生问题，以及程序设计缺陷导致的逻辑锁死问题，典型的数据恢复方法包括固件程序的读写备份、模块替换和重置等。目前，对于固件程序的研究由于面临技术垄断、知识产权保护等原因，未形成通用解决方案，但是针对不同产家、不同类型、不同批次的存储介质，些安全商基于逆向等技术段提出了对应故障的解决案，其中数据恢复比较有代表性的软硬件具包括PC3000和MRT。

PC3000是由俄罗斯ACELaboratory实验室研究开发的软硬体综合工具，主要用来解决常见磁性存储介质（机械硬盘为主）的固件问题，其软件通过定期更新基本覆盖了全球所有生产供应商（希捷、西部数据、、三星等）的全批次硬盘型号。PC3000主要包括Express与Data Extractor两部分，Express为实体专板，需要接作站的PCI-Express扩展插槽作为前置输，专用板提供SATA、PATA、SAS等端口连接对应存储介质，同时，使用DataExtractor管理软件进固件层数据的读写操作。管理软件定期更新各厂家、批次硬盘的固件内核程序，并提供读写、备份、替换、重置等固件管理功能。

MRT是与PC3000功能类似的国产化数据恢复具，同样包含硬件和软件两部分，硬件部分的控制器使硬盘作在厂模式，开放全部操作权限，以访问其内部固件程序和微代码。固件程序的识别、读写、替换与重置方案由MRT独立维护，相比PC3000覆盖率尚有不，但基本实现了主知识产权。

在逻辑层，常见的故障类型包括误删除、分区错误、误格式化、病毒破坏等，典型的数据恢复方法包括基于文件系统的目录树重构、基于文件指纹特征的检索定位等。逻辑层数据恢复主要依托各类恢复软件，这些软件运在操作系统环境下，对磁盘的读取访问依赖于操作系统对磁盘的访问管理，因此，逻辑层数据恢复需要磁盘无物理层或固件层故障问题。目前，逻辑层的数据恢复工具软件较多，其原理主要是基于对不同操作系统、件系统的理解，设计对应的检索算法，通过对数据区的内容进全盘扫描来实现丢失文件的重现。根据设计思路不同，逻辑层数据恢复的代表性具软件为X-ways和R-Studio。

X-ways是一款面向底层数据的16进制编辑器，通用性很强，可将任意文件、数据区甚至磁盘空间视为读写对象，读取编辑对应的数据内容，本质上可类比为一款数据编辑器。为便于操作，软件窗界中主要以16进制数据和对应的编码字符来展示相关内容。X-ways的软件操作具有很的由度，对使者的能平和知识理解要求较，需要理解数据存储的基本原理，具有一定的技术门槛。软件的更新维护较好，新版本中陆续加入了对各类不同文件系统、不同件类型数据结构的辅助解析和数值填充，提供了模板功能进一步简化操作，持脚本和API，针对RAID重组等应场景还提供了针对性解决案。

R-Studio侧重提供应用层面的一体化解决案，支持FAT、NTFS、Ext等各类常见件系统、数据结构的智能解析，通过内置的恢复算法帮助用户挽救丢失文件。相比X-ways，R-Studio基本屏蔽了底层二进制数据内容的检索和修改，主要依托内置算法，通过全盘扫描的形式进数据重组，将恢复结果以件目录的形式提供直观可见的展示界面，具有度的易用性。软件通过定期更新，不断优化恢复算法在不同场景下的使用效果，目前已成为数据恢复行业内使用率较高的通用型软件。

除此之外，随着司法鉴定领域数据恢复需求的持续高涨，国内不少安全厂商针对司法鉴定领域的特殊需求或法律要求，推出了一些高集成工具，同样包含数据恢复功能，并在原始介质保护、数据镜像、关联分析等维度设计了更多易功能。其代表性具包括厦门市美亚柏科信息股份有限公司、上海弘连络科技有限公司、奇安信集团、杭州平航科技有限公司、苏州龙信信息科技有限公司、四川效率源信息安全技术股份有限公司等研发的计算机取证分析系统和机取证分析系统。

## 第二节 逻辑数据恢复

在实际应场景中，随着软件系统的复杂度不断提升，对应逻辑层的数据丢失问题也占据了整个数据恢复需求的半，其涉及操作系统、件系统、应系统等多个层级。逻辑数据恢复主要研究逻辑层相关内容，以物理层和固件层不存在任何问题、数据可正常读写为前提。本节针对逻辑数据恢复，分别从系统级、件级以及应级逐进讲述。

## 一、系统级数据恢复技术

系统级数据恢复主要研究不同操作系统及对应件系统的差异，通过正向梳理文件数据的存放管理策略，以便在系统失效时动进数据定位和重组。本节以常见件系统为分类基础，重点研究了Windows系统、iOS系统和Linux系统环境下的数据恢复技术方法，Android系统本质上是种类Linux系统,使了同样的件系统管理策略，在系统层不做单独区分。

此外，随着国内技术的不断进步和政策扶持,国产操作系统也被越来越多的企业和个所使用，目前常见的国产操作系统包括：中国操作系统（COS）、银河麒麟、统信操作系统、中标麒麟等。国产操作系统在设计理念、系统调接、内存管理式等与Linux存在定差异，但多基于Linux内核开发，相应的件管理策略和数据恢复原理同Linux本质差别。

本节以实际案例介绍的形式，分别对不同件系统下数据恢复的主要操作流程和工具软件使用技巧进行讲述。

## 案例一 NTFS件系统数据恢复

## 1.任务目标

在某U盘中存储了一些视频数据，因误操作导致其中部分文件被删除，需对删除文件进行恢复。

## 2.操作环境

操作系统：Windows 10;软件程序：X-ways、R-Studio。

## 3.操作流程

根据标准法中约定的检验规程,数据恢复操作的主要流程如下：

1）使用只读设备将检材U盘接入到检验工作站中，确保检验过程中不会受到任何写操作影响。 用，请勿商用。

2）对检材U盘进镜像操作，计算原始介质和镜像件的哈希值，保证其原始性。

进镜像操作时，确保原始介质通过只读设备连接到作站中，可使用X-ways的“Clone

Disk”功能对其进行镜像，如图17-1所示，完成后使用“Compute hash”功能对原始介质和镜像结果计算哈希值，比对一致后证明镜像完整，以保证其原始性。

![](images/326f838e04486449fc6ff3ff29a7871991a556dfdf5485bd332c67c7ae4bb4c8.jpg)  
图17–1X-ways 的"Clone Disk"功能

3）对镜像结果进行数据恢复操作，使用R-Studio打开镜像文件，可检验各个分区信息，包括文件系统、分区大小、起始位置等，当前介质只有一个分区，显示文件系统为NTFS。首先对该分区进行“扫描”操作，即对NTFS文件系统的底层数据结构进行全面扫描。

扫描完成后显示结果如图17-2所示，文件名前带有叉状的即为被删除的文件，选中需要恢复的数据文件，选择恢复功能，将目标文件恢复到另一介质中，注意不可将其恢复到原介质中，以免对其原始性造成破坏。

![](images/3d899ea1bb1d6e339ca40d41e31a74ee6108d879a879a07ca8a7da5c8e98bf26.jpg)  
图17-2结果显示

4）对恢复文件结果进行验证，确认可正常播放；数据恢复完成。

## 4.原理分析

上述使用R-studio进行“扫描”操作，是对NTFS的存储结构的扫描过程，包括MBR、启动扇区DBR、MFT、目录项等，然后通过指针位置分析其关联关系，对数据进行重组、恢复等操作。以图17-2中的“2.mp4”为例，分析其存储状态：

一般针对NTFS文件系统的数据恢复，其重点就在于MFT结构的解析，R-studio软件的扫描功能将这一过程大大简化了，基本屏蔽了底层数据。我们可使用X-Ways查看底层的数据情况，遍历当前分区的MFT，在“6291540”扇区处发现“2.mp4”的MFT文件记录，如图17-3所示，其删除标识显示为“0x0000”，即为被删除状态，文件簇指针显示为“0x321B699CB700”，结合DBR中记录的参数信息计算并跳转到该件的数据区“0x376032”处，如图17-4所，即为“2.mp4”的起始数据区。

<table><tr><td rowspan=1 colspan=7>扇区6291540</td><td rowspan=1 colspan=13>MFT标识删除标识</td></tr><tr><td rowspan=1 colspan=1>CO00A800:</td><td rowspan=1 colspan=2>4649</td><td rowspan=1 colspan=1>4C</td><td rowspan=1 colspan=1>45</td><td rowspan=1 colspan=2>30g</td><td rowspan=1 colspan=2>0300</td><td rowspan=1 colspan=2>-Co</td><td rowspan=1 colspan=1>11</td><td rowspan=1 colspan=1>CO</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=2>220</td><td rowspan=1 colspan=2>FILEO</td><td rowspan=1 colspan=1>??         □□O.EA.</td></tr><tr><td rowspan=1 colspan=1>CO00A810:</td><td rowspan=1 colspan=2>0200</td><td rowspan=1 colspan=1>01</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=2>380</td><td rowspan=1 colspan=2>0000</td><td rowspan=1 colspan=2>一50</td><td rowspan=1 colspan=1>01</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>04</td><td rowspan=1 colspan=1>0000</td><td rowspan=1 colspan=2>。</td><td rowspan=1 colspan=1>..8.0.E.</td></tr><tr><td rowspan=1 colspan=1>C000A820:</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=2>00</td><td rowspan=1 colspan=2>0000</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>03</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>2A</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=2></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>C000A830:</td><td rowspan=1 colspan=1>09</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=2>000</td><td rowspan=1 colspan=2>000</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>10</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>60</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>000</td><td rowspan=1 colspan=2></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>C000A840:</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=2>0000</td><td rowspan=1 colspan=2>000</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>48</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>18</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=3>.H..</td></tr><tr><td rowspan=1 colspan=1>C000A850:</td><td rowspan=1 colspan=2>ABFA</td><td rowspan=1 colspan=1>4A</td><td rowspan=1 colspan=1>6C</td><td rowspan=1 colspan=2>2669</td><td rowspan=1 colspan=2>D901</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>FO</td><td rowspan=1 colspan=1>9B</td><td rowspan=1 colspan=1>08</td><td rowspan=1 colspan=1>28</td><td rowspan=1 colspan=1>24</td><td rowspan=1 colspan=1>69</td><td rowspan=1 colspan=1>D901</td><td rowspan=1 colspan=2>.Jl&i</td><td rowspan=1 colspan=1>.J1&amp;1?0.($1?      □□□0□.□0</td></tr><tr><td rowspan=1 colspan=1>C000A860:</td><td rowspan=1 colspan=2>3BFE</td><td rowspan=1 colspan=1>83</td><td rowspan=1 colspan=1>4A</td><td rowspan=1 colspan=1>26</td><td rowspan=1 colspan=1>69</td><td rowspan=1 colspan=2>D901</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>AA</td><td rowspan=1 colspan=1>70</td><td rowspan=1 colspan=1>A6</td><td rowspan=1 colspan=1>79</td><td rowspan=1 colspan=1>26</td><td rowspan=1 colspan=1>69</td><td rowspan=1 colspan=1>D901</td><td rowspan=1 colspan=2>:.J&amp;1?0.s1?</td><td rowspan=1 colspan=1>:.J&amp;1?0.s1?       □□□O□_□O</td></tr><tr><td rowspan=1 colspan=1>CO00A870:</td><td rowspan=1 colspan=2>2000</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=2>0000</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>0000</td><td rowspan=1 colspan=2></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>C000A880:</td><td rowspan=1 colspan=2>00</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>09</td><td rowspan=1 colspan=1>01</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=2></td><td rowspan=1 colspan=1>...</td></tr><tr><td rowspan=1 colspan=1>C000A890:</td><td rowspan=1 colspan=2>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=2>-30</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>68</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0000</td><td rowspan=1 colspan=3>....0.h.</td></tr><tr><td rowspan=1 colspan=1>COO0A8AO:</td><td rowspan=1 colspan=2>0000</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>02</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=2>一4C</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>18</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>010</td><td rowspan=1 colspan=3>..L..</td></tr><tr><td rowspan=1 colspan=1>CO00A8B0:</td><td rowspan=1 colspan=2>050</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>05</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>AB</td><td rowspan=1 colspan=1>FA</td><td rowspan=1 colspan=1>4A</td><td rowspan=1 colspan=1>6C</td><td rowspan=1 colspan=1>26</td><td rowspan=1 colspan=1>69</td><td rowspan=1 colspan=1>D901</td><td rowspan=1 colspan=3>.Jl&amp;i?     ...□0□0</td></tr><tr><td rowspan=1 colspan=1>CO00A8CO:</td><td rowspan=1 colspan=2>ABFA</td><td rowspan=1 colspan=1>4A</td><td rowspan=1 colspan=1>6C</td><td rowspan=1 colspan=1>26</td><td rowspan=1 colspan=1>69</td><td rowspan=1 colspan=1>D9</td><td rowspan=1 colspan=1>01</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>AB</td><td rowspan=1 colspan=1>FA</td><td rowspan=1 colspan=1>4A</td><td rowspan=1 colspan=1>6C</td><td rowspan=1 colspan=1>26</td><td rowspan=1 colspan=1>69</td><td rowspan=1 colspan=1>D901</td><td rowspan=1 colspan=3>.J1&amp;1?.J1s1?      □□□□□□</td></tr><tr><td rowspan=1 colspan=1>C000A8D0:</td><td rowspan=1 colspan=2>ABFA</td><td rowspan=1 colspan=1>4A</td><td rowspan=1 colspan=1>6C</td><td rowspan=1 colspan=1>26</td><td rowspan=1 colspan=1>69</td><td rowspan=1 colspan=1>D9</td><td rowspan=1 colspan=1>01</td><td rowspan=1 colspan=1>一</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>B0</td><td rowspan=1 colspan=1>91</td><td rowspan=1 colspan=1>06</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>0000</td><td rowspan=1 colspan=3>.J1&amp;i?.□..         □□□0型；..</td></tr><tr><td rowspan=1 colspan=1>COOOA8EO:</td><td rowspan=1 colspan=2>002</td><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>000</td><td rowspan=2 colspan=3>2...m.p.4        .2.mp4..</td></tr><tr><td rowspan=1 colspan=1>C000A8F0:</td><td rowspan=1 colspan=2>0500</td><td rowspan=1 colspan=1>32</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>2E</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>6D</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>70</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>34</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0000</td></tr><tr><td rowspan=1 colspan=1>C000A900:</td><td rowspan=1 colspan=2>8000</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>48</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>01</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>010</td><td rowspan=1 colspan=3>·文件名H..</td></tr><tr><td rowspan=1 colspan=1>C000A910:</td><td rowspan=1 colspan=2>000</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>1A</td><td rowspan=1 colspan=1>69</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0000</td><td rowspan=1 colspan=3>..□...</td></tr><tr><td rowspan=1 colspan=1>C000A920:</td><td rowspan=1 colspan=2>402</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>B0</td><td rowspan=1 colspan=1>91</td><td rowspan=1 colspan=1>06</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=3>@</td></tr><tr><td rowspan=1 colspan=1>CO00A930:</td><td rowspan=1 colspan=2>30A.5</td><td rowspan=1 colspan=1>91</td><td rowspan=1 colspan=1>06</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>30</td><td rowspan=1 colspan=1>A5</td><td rowspan=1 colspan=1>91</td><td rowspan=1 colspan=1>06</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=3>0.</td></tr><tr><td rowspan=1 colspan=1>C000A940:</td><td rowspan=1 colspan=2>321B</td><td rowspan=1 colspan=1>69</td><td rowspan=1 colspan=1>9CB7</td><td rowspan=1 colspan=1>B7</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>FE</td><td rowspan=1 colspan=1>FF</td><td rowspan=1 colspan=1>FE</td><td rowspan=1 colspan=1>FE</td><td rowspan=1 colspan=1>82</td><td rowspan=1 colspan=1>79</td><td rowspan=1 colspan=1>4711</td><td rowspan=1 colspan=3>2.10</td></tr><tr><td rowspan=1 colspan=1>CO00A950:</td><td rowspan=1 colspan=2>0000</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>8</td><td rowspan=2 colspan=4>000000</td></tr><tr><td rowspan=1 colspan=1>C000A960:</td><td rowspan=1 colspan=2>802</td><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td></tr><tr><td rowspan=1 colspan=1>C000A970:</td><td rowspan=1 colspan=2>02</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=2>22</td><td rowspan=1 colspan=2>80</td><td rowspan=1 colspan=2>0-</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=4>20</td></tr><tr><td rowspan=1 colspan=1>C000A980:</td><td rowspan=1 colspan=2>000</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=2>00</td><td rowspan=1 colspan=2>00</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=2>00</td><td rowspan=2 colspan=2></td></tr><tr><td rowspan=1 colspan=1>CO00A990:</td><td rowspan=1 colspan=2>02</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=2>00</td><td rowspan=1 colspan=2>000</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=2>00</td></tr><tr><td rowspan=1 colspan=1>CO00A9AO:</td><td rowspan=1 colspan=2>02</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=2>000</td><td rowspan=1 colspan=2>000</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>2</td><td rowspan=3 colspan=4>0020000</td></tr><tr><td rowspan=1 colspan=1>COO0A9B0:</td><td rowspan=1 colspan=2>08</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=2>000</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>0</td></tr><tr><td rowspan=1 colspan=1>COO0A9CO:</td><td rowspan=1 colspan=2>000</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=2>0000</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1>0</td></tr><tr><td rowspan=1 colspan=1>COO0A9DO:</td><td rowspan=1 colspan=2>02</td><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=2>80</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>0</td><td rowspan=3 colspan=4>0000002</td></tr><tr><td rowspan=1 colspan=1>CO00A9E0:</td><td rowspan=1 colspan=2>000</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=2>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=2>0000</td></tr><tr><td rowspan=1 colspan=1>COO0A9F0:</td><td rowspan=1 colspan=2>0000</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=2>0000</td><td rowspan=1 colspan=2>0000</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>0</td></tr></table>

图17-3“6291540”扇区的MFT文件记录

![](images/f3654ece535ea13f16a3fe6fddb565087652044e215f164636643cab87c09079.jpg)  
图17-4“2.MP4”的起始数据区

经上述分析，“2.MP4”显示被删除，但文件簇指针完整，由此可见，NTFS文件系统下的文件删除操作，只是对文件记录的标识位进行了修改，进而依据元数据定义做不可视转化，但实际底层数据仍然存在，在未被覆盖的情况下通过遍历搜索很容易重建出来。

## 5.要点与难点

1）在进行数据恢复前，保证数据的原始性非常重要，一旦存在新文件写入，就可能会导致删除数据被覆盖，进而降低恢复成功率。

2）标准方法的选择与适用很重要，镜像操作和计算哈希值是必不可少的环节，这也是保证数据恢复结果有效性和合规性的前提。

3）恢复过程中，由于删除文件或碎片文件较多，可能会出现找不到目标文件的情况，可利用R-Studio提供的“查找/标记”功能，通过文件名、文件大小、文件类型、时间属性等信息进行交叉检索。实践中还可借助其他恢复软件做辅助检验，比如X-ways、UFS等，不同恢复软件的主要差异在于恢复算法的设计与实现。

4）验证恢复数据时，难免会出现件无法正常打开的情况。排除检验恢复过程的操作失误外，还可结合文件级数据恢复技术进行操作，详见下节内容。

## 案例二 exFAT件系统数据恢复

## 1.任务目标

在某U盘中存储着一些pdf类型件,删除并尝试恢复其中某件,检验其件系统变化。

## 2.操作环境

操作系统：Windows10;软件程序：X-ways、R-Studio。

## 3.操作流程

根据标准方法中约定的检验规程，数据恢复操作的主要流程如下：

1）使用只读设备将检材U盘接入到检验工作站中，确保检验过程中不会受到任何写入操作影响。

2）对检材U盘进镜像操作，计算原始介质和镜像文件的哈希值，保证其原始性。

进行镜像操作时，确保原始介质通过只读设备连接到工作站中，可使用X-ways的“CloneDisk”功能对其进镜像，完成后使“Computehash”功能对原始介质和镜像结果计算哈希值，比对一致后证明镜像完整，以保证其原始性。

3）对镜像结果进行数据恢复操作，使用R-Studio打开镜像，可检验各个分区信息，包括文件系统、分区大小、起始位置等，该介质只有一个分区，文件系统为exFAT。首先对该文件系统进行“扫描”操作。待扫描完成后打开结果，如图17-5所示，文件名前带有叉状的即为被删除的文件，选中需要恢复的数据文件(2.pdf)，选择恢复功能，将目标文件恢复到另一介质中，注意不可将其恢复到原介质中，以免对原介质的原始性造成破坏。

![](images/bef52627ec58817651f28677c2452d1587bb0790dd45f0ee6fbd305aeb619948.jpg)  
图17-5文件显示

4）对恢复结果进行验证，打开恢复出的“2.pdf”，提示文件已损坏，无法正常打开，进一步进后续分析。

## 4.原理分析

上述使用R-Studio进行“扫描”操作，是对exFAT的存储结构的扫描过程，包括MBR、启动扇区DBR、FAT表、FAT目录项等，并通过指针位置分析其关联关系，对数据进行重组、恢复。以图17-5中的“2.pdf”为例，分析其存储状态：

删除“2.pdf”前，该文件的FAT目录项结构如图17-6所示，其中该用户文件的目录项的三属性值为“0x85”、“OxC0”和“0xC1”，即用户文件的特征值，其属性值记录着该文件的文件名、文件大小、起始簇号等属性信息，根据这些指针通过FAT表链跳转到数据区获取数据。

![](images/fb3a8999aaea2e6b9f1cc972fd96b0c388c5a1e0524b522f3a6f9058f6f30b32.jpg)  
图17–6 删除“2.pdf"前 FAT目录项结构

将“2.pdf”文件删除后，该文件的FAT目录项结构如图17-7所示。可见，该用户文件的目录项的三属性值被修改，作为删除标记，其他属性值包括文件名、文件大小、起始簇号等均未发生改变。但通过指针跳转到该文件的文件簇链时，发现被清空。

![](images/2b798847f2317c6aa7431a93573b779680e5491d3574f45332f63b13e95eba41.jpg)  
图17–7 删除“2.pdf"后FAT目录项结构

基于上述分析，用户数据文件内容均存放在数据区，通过FAT表进行操作管理，当进行文件删除时，会更改文件目录项首字节的删除标记，即做删除标注，实际的数据内容仍暂存在磁盘的数据空间中，但对于FAT类文件系统，文件的删除标注会导致簇位图文件中簇链信息清零，虽然通过底层数据扫描可找到文件的起始簇号，但由于簇链被清空，如果该文件没有连续存储，也很难完整恢复所有数据，即出现上述文件损坏或无法打开的情况。

## 5.要点与难点

exFAT与NTFS文件系统在被删除文件的恢复方面存在较大差异，虽然两者均未把数据区对应内容重置，但exFAT的恢复成功率较低，尤其被删除文件没有连续存放时，会导致恢复出的件中包含很多无法正常打开的件。

## 案例三 Ext3文件系统数据恢复

## 1.任务要求

挂载在linux系统下的某硬盘中存储着一些数据，删除并尝试恢复其中某文件，检验其文件系统变化。

## 2.操作环境

操作系统：Windows 10;软件程序：X-ways、R-Studio。

## 3.操作流程

1）使用只读设备将检材硬盘接到检验工作站中，确保检验过程中不会受到任何写操作影响。

2）对检材硬盘进镜像操作，计算原始介质和镜像件的哈希值，保证其原始性。

进行镜像操作时，确保原始介质通过只读设备连接到工作站中，可使用X-Ways的“CloneDisk”功能对其进镜像,完成后使“Computehash”功能对原始介质和镜像结果计算哈希值，比对一致后证明镜像完整，以保证其原始性。

3）对镜像结果进行数据恢复操作，使用R-Studio打开镜像，可检验各个分区信息，包括文件系统、分区大小、起始位置等，该介质只有一个分区，文件系统为Ext3。首先对该文件系统进“扫描”操作。待扫描完成后打开结果，文件名前带有叉状的即为被删除的文件,选中需要恢复的数据文件(RedHat.gif),选择恢复功能,将目标文件恢复到另一介质中,注意不可将其恢复到原介质中，以免对原介质的原始性造成破坏。

4）对恢复结果进行验证，打开恢复的“RedHat.gif”，提示文件已损坏，无法正常打开，进一步进后续分析。

## 4.原理分析

R-Studio的“扫描”操作是对Ext3文件系统存储结构的扫描过程，包括超级块、块组描述符、目录项、inode等，通过指针位置分析其关联关系，可对数据文件进行重组、恢复。以“RedHat.gif”文件为例,分析其存储状态：

首先从超级块中获取当前件系统的重要参数，如块大小、每块组中包含的块数、每块组中包含的inode数以及inode大小等。然后从根目录(2号inode)开始，根据inode中记录的块指针逐层跳转到标件，记录标件的上级录的录项如图17-8所示，得知“RedHat.gif”文件的inode号。通过计算获取到该inode，包含了文件的块指针，最后通过块指针获取数据区内容，如图17-9所示。

![](images/e2e98460352ef9a1850e24199991890c1f29b09418c26321af05be00128d8f7c.jpg)  
图17-8目标文件的上级目录的目录项

![](images/3358f48879b26d632944b7a5956e59eb750a2de9e79b3e7e03721966093923d4.jpg)  
图17-9数据区内容

将“RedHat.gif”件被删除后，其录项所占的空间会被收回。收回的式是把“RedHat.$\mathrm { g i f } ^ { \prime \prime }$ 件录项的长度值添加到上个录项的报告长度中，这样系统就会忽略对“RedHat.$\mathrm { g i f } ^ { \prime \prime }$ 文件目录项的读取。从目录项中可知，“RedHat.gif”文件删除后其目录项中的inode号并没有改变，文件名也没有改变，所以还可根据这些信息定位到“RedHat.gif”文件的inode，如图17-10所示。

![](images/1f294c748cbbf09aa1b3db47bec26c58d098a188c77dd164664e8e74dd7fa82d.jpg)  
图17-10删除后的目录项

跳转到该inode,其“链接数”减1,如果链接数成为0,意味着必须回收该inode,文件大和件的块指针也全部清零，同时将件的删除时间记录下来，如图17–11所。

![](images/5b34ffad9f49c26462cf4c92c598b56d96259b2220b635df771d1fb8421dab5f.jpg)  
图17-11删除后的目录项

基于上述分析，当件被删除后，其录项中的件名和inode号还存在。通过这两个信息可找到文件的inode，发现inode中的文件大小和块指针都被清零，即使数据块不会清零，但要找到文件的存储位置非常困难。因此，Ext文件系统下文件删除后同样难以恢复，通常按照文件指纹特征进行恢复，但如果文件占用的块比较多，文件不连续存储的可能性也会增大，恢复成功率会进步降低。

## 5.要点与难点

Ext与FAT件系统在被删除件的恢复方面有些类似，两者的恢复成功率都较低，尤其当被删除件没有连续存储时，会导致恢复的件中含有许多无法正常打开的件。但是，Linux系统的版本众多，Android以及多数国产操作系统都是类Linux系统，在图形化界面下，删除件的命令及式也较为多样，部分情况下可完美恢复出被删除的数据件。同时，不同的数据恢复软件对Ext件系统的恢复效果也差异较，可尝试不同的恢复式。

## 二、件级数据恢复技术

文件级数据恢复是在系统级恢复基础上，重点研究不同文件类型的构造差异，提取文件头尾、元数据等指纹特征，以实现不依托文件系统在数据空间中的直接定位和重组。其中，根据操作流程和目标不同，还可细分为文件数据恢复和文件数据修复。文件数据恢复的目标是，在开放数据空间内，不依托文件系统定位，基于对文件指纹特征的识别，检索文件头尾以重新构造出原始件信息。件数据修复的标是，在件内部结构损坏或数据丢失等情况下，最大限度地提取可用数据信息。

## (一)文件数据恢复技术

根据上节对不同件系统的介绍，部分情况下，可能不支持通过重构目录项的法进件恢复，此外，由于格式化、重新分区等问题，也会导致文件的目录记录覆盖或丢失。在这类情

况下，一般可使用文件指纹定位的方法，不依托文件系统信息进行不同类型文件的重组恢复，也通常称之为基于文件指纹特征的恢复方法。

文件指纹特征的恢复方法，关键是提取整理不同类型数据文件的底层数据特征，包括数据头尾、文件结构等，提取其中的唯一性标识以识别此类型文件，在文件数据存放连续性较好的情况下，此类方法可恢复出大量可用文件。

对文件指纹特征的提取整理，可依靠X-ways等底层数据编辑器手动识别并建立特征库，也可依托一些第三方整理出的常见文件特征库，在R-Studio等通用恢复软件中，也会集成一些预设的文件特征库。本文仅列出一些常见文件类型的指纹特征，见表17-1，也可在实践中自行设计添加。

表17-1常见文件类型的指纹特征
<table><tr><td>文件类型</td><td>特征值</td><td>偏移字节数</td></tr><tr><td>JPG;jpeg ; jpe</td><td>\xFF+\xD8\xFF [ \xC4\xDB \xE0-\xE3\xE8\ xEB\xED\xEE\xFE]</td><td>0</td></tr><tr><td>png</td><td>\x89PNG\x0D\x0A\x1A\x0A</td><td>0</td></tr><tr><td>gif</td><td>GIF8[79]a</td><td>0</td></tr><tr><td>TIF ;if ; nef; er2;dng</td><td>(\x49\x49\x2A\x00)1（\x4D\x4D\x00\x2A)</td><td>0</td></tr><tr><td>pdf</td><td>%PDF\x2D1\x2E</td><td>0</td></tr><tr><td>mp4</td><td>ftypmp41</td><td>0</td></tr><tr><td>ole2; doc ; xls ; dot ;pt; xla; pa; ps; pot; msi ; sdw ;db;vsd;msg</td><td>；\xD0\xCF\x11\xE0\xA1\xB1\x1A\xE1</td><td>0</td></tr><tr><td>docx ; xlsx; pptx</td><td>_Types \]\.xml</td><td>38</td></tr></table>

## (二)文件数据修复技术

针对上一节提出的基于文件指纹特征的数据恢复方法，一般很容易识别出文件头，但由于数据非连续存放等原因，可能导致文件结束标识不清，文件重组后结构损坏等问题。因此，部分专业团队进一步研究了基于已知文件结构，如何对损坏文件进行修复，提取内容片段的技术方法，典型的应用场景主要包括文档类数据文件，比如office文档的修复。

常见的Office 文档包括 word(doc 和 docx）、excel(xls和xlsx)、powerpoint(ppt 和 pptx)等，其中doc、xls、ppt主要是Office2007之前产生的版本格式，这种文档格式是OLESS（OLEStructured Storage），微软采用的是OLE1.0文档规范。使用微软提供的OffVis工具可打开文档并查看OLESS文档结构，主要包含四部分，如图17-12所示。

![](images/a6ee13abf608caf08c6d2f1b9a6548cf403c222f0a6b8fa51b1f17d8b07fa9d7.jpg)  
图17-12 OLESS文档结构

Office2007及之后的版本在原有Office文件格式的基础上加入了XML文件格式，这种新的文件格式称为OOXML(Ofice Open XML)，是一种基于zip+xml 定义的文件存储格式，可使用任何常见的解压软件解压后进行分析，如图17–13所示。

![](images/0e70f2c020f729e3a39ec55fb219f26af18178f59f964889eabff3e3fd0f2d3b.jpg)  
图17-13解压软件解压后文档结构

以docx文件格式为例，解析流程为：读取[Content_Types].xml文件，获得所有文件的类型;读取_rels\.rels 对应的 Relationship文件，获取 document.xml 文件的位置，即 word\document.xml;读取 word \document. xml 文件以及其关联的 Relationship 文件 word\_rels\document. xml.rels，获取该Word 所有文件内容的存储位置，如 word 中插图所在文件夹为word\media。

基于上述分析，了解某一类特定文件的标准结构后，针对恢复出的文件无法正常打开时，可通过结构定义手动提取文件内容，比如典型的OfficeRecovery软件，主要功能为从损坏的Word、Excel、Powerpoint文档中挽救可用数据。

## （三）案例介绍

## 1.任务要求

恢复某硬盘中的文档、图片类数据文件。

## 2.操作环境

操作系统：Windows 10;软件程序：X-ways、R-Studio。

## 3.操作流程

根据标准方法中约定的检验规程，数据恢复操作的主要流程如下：

1）使用只读设备将检材硬盘接入到检验工作站中，确保检验过程中不会受到任何写操作影响。

2）对检材硬盘进镜像操作，计算原始介质和镜像件的哈希值，保证其原始性。

进行镜像操作时，确保原始介质通过只读设备连接到工作站中，可使用X-Ways的“CloneDisk”功能对其进镜像，完成后使“Computehash”功能对原始介质和镜像结果计算哈希值，比对一致后证明镜像完整，以保证其原始性。

3）对镜像结果进行数据恢复操作，根据文件指纹特征，使用X-ways进行检索恢复，打开“Tools"→“Disk Tools"→“File Recovery By Type"进入功能界面,勾选需要检索的文件类型，如常见的Pictures和Documents 类型文件，也可根据需要自定义配置文件特征，如图17– 14所示。选择输出文件夹后点击确认，等待恢复完成即可。同样注意不可将其恢复到原始介质中。

4）对恢复结果进验证，通过文件指纹特征进数据恢复，其恢复效果同文件连续性、文件类型以及文件大小有密切联系，若文件不连续性、文件较大则恢复效果不好，同时，文档图片类恢复效果相对较好，视频类件普遍较差。

## 4.原理分析

文件指纹特征的恢复方法，即全盘逐扇区扫描，匹配各类型文件的特征值，如JPG图文件底层以“0xFFD8”开头，如图17-15所示；pdf是以“%PDF”开头，如图17-16所示;office文档类是在38字节偏移处以“_Types\]\.xml”为特征值，如图17-17 所示。再结合各类型文件的属性信息判断件，或者尝试默认以另存该件内容。

![](images/57a65e2326fb93aeb04ca85d75fb23180d6cb2f4427258d5e72f42c02e26f272.jpg)  
图17-14X-ways功能界面

![](images/2b63af954fdaf8903807976a2ce6ab6855dd8c6df0a80fd2306d1d4361c1f151.jpg)  
图17-15JPG图特征值

![](images/ce6362cbc3697328561b3f8b13f6e96317dba76340a8855ebb9e58e10493e42e.jpg)  
图17-16 pdf文档特征值

![](images/fb093a0d781d90e60d569f34fe78f6900f014e3280412519c4553804c91dc74a.jpg)  
图17-17 office文档类特征值

## 5.要点与难点

1）件指纹特征的恢复法通常在件系统录结构不完整、恢复效果较差或覆盖较严重的情况下使用，其恢复效果因个体因素差异较大，数据完整性及正确性得不到保证，通常作为最后的恢复方法。

2）该法适于含有特征值的类型件，当某些特殊件不在软件默认的特征值列表中时，需自定义其特征值，但如果目标类型文件没有明显的特征值或者被加密时，此方法也难以发挥作用。

## 三、服务器数据重组

信息化的快速发展也催了数据量级的急速飞升,对应的数据存储和管理式也经过多轮技术迭代，从最初的存储设备直连逐步发展为相对独的磁盘阵列，并进步演化为络挂载的磁盘阵列，典型的应用方案包括NAS、SAN等。与此同时，分布式存储技术也在飞速演化，出现了GFS、TFS、HDFS、MooseFs等一系列面向应用的文件管理系统，对应的数据恢复解决方案也开始出现分层，分为面向上层文件管理系统的恢复和面向介质的数据阵列重组分析。由于上层件系统在设计之初既考虑到了数据的冗余备份和安全管理,相应的数据恢复需求可能会以灾备恢复的形式来实现，因此，在实践中，面向服务器层面的数据恢复，仍然以数据阵列的重组分析为主，大多是由于存储阵列本身出现问题，可能存在磁盘介质的故障或阵列算法的异常。因此，本节将介绍磁盘存储阵列的基础知识和恢复原理，并针对服务器恢复中常见的数据库问题进阐述。

## (一)基础知识

服务器的存储阵列在应中主要体现为RAID，是种由多个存储设备组成的、能够协同工作的存储设备，根据组合模式和调度算法不同，可充分发挥出多个存储设备的优势，包括提升存储速度，增大存储容量，以及利用冗余校验进数据容错和灾难恢复。具体来说，常见RAID的组合形式包括RAIDO,RAID1,RAID5等，不同级别对应的存储性能、数据安全和存储成本有较差异，梳理对照见表17–2。

表17-2不同级别对应的存储性能、数据安全和存储成本情况
<table><tr><td>RAID类别</td><td>采用技术</td><td>容错能力</td><td>特点</td></tr><tr><td>RAID 0</td><td>术</td><td>数据条带化技无容错能力，若1个硬盘损坏，所有的数据都无法可以并行读写， 使用</td><td>读写速度最快</td></tr><tr><td>RAID 1</td><td>数据镜像技术</td><td>RAID组中有一个是工作盘，其余为镜像盘，容错能力 最高</td><td>容量利用率低</td></tr><tr><td>RAID5</td><td>奇偶校验技术</td><td>数据分块存储在多个磁盘上，并通过奇偶校验码来实 现容错能力。RAID5至少需要三个磁盘，但是它可以 在一定程度上提高性能，并且容错能力也比较强</td><td>常应用于写操作 较多的场合</td></tr></table>

具体来说，服务器中组建RAID存储阵列通常采用两种方法，一种是利用硬件卡，通过专用控制器完成，即常见的RAID卡；另一种是软实现，需要在系统中通过软件算法来组建RAID。由于软实现的稳定性不如硬件卡，前应用中服务器的RAID组建多使RAID卡。此外，RAID技术创立之初主要服务于高端服务器，多与当时的SCSI硬盘配合使用，近年来，随着技术的发展成熟和产品成本不断下降，RAID卡也开始持IDE和SATA接硬盘，使得服务器整体存储性能得到大幅提升。

RAID的基本原理是数据分块存放，将连续的数据文件分成若干块，每个块分别存储在不同磁盘上，通过算法进行统筹管理。不同RAID级别对数据分配的方式有所不同，RAID0使条带化(striping)式,将数据平均分块后顺序存放在不同的磁盘上,RAID1使镜像技术将数据同时写两块磁盘中，RAID5和RAID6使用分布式奇偶校验技术，将数据和校验信息分别存储在多个磁盘中。

除了RAIDO，其他RAID级别均具备了一定容错能，但容错方法有所不同，最常见的是使用奇偶校验技术。当一个磁盘出现故障时，RAID可以使用校验信息来恢复数据。不同的RAID级别对容错能的要求也有所不同。RAID1通过镜像技术提供容错能，当个磁盘出现故障时，数据仍然可从另个磁盘中直接提取。RAID5和RAID6使分布式奇偶校验技术，可在个或多个磁盘出现故障时进逆向恢复。

对应下列各级别RAID的图形组合式，如图17-18所。

![](images/9ea8dcc3e2c6e1d67336b630984e3453e14043cb2481517ac559c71dd1660597.jpg)  
图17-18各级别RAID的图形组合方式

## （二）服务器恢复技术

根据上述分析，当RAID阵列中单盘损坏超过上限，或者算法管理存在异常时，可能会出现数据丢失的情况。此时，直接挂载任何一块单盘均无法正常识别内部信息，甚至无法判断阵列存储空间中采的哪种件系统。因此，针对RAID阵列数据恢复，先需要确定原始排列式并进虚拟重组，以识别出原始件系统,进基于原始件系统的相关特征,在磁盘空间中进检索定位，通过计算拼接规律来进数据重组。

具体来说，RAID阵列的数据恢复先需确定原始阵列信息和磁盘排列顺序，这个可通过检验服务器的相关配置和标识信息进行确定。在确定组成方式后，可借助各类恢复软件进行软重组，比如X-ways、R-Studio、UFSExplorer等，大多提供了自动分析和适配重组功能，但是由于阵列存储的参数众多，许多时候仍然需要人工干预。

第一次软重组后，首要目标是提取RAID阵列的关键信息，比如类型、条带大小、盘序和校验方向，以及同步异步设定等。基于上述信息，需要进一步确定重组空间中使用的文件系统，依据文件系统中拥有顺序编号或存储规律的单元信息，在不同硬盘中检验跳转规律，计算对应的重组算法。如NTFS中的MFT编号、EXT4中的块组描述符等，通过观察上述信息在不同硬盘中的分布和跳转规律，可计算出对应的拼接算法。

当上述参数和拼接规律计算完成后，可进第二次软重组，优化相关参数设置，并利用检验盘进数据替代，可借助第三方软件，也可通过自主程序开发做针对性的拼接与提取。

## （三）数据库修复技术

前两节内容主要介绍了服务器阵列存储的系统级和件级数据恢复，大多数应用场景下，服务器中最核心的数据会以数据库的形式进存放管理。数据库件恢复有其特殊性，一般单件较,内部结构复杂,完整恢复的概率不，挂载中也可能出现各类问题。前主流数据库主要有Access、MySQL、SQL Server、Oracle等。

Access数据库是MicrosoftOffice软件套装中的一个组件，它可使用户轻松地访问各种数据库中的数据，包括桌面应用程序、网络应用程序和在线数据服务。MySQL是一个关系型数据库管理系统，由于其轻量化的特点，是前最常见的关系型数据库管理系统之。SQLServer是Microsoft公司推出的关系型数据库管理系统，具有兼容性好、伸缩性强、与相关软件集成程度等优点，持多数应系统平台。Oracle是甲骨公司推出的关系数据库管理系统，多用于吞吐、并发等商用场景中。

在使用数据库期间会出现各类问题，包括误删除、无法加载数据库、加载中可能出现的各类错误提示，以及在对存储介质进恢复后，因为恢复效果不好导致的数据库问题等。针对数据库损坏的问题可以采取①数据库校验技术：检测数据库中的数据是否存在错误或损坏，如果检测到错误或损坏，可根据校验的纠偏算法修复；②数据库日志技术：可记录所有的数据库操作，当发生损坏时，可通过回放日志来还原数据；③数据库结构修复技术：可根据数据库的存储结构，跳过应用层面的错误，直接读取数据内容，重构数据库以达到修复数据的效果。本节将以MySQL、SQLServer为例，对数据库修复技术进阐述。

## （四）案例介绍

## 案例一 阵列重组数据恢复

## 1.任务要求

某磁盘阵列因为硬盘掉线等原因，无法正常读取其中数据，需要进行数据恢复。初步确定该阵列由6块硬盘组成。

## 2.操作环境

操作系统：Windows 10;软件程序：X-ways、R-Studio。

## 3.操作流程

根据标准法中约定的检验规程，数据恢复操作的主要流程如下：

1）使用只读设备将检材硬盘接入检验工作站，制作对应的镜像文件，并计算哈希值，保证原始性。

## 2）对磁盘镜像进数据重组和恢复

a）通过寻找MBR、DBR或者存储结构特征值确定件系统类型：在0号盘扇区发现MBR，其标识位表示其分区类型为NTFS；

b）利NTFS件系统中的MFT属性值分析RAID组建信息，如类型、条带、盘序和校验方向，以及同步异步设定等；

c）使用R-studio的“创建虚拟RAID”功能，如图17-19所示，将上述分析计算出的参数输到设置项中后，点击“立即应用”，便会在左侧界面中显示重组结果；

d）经过纠偏后,将数据保存到另块介质中完成恢复作。

![](images/5f67b7d99e05f9ad06292b03caf18f17de48a06a1a16394a1095d4ebc104962b.jpg)  
图17-19 对磁盘镜像进数据重组和恢复

## 4.原理分析

上述恢复过程中，最重要的步骤是利MFT来计算RAID中的各种参数配置。MFT中包含许多件记录，其特征值为扇区开头的“FILE”标识，在件记录的多种属性值中，“序列号”属性是计算RAID信息的关键因素，该属性值以升序的式记录,即每建个新件记录，其“序列号”属性便会加1,如图17-20所。

![](images/27efd6a4738a209179d79afd565bec6bc9ae014e6ca16b7badf09b405669a364.jpg)  
图17-20 RAID信息的关键因素

据此,定位到每块硬盘相同扇区位置的MFT,分析他们之间“序列号”的变化规律,再结合RAID各种类型的排列组合式，匹配出正确的参数设置即可。

## 5.要点与难点

1）上述案例中可以通过分析MFT的“序列号”属性计算RAID参数，但是在某些版本的NTFS中MFT并不记录“序列号”，还需要利其他法，这需要对件系统的存储结构、参数定义常熟悉，并善于寻找规律。由此延伸,FAT、HFS+、EXT以及常规的件系统中都需要沿类似法计算RAID参数以恢复数据。

2）设置完成RAID参数后，验证数据有时会效果不佳，甚软件会报错。类似情况发时，先要核验参数是否计算正确，也要考虑硬盘中数据不完整或者不同步的情况，重点是得利RAID的校验功能,当某块或某块硬盘中的数据镜像不完整，或者硬盘出现问题后未及时更换导致数据不同步等情况,都需要使校验数据替换，具体替换规则根据RAID类型不同不同。

## 案例二 MySQL数据恢复

## 1.任务要求

在使MySQL时因为误操作删除或修改了某数据,现需恢复其中的数据。

## 2.操作环境

操作系统：Windows10;软件程序： $\textstyle \mathrm { M y S Q L }$ O

## 3.操作流程

根据标准法中约定的检验规程,数据恢复操作的主要流程如下：

1）使只读设备将检材硬盘接检验作站，制作对应的镜像件，并计算哈希值。

2）定位数据库及关联件,分析其件结构如图17-21所。

![](images/0e3b42425258dfd2a5476bdf82182edc93cfc835a5bafa836e7b73afb918852a.jpg)  
图17-21 数据库及关联件结构

3）进数据恢复操作

a）更改mysql/my.ini配置件,设置datadir到数据库件所在录如图17-22所；

![](images/cc5d6652dfc3f31e2f846a70e5ad1a0d5e7363eb7827e2ab349139789adec9ad.jpg)  
图17-22 指向数据库件录

b）在命令下运MySql;cd MySQL\bin; mysqld.exedefaults-file=“xxx具体目录\ MySQL\my.ini";

c）使mysqlbinlog解析志件，般版本的mysql会默认装有mysqlbinlog具（MySQL\bin\），若没有安装可下载，注意位数和版本号；

d）查看志件：showbinary logs命令,如图17-23所；

![](images/017b91fbe9a4ca6681a6131d945884da2f13141eeb5df8ba9203785de48654b2.jpg)  
图17-23 查看志件命令

e)查看 binlog 日志内容：mysqlbinlog -no-defaults -database = db --start-datetime = 'xxx'--stop-datetime ='xxx' mysql-bin.000007| more;具体参数可以根据需求更改，如图 17– 24 所示；f）此日志中记录了时间节点对应的操作，可根据此记录进数据分析或回滚等操作。

![](images/0b4f283582a1d502dd94e774925f407f095722d8fe1a1126f5107762f40b5f44.jpg)  
图17-24查看日志文件

## 4.原理分析

数据库日志是数据库系统中用于记录事务操作和系统活动的文件，其中包含对数据库所有修改和更新操作的记录，以及系统中的错误和异常情况。数据库日志可记录物理数据页面的修改信息，包括每个页面的写入时间、写入操作类型、写入的数据内容等。在发生故障或崩溃时，可通过日志快速定位和恢复数据。

每当要对一条记录做改动时（包括INSERT、DELETE、UPDATE），数据库日志都需要记录下来。比如插入一条记录时，需要把这条记录的主键值记下来，之后回滚时把该主键值对应的记录删掉;删除一条记录时，需要把这条记录中的内容都记下来，之后回滚时把由该内容组成的记录插入到表中；修改一条记录时，至少要把修改这条记录前的旧值都记录下来，之后回滚时把该记录更新为旧值。

## 5.要点与难点

1）除了MySQL数据库，其他主流的数据库都留存各类形式的日志数据，数据库日志在数据库恢复中起到重要作用。常规的数据恢复有时专注于数据库文件本身，而忽略了日志。

2）数据库日志记录着几乎每一条增删改的操作，日志条目量巨大，查询和回滚的工作量都很大，但日志通常是以时间属性为键值，在检验中可灵活利用。

3）当日志量过大时，数据库有时会设置为收缩或简化日志内容，给检验恢复工作产生障碍。

## 案例三 SQL server 数据库恢复

## 1.任务要求

某单位SQL server数据库服务因为未正常停止，再次启动时无法加载mdf数据库文件，现需恢复其中数据。

## 2.操作环境

操作系统：Windows 10;软件程序：Recovery Toolbox for SQL Server。

## 3.操作流程

根据标准法中约定的检验规程，数据恢复操作的主要流程如下：

1）使只读设备将检材硬盘接检验作站，制作对应的镜像件，并计算哈希值。

2）使RecoveryToolbox软件对镜像结果中的数据库进恢复操作。

a）分析来自损坏数据库的系统信息；

b）预览数据，可以从扩展名为\*.mdf的损坏文件中检索；

c）选择数据导出方法，可另存为一组SQL语脚本，也可将恢复的数据直接导出到新的数据库。

d）导出想要修复和保存的数据信息。

e）预览数据导出报告。

## 4.原理分析

mdf类型的数据库文件是一种页式存储格式，整个文件由若干数据页组成，每个数据页内包含3个主要部分：页面标题、记录和记录偏移量数组。数据页的页号从0开始，每个数据页占用8192个字节，是固定大小，其中页面标题占96个字节，随后的记录偏移量是一个1维数组，数组中每个元素占用2个字节，最后的字节空间存放记录内容。数据页的结构分布同NTFS系统中MFT管理策略类似，不同数据页拼接在起组成了整个数据库件。

在每个数据页中，页面标题占用前96个字节，主要包含图示字段项。页面标题后的数据空间以存储表的形式管理数据记录。1条记录最大占用8060个字节，单条记录一般不能跨越多个页，但本或图像类型数据可能会存储在对应的独页中。每个页中存储的记录数根据表结构定义和数据类型产变化，对于固定长度列的表，每个页面存储记录条数相同，可变长度记录的表，将根据数据实际长度来决定页中容纳的记录数。

记录偏移量的存储管理是基于1维数组，每个数组元素记录了页面中相应条开始的偏移量。数组排序从0开始，每个数组元素占2个字节，存储位置从第8192字节开始倒序存放。如第1个元素[0]，存储位置对应该页的第8192和第8191字节，第2个元素[1,存储位置对应该页的第8190字节和第8189字节。记录偏移量数组描述了当前页中记录的存储逻辑顺序。SQLServer组合使页面中的件编号、页码和记录偏移量数组元素来唯一地标识表中的每一条记录。

## 5.要点与难点

Mdf文件的存储结构非常复杂，上述案例中mdf文件只是内部结构出现问题，恢复成功概率较，但当mdf文件碎化时，就无法通过上述选定数据库件的式进恢复，只能尝试碎化拼凑的法。碎化拼凑类似件指纹特征恢复的逻辑，会遍历整个硬盘寻找mdf件的存储特征值，然后利键值将其拼凑，以达到恢复的效果。

## 四、硬盘录像机数据恢复

前在应用层面，除了传统服务器的数据恢复，视频监控录像的恢复也是一个典型性问题，不仅录像机的品牌型号种类繁多，对应的存储管理系统也趋封闭。因此，本节单独对硬盘录像机的数据恢复进详解，重点对个典型品牌的存储管理系统进解析，以形成监控数据的解析定位和提取能力。

## (一)基础知识

随着信息化发展需求的增长，视频监控设备的业领域规模在短短年间实现了跨越式发展,海康威视、华股份两家龙头公司的相关产品乎占据了整个视频监控业的三分之，在安防布控、调查取证过程中发挥了重要的支撑作用。在实际应用中，为了保障监控数据的安全存储和可控管理,不少视频监控录像机等相关设备都采了闭源系统,对应的件管理系统也并常见的NTFS、Ext4等，而是各个厂商定制或次开发的件系统，比如DHFS、WFS、H.264等。

以华视频监控设备为例,其采的DHFS件系统就是种典型的通型件系统。使用X-ways等工具，读取大华视频监控对应磁盘的0号扇区，在0x0000位置有明显的“DHFS”标识信息，后续位置还存有对应件系统的版本信息，如DHFS4.1。对DHFS的相关结构进行解析，其第0扇区为标识和引导扇区，第1扇区至33扇区为保留扇区，第34扇区为管理系统启动扇区。在数据存储中，DHFS定义数据块为视频文件分配的最小存储单元，数据块的存在为优化DHFS视频监控恢复算法起到了分重要的作。

此外，WFS（通型视频监控件系统)也是一种常见的专用于视频监控存储管理的件系统,其数据存储结构持厂商定义，并在视频监控管理系统中进相应参数设置，以便正确加载视频监控数据。WFS件系统是一种件系统模板，持不同场景的定义设置，对些不具备主研发能的视频监控设备厂商，WFS件系统是一种常见的解决案。WFS件系统，同样将0号扇区作为标识和引导扇区，1号扇区至23号扇区作为保留扇区，24号扇区为系统启动扇区，24号扇区0x10偏移位置记录了当前视频监控系统最后次录制视频的起始时间。

除了通用件管理，视频监控的一个重要环节是对视频件的编码存储，前视频监控领域通常采H.264视频编码标准，这是一种分辨率、压缩率的编码标准，可以在保持较图像质量的同时，实现更高的压缩率，有效降低文件大小，提升处理效率。H.264标准最初由ITU–T提出，随后被ISO和IEC共同认可并成为国际标准。

基于上述分析，可以看到，对于视频监控录像机，其视频数据的存放管理涉及多个层次，自上下包括视频编码、管理系统、件系统、存储介质等，其中只有最底层的存储介质为通产品，上层的文件系统、管理系统乃至视频编码标准等都可能存在定制化差异。因此，视频监控数据的解析恢复，需要根据情况不同形成定制化技术案。

视频监控设备多采通型管理和件系统,对应视频的编码格式标准也尚未统，其中存储的视频监控数据,可能会由于物理介质损坏、管理系统故障或误操作等原因造成数据丢失，对应的恢复难度比较大。本节以市场占有率较大的大华视频监控系统（DHFS)为例，分析视频码流的编码和存储规则，以及DHFS件系统的关键参数设置等，从针对误格式化或部分数据覆盖等问题，进监控数据的通道分离与重组，提取可正常播放的视频监控记录，也为其他通型视频监控件系统的提取恢复提供参考。

## (二）案例介绍

## 1.任务要求

某大华视频监控设备因为异常掉电的原因，无法正常读取其中数据，现需对其进行数据恢复。

## 2.操作环境

操作系统：Windows10;软件程序：X-ways、蓝梦监控录像恢复软件。

## 3.操作流程

根据检验规程，对该案件的检验大致分为以下过程：

1）使用只读设备将检材硬盘接检验作站，制作对应的镜像件，并计算哈希值。

2）对镜像结果进数据恢复操作使用蓝梦监控录像恢复软件打开镜像，点击“视频解析”功能，会扫描分析整个镜像数据，完成后展示出所有可用视频数据，包括对应的时间属性和通道数等，其中还会标记出删除视频，选定目标视频后导出即可验证。

## 4.原理分析

使用X-ways查看硬盘镜像的0号扇区，在Ox0000位置发现DHFS标识信息，说明当前硬盘中存储了基于DHFS管理的视频监控数据，如图17-25所示。

![](images/d5ab6da3993c21c9b3df8429879bb68c27057fdef3a667037e6be1c8dd5ffc0e.jpg)  
图17-25 DHFS标识信息

搜索视频文件的头部特征“0x44484156”，定位到视频帧头，手动解码视频数据结构，包括通道号，时间，帧号等，如图17-26所示。

![](images/37f977a8bc050b4cbe4cd72b317ec061c607420b6559d36ff31fdec90c9dfc9d.jpg)  
图17-26 视频文件的头部特征“0x44484156”

截取两个连续的视频帧，逐字节进行对照分析，红色标识对应上面结构体的定义内容，通过header 可定位所有视频帧，帧1 的 tail 和 tail_size 是描述上一帧数据，可以看到帧2的 tail_size等于帧1的 $\mathrm { s i z e } ^ { \cdots } 0 \mathrm { x } 0 \mathrm { D } 0 \mathrm { A } ^ { \cdots }$ 。以header为起始偏移 size字节，就是第二个连续帧。

验证通道数据是否交叉是通过channel定义，也就是记录视频的通道号，大华的通道号比实际的小1，所以对应数据为0x0000+1。data记录了监控录像时间，以十进制的形式存储。frameNO是帧号，帧1和帧2的data和frameNO是连续的，就说明这两个视频数据是连续的，无通道和时间交叉，如图17–27 所示。

![](images/482acd5e8e4d3fba6076fa5e6b6059b7929f1f90e71ff0848e177c1f26c6bc9b.jpg)  
图17-27视频文件帧1 和帧 2

依据上述分析内容，可设计对应算法对多通道时间交叉的视频碎进重组，从而重现完整的视频文件。

## 5.要点与难点

1）当镜像结果不完整或者件系统出现问题时，可能会导致件录或者视频属性丢失，尤其是时间属性丢失，会对视频件恢复造成严重影响。但是，视频件的时间属性不仅仅记录在文件系统中，往往在视频画面中也会记录，通过截取底层十六进制数据，再使用对应的播放软件播放，往往对恢复和鉴定有出其不意的效果。但需要注意的是，论是件系统中还是视频画中记录的时间属性都是系统时间,以监控设备的硬件时间为基准，往往未经过络时间同步，一般需要在恢复和鉴定前进验证。

2）监控系统通常是24小时不间断录制，由于存储介质容量有限，往往会设置为循环覆盖，根据存储介质的容量大小就会形成一个录制周期，当目标视频超出录制周期时，基本会被滚动覆盖，无法继续恢复。

## 第三节 物理数据恢复

本节主要介绍物理层和固件层的相关技术原理，以及对应的数据恢复技术法。相逻辑数据恢复，物理层数据恢复软件复杂度不，侧重机械维修，而固件层数据存在技术垄断、知识产权保护等原因，相应的逆向和恢复作也存在定门槛。具体来说,在物理层，数据恢复主要根据存储介质的不同电磁特性，开展设备功能修复，固件层数据恢复则根据不同品牌型号的固件程序库，通过读写备份、模块替换和重置等方法，调整适配驱动控制逻辑，实现对硬件设备的正常调用和解析。

## 一、硬盘物理故障恢复

硬盘的概念最早起源于20世纪50年代，由于计算机业应发展迅速，数据量飞速增长，早期的磁带类型存储介质存取速度较慢，容量有限，且随机存取不便。为了解决这些问题，IBM公司在1956年推出了第一款硬盘驱动器，称为“IBM305RAMAC”，使了种名为“磁性表面储存”的新技术，以实现在较小的空间内存储大量数据，并可以随机读取。这就是现在常见的机械式磁性硬盘的雏形，随着技术工艺的改进，单盘容量、盘转速、读写访问策略等不断优化提升，规格尺寸、外部接也不断调整，在某种场景下前仍然是计算机设备的主流存储介质。

固态盘最早由闪迪公司在1991年推出，商发展历程今已三多年。随着主控芯与闪存颗粒技术的不断进化，固态硬盘的产品线也不断细分，从技术构成来看，芯片颗粒从2DNAND发展到3DNAND，主控芯的成熟度不断提。从应场景来看，固态盘读写速度增长了倍，单盘容量也实现了跨越式发展。从规格型号来看，接种类从传统的SATA发展到mSATA、M.2、SAS、PCI-E、U.2等，外观尺寸等也有了很大差异。从数据恢复的角度，固态盘最关注的主控芯片方案也发展出LSISandForce、Indilinx、JMicron、Marvell、Phison、Sandisk、Goldendisk、Samsung以及Intel等家主流商的应案以及更多国产化案。从长远来看，固态盘由于其轻便性、灵活性和低成本在越来越多的场合会逐步取代机械硬盘，相应的数据恢复技术研究仍在快速发展中。

## (一)机械硬盘工作原理及维修技术

机械硬盘的工作原理是利用特定的磁性粒子来记录数据。磁头读取数据时，根据磁性粒的不同极性转换成不同的电脉冲信号，再利数据转换器将这些原始信号变成计算机理解的二进制代码。写操作则是相反的过程，根据计算机指令要求，通过磁头改变对应位置的磁性粒子的极性。由于计算机指令运行速度较快，硬盘的数据读写可能存在速度差，一般会在硬盘中设置一个存储缓冲区，以协调硬盘与计算机在数据处理速度上的差异。

硬盘内的磁性盘片，在每一面上均划分为若干个同心圆，以转动轴为轴心，以不同磁密度为间隔进读写识别和存储管理。这些同圆也称之为磁道(track），每个磁道又被划分为若个扇区(sector)，计算机数据按扇区存放在硬盘上。磁性盘的每上都有个对应的读/写磁头(head),通过内置机械臂进传动和位移管理,不同磁头在相同位置的磁道构成了所谓的柱面（cylinder）。硬盘内的数据读写就是以柱面、磁头、扇区为三维坐标体系进行寻址定位，也称之为CHS寻址。

硬盘驱动器正常加电后，首先启动PCB板控制电路中的初始化模块，此时磁头一般置于盘中心的默认位置，初始化完成后主轴电机启动，带动盘开始旋转，磁头机械臂也调整移位至盘片表面的00道，磁头悬浮等待指令的启动状态。运行中，磁盘接口电路接收到计算机系统传来的指令信号时，通过前置放大控制电路，驱动音圈电机发出磁信号，通过磁头感应盘片的阻值变化，以进行寻址定位，并将定位后接收的数据信息进解码，通过控制电路传输给接电路，并反馈给计算机系统完成指令操作。

对传统机械硬盘进拆解，其外部结构主要包括硬盘的外壳和PCB板，内部结构常精密，包括磁盘、磁头、电机组件等，如图17-28所示。硬盘的外部结构相对稳定，出现的故障问题多是在PCB板上。硬盘的PCB板上分布着主控芯、缓存、电机驱动芯、BIOS及其他电子元器件，前端还有硬盘的电源接口和数据传输接口。电源接口有限压保护，超出规定电压时保护极管或者保险电阻会烧毁，导致硬盘无法供电。

其中，电路板上的BIOS芯是最核心的组件，内部存储了与硬盘匹配的固件信息，包括硬盘容量、接、坏扇等重要参数。BIOS芯如图17-29所。

![](images/4267959c7e0f2403280edc7f727c772fcbb0daab1b15e4b1a06013460913416b.jpg)  
图17-28传统机械硬盘

![](images/2fa1cffe45029105cbd794c238a3f6d890605eb51fa00383378061ba5373111d.jpg)  
图17-29BIOS芯片

硬盘的正常运转完全依托BIOS芯中的固件程序，可理解固件程序是一套管理硬件设备的单机系统，无论是硬件状态变化或者固件程序错误都会导致硬盘驱动器作异常，相比动还原硬件状态或者修复调整固件程序，最简单的修复法还是进同类替换。

硬盘修复通常进行PCB板的同类替换，要求使用同一产品型号，生产批次相近的功能正常PCB板进替换，但由于BIOS芯内存储了与硬件状态相关的程序或微代码信息，替换后的PCB板通常法驱动硬盘正常运转，必须把原始PCB板上的BIOS芯替换焊接新的电路板上，才能保障硬盘的正常识别。或者，也可使用编程器配合PC3000等固件修复软件，进内部固件程序的备份和替换。

相比硬盘外部结构，硬盘的内部结构更加精密复杂，包括磁盘盘片、磁头、主轴与传动轴等几个重要组件。其中，机械硬盘通常由多个盘组成，每个盘都是由磁性材料制成的，可记录数据。这些盘片安装在同一个旋转轴上，通过马达驱动旋转起来，对应转速的概念。

硬盘内的读写磁头通常由个机械臂撑，可在盘的表上移动，以便于在不同的位置读写数据，实现随机存取。磁头可感知到盘片上的磁场，通过控制电流来写入或读取数据，每个盘面均有一个对应的读写磁头，这些磁头通过机械臂统一控制，构成了磁头组件。磁头的数据解析还需要后端的控制器配合，以解读计算机指令，完成相关机械动作。

前实践中,最核也最常出问题的就是磁头组件,可能产的故障包括磁头芯故障、前置信号处理器故障、磁头物理故障以及衍的盘划伤等问题。磁头组件出现故障时，硬盘在计算机系统中无法识别，且盘腔内部会有各种异响，一般需要开盘进物理修复。由于盘工作时在电机带动下高速旋转，速度可达到5400至15000RPM，一粒微小的灰尘都会造成盘划伤，所以硬盘的内腔均为无尘环境，有些还会填充高压氮气确保不受外部环境影响。因此，进硬盘开盘操作也必须保证足够的洁净度，需要在洁净间或者洁净台内操作。磁头组件的修复也多采用同类替换的方法，选取同产品型号和同批次的正常硬盘，拆取其内部磁头组件进行替换，基本的操作流程如下：

1）准备好同故障盘产品型号相同，产批次相近的备件盘。

2）对备件盘和故障盘的表面进行灰尘处理，做好个人清洁，穿专用工作服，戴专用手套。

3）将故障盘和备件盘同带洁净间，打开故障盘外壳，查看盘表是否存在明显划伤，并进行清洁处理。

4）如果盘上无划伤，将故障盘磁头拆除。用同样法将备件盘的外壳打开，拆除磁头组件，并安装到故障盘中替代原磁头组件。随后，复原硬盘外壳。

5）使PC3000等具加电检测故障盘能否正常识别,识别成功说明替换磁头运转正常。

## （二）固态硬盘工作原理及维修技术

随着固态硬盘业竞争不断加剧，国内外主流的固态硬盘生产企业也在不断改进技术、调整方案，其中主控芯片的相关算法是一个聚焦点，也在持续不断地调整优化，这给数据恢复研究也带来了许多新的挑战。目前，对固态盘进分解，主要包括主控芯、闪存芯片、DRAM缓存等组成，运行中，数据通过接口进人主控芯片，经主控芯片相关算法处理后储存到各个闪存芯颗粒中，如图17-30所，对其中的关键模块解析说明如下。

![](images/1f1499a59f0f505be8b3743897e708cb2616c186ea309eef07e307f9589c99cf.jpg)  
图17-30固态硬盘

主控芯片：主控芯片是固态硬盘进行数据管理的重要组成部分，它负责管理和控制固态硬盘的读写操作，以及对闪存芯片进行调度和管理。控制器芯片还包含一些固件和算法，用于实现数据的压缩、加密、错误纠正和垃圾回收等功能。

闪存芯片：闪存芯是固态硬盘存储数据的主要组成部分，它使用NAND或NOR闪存技术来存储数据。NAND闪存芯通常用于容量存储，NOR闪存芯则用于存储启动代码和固件等小容量存储。

DRAM缓存：SSD还可能包含一些DRAM缓存，用于加速数据的读取和写入操作。DRAM 缓存是一种临时性存储，它能快速缓存数据，但是当固态硬盘断电时，缓存中的数据会丢失。

连接接口：固态硬盘通常使用SATA、PCI-E、U.2或M.2 等接口与计算机主板连接。这些接口提供了高速的数据传输和稳定的电源供应。

在读写存储中，SSD主控通过若干个通道(channel)并行操作多块闪存颗粒，类似RAIDO，以提高底层传输带宽。举例来说，假设主控与FLASH 颗粒之间有8个通道，每个通道可挂载了一个闪存颗粒，HOST与FLASH 之间数据传输速率为200 MB/s。该闪存颗粒 Page 大小为8 KB， FLASH page 的读取时间为 $\mathrm { T r } = 5 0 ~ \mu \mathrm { s }$ ,平均写入时间为 $\mathrm { T p } = 8 0 0 ~ \mu \mathrm { s } , 8 ~ \mathrm { K B }$ 数据传输时间为 $\mathrm { T x } = 4 0 ~ \mu \mathrm { s } ,$ 。那么底层读取最大带宽为（ $8 ~ \mathrm { K B } / ( 5 0 ~ \mu \mathrm { s } + 4 0 ~ \mu \mathrm { s } ) ~ ) \times 8 = 7 1 1 ~ \mathrm { M B } / \mathrm { s }$ ,写入最大带宽为 $( 8 ~ \mathrm { K B } / ( 8 0 0 ~ \mu \mathrm { s } + 4 0 ~ \mu \mathrm { s } ) ) \times 8 ~ = ~ 7 6 ~ \mathrm { M B } / \mathrm { s }$ 。从上可看出，要提高底层带宽，可增加底层并行的颗粒数目，也可选择速度快的FLASH颗粒（或者让速度慢的颗粒变快，比如MLC配成SLC使用）。主控通过8通道连接8个FLASH DIE，为方便解释，这里只画了每个DIE里的一个Block，其中每个小方块表示一个Page（假设大小为4KB），如图17-31～图17–33所示。当所有Channel 上的 Block 都写满时，SSD主控会挑选下一个Block 以同样的方式继续写人料来在 之用，请勿商用。

![](images/b9591090e498c6f665289d14ea43429e8e17d0c1c41a00dab110d398a42d0ca7.jpg)  
图17-31 HOST写4KB数据

![](images/32f64f11b89d5d14a8da3d00b784d24edb9b2fd5a448aa4035f6f7bfd8d59bec.jpg)  
图17-32 HOST继续写入16KB数据

![](images/47293d8ec030c774623731c4a097783fecd8938dccfccd3ea9de0fe9d4227bf1.jpg)  
图17-33 SSD主控

HOST是通过LBA(LogicalBlockAddress,逻辑地址块）访问SSD的，每个LBA代表着个Sector（般为512B），操作系统般以4KB为单位访问SSD。HOST访问SSD的基本单元叫户页（HostPage）。在SSD内部,SSD主控与FLASH之间是FLASHPage为基本单元访问FLASH,称为FLASH Page为物理页（Physical Page）。HOST每写个HostPage，SSD主控会找个PhysicalPage把Host数据写,SSD内部同时记录了这样条映射（Map），如图17-34所。有了这样个映射关系后，下次HOST需要读某个HostPage时,SSD就知道从FLASH的哪个位置把数据读取上来。

![](images/14e43f29e0697390be512ea0f665822dd9c8884a5f56f9faf00fd235afe5e2ec.jpg)  
图17-34 LBA与Physical Page

SSD 内部维护了张映射表(Map Table),HOST每写个Host Page，就会产个新的映射关系，这个映射关系会加(第一次写)或者更改(覆盖写)Map Table;当读取某个HostPage 时,SSD首先查找Map Table 中该Host Page 对应的Physical Page，然后再访问 Flash读取相应的Host数据，如图17-35所示。

![](images/42758c2772cdc365cf4f7397f04df5006b10302b0e93231aa81e75885276144b.jpg)  
图17 – 35 Map Table

目前SSD的物理故障主要体现在接口损坏、电路破坏、异常发热等，其中造成数据丢失的主要原因包括电路板变形、电路断裂、芯片组异常高温等。针对不同类型物理故障，数据修复方法也存在差异。对于外观变形造成电路损坏的情况，可做电路修复还原，使用敷铜线、锡线和电烙铁等对断裂的电路进联通修复。对于元器件损坏严重，同时闪存颗粒不多的固态硬盘,还可考虑物理替换的方式，也称搬板，将主控芯和存储芯逐一拆焊接到新的可用电路板上，从而识别内部数据。

相比机械硬盘，固态硬盘的机械复杂度较低，非暴力破坏情况下物理损坏概率不，相对恢复段也不多。但随着主控管理程序趋精密复杂，常应用中固件故障导致数据丢失的情况占比不断提升，固件的修复问题在后续章节会做进一步展开。

## 二、硬盘固件的修复

硬盘固件是内部各组件关联运的基础,也是调各种硬件资源的基础驱动,固件错误会直接影响硬盘的识别和运。随着各类存储介质容量不断提升，读写速度不断加快，固件程序的复杂度也在不断提高，开发难度的提升不可避免产生了各类错误异常，如常见的逻辑错误、模块丢失、校验出错等等，相应的恢复法只能依靠第三具软件。固件修复的原理就是利用软件调整编辑硬盘的内置固件程序，包括读写备份、模块替换和重置等，但由于固件程序的高敏感性，一般不能直接读取访问，需要特定的技术条件持才可以实现，这就对操作软件提出了较要求，前常见软件包括PC3000和MRT。

PC3000系列产品是目前行业内公认的固件恢复的最佳解决方案，对SATA/IDE、SAS/SCSI、RAID以及SSD/USB Flash等各类型产品均提供了全方位支持，但该软件复杂度较高，对个能储备有定门槛要求。MRT是国内技术团队对标PC3000开发的同类型产品，目前仅持SATA/IDE、SSD/USB Flash固件问题处理，功能细节方面仍存在一定差距，但提供了智能操作指引，对些常见硬盘型号的固件问题提供了动化处理案。

本节后续内容将以上述2个软件的操作实践为主线,讲述不同品牌型号、技术问题的固件修复解决案，重点以案例介绍的式，讲解软件的操作步骤和经验技巧。

## (）MRT操作指引

固件修复软件的核是固件程序库，这需要长期的积累和总结，前MRT对常见SATA/IDE硬盘的持度较好，相应固件库的积累较充。本节针对常见的希捷、西数、硬盘讲解使MRT进固件操作的基本流程和主要特点。

## 1.希捷硬盘固件操作

对任何块存储介质进固件操作前，都需要备份其原始固件，原始固件内包含了许多当前介质的硬件参数信息,如缺陷扇区、错误志等,在后续操作时都需要进针对性分析。点击“硬盘资源备份”可选择具体备份内容，如图17-36所。般少包括电路板ROM信息、模块对象，系统件等。

![](images/a9ed45fd6445690cd31be835ff9ec23489b47ee211bd80493583af01f3e0ef6a.jpg)  
图17-36 固件区备份与还原

如当前硬盘可正常识别，尽量备份所有固件数据,如图17–37所。

![](images/7d90b4aad7589fcc90729ba9f34915755c87c41cbb1a0e3852c4c53e164569cc.jpg)  
图17-37 选择具体备份内容

对于固件程序内部产的逻辑问题,通常可通过覆写或重置等操作进恢复,这就需要标准固件库的持，MRT软件本身提供了常见希捷硬盘的正常固件程序备份，可通过固件回写的式尝试修复。回写时般针对通模块对象和系统件对象进操作,可使批量写的式对重要模块内容进重置。

电路板BIOS芯中的ROM件对物理故障修复后的调试关重要，MRT中也可主提取编辑，点击“编辑ROM件”后,可直接导备份ROM,也可编辑相关内容,如图17-38、图17-39所。

![](images/aacf6d75a6a02d7bc166e9f13636f4029cfd65f6afb72223c05d83347e40528d.jpg)  
图17-38选择ROM工具

![](images/d4f8cc12a96dc0d0bbe1316958bcf6b4b926fe1e9338ce5d901affe1e7088fe8.jpg)  
图17-39 编辑ROM件

下通过案例介绍的式讲述相关软件的操作技巧。

（1）任务要求 希捷硬盘ST4000DM004-2CN1104无法识别，存储数据无法使用，需要进数据恢复。

(2)操作环境 操作系统：Windows10;软件程序：MRT。

## (3）操作流程

●将故障硬盘接MRT进检测，加电启动正常异响,MRT软件指灯处于Busy状态。

•首先备份原始 Rom，因该系列硬盘有固件锁，执行指令会提示Diagnostic Port Locked，所以需要先读取原始Rom以创建虚拟引导。

• 选择MRT特有的虚拟启动功能如图17–40所示。

![](images/6ee461d872fdc1732ebc22b16230b842f631ee3bc1dbdd67ef43b1471cac51bb.jpg)  
图17– 40 MRT 特有的虚拟启动功能

• 在软件中导入原始ROM信息后，创建虚拟引导并写入，重新给硬盘加电并进行握手，选择加载固件中的3D模块，优先选择自身模块，无法获取时可适配同型号硬盘的3D模块信息。Patch选项中，对于存在固件锁的情况，勾选SerialPort-unlock 选项进行解锁。

1）下载虚拟启动资源后，进入终端模式T级，执行以下指令：

F3 T>m0,6,2, , , , ,22   
Max Wr Retries = 00, Max Rd Retries = 00, Max ECC T-Level = 14, Max Certify Rewrite   
Retries = 00C8   
User Partition Format Successful - Elapsed Time 0 mins 00 secs  
指令显示成功后重新识别设备，故障盘已可正常识别。

2）接镜像盘对该故障盘进行全盘镜像，镜像过程中不可断电，如果断电需重复虚拟启动操作。

3）镜像成功后，验证镜像盘数据是否完整，随机抽取相关文件可正常打开，数据恢复完成。

（4）要点与难点通过数据恢复设备读取ROM芯片并解密，如果解密不成功无法执行指令，在执行终端指令时，一定要注意硬盘的状态，如果异响待状态正常后再对硬盘做指令。

## 2.西数硬盘固件操作

西数系列硬盘进行固件操作，第一步同样也需要进行备份，与希捷不同，不同厂家的固件程序结构不同，备份内容也略有差异。同样在MRT中点击“硬盘资源备份”，对于西数硬盘可以备份硬盘ROM、Modules和Tracks三类数据，如图17–41所示。

针对西数硬盘常见的固件故障，MRT也提供了针对性解决方案。比如硬盘通电正常，但读取速度慢，长时间显示busy状态，可尝试使用自动化解决方案，在功能选项中点击“修复启动慢”，如图17–42所示；也可手动修改，在模块列表中加载02模块，清除指定区域数据进行重置。

![](images/30dbae68771f9933dbd995fbb21bfad948338e4dde7e353379efcbe9e9f150d3.jpg)  
图17-41硬盘资源备份

![](images/e6b1995a6efd707fff7f0ff57dd40a78ba0b203660aa1a9227c99e36bcc8c996.jpg)  
图17-42 修复启动慢

由于自动修复在实践应用会出现修复后硬盘型号无法识别，造成不可逆操作。为了安全起见首先备份固件，然后对相应的模块进行手动修改。

本节对应的案例介绍如下。

（1）任务要求 西数硬盘WD5000AAKX-08ERMA0无法识别，需要进行数据恢复。

(2)操作环境 操作系统：Windows10;软件程序：MRT。

(3)操作流程

• 将故障盘接MRT进行检测，硬盘加电后迅速进入就绪状态，但需要长时间自动检测和完全初始化，读取服务区模块和扇区数据非常慢，初步判断为慢反应故障。

· 首先进行模块备份，打开模块列表并备份02 模块，如图 17-43 所示。

![](images/3bd8e3106e29dca59a96bba78055c9b046edba7514a328ebefc6d7341f4ce630.jpg)  
图 17- 43 打开模块列表

1）备份完成后，定位如图17-44所示的标识位置，将标识区域内数据清零并保存，重新加电后解决反应慢问题。如果修改后出现其他故障现象，可使用备份的02模块进行还原。

![](images/83a1c7903efc24f6ce7236871d2061a6bb45687de9168687676b38e599030f7a.jpg)  
图17- 44 定位标识位置

2）接镜像盘对该故障盘进行全盘镜像，镜像成功后，验证镜像盘数据是否完整，随机抽取相关文件可正常打开访问，数据恢复完成。

（4）要点与难点 西数系列硬盘的反应慢问题,在没有固件备份的情况下不要贸然尝试软件的动解决案，实践中有可能会导致硬盘型号法识别。

## 3.日立、三星硬盘固件操作

相比希捷、西数的机械硬盘，日、三星机械硬盘市场占有率较小，固件更新换代不快，问题表现不多，在实践中汇总梳理后，MRT基本提出了针对性解决案。本节以案例介绍的形式,讲述这两个系列硬盘的常见问题解决法。

（1）任务要求 硬盘HTS545032A7E380法识别，需要进数据恢复。

(2)操作环境 操作系统：Windows10;软件程序：MRT。

## (3）操作流程

·将故障硬盘接MRT进检测，第次启动Hitachi-ARM厂程序不认盘，尝试再次启动Hitachi-ARM程序正常，但是编译器没有正常加载，部分数据区内容法访问。

●优先备份PSHT（P-List module）和RDMT（G-listmodule）两个固件模块，如图17–45所示。

![](images/4ef406934e20dca815dae07d047d68063deed6270043835f02c1624f357b7a69.jpg)  
图17-45 备份PSHT和RDMT

·使MRTHitachi-ARM厂程序的虚拟编译器功能，选择从件加载，使用已备份好的PSHT和RDMT执虚拟编译器,如图17-46、图17-47所。

![](images/e7a369b36e8757dbdd6fb755b63d78acef1404253e10e3675b41f4613209ef13.jpg)  
图17-46 虚拟编译器

![](images/9bb46f6e83de3e85ae8fc5e0f47b2f8180f378d4242bf07bc48d90524383ee82.jpg)  
图17-47 虚拟编译器加载选项

·完成虚拟编译器后，如果程序没有报错，说明虚拟编译器成功。如果想进步确定编译器是否正常作，可打开“磁盘扫描具”扫描最后个扇区或者使“扇区查看器”查看最后个扇区是否正常。

启动“虚拟编译器”后，既不能硬复位也不能执掉电操作，否则功能失效。对于某些状态不好的硬盘必须执此类操作时,可在镜像数据的“任务参数”选项卡中将“传输模式”设置为“程序读取模式”，如图17-48所。

![](images/78ca5ef1e4f2f610f33ecb269187417f19196a18c0c2bf86bcf9eb7edbce8e36.jpg)  
图17-48“传输模式”设置

设置完成后尝试数据镜像,如果使程序读取模式镜像速度会很慢，般在10M/S甚至更低。

镜像完成后，验证镜像盘数据是否完整，随机抽取相关文件可正常打开访问，数据恢复完成。

## （二）PC3000操作指引

相比MRT，PC3000的固件库更丰富，支持的功能也更多，本节同样针对不同品牌型号的硬盘，结合常见故障类型在软件操作层进讲述。针对每类硬盘系列，在每节最后均提供了个实践案例，便对验证。

## 1.希捷硬盘固件操作

PC3000中将个完整的希捷系列硬盘固件保存为LDR格式件，内部包含ROM、APP、CERT、CERTTABLE、ATA、Vendor等个重要模块。无论进任何操作，都要先进固件备份。通过PC3000连接希捷硬盘，般需要选择硬盘对应的家族，点击ROM标识即可读取保存的ROM信息，想要备份完整信息则需要使“HDDresourcesbackup”,如图17-49所。如果想进步读写固件模块的系统件，可点击“Readingmodules”（图17-50）以选择主要模块进备份,如图17-51所,对应的“Writingmodules”（图17-52)可选择性重新回写指定模块。

![](images/fefab472a6b21a48f7787ea18d49f86c3bb0059c2edb96589c1048b7cc6899e8.jpg)  
图17-49 查看相关信息

![](images/2bb37e32774db27d156e7554c99d2dacf587064706d8ea62b95099e2395a76e2.jpg)  
图17–50 Reading modules

![](images/a6186d47c88eccd6c9bdc17e84b2fad5269d5085b640c4030670d0c5511e15f0.jpg)  
图17-51ReadROM

![](images/7f0f152ef08bc3221f77d7c193139e8bb1d3ef133d88ad7f0afc74190b116719.jpg)  
图17–52 Writing modules

本节对应的案例介绍如下：

(1）任务要求 希捷硬盘ST3500820AS法识别，需要进数据恢复。

(2）操作环境 操作系统：Windows10;软件程序：PC3000。

## (3）操作流程

●将故障硬盘接PC3000进检测，法识别硬盘型号，且状态灯直处于“Busy”状态。初步判断为硬盘“锁死”，可能是固件中的SMART表和G表出现错误。

●尝试重置SMART表，并重新校验G表。重新加电复位后按Ctrl+Z进T级指令模式，输入下列指令：

T>/2

2>/Z 电机停转

(电机停转后将电路板上隔离物去除并拧回螺丝)

继续输指令：

2>/U 电机启转

2>/1

1>N1 清除SMART

T>i4,22 清除G表

（断电重新加电，使硬盘复位并重新进T级，继续输指令)

T>/m0,6,2, ,,,,22 重建编译器

●经过上述重置操作,再次加电后,硬盘可正常识别并可读取数据。

·接镜像盘对该故障盘进全盘镜像，镜像成功后，验证镜像盘数据是否完整，随机抽取相关件可正常打开访问，数据恢复完成。

(4）要点与难点子希捷硬盘的部分批次在使用过程中出现的“锁死”问题，是典型的固件问题，一般是由于SMART表和G表出错导致硬盘无法识别，最常见的解决方法就是用希捷的专业指令清空SMART表，并重新校验G表，随后硬盘恢复正常，数据均可正常读取。

## 2.西数硬盘固件操作

西数硬盘固件构成同希捷硬盘有所不同，固件中的每个模块都会单独计算校验值，任何一个模块校验出错，都会产固件错误导致硬盘法正常启动。

在经典西数架构中，ROM中的固件内容较少，模块表、区域分配表等都保存在盘面固件区,因此,ROM芯具有很强的替代性，也导致经典西数架构的固件问题修复较简单，只要型号相同、固件版本号相同，均可获得较的修复成功率。

对于Marvell架构,ROM与盘固件的相关性常强，ROM中包含访问盘固件区的多项参数，盘面固件区的overlay等模块也必须与ROM模块相匹配。因此，Marvell架构硬盘固件修复需要注意配对参数非常多，匹配更加严格，必须保证型号一致、固件版本号相同、硬盘电机号致、磁头位置致才能保证较的修复成功修复。

西数硬盘同样使用“HDDresources backup”和“Reading modules”功能模块进备份操作，在实践中针对西数热交换常用的03、31、32、40、49、4A模块可通过Readingmodules单独备份。此外，常见的型号信息无法识别，一般是11模块损坏；可识别型号但无法访问扇区，一般是31、32模块损坏，均可通过Writing modules 功能，回写正常的固件库模块来进行修复。上述模块的对应参数见表17-3。

表17-3模块的对应参数
<table><tr><td>模块名称</td><td>参数信息</td></tr><tr><td>03模块</td><td>Format Select Data Module，段位表信息，决定硬盘的访问区域</td></tr><tr><td>31模块</td><td>Translator，硬盘用户区的编译器模块，管理用户区P表缺陷</td></tr><tr><td>32模块</td><td>辅助译码表，一般用于管理G表缺陷，即用户区增长缺陷，通常可以为空</td></tr><tr><td>40 模块</td><td>Adaptive Data 主要适配参数</td></tr><tr><td>49模块</td><td>Adaptive Data适配参数</td></tr><tr><td>4A模块</td><td>Adaptive Data 适配参数</td></tr></table>

本节对应的案例介绍如下：

(1）任务要求 西数硬盘WD5000AAKX-083CA0无法识别，需要进行数据恢复。

(2)操作环境 操作系统：Windows10;软件程序：PC3000。

## (3)操作流程

·将故障硬盘接PC3000进检测，状态灯“DRD”与“DSC”常亮，说明硬件状态良好,但法识别硬盘型号，初步判断为固件损坏，考虑使用热交换方法。

•准备一块与故障盘同型号批次的备件盘，备份备件盘的所有模块，包括ROM，盘体固件等。

•备份故障盘所有模块。如果故障盘已无法读取备份，可利用备件盘作为中介，将备件盘进普通模式后点击停转，再将前端电路板接到故障盘上启转，以备份故障盘内的固件模块。

●将故障盘上的03、31、32、40、49、4A模块写入备件盘。

• 重新加电备件盘，硬盘复位后停转，将电路板接到故障盘再启转。

●启转后查看扇区，如果扇区访问成功说明热交换操作成功，即可镜像故障盘数据。

●镜像成功后将备件盘原始固件模块回写，以备下次使用。

• 镜像盘数据完整，达到数据恢复效果。

（4）要点与难点“热交换”是处理西数硬盘过程中常用的一种解决方案，主要针对故障盘硬件状态不稳定或损坏固件模块较多的情况，通过备件盘虚拟引导的方式，减少对故障盘固件的操作，在读取主要模块时可使用ABA方式读取，根据磁头的状态选择不同磁头读取固件，通过文件对比方法修复损坏模块，再将修复后的主要模块写入备件盘来完成热交换的目的。

## 3.日立、三星硬盘固件操作

日立系列硬盘的固件引导程序通常位于PCB板上的ROM芯片中，包括部分控制电机的伺服程序，在NV-RAM中则保存了硬盘的配置信息，包括启动标示、磁头位图、服务区入口地址、用户区入口地址、SA适配信息等。日立系列硬盘如果ROM损坏，多数情况会导致伺服系统无法工作，或表现为Busy 状态灯常亮。如果NV-RAM 信息不匹配，将导致硬盘敲盘或无法正确加载模块。

三星系列硬盘固件则分为两部分，即PCB板的ROM与盘面固件区SA。ROM固件中包含了启动代码及调节磁头读/写盘面固件区的适配参数。硬盘加电后，会通过主控芯优先加载ROM代码，随后再根据 ROM固件读取盘面固件区的模块。

日立系列硬盘的常见固件问题主要是P表问题，表现为数据读写前好后坏，修复中可完整提取P表的COPY0和COPY1，通过同步比较剔除坏扇区后进行重组加载，或者优先加载COPY1，一般可解决多数固件问题。

三星系列硬盘的常见固件问题在PC3000中提出了不少解决方案，比如硬盘加电后，长时间busy状态随后停转，可通过进安全模式后清除ALIST表来解决，重新加电后即可读取数据镜像。注意，不管对任何系列硬盘固件进行操作，一定要进行备份，如图17-53所示。

![](images/870e762379dc646b7506640567fc7b9532489dca6c1bc292eeda73c557b6c0c1.jpg)  
图17-53 备份硬盘固件

本节对应的案例介绍如下：

(1)任务要求 三星硬盘HD161HJ无法识别，需要进行数据恢复。

(2)操作环境 操作系统：Windows10;软件程序：PC3000。

## (3)操作流程

•将故障盘接PC3000进行检测，加电后指示灯处于busy状态，随后电机停转，初步判断为缺陷列表溢出故障如图17-54所示。

•使用三星专用的com口连接硬盘并进入安全模式(safe mode)，清空ALIST,如图17–55所示。

![](images/366c47253c33094918efbecfb5d78fdfe0d48a2fd04c00cdda886c6eb96a0cfa.jpg)  
图17-54检测加电

![](images/bcfcb39dbcc5bf095b7689f0115320b1c7caf51950e28f244f01fc00001d0e38.jpg)  
图17– 55 清空ALIST

· 清空ALIST后重新加电，进正常模式，尝试访问扇区已能正常打开。

• 接镜像盘对该故障盘进行全盘镜像，镜像成功后，验证镜像盘数据是否完整，随机抽取相关文件可正常打开访问，数据恢复完成。

（4）要点与难点此固件问题是“三星”硬盘的通病，状态及表现基本一致，清空ALIST功能是清空重定位扇区表并修正保留空间表，是逻辑描述与缺陷位定位的预先操作，此操作是为了将数据扇区返回原始位置。

## 4.固态盘的固件操作

固态硬盘中也存在固件问题，固态盘的固件通常是指固化在ROM中的引导管理程序，一般用于管控读/写和传输算法，协调和控制硬盘内各部件之间的相互作用，比如管理数据在NAND中的存放位置，记录NAND中有缺陷的扇区以避免再次使用等。固态盘的固件恢复流程同机械盘基本相同，一般先检测固件版本，提取备份固件数据后进行分析，通过参数调整进修复操作。在PC3000中，固态盘固件修复的主要操作流程和方法基本如下。

将固态硬盘接PC3000SSD端口，启动程序并加电，进通用模式即可查看固态硬件对应的基本信息及健康状态，如图17-56 所示。对于部分加密的固态硬盘还可进入专业模式清除密码。

固态盘根据主控芯片不同，固件程序版本及内容也有较大差异，以国产固态盘常见的SM2258XT为例，其包含的固件模块和配置参数如图17-57所示。

![](images/1ee71c3d3f3f3738af3cb6a412e34236f047a87080daa3a9a0243492715e7a87.jpg)  
图17-56 查看固态硬件对应的基本信息及健康状态

![](images/296598246d1b2d3ab37f992003f0054580ac32731687c36806f034feccdca66f.jpg)  
图17-57 查看固件模块和配置参数

固态盘中的固件问题多与编译器有关，相关问题的解决主要依靠PC3000提供的预制案，主要针对编辑器本的软件错误或户误操作产的故障问题。

本节对应的案例介绍如下，在何权莉，技供公众及法律从业著学生等法学研凭学习之用，请勿商用。

(1）任务要求 送检固态盘法识别，需要进数据恢复，如图17–58所。

(2）操作环境 操作系统：Windows10;软件程序：PC3000 SSD、R-Studio。

![](images/83441f46a44db00edf3cc243df24b4d72de2c3a6e88645c5845d1daea83628b2.jpg)  
图17-58送检固态盘

## (3）操作流程

• 将送检固态盘接PC3000 进行检测，硬盘识别访问慢，无法正常读取数据。

• 通过短接进入工厂模式，识别选择对应的主控程序，加载 Loader 相关信息，虚拟重建编译器。

• 重建后硬盘可正常读取访问，接镜像盘进行全盘镜像，镜像成功后，验证镜像盘数据是否完整。

•使用R-Studio 软件解析数据镜像，提取指定类型数据文件，对提取的文件计算哈希值。

（4）原理分析送检固态盘初步检测判断为固件问题，故障表现为数据读取速度极不稳定，偶尔遇到坏扇可能产生“假死”。

首先通过主控芯片检测确定为SM2258XT，使用镊子短接进入硬盘安全模式，此时PC3000中状态灯DRD和DSC灯常亮，说明硬件状态连接正常，通过控制器选择加载SM2258XT主控程序，识别对应芯片ID及类型后，加载Loader对应固件如图17-59所示。

![](images/a7c068d7aaf1b8d85765cc4d97540c0599824932e3047348117b96162caf14dc.jpg)  
图17–59 加载 Loader对应固件

通过PC3000DE创建数据恢复任务，设置读取参数为“用有效的PC-3000工厂实用程序读取数据”，如图17–60 所示。该功能会重新创建翻译器，虚拟原固件状态以达到正常启动的目的。

![](images/9963eec947d00be82c7fd31423f1bac6b6cb7dc3e649d2d36779857cb7199ccf.jpg)  
图17-60设置读取参数

（5）要点与难点固态盘的固件问题修复，核心难点在于主控信息库的内容披露较少，相比市面流通的固态盘产品覆盖率非常低，不少品牌型号的主控信息存在加密，兼容适配性低，这都导致固态盘的固件修复成功率不高。本案例中分析的 SM2258XT，在近两年推出的国产固态盘中适用很广，相关研究比较深，对应的解决方案也相对成熟。

## 三、芯级数据恢复

近些年，随着半导体芯片业的飞速发展，基于闪存芯的存储介质也日渐占据个人消费领域的广大市场，常见的芯片类存储设备包括闪存盘（又称优盘或U盘）、存储卡（SD、TF等)和固态硬盘(SSD)等。基于芯片的存储介质其制造工艺、存储原理同传统的机械硬盘有较大差异，数据恢复中的整体思路也有很大差别。总体来说，根据颗粒规格、封装方式、是否独立主控等几个主要特征，可分成几类问题进行处理。

## (一)基础知识

目前闪存芯的颗粒规格主要包括Nor Flash和Nand Flash，根据其参数特征，在用户数据存储方面，无论SSD、存储卡、闪存盘或智能设备的内置存储均使用Nand Flash，包括 EMMC也只是一种基于Nand Flash 的封装解决方案。基于Nand Flash构造的存储，通常以页为单位进行数据的存取管理，需要主控程序的合理调度才能保证较快的读写速度和较长的芯片使用周期。其中，为了平衡读写速度和芯片的使用周期，在主控程序中引入了Trim命令加速空闲空间的定时回收，但这样也导致逻辑层常用的数据恢复机制难以发挥作用，通过算法定位到的用户数据区文件，很可能在文件刚删除时就被清零了，无法再进行重建。

前，针对芯的数据恢复，大多是对物理层和固件层的研究，尤其固件层根据主控特征不同，衍出许多不同案的数据提取技术，但核心问题都是芯直读后的数据重组还原。目前芯类存储设备仍在快速发展中，主控程序的调整完善也始终在路上，不少主控程序的设计开发或者后期灌装中存在问题隐患，由此产了各种类型的数据丢失问题。如常见的设备无法识别、磁盘未格式化等。其中，除了部分是晶振元件损坏，其他都是主控程序的问题，由于前尚未能建完整的主控程序库,所以很多数据恢复只能在主控程序缺失的情况下进数据重组，其核心问题就是数据重组的算法研究。

随着数据安全技术发展更新，越来越多的存储设备都会在主控中引加密存储，主要的技术实现式是在数据存闪存颗粒前进异或加密运算,这也导致通过芯直读得到的数据块均为零散的加密内容，相比RAID恢复方法，这种加密分散存储甚至没有校验位可参照。因此，此类问题的破解需要确定加密算法以及随机数或密钥值，并借助相关程序算法进行数据拼接验证。以相对简单的U盘恢复为例，目前常见的恢复工具虽然可以做芯片内容直读，但很难解析出对应的加密密钥，仍然需要人工检验和解密拼接。

## （二）案例介绍

案例一 U盘芯直读重组恢复

## 1.任务要求

送检的某品牌U盘无法识别，通过数据恢复提取其中的照件。

## 2.操作环境

操作系统：Windows10;软件程序：PC3000 DE、R-Studio。

## 3.操作流程

1）将送检U盘接数据恢复平台进检测，法识别访问，初步判断主控信息损坏。

2）尝试芯直读法,通过热风台将芯加热取下并清理引脚污垢。

3）接PC3000Flash,读取存储芯信息及DUMP件。

4）通过分析DUMP数据，确定相关加密和重组算法，完成数据恢复作。

## 4.要点与难点

本案例以主控为SSS6698及存储芯型号TC58TEG6DDJTA00的NandFlash芯为例，利扰码位图的研究法，解析发现LFSR产XORkey的相关规律，从逆推XORkey，通过重组验证了XORkey的正确性。

先，需要确定芯内部的数据存储结构，包括芯的ID号、芯型号、Page大小和Block等关键参数，其难点在于page页内结构的分析，可借助些数据算法具辅助计算。其次，观察加密后的数据特征，判断密钥值的构成方式，一般分为定长随机序列、不定长随机序列以及随机抽取等类，在确定构成方式后，根据第一步计算出的页内扇区数确定密钥值长度。最后，尝试各类数学算法进破解，反推密钥值。算法逆推是芯类数据恢复同磁介质数据恢复最大的差异，目前尚无更成熟的解决方案。本案例中采用的异或解密算法的分析思路，可以将被主控进行扰码操作的NandFlash芯内部的数据还原成明文，以进行后续的数据重组操作。

## 案例手机存储芯片装需，表幕变复葬作坚素年年主 之用，请如肖用。

## 1.任务要求

送检的HUAWEIU7300机法开机，通过数据恢复提取其中的录件。

## 2.操作环境

操作系统：Windows10;软件程序：UFED 4PCR-Studio。

## 3.操作流程

根据检验规程，对该案件的检验大致分为以下过程：

1）初检发现送检机法正常打开，可能存在硬件故障。

![](images/67dbe2b9ccb472aa3b2b9d5e168fbeb1bf4c6fdb0cdb6116cfa9332beb293dbd.jpg)  
图17-61 存储芯

2）检测发现PCB板有烧熔痕迹，法正常加电运转，尝试进芯移植，将送检手机中的存储芯拆除后移植到备件机中。

3）移植完成后，机可正常开机访问，使UFED4PC软件解析机数据，提取指定录件。

## 4.要点与难点

送检手机无法正常点亮，拆机检测后初步确定主板物理损坏，加电响应。进步检测发现主板上有烧焦痕迹，个别芯有轻微位移，使用放大镜观察存储芯，有轻微倾斜，具体情况如图17-61所。

使同型号的备件机尝试芯移植,将存储芯移植到备件机中，开机后可正常点亮，确定故障排除，如图17–62所。

![](images/ac294b6c43ae484def63a4f0daa7eedfefb14665b74c549ca53ec6ea4812f1d9.jpg)  
图17-62 移植存储芯

## 第四节小结

电数据恢复是电数据鉴定技术领域的项基本技能，整体技术思路偏向于逆向程，在理解数据存储原理的基础上，分层级进行读取和解析，以复原出数据包含的有效信息。可以说，电子数据恢复的本质，就是基于对不同类型存储单元的分层研究，深入理解其对应的物理层、固件层和逻辑层的功能实现原理，结合逆向分析和比照验证等技术段，在相应层级的功能失效或数据损坏的情况下，手动进数据重建，挽救重要数据信息。

在司法鉴定实务活动中，面向存储介质的数据恢复是一项基础工作，从前期的数据固定，到后续的解析恢复和深度检验，电数据恢复解决了最重要的数据来源问题，为案件的调查分析和事实认定奠定基础。因此，电数据恢复在司法鉴定领域得到度重视，针对不同存储介质的发展变化，相应的理论体系、技术法和工具软件等也在不断更新。前主流的三类存储介质，磁存储介质和光存储介质的技术体系已相对稳定，在对应的产品领域,大部分产品均来少数家产商,但由于专利保护等因素,相应存储产品的技术分析和逆向验证只在范围开展，最终以解决方案的形式对外提供数据恢复工具。而电存储介质伴随芯业的快速发展仍在不断迭代中，对应的技术体系尚不稳定，相应的恢复理论和技术工具也还不够完善，具有较大的发展空间。在物理层和固件层之上，逻辑层的技术发展也非常迅猛，根据应用场景不同,数据存储也趋于多层和类型化,随着数据库、分布式存储以及安防监控等特定类型产品的不断发展丰富，相应的数据恢复理论也需要持续更新，对应的数据恢复工具也很难再具有普适性，对从业人员自身的知识积累和实践经验提出更要求。

电数据恢复具有存储介质的相关性，也受到数据层级和应场景的影响，是项糅合了软硬件的系统工程，根据存储介质的类型不同，抑或是数据存储层级的差异，相应的恢复理论和工具软件都具有较大的差异性。这都要求从业人员保持一种持续学习的态度，对相关领域的技术发展及时研究跟进，不能依靠单一工具解决所有问题。同时，电子数据恢复也是一项考验耐心和细心的技术工作，无论是底层数据的信息释义，还是碎数据的重组分析，都需要从业员保持度的专注和责任。未来，论社会如何发展，技术如何进步，电数据恢复作为一项前置性工作都具有不可替代性，希望读者能在本节的内容中有所收获,找到自已擅长的方向，以不息为本，以日新为道，在热爱的领域做出自己的一份贡献。

![](images/1f05b32a8f53148b8283912fbd7131bbe7c7e71f62286f9042e3dd2123fb1586.jpg)

## ·思考题

1.在实际应用领域，简述数据存储的基础原理主要类别。

2.简述NTFS文件系统数据的恢复过程。

3.简述文件指纹特征的恢复方法。

4.简述RAID 阵列的数据恢复过程。
