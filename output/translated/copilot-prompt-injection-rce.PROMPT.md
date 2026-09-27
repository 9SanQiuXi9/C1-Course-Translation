# 翻译留痕：copilot-prompt-injection-rce

- doc_id：`copilot-prompt-injection-rce`
- 时间：2026-09-27T16:47:05+08:00
- 原文：`extracted/copilot-prompt-injection-rce.md`
- 译文：`translated/copilot-prompt-injection-rce.md`
- 原文 sha256：`96fb390c61775745e65fbcbc167b522fadb1ce9a23b10e29f17985f791dc4625`
- 译文 sha256：`213589484f9695c62bf1627bb3ec5efab40190b9596e5c040a26466f1e690bb0`
- 术语约束条数：16

## 一、本文档涉及的术语清单

| 英文 | 译法 | handling | 出现次数 |
|---|---|---|---|
| `prompt` | 提示词 | `translate` | 14 |
| `injection` | 注入 | `translate` | 14 |
| `security` | 安全 | `translate` | 10 |
| `prompt injection` | 提示词注入 | `translate` | 10 |
| `agent` | 智能体 | `translate` | 6 |
| `vulnerability` | 漏洞 | `translate` | 6 |
| `exploit` | 漏洞利用 | `translate` | 4 |
| `mcp` | MCP | `acronym` | 3 |
| `server` | 服务器 | `translate` | 2 |
| `llm` | LLM | `acronym` | 2 |
| `tool` | 工具 | `translate` | 1 |
| `model` | 模型 | `translate` | 1 |
| `agentic` | 智能体的 | `translate` | 1 |
| `deployment` | 部署 | `translate` | 1 |
| `commit` | 提交 | `translate` | 1 |
| `rag` | RAG | `acronym` | 1 |

## 二、落盘校验结果

```json
{
  "non_empty": true,
  "code_blocks_total": 0,
  "code_blocks_in_translation": 0,
  "code_blocks_match": true,
  "code_blocks_byte_identical": true,
  "urls_orig": 15,
  "urls_trans": 15,
  "urls_all_present": true,
  "urls_counts_equal": true,
  "headings_orig": 14,
  "headings_trans": 14,
  "headings_match": true,
  "orig_chars": 7901,
  "trans_chars": 4389,
  "length_ratio": 0.5555,
  "length_ratio_ok": true
}
```

## 四、发出的 prompt 全文

