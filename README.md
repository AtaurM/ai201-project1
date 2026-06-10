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

```
You are a helpful assistant that answers questions about CS professors at Hunter College using student reviews.

Answer ONLY using the document excerpts provided below. Do not use any knowledge from your training data.
If the provided excerpts do not contain enough information to answer the question, respond with exactly:
"I don't have enough information on that."

Do not speculate, generalize, or fill in gaps with outside knowledge. Stick strictly to what the excerpts say.
```

The user message then passes the retrieved chunks formatted as `[Source: filename]\n{chunk text}` followed by the question. Temperature is set to 0.2 to reduce creative variance.

**How source attribution is surfaced in the response:** Source filenames are extracted programmatically from ChromaDB metadata at retrieval time and passed to the UI as a separate field-- the LLM never controls this. The UI displays them in a dedicated "Sources" box alongside the answer, so attribution is always present regardless of how the model phrases its response.

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What do students say about Melissa Lynch's grading in CSCI160? | Mixed; complaints about lateness and slow grading, but some say she gives good partial credit | Cited slow grading, no email responses, and clear grading criteria from different reviewers | Relevant | Accurate |
| 2 | Is Maryash good for CSCI135 if you have no C++ experience? | Mixed; some warn it's tough without C++ background, others say he's fair | "I don't have enough information on that."-- retriever returned CSCI160 chunks for Maryash instead of the CSCI135 reviews that mention C++ | Partially relevant | Inaccurate |
| 3 | How important is attendance for Shostak's CSCI260? | Very important; he doesn't post slides so missing class means missing content | Correctly explained attendance is technically optional but practically necessary since slides aren't posted | Relevant | Accurate |
| 4 | What do students say about Mneimneh's teaching style in CSCI150? | Highly praised by some; others find lectures unhelpful and grade heavily | Returned a balanced summary citing both strong praise and criticism from different reviewers | Relevant | Accurate |
| 5 | Do recent reviews recommend taking St. John for CSCI127? | Mostly negative in recent reviews; cheating accusations, heavy workload, poor lecture structure | Correctly identified recent reviews as mixed-to-negative, cited specific years and complaints | Relevant | Accurate |

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

**Question that failed:** "Is Maryash good for CSCI135 if you have no C++ experience?"

**What the system returned:** "I don't have enough information on that." -- even though `prof_maryash_csci135.txt` contains two reviews that explicitly mention C++ experience. All 5 retrieved chunks came from `prof_maryash_csci160.txt`.

**Root cause (tied to a specific pipeline stage):** This is a retrieval stage failure caused by course-level ambiguity. Maryash has files for both CSCI135 and CSCI160. The query asks about CSCI135 and C++, but the embedding model ranks the CSCI160 reviews as more semantically similar overall-- those reviews discuss studying and effort in ways that align with "is this professor good if you're struggling." The two reviews that mention C++ experience are in the CSCI135 file, but that specific phrasing doesn't dominate the chunk's embedding enough to outrank the CSCI160 chunks. The relevant content exists in the index but never reaches the top-5.

**What you would change to fix it:** Embed the course code as a stronger signal by repeating it inside the chunk body rather than only in the header. Alternatively, parse the course code out of the query and filter retrieved chunks by metadata before ranking, so a query that names CSCI135 never pulls CSCI160 chunks at all.

---

**Note-- a previously observed failure that was resolved:** An earlier version of the system used fixed-size 400-character chunks. This caused the top result for "How important is attendance for Shostak's CSCI260?" to be an anonymous mid-review chunk from `prof_maryash_csci160.txt` because the professor header had been split into the previous chunk. Switching to review-boundary chunking fixed this. See the Chunking Strategy section for details.

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

- *What I gave the AI:* The Chunking Strategy section from planning.md (400 char / 50 char overlap) and the document format, and asked Claude to implement `chunk_documents()` that loads all `.txt` files and splits them into overlapping chunks.
- *What it produced:* A working fixed-size character split with the specified size and overlap, plus preprocessing to strip blank lines.
- *What I changed or overrode:* After running retrieval tests, I observed that fixed-size chunking was splitting professor headers from review bodies, causing anonymous chunks to rank highly for wrong professors. I overrode the entire chunking approach to split on review boundaries (`Quality:` lines) instead, prepending the professor header to every chunk. This was a complete departure from the original spec, not just a parameter tweak.

**Instance 2**

- *What I gave the AI:* The Architecture diagram from planning.md, the desired system prompt behavior (answer only from context, cite sources, decline if not enough info), and the Gradio skeleton from the project spec.
- *What it produced:* Working `query.py` with a `retrieve()` and `ask()` function, and `app.py` with a Gradio UI including example questions.
- *What I changed or overrode:* I tightened the system prompt to explicitly say "Do not use any knowledge from your training data" rather than a softer suggestion, and set temperature to 0.2. I also moved source attribution to be programmatically extracted from ChromaDB metadata rather than relying on the LLM to include it in the response text.
