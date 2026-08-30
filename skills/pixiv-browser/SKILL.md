---
name: pixiv-browser
description: Search, inspect, and preview public illustrations from Pixiv when the user explicitly asks to find Pixiv artwork, creators, or images.
---

# Pixiv Browser

Use the `pixiv-browser` MCP tools for requests specifically involving Pixiv.

## Workflow

1. Call `search_pixiv` with the user's keywords. Japanese tags often give better results.
2. Present a compact selection with title, creator, artwork ID, and the official Pixiv URL.
3. Call `get_pixiv_artwork` when the user asks about one result.
4. Call `preview_pixiv_artwork` only for the selected public artwork or when visual comparison is useful.

## Safety and attribution

- Keep the official Pixiv artwork URL beside every result.
- Treat artwork and metadata as creator-owned content; do not imply ownership or permission to reuse it.
- Do not attempt to bypass login, age gates, deleted/private status, geographic restrictions, or Pixiv safety settings.
- The plugin uses Pixiv website endpoints that are not a documented public developer API and may change without notice.
- If Pixiv rejects a request, report the limitation instead of repeatedly retrying or changing identity headers.
