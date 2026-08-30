#!/usr/bin/env python3
"""Minimal stdio MCP server for public Pixiv website search and previews."""

from __future__ import annotations

import base64
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any


PROTOCOL_VERSION = "2025-03-26"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/136 Safari/537.36"
PIXIV_ORIGIN = "https://www.pixiv.net"
ALLOWED_IMAGE_HOST = "i.pximg.net"
MAX_RESULTS = 20
MAX_IMAGE_BYTES = 8 * 1024 * 1024
MAX_QUERIES = 8


TOOLS = [
    {
        "name": "search_pixiv",
        "description": "Search public illustrations on the official Pixiv website and return metadata and official artwork links.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Keywords or Pixiv tags to search for."},
                "limit": {"type": "integer", "minimum": 1, "maximum": MAX_RESULTS, "default": 10},
                "order": {"type": "string", "enum": ["date_d", "date"], "default": "date_d"}
            },
            "required": ["query"],
            "additionalProperties": False
        }
    },
    {
        "name": "get_pixiv_artwork",
        "description": "Get public metadata and image URLs for one Pixiv artwork ID from the official website.",
        "inputSchema": {
            "type": "object",
            "properties": {"artwork_id": {"type": "integer", "minimum": 1}},
            "required": ["artwork_id"],
            "additionalProperties": False
        }
    },
    {
        "name": "search_pixiv_ranked",
        "description": "Search Pixiv with multiple query variants, deduplicate results, filter Pixiv-declared AI works, and rank public candidates by bookmark count.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "queries": {
                    "type": "array",
                    "items": {"type": "string"},
                    "minItems": 1,
                    "maxItems": MAX_QUERIES,
                    "description": "Multilingual character, series, and tag queries."
                },
                "limit": {"type": "integer", "minimum": 1, "maximum": 20, "default": 10},
                "exclude_ai": {"type": "boolean", "default": True},
                "include_mature": {"type": "boolean", "default": True}
            },
            "required": ["queries"],
            "additionalProperties": False
        }
    },
    {
        "name": "preview_pixiv_artwork",
        "description": "Fetch a preview image for a public Pixiv artwork ID and return it as an MCP image block.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "artwork_id": {"type": "integer", "minimum": 1},
                "page": {"type": "integer", "minimum": 0, "default": 0}
            },
            "required": ["artwork_id"],
            "additionalProperties": False
        }
    }
]


def _json_request(url: str) -> dict[str, Any]:
    if not url.startswith(PIXIV_ORIGIN + "/"):
        raise ValueError("Only the official www.pixiv.net origin is allowed")
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.7,ja;q=0.6",
            "Referer": PIXIV_ORIGIN + "/"
        }
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        data = response.read(5 * 1024 * 1024 + 1)
    if len(data) > 5 * 1024 * 1024:
        raise ValueError("Pixiv response exceeded the safety limit")
    payload = json.loads(data.decode("utf-8"))
    if payload.get("error"):
        raise RuntimeError(payload.get("message") or "Pixiv returned an error")
    return payload


def _image_request(url: str) -> tuple[bytes, str]:
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme != "https" or parsed.hostname != ALLOWED_IMAGE_HOST:
        raise ValueError("Only images hosted by i.pximg.net are allowed")
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Referer": PIXIV_ORIGIN + "/"})
    with urllib.request.urlopen(request, timeout=25) as response:
        content_type = response.headers.get_content_type()
        data = response.read(MAX_IMAGE_BYTES + 1)
    if len(data) > MAX_IMAGE_BYTES:
        raise ValueError("Pixiv preview exceeded the 8 MB safety limit")
    if content_type not in {"image/jpeg", "image/png", "image/gif", "image/webp"}:
        raise ValueError(f"Unexpected Pixiv content type: {content_type}")
    return data, content_type


def _artwork_link(artwork_id: int | str) -> str:
    return f"{PIXIV_ORIGIN}/artworks/{artwork_id}"


