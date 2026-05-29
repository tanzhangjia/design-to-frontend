#!/usr/bin/env python3
"""Fetch Figma file structure, node tree, colors, fonts and screenshot via REST API."""

import json
import os
import re
import sys
import urllib.request
import urllib.error


def get_file_key(url_or_key: str) -> str:
    if re.match(r'^[a-zA-Z0-9]{20,}$', url_or_key):
        return url_or_key
    m = re.search(r'/(?:file|site)/([a-zA-Z0-9]{20,})', url_or_key)
    if m:
        return m.group(1)
    m = re.search(r'/design/([a-zA-Z0-9]{20,})', url_or_key)
    if m:
        return m.group(1)
    raise ValueError(f"Cannot extract file key: {url_or_key}")


def extract_node_id(url: str) -> str | None:
    m = re.search(r'[?&]node-id=([\w%-]+)', url)
    return m.group(1) if m else None


def figma_api_get(path: str) -> dict:
    token = os.environ.get("FIGMA_TOKEN")
    if not token:
        print(json.dumps({"error": "FIGMA_TOKEN environment variable not set"}, ensure_ascii=False))
        sys.exit(1)

    url = f"https://api.figma.com/v1/{path}"
    req = urllib.request.Request(url, headers={
        "X-Figma-Token": token,
        "User-Agent": "OpenClaw/1.0",
    })
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        try:
            err_data = json.loads(body)
        except json.JSONDecodeError:
            err_data = {"body": body}
        return {"error": f"HTTP {e.code}", "detail": err_data}


def dump_node_tree(node: dict, depth: int = 0) -> list[str]:
    lines = []
    prefix = "  " * depth
    ntype = node.get("type", "?")
    name = node.get("name", "?")
    bounds = node.get("absoluteBoundingBox", {})
    size = f" {bounds.get('width','?')}x{bounds.get('height','?')}" if bounds else ""
    fills = node.get("fills", [])
    fill_info = ""
    for f in fills:
        if f.get("type") == "SOLID" and f.get("color"):
            c = f["color"]
            fill_info = f" fill:rgba({int(c['r']*255)},{int(c['g']*255)},{int(c['b']*255)},{c.get('a',1)})"
            break
    lines.append(f"{prefix}[{ntype}] {name}{size}{fill_info}")
    for child in node.get("children", []):
        lines.extend(dump_node_tree(child, depth + 1))
    return lines


def traverse_colors(node: dict, colors: set):
    for fill in node.get("fills", []):
        if fill.get("type") == "SOLID" and fill.get("color"):
            c = fill["color"]
            hex_str = f"#{int(c['r']*255):02x}{int(c['g']*255):02x}{int(c['b']*255):02x}"
            rgba = f"rgba({int(c['r']*255)},{int(c['g']*255)},{int(c['b']*255)},{c.get('a',1)})"
            colors.add((hex_str, rgba))
    for stroke in node.get("strokes", []):
        if stroke.get("type") == "SOLID" and stroke.get("color"):
            c = stroke["color"]
            hex_str = f"#{int(c['r']*255):02x}{int(c['g']*255):02x}{int(c['b']*255):02x}"
            rgba = f"rgba({int(c['r']*255)},{int(c['g']*255)},{int(c['b']*255)},{c.get('a',1)})"
            colors.add((hex_str, rgba))
    for child in node.get("children", []):
        traverse_colors(child, colors)


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/figma_fetch.py <figma_url_or_key>", file=sys.stderr)
        sys.exit(1)

    input_str = sys.argv[1]
    file_key = get_file_key(input_str)
    node_id = extract_node_id(input_str)

    result = {"file_key": file_key, "node_id": node_id, "source": input_str}

    file_data = figma_api_get(f"files/{file_key}")
    if file_data.get("error"):
        result["file_error"] = file_data["error"]
        result["file_type"] = "site_or_community"
    else:
        result["file_type"] = "standard"
        result["file_name"] = file_data.get("name", "")
        doc = file_data.get("document", {})
        result["pages"] = [
            {"name": p.get("name"), "type": p.get("type"), "children_count": len(p.get("children", []))}
            for p in doc.get("children", [])
        ]
        tree_lines = []
        for page in doc.get("children", [])[:3]:
            tree_lines.extend(dump_node_tree(page))
        result["node_tree"] = "\n".join(tree_lines[:120])

        color_set = set()
        for page in doc.get("children", []):
            traverse_colors(page, color_set)
        result["colors"] = [{"hex": h, "rgba": r} for h, r in sorted(color_set)]

    if node_id:
        images_result = figma_api_get(f"images/{file_key}?ids={node_id}&format=png&scale=2")
        if not images_result.get("error"):
            result["screenshot_url"] = images_result.get("images", {}).get(node_id)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
