# Self-study guide: Review the deployment before the client's security team does

Client security teams reject deployments for the same handful of reasons every time. Turning their checklist into a check that runs in CI moves those findings to the day the code is written instead of the week of go-live. It is also how an FDE earns the trust of the platform team that owns the cluster.

## Revise first (in the course)

- hardened, multi-stage Dockerfiles
- a security linter for a Dockerfile and a Kubernetes manifest
- operating inside the client's IT organisation

## Read the email like an FDE

The security engineer gives you a fixed list of finding codes, and the acceptance criteria define each one precisely. Read them as rules: a missing USER line counts as root, so does switching back to root at the end; an untagged image counts as latest; probes and limits must both be present; a secret-looking variable is fine when it comes from a secret store and wrong when it holds a literal value. 'A fixed version so you can see both outcomes' means your check must report every code on one pair of files and nothing on the other.

## Questions to ask the client first

- **Are images pinned by digest in your cluster, or are version tags enough?** Some security teams require digests; a tag check alone would not satisfy them.
- **Which registries are allowed?** An allow-list of registries is often the next finding after tags.
- **Do init containers and sidecars need the same rules?** Checking only the main container leaves the others unreviewed.

## How each criterion is checked

1. **Every problem in the current files is reported:** review on the current Dockerfile and manifest must return all seven codes, sorted.
2. **The fixed files pass clean:** review on the fixed files must return nothing.
3. **An untagged base image counts as latest:** A Dockerfile whose base image has no tag must report LATEST_TAG.
4. **Switching back to root is caught:** A Dockerfile that switches back to root at the end must report ROOT_USER.
5. **Secrets from a secret store are fine:** An environment variable that takes a secret from a secret store must not be reported.

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
| A registry with a port counts as tagged | The colon in host:5000 was read as a tag. | Look for the tag only in the part after the last slash. |
| ROOT_USER is missed when root comes back later | Only the first USER line was read. | Judge the last USER line. |
| A secret from a secret store is reported | Every variable with a secret-like name was flagged. | Flag only variables that hold a literal value. |
| WRITABLE_ROOT_FS is missed when the setting is absent | Only an explicit false was flagged. | Anything other than true counts as writable. |

## Test yourself before you check

- Read the current files yourself and list the findings before running review.
- Run review on the fixed files and make sure the result is empty.
- Edit one line of the fixed Dockerfile at a time and watch exactly one code appear.
- Try a manifest with two containers where only the second has a problem.

## What a senior reviewer also looks for

A reviewer would want each code mapped to a short explanation and a fix, printed by CI, so developers can act without asking the security team. They would check that the parser tolerates lower-case instructions and comments, and that a missing section in the manifest is reported rather than crashing the check.

## Stretch goal

Print each finding with the file, the line or the container name, and a one-line fix, and make the script exit with an error code when anything is found, ready for a CI job.
