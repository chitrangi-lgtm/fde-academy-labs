# An MCP-style tool server that follows the protocol

**From:** Omar Farouk, Integration Architect, Pellucid Insurance

We want our claims system available to any agent through the Model Context Protocol. Before we adopt an SDK, I want the team to understand the wire protocol: write the message handler for a server with one tool, get_claim. It must speak JSON-RPC 2.0 correctly, including the error cases client libraries test for.

## Done when

- `handle(text)` takes one JSON-RPC message (a string) and returns the response as a string, or None for a notification (a message with no id)
- initialize -> result with protocolVersion "2025-06-18", capabilities {"tools": {}} and serverInfo {"name": "claims", "version": "1.0"}
- tools/list -> result {"tools": [{"name", "description", "inputSchema"}]}
- tools/call get_claim -> result {"content": [{"type": "text", "text": ...}], "isError": False}; an unknown claim -> isError True with a text explanation
- Errors: -32700 parse error (id null), -32600 invalid request (no jsonrpc "2.0" or no method), -32601 method not found, -32602 invalid params (unknown tool or missing claim_id)

## Files

none

`provided.py` holds code the client gives you; the checker runs it before your code.

## Work and check

Write your code in `solution.py`, then from the kit's folder run:

```bash
python tools/fde_check.py ag08
```

There are no steps: how you build it is up to you. `GUIDE.md` explains how to read the email, how each criterion is checked and the common mistakes. If you are stuck, `NUDGES.md` has two hints and then the approach in plain English. The course site's version of this challenge records your score.
