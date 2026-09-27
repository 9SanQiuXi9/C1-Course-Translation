# 翻译留痕：archive-raw.githubusercontent.com-assignment-67e0a761

- doc_id：`archive-raw.githubusercontent.com-assignment-67e0a761`
- 时间：2026-09-27T17:10:06+08:00
- 原文：`extracted/archive-raw.githubusercontent.com-assignment-67e0a761.md`
- 译文：`translated/archive-raw.githubusercontent.com-assignment-67e0a761.md`
- 原文 sha256：`e6b3b8cd702dd634d3eb62ef69f34ac25e7611e253dc542344eb5f483b694d85`
- 译文 sha256：`566a7e5d4f93440e0b1417d7c97806e9c26285cce192fae3987faf6183ea5b5c`
- 术语约束条数：15

## 一、本文档涉及的术语清单

| 英文 | 译法 | handling | 出现次数 |
|---|---|---|---|
| `tool` | 工具 | `translate` | 12 |
| `agent` | 智能体 | `translate` | 9 |
| `api` | API | `acronym` | 5 |
| `model` | 模型 | `translate` | 3 |
| `prompt` | 提示词 | `translate` | 3 |
| `mcp` | MCP | `acronym` | 2 |
| `context` | 上下文 | `translate` | 2 |
| `repository` | 仓库 | `translate` | 2 |
| `coding agent` | 编码智能体 | `translate` | 2 |
| `system prompt` | 系统提示词 | `translate` | 2 |
| `annotation` | 标注 | `translate` | 2 |
| `evaluation` | 评估 | `translate` | 1 |
| `reasoning` | 推理 | `translate` | 1 |
| `orchestration` | 编排 | `translate` | 1 |
| `subagent` | 子智能体 | `translate` | 1 |

## 二、落盘校验结果

```json
{
  "non_empty": true,
  "code_blocks_total": 2,
  "code_blocks_in_translation": 2,
  "code_blocks_match": true,
  "code_blocks_byte_identical": true,
  "urls_orig": 7,
  "urls_trans": 7,
  "urls_all_present": true,
  "urls_counts_equal": true,
  "headings_orig": 14,
  "headings_trans": 14,
  "headings_match": true,
  "orig_chars": 8235,
  "trans_chars": 4278,
  "length_ratio": 0.5195,
  "length_ratio_ok": true
}
```

## 四、发出的 prompt 全文

```markdown
(未找到 prompt 导出文件)
```

## 五、AI 返回的译文全文

```markdown
# 第 1 周：解剖一次真实 Claude Code 会话的 Trace

### 作业概览

本周你将把一次真实的 Claude Code 会话放到代理后面，捕获它发出的实际 HTTP 请求，并**解剖它们**。你不需要构建任何新东西。你要做的是以能看清设计决策的细致程度，去阅读一个别人做的生产系统。

#### 学习目标

- **追踪（Trace）**一次来自生产级编码智能体的真实编码会话，理解它的调用结构。
- **识别**在一个非平凡的编码任务中，提示词、工具 schema 与模型响应是如何相互作用的。
- **反思**在你自己的自定义智能体中，哪些行为你会照搬、哪些你会改动。

### 材料

- **[拦截 Claude Code 请求](https://www.ai.moda/en/blog/tutorial-intercepting-claude-code-requests)**：本作业所基于的技术。请先读它。
- **[Anthropic Messages API 参考](https://docs.claude.com/en/api/messages)**：你将阅读的请求形态（`system`、`tools`、`messages`）。
- **[Claude Code 设置参考](https://docs.claude.com/en/docs/claude-code/settings)**：用户级（`~/.claude/settings.json`）与项目级（`.claude/settings.json`）设置如何工作。

### 环境准备

**前置条件：Claude Code**。斯坦福通过你的 SUNet ID 提供 Claude Code 访问权限。如果你还没激活账号，请先[申请访问权限](https://uit.stanford.edu/service/claude)，然后[安装并登录](https://code.claude.com/docs/en/setup)。你的账号获批并完成安装后，用 `claude --version` 确认，并把这个版本号记进你的报告中。

**1. 安装 mitmproxy：**

- **macOS**：`brew install --cask mitmproxy`。
- **Windows**：从 [mitmproxy.org](https://mitmproxy.org/) 运行安装程序，它会把 `mitmweb` 放到你的 `PATH` 上。
- **Linux 或任何平台**：`pip install mitmproxy`，如果你建了课程用的 conda 环境，就在其中执行。

**2. 把它作为反向代理启动：**

```bash
mitmweb --listen-host 127.0.0.1 --listen-port 58888 \
        --web-open-browser --mode reverse:https://api.anthropic.com \
        -w session.flows
