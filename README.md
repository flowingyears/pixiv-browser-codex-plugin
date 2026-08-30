# Pixiv Browser for Codex

A dependency-free local Codex plugin for searching, ranking, inspecting, and previewing public illustrations from Pixiv's official website.

## Features

- Multilingual Pixiv search with official artwork links
- Popularity and recency discovery channels
- Ranking by public bookmark, like, and view counts
- Filtering of works Pixiv declares as AI-generated
- Optional inclusion of mature-rated candidates when Pixiv exposes them to the current session
- Artwork metadata and thumbnail preview tools
- Strict network allowlist for `www.pixiv.net` and `i.pximg.net`
- No password collection, third-party proxy, or arbitrary-URL fetcher

## Tools

| Tool | Purpose |
| --- | --- |
| `search_pixiv` | Fast search for one query |
| `search_pixiv_ranked` | Multi-query discovery, deduplication, AI filtering, and bookmark ranking |
| `get_pixiv_artwork` | Public metadata, engagement counts, rating fields, and image URLs |
| `preview_pixiv_artwork` | Return a public preview as an MCP image block |

## Installation

Requirements: Python 3.10 or later and a Codex build with local stdio MCP support.

1. Clone this repository into your local plugins directory.
2. Run `scripts/configure.ps1` on Windows. It writes the absolute local server path into `.mcp.json`.
3. Add the plugin to a personal or team Codex marketplace.
4. Validate the plugin, install it, and start a new Codex task so the tools are reloaded.

```powershell
pwsh -File scripts/configure.ps1
```

The committed `.mcp.json` uses a relative path for readability. The configuration script makes the runtime path explicit because local MCP launchers do not all resolve relative paths identically.

## Recommended search prompt

Ask for multiple language variants and a candidate pool larger than the final output. For example:

> Search Pixiv for Kai'Sa using Japanese, Chinese, Korean, and English tags. Exclude declared AI works, rank by bookmarks, visually review the leading candidates, and return ten stylistically distinct illustrations.

Ranking alone does not guarantee artistic quality or stylistic diversity. The agent should preview a larger pool and remove duplicate compositions, repeated skins, obvious unlabelled generation artifacts, and unrelated tag collisions before presenting the final set.

## Content boundaries

The plugin does not bypass login, age verification, deleted/private status, geographic restrictions, or Pixiv safety settings. `include_mature` only retains mature candidates already returned to the current Pixiv session. Anonymous requests may not receive age-gated results.

## Stability notice

Pixiv does not publish a stable public developer API for this workflow. The plugin relies on endpoints used by the official website and may require maintenance when the site changes. See [MAINTENANCE.md](MAINTENANCE.md) and [docs/SEARCH_LOGIC.md](docs/SEARCH_LOGIC.md).

## Attribution and reuse

Artwork remains the property of its creators. Keep the official Pixiv artwork link with every result and verify the creator's reuse terms before downloading, reposting, training on, or publishing an image.

## License

No open-source license has been selected yet. The source is publicly inspectable, but no permission to redistribute or modify it is granted until the repository owner adds a license.
