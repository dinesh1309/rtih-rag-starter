# When is it RAG, and when is it not? (Block 2)

Slide-ready. Generic examples, no company names.

## What RAG actually does

RAG does **fuzzy meaning-search over text**. It embeds your question, finds the few text
chunks that look most similar in meaning, and hands them to the LLM to answer from.

So RAG fits only when **the answer is a passage of text sitting in a pile of documents,
and finding the right passage is the hard part.**

When the real task is something else, RAG is the wrong tool.

## Match the data to the verb

| The real task is to... | Right tool | Example data |
|---|---|---|
| **Retrieve** text from a pile of documents | RAG / Document Store | emails, PDFs, policy docs, support tickets, manuals |
| **Compute** over all structured rows | Text-to-SQL | accounting / ERP, invoices, inventory, sales tables |
| **Judge** an incoming item against a rule | Classification (rule in the prompt) | content moderation, spam detection, lead scoring |
| **Learn** patterns from raw signals | ML model training | sensor data, images, audio, clickstreams |

RAG only does the first row. The triage question to ask any founder:

> **"Is your answer buried in text — or do you need to calculate, decide, or learn?"**
> Only "buried in text" is RAG.

---

## Why financial / ERP data is NOT RAG

Questions like *"total receivables over 90 days?"*, *"sum of invoices for client X in Q2"*,
*"top 5 vendors by spend"*. Three reasons RAG breaks:

1. **It computes, it doesn't look up.** Those answers need to scan *all* the rows and do
   math (SUM, COUNT, GROUP BY, date filters). RAG only pulls the top few "most similar"
   chunks — it never sees the whole table, so it cannot add up thousands of invoices. It
   grabs a few that vaguely match the words and the LLM guesses. Wrong by design.
2. **Embeddings throw away the numbers.** Embedding turns `Invoice #4471: 84,320` into a
   fuzzy meaning-vector. Vectors capture topic, not exact value — `84,320` and `84,230`
   look almost identical. There is no "greater than", "between these dates", or "exactly
   equal" in similarity search.
3. **The data is already structured** — typed columns, dates, amounts. RAG would flatten
   that into text and destroy it. The right tool already exists: **SQL**. Text-to-SQL =
   the LLM writes the query, the database runs it (exact, complete, does the math),
   returns the precise number.

> Slide line: *RAG is a librarian — great at "find the document about X." A financial
> question needs an accountant — "add up these 4,000 numbers." Different job.*

## Why content moderation is NOT RAG

Task: every incoming message, is it OK or a violation? That is a **judgment about the new
item**, not a lookup of stored knowledge.

1. **Wrong question shape.** RAG answers "what does my knowledge say about X?" Moderation
   asks "does THIS message break the rule?" That is classification, not retrieval.
2. **You can't retrieve your way to a yes/no.** Storing toxic examples and retrieving the
   most similar one fails: toxicity is phrased in infinite new ways your examples never
   saw, and "similar" is not "violating" — a message can sit next to a stored insult but
   actually be a quote, satire, or someone reporting abuse. RAG gives you nearest stored
   text, never a verdict.
3. **The right design is the opposite of RAG.** Put the policy in the **system prompt** and
   ask the LLM to **classify** each message against it (category + reason). The policy is
   small and stable — nothing to search. It fits in the prompt.

> Slide line: *You don't check if something breaks the rules by finding a similar past
> thing. You read the rule and decide.*
