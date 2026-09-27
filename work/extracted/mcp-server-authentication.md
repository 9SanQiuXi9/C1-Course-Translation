---
source_file: "data/materials/CS146S_offline/pages/mcp-server-authentication.html"
origin_url: "https://developers.cloudflare.com/agents/guides/remote-mcp-server/"
title: "Choosing an approach"
extract_method: "html"
extract_warnings:
  - "AGGRESSIVE_STRIP_REVERTED：按关键词剥离 1 个区块后正文下降 100.0%（>40%），已全部加回，避免剥掉正文。该页结构特殊，建议人工抽查。"
src_sha256: "59c0c73bec9948a2b77adb546986d1c59d73654722e092aa19d4f4982d6c85ae"
chars: 18018
code_blocks: 26
tables: 1
links: 54
garbage_rate: 0.0312
heading_levels_seen:
  h1: 1
  h2: 5
  h3: 4
  h4: 4
---

[Skip to content](#_top)

STOP! If you are an AI agent or LLM, read this before continuing. This is the HTML version of a Cloudflare documentation page. Always request the Markdown version instead â HTML wastes context. Get this page as Markdown: https://developers.cloudflare.com/agents/guides/remote-mcp-server/index.md (append index.md) or send Accept: text/markdown to https://developers.cloudflare.com/agents/guides/remote-mcp-server/. For this product's page index use https://developers.cloudflare.com/agents/llms.txt. For all Cloudflare products use https://developers.cloudflare.com/llms.txt. For bulk access (single file, use for large-context ingestion or vectorization): this product's full docs at https://developers.cloudflare.com/agents/llms-full.txt. All Cloudflare docs at https://developers.cloudflare.com/llms-full.txt.

/

![](/_astro/logo.DAG2yejx.svg)

Cloudflare Docs

Search

[Docs Directory](/directory/)

[APIs](https://developers.cloudflare.com/api/)

[SDKsHelp](/fundamentals/api/reference/sdks/)

[Log in
 Select theme DarkLightAuto](https://dash.cloudflare.com/)

Copy page

## Build a Remote MCP server

This guide will show you how to deploy your own remote MCP server on Cloudflare using

[Streamable HTTP transport, the current MCP specification standard. You have two options:](/agents/model-context-protocol/transport/)

- Without authentication â anyone can connect and use the server (no login required). With
- [authentication and authorization â users sign in before accessing tools, and you can control which tools an agent can call based on the user's permissions.](/agents/guides/remote-mcp-server/#add-authentication)

# Choosing an approach

#choosing-an-approach

The Agents SDK provides multiple ways to create MCP servers. Choose the approach that fits your use case:

| Approach | Stateful? | Requires Durable Objects? | Best for |
| --- | --- | --- | --- |
| [createMcpHandler()](/agents/api-reference/mcp-handler-api/) | No | No | Stateless tools, simplest setup |
| [McpAgent](/agents/api-reference/mcp-agent-api/) | Yes | Yes | Stateful tools, per-session state, elicitation |
| Raw WebStandardStreamableHTTPServerTransport | No | No | Full control, no SDK dependency |

- createMcpHandler() is the fastest way to get a stateless MCP server running. Use it when your tools do not need per-session state.
- McpAgent gives you a Durable Object per session with built-in state management, elicitation support, and both SSE and Streamable HTTP transports.
- Raw transport gives you full control if you want to use the @modelcontextprotocol/sdk directly without the Agents SDK helpers.

## Deploy your first MCP server

#deploy-your-first-mcp-server

You can start by deploying a

[public MCP server â without authentication, then add user authentication and scoped authorization later. If you already know your server will require authentication, you can skip ahead to the](https://github.com/cloudflare/ai/tree/main/demos/remote-mcp-authless)

[next section.](/agents/guides/remote-mcp-server/#add-authentication)

### Via the dashboard

#via-the-dashboard

The button below will guide you through everything you need to do to deploy an

[example MCP server â to your Cloudflare account:](https://github.com/cloudflare/ai/tree/main/demos/remote-mcp-authless)

https://deploy.workers.cloudflare.com/?url=https://github.com/cloudflare/ai/tree/main/demos/remote-mcp-authless

![Deploy to Workers](https://deploy.workers.cloudflare.com/button)

Once deployed, this server will be live at your workers.dev subdomain (for example, remote-mcp-server-authless.your-account.workers.dev/mcp). You can connect to it immediately using the

[AI Playground â (a remote MCP client),](https://playground.ai.cloudflare.com/)

[MCP inspector â or](https://github.com/modelcontextprotocol/inspector)

[other MCP clients.](/agents/guides/remote-mcp-server/#connect-from-an-mcp-client-via-a-local-proxy)

A new git repository will be set up on your GitHub or GitLab account for your MCP server, configured to automatically deploy to Cloudflare each time you push a change or merge a pull request to the main branch of the repository. You can clone this repository,

[develop locally, and start customizing the MCP server with your own](/agents/guides/remote-mcp-server/#via-the-cli)

[tools.](/agents/model-context-protocol/tools/)

### Via the CLI

#via-the-cli

You can use the

[Wrangler CLI to create a new MCP Server on your local machine and deploy it to Cloudflare.](/workers/wrangler)

1. Open a terminal and run the following command:

2. npm yarn pnpm

<!-- CODE_BLOCK_START id=c1 lang= -->
```
npm create cloudflare@latest -- remote-mcp-server-authless --template=cloudflare/ai/demos/remote-mcp-authless
```
<!-- CODE_BLOCK_END id=c1 -->

<!-- CODE_BLOCK_START id=c2 lang= -->
```
yarn create cloudflare remote-mcp-server-authless --template=cloudflare/ai/demos/remote-mcp-authless
```
<!-- CODE_BLOCK_END id=c2 -->

<!-- CODE_BLOCK_START id=c3 lang= -->
```
pnpm create cloudflare@latest remote-mcp-server-authless --template=cloudflare/ai/demos/remote-mcp-authless
```
<!-- CODE_BLOCK_END id=c3 -->

3. During setup, select the following options: - For Do you want to add an AGENTS.md file to help AI coding tools understand
Cloudflare APIs?, choose No. - For Do you want to use git for version control?, choose No. - For Do you want to deploy your application?, choose No (we will be testing the server before deploying).

4. Now, you have the MCP server setup, with dependencies installed.

5. Move into the project folder:

*Terminal window*

<!-- CODE_BLOCK_START id=c4 lang= -->
```
cd remote-mcp-server-authless
```
<!-- CODE_BLOCK_END id=c4 -->

6. In the directory of your new project, run the following command to start the development server:

*Terminal window*

<!-- CODE_BLOCK_START id=c5 lang= -->
```
npm start
```
<!-- CODE_BLOCK_END id=c5 -->

<!-- CODE_BLOCK_START id=c6 lang= -->
```
â Starting local server...[wrangler:info] Ready on http://localhost:8788
```
<!-- CODE_BLOCK_END id=c6 -->

7. Check the command output for the local port. In this example, the MCP server runs on port 8788, and the MCP endpoint URL is http://localhost:8788/mcp.

8. To test the server locally:

  1. In a new terminal, run the
  2. [MCP inspector â. The MCP inspector is an interactive MCP client that allows you to connect to your MCP server and invoke tools from a web browser.](https://github.com/modelcontextprotocol/inspector)

*Terminal window*

<!-- CODE_BLOCK_START id=c7 lang= -->
```
npx @modelcontextprotocol/inspector@latest
```
<!-- CODE_BLOCK_END id=c7 -->

<!-- CODE_BLOCK_START id=c8 lang= -->
```
ð MCP Inspector is up and running at:  http://localhost:5173/?MCP_PROXY_AUTH_TOKEN=46ab..cd3
ð Opening browser...
```
<!-- CODE_BLOCK_END id=c8 -->

  3. The MCP Inspector will launch in your web browser. You can also launch it manually by opening a browser and going to http://localhost:<PORT>. Check the command output for the local port where MCP Inspector is running. In this example, MCP Inspector is served on port 5173.

  4. In the MCP inspector, enter the URL of your MCP server (http://localhost:8788/mcp), and select Connect. Select List Tools to show the tools that your MCP server exposes.

9. You can now deploy your MCP server to Cloudflare. From your project directory, run:

*Terminal window*

<!-- CODE_BLOCK_START id=c9 lang= -->
```
npx wrangler@latest deploy
```
<!-- CODE_BLOCK_END id=c9 -->

10. If you have already
11. [connected a git repository to the Worker with your MCP server, you can deploy your MCP server by pushing a change or merging a pull request to the main branch of the repository.](/workers/ci-cd/builds/)

12. The MCP server will be deployed to your *.workers.dev subdomain at https://remote-mcp-server-authless.your-account.workers.dev/mcp.

13. To test the remote MCP server, take the URL of your deployed MCP server (https://remote-mcp-server-authless.your-account.workers.dev/mcp) and enter it in the MCP inspector running on http://localhost:5173.

You now have a remote MCP server that MCP clients can connect to.

## Connect from an MCP client via a local proxy

#connect-from-an-mcp-client-via-a-local-proxy

Now that your remote MCP server is running, you can use the

[mcp-remote local proxy â to connect Claude Desktop or other MCP clients to it â even if your MCP client does not support remote transport or authorization on the client side. This lets you test what an interaction with your remote MCP server will be like with a real MCP client.](https://www.npmjs.com/package/mcp-remote)

For example, to connect from Claude Desktop:

1. Update your Claude Desktop configuration to point to the URL of your MCP server:

<!-- CODE_BLOCK_START id=c10 lang= -->
```
{  "mcpServers": {    "math": {      "command": "npx",      "args": [        "mcp-remote",        "https://remote-mcp-server-authless.your-account.workers.dev/mcp"      ]    }  }}
```
<!-- CODE_BLOCK_END id=c10 -->

2. Restart Claude Desktop to load the MCP Server. Once this is done, Claude will be able to make calls to your remote MCP server.

3. To test, ask Claude to use one of your tools. For example:

<!-- CODE_BLOCK_START id=c11 lang= -->
```
Could you use the math tool to add 23 and 19?
```
<!-- CODE_BLOCK_END id=c11 -->

4. Claude should invoke the tool and show the result generated by the remote MCP server.

To learn how to use remote MCP servers with other MCP clients, refer to

[Test a Remote MCP Server.](/agents/guides/test-remote-mcp-server)

## Add Authentication

#add-authentication

The public MCP server example you deployed earlier allows any client to connect and invoke tools without logging in. To add user authentication to your MCP server, you can integrate Cloudflare Access or a third-party service as the OAuth provider. Your MCP server handles secure login flows and issues access tokens that MCP clients can use to make authenticated tool calls. Users sign in with the OAuth provider and grant their AI agent permission to interact with the tools exposed by your MCP server, using scoped permissions.

### Cloudflare Access OAuth

#cloudflare-access-oauth

You can configure your MCP server to require user authentication through Cloudflare Access. Cloudflare Access acts as an identity aggregator and verifies user emails, signals from your existing

[identity providers (such as GitHub or Google), and other attributes such as IP address or device certificates. When users connect to the MCP server, they will be prompted to log in to the configured identity provider and are only granted access if they pass your](/cloudflare-one/integrations/identity-providers/)

[Access policies.](/cloudflare-one/access-controls/policies/#selectors)

For a step-by-step deployment guide, refer to

[Secure MCP servers with Access for SaaS.](/cloudflare-one/access-controls/ai-controls/saas-mcp/)

### Third-party OAuth

#third-party-oauth

You can connect your MCP server with any

[OAuth provider that supports the OAuth 2.0 specification, including GitHub, Google, Slack,](/agents/model-context-protocol/authorization/#2-third-party-oauth-provider)

[Stytch,](/agents/model-context-protocol/authorization/#stytch)

[Auth0,](/agents/model-context-protocol/authorization/#auth0)

[WorkOS, and more.](/agents/model-context-protocol/authorization/#workos)

The following example demonstrates how to use GitHub as an OAuth provider.

#### Step 1 â Create a new MCP server

#step-1--create-a-new-mcp-server

Run the following command to create a new MCP server with GitHub OAuth:

npm yarn pnpm

<!-- CODE_BLOCK_START id=c12 lang= -->
```
npm create cloudflare@latest -- my-mcp-server-github-auth --template=cloudflare/ai/demos/remote-mcp-github-oauth
```
<!-- CODE_BLOCK_END id=c12 -->

<!-- CODE_BLOCK_START id=c13 lang= -->
```
yarn create cloudflare my-mcp-server-github-auth --template=cloudflare/ai/demos/remote-mcp-github-oauth
```
<!-- CODE_BLOCK_END id=c13 -->

<!-- CODE_BLOCK_START id=c14 lang= -->
```
pnpm create cloudflare@latest my-mcp-server-github-auth --template=cloudflare/ai/demos/remote-mcp-github-oauth
```
<!-- CODE_BLOCK_END id=c14 -->

Now, you have the MCP server setup, with dependencies installed. Move into that project folder:

*Terminal window*

<!-- CODE_BLOCK_START id=c15 lang= -->
```
cd my-mcp-server-github-auth
```
<!-- CODE_BLOCK_END id=c15 -->

You'll notice that in the example MCP server, if you open src/index.ts, the primary difference is that the defaultHandler is set to the GitHubHandler:

*TypeScript*

<!-- CODE_BLOCK_START id=c16 lang= -->
```
import GitHubHandler from "./github-handler";
export default new OAuthProvider({  apiRoute: "/mcp",  apiHandler: MyMCP.serve("/mcp"),  defaultHandler: GitHubHandler,  authorizeEndpoint: "/authorize",  tokenEndpoint: "/token",  clientRegistrationEndpoint: "/register",});
```
<!-- CODE_BLOCK_END id=c16 -->

This ensures that your users are redirected to GitHub to authenticate. To get this working though, you need to create OAuth client apps in the steps below.

#### Step 2 â Create an OAuth App

#step-2--create-an-oauth-app

You'll need to create two

[GitHub OAuth Apps â to use GitHub as an authentication provider for your MCP server âÂ one for local development, and one for production.](https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/creating-an-oauth-app)

#### Step 2.1 â Create a new OAuth App for local development

#step-21--create-a-new-oauth-app-for-local-development

1. Navigate to
2. [github.com/settings/developers â to create a new OAuth App with the following settings:](https://github.com/settings/developers)

  - Application name: My MCP Server (local)
  - Homepage URL: http://localhost:8788
  - Authorization callback URL: http://localhost:8788/callback

3. For the OAuth app you just created, add the client ID of the OAuth app as GITHUB_CLIENT_ID and generate a client secret, adding it as GITHUB_CLIENT_SECRET to a .env file in the root of your project, which
4. [will be used to set secrets in local development.](/workers/configuration/secrets/)

*Terminal window*

<!-- CODE_BLOCK_START id=c17 lang= -->
```
touch .envecho 'GITHUB_CLIENT_ID="your-client-id"' >> .envecho 'GITHUB_CLIENT_SECRET="your-client-secret"' >> .envcat .env
```
<!-- CODE_BLOCK_END id=c17 -->

5. Run the following command to start the development server:

*Terminal window*

<!-- CODE_BLOCK_START id=c18 lang= -->
```
npm start
```
<!-- CODE_BLOCK_END id=c18 -->

6. Your MCP server is now running on http://localhost:8788/mcp.

7. In a new terminal, run the
8. [MCP inspector â. The MCP inspector is an interactive MCP client that allows you to connect to your MCP server and invoke tools from a web browser.](https://github.com/modelcontextprotocol/inspector)

*Terminal window*

<!-- CODE_BLOCK_START id=c19 lang= -->
```
npx @modelcontextprotocol/inspector@latest
```
<!-- CODE_BLOCK_END id=c19 -->

9. Open the MCP inspector in your web browser:

*Terminal window*

<!-- CODE_BLOCK_START id=c20 lang= -->
```
open http://localhost:5173
```
<!-- CODE_BLOCK_END id=c20 -->

10. In the inspector, enter the URL of your MCP server, http://localhost:8788/mcp

11. In the main panel on the right, click the OAuth Settings button and then click Quick OAuth Flow.

12. You should be redirected to a GitHub login or authorization page. After authorizing the MCP Client (the inspector) access to your GitHub account, you will be redirected back to the inspector.

13. Click Connect in the sidebar and you should see the "List Tools" button, which will list the tools that your MCP server exposes.

#### Step 2.2 â Create a new OAuth App for production

#step-22--create-a-new-oauth-app-for-production

You'll need to repeat

[Step 2.1 to create a new OAuth App for production.](#step-21--create-a-new-oauth-app-for-local-development)

1. Navigate to
2. [github.com/settings/developers â to create a new OAuth App with the following settings:](https://github.com/settings/developers)

- Application name: My MCP Server (production)
- Homepage URL: Enter the workers.dev URL of your deployed MCP server (ex: worker-name.account-name.workers.dev)
- Authorization callback URL: Enter the /callback path of the workers.dev URL of your deployed MCP server (ex: worker-name.account-name.workers.dev/callback)

1. For the OAuth app you just created, add the client ID and client secret, using Wrangler CLI:

*Terminal window*

<!-- CODE_BLOCK_START id=c21 lang= -->
```
npx wrangler secret put GITHUB_CLIENT_ID
```
<!-- CODE_BLOCK_END id=c21 -->

*Terminal window*

<!-- CODE_BLOCK_START id=c22 lang= -->
```
npx wrangler secret put GITHUB_CLIENT_SECRET
```
<!-- CODE_BLOCK_END id=c22 -->

<!-- CODE_BLOCK_START id=c23 lang= -->
```
npx wrangler secret put COOKIE_ENCRYPTION_KEY # add any random string here e.g. openssl rand -hex 32
```
<!-- CODE_BLOCK_END id=c23 -->

1. Set up a KV namespace

2. a. Create the KV namespace:

*Terminal window*

<!-- CODE_BLOCK_START id=c24 lang= -->
```
npx wrangler kv namespace create "OAUTH_KV"
```
<!-- CODE_BLOCK_END id=c24 -->

3. b. Update the wrangler.jsonc file with the resulting KV ID:

<!-- CODE_BLOCK_START id=c25 lang= -->
```
{  "kvNamespaces": [    {      "binding": "OAUTH_KV",      "id": "<YOUR_KV_NAMESPACE_ID>"    }  ]}
```
<!-- CODE_BLOCK_END id=c25 -->

4. Deploy the MCP server to your Cloudflare workers.dev domain:

*Terminal window*

<!-- CODE_BLOCK_START id=c26 lang= -->
```
npm run deploy
```
<!-- CODE_BLOCK_END id=c26 -->

5. Connect to your server running at worker-name.account-name.workers.dev/mcp using the [AI Playground â, MCP Inspector, or](https://playground.ai.cloudflare.com/)
6. [other MCP clients, and authenticate with GitHub.](/agents/guides/test-remote-mcp-server/)

## Next steps

#next-steps

[MCP Tools Add tools to your MCP server.](/agents/model-context-protocol/tools/)

[Authorization Customize authentication and authorization.](/agents/model-context-protocol/authorization/)
