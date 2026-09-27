# 让 AI 在复杂代码库中工作

AI 编码工具在真实的生产代码库上很吃力，这一点似乎已被普遍接受。[斯坦福关于 AI 对开发者生产力影响的研究](https://www.youtube.com/watch?v=tbDDYKRFjhk)发现：

1. AI 工具交付的许多「额外代码」，最终只是在返工上周交付的那些糊弄出来的东西。
2. 编码智能体对新项目或小改动很好用，但在大型成熟代码库里，它们往往会让开发者的生产力**更低**。

普遍的回应介于悲观派的「这永远不会成功」和更克制的「也许等模型更聪明的时候」之间。

在折腾了几个月之后，我发现：**只要拥抱核心的上下文工程原则，用今天的模型就能走得很远**。

这不是又一篇「让生产力提升 10 倍」的宣传。在跟 AI 炒作机器打交道这件事上，[我一向相当克制](https://hlyr.dev/12fa)。但我们无意中摸索出的一些工作流，让我对可能性抱有很大的乐观。我们让 Claude Code 处理了 30 万行的 Rust 代码库、一天之内交付了一周的工作量，并维持了通过专家审查的代码质量。我们使用的这一系列技术，我称之为「**频繁的有意压缩**（frequent intentional compaction）」—— 有意地设计你在整个开发过程中向 AI 输送上下文的方式。

我现在完全确信，AI 用于编码不只是玩具和原型，而是一门极具技术含量的工程手艺。

**视频版**：如果你更喜欢视频，本文基于 [8 月 20 日在 Y Combinator 的一次演讲](https://hlyr.dev/ace)

#### 来自 AI Engineer 的基础语境

AI Engineer 2025 的两场演讲从根本上塑造了我对这个问题的思考。

第一场是 [Sean Grove 关于「规格说明即新代码」的演讲](https://www.youtube.com/watch?v=8rABwKRsec4)，第二场是[斯坦福关于 AI 对开发者生产力影响的研究](https://www.youtube.com/watch?v=tbDDYKRFjhk)。

Sean 主张我们**凭感觉写代码的方式都搞错了**。和一个 AI 智能体聊上两小时、说明你想要什么，然后把所有提示词都扔掉、只提交最终代码……这就像一个 Java 开发者编译出 JAR、把编译产物提交进仓库，却把源代码扔了。

Sean 提出，在 AI 的未来，规格说明将成为真正的代码。两年后，你打开 IDE 里的 Python 文件的频率，大约会跟今天你打开十六进制编辑器去读汇编差不多（对我们大多数人来说，就是从不）。

[Yegor 关于开发者生产力的演讲](https://www.youtube.com/watch?v=tbDDYKRFjhk)处理的是一个正交的问题。他们分析了 10 万名开发者的提交，发现（除其他之外）：

1. AI 工具常常导致大量返工，削弱了人们感知到的生产力提升

<img width="2008" height="1088" alt="image" src="https://github.com/user-attachments/assets/f7cec497-3ee2-47d1-8f91-a18210625e19" />

2. AI 工具对全新项目效果好，但对存量代码库与复杂任务往往适得其反

<img width="1326" height="751" alt="Screenshot 2025-08-29 at 10 55 32 AM" src="https://github.com/user-attachments/assets/06f03232-f9d9-4a92-a182-37056bf877a4" />

这与我与创始人交流时听到的一致：

* 「太多糊弄出来的东西了。」
* 「技术债工厂。」
* 「在大仓库里不工作。」
* 「对复杂系统不工作。」

关于 AI 编码处理难题的普遍氛围往往是

> 也许某天，当模型更聪明的时候……

甚至连 [Amjad](https://x.com/amasad) 也在 [9 个月前的 lenny 播客](https://www.lennysnewsletter.com/p/behind-the-product-replit-amjad-masad)上说过，产品经理用 Replit 智能体做新东西的原型，然后交给工程师去实现到生产环境。
（免责声明：我最近没跟上他（好吧，从来没跟上过），这个立场可能已经变了）

每当我听到「也许某天等模型变聪明」，我一般会跳起来说：**这正是上下文工程的意义所在** —— 从**今天**的模型里榨出最大价值。

#### 今天实际能做到什么

我稍后会深入讲这一点，但为证明这不只是理论，让我勾勒一个具体的例子。几周前，我决定在一门处理 LLM 的编程语言 [BAML](https://github.com/BoundaryML/baml) 上测试我们的技术，那是一个 30 万行的 Rust 代码库。我顶多算个业余 Rust 开发者，此前从未碰过 BAML 的代码库。

大约一小时内，我就有了一个[修复缺陷的 PR](https://github.com/BoundaryML/baml/pull/2259#issuecomment-3155883849)，第二天早上就被维护者批准了。几周后，[@hellovai](https://x.com/hellovai) 和我结对向 BAML 交付了 3.5 万行代码，加入了[取消支持](https://github.com/BoundaryML/baml/pull/2357)与 [WASM 编译](https://github.com/BoundaryML/baml/pull/2330) —— 团队估计这两个功能各需一位资深工程师 3-5 天。我们在约 7 小时内把两个草稿 PR 都准备好了。

再次强调，这一切都建立在一种我们称为[频繁的有意压缩](#what-works-even-better-frequent-intentional-compaction)的工作流之上 —— 本质上就是围绕上下文管理来设计你整个开发过程，把利用率保持在 40-60% 区间，并在恰到好处的节点嵌入高杠杆的人工审查。我们用「研究、计划、实现」的工作流，但这里的核心能力／心得，远比任何具体工作流或提示词组合更具普遍性。

#### 我们走到这一步的古怪历程

我曾与一位我见过的最多产的 AI 编码者共事。
每隔几天，他们就会丢出 **2000 行的 Go PR**。
而且这不是什么 nextjs 应用或 CRUD API。这是复杂的、[容易出竞态的 systems 代码](https://github.com/humanlayer/humanlayer/blob/main/hld/daemon/daemon_subscription_integration_test.go#L45)：通过 unix socket 走 JSON RPC，并管理从 fork 出来的 unix 进程（大多是 claude code sdk 进程，这个稍后再说 🙂）流式输出的 stdio。

每隔几天就仔细读 2,000 行复杂 Go 代码，这个想法根本不可持续。我开始有点体会 Mitchell Hashimoto 当年为 ghostty 加上[「AI 贡献必须披露」](https://github.com/ghostty-org/ghostty/pull/8289)规则时的心情了。

我们的做法是采纳类似 Sean 的**规格驱动开发**。

一开始很不舒服。
我必须学会放下「逐行读 PR 代码」的习惯。
我仍然相当仔细地读测试，但规格说明成了我们关于「在构建什么、为什么」的事实来源。

这个转变花了大约 8 周。
对所有参与者来说都极其不适，尤其对我。
但我们现在飞起来了。几周前，我一天交付了 6 个 PR。
过去三个月里，我手工编辑非 markdown 文件的次数，一只手数得过来。

### 面向编码智能体的高级上下文工程

我们需要的是：

* 在存量代码库里也好用的 AI
* 能解决复杂问题的 AI
* 不糊弄（No Slop）
* 让全团队保持认知对齐

（当然，还要尽可能多烧 token。）

我会深入讲：

1. 我们把上下文工程应用到编码智能体上学到了什么
2. 使用这些智能体是一门极具技术含量的手艺，体现在哪些维度上
3. 我为什么认为这些做法不可通用化
4. 关于第 (3) 点，我被反复证明错了多少次

#### 但首先：管理智能体上下文的朴素方式

我们大多数人一开始把编码智能体当聊天机器人用。你和它来回聊（或者[醉醺醺地喊](https://ghuntley.com/six-month-recap/#:~:text=Last%20week%2C%20over%20Zoom%20margaritas%2C%20a%20friend%20and%20I%20reminisced%20about%20COBOL.)），凭感觉把一个问题的路走完，直到要么上下文用完、要么你放弃、要么智能体开始道歉。

<img width="7718" height="4223" alt="image" src="https://github.com/user-attachments/assets/7361a203-9d95-42e2-ac16-1f38b04adb58" />

稍微聪明点的做法是：一旦跑偏就重来，丢掉当前会话、开一个新的，也许在提示词里多加点引导。

> [原始提示词]，但要确保你用 XYZ 方案，因为 ABC 方案行不通

<img width="7727" height="4077" alt="image" src="https://github.com/user-attachments/assets/1bbbc8ad-60da-4f8b-98c3-e6603b04a0ce" />

#### 稍微再聪明点：有意的压缩

你很可能做过一件我称之为「有意的压缩」的事。无论有没有跑偏，当上下文开始被填满时，你大概都想暂停工作、用一个全新的上下文窗口重开。为此，你可能会用这样的提示词：

> 「把我们目前为止做的一切都写到 progress.md，务必注明最终目标、我们采用的做法、至今完成的步骤，以及我们当前正在处理的那个失败」

<img width="7309" height="4083" alt="image" src="https://github.com/user-attachments/assets/64b940e5-89b1-4f6c-a79c-ec2810d9af77" />

你也可以[用提交信息来做有意的压缩](https://x.com/dexhorthy/status/1961490837017088051)。

#### 我们到底在压缩什么？

是什么在吃掉上下文？

* 搜索文件
* 理解代码流程
* 应用编辑
* 测试／构建日志
* 来自工具的巨型 JSON 块

这些都会淹没上下文窗口。**压缩**就是把它们蒸馏成结构化的产物。

一次好的有意压缩，输出可能类似这样

<img width="1309" height="747" alt="Screenshot 2025-08-29 at 11 10 36 AM" src="https://github.com/user-attachments/assets/a7d5946d-4e81-46e8-b314-d02dae1f00ee" />

#### 为什么要死磕上下文？

正如我们在 [12-factor agents](https://hlyr.dev/12fa) 里深入讨论过的，LLM 是无状态函数。在不训练／微调模型本身的前提下，唯一影响输出质量的东西，就是输入的质量。

这对[驾驭](https://www.youtube.com/watch?v=F_RyElT_gJk)编码智能体同样成立，就像它对通用智能体设计成立一样，只是你的问题空间更小，而且我们谈的不是构建智能体，而是使用智能体。

在任何给定的时刻，像 claude code 这样的智能体的一「轮」，都是一次无状态的函数调用。上下文窗口进，下一步出。

<img width="7309" height="4083" alt="image" src="https://github.com/user-attachments/assets/c1e920e8-5dc5-4dd2-b76d-853b85a92e6a" />

也就是说，你的上下文窗口里的内容，是你影响输出质量的**唯一**杠杆。所以是的，它值得死磕。

你应当为以下目标优化你的上下文窗口：

1. 正确性
2. 完整性
3. 规模
4. 轨迹

换个说法，你的上下文窗口可能遭遇的最糟情况，按严重程度排序是：

1. 信息不正确
2. 信息缺失
3. 噪声太多

如果你喜欢公式，这里有一个你可以参考的（很粗糙的）公式：

<img width="1320" height="235" alt="Screenshot 2025-08-29 at 11 11 30 AM" src="https://github.com/user-attachments/assets/a6ea98a6-665b-48af-983b-a1cb2c45e44c" />

正如 [Geoff Huntley](https://x.com/GeoffreyHuntley) 所说，

> 这个游戏的关键在于，你只有大约 **170k 的上下文窗口**可用。
> 所以尽可能少用它至关重要。
> 你用掉的上下文窗口越多，得到的结果就越差。

Geoff 对这个工程约束的解法，是一种他称为 [Ralph Wiggum 作为软件工程师](https://ghuntley.com/ralph/)的技术，基本上就是用一条简单的提示词把智能体放进一个 while 循环里永远跑下去。

```
while :; do
  cat PROMPT.md | npx --yes @sourcegraph/amp
done
```

如果你想进一步了解 ralph 或 PROMPT.md 里有什么，可以看 Geoff 的文章，或者深入了解 [@simonfarshid](https://x.com/simonfarshid)、[@lantos1618](https://x.com/lantos1618)、[@AVGVSTVS96](https://x.com/AVGVSTVS96) 和我在上周末 YC Agents Hackathon 上构建的项目 —— 它（大体上）[在一夜之间把 BrowserUse 移植到了 TypeScript](https://github.com/repomirrorhq/repomirror/blob/main/repomirror.md)

Geoff 把 ralph 形容为对上下文窗口问题一个「蠢得好笑」的解法。[我不完全确定它蠢](https://ghuntley.com/content/images/size/w2400/2025/07/The-ralph-Process.png)。

#### 回到压缩：使用子智能体

子智能体是管理上下文的另一种方式，通用子智能体（即非[自定义](https://docs.anthropic.com/en/docs/claude-code/sub-agents)的）从早期起就一直是 claude code 与许多编码 CLI 的功能。

子智能体不是为了[玩过家家、把角色拟人化](https://x.com/dexhorthy/status/1950288431122436597)。子智能体是为了控制上下文。

子智能体最常见、最直接的用例，是让你用一个全新的上下文窗口去做查找／搜索／总结，从而使父智能体能直奔工作，而不必用 `Glob` / `Grep` / `Read` 等调用把它的上下文窗口搅浑。

https://github.com/user-attachments/assets/cb4e7864-9556-4eaa-99ca-a105927f484d

<details><summary>（手机上看不了视频？展开看静态图版本）</summary>
  <img width="7309" height="4083" alt="image" src="https://github.com/user-attachments/assets/c72e7dba-1476-4ee9-9cb0-0f97d428b82a" />
</details>

理想的子智能体响应，大概与上面那种理想的一次性压缩很像

<img width="1309" height="747" alt="Screenshot 2025-08-29 at 11 10 36 AM" src="https://github.com/user-attachments/assets/a7d5946d-4e81-46e8-b314-d02dae1f00ee" />

让子智能体返回这种结果并不简单：

<img width="7309" height="4083" alt="image" src="https://github.com/user-attachments/assets/2bcd30f6-84fd-4911-ac15-63f75619e76d" />

#### 效果更好的做法：频繁的有意压缩

我想谈、也是我们在过去几个月采纳的技术，都归入我所说的「频繁的有意压缩」。

本质上，这意味着围绕上下文管理来设计你的**整个工作流**，并把利用率保持在 40%-60% 区间（取决于问题的复杂度）。

我们的做法是拆成（大约）三步。

我说「大约」，是因为有时我们会跳过研究直接进入计划，有时我们会在准备好实现之前做多轮压缩后的研究。

下面我会用一个具体例子分享每一步的示例产出。对于某个功能或缺陷，我们倾向于这样做：

**研究（Research）**

理解代码库、与该问题相关的文件、信息如何流动，可能还包括问题的潜在成因。

这是我们的[研究提示词](https://github.com/humanlayer/humanlayer/blob/main/.claude/commands/research_codebase.md)。
它目前用自定义子智能体，但在其他仓库里，我用一个更通用的版本：通过 claude code 的 Task() 工具配 `general-agent`。
通用版本效果几乎一样好。

**计划（Plan）**

列出我们修复该问题将要采取的确切步骤，以及需要编辑哪些文件、怎么编辑，并对每个阶段的测试／验证步骤极其精确。

这是[我们用于计划的提示词](https://github.com/humanlayer/humanlayer/blob/main/.claude/commands/create_plan.md)。

**实现（Implement）**

按阶段逐步走完计划。对复杂工作，我常常在每个实现阶段验证通过后，把当前状态压缩回原来的计划文件。

这是[我们使用的实现提示词](https://github.com/humanlayer/humanlayer/blob/main/.claude/commands/implement_plan.md)。

附带一句 —— 如果你最近听到很多关于 git worktree 的讨论，只有这一步需要在 worktree 里做。其他我们都在 main 上做。

**我们如何管理／共享这些 markdown 文件**

为简洁起见这部分我跳过，但欢迎你在 [humanlayer/humanlayer](https://github.com/humanlayer/humanlayer) 里启动一个 claude 会话，问问「thoughts tool」是怎么工作的。

#### 把它付诸实践

我和 [@vaibhav](https://www.linkedin.com/in/vaigup/) 每周做一次[直播编码](https://github.com/ai-that-works/ai-that-works)，在白板上推演并写代码解决一个高级 AI 工程问题。这是我一周的亮点之一。

几周前，我[决定多分享一些这个过程](https://hlyr.dev/he-gh)，想看看我们内部的技术能不能一次性修好 BAML 那个 30 万行 Rust 代码库的问题 —— BAML 是一门处理 LLM 的编程语言。我从 @BoundaryML 仓库里挑了一个（老实说是偏小的）[缺陷](https://github.com/BoundaryML/baml/issues/1252)就开工了。

你可以[看那一期](https://hlyr.dev/he-yt)了解更多过程，但概括来说：

**值得注意**：我顶多算个业余 Rust 开发者，而且此前从未在 BAML 代码库里工作过。

##### 研究阶段

- 我生成了一份研究报告，读了它。Claude 判定这个缺陷不成立、代码库是对的。
- 我把那份研究扔掉，带着更多引导重新起了一份。
- 这是我[最终采用的那份研究文档](https://github.com/ai-that-works/ai-that-works/blob/main/2025-08-05-advanced-context-engineering-for-coding-agents/thoughts/shared/research/2025-08-05_05-15-59_baml_test_assertions.md)

##### 计划阶段

- 研究还在跑的时候，我等不及了，没等研究就起了一份计划，想看看 claude 能不能直接给出实现计划 —— [你可以在这里看到它](https://github.com/ai-that-works/ai-that-works/blob/main/2025-08-05-advanced-context-engineering-for-coding-agents/thoughts/shared/plans/fix-assert-syntax-validation-no-research.md)
- 研究完成后，我又起了一份利用了研究结果的实现计划 —— [你可以在这里看到它](https://github.com/ai-that-works/ai-that-works/blob/main/2025-08-05-advanced-context-engineering-for-coding-agents/thoughts/shared/plans/baml-test-assertion-validation-with-research.md)

两份计划都相当短，但差异显著。它们以不同方式修复了问题，测试思路也不同。不展开细节的话，它们「本来都能用」，但那份基于研究做出来的，把问题修在了**最合适的地方**，并且规定的测试也符合代码库的惯例。

##### 实现阶段

- 这一切都发生在播客录制的前一晚。我把两份计划并行执行，并在当晚收工前把两个都提交成了 PR。

到第二天太平洋时间上午 10 点我们上节目时，[那份带研究的计划产出的 PR 已经被 @aaron 批准](https://github.com/BoundaryML/baml/pull/2259#issuecomment-3155883849)，而他甚至不知道我在为播客搞个小节目 🙂。我们[关掉了另一个](https://github.com/BoundaryML/baml/pull/2258/files)。

所以我们最初 4 个目标，达成了：

- ✅ 在存量代码库里可用（30 万行 Rust 项目）
- 能解决复杂问题
- ✅ 不糊弄（PR 已合并）
- 保持认知对齐

#### 解决复杂问题

Vaibhav 仍有怀疑，而我想看看我们能不能解决一个更复杂的问题。

于是几周后，我们两人花了 7 小时（3 小时研究／计划，4 小时实现），交付了 3.5 万行代码，为 BAML 加上取消与 wasm 支持。
[取消那个 PR 上周刚合并](https://github.com/BoundaryML/baml/pull/2357)。[WASM 那个还开着](https://github.com/BoundaryML/baml/pull/2330)，但已经有一个可用 demo：在浏览器里从 JS 应用调用 wasm 编译后的 Rust 运行时。

虽然取消那个 PR 还需要一点额外打磨才能达标，但我们在仅仅一天内取得了惊人的进展。Vaibhav 估计这两个 PR 若由 BAML 团队的资深工程师来做，每个都需要 3-5 天。

✅ 所以我们也能解决复杂问题。

#### 这不是魔法

还记得例子里的那部分吗 —— 我读了研究报告、发现它是错的就扔掉了？或者我和 Vaibhav **深度投入地坐了 7 小时**？做这件事时你必须投入你的任务，否则它**不会**奏效。

有某一类人总是在找那条能解决所有问题的神奇提示词。它不存在。

通过研究／计划／实现来做频繁的有意压缩，会让你的表现**更好**，但让它**对难题足够好**的，是你在流水线里嵌入了高杠杆的人工审查。

<img width="7309" height="4083" alt="image" src="https://github.com/user-attachments/assets/01c7818a-9a0d-4ede-a23b-fb0c2e80f843" />

#### 出糗的时候

几周前，[@blakesmith](https://www.linkedin.com/in/bhsmith/) 和我坐下来花了 7 小时，[试图从 parquet java 里移除 hadoop 依赖](https://github.com/dexhorthy/parquet-java/blob/remove-hadoop/thoughts/shared/plans/remove-hadoop-dependencies.md) —— 关于出了什么问题、以及我对原因的理论，我留到另一篇文章。一句话说，它进展不顺。tl;dr 是研究步骤没有足够深入依赖树，并且假定可以把类往上移到上游、而不会引入深层嵌套的 hadoop 依赖。

有些大难题不是你在 7 小时里靠提示词就能趟过去的，我们仍然好奇而兴奋地和朋友与伙伴们一起冲击边界。我认为这里另一个教训是：你大概至少需要一个熟悉该代码库的专家，而在这个案例里，我们俩都不是。

#### 关于人的杠杆

如果这一切你只带走一件事，那就带走这个：

一行糟糕的代码……就是一行糟糕的代码。
但**计划**里一行糟糕的内容，可能导致数百行糟糕的代码。
而**研究**里一行糟糕的内容 —— 对代码库如何工作、或某功能位于何处的误解 —— 可能让你得到数千行糟糕的代码。

<img width="7309" height="4083" alt="image" src="https://github.com/user-attachments/assets/dab49f61-caae-4c15-b481-ee9b8f64995f" />

所以你要把**人的精力与注意力**集中在流水线中杠杆**最高**的部分。

<img width="9830" height="4520" alt="image" src="https://github.com/user-attachments/assets/cf981f70-5e61-4938-aa9a-7dcb88c9f8a4" />

当你审查研究与计划时，你获得的杠杆比审查代码时更大。（顺便一提，我们在 [humanlayer](https://hlyr.dev/code) 的一个主要关注点，就是帮助团队构建并利用高质量的工作流提示词，为 AI 生成的代码与规格说明打造出色的协作工作流）。

#### 代码审查是为了什么？

关于代码审查是为了什么，人们有很多不同看法。

我更偏好 [Blake Smith 在《软件团队的代码审查要点》里的框架](https://blakesmith.me/2015/02/09/code-review-essentials-for-software-teams.html)：他说代码审查最重要的部分是**认知对齐** —— 让团队成员对代码正在如何变化、以及为什么变化保持在同一页上。

<img width="7309" height="4083" alt="image" src="https://github.com/user-attachments/assets/77f4001b-175f-4da6-a6d4-e00b80489476" />

还记得那些 2k 行的 golang PR 吗？我在意它们是否正确、设计是否良好，但团队内部不安与沮丧的最大来源是**缺乏认知对齐**。**我开始对自己产品是什么、如何运作失去感觉。**

我猜想，任何与一位非常多产的 AI 编码者共事过的人都有过这种体验。

这实际上正是研究／计划／实现对我们最重要的部分。
每个人都交付多得多的代码，一个必然的副作用就是：在任何时点，代码库中更大比例的部分对任何一位工程师来说都是陌生的。

我甚至不打算说服你研究／计划／实现是大多数团队的正确答案 —— 它很可能不是。但你**绝对**需要一套工程流程，能够

1. 让团队成员保持在同一页上
2. 让团队成员快速了解代码库中陌生的部分

对大多数团队来说，这就是拉取请求与内部文档。对我们来说，现在是规格说明、计划与研究。

我没法每天读 2000 行 golang。但我**能**读一份写得很好的实现计划的 200 行。

当东西坏掉时，我没法花一小时以上在 40 多个 daemon 代码文件里探险（好吧，我能，但我不想）。我**能**引导一条研究提示词，让它给我一份关于「我该看哪里、为什么」的速通。

#### 回顾

基本上我们得到了需要的一切。

- ✅ 在存量代码库里可用
- ✅ 能解决复杂问题
- ✅ 不糊弄
- ✅ 保持认知对齐

（哦对，我们三人的团队，opus 上平均每月花约 1.2 万美元）

为了让你不觉得我只是又一个[亢奋的、留着八字胡的销售](https://www.youtube.com/watch?v=IS_y40zY-hc&lc=UgzFldRM6LU5unLuFn54AaABAg.AMKlTmJAT5ZAMKrOOAMw3I)，我要说明这对每个问题都不是完美奏效（我们还会再回来的，parquet-java）。

8 月份整个团队花了两周在一个非常棘手的竞态条件上原地打转，最后掉进了 golang 里 MCP sHTTP keepalive 问题以及其他一堆死胡同的兔子洞。

但现在已经成了例外。总体而言，这对我们效果很好。我们的实习生第一天交付了 2 个 PR，第 8 天交付了 10 个。我原本真心怀疑这对别人是否也管用，但我和 Vaibhav 在 7 小时里交付了 3.5 万行可用的 BAML 代码。（如果你没见过 Vaibhav，在代码设计与质量上，他是我认识的最一丝不苟的工程师之一。）

#### 接下来会怎样

我相当确信，编码智能体会被商品化。

难的部分将是团队与工作流的转型。在一个 AI 写出我们 99% 代码的世界里，关于协作的一切都会改变。

而我很强烈地相信，如果你不把这件事搞明白，你会被搞明白的人远远甩在后面。

#### 好吧，显然你有东西要卖给我

我们对规格优先、智能体式的工作流相当看好，所以我们在构建工具让它更容易。在诸多事情中，我痴迷于如何把这些「频繁的有意压缩」工作流在大型团队中协同地规模化。

今天，我们推出 CodeLayer —— 我们新的「后 IDE 时代的 IDE」，进入私募测试 —— 你可以想成「claude code 的 Superhuman」。如果你是 Superhuman 和／或 vim 模式的粉丝，并且准备好超越「凭感觉写代码」、认真用智能体构建，我们很希望你能加入等候名单。

**在 [https://humanlayer.dev](https://humanlayer.dev) 注册**。

### 给开源维护者 —— 我们一起交付点什么

如果你是某个复杂开源项目的维护者、且住在湾区，我的公开提议是：我会在某个周六和你面对面在旧金山结对 7 小时，看看我们能不能交付点大东西。

我能学到很多关于这些技术的局限、以及它们在哪里不够用（运气好的话，还能得到一个已合并、带来大量价值、可以拿来说事的可用 PR）。你能以我发现唯一有效的学习方式学到这套工作流 —— 直接一对一结对。

### 给工程负责人

如果你或你认识的人是工程负责人，想让团队的 AI 生产力提升 10 倍，我们正在与各种规模的团队一起前置部署，帮助推动向 AI 优先的编码世界转型所需的「文化／流程／技术」变革。

#### 致谢

- 感谢所有听我念叨过本文早期啰嗦版本的朋友与创始人 —— Adam、Josh、Andrew，以及更多更多人
- 感谢 Sundeep 陪我熬过这场古怪的风暴
- 感谢 Allison、Geoff 和 Gerred，把我们连踢带喊地拖进未来
