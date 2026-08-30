# Maintenance Protocol

## Scope

This document defines how maintainers update the plugin when Pixiv, Codex MCP, or local runtime behavior changes.

## Release policy

- Use semantic versioning.
- Patch: fixes that preserve tool schemas and behavior.
- Minor: backward-compatible tools, fields, or ranking options.
- Major: renamed tools, incompatible schemas, authentication changes, or removed behavior.
- Record user-visible changes in `CHANGELOG.md` before release.

## Routine checks

Run these checks before every release and at least monthly while the plugin is actively maintained:

1. Validate `.codex-plugin/plugin.json` against the current Codex plugin validator.
2. Parse `scripts/pixiv_mcp.py` with the supported Python versions.
3. Exercise MCP `initialize`, `tools/list`, and one call per tool.
4. Search a stable public tag and confirm result IDs, titles, creator names, and official URLs.
5. Read one artwork detail and verify bookmark, AI, and rating fields.
6. Preview one image and confirm the `i.pximg.net` referer rule still works.
7. Confirm all outbound requests remain restricted to the two allowlisted Pixiv hosts.
8. Confirm no cookie, token, local absolute path, downloaded artwork, or user search history is committed.

## Endpoint-change response

When Pixiv changes an endpoint or response shape:

1. Reproduce the failure with a public, non-sensitive artwork.
2. Capture only sanitized status codes and field names; never publish session cookies or full authenticated responses.
3. Add a focused compatibility parser instead of silently accepting arbitrary payloads.
4. Preserve old fields when possible and add regression fixtures containing metadata only.
5. Update `docs/SEARCH_LOGIC.md` if ranking or filtering semantics change.
6. Release a patch or minor version and describe the affected tools.

## Security invariants

- Do not add arbitrary URL fetching.
- Do not weaken the `www.pixiv.net` and `i.pximg.net` allowlists.
- Do not automate password collection or browser-cookie extraction.
- Do not bypass login, age verification, private/deleted status, geographic restrictions, or safety settings.
- Cap JSON and image response sizes and retain network timeouts.
- Keep access tokens, cookies, and authenticated URLs out of logs, issues, fixtures, commits, and releases.

## AI and mature-content semantics

- `aiType=2` is filtered by default as Pixiv-declared AI-generated work.
- Unknown or historical AI metadata requires cautious visual review; it is not proof either way.
- `include_mature` does not grant access. It only avoids discarding rated results already returned by Pixiv.
- Changes to these semantics require a documented minor release at minimum.

## Deprecation policy

Mark a tool or field deprecated for at least one minor release before removal. Include a replacement path in the README and changelog. Immediate removal is reserved for security, legal, or platform-compliance issues.