def _compact_illust(item: dict[str, Any]) -> dict[str, Any]:
    artwork_id = int(item.get("id", 0))
    return {
        "id": artwork_id,
        "title": item.get("title", ""),
        "creator": item.get("userName", ""),
        "creator_id": item.get("userId", ""),
        "page_count": item.get("pageCount", 1),
        "width": item.get("width"),
        "height": item.get("height"),
        "tags": item.get("tags", []),
        "thumbnail_url": item.get("url", ""),
        "artwork_url": _artwork_link(artwork_id)
    }


def search_pixiv(arguments: dict[str, Any]) -> list[dict[str, Any]]:
    query = str(arguments.get("query", "")).strip()
    if not query or len(query) > 200:
        raise ValueError("query must contain 1 to 200 characters")
    limit = max(1, min(int(arguments.get("limit", 10)), MAX_RESULTS))
    order = arguments.get("order", "date_d")
    encoded = urllib.parse.quote(query, safe="")
    params = urllib.parse.urlencode({"word": query, "order": order, "mode": "all", "p": 1, "s_mode": "s_tag_full", "type": "all", "lang": "zh"})
    payload = _json_request(f"{PIXIV_ORIGIN}/ajax/search/artworks/{encoded}?{params}")
    body = payload.get("body") or {}
    section = body.get("illustManga") or body.get("illust") or {}
    items = section.get("data") or []
    return [_compact_illust(item) for item in items[:limit]]


def get_pixiv_artwork(arguments: dict[str, Any]) -> dict[str, Any]:
    artwork_id = int(arguments["artwork_id"])
    payload = _json_request(f"{PIXIV_ORIGIN}/ajax/illust/{artwork_id}?lang=zh")
    body = payload.get("body") or {}
    tags = [tag.get("tag") for tag in (body.get("tags") or {}).get("tags", []) if tag.get("tag")]
    urls = body.get("urls") or {}
    return {
        "id": artwork_id,
        "title": body.get("illustTitle", ""),
        "description_html": body.get("illustComment", ""),
        "creator": body.get("userName", ""),
        "creator_id": body.get("userId", ""),
        "page_count": body.get("pageCount", 1),
        "bookmark_count": body.get("bookmarkCount", 0),
        "like_count": body.get("likeCount", 0),
        "view_count": body.get("viewCount", 0),
        "ai_type": body.get("aiType", 0),
        "x_restrict": body.get("xRestrict", 0),
        "width": body.get("width"),
        "height": body.get("height"),
        "tags": tags,
        "preview_url": urls.get("regular") or urls.get("small") or urls.get("thumb_mini"),
        "original_url": urls.get("original"),
        "artwork_url": _artwork_link(artwork_id)
    }


def search_pixiv_ranked(arguments: dict[str, Any]) -> list[dict[str, Any]]:
    queries = arguments.get("queries") or []
    if not 1 <= len(queries) <= MAX_QUERIES:
        raise ValueError(f"queries must contain 1 to {MAX_QUERIES} items")
    limit = max(1, min(int(arguments.get("limit", 10)), 20))
    exclude_ai = bool(arguments.get("exclude_ai", True))
    include_mature = bool(arguments.get("include_mature", True))

    candidates: dict[int, dict[str, Any]] = {}
    for raw_query in queries:
        query = str(raw_query).strip()
        if not query:
            continue
        # Popularity and recency are separate discovery channels. Pixiv may
        # restrict popularity ordering for some sessions, so failures fall
        # back to the public newest order without aborting the whole search.
        for order in ("popular_d", "date_d"):
            try:
                for item in search_pixiv({"query": query, "limit": 20, "order": order}):
                    candidates.setdefault(int(item["id"]), item)
            except (RuntimeError, urllib.error.HTTPError, urllib.error.URLError):
                continue

    ranked: list[dict[str, Any]] = []
    for artwork_id, summary in candidates.items():
        try:
            detail = get_pixiv_artwork({"artwork_id": artwork_id})
        except (RuntimeError, urllib.error.HTTPError, urllib.error.URLError):
            continue
        # Pixiv currently uses aiType=2 for declared AI-generated works.
        # aiType=0 is historical/unspecified and still needs visual review.
        if exclude_ai and detail.get("ai_type") == 2:
            continue
        if not include_mature and int(detail.get("x_restrict") or 0) > 0:
            continue
        ranked.append({**summary, **detail})

    ranked.sort(
        key=lambda item: (
            int(item.get("bookmark_count") or 0),
            int(item.get("like_count") or 0),
            int(item.get("view_count") or 0)
        ),
        reverse=True
    )
    return ranked[:limit]


