#!/usr/bin/env python3
"""Fetch and analyze MasterGo design file structure, tokens, and component data via DSL API."""

import json
import os
import re
import sys
import urllib.request
import urllib.error
from urllib.parse import urlparse, parse_qs
from typing import Optional


API_ENDPOINT = "https://mastergo.com"
TOKEN_ENV = "MASTERGO_TOKEN"
TIMEOUT = 30


def get_token() -> str:
    token = os.environ.get(TOKEN_ENV)
    if not token:
        print(json.dumps({"error": f"Environment variable {TOKEN_ENV} not set"}, ensure_ascii=False))
        sys.exit(1)
    return token


def resolve_short_link(url: str, token: str) -> Optional[str]:
    """Resolve a short link (/goto/xxx) to the actual file URL."""
    try:
        req = urllib.request.Request(
            url,
            headers={
                "Authorization": f"Bearer {token}",
                "User-Agent": "OpenClaw/1.0",
            },
            method="HEAD",
        )
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return resp.geturl()
    except Exception as e:
        return None


def parse_url(url: str) -> dict:
    """Extract fileId and layerId from MasterGo URL."""
    parsed = urlparse(url)

    # /file/YYYYYY?layer_id=XXX
    m = re.search(r'/file/(\d+)', parsed.path)
    file_id = m.group(1) if m else None

    # /goto/XXX — need to resolve
    m = re.search(r'/goto/([a-zA-Z0-9]+)', parsed.path)
    goto_id = m.group(1) if m else None

    layer_id = parse_qs(parsed.query).get("layer_id")
    layer_id = layer_id[0] if layer_id else None

    return {"fileId": file_id, "gotoId": goto_id, "layerId": layer_id}


def api_get(path: str, token: str) -> dict:
    """Call MasterGo REST API."""
    url = f"{API_ENDPOINT}{path}"
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "User-Agent": "OpenClaw/1.0",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        try:
            err_data = json.loads(body)
        except json.JSONDecodeError:
            err_data = {"body": body[:500]}
        return {"error": f"HTTP {e.code}", "detail": err_data}


def extract_texts(node: dict, texts: list):
    """Recursively extract text content from DSL nodes."""
    if node.get("type") == "TEXT" and node.get("characters"):
        texts.append({
            "id": node.get("id"),
            "name": node.get("name"),
            "text": node.get("characters"),
        })
    for child in node.get("children", []):
        extract_texts(child, texts)


def extract_colors(node: dict, colors: set):
    """Recursively extract color tokens."""
    style = node.get("style", {})
    for token_id, token_val in style.get("value", {}).items():
        if isinstance(token_val, str) and token_val.startswith("#"):
            colors.add(token_val)
    for child in node.get("children", []):
        extract_colors(child, colors)


def extract_navigations(node: dict, navs: list):
    """Recursively extract navigation interactions."""
    for action in node.get("interactive", []):
        if action.get("type") == "navigation" and action.get("targetLayerId"):
            navs.append({
                "sourceId": node.get("id"),
                "sourceName": node.get("name"),
                "targetLayerId": action["targetLayerId"],
            })
    for child in node.get("children", []):
        extract_navigations(child, navs)


def build_component_tree(node: dict, depth: int = 0) -> list:
    """Build a simplified human-readable component tree."""
    lines = []
    prefix = "  " * depth
    ntype = node.get("type", "?")
    name = node.get("name", "?")

    layout = node.get("layout", {})
    w = layout.get("width", {}).get("value", "?")
    h = layout.get("height", {}).get("value", "?")
    size = f" {w}x{h}" if w != "?" else ""

    text = node.get("characters", "")
    text_snippet = f" = \"{text[:60]}\"" if text else ""

    lines.append(f"{prefix}[{ntype}] {name}{size}{text_snippet}")

    for child in node.get("children", []):
        lines.extend(build_component_tree(child, depth + 1))

    return lines


def main():
    if len(sys.argv) < 2:
        print(f"Usage: python3 {sys.argv[0]} <mastergo_url>", file=sys.stderr)
        sys.exit(1)

    input_url = sys.argv[1]
    token = get_token()

    result = {"source": input_url, "source_type": "mastergo"}

    # Parse URL
    parsed = parse_url(input_url)
    result["parsed"] = parsed

    # Resolve short link if needed
    if parsed.get("gotoId"):
        resolved = resolve_short_link(input_url, token)
        if resolved:
            result["resolved_url"] = resolved
            parsed = parse_url(resolved)
            result["parsed"] = parsed

    file_id = parsed.get("fileId")
    if not file_id:
        result["error"] = "Could not extract fileId from URL"
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(1)

    # Get DSL data
    dsl_data = api_get(f"/api/design/file/{file_id}/dsl", token)
    if dsl_data.get("error"):
        result["error"] = dsl_data["error"]
        result["detail"] = dsl_data.get("detail")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(1)

    # Extract DSL root
    dsl_root = dsl_data.get("dsl", dsl_data)

    result["file_id"] = file_id

    # Tokens / design system
    local_styles = dsl_root.get("localStyleMap", {})
    result["tokens"] = {
        tid: {"name": t.get("name"), "type": t.get("type"), "value": t.get("value")}
        for tid, t in local_styles.items()
    }

    # Colors
    colors = set()
    for node in dsl_root.get("nodes", []):
        extract_colors(node, colors)
    if dsl_root.get("root"):
        extract_colors(dsl_root["root"], colors)
    result["colors"] = sorted(colors)

    # Texts
    texts = []
    for node in dsl_root.get("nodes", []):
        extract_texts(node, texts)
    if dsl_root.get("root"):
        extract_texts(dsl_root["root"], texts)
    result["texts"] = texts[:50]  # limit output

    # Navigations
    navs = []
    for node in dsl_root.get("nodes", []):
        extract_navigations(node, navs)
    if dsl_root.get("root"):
        extract_navigations(dsl_root["root"], navs)
    result["navigations"] = navs

    # Component tree (human readable)
    tree_lines = []
    for node in dsl_root.get("nodes", []):
        tree_lines.extend(build_component_tree(node))
    if dsl_root.get("root"):
        tree_lines.extend(build_component_tree(dsl_root["root"]))
    result["node_tree"] = "\n".join(tree_lines[:150])

    # Component doc links
    comp_links = dsl_data.get("componentDocumentLinks", [])
    if comp_links:
        result["component_doc_links"] = comp_links

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
