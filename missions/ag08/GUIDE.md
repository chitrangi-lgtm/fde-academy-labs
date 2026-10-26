# Self-study guide: An MCP-style tool server that follows the protocol

The Model Context Protocol is becoming the standard way to expose enterprise systems to agents. SDKs hide the wire format until something breaks, and then the team that understands JSON-RPC fixes it in minutes. Knowing the difference between a protocol error and a tool error is also what lets an agent recover correctly.

## Revise first (in the course)

- JSON-RPC 2.0 and the MCP lifecycle
- building an MCP server
- a JSON-RPC 2.0 dispatcher

## Read the email like an FDE

The integration architect wants the protocol, not an SDK. Each message is one JSON-RPC 2.0 request; a message without an id is a notification and gets no reply at all. The criteria list the three methods to support and their exact results, and the error codes client libraries test for. The key distinction: a malformed call (unknown tool, missing claim id) is a protocol error, while a claim that does not exist is a normal result with isError true, because the model can act on it.

## Questions to ask the client first

- **Which protocol version do your agent clients speak?** Servers and clients must agree on the version at initialize.
- **Who is allowed to call get_claim, and how is that checked?** MCP carries requests; authorisation still has to happen somewhere.
- **Should claim details be minimised in the tool's reply?** Everything a tool returns goes into the model's context.

## How each criterion is checked

1. **initialize describes the server:** initialize must return the protocol version, the tools capability and the server's name and version.
2. **tools/list publishes the tool and its schema:** tools/list must publish get_claim with a description and an input schema that requires claim_id.
3. **tools/call returns text content:** tools/call for a known claim must return its status as text content with isError false.
4. **A tool-level failure is a result with isError:** tools/call for an unknown claim must return a result with isError true.
5. **Protocol errors use the right codes:** Bad JSON, an unknown method, missing arguments, an unknown tool and an invalid request must each return the right error code.
6. **A parse error has a null id; a notification gets no reply:** A parse error must carry a null id, and a notification must get no reply.

## How to work it

1. Read the email twice: once for the story, then with a pen, underlining every number, every rule and every 'must' or 'never'. Those words become the checks.
2. Turn the acceptance criteria into your own checklist, one line per criterion, and decide how you will see each one working before you build it.
3. Open the data files and the provided code before writing anything. Real files hold the awkward cases (blanks, duplicates, odd formats) the checks use.
4. Build the smallest piece that runs, print its result, and compare it with what you worked out by hand.
5. Add the next rule, run again, and keep each business rule in one obvious, named place.
6. Press Check only when your own prints agree with the criteria, then read each failing criterion's message before you change any code.
7. When it passes, read your code as the client's reviewer would, then compare it with the debrief.

## Common mistakes

| What you see | Why | Fix |
|---|---|---|
| A notification gets a reply | The id check came after dispatching. | Return None for messages without an id before dispatching. |
| An unknown claim is an error response | Tool failures were treated as protocol failures. | Return a result with isError true for a claim that does not exist. |
| The response is a dict | The handler returned Python objects. | Return the response as a JSON string. |
| A parse error has the wrong id | The id was read from a message that could not be parsed. | Use a null id for parse errors. |

## Test yourself before you check

- Write each request from the criteria as JSON by hand and send it through handle.
- Send a request with jsonrpc '1.0' and check the error.
- Send a notification and confirm nothing comes back.
- Compare your initialize result with the protocol's documentation.

## What a senior reviewer also looks for

A reviewer would check that the tool's schema is defined once and used for both listing and validation, that error messages never leak internal details, and that every call is logged with its method and outcome. They would also ask what happens when two requests share an id.

## Stretch goal

Add a second tool with its own schema and route tools/call through a small registry, so adding tools never changes the dispatch code.
