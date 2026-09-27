[跳到内容](#start-of-content)

[跳到侧边栏](#sidebar)

[/](https://github.com)

[博客](https://github.blog/)

[试用 GitHub Copilot](https://github.com/features/copilot?utm_source=blog-tap-nav&utm_medium=blog&utm_campaign=universe25)

[看看有什么新东西](https://github.com/events/universe/recap?utm_source=k2k-blog-tap-nav&utm_medium=blog&utm_campaign=universe25)

搜索

[首页 /](https://github.blog/)

[开发者技能 /](https://github.blog/developer-skills/)

[GitHub](https://github.blog/developer-skills/github/)

## 如何高效做代码审查：一位 GitHub 主任工程师的理念

GitHub 主任工程师 Sarah Vessels 讨论她的代码审查理念、好的代码审查与差的差在哪里、她寻找与审查代码的策略，以及如何从别人对她代码的审查中获得最大价值。

![](https://github.blog/wp-content/uploads/2024/05/Collaboration-LightMode-2-1.png?resize=1200%2C630)

[Sarah Vessels·](https://github.blog/author/cheshire137/)

[@cheshire137](https://github.com/cheshire137)

July 23, 2024

|

 16 分钟

- 分享：
- https://x.com/share?text=How%20to%20review%20code%20effectively%3A%20A%20GitHub%20staff%20engineer%E2%80%99s%20philosophy&url=https%3A%2F%2Fgithub.blog%2Fdeveloper-skills%2Fgithub%2Fhow-to-review-code-effectively-a-github-staff-engineers-philosophy%2F
- https://www.facebook.com/sharer/sharer.php?t=How%20to%20review%20code%20effectively%3A%20A%20GitHub%20staff%20engineer%E2%80%99s%20philosophy&u=https%3A%2F%2Fgithub.blog%2Fdeveloper-skills%2Fgithub%2Fhow-to-review-code-effectively-a-github-staff-engineers-philosophy%2F
- https://www.linkedin.com/shareArticle?title=How%20to%20review%20code%20effectively%3A%20A%20GitHub%20staff%20engineer%E2%80%99s%20philosophy&url=https%3A%2F%2Fgithub.blog%2Fdeveloper-skills%2Fgithub%2Fhow-to-review-code-effectively-a-github-staff-engineers-philosophy%2F

作为 GitHub 的主任工程师，

[代码审查是我日常工作中的一个主要关注领域。过去八年里，我审查了超过 7,000 个拉取请求。为什么这么多？因为代码审查对构建好软件至关重要，而另一双眼睛往往能发现你本来会漏掉的问题。](https://github.com/features/code-review)

我把代码审查看作工作中最重要的方面之一。事实上，每当看到队友有一个拉取请求已准备好接受代码审查时，我宁愿放下自己正在做的分支，去审查他们提出的改动。毕竟，他们的拉取请求已经通过了持续集成（CI）的重重关卡，也达到了他们自己心中「完成」的标准，所以它大概比我手上未完成的工作更接近可交付状态。我宁愿把他们的代码送过终点线，也不愿为了完成自己的代码再多耗费不确定的时间。

我越早给出反馈 ——「这里可能是 nil，会导致报错」、「这看起来是个 n+1 查询」、「这里最好有个方法签名」—— 反馈就能越快被处理，缺陷越快被消灭、功能越快被交付。

我想分享一下我如何处理代码审查，希望我们都能交付更好的代码。

# [什么是代码审查？](#what-is-code-review)

严格来说，代码审查 —— 通过

[GitHub 上的拉取请求审查 —— 让协作者可以评论拉取请求中提出的改动、表示他们对这些改动的批准，或在拉取请求合并前要求进一步修改。](https://docs.github.com/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/about-pull-request-reviews)

我把拉取请求看作一场对话的开端。我把它读作作者在说「我认为这比我们今天已有的东西更好」。代码审查是塑造产品实现方式的绝佳机会。作为代码审查者，我的职责是与作者来回讨论，通过提问、质疑假设，以及总体上充当另一双眼睛，来改进他们的代码。

## [微调你的代码审查流程](#fine-tune-your-code-review-process)

### [如何找到待审查的拉取请求](#how-to-find-pull-requests-for-review)

我就住在我的

[GitHub 通知收件箱里。它是我浏览器里仅有的几个固定标签页之一，所以随时可用。每当我等 CI、处在任务间隙、刚开始一天的工作，或者只是有片刻空闲时，我都喜欢看一眼收件箱。我审查的大多数拉取请求都是在那里找到的。GitHub 的各个团队往往有一个特定的 Slack 频道作为大本营，那是分享「已可审查」拉取请求的好地方 —— 这也是我发现拉取请求的另外主要途径之一。](https://github.com/notifications?query=is:unread)

我使用

[GitHub 的 Slack 集成把一个 Slack 频道订阅到我团队相关的新拉取请求，效果也不错。为了筛选哪些拉取请求会出现在 Slack 里，我用一个团队专属标签，然后在 Slack 里用 `subscribe` 命令，例如 `/github subscribe your/repo pulls +label:"your-team-label"`。](https://slack.github.com/)

我喜欢用这样的查询来搜索可能需要审查的未决拉取请求：`is:open archived:false is:pr org:github -is:draft team-review-requested:github/relevant-codeowner-team`。用这个查询，我能找到

[处于](https://docs.github.com/search-github/searching-on-github/searching-issues-and-pull-requests#search-by-open-or-closed-state)

[未归档](https://docs.github.com/en/search-github/searching-on-github/searching-issues-and-pull-requests#search-based-on-whether-a-repository-is-archived)

[的拉取请求](https://docs.github.com/en/search-github/searching-on-github/searching-issues-and-pull-requests#search-only-issues-or-pull-requests)

[，它们在 GitHub 组织内、非](https://docs.github.com/en/search-github/searching-on-github/searching-issues-and-pull-requests#search-within-a-users-or-organizations-repositories)

[草稿状态，并且](https://docs.github.com/search-github/searching-on-github/searching-issues-and-pull-requests#search-for-draft-pull-requests)

[把相关 codeowner 团队列为被请求的审查者。我通常会省略](https://docs.github.com/search-github/searching-on-github/searching-issues-and-pull-requests#search-by-pull-request-review-status-and-reviewer)

[`review:required` 搜索限定符，因为即使队友已经审查过，我仍然有兴趣审查这个拉取请求。毕竟，审查代码不仅帮助作者，也帮助我跟上影响我所负责代码的改动。](https://docs.github.com/search-github/searching-on-github/searching-issues-and-pull-requests#search-by-pull-request-review-status-and-reviewer)

### [用审查者团队来管理通知](#use-reviewer-teams-to-manage-notifications)

你不会希望代码改动去 ping 一个太大的团队，以至于团队里每个人都认为审查这个改动不是自己的

[责任。这可能导致拉取请求要么无人审查地搁置，要么在本该合并之前就被合并 —— 因为关键审查者在一大堆通知里错过了它。这两种情况都会影响产品质量。](https://en.wikipedia.org/wiki/Diffusion_of_responsibility)

如果可能，我建议精简你所在的

[code owner 团队数量，让你的通知保持在可管理的规模。这样，落进你收件箱的拉取请求就不只是噪声，而是你确实觉得该审查的东西。虽然庞大、什么都包的 code owner 团队作为兜底选项还可以，但作为自动审查请求的第一道默认并不好。把仓库的 CODEOWNERS 文件组织好，并配上定义清晰的代码边界，以限制通知量、帮助审查者避免通知疲劳。](https://docs.github.com/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)

限制基于团队的通知的另一种方式，是创建一个「第一响应者」团队，然后用自动化按排班来增删团队成员。这能让你的团队专注于日常的代码库，而排班的第一响应者则接收你团队服务区域内的拉取请求通知。例如，使用

[PagerDuty API，你可以确定某一天谁是第一响应者。然后你可以用](https://developer.pagerduty.com/api-reference/3f03afb2c84a4-get-a-schedule)

[Octokit 库来增删团队成员。](https://docs.github.com/rest/using-the-rest-api/libraries-for-the-rest-api?apiVersion=2022-11-28#official-github-libraries)

### [用自动化在各团队间统一代码审查](#standardize-code-reviews-across-teams-with-automation)

仓库级的配置与自动化，例如使用

[CODEOWNERS 文件与](https://docs.github.com/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners#codeowners-file-location)

[分支保护规则，有助于在各团队间强制执行审查流程标准。而其他标准，比如在拉取请求里什么值得评论，就必须由我们人类来维持。把你们团队内部代码审查如何运作写下来，确保任何提供代码审查或提交拉取请求的人都知道：如何让自己的拉取请求得到审查、预期的审查周转时间，以及有哪些自动化在辅助审查。](https://docs.github.com/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/managing-a-branch-protection-rule)

一些团队用项目看板来跟踪有哪些拉取请求进来待审；我见过这在管理共享 API 的团队里效果不错 —— 这类区域经常被团队之外的人修改。其他团队只依赖 GitHub 通知，我见过这在代码所有权界定得很紧、且团队能自律地随到随审时效果不错。

如果你遵循的是自己团队特有的流程，自动化能帮助向团队之外的人传达预期。例如，如果有很多其他团队依赖你们团队的审查，你可以用一个机器人自动在任何请求你们团队审查的拉取请求上留言，告诉作者大概什么时候能收到回复。

## [什么让代码审查变好或变差？](#what-makes-a-code-review-good-or-bad)

好的代码审查带来清晰度，并把代码推向比起点更好的状态。

作为审查者，沟通清晰是关键。你要让人清楚哪些评论是个人偏好、哪些是批准前的阻塞项。把你建议的做法给出示例，会提升你的代码审查、让意思更清楚。如果你能从该拉取请求所在的同一个仓库里给出示例，那就更好 —— 这通过鼓励实现方式的一致性，进一步支持了你的建议。

相比之下，糟糕的代码审查缺乏清晰度。例如，不做任何评论的一揽子批准或拒绝，会让拉取请求作者怀疑这次审查是否真的彻底。即便是仅仅在批准时复述你对作者意图的理解，也能暴露你和作者是否理解一致。

如果一次代码审查没有说清它的建议何时应当落实，对作者来说也会是糟糕的体验。指出既有、未改动的代码该重构，或某个额外情况该处理，这没问题，但重要的是要说明这些是不是批准的前置条件。如果这个拉取请求没有你的建议也可以合入，一定要说出来。保留一个小的 diff、把那些改动作为独立拉取请求单独交付，可能更稳妥。

下面这条代码审查评论展示了具体性，并清楚地传达了建议的实现方式：

「我看到你新写的方法与这个文件里既有风格一致，接受了 [X] 个参数。参数这么多会损害可读性，也意味着这个函数做得太多了。你觉得在后面某个拉取请求里重构这个方法以及既有的那些方法、减少它们接受的参数数量，怎么样？」

这条评论好在哪里：

- 给出了具体细节。
- 引用了具体的代码或问题。
- 给出了问题的解决方向。
- 引用了证据或提供了解释

在光谱的另一端，以下是一些本可以更好的审查评论例子：

「我不喜欢这个。」—— 审查者不喜欢什么？他心里有没有一个可以明确说出来的替代方案？

可能的改进：

- 「这一行做的事太多了，我们能不能把它简化以提升可读性？」
- 「我认为这会有性能问题，因为是个 n+1 查询。」
- 「我们能不能用 [首选框架] 的方案，而不是自己写一个实现？」

「这行不通。」—— 为什么这些改动行不通？

可能的改进：

- 「这行不通，因为 [X]，见这个相关问题：[issue 链接]。」
- 「这之前在 [拉取请求链接] 里试过，因为 [X] 没能成功。」
- 「如果你在 [X] 上遇到问题，可以改用 [替代方案] 试试。」

「我认为这修掉了一个缺陷。」—— 我很喜欢这种点名，但是否有额外的上下文，比如一个 issue 链接，能让它更清楚？

可能的改进：

- 「我认为这修掉了 [issue 链接]。」
- 「这是在修 [issue 链接] 里的那个缺陷吗？」
- 「这看起来就是我们遇到过的 [构建失败链接] 那个缺陷。谢谢修复！」

## [如何给出好的代码审查](#how-to-give-a-good-code-review)

### [提问](#ask-questions)

我把拉取请求作者看作对这次改动拥有最多上下文的人。我可以基于自己的经历 —— 在 Ruby on Rails 单体应用、TypeScript，或在高流量数据库上的经验 —— 指出我看到的问题，但我相信作者对我问题的回答。我把他们对具体细节的理解看得比我的更准。

我也很喜欢问涉及代码中假设的问题。他们处理的数据是什么形状？是否存在不符合该形状的数据？代码能妥善应对吗？代码是否资源密集？性能会好吗？作为审查者，我最喜欢的回应是作者提供自动化测试来验证那些场景下的行为。第二喜欢的是实证数据，例如来自我们数据仓库的一次查询，或一张 Datadog 图表，说明为什么那些场景不是问题。

作为拉取请求作者，我很欢迎收到提问。当有人提问时，就给了我空间去解释为什么我对自己的改动有信心，并在必要时引用 issue、查询或图表。这也让我能把自己的知识与经验分享给别人。不仅作者会看到我的回应，其他审查者以及未来可能来追溯某个旧决策上下文的人也会看到。

### [给出肯定](#offer-affirmations)

除了提问，对拉取请求中你认同的部分做出评论也是好做法。这些评论可以表明你读过并理解了被改动的内容，或者你验证了代码中的某个假设。以下是几个例子：

- 「看起来这和本模块其他类里用的模式一致。」
- 「谢谢你为这个加了测试！」
- 「这比之前可读性强多了。」

以我的经验，收到这类评论本身也很愉快。收到代码审查有时让人心力交瘁。当我要应对来自多方的提问与建议时，收到几条不对我提任何要求、而是支持和认可我已投入工作的评论，会是很好的提振。

### [留意偏见与假设](#be-aware-of-biases-and-assumptions)

人很容易让自己对审查对象、或对他们所改代码区域的偏见影响审查。你会习惯某个人在某个领域工作、或具有某种资历，就假定他们知道自己在做什么 —— 但每个人都会犯错。你对改动的关注、你检验他们假设或验证自己假设的提问，能在部署前抓住问题。

我很推崇写测试，因为它们能去掉一部分偏见。当你写一个测试来检查代码是否正确工作时，

[你就不必只听作者的一面之词，你只需看测试是否通过 —— 当然前提是测试本身写对了。😅](https://www.youtube.com/watch?v=NIKAsGC1Iy8)

我也很推崇初级开发者在代码审查中向资深开发者提问，即使他们觉得自己问得傻、或答案显而易见。如果对你来说不明显，那是合理的。对别人来说也同样不明显！把问题问出来，给作者空间把答案写下来，并把这份教育保留给后来的人。

### [批准还是不批准](#to-approve-or-not)

我把自己的审查看作一道能阻止别人改进我们产品的闸门，所以我审慎地使用不予批准。我常常会有个人偏好、并提出我希望作者做的可选改动，但我不会仅凭这些就不予批准。如果我对某人的拉取请求有建议，但他们的拉取请求照原样并不会搞坏生产、不会负面影响用户、也不会造成其他问题，我就会带着这些评论批准它。作者可以选择在合并前处理我的反馈，也可以在另一个分支里跟进。

审查代码时，要记得斟酌你建议的重要性。为了落实你的建议而推迟交付，值得吗？让作者看到你的反馈、做出建议的改动、等 CI、重新审查、部署、最后合并这一整个循环，值得吗？如果缺少某个建议并不会让谁的日子更难过，那就让作者来决定是否改、什么时候改。

[「要求修改（Request changes）」选项会让拉取请求在审查者回来批准之前无法合并。我极少用它，因为它通常显得过于强硬。我相信我的团队知道什么时候该批准一个拉取请求，所以队友的批准可以代替我的。同样，我相信拉取请求作者会尊重并考虑我的反馈，而不是因为别人批准了、我没批准就盲目合并。我大约只有在认为存在紧迫的安全问题、并且担心他们在合并前看不到我的担忧时，才会选择「要求修改」。](https://docs.github.com/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/reviewing-proposed-changes-in-a-pull-request#submitting-your-review)

## [如何从代码审查中获得最大价值](#how-to-get-the-most-out-of-code-reviews)

### [审查你自己的代码](#review-your-own-code)

GitHub 高级软件工程师

[Paul Smith 教会我在请别人审查之前先审查自己的拉取请求，我也建议你这么做。先过一遍，对那些不明显、或如果你在别人拉取请求里看到也会发问的改动，留下行内评论。自审也有助于判断一个拉取请求是否太大、是否适合](https://github.com/paulcsmith)

[拆分。](https://github.blog/2020-05-21-github-protips-tips-tricks-hacks-and-secrets-from-sarah-vessels/)

特别推荐：如果你在意让自己的拉取请求保持小规模，可以用

[lerebear/sizeup-action 自动给拉取请求打上表示其复杂度与规模的标签。](https://github.com/lerebear/sizeup-action)

### [欢迎合并后的审查](#be-welcoming-of-post-merge-reviews)

如果我碰巧在别人有机会审查之前就合并了拉取请求，我仍然欢迎他们的审查。如果我的拉取请求弄坏了什么、或带来了意外后果，在拉取请求上评论几句就留下了那条面包屑轨迹，帮助未来的读者追溯发生了什么！

如果我在一个已合并的拉取请求上收到审查，我会像它在合并之前那样处理反馈。也许是一条评论解释我的视角，也许是额外的拉取请求来迭代我原本交付的代码。也许是开新的 issue 来记录待做的额外工作。

### [使用草稿拉取请求](#use-draft-pull-requests)

创建新拉取请求时，你可以选择把它设为草稿。我大量依赖

[草稿阶段来表示我是否想要审查。例如，如果某个必需的 CI 构建失败了，或者我只是还没做完，我就会让它保持草稿状态。我也倾向于以同样方式理解别人的拉取请求：如果是草稿，我就假定作者还没准备好接受审查。如果它标记为已可供审查，我就假定拿到足够多的批准就是阻止他们部署这个拉取请求的唯一障碍了。](https://docs.github.com/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/changing-the-stage-of-a-pull-request)

草稿状态意味着拉取请求尚未完成，所以在解决合并冲突或处理审查者反馈时，我会把拉取请求移回草稿。如果我必须修改代码，我会先把拉取请求标记为草稿，以免打扰已经审查过它的人。当我把它移回「已就绪」时，GitHub 会给那些审查者发通知，让他们能再看一眼。

### [保持得体](#be-gracious)

「蜂蜜比醋能抓到更多苍蝇」这句话浮现在我脑海。我希望自己的拉取请求得到审查，所以我喜欢回复拉取请求上的评论 —— 尤其是我不同意审查者的时候。即使我不写回复，我也常常用 👍 表示同意、或用 ❤ 表示感谢。

我希望审查者相信他们的建议不会被遗忘，所以我通过评论让他们了解进展。如果我同意他们的建议 —— 例如进一步重构既有代码 —— 我可能会在表示同意的同时，也对在当前这个拉取请求里就做这个改动表示保留。当我在后面的拉取请求里处理了他们的反馈时，我会回来给出链接，让审查者知道他们的反馈没有被忽视。

我也会在后续实现这些建议改动的拉取请求里 @ 他们，并附一句「这处理了 @某某 在 <之前的拉取请求 URL> 里的反馈」。这既为其他读者提供了上下文，也相当于向原审查者致意，把这份想法的功劳给他。

当你兑现了「在后续分支里处理反馈」的承诺，这有助于与审查者建立信任，让他们更放心地批准你未来的拉取请求，因为他们知道你不会把某件事半途丢下。

## [总结](#wrap-up)

代码审查对产品质量的重要性怎么强调都不过分，在 AI 代码生成的时代尤其如此。在我的职业生涯中，有很多次仅仅因为有那第二双眼睛，就抓住了一个缺陷、避免了一次故障。代码审查非常值得投入时间，无论是花在日常审查、理顺流程，还是构建支持它的自动化上。对开发者来说，现在彻底审查拉取请求，比以后去处理一个已经上线到生产的问题，要更快也更少痛苦。

感谢你对代码质量如此在意，愿意读我关于代码审查的理念。你最近查看过

[自己的审查队列吗？也许现在正是把这些想法付诸行动的好时机。](https://github.com/search?q=review-requested:@me+is:open+archived:false&type=pullrequests)

如果你想进一步了解如何在 GitHub 上使用拉取请求审查，请看 GitHub Community 上主任 DevOps 架构师

[Mickey Gousset 与主任 DevOps 架构师](https://github.com/mickeygousset)

[Joshua Johanning 讨论](https://github.com/joshjohanning)

[审查拉取请求的 5 个技巧。](https://github.com/orgs/community/discussions/130771)

---

## 标签：

- [code review](https://github.blog/tag/code-review/)

## 作者

![Sarah Vessels](https://avatars.githubusercontent.com/u/82317?v=4&s=200)

### [Sarah Vessels](https://github.blog/author/cheshire137/)

[@cheshire137](https://github.com/cheshire137)

Staff Software Engineer, GitHub

## 相关文章

![带有「Beginner security tools」字样的题图](https://github.blog/wp-content/uploads/2026/03/GIT850_THUMB_GFB_A-1.png?resize=400%2C212)

[开发者技能](https://github.blog/developer-skills/)

### [GitHub 新手指南：GitHub 安全入门](https://github.blog/developer-skills/github/github-for-beginners-getting-started-with-github-security/)

了解如何用 GitHub Advanced Security 保护你的项目、让它们保持安全。

![Copilot 悬浮在一簇几何立方体旁，场景具装饰性。](https://github.blog/wp-content/uploads/2026/01/generic-copilot-logo-github.png?resize=400%2C212)

[AI 与 ML](https://github.blog/ai-and-ml/)

### [用 Copilot SDK 构建 AI 驱动的 GitHub issue 分诊](https://github.blog/ai-and-ml/github-copilot/building-ai-powered-github-issue-triage-with-the-copilot-sdk/)

了解如何把 Copilot SDK 集成进 React Native 应用以生成 AI 驱动的 issue 摘要，并包含优雅降级与缓存的生産环境模式。

![带有「Intro to GitHub Actions」字样的装饰性题图](https://github.blog/wp-content/uploads/2026/03/GIT829_THUMB_GFB_A.png?resize=400%2C212)

[开发者技能](https://github.blog/developer-skills/)

### [GitHub 新手指南：GitHub Actions 入门](https://github.blog/developer-skills/github/github-for-beginners-getting-started-with-github-actions/)

在这篇操作指南里配置你的第一个 GitHub Actions 工作流。

## 我们也做通讯

在我们每两周一次、专为开发者准备的通讯里，发现技巧、技术指南与最佳实践。

你的电子邮箱地址

*

 你的电子邮箱地址

订阅

好的，我希望 GitHub 及其关联方将我的信息用于个性化沟通、定向广告与活动效果分析。详见

[GitHub 隐私声明。](https://github.com/site/privacy)

订阅