```

发往 `127.0.0.1:58888` 的流量会被转发到真实 API；检查界面打开在 `http://localhost:8081`。反向模式意味着你把 Claude Code 指向一个纯 HTTP 的本地地址，因此无需安装 CA 证书。`-w session.flows` 会把每个流量保存到磁盘；请从**任何 git 仓库之外**的目录运行该命令，以免捕获文件被误提交。

**3. 让 Claude Code 指向它**：在你将用于第一部分的仓库里，创建一个**项目级**的 `.claude/settings.json`：

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "http://127.0.0.1:58888",
    "ENABLE_TOOL_SEARCH": "true"
  }
}
```

> ⚠️ **不要把它放进 `~/.claude/settings.json`！** 否则你机器上任何 Claude Code 会话都会落进你的捕获里（而且一旦停掉 `mitmweb`，会话就无法工作）。

**4. 验证**：启动一个新的 `claude` 会话，随便发点什么，确认 mitmweb 里出现了一个 `POST /v1/messages` 流量。

**5. 作业完成后**：做完后，删除该仓库的 `.claude/settings.json`（或其中的 `env` 块），并停掉 `mitmweb`。

### 第一部分：捕获一次会话（15 分）

在代理下运行**一次**满足全部四项要求的会话：

1. **多文件**：至少触及两个文件。
2. **至少失败一次**：你需要一段错误恢复过程。故意弄坏一个测试是获得它的可靠办法。
3. **长到需要规划**：智能体应当做出明确的规划，而不是只发一次工具调用：任务清单、计划模式，或一个计划文件。
4. **你自己的仓库**：一个临时项目，不是本仓库。

**任务点子**，如果你不想自己想：

- 删掉一个其他模块会导入的函数，然后让 Claude 在测试通过的前提下恢复完整功能。
- 给一个小型 Web 应用加一个端点加测试，然后让它在某个你没安装的依赖版本上让测试套件通过。
- 重命名一个模块并让它更新每一处导入，然后运行 lint 与测试。
- 要一个需要用到陌生库的功能，迫使智能体在写任何东西之前先去查 API。

在 mitmweb 界面中，选中一个 `POST /v1/messages` 流量，把**请求体**下载为 JSON。把这些文件保存在本地。你不需要提交它们，但后面每一部分的评分都基于从中提取的证据，所以要保留足够支撑你答案的内容。

如果你的 mitmweb 会话终止了，你可以从保存的 `session.flows` 文件继续工作：用 `mitmweb -r session.flows` 重新打开它。

#### ⚠️ 引用前先脱敏

你的捕获里包含你自己的源代码、文件路径与凭据。除了你在 `writeup.md` 中有意引用的片段之外，其中任何内容都不应进入仓库。

- 绝不要粘贴原始流量或 HTTP 头，因为 `x-api-key` / `authorization` 就在那里。
- **请求体也可能包含密钥。** 智能体读过的任何东西（`.env`、配置文件、命令输出）都会在 `messages` 里重现。引用工具返回结果之前先检查。
- 让 `session.flows` 远离每一个 git 仓库。
- 在你的引文中用可见标记（`[REDACTED: 内部主机名]`）遮蔽隐私内容，而不是悄悄删掉。
- 如果某段引文无法在保留其含义的前提下脱敏，就在一个一次性仓库上重新捕获。

### 第二部分：为系统提示词做注解（25 分）

把 `system` 块以及任何 `role: "system"` 的消息拆成各自的段落。对每一段回答：**它在换来什么行为，它在防御什么失效模式？** 这是注解，不是摘要。

至少要覆盖：

- **结构**：主要段落、它们的顺序，以及为什么是这个顺序。
- **语气与篇幅**：控制回答长度与格式的具体措辞，以及为什么值得花这些 token。
- **何时不该行动**：破坏性操作的闸门、范围限制、拒绝条件。
- **环境上下文**：智能体被告知了关于机器、仓库与会话的什么信息，以及这些信息在请求中的什么位置。

然后，专门针对 `<system-reminder>`：它们出现在哪里（system 块、messages，还是两者都有，并引用一个例子），你能举出证据的两种不同用途是什么，以及为什么要在对话中途注入它们，而不是一开始就讲一次？

### 第三部分：为工具设计做注解（25 分）

**清点：要数字，不要散文。** 当时有多少工具可用，按内置／MCP 提供／延迟加载可搜索来分？指出工具集在各次请求之间发生的任何变化，以及是什么触发了它。好的答案读起来像*「第一次请求里有 117 个工具：35 个内置，82 个来自三个 MCP 服务器」*，而不是*「当时有很多工具可用」*。

**设计分析。** 挑**两个**工具，各自作为接口设计来分析：

- 复现 schema 中的相关部分。
- 为什么是这套参数？什么是必填、什么是选填、什么被刻意不暴露？
- 这个描述在防御什么？一个成熟智能体里的工具描述，大部分是累积起来的疤痕组织。找出那种只因为模型老是做错某件事才存在的句子，并说出那件错事是什么。
- 这个工具刻意**不**做什么，这对周边系统意味着什么？

挑两个有差异的工具。两个文件操作工具是很弱的选择；一个文件工具配一个编排工具、或配一个有异常失败契约的工具，才是强的选择。

### 第四部分：带证据的行为分析（25 分）

用你自己的 trace 回答每个问题。每个答案都必须**引用其证据**（哪次请求、消息索引、工具调用），并**自我标注 `[OBSERVED]` 或 `[INFERRED]`**：observed 意味着你能在捕获里把它指出来，inferred 意味着你在依据定义推理、而并未亲眼看到它发生。两者都可以；标错不行，未标注的答案不得分。

- **错误恢复**：把一个失败从头到尾走一遍。智能体看到了什么，接下来试了什么，恢复用了几轮？逐字引用。
- **规划**：来自一个工具、一条提示词指令、涌现行为，还是几者的组合？什么证据能把这些区分开？
- **计划与任务状态**：它是如何被创建并推进的？每一轮模型能看到关于任务状态的什么信息，而这些信息在请求中的什么位置？
- **子智能体**：智能体何时委派？子智能体被告知了什么，又返回了什么？（如果你的会话从未触发过，一个诚实的 `[INFERRED]` 就足够了。）
- **上下文管理**：随着会话增长，载荷里发生了什么变化？更早的轮次在后续是如何被表示的？

### 第五部分：反思（10 分）

最多一页：**你会照搬的两个决策**以及各自解决了什么问题；**一个你会做得不同的**，并探讨它为什么可能被那样设计；以及**这次 trace 改变了的**一件事 —— 关于你今后日常会如何驾驭编码智能体。

### 交付物

一份填写了所有 `TODO` 的 **`week1/writeup.md`**。你捕获的 trace 留在你自己机器上。

### 评分标准（总分 100 分）

| 部分 | 分值 | 怎样拿到满分 |
|---|---|---|
| 一、捕获与可复现性 | 15 | 四项会话要求全部满足；环境配置与会话记录详细到能仅凭你的报告复现 |
| 二、系统提示词注解 | 25 | 各段落与行为及失效模式挂钩；`<system-reminder>` 用引用的例子解释清楚 |
| 三、工具清点与设计 | 25 | 给出带分类的具体数字；两个真正不同的工具按接口设计做了分析 |
| 四、行为分析 | 25 | 每个答案都引用并正确标注；错误恢复逐字引用 |
| 五、反思 | 10 | 给出具体、有论证的立场，而不是复述 |

以下情况扣分：引用的片段里有未脱敏的凭据；以及把你的 trace 并不支持的说法当作观察来呈现。

### 提交说明

1. 确保你已把所有改动推送到用于评分的远程仓库。
2. **确保你已把 `mihail911`、`isaackann` 与 `vdaita` 添加为你作业仓库的协作者。**
3. 通过 Gradescope 提交。
4. **别忘了从你仓库的 `.claude/settings.json` 里移除 `ANTHROPIC_BASE_URL`！**

```
