---
source_file: "data/fetched/reactjs.org/error-decoder-2ccbc8e1.html"
origin_url: "https://reactjs.org/docs/error-decoder.html?invariant="
title: "#undefined"
extract_method: "html"
extract_warnings:
  - "AGGRESSIVE_STRIP_REVERTED：按关键词剥离 1 个区块后正文下降 100.0%（>40%），已全部加回，避免剥掉正文。该页结构特殊，建议人工抽查。"
src_sha256: "441514060073510b3e60224e66c3fa87412502b6a3b133a4ff574c764297994d"
chars: 618
code_blocks: 0
tables: 0
links: 3
garbage_rate: 0.1667
heading_levels_seen:
  h1: 1
---

[Learn React](/learn)

Copy pageCopy

Minified Error Decoder

# #undefined

In the minified production build of React, we avoid sending down full error messages in order to reduce the number of bytes sent over the wire.

We highly recommend using the development build locally when debugging your app since it tracks additional debug info and provides helpful warnings about potential problems in your apps, but if you encounter an exception while using the production build, the error message will include just a link to the docs for the error.

For an example, see:

[https://react.dev/errors/149.](/errors/149)

---
