## GitHub Copilot：经由提示词注入实现远程代码执行（CVE-2025-53773）

发布于

 Aug 12, 2025

[#llm](https://embracethered.com/blog//tags/llm)

[#agents](https://embracethered.com/blog//tags/agents)

[#month of ai bugs](https://embracethered.com/blog//tags/month-of-ai-bugs)

这篇讲的是一个重要、但也令人后怕的提示词注入发现：它会导致开发者机器的完整沦陷，涉及

[GitHub Copilot 与 VS Code。](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2025-53773)

其实现方式是通过修改项目的 settings.json 文件，把 Copilot 置入 YOLO 模式。

/blog/images/2025/episode12-yt.png

![vscode episode 18](/blog/images/2025/episode12-yt.png)

正如几天前在

[关于 Amp 的文章中所述，智能体有一类可能被忽视的漏洞模式：如果智能体能够写文件、并修改自身配置或更新与安全相关的设置，就可能导致远程代码执行。这种情况并不罕见，是做安全评审时应当始终留意的一个领域。](/blog/posts/2025/amp-agents-that-modify-system-configuration-and-escape/)

# 背景研究

在查看 VS Code 与 GitHub Copilot 的智能体模式时，我注意到一个奇怪的行为……它无需用户批准就能在工作区里创建并写入文件。

这些编辑立即持久化，并不是作为待审阅的 diff 留在内存中。改动会立刻写入磁盘。

/blog/images/2025/agents-that-can.png

![vscode 中能修改自身设置的智能体](/blog/images/2025/agents-that-can.png)

作为一名红队成员，你知道这类事情大概率不是好事……于是我开始研究它能否被用来提权并执行代码。

### YOLO 模式

接着，我研究了 VS Code 中那些依赖项目/工作区文件夹内设置的特性，很快找到了一个有意思的。

/blog/images/2025/vscode-documentation-settings-json.png

![vscode-exp-yolo-mode](/blog/images/2025/vscode-documentation-settings-json.png)

原来在 .vscode/settings.json 文件里，可以加上这样一行：

"chat.tools.autoApprove": true

这会把 GitHub Copilot 置入 YOLO 模式。

它会禁用所有用户确认，于是我们可以运行 shell 命令、浏览网页，等等！

有意思的是，这是一个实验性特性，但它默认就存在。我并没有下载特殊版本，也没有把我的 VS Code 整体设为实验模式。

此外，它在 Windows、macOS 以及 Linux 上都能生效。

## 漏洞利用链详解

劫持 Copilot 并提权的概念验证利用链如下：

1. 攻击始于植入在源代码文件、网页、GitHub issue、工具调用响应或其他内容里的提示词注入……载荷也可以使用不可见文本来充当指令。
2. 提示词注入先往 ~/.vscode/settings.json 文件里加上 `"chat.tools.autoApprove": true` 这一行。如果文件夹和文件不存在，会被创建。
3. GitHub Copilot 立刻进入 YOLO 模式！
4. 攻击者运行一条终端命令。借助条件式提示词注入，我们实际上可以按操作系统来决定运行什么。
5. 我们实现了由提示词注入驱动的远程代码执行。

下面这张截图展示了带提示词注入的演示文件、开发者在右侧聊天框里与该文件交互，以及计算器弹出来！

/blog/images/2025/copilot-chat-result.png

![vscode-e2e-calc](/blog/images/2025/copilot-chat-result.png)

当然，任何其他投递提示词注入的手段，比如通过网页，或来自 MCP 服务器的返回数据，都是攻击角度。我只是把它放在源代码文件里，因为这样最容易测试。

## 视频讲解

### 短演示

下面这段演示视频展示了在 Windows 上的代码执行。

这一段是 macOS 上的：

### 完整讲解

下面是一段较长的视频，详细讲解发现与漏洞利用过程：

能自行设置自身权限与配置的 AI 太离谱了！

## 把工作站加入僵尸网络 —— ZombAI

当然，这意味着我们可以把开发者的机器作为 ZombAI 加入僵尸网络。

另外，为了好玩，我们可以修改 settings.json 文件，把 VS Code 切换成红色配色之类的东西。

但这还没完！这也意味着我们可以构建一个真正的 AI 病毒，它附着在文件上，在开发者下载并与被感染文件交互时传播。

最后但同样重要的一点：为了证明我们对开发者主机拥有完全控制权，我们展示了 Copilot 可以被劫持去下载恶意软件，并加入远程命令与控制服务器。

/blog/images/2025/github-agent-e2e-zombai.png

![vscode-zombai-deployment](/blog/images/2025/github-agent-e2e-zombai.png)

这意味着大门向恶意软件、勒索软件、信息窃取程序等等敞开了。

很可怕的东西。

## 构建 AI 病毒

看到这里，你会注意到这基本上允许造出一个病毒。攻击者可以嵌入指令，一旦获得代码执行能力，额外的恶意软件就能感染其他 Git 项目（以及 RAG 数据源）以嵌入恶意指令，并提交这些改动，甚至强推送到上游。

随着其他开发者在不知情的情况下传播被感染的代码，这会进一步扩散。

最后，我们还需要谈谈不可见指令！

## 使用不可见指令

有人可能会说，如果指令以注释形式嵌入，很快就会被发现。所以为了让事情更有意思一点，我做了一个不可见载荷，它能完成整条攻击链，但用户看不到。这种方式可靠性没那么高，但它仍然奏效：

注意：虽然这里使用不可见指令的演示在我这边成功了多次，但使用不可见指令往往会让漏洞利用变得非常不可靠，而且模型通常也会拒绝，此外 VS Code 通常还会对 Unicode 字符给出可视化提示。不过，攻击手段（以及模型）会随时间变强。同样值得强调的是，并非所有模型都容易受到这类不可见提示词注入攻击。

## 建议与修复

除了我分享的 YOLO 模式这个例子之外，其实还有更多攻击角度。当 Microsoft 问我是否还有更多信息时，我又多看了一下，注意到还有其他有问题的地方，例如 AI 可以写入 .vscode/tasks.json，或者添加伪造的恶意 MCP 服务器等等，这些都可能导致代码执行。而且 AI 还能重新配置项目的用户界面与配置设置。

最近我注意到开发者常常使用多个智能体，因此还存在覆盖其他智能体配置文件的威胁（允许清单里的 bash 命令、添加 MCP 服务器……），因为这些文件通常也在项目文件夹里。

理想情况下，AI 不应在未经人类事先批准的情况下修改文件。许多其他编辑器确实会显示 diff，然后由开发者批准。

## 负责任披露

在 2025 年 6 月 29 日报告该漏洞后，Microsoft 确认了复现，并追问了几个问题。几周后，MSRC 指出这是他们已在跟踪的问题，并会在 8 月修补。随着 8 月的「补丁星期二」发布，该问题现已修复。

特别感谢

[来自](https://x.com/marver)

[Persistent Security 的 Markus Vervier，他也发现并向 Microsoft 报告了这个漏洞。你可以找到他们的分析文章](https://persistent-security.net/)

[在这里。同时也要感谢](https://www.persistent-security.net/post/part-iii-vscode-copilot-wormable-command-execution-via-prompt-injection)

[Ari Marzuk，他似乎也并行地发现了它。](https://x.com/Ari_MaccariTA)

感谢 MSRC 和产品团队的成员在推动缓解过程中提供的帮助。

## 结论

这是又一个例子，说明 智能体式 AI 可能不会老实待在它的盒子里！通过修改自身环境，GitHub Copilot 能够提权并执行代码，从而攻陷开发者的机器。正如我所发现的，这是智能体系统里并不罕见的设计缺陷。

请持续留意这类设计缺陷，它们在威胁建模阶段应该很容易被捕捉到。

干杯。

## 参考资料

- [Month of AI Bugs 2025](https://monthofaibugs.com)
- [Amp Code：经由提示词注入的任意命令执行（已修复）](/blog/posts/2025/amp-agents-that-modify-system-configuration-and-escape/)
- [Copilot 设置](https://code.visualstudio.com/docs/copilot/reference/copilot-settings)
- [CVE-2025-53773：GitHub Copilot 与 Visual Studio 远程代码执行漏洞](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2025-53773)
- [Persistent Security 的分析文章](https://www.persistent-security.net/post/part-iii-vscode-copilot-wormable-command-execution-via-prompt-injection)
- [Persistent Security](https://persistent-security.net/)

---

- [更新 →](https://embracethered.com/blog/posts/2025/google-jules-vulnerable-to-data-exfiltration-issues/)
- [联系我](mailto:security@wunderwuzzi.net)
- [← 更早](https://embracethered.com/blog/posts/2025/claude-code-exfiltration-via-dns-requests/)
