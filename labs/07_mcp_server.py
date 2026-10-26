"""Lab 07 — Build an MCP server with the official Python SDK, then connect to it as a client.

Run:   docker compose exec labs python 07_mcp_server.py          (starts the server over stdio, then lists and calls its tools)
       docker compose exec labs python 07_mcp_server.py serve    (just the server, for any MCP client: the MCP Inspector,
                                                                  Claude Desktop or your own agent)
Try:   add a tool that writes (create_po_draft is here as an example) and give it readOnlyHint=False; break an argument's type
       and read the error the client gets; change get_stock's description and think about what a gateway should do (Module 8).

This is the browser lab GTX-142 (Module 15, client project cp-m15) with the real SDK: the SDK handles JSON-RPC, the
initialize handshake, tool schemas from type hints and validation, so your code is just the tools.
"""

from __future__ import annotations

import asyncio
import json
import re
import sys

from mcp.server.fastmcp import FastMCP

STOCK = {"YRN-30S-CTN": {"item": "Cotton yarn 30s", "qty": 1240, "unit": "kg"},
         "FAB-POPLIN-WHT": {"item": "White poplin", "qty": 860, "unit": "m"}}
SUPPLIERS = {"S1": {"name": "Navsari Spinners", "tax_id": "TX059173544", "bank_account": "001234567890"}}
DRAFTS: dict = {}

mcp = FastMCP("ganga-erp")


def item_code(value: str) -> str:
    """'yrn 30s ctn' -> 'YRN-30S-CTN'."""
    return re.sub(r"[\s_]+", "-", value.strip()).upper()


@mcp.tool()
def get_stock(item_code_text: str) -> dict:
    """Stock on hand for an item code such as YRN-30S-CTN (spaces and lower case are fine)."""
    found = STOCK.get(item_code(item_code_text))
    return found or {"error": f"no item {item_code(item_code_text)}"}


@mcp.tool()
def get_supplier(supplier_id: str) -> dict:
    """A supplier's details; the bank account is masked to its last 4 digits."""
    s = SUPPLIERS.get(supplier_id.strip().upper())
    return dict(s, bank_account="XXXXXXXX" + s["bank_account"][-4:]) if s else {"error": "no such supplier"}


@mcp.tool(annotations={"readOnlyHint": False})
def create_po_draft(supplier_id: str, item_code_text: str, quantity: int) -> dict:
    """Draft a purchase order for a buyer to approve in the ERP. It never approves anything."""
    draft = {"draft_id": f"DRAFT-{len(DRAFTS) + 1}", "supplier_id": supplier_id.upper(), "item_code": item_code(item_code_text),
             "quantity": quantity, "status": "awaiting_approval"}
    DRAFTS[draft["draft_id"]] = draft
    return draft


@mcp.resource("erp://suppliers/{supplier_id}")
def supplier_resource(supplier_id: str) -> str:
    """The supplier record as a resource the client can read (masked)."""
    return json.dumps(get_supplier(supplier_id))


async def client_demo() -> None:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    params = StdioServerParameters(command=sys.executable, args=[__file__, "serve"])
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            init = await session.initialize()
            print(f"connected to {init.serverInfo.name} (protocol {init.protocolVersion})")
            tools = await session.list_tools()
            for t in tools.tools:
                print(f"  tool {t.name}: {t.description.splitlines()[0]}  args={list(t.inputSchema.get('properties', {}))}")
            stock = await session.call_tool("get_stock", {"item_code_text": "yrn 30s ctn"})
            print("get_stock ->", stock.content[0].text)
            bad = await session.call_tool("create_po_draft", {"supplier_id": "S1", "item_code_text": "YRN-30S-CTN", "quantity": "lots"})
            print("create_po_draft with a bad quantity -> isError =", bad.isError)
            draft = await session.call_tool("create_po_draft", {"supplier_id": "S1", "item_code_text": "YRN-30S-CTN", "quantity": 500})
            print("create_po_draft ->", draft.content[0].text)
            res = await session.read_resource("erp://suppliers/S1")
            print("resource erp://suppliers/S1 ->", res.contents[0].text)
            assert "001234567890" not in res.contents[0].text, "the bank account must be masked"


if __name__ == "__main__":
    if sys.argv[1:] == ["serve"]:
        mcp.run()   # stdio transport
    else:
        asyncio.run(client_demo())
