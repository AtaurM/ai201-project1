# The Unofficial Guide — Project 1

<!-- > **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit. -->

---

## Domain

Student reviews of CS professors at Hunter College, covering the intro and core courses: CSCI127 (Intro to CS), CSCI135 (Software Analysis & Design 1), CSCI150 (Discrete Mathematics), CSCI160 (Computer Architecture 1), and CSCI260 (Computer Architecture 2). Official course descriptions don't tell you anything useful before picking a class. They won't tell you if the professor is hard to understand, if the TAs grade fairly, how much you'll need to self-study, or what the final actually looks like. Students figure this out through word of mouth and Rate My Professors, but that info is spread out and hard to search through.

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | Melissa Lynch - CSCI127 | RMP reviews (14) | documents/prof_lynch_csci127.txt |
| 2 | Melissa Lynch - CSCI160 | RMP reviews (15) | documents/prof_lynch_csci160.txt |
| 3 | Katherine St. John - CSCI127 | RMP reviews (15) | documents/prof_stjohn_csci127.txt |
| 4 | Tong Yi - CSCI135 | RMP reviews (15) | documents/prof_yi_csci135.txt |
| 5 | Gennadi Maryash - CSCI135 | RMP reviews (15) | documents/prof_maryash_csci135.txt |
| 6 | Saad Mneimneh - CSCI150 | RMP reviews (15) | documents/prof_mneimneh_csci150.txt |
| 7 | Susan Epstein - CSCI150 | RMP reviews (15) | documents/prof_epstein_csci150.txt |
| 8 | Gennadi Maryash - CSCI160 | RMP reviews (15) | documents/prof_maryash_csci160.txt |
| 9 | Eric Schweitzer - CSCI160 | RMP reviews (13) | documents/prof_schweitzer_csci160.txt |
| 10 | Shostak - CSCI260 | RMP reviews (15) | documents/prof_shostak_csci260.txt |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:** One review per chunk (no fixed character limit)

**Overlap:** None

**Why these choices fit your documents:** Originally implemented 400-character fixed-size chunks with 50-character overlap. During retrieval testing, a mid-review chunk from a different professor ranked as the top result for a Shostak attendance query because the professor header had been split into the previous chunk, leaving an anonymous fragment that matched on surface keywords alone. Switching to review-boundary chunking means every chunk starts with the professor/course header and contains exactly one complete review, so the retriever always has attribution context. See Failure Case Analysis for the full breakdown.

**Final chunk count:** 147 (one per review, down from 204 with fixed-size chunking)

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:** all-MiniLM-L6-v2 via sentence-transformers (runs locally, no API key needed)

**Production tradeoff reflection:** all-MiniLM-L6-v2 is fast and free but it's a general-purpose model, not tuned for student reviews or CS course discussion. For a real deployment you'd weigh a few things: a larger model like text-embedding-3-large would probably rank review-specific phrasing better but adds API cost and latency per query. If the user base included a lot of non-native English speakers (which is realistic at Hunter), a multilingual model like multilingual-e5 would be worth considering. For this project the tradeoff is straightforward: local speed over raw accuracy.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

**How source attribution is surfaced in the response:**

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:** "How important is attendance for Shostak's CSCI260?"

**What the system returned:** The top retrieved chunk (distance: 0.8765) was from `prof_maryash_csci160.txt`, not Shostak. It opened with `60 | Date: Jan 3rd, 2024 / Attendance: Mandatory | Would Take Again: Yes` and contained no mention of Shostak or CSCI260.

**Root cause (tied to a specific pipeline stage):** This is a chunking stage failure. The chunk starts mid-review because the professor header was split into the previous chunk. With no professor name or course code present, the chunk is effectively anonymous-- it just looks like a generic "attendance is mandatory" fragment. The embedding model matched it to the query based on the word "Attendance: Mandatory" alone, with no context to distinguish it from Shostak's file.

**What you would change to fix it:** Chunk at review boundaries instead of fixed character counts. Each chunk should start at the `Quality:` metadata line of a review so the professor name and course always appear together with the review body. Alternatively, include the professor name and course as a metadata prefix on every chunk so the retriever always has that context even when a chunk falls mid-review.

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

**One way your implementation diverged from the spec, and why:**

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*

**Instance 2**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*
