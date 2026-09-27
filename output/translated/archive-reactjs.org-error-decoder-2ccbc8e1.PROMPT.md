# 翻译留痕：archive-reactjs.org-error-decoder-2ccbc8e1

- doc_id：`archive-reactjs.org-error-decoder-2ccbc8e1`
- 时间：2026-09-27T16:06:24+08:00
- 原文：`extracted/archive-reactjs.org-error-decoder-2ccbc8e1.md`
- 译文：`translated/archive-reactjs.org-error-decoder-2ccbc8e1.md`
- 原文 sha256：`e9fb9deeb968d0834f1fe60609a9ca1a4953da869c1c932d6cc292f151c2be10`
- 译文 sha256：`01dbd28747375d8252a8077b054cb0989f2f70526d3d6bf6c1682ab51935a44f`
- 术语约束条数：1

## 一、本文档涉及的术语清单

| 英文 | 译法 | handling | 出现次数 |
|---|---|---|---|
| `debugging` | 调试 | `translate` | 1 |

## 二、落盘校验结果

```json
{
  "non_empty": true,
  "code_blocks_total": 0,
  "code_blocks_in_translation": 0,
  "code_blocks_match": true,
  "code_blocks_byte_identical": true,
  "urls_orig": 1,
  "urls_trans": 1,
  "urls_all_present": true,
  "urls_counts_equal": true,
  "headings_orig": 1,
  "headings_trans": 1,
  "headings_match": true,
  "orig_chars": 517,
  "trans_chars": 212,
  "length_ratio": 0.4101,
  "length_ratio_ok": true
}
```

## 四、发出的 prompt 全文

```markdown
# 翻译任务：archive-reactjs.org-error-decoder-2ccbc8e1

## 一、文档元数据

- doc_id：`archive-reactjs.org-error-decoder-2ccbc8e1`
- title：A#undefined
- origin_url：https://reactjs.org/docs/error-decoder.html?invariant=
- 本段字符数：622

## 二、术语约束（本文档用到的，必须严格遵守）

| 英文 | 处理方式 | 出现次数 |
|---|---|---|
| `debugging` | 翻译为「调试」 | 1 |

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


[Learn React](/learn)

Copy pageCopy

Minified Error Decoder

# A#undefined

In the minified production build of React, we avoid sending down full error messages in order to reduce the number of bytes sent over the wire.

We highly recommend using the development build locally when debugging your app since it tracks additional debug info and provides helpful warnings about potential problems in your apps, but if you encounter an exception while using the production build, the error message will include just a link to the docs for the error.

For an example, see:

[https://react.dev/errors/149.](/errors/149)

---

````

## 五、输出要求

直接给出译文，用 ``` 包裹便于复制。**不要**输出任何解释、前言或后记。

```

## 五、AI 返回的译文全文

```markdown
React 错误解码器

复制页面

# #undefined

在 React 的压缩生产构建中，我们不会下发完整的错误信息，以减少通过网络传输的字节数。

我们强烈建议在本地调试应用时使用开发构建，因为它会记录额外的调试信息，并针对应用中的潜在问题给出有用的警告；但如果你在使用生产构建时遇到异常，错误信息中只会包含一个指向该错误文档的链接。

示例见：

[https://react.dev/errors/149。](/errors/149)

---

```
