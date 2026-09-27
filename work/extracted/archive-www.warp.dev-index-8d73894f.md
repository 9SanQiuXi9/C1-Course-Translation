---
source_file: "data/fetched/www.warp.dev/index-8d73894f.html"
origin_url: "https://www.warp.dev/"
title: "Open infrastructure for cloud software factories"
extract_method: "html"
extract_warnings:
  - "STRIPPED_BLOCKS：按 class/id 关键词剥离了 1 个非正文区块（正文下降 0.0%）"
src_sha256: "279da08823ccd7a3ccb3ff018d30964b1497c81d938da6747ccfca02fb26c87f"
chars: 12006
code_blocks: 5
tables: 0
links: 16
garbage_rate: 0.0136
heading_levels_seen:
  h1: 1
  h2: 8
  h3: 6
  h4: 15
---

/

![Warp](/img/logos/warp-pixel-icon-white.svg)

[[S] SDLC](#sdlc)

[[Q] Quality loop](#quality)

[[E] Enterprise](#enterprise-ready)

[[L] Layers](#layers)

[[G] Governance](#governance)

[[W] Warp everywhere](#use-warp-everywhere)

[[F] FAQ](#faq)

[request early access](/factories/request-access)

# Open infrastructure for cloud software factories

build on Warp: factories as code, any model or harness, with evals, benchmarks, and self-improvement built in.

[request early access](/factories/request-access)

[download warp terminal](/download)

get up to $10,000 in free factory usage

>_[ fig. 1 — the factory ]⌗

livefactory.yaml

factory.yamlapplied to all 112 agents

<!-- CODE_BLOCK_START id=c1 lang= -->
```
## factory.yaml

schemaVersion: v1alpha1
name: acme-web
repositories:
  - owner: acme
    name: web
mcpServers:
  github:
    warpId: mcp_github
agentDefaults:
  model: claude-5-fable-high
```
<!-- CODE_BLOCK_END id=c1 -->

trusted by 800k+ devs at

![Asana](/img/logos/trusted-by/asana-black.svg)

![Docker](/img/logos/trusted-by/docker-black.svg)

![GitHub](/img/logos/trusted-by/github-black.svg)

![VMware](/img/logos/trusted-by/vmware-black.svg)

![Amplitude](/img/logos/trusted-by/amplitude-black.svg)

![Teamworks](/img/logos/trusted-by/teamworks-black.svg)

![NVIDIA](/img/logos/trusted-by/nvidia-black.svg)

![Ramp](/img/logos/trusted-by/ramp-black.svg)

SDLC coverage

### Beyond CI/CD to automating the whole SDLC

defined in code, built for scale, and easy to deploy.

01

##### opinionated, but flexible

set up your first factory in 5 minutes, build it out over time.

>_[ fig. 2 · quickstart ]⌗

02

##### factories as code

repos, agents, models, permissions, and checkpoints in one definition.

>_[ fig. 2 · factory.yaml ]⌗

<!-- CODE_BLOCK_START id=c2 lang= -->
```
## factory.yaml — factories as code

schemaVersion: v1alpha1
name: pr-review
repositories:
  - owner: acme
    name: web
agentDefaults:
  model: claude-5-fable-high

## agents/foreman/agent.md

agentType: FOREMAN

## agents/review/agent.md

agentType: REVIEW
model: glm-5.2-fireworks

## automations/on-pr/automation.md

agent: review
triggers:
  - provider: github
    event: pull_request_ready
```
<!-- CODE_BLOCK_END id=c2 -->

03

##### API, CLI, SDK and MCP

built as a platform, not a vertical product or AI teammate.

>_[ fig. 2 · API / CLI / SDK / MCP ]⌗

<!-- CODE_BLOCK_START id=c3 lang= -->
```
## cli

$ warp agent run-cloud --environment ENV_ID \
    --prompt "fix LIN-482, low risk only"

## api

$ curl -X POST https://app.warp.dev/api/v1/agent/runs \
    -H "Authorization: Bearer $WARP_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{ "prompt": "fix LIN-482" }'
{ "run_id": "run_4026", "state": "QUEUED" }

## sdk (typescript)

const run = await client.agent.run({ prompt: 'fix LIN-482' });
console.log(run.run_id);

## mcp · warp-factory server

{ "tool": "send_task", "factory_uid": "fct_acme_web",
  "title": "Fix LIN-482", "note": "low risk only" }
```
<!-- CODE_BLOCK_END id=c3 -->

04

##### integrations

work flows in from chat, tickets, and source control; status flows back to where it started.

>_[ fig. 2 · integrations ]⌗

05

##### any surface

watch, steer, and hand off runs from web, mobile, terminal, or IDE.

>_[ fig. 2 · any surface ]⌗

06

##### evals, self-improvement, and memory

every run is scored; observer agents open PRs against your factory config to improve it.

>_[ fig. 2 · self-improvement ]⌗

>_[ fig. 2 · quickstart ]⌗

>_[ fig. 2 · factory.yaml ]⌗

<!-- CODE_BLOCK_START id=c4 lang= -->
```
## factory.yaml — factories as code

schemaVersion: v1alpha1
name: pr-review
repositories:
  - owner: acme
    name: web
agentDefaults:
  model: claude-5-fable-high

## agents/foreman/agent.md

agentType: FOREMAN

## agents/review/agent.md

agentType: REVIEW
model: glm-5.2-fireworks

## automations/on-pr/automation.md

agent: review
triggers:
  - provider: github
    event: pull_request_ready
```
<!-- CODE_BLOCK_END id=c4 -->

>_[ fig. 2 · API / CLI / SDK / MCP ]⌗

<!-- CODE_BLOCK_START id=c5 lang= -->
```
## cli

$ warp agent run-cloud --environment ENV_ID \
    --prompt "fix LIN-482, low risk only"

## api

$ curl -X POST https://app.warp.dev/api/v1/agent/runs \
    -H "Authorization: Bearer $WARP_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{ "prompt": "fix LIN-482" }'
{ "run_id": "run_4026", "state": "QUEUED" }

## sdk (typescript)

const run = await client.agent.run({ prompt: 'fix LIN-482' });
console.log(run.run_id);

## mcp · warp-factory server

{ "tool": "send_task", "factory_uid": "fct_acme_web",
  "title": "Fix LIN-482", "note": "low risk only" }
```
<!-- CODE_BLOCK_END id=c5 -->

>_[ fig. 2 · integrations ]⌗

>_[ fig. 2 · any surface ]⌗

>_[ fig. 2 · self-improvement ]⌗

quality loop

### Baked-in measurement and self-improvement

evals, benchmarks, and self-improvement loops drive measurable gains.

>_[ fig. 4 · quality loop · sample run ]⌗

##### evals on your own work

pass96%

8/13 07:03fail0.4$0.39

8/13 07:02pass0.8$0.53

8/13 07:02pass0.8$0.46

##### benchmarks across models

best1.00x

Claude Fable 5pass1.00x$0.53

GPT-5.6 Solpass0.94x$0.41

Gemini 3.6 Flashfail0.89x$0.32

##### self-improvement loops

auto-fix+3.7

memory updatedpass+0.2#4021

prompts tunedpass+3.2%#4022

regression caughtfail-0.4#4023

case study

### Cutting our cost per PR from $80 to $30

How we used Warp Factories Benchmarks to test models on our own engineering tasks and optimize for cost without sacrificing quality.

[read case study](/factories/benchmarks/warpbench)

![Benchmark results comparing correctness against average cost across model configurations, with gpt-5.6-sol (high) called out as the benchmark winner at 95% correctness and $6.13 average cost.](/img/factories-landing/case-study-benchmark-results.png)

### Warp is enterprise ready

Run agents confidently with guardrails in place, centrally configured agent access, and centrally managed permissions.

![Rectangle Health story cover](/img/customers/rectangle-health.png)

#### Rectangle Health uses Warp to build a self-improving AI teammate

Rectangle Health turned a senior engineer's side project into Rex, a self-improving AI teammate built on Oz that now writes 54% of its own code.

[read the story](/customers/rectangle-health-uses-warp-to-build-a-self-improving-ai-teammate)

![Docker story cover](/img/customers/docker.png)

#### Docker uses Warp to reduce onboarding time and give every engineer a shared source of truth

Docker adopted Warp for a more user-friendly terminal experience, using Warp Drive to streamline repetitive workflows and boost team productivity.

[read the story](/customers/docker)

no lock-in

### Open at every layer

>_[ fig. 3 · open at every layer ]⌗

layer 01

#### Any agent

warpclaude codecodexcursor

any MCP-capable coding agent.

layer 02

#### Any model

frontieropen-weight

frontier or open-weight, chosen per pipeline stage.

layer 03

#### Your compute or ours

warp cloudself-hosted

warp's cloud, or self-hosted in your own VPC.

layer 04

#### Data lives where you want

pluggablezero-retentionyour VPC

you own and store what your factory produces.

governance

### Control your coding agent chaos

continuous improvement, better governance and security, by default.

>_[ fig. 5 · control plane ]⌗

##### increase agent roi · cost per pr

$—

computeplatforminference

##### one control plane for every agent

resolve merge conflicts on server pr 14090fable 5orchestrationfnow

refactor auth middleware for session reuseopus 4.8claude codez14m

investigate child process kill issuefable 5slackj37m

investigate usize panic in offset codegpt-5.6 solslackf1h

fix desktop tab crashgemini 3.6slackj2h

add rate limiting to public api endpointsgpt-5.3codexe4h

##### agents prove their work with computer use

every factory agent captures a screenshot or video so you can verify its work before shipping a PR.

f

Activations dropped on the contact sales page this week. Can you investigate and fix the culprit?

On it — opening the browser to test the flow myself...

warp.dev/contact-sales

Bring Warp
to your team

Enter your work email and answer one question — we'll get you to the right person on our team.

Book a demoWork Email*you@company.comCONTINUE

Trusted by over 800,000 developers and thousands of engineering teams at leading companies

![](/img/logos/trusted-by/asana-black.svg)

![](/img/logos/trusted-by/docker-black.svg)

![](/img/logos/trusted-by/github-black.svg)

![](/img/logos/trusted-by/vmware-black.svg)

![](/img/logos/trusted-by/amplitude-black.svg)

![](/img/logos/trusted-by/teamworks-black.svg)

![](/img/logos/trusted-by/nvidia-black.svg)

![](/img/logos/trusted-by/ramp-black.svg)

![](/img/logos/trusted-by/asana-black.svg)

![](/img/logos/trusted-by/docker-black.svg)

![](/img/logos/trusted-by/github-black.svg)

![](/img/logos/trusted-by/vmware-black.svg)

![](/img/logos/trusted-by/amplitude-black.svg)

![](/img/logos/trusted-by/teamworks-black.svg)

![](/img/logos/trusted-by/nvidia-black.svg)

![](/img/logos/trusted-by/ramp-black.svg)

Found it — the testimonials section was hidden by collapsing divs. Patched, PR #436 is up for review.

### Use Warp everywhere

Warp is an open agentic development platform that was built to work wherever and however you work.

![Warp Factories product image, recomposed on a factories-neutral panel](/img/products/homepage-v2-factories.png)

##### Factories

A software factory that automates and orchestrates software development.

[request access](/factories/request-access)

![Warp Terminal product image, recomposed on a factories-neutral panel](/img/products/homepage-v2-terminal.png)

##### Terminal

An open-source terminal built for AI-assisted software development.

[Download Warp](/download)

![Warp Agent CLI product image, recomposed on a factories-neutral panel](/img/products/homepage-v2-agent-cli.png)

##### Agent CLI

A powerful coding agent that works in any terminal.

$

curl -fsSL https://app.warp.dev/download/agent-cli | bash

Mac

|Linux

|Windows

### Frequently asked questions

what is a cloud software factory?[+]

a factory is a fleet of agents wired to your SDLC — triggered by an issue, a slack message, or a schedule, and coordinated by warp factories from triage through review to a mergeable PR.

how do i define a factory?[+]

as code, in a factory.yaml + supporting agent files. define triggers, agents, models, and approval gates — check it into your repo like any other config.

do i have to use warp's models or config?[+]

no. bring your own model or harness (e.g. claude code or codex) — warp factories works with whatever your team prefers and helps identify the most cost-effective configuration over time.

do i need warp terminal to use factories?[+]

no. factories is a separate product — nobody at your company has to use warp terminal. work comes in through tools you already use, like slack, linear, jira, github, and gitlab. if you do use warp terminal, it has built-in factory integrations (native mcp) so you can iterate locally.

how much of my SDLC can be automated?[+]

most orgs start around 20-30% of PRs fully automated, starting with simple tasks. over time this goes up as models improve and your factory self-improves.

where does our data live?[+]

wherever you choose — warp's cloud, or fully self-hosted inside your own VPC, under your existing retention and compliance rules.

how do humans interact with the factory?[+]

humans put work into the factory via your existing tools like slack, teams, linear, jira, github and gitlab. at any time you can iterate on that work locally and the factory agents loop you in proactively when they need help.

can we start small?[+]

yes — most teams start with a single low-risk workflow, like dependency bumps or flaky test triage, before expanding coverage.

what does it cost?[+]

usage-based, priced per agent run. qualifying orgs get $10k of factory usage during closed early access.