```markdown
# 翻译任务：copilot-prompt-injection-rce

## 一、文档元数据

- doc_id：`copilot-prompt-injection-rce`
- title：Background Research
- origin_url：https://embracethered.com/blog/posts/2025/github-copilot-remote-code-execution-via-prompt-injection/
- 本段字符数：9,258

## 二、术语约束（本文档用到的，必须严格遵守）

| 英文 | 处理方式 | 出现次数 |
|---|---|---|
| `prompt` | 翻译为「提示词」 | 14 |
| `injection` | 翻译为「注入」 | 14 |
| `security` | 翻译为「安全」 | 10 |
| `prompt injection` | 翻译为「提示词注入」 | 10 |
| `agent` | 翻译为「智能体」 | 6 |
| `vulnerability` | 翻译为「漏洞」 | 6 |
| `exploit` | 翻译为「漏洞利用」 | 4 |
| `mcp` | 保留英文缩写（首次出现给全称） | 3 |
| `server` | 翻译为「服务器」 | 2 |
| `llm` | 保留英文缩写（首次出现给全称） | 2 |
| `tool` | 翻译为「工具」 | 1 |
| `model` | 翻译为「模型」 | 1 |
| `agentic` | 翻译为「智能体的」 | 1 |
| `deployment` | 翻译为「部署」 | 1 |
| `commit` | 翻译为「提交」 | 1 |
| `rag` | 保留英文缩写（首次出现给全称） | 1 |

⚠️ 上表是硬约束，**不得自行更换译法**。
⚠️ 未列出的词按常规翻译；专有名词（MCP、token、vibe coding 等）保留英文。

## 三、翻译要求

- 严格按上表术语译法，不得自行更换
- 专有名词保留英文（MCP、token、vibe coding 等）
- 代码块内容**逐字节原样保留**，不翻译、不改变量名、不动缩进
- 保留所有 Markdown 结构（标题层级、列表、表格、链接）
- URL 一个字都不能改
- 保留 `<!-- CODE_BLOCK_START ... -->` 与 `<!-- CODE_BLOCK_END ... -->` 注释标记
- 标题行数量与原文一致，不要新增或删除标题
- 输出纯中文，不要中英对照
- ⚠️ 只翻译给定内容，不要补充、摘要、扩展、评论

## 四、待翻译原文

````markdown


## GitHub Copilot: Remote Code Execution via Prompt Injection (CVE-2025-53773)

Posted on

 Aug 12, 2025

[#llm](https://embracethered.com/blog//tags/llm)

[#agents](https://embracethered.com/blog//tags/agents)

[#month of ai bugs](https://embracethered.com/blog//tags/month-of-ai-bugs)

This post is about an important, but also scary, prompt injection discovery that leads to full system compromise of the developer’s machine in

[GitHub Copilot and VS Code.](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2025-53773)

It is achieved by placing Copilot into YOLO mode by modifying the project’s settings.json file.

/blog/images/2025/episode12-yt.png

![vscode episode 18](/blog/images/2025/episode12-yt.png)

As described a few days ago with

[Amp, a vulnerability pattern in agents that might be overlooked is that if an agent can write to files and modify its own configuration or update security-relevant settings it can lead to remote code execution. This is not uncommon and is an area to always look for when performing a security review.](/blog/posts/2025/amp-agents-that-modify-system-configuration-and-escape/)

# Background Research

When looking at VS Code and GitHub Copilot Agent Mode I noticed a strange behavior… it can create and write to files in the workspace without user approval.

The edits are immediately persistent, they are not in-memory as a diff to review. The modifications are written to disk right away.

/blog/images/2025/agents-that-can.png

![vscode agents that can modify their own settings](/blog/images/2025/agents-that-can.png)

It’s one of these things that as a red teamer you know is probably not good… so I was looking if this could be used to escalate privileges and execute code.

### YOLO Mode

So, next I researched features in VS Code that depend on settings that are within the project/workspace folder, and quickly found an interesting one.

/blog/images/2025/vscode-documentation-settings-json.png

![vscode-exp-yolo-mode](/blog/images/2025/vscode-documentation-settings-json.png)

It turns out that in the .vscode/settings.json file one can add the following line:

"chat.tools.autoApprove": true

This will put GitHub Copilot in YOLO mode.

And it disables all user confirmations, and we can run shell commands, browse the web, and more!

What is interesting is that this is an experimental feature, but it is still present by default. I did not download a special version or set my VS Code overall into an experimental mode.

Furthermore, it works on Windows, macOS and also Linux.

## Exploit Chain Explained

The proof-of-concept exploit chain to hijack Copilot and escalate privileges is as follows:

1. The attack starts with a prompt injection planted in a source code file, web page, GitHub issue, tool call response, or other content… The payload can also use invisible text as instructions.
2. The prompt injection first adds the line “chat.tools.autoApprove”: true, to the ~/.vscode/settings.json file. Folder and file will be created if they don’t exist yet.
3. GitHub Copilot immediately enters YOLO mode!
4. Attack runs a Terminal command. And using conditional prompt injection we can actually target what to run based on the operating system.
5. We achieved Remote Code Execution powered by Prompt Injection.

Here is a screenshot that shows the demo file with the prompt injection, the developer interacting with the file on the right side in the chat box, and the calculator popping up!

/blog/images/2025/copilot-chat-result.png

![vscode-e2e-calc](/blog/images/2025/copilot-chat-result.png)

Of course any other means of prompt injection delivery, like web or data coming back from an MCP server is an attack angle. I just used it inside the source code file because it’s easiest to test with.

## Video Walkthrough

### Short Demos

Here is a demonstration video that shows the code execution on Windows.

And this one on macOS:

### Walkthrough

Here is a longer form video explaining the discovery and exploit in detail:

AI that can set its own permissions and configuration settings is wild!

## Joining the Workstation to a Botnet - ZombAIs

Of course, this means we can join the developer’s machine to a botnet as a ZombAI.

Also, for fun we can modified the settings.json file to switch VS Code into a Red color scheme and similar things.

It doesn’t end here though! This also means we can build an actual AI virus that attaches to files and propagates as developers download and interact with infected files.

Last but not least, to demonstrate that we have full control of the developer’s host, we show that Copilot can be hijacked to download malware, and join a remote command and control server.

/blog/images/2025/github-agent-e2e-zombai.png

![vscode-zombai-deployment](/blog/images/2025/github-agent-e2e-zombai.png)

This means the door is open for malware, ransomware, info stealers, etc.

Scary stuff.

## Building an AI Virus

When seeing this, one will notice that this basically allows the creation of a virus. An attacker can embed instructions and once they gain code execution, additional malware can compromise other Git projects (and RAG sources) to embed the malicious instructions, and commit the changes or even force push them upstream.

This can lead to further spread as other developers unknowingly propagate the infected code.

Finally, we also need to talk about invisible instructions!

## Using Invisible Instructions

One might say that it would be quickly discovered if instructions are embedded as comments. So in order to make it a bit more interesting, I went ahead and created an invisible payload that achieves the attack chain, but is not visible to users. This was not as reliable, but it still worked:

Note: Although the demo here with invisible instructions worked multiple times for me, using invisible instructions often leads to the exploit being very unreliable, and is also commonly also refused by the model and there is also typically a visual indicator that VS Code shows about Unicode characters. However, attacks (and models) get better over time. It’s also worth highlighting that not all models are vulnerable to such invisible prompt injection attacks.

## Recommendations and Fix

There are actually more attack angles then just the YOLO mode example I shared. When Microsoft asked me if there is any more info I have, I had looked a bit more and noticed there are other problematic places, for instance .vscode/tasks.json that the AI can write to, or adding fake malicious MCP servers, etc which can lead to code execution. And the AI can reconfigure the user interface and configuration settings of the project.

Recently I noticed that developers often use multiple agents, so there is also the threat of overwriting other agent configuration files (allow-list bash commands, add MCP servers…), as they are commonly in the project folder as well.

Ideally, the AI would not be able to modify files without a human first approving it. Many other editors do show the diff, which then can be approved by the developer.

## Responsible Disclosure

After reporting the vulnerability on June 29, 2025 Microsoft confirmed the repro and asked a few follow up questions. A few weeks later MSRC pointed out that it is an issue they were already tracking, and that it will be patched by August. With the August Patch Tuesday release this is now fixed.

Shout out to

[Markus Vervier from](https://x.com/marver)

[Persistent Security who has also identified and reported this vulnerability to Microsoft. You can find their write-up](https://persistent-security.net/)

[here. And also a shout out to](https://www.persistent-security.net/post/part-iii-vscode-copilot-wormable-command-execution-via-prompt-injection)

[Ari Marzuk who seems to also have discovered it in parallel.](https://x.com/Ari_MaccariTA)

Thanks to the members of the MSRC and product team for the help in getting it mitigated.

## Conclusion

This is another example of how an AI agent might not stay in its box! By modifying its own environment GitHub Copilot can escalate privileges and execute code to compromise the developer’s machine. It’s a not uncommon design flaw in agentic systems as I have discovered.

Keep looking out for such design flaws, these should be easily caught during threat modeling.

Cheers.

## References

- [Month of AI Bugs 2025](https://monthofaibugs.com)
- [Amp Code: Arbitrary Command Execution via Prompt Injection Fixed](/blog/posts/2025/amp-agents-that-modify-system-configuration-and-escape/)
- [Copilot Settings](https://code.visualstudio.com/docs/copilot/reference/copilot-settings)
- [CVE-2025-53773: GitHub Copilot and Visual Studio Remote Code Execution Vulnerability](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2025-53773)
- [Persistent Security Write-Up](https://www.persistent-security.net/post/part-iii-vscode-copilot-wormable-command-execution-via-prompt-injection)
- [Persistent Security](https://persistent-security.net/)

---

- [Newer →](https://embracethered.com/blog/posts/2025/google-jules-vulnerable-to-data-exfiltration-issues/)
- [Contact me](mailto:security@wunderwuzzi.net)
- [← Older](https://embracethered.com/blog/posts/2025/claude-code-exfiltration-via-dns-requests/)

````

## 五、输出要求

直接给出译文，用 ``` 包裹便于复制。**不要**输出任何解释、前言或后记。

```

## 五、AI 返回的译文全文

```markdown
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

下面是一段较长的视频，详细讲解发现与利用过程：

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

这是又一个例子，说明 AI 智能体可能不会老实待在它的盒子里！通过修改自身环境，GitHub Copilot 能够提权并执行代码，从而攻陷开发者的机器。正如我所发现的，这是智能体系统里并不罕见的设计缺陷。

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

```
