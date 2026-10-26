# Self-study guide: Semantic search with embeddings in NumPy

A help-centre search returns the same long FAQ page for every question. The team ranks documents by the dot product of their embedding vectors. embeddings.json holds six documents, each with its text and a short vector, and three example queries as vectors (login, refund and address). You show why the FAQ page always wins and rank by cosine similarity instead.

## Revise first (in the course)

- vector embeddings and the exact math of cosine similarity
- cosine similarity and top-k search from scratch
- vector search at scale

## Questions to ask the client first

- **Are your stored embeddings already normalised to length 1?** If they are, the dot product equals cosine and the bug lies elsewhere.
- **How long are the documents, and is the FAQ page much longer than the rest?** Long documents covering many topics are the usual cause of this pattern.
- **Do you have a set of real questions with the answers people expected?** Without them, nobody can say whether the new ranking is better.

## Ideas you will use

- **Dot product:** Multiplies two vectors element by element and adds the results. It grows with both the angle between the vectors and their lengths, so a long vector scores high against everything.
- **Vector length:** np.linalg.norm gives a vector's length. The starter prints each document's length: the FAQ page's vector is much longer than the others because it mentions every topic.
- **Cosine similarity:** The dot product divided by both lengths. It measures only the angle, so it ranks by direction (meaning) and ignores length. It runs from -1 to 1, and 1 means the same direction.
- **Top k:** Score every document against the query, sort from best to worst and keep the first k ids. With a few thousand documents this is fine; vector databases do the same thing faster at scale.

## Steps, check by check

1. **Perpendicular vectors have cosine 0:** Write cosine so that two perpendicular vectors give 0.
2. **Parallel vectors have cosine 1, whatever their length:** Make sure two vectors pointing the same way give 1 whatever their lengths, by dividing by both lengths.
3. **The login question finds the two sign-in documents:** Write top_k: score every document by cosine against the query and return the ids of the best k, best first. The login query should find the two sign-in documents.
4. **The refund question finds refunds and billing, not the FAQ page:** Check that the refund query now finds the refunds and billing documents, not the FAQ page.
5. **The address question's best match is the delivery document:** Check that the address query's best match is the delivery document.
6. **You found what the dot product picks for 'refund':** Rank the documents for the refund query by the plain dot product and store the winner in dot_winner.

## How to work it

1. The first run downloads Python and the lab's libraries into your browser (about 10 MB) and can take a minute; after that they are kept, and runs take a second or two.
2. Run the starter before changing anything: it prints the data and its types, which is where most surprises are.
3. Do one step at a time and print the result of each, comparing it with what you expect from the data.
4. Press Check my work after each step: the checks run in your browser, so they are free and instant.
5. When a check fails, read its name and message, then print the variable it looks at.
6. When everything passes, read the 'what the result means' section and write the two-sentence answer you would send the client: the number, what it means for them, and anything you excluded or assumed.
7. Open the reference solution only after you pass or after three real attempts, and look for one idea you did not use.

## When a check fails

If a ranking check fails, print every document's cosine score for that query, sorted. If cosine of parallel vectors is not 1, you divided by the wrong lengths or by one length only. If dot_winner is wrong, make sure you used the refund query and the dot product, not cosine, over all six documents.

## Common mistakes

| What you see | Why | Fix |
|---|---|---|
| Cosine of parallel vectors is 2.5 | Only the dot product was returned. | Divide by the product of both vectors' lengths. |
| Rankings come out reversed | Sorting was ascending. | Sort with the best score first. |
| top_k returns documents, not ids | The whole dictionaries were returned. | Return only the ids. |
| An error about shapes | Plain lists were mixed with arrays. | Convert vectors to NumPy arrays before multiplying. |

## What the result means for the client

The FAQ page won because its vector is long, not because it is relevant. Ranking by cosine, or normalising every embedding once when documents are indexed, fixes the help-centre search. Tell the team the fix is a one-line change at indexing time, and show them the before-and-after rankings for the three example questions.

## What to send the client

A note to the search team showing the before-and-after rankings for the three example questions, the length of the FAQ page's vector as the cause, and the one-line fix at indexing time.

## Stretch goal

Normalise every document vector once, rank by the plain dot product of normalised vectors, and confirm the rankings match cosine exactly. Then explain in a sentence why normalising at indexing time is cheaper than computing cosine for every query.
