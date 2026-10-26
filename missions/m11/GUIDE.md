# Self-study guide: Will this API change break the mobile app?

Mobile apps cannot be updated overnight, so a breaking API change becomes an incident for millions of users. Enterprises protect themselves with a contract check in CI that fails the build before anyone ships. Knowing exactly what counts as breaking, and what does not, is the core of API governance, and the same check protects every partner and internal team that calls the API.

## Revise first (in the course)

- strict API contracts and compatibility
- designing REST APIs clients can depend on
- turning a data contract into versioned models

## Read the email like an FDE

The manager defines 'breaking' precisely, and the definition is asymmetric. On responses, removing a field or changing its type breaks the app, but adding a field does not. On requests, changing a field's type breaks callers, and a new field breaks them only when it is required. Removing a whole endpoint always breaks. 'And nothing that isn't one' matters as much as finding them: a CI check that cries wolf gets switched off. The message format is fixed by the examples in the checks.

## Questions to ask the client first

- **How long must the API support version 1 after version 2 ships?** The deprecation window decides whether a breaking change can ever be accepted.
- **Are enum values part of the contract?** A new status value can break an app that switches on the old list.
- **Who can override the CI check, and how is that recorded?** Some breaks are intended; the override needs an owner and a trail.

## How each criterion is checked

1. **Every breaking change is found, and nothing else:** breaking_changes on the real v1 and v2 contracts must return exactly the expected five messages, word for word and sorted.
2. **Identical contracts have no breaking changes:** Comparing a contract with itself must return nothing.
3. **Additions alone are not breaking, changes are:** A small contract that only adds an optional request field and a response field must return nothing.
4. **The result is sorted:** The result must already be sorted.

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
| A new response field is reported | Response and request rules were treated the same. | Only removals and type changes break responses. |
| A new optional request field is reported | The required flag was not checked. | Report a new request field only when it is required. |
| Messages do not match | Quotes or wording differ from the examples. | Copy the format exactly, including the quotes around field names. |
| A removed endpoint also lists all its fields | The loop went on into the endpoint's fields. | Report the endpoint once and move to the next. |

## Test yourself before you check

- Diff the two contract files by eye and list the breaking changes before running your code.
- Run your check with the contracts swapped and think about what a downgrade would break.
- Add an optional request field to a copy of v1 and confirm nothing is reported.
- Change one response type in a copy and confirm exactly one message.

## What a senior reviewer also looks for

A reviewer would want the rules visible as separate, named checks (endpoint removed, response field removed, type changed, required request field added) so the API team can discuss each. They would also ask that CI prints the messages clearly and exits with an error code, because that is what blocks the merge.

## Stretch goal

Also detect a request field that changed from optional to required, and a response field that became optional (nullable), and decide with a comment whether each one breaks the mobile app.
