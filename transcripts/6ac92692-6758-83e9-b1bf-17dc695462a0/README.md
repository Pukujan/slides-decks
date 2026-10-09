# ChatGPT share archive

Source: https://chatgpt.com/share/6ac92692-6758-83e9-b1bf-17dc695462a0

`messages-*.jsonl` files contain the current shared branch in order. Each line is one original message record with its node ID, parent ID, children, and source message object. The archive includes user messages, visible assistant messages, assistant tool-call payloads, and tool outputs. `message-tree.json` records node relationships; `attachments.json` preserves every attachment pointer and its metadata; `archive-manifest.json` describes counts and files.

Private internal reasoning and system/developer messages are not included. The share endpoint exposed attachment references, but downloading the referenced binaries returned HTTP 401; the references and metadata are retained as-is.

To reconstruct the ordered JSONL stream, concatenate the `messages-*.jsonl` files in numeric order.
