#!/usr/bin/env python3
"""Archive a public ChatGPT share as an ordered transcript and tool log.

The archive preserves user and visible assistant messages, assistant tool-call
payloads, tool outputs, attachment references, and the complete message-tree
metadata for the current shared branch. It excludes system messages and
private internal reasoning (thoughts/reasoning recap channels).

Usage:
  python extract_chatgpt_share.py SHARE_URL --output-dir archive
  python extract_chatgpt_share.py SHARE_URL --source-json saved-response.json

The share API may expose attachment references without granting access to the
underlying binary. In that case the references are retained in attachments.json.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


SHARE_ID_RE = re.compile(r"/share/([0-9a-fA-F-]{16,})")
PRIVATE_CONTENT_TYPES = {"thoughts", "reasoning_recap"}


def share_id_from(value: str) -> str:
    match = SHARE_ID_RE.search(value)
    if not match:
        raise ValueError("Expected a ChatGPT share URL containing /share/<id>.")
    return match.group(1)


def fetch_share(share_id: str, timeout: float) -> dict:
    url = f"https://chatgpt.com/backend-api/share/{share_id}"
    request = Request(url, headers={
        "Accept": "application/json",
        "User-Agent": "chatgpt-share-archive/1.0",
    })
    with urlopen(request, timeout=timeout) as response:
        raw = response.read()
        if response.status != 200:
            raise RuntimeError(f"Share endpoint returned HTTP {response.status}.")
    value = json.loads(raw)
    if not isinstance(value, dict):
        raise RuntimeError("Share endpoint returned an unexpected JSON shape.")
    return value


def current_branch(mapping: dict, tip: str) -> list[str]:
    ordered: list[str] = []
    seen: set[str] = set()
    current: str | None = tip
    while isinstance(current, str) and current in mapping and current not in seen:
        seen.add(current)
        ordered.append(current)
        node = mapping[current]
        current = node.get("parent") if isinstance(node, dict) else None
    ordered.reverse()
    return ordered


def attachment_refs(message: dict, node_id: str) -> list[dict]:
    refs: list[dict] = []
    content = message.get("content") or {}
    parts = content.get("parts") if isinstance(content, dict) else None
    if not isinstance(parts, list):
        return refs
    for index, part in enumerate(parts):
        if not isinstance(part, dict):
            continue
        kind = part.get("content_type", "")
        pointer = part.get("asset_pointer") or part.get("url")
        if pointer or "file" in kind or "image" in kind or "audio" in kind:
            refs.append({"node_id": node_id, "part_index": index, "part": part})
    return refs


def archive(share_id: str, source: dict) -> tuple[dict, list[dict], list[dict]]:
    mapping = source.get("mapping")
    tip = source.get("current_node")
    if not isinstance(mapping, dict) or not isinstance(tip, str):
        raise RuntimeError("Share response does not contain a message tree.")

    transcript: list[dict] = []
    tree: list[dict] = []
    attachments: list[dict] = []
    for node_id in current_branch(mapping, tip):
        node = mapping[node_id]
        if not isinstance(node, dict):
            continue
        # Retain tree structure and node-level metadata, except message content
        # for messages intentionally excluded from the publishable archive.
        message = node.get("message")
        if not isinstance(message, dict):
            tree.append({k: v for k, v in node.items() if k != "message"} | {"node_id": node_id})
            continue

        author = message.get("author") or {}
        role = author.get("role")
        content = message.get("content") or {}
        content_type = content.get("content_type")
        metadata = message.get("metadata") or {}
        channel = message.get("channel") or metadata.get("channel")

        # System/developer messages and private reasoning are not included.
        if role in {"system", "developer"} or content_type in PRIVATE_CONTENT_TYPES:
            continue
        if role not in {"user", "assistant", "tool"}:
            continue
        # Keep every tool call (assistant code) and tool result. For assistant
        # prose, only retain messages shown in the shared conversation.
        if role == "assistant" and content_type not in {"code", "execution_output"}:
            if metadata.get("is_visually_hidden_from_conversation"):
                continue
        record = {
            "node_id": node_id,
            "parent_id": node.get("parent"),
            "children": node.get("children", []),
            "message": message,
        }
        transcript.append(record)
        tree.append({k: v for k, v in record.items() if k != "message"})
        attachments.extend(attachment_refs(message, node_id))

    result = {
        "source_url": f"https://chatgpt.com/share/{share_id}",
        "share_id": share_id,
        "conversation_id": source.get("conversation_id"),
        "title": source.get("title"),
        "create_time": source.get("create_time"),
        "update_time": source.get("update_time"),
        "current_node": tip,
        "record_count": len(transcript),
        "records": transcript,
    }
    return result, tree, attachments


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("share_url", help="Public ChatGPT /share/ URL")
    parser.add_argument("--source-json", type=Path, help="Use an already-fetched share response")
    parser.add_argument("--output-dir", type=Path, default=Path("chatgpt-share-archive"))
    parser.add_argument("--timeout", type=float, default=30.0)
    args = parser.parse_args()
    try:
        share_id = share_id_from(args.share_url)
        if args.source_json:
            source = json.loads(args.source_json.read_text(encoding="utf-8"))
        else:
            source = fetch_share(share_id, args.timeout)
        full, tree, attachments = archive(share_id, source)
        out = args.output_dir
        out.mkdir(parents=True, exist_ok=True)
        write_json(out / "transcript.json", full)
        with (out / "messages.jsonl").open("w", encoding="utf-8") as stream:
            for record in full["records"]:
                stream.write(json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n")
        write_json(out / "message-tree.json", tree)
        write_json(out / "attachments.json", attachments)
        summary = {
            "source_url": full["source_url"],
            "record_count": full["record_count"],
            "roles": {},
            "content_types": {},
            "attachment_reference_count": len(attachments),
            "included": ["user messages", "visible assistant messages", "assistant tool-call payloads", "tool outputs", "attachment references"],
            "excluded": ["system/developer messages", "private thoughts and reasoning recap messages", "hidden assistant prose"],
        }
        for record in full["records"]:
            message = record["message"]
            role = (message.get("author") or {}).get("role", "unknown")
            kind = (message.get("content") or {}).get("content_type", "unknown")
            summary["roles"][role] = summary["roles"].get(role, 0) + 1
            summary["content_types"][kind] = summary["content_types"].get(kind, 0) + 1
        write_json(out / "archive-manifest.json", summary)
    except (ValueError, HTTPError, URLError, TimeoutError, RuntimeError,
            json.JSONDecodeError, OSError) as exc:
        print(f"Extraction failed: {exc}", file=sys.stderr)
        return 1

    print(f"Saved {full['record_count']} records and {len(attachments)} attachment references to {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
