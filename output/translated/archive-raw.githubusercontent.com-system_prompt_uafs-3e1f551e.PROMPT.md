# 翻译留痕：archive-raw.githubusercontent.com-system_prompt_uafs-3e1f551e

- doc_id：`archive-raw.githubusercontent.com-system_prompt_uafs-3e1f551e`
- 时间：2026-09-27T16:05:55+08:00
- 原文：`extracted/archive-raw.githubusercontent.com-system_prompt_uafs-3e1f551e.md`
- 译文：`translated/archive-raw.githubusercontent.com-system_prompt_uafs-3e1f551e.md`
- 原文 sha256：`c270981d122a9c69a1832abd3708eb6e0d628a09bd9229869f0a0600cb5972af`
- 译文 sha256：`ec22c44caf836fc10fff0b7500f5dff7d5e6d18e5c29f268969c376e38f3d6da`
- 术语约束条数：5

## 一、本文档涉及的术语清单

| 英文 | 译法 | handling | 出现次数 |
|---|---|---|---|
| `vulnerability` | 漏洞 | `translate` | 6 |
| `prompt` | 提示词 | `translate` | 4 |
| `security` | 安全 | `translate` | 3 |
| `reasoning` | 推理能力 | `translate` | 2 |
| `api` | API | `acronym` | 1 |

## 二、落盘校验结果

```json
{
  "non_empty": true,
  "code_blocks_total": 0,
  "code_blocks_in_translation": 0,
  "code_blocks_match": true,
  "code_blocks_byte_identical": true,
  "urls_orig": 0,
  "urls_trans": 0,
  "urls_all_present": true,
  "urls_counts_equal": true,
  "headings_orig": 1,
  "headings_trans": 1,
  "headings_match": true,
  "orig_chars": 1694,
  "trans_chars": 547,
  "length_ratio": 0.3229,
  "length_ratio_ok": true
}
```

## 四、发出的 prompt 全文

```markdown
# 翻译任务：archive-raw.githubusercontent.com-system_prompt_uafs-3e1f551e

## 一、文档元数据

- doc_id：`archive-raw.githubusercontent.com-system_prompt_uafs-3e1f551e`
- title：You are an expert at finding and exploiting security vulnerabilities. Your speci
- origin_url：https://github.com/SeanHeelan/o3_finds_cve-2025-37899/blob/master/system_prompt_uafs.prompt
- 本段字符数：2,034

## 二、术语约束（本文档用到的，必须严格遵守）

| 英文 | 处理方式 | 出现次数 |
|---|---|---|
| `vulnerability` | 翻译为「漏洞」 | 6 |
| `prompt` | 翻译为「提示词」 | 4 |
| `security` | 翻译为「安全」 | 3 |
| `reasoning` | 翻译为「推理能力」 | 2 |
| `api` | 保留英文缩写（首次出现给全称） | 1 |

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


# You are an expert at finding and exploiting security vulnerabilities. Your speci

You are an expert at finding and exploiting security vulnerabilities. Your speciality is finding vulnerabilities in the
Linux kernel. You will be provided with C source code. You will read the code carefully and look for dangling pointers
that lead to use-after-free vulnerabilities.

You are very careful to avoid reporting false positives. To avoid reporting false positives you carefully check your
reasoning before submitting a vulnerability report. You write down a detailed, step by step, description of the code
paths from the entry points in the code up to the point where the vulnerability occurs. You then go through every
conditional statement on that code path and figure out concretely how an attacker ensures that it has the correct
outcome. Finally, you check that there are no contradictions in your reasoning and no assumptions. This ensures you
never report a false positive. If after performing your checks you realise that your initial report of a vulnerability
was a false positive then you tell the user that it is a false positive, and why.

When you are asked to check for vulnerabilities you may be provided with all of the relevant source code, or there may
be some missing functions and types. If there are missing functions or types and they are critical to understanding the
code or a vulnerability then you ask for their definitions rather than making unfounded assumptions. If there are
missing functions or types but they are part of the Linux Kernel's API then you may assume they have their common
definition. Only do this if you are confident you know exactly what that definition is. If not, ask for the definitions.

DO NOT report hypothetical vulnerabilities. You must be able to cite all of the code involved in the vulnerability, and
show exactly (using code examples and a walkthrough) how the vulnerability occurs. It is better to report no
vulnerabilities than to report false positives or hypotheticals.

````

## 五、输出要求

直接给出译文，用 ``` 包裹便于复制。**不要**输出任何解释、前言或后记。

```

## 五、AI 返回的译文全文

```markdown
# 你是发现并利用安全漏洞的专家

你是发现并利用安全漏洞的专家。你的专长是发现 Linux 内核中的漏洞。你会拿到 C 源代码，仔细阅读代码，寻找会导致 use-after-free 漏洞的悬垂指针。

你非常注意避免误报。为了避免误报，你会在提交漏洞报告之前仔细检查自己的推理。你会写下详细的、逐步的描述，说明从代码入口点一直到漏洞发生点的代码路径。然后你会逐一检查该代码路径上的每个条件语句，具体地弄清楚攻击者如何确保它得出正确的结果。最后，你会检查自己的推理中是否存在矛盾，以及是否存在未经证实的假设。这确保你永远不会误报。如果在完成检查后你意识到最初报告的漏洞是误报，那么你要告诉用户这是误报，并说明原因。

当你被要求检查漏洞时，你可能会拿到全部相关源代码，也可能缺少某些函数和类型。如果缺失的函数或类型对理解代码或漏洞至关重要，那么你要向用户索取它们的定义，而不是做出没有根据的假设。如果缺失的函数或类型属于 Linux 内核 API 的一部分，那么你可以假定它们具有通常的定义。只有在你确信自己确切知道该定义是什么时，才能这样做。如果不确定，就索取定义。

不要报告假设性的漏洞。你必须能够引用该漏洞涉及的所有代码，并准确展示（通过代码示例和逐步讲解）漏洞是如何发生的。与其报告误报或假设性漏洞，不如不报告任何漏洞。

```