def preview_pixiv_artwork(arguments: dict[str, Any]) -> tuple[bytes, str, str]:
    artwork_id = int(arguments["artwork_id"])
    page = max(0, int(arguments.get("page", 0)))
    detail = get_pixiv_artwork({"artwork_id": artwork_id})
    if page >= int(detail.get("page_count") or 1):
        raise ValueError("page is outside this artwork's page range")
    preview_url = detail.get("preview_url")
    if not preview_url:
        raise ValueError("Pixiv did not provide a public preview URL")
    if page:
        preview_url = re.sub(r"_p0(?=\.[A-Za-z0-9]+(?:\?|$))", f"_p{page}", preview_url)
    data, mime_type = _image_request(preview_url)
    return data, mime_type, detail["artwork_url"]


def _text_result(value: Any) -> dict[str, Any]:
    return {"content": [{"type": "text", "text": json.dumps(value, ensure_ascii=False, indent=2)}]}


def _call_tool(name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    if name == "search_pixiv":
        return _text_result(search_pixiv(arguments))
    if name == "get_pixiv_artwork":
        return _text_result(get_pixiv_artwork(arguments))
    if name == "search_pixiv_ranked":
        return _text_result(search_pixiv_ranked(arguments))
    if name == "preview_pixiv_artwork":
        data, mime_type, artwork_url = preview_pixiv_artwork(arguments)
        return {"content": [
            {"type": "image", "data": base64.b64encode(data).decode("ascii"), "mimeType": mime_type},
            {"type": "text", "text": artwork_url}
        ]}
    raise ValueError(f"Unknown tool: {name}")


def _respond(request_id: Any, result: Any = None, error: dict[str, Any] | None = None) -> None:
    payload: dict[str, Any] = {"jsonrpc": "2.0", "id": request_id}
    if error is not None:
        payload["error"] = error
    else:
        payload["result"] = result
    raw = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    sys.stdout.write(raw + "\n")
    sys.stdout.flush()


def _read_message() -> dict[str, Any] | None:
    while True:
        line = sys.stdin.readline()
        if not line:
            return None
        if len(line) > 10 * 1024 * 1024:
            raise ValueError("MCP message exceeded the 10 MB safety limit")
        if line.strip():
            return json.loads(line)


def main() -> None:
    while True:
        try:
            message = _read_message()
            if message is None:
                return
            method = message.get("method")
            request_id = message.get("id")
            if method == "initialize":
                _respond(request_id, {"protocolVersion": PROTOCOL_VERSION, "capabilities": {"tools": {}}, "serverInfo": {"name": "pixiv-browser", "version": "0.2.0"}})
            elif method == "notifications/initialized":
                continue
            elif method == "ping":
                _respond(request_id, {})
            elif method == "tools/list":
                _respond(request_id, {"tools": TOOLS})
            elif method == "tools/call":
                params = message.get("params") or {}
                try:
                    _respond(request_id, _call_tool(params.get("name", ""), params.get("arguments") or {}))
                except (ValueError, RuntimeError, urllib.error.HTTPError, urllib.error.URLError) as exc:
                    _respond(request_id, {"content": [{"type": "text", "text": f"Pixiv request failed: {exc}"}], "isError": True})
            elif request_id is not None:
                _respond(request_id, error={"code": -32601, "message": f"Method not found: {method}"})
        except Exception as exc:
            print(f"pixiv-browser server error: {exc}", file=sys.stderr, flush=True)


if __name__ == "__main__":
    main()
