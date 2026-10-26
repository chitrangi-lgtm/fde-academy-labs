# Twelve supplier quotes, fast and polite

**From:** Ines Duarte, Platform Engineer, Halden Procurement

Our quote page calls twelve suppliers one after another and takes several seconds. Two suppliers sometimes hang. Suppliers have also complained that we hammer them, so we've agreed never to have more than four requests open at once. I need a function that gets every quote as fast as possible within that limit, gives up on a supplier after 0.2 seconds, and still returns the other quotes in the order we asked. `fetch_quote(supplier)` is provided and behaves like the real client.

## Done when

- `gather_quotes(suppliers, limit=4, timeout=0.2)` is a coroutine that returns one dict per supplier, in input order: {"supplier", "price"} or {"supplier", "error": "timeout"}
- Never more than `limit` calls to fetch_quote are in progress at the same time
- A slow supplier is given up after `timeout` seconds without failing the others
- The whole call finishes well under the time of calling suppliers one by one

## Files

none

`provided.py` holds code the client gives you; the checker runs it before your code.

## Work and check

Write your code in `solution.py`, then from the kit's folder run:

```bash
python tools/fde_check.py m05
```

There are no steps: how you build it is up to you. `GUIDE.md` explains how to read the email, how each criterion is checked and the common mistakes. If you are stuck, `NUDGES.md` has two hints and then the approach in plain English. The course site's version of this challenge records your score.
