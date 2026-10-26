# Self-study guide: Make a quote that cannot add up wrongly

Money bugs are the ones finance teams never forget: a total a cent out, a quote that mixed currencies, a discount nobody approved. Enterprise code prevents them by design, with value objects that cannot be built in an invalid state. This challenge is the pattern you will reuse in every billing, quoting and payments engagement.

## Revise first (in the course)

- dataclasses, frozen instances and type hints
- invariants: rules an object must never break
- a frozen Money value object with boundary validation

## Read the email like an FDE

Each complaint in the email maps to a rule. 'Totals that are a cent out' means binary floats are banned for money and rounding happens once, half up, at the end. 'Quotes with zero-quantity lines' means a line must refuse a quantity that is not a positive whole number when it is created. 'Mixed dollars and euros' means adding two amounts in different currencies must fail loudly, and a quote must hold one currency. 'Can't be changed after it's created' means immutability. 'Discounts up to 30 percent' is a limit to enforce, not a suggestion. The last sentence fixes the exact format finance expects from to_dict: the total as text with two decimals.

## Questions to ask the client first

- **Is the discount applied to the whole quote or line by line?** Rounding per line and rounding once give different totals, and finance will notice the cent.
- **Which currencies must be supported, and does a quote ever need conversion?** If conversion is ever needed, the rate and its date become part of the quote.
- **Who may approve a discount above 30 percent, if anyone?** Hard limits often have an approval path; the code should not block a legitimate exception forever.

## How each criterion is checked

1. **The total applies the discount:** A quote with a venue line and forty catering lines at a 10 percent discount must total exactly 1755.00 dollars, compared as Money, so both the amount and the currency must match.
2. **Rounding is half up to the cent:** Two small quotes test rounding at the half cent: half up means 0.225 becomes 0.23, where banker's rounding would give 0.22.
3. **Money of different currencies cannot be added:** Adding dollars to euros must raise ValueError, not return a result.
4. **Money cannot be changed after creation:** Setting the amount on an existing Money must raise an error, so the object has to be truly read-only.
5. **A zero or fractional quantity is rejected:** Creating a line with quantity 0 or 1.5 must raise ValueError.
6. **A discount above 30 percent is rejected:** A 35 percent discount must be refused when the quote is created.
7. **Mixed currencies in one quote are rejected:** A quote with one dollar line and one euro line must be refused when it is created.
8. **to_dict gives finance the total as text:** to_dict must give the total as the text '1755.00', the currency and the discount percentage.

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
| The total is 1754.99 or 1755.0000001 | Floats were used somewhere in the arithmetic. | Keep every amount in Decimal, created from text or integers, never from floats. |
| Rounding gives 0.22 instead of 0.23 | Python's round() uses banker's rounding. | Use Decimal's quantize with half-up rounding instead of round(). |
| Validation in __post_init__ fails on a frozen class | Assigning to self in a frozen dataclass raises an error. | Only read fields when validating; if you must normalise one, use object.__setattr__. |
| True is accepted as a quantity | bool is a subclass of int in Python. | Exclude bool explicitly when you check for a whole number. |

## Test yourself before you check

- Work the 1755.00 total out by hand first: 1200 + 40 × 18.75, minus 10 percent.
- Try every invalid input from the email in a quick loop and print which ones raise.
- Try to change an amount after creating a Money and confirm it fails.
- Print to_dict() and compare it with what finance asked for, field by field.

## What a senior reviewer also looks for

A senior reviewer would look for rounding in exactly one place, errors raised at construction with messages a sales operator could understand, and no float literal anywhere near money. They would also check that Quote does not let lines be swapped for another currency after creation, and that the discount rule is a named constant rather than a magic number repeated in two places.

## Stretch goal

Add tax per line with its own rounding rule, and a quote_from_dict that rebuilds a Quote from what to_dict produced, so invoicing can send it back for changes.
