##  WSL 详解

### 启用WSL

```
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
```

### 安装WSL2需要什么版本

对于 x64 系统：**版本 1903**或更高版本，**版本 18362 或**更高版本

### WSL与WSL2比较

| 特征                                   | WSL1 | WSL2 |
| -------------------------------------- | ---- | ---- |
| Windows和Linux之间的集成               | ✓    | ✓    |
| 快速启动时间                           | ✓    | ✓    |
| 小资源足迹                             | ✓    | ✓    |
| 与当前版本的VMware和VirtualBox一起运行 | ✓    | ✓    |
| 托管虚拟机                             | ✕    | ✓    |
| 完整的Linux内核                        | ✕    | ✓    |
| 全面的系统调用兼容性                   | ✕    |      |
| 跨OS文件系统的性能                     | ✓    | ✕    |

### WSL2 新特性

* WSL 2使用了VM，但效率上与WSL一样快

* 完整的Linux内核

* 提高文件IO性能

  如git clone，npm install，apt更新，apt升级等，在WSL这些操作非常的慢。

* 对Docker应用支持更好

* 

* 

*  

###  Windows Terminal 终端工具

在Mircrosoft Store中搜索Windows Terminal安装则可。

### WSL 2 是否使用 Hyper-V？它在 Windows 10 主页上可用吗？

WSL 2 在 WSL 当前可用的所有 SKU 上可用，包括 Windows 10 家庭。

最新版本的 WSL 使用 Hyper-V 体系结构来启用其虚拟化。此体系结构将在"虚拟机平台"可选组件中提供。此可选组件将在所有 SKU 上可用。一旦我们接近 WSL 2 版本，您就可以期待看到有关此体验的更多详细信息。

### WSL 1 会怎么样？会不会被抛弃？

我们目前没有弃用 WSL 1 的计划。您可以并排运行 WSL 1 和 WSL 2 分时，并可随时升级和降级任何分版本。将 WSL 2 添加为新体系结构为 WSL 团队提供了一个更好的平台，以提供使 WSL 成为在 Windows 中运行 Linux 环境的惊人方式的功能。

### 我能否运行 WSL 2 和其他第三方虚拟化工具（如 VMware 或 VirtualBox）？

某些第三方应用程序在 Hyper-V 使用时无法工作，这意味着在启用 WSL 2 时，它们将无法运行，例如 VMware 和 VirtualBox。但是，最近 VirtualBox 和 VMware 都发布了支持 Hyper-V 和 WSL2 的版本。在此处了解有关[VirtualBox 更改和](https://www.virtualbox.org/wiki/Changelog-6.0) [VMware 更改的详细了解](https://blogs.vmware.com/workstation/2020/01/vmware-workstation-tech-preview-20h1.html)。要解决故障，请看 GitHub 上的[WSL 存储库中的 VirtualBox 问题讨论](https://github.com/MicrosoftDocs/WSL/issues?q=is%3Aissue+virtualbox+sort%3Acomments-desc)。

我们一直在开发支持 Hyper-V 第三方集成的解决方案。例如，我们公开了一组名为"虚拟机[管理平台"的 API，](https://docs.microsoft.com/en-us/virtualization/api/)第三方虚拟化提供商可以使用这些 API 使其软件与 Hy

###  WSL 2 能否使用网络应用程序？

是的，一般来说，网络应用程序会更快，工作更好，因为我们有完整的系统调用兼容性。但是，新体系结构使用虚拟化网络组件。这意味着在初始预览版中，WSL 2 的行为将更像虚拟机，例如：WSL 2 的 IP 地址与主机不同。我们致力于让 WSL 2 感觉与 WSL 1 相同，包括改进我们的网络故事。