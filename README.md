# Pixiv Browser for Codex

[中文](#中文) | [English](#english)

## 中文

一个无第三方依赖的本地 Codex 插件，用于从 Pixiv 官方网站搜索、排序、检查和预览公开插画。

### 功能

- 使用多语言关键词搜索 Pixiv，并保留官方作品链接
- 同时从热门度和发布时间两个方向发现候选作品
- 按公开收藏数、点赞数和浏览数综合排序
- 排除 Pixiv 明确标记为 AI 生成的作品
- 可选保留当前 Pixiv 会话能够正常显示的年龄限制候选作品
- 提供作品元数据查询和缩略图预览工具
- 网络请求严格限制于 `www.pixiv.net` 和 `i.pximg.net`
- 不收集密码，不使用第三方代理，也不提供任意网址抓取功能

### 工具

| 工具 | 用途 |
| --- | --- |
| `search_pixiv` | 对单个关键词进行快速搜索 |
| `search_pixiv_ranked` | 多关键词发现、去重、AI 作品过滤和收藏量排序 |
| `get_pixiv_artwork` | 获取公开元数据、互动数据、分级字段和图片地址 |
| `preview_pixiv_artwork` | 以 MCP 图片内容块返回公开预览图 |

### 安装

要求：Python 3.10 或更高版本，以及支持本地 stdio MCP 的 Codex 版本。

1. 将此仓库克隆到本地插件目录。
2. 在 Windows 上运行 `scripts/configure.ps1`，脚本会把本地服务程序的绝对路径写入 `.mcp.json`。
3. 将插件添加到个人或团队 Codex marketplace。
4. 验证并安装插件，然后新建一个 Codex 任务以重新加载工具。

```powershell
pwsh -File scripts/configure.ps1
```

仓库中的 `.mcp.json` 使用相对路径以便阅读。由于不同的本地 MCP 启动器对相对路径的解析并不完全一致，配置脚本会将运行路径改为明确的绝对路径。

### 推荐搜索提示词

建议同时提供多种语言的关键词，并让候选池大于最终输出数量。例如：

> 使用日语、中文、韩语和英语标签搜索 Pixiv 上的卡莎。排除明确标记的 AI 作品，按收藏量排序，预览靠前的候选作品，最终返回十张风格各异的插画。

单纯按数据排序不能保证艺术质量和风格多样性。展示最终结果前，应预览更大的候选池，并排除构图重复、皮肤主题过度集中、带有明显未标注生成痕迹以及标签误匹配的作品。

### 内容边界

插件不会绕过登录、年龄验证、作品删除或私密状态、地区限制以及 Pixiv 的安全设置。`include_mature` 只会保留当前 Pixiv 会话已经返回的年龄限制候选作品；匿名请求可能无法获得此类结果。

### 稳定性说明

Pixiv 没有为这一检索流程提供稳定的公开开发者 API。本插件使用官方网站所调用的接口，因此网站变更后可能需要维护。详见 [MAINTENANCE.md](MAINTENANCE.md) 和 [docs/SEARCH_LOGIC.md](docs/SEARCH_LOGIC.md)。

### 署名与再利用

作品版权归原作者所有。每条结果都应保留 Pixiv 官方作品链接；下载、转载、用于训练或公开发布图片前，请先确认作者的再利用条款。

### 许可证

本项目目前尚未选择开源许可证。源代码可以公开查看，但在仓库所有者添加许可证前，不代表授予再分发或修改许可。

## English

A dependency-free local Codex plugin for searching, ranking, inspecting, and previewing public illustrations from Pixiv's official website.

### Features

- Multilingual Pixiv search with official artwork links
- Popularity and recency discovery channels
- Ranking by public bookmark, like, and view counts
- Filtering of works Pixiv declares as AI-generated
- Optional inclusion of mature-rated candidates when Pixiv exposes them to the current session
- Artwork metadata and thumbnail preview tools
- Strict network allowlist for `www.pixiv.net` and `i.pximg.net`
- No password collection, third-party proxy, or arbitrary-URL fetcher

### Tools

| Tool | Purpose |
| --- | --- |
| `search_pixiv` | Fast search for one query |
| `search_pixiv_ranked` | Multi-query discovery, deduplication, AI filtering, and bookmark ranking |
| `get_pixiv_artwork` | Public metadata, engagement counts, rating fields, and image URLs |
| `preview_pixiv_artwork` | Return a public preview as an MCP image block |

### Installation

Requirements: Python 3.10 or later and a Codex build with local stdio MCP support.

1. Clone this repository into your local plugins directory.
2. Run `scripts/configure.ps1` on Windows. It writes the absolute local server path into `.mcp.json`.
3. Add the plugin to a personal or team Codex marketplace.
4. Validate the plugin, install it, and start a new Codex task so the tools are reloaded.

```powershell
pwsh -File scripts/configure.ps1
```

The committed `.mcp.json` uses a relative path for readability. The configuration script makes the runtime path explicit because local MCP launchers do not all resolve relative paths identically.

### Recommended search prompt

Ask for multiple language variants and a candidate pool larger than the final output. For example:

> Search Pixiv for Kai'Sa using Japanese, Chinese, Korean, and English tags. Exclude declared AI works, rank by bookmarks, visually review the leading candidates, and return ten stylistically distinct illustrations.

Ranking alone does not guarantee artistic quality or stylistic diversity. The agent should preview a larger pool and remove duplicate compositions, repeated skins, obvious unlabelled generation artifacts, and unrelated tag collisions before presenting the final set.

### Content boundaries

The plugin does not bypass login, age verification, deleted/private status, geographic restrictions, or Pixiv safety settings. `include_mature` only retains mature candidates already returned to the current Pixiv session. Anonymous requests may not receive age-gated results.

### Stability notice

Pixiv does not publish a stable public developer API for this workflow. The plugin relies on endpoints used by the official website and may require maintenance when the site changes. See [MAINTENANCE.md](MAINTENANCE.md) and [docs/SEARCH_LOGIC.md](docs/SEARCH_LOGIC.md).

### Attribution and reuse

Artwork remains the property of its creators. Keep the official Pixiv artwork link with every result and verify the creator's reuse terms before downloading, reposting, training on, or publishing an image.

### License

No open-source license has been selected yet. The source is publicly inspectable, but no permission to redistribute or modify it is granted until the repository owner adds a license.
