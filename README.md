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

**Sample chunks:**

Chunk 1 — `prof_epstein_csci150.txt`
```
Professor: Susan Epstein | Course: CSCI150 | Source: Rate My Professors
Quality: 2.0 | Difficulty: 5.0 | Course: CSCI150 | Date: Dec 29th, 2025
Attendance: Mandatory | Grade: C
Tags: Get ready to read, Lots of homework, Lecture heavy
You will not learn anything from her slides, contains dense math. She is smart but can't teach. Slides have many mistakes. Homework questions are often confusing and there is no clear rubric what she wants. The grading is even worse, she wants specific things, only what she wants.
```

Chunk 2 — `prof_lynch_csci127.txt`
```
Professor: Melissa Lynch | Course: CSCI127 | Source: Rate My Professors
Quality: 1.0 | Difficulty: 4.0 | Course: CSCI127 | Date: Feb 2nd, 2026
Attendance: Mandatory | Grade: A+
She dont answer her emails. Shes either late 15-30 mins or doesn't even show up. Shes difficult to work with as a professor.
```

Chunk 3 — `prof_lynch_csci160.txt`
```
Professor: Melissa Lynch | Course: CSCI160 | Source: Rate My Professors
Quality: 1.0 | Difficulty: 3.0 | Course: CSCI160 | Date: May 29th, 2026
Attendance: Not Mandatory | Grade: B+
Tags: Graded by few things
Comes to class 30 minutes late, grades late, doesn't respond to emails, talks absolute nonsense to waste lecture time, and uploads review quizzes the night before exams, or not at all. She lied about the contents inside the final exam. The final was NOT commulative.
```

Chunk 4 — `prof_maryash_csci135.txt`
```
Professor: Gennadi Maryash | Course: CSCI135 | Source: Rate My Professors
Quality: 5.0 | Difficulty: 1.0 | Course: CSCI135 | Date: Feb 1st, 2023
Attendance: Not Mandatory | Would Take Again: Yes | Grade: A+
Tags: Clear grading criteria, Lots of homework, Respected
Maryash is the best CS professor in Hunter. He is actually caring and wants his students to pass. Like many, all he does is read the slides but his curriculum and coursework is doable. He is very good with partial credit, I failed every-time Tong Yi taught it, as soon as it changed to Maryash, I passed. Only drag is fail final you fail the course.
```

Chunk 5 — `prof_maryash_csci160.txt`
```
Professor: Gennadi Maryash | Course: CSCI160 | Source: Rate My Professors
Quality: 5.0 | Difficulty: 3.0 | Course: CSCI160 | Date: Jul 14th, 2024
Attendance: Mandatory | Would Take Again: Yes | Grade: A
Tags: Gives good feedback, Lots of homework, Lecture heavy
I had to retake but he uses the same tests and quiz altered a little bit. Failed because you have to remember the circuits for the finals and also score a 70 on the finals no matter your grade. Homeworks were literally blank files on gradescope and I got credit for them. Quizzes can have phone out. No cheat sheet.
```

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

## Retrieval Tests

**Query 1:** "What do students say about Mneimneh teaching style in CSCI150?"

Top 3 returned chunks (all from `prof_mneimneh_csci150.txt`, distances: 0.7851, 0.8041, 0.8127):
- Chunk starting: *"This professor should not be teaching, at least in this manner, the exam changes last second..."*
- Chunk starting: *"He is a bad teacher, bad orator, does not have enthusiasm for the class..."*
- Chunk starting: *"Challenging and time consuming, can't really go into his teaching style as I rarely went to the lectures..."*

**Why these are relevant:** All three chunks are from the correct file and directly discuss how Mneimneh teaches -- his lecture style, how he takes questions, and how students experience the class. The low distances (under 0.82) confirm strong semantic similarity. The query asked about teaching style and the chunks all contain first-hand opinions about exactly that.

---

**Query 2:** "How important is attendance for Shostak CSCI260?"

Top 3 returned chunks (all from `prof_shostak_csci260.txt`, distances: 0.8365, 0.9184, 0.9641):
- Chunk starting: *"If you have accommodations, dont take him. hes very difficult when it comes to accommodations"*
- Chunk starting: *"He is a decent professor with harsh grading criteria. You must pass the final... Attendance is not mandatory but you should go if you want to pass..."*
- Chunk starting: *"Do not take this course... he won't offer any additional outside help... doesn't post the slides on blackboard."*

**Why these are relevant:** All three chunks are from the correct file. Two of them directly address attendance and what happens when you miss class. The retriever correctly associated "attendance" and "CSCI260" with Shostak's file rather than pulling generic attendance-related chunks from other files -- a marked improvement over the original fixed-size chunking approach.

---

**Query 3:** "What do students say about Melissa Lynch grading in CSCI160?"

Top 3 returned chunks (distances: 0.4937, 0.4983, 0.5397):
- `prof_lynch_csci160.txt` — *"Comes to class 30 minutes late, grades late, doesn't respond to emails..."*
- `prof_lynch_csci160.txt` — *"A true gem of a professor. She wanted us to succeed. The grading criteria is very..."*
- `prof_lynch_csci127.txt` — *"She wasn't that bad throughout the semester aside from only explaining one concept..."*

The first two results are the right file and reflect the spread of opinions (negative vs positive). The third result pulls a Lynch CSCI127 chunk rather than another CSCI160 review, which is a minor miss -- but Lynch is still the right professor, so the answer won't be wrong, just slightly diluted by a different course's reviews.

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

**How source attribution is surfaced in the response:** Source filenames are extracted programmatically from ChromaDB metadata at retrieval time and passed to the UI as a separate field -- the LLM never controls this. The UI displays them in a dedicated "Sources" box alongside the answer, so attribution is always present regardless of how the model phrases its response.

**Example response 1:**

> *Query:* "How important is attendance for Shostak's CSCI260?"
>
> *Answer:* According to the excerpts, attendance is "Not Mandatory" for Professor Shostak's CSCI260 course, but it is highly recommended. Multiple reviews state that attending lectures is necessary to pass the course, as the professor does not post slides or other materials on Blackboard, and lectures provide important information for understanding the material and doing well on tests. One review says, "Lectures are not mandatory, but you need to attend them if you want to pass." Another review states, "Attendance is not mandatory but you should go if you want to pass..."
>
> *Sources:* prof_shostak_csci260.txt

**Example response 2:**

> *Query:* "What do students say about Mneimneh's teaching style in CSCI150?"
>
> *Answer:* According to the excerpts, students describe Mneimneh as a "bad teacher" and "bad orator" who lacks enthusiasm. His slides are described as just his notes, and he is "bad at taking questions." He relies almost entirely on students to self-study, and some say lectures are useless because he assumes prior knowledge of discrete math. A few students note that his class makes them think about mathematical concepts in a meaningful way and that paying close attention to lectures is helpful.
>
> *Sources:* prof_mneimneh_csci150.txt

**Out-of-scope query:**

> *Query:* "What is the capital of France?"
>
> *Answer:* I don't have enough information on that.
>
> *Sources:* prof_epstein_csci150.txt, prof_stjohn_csci127.txt, prof_yi_csci135.txt

The system correctly declines to answer and does not draw on general knowledge. The listed sources are the closest semantic matches in the index (irrelevant to the query), confirming the fallback is triggered by the grounding instruction, not by an absence of retrieved documents.

---

## Query Interface

The interface is a Gradio web app (`app.py`) running at `http://localhost:7860`.

**Input:** A single text box labeled "Ask a question" where the user types a free-form question about a Hunter College CS professor or course.

**Output:** Two text boxes displayed side by side:
- *Answer* — the LLM-generated response grounded in the retrieved reviews
- *Sources* — the filenames of the documents the retrieved chunks came from

**Example buttons:** 10 pre-written questions are shown at the bottom as clickable examples. Clicking one fills the input box; the user then clicks "Ask" or presses Enter to submit.

**Sample interaction:**

> *Input:* "How important is attendance for Shostak's CSCI260?"
>
> *Answer:* According to the excerpts, attendance is "Not Mandatory" for Professor Shostak's CSCI260 course, but it is highly recommended. Multiple reviews state that attending lectures is necessary to pass the course, as the professor does not post slides or other materials on Blackboard...
>
> *Sources:*
> • prof_shostak_csci260.txt

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

**One way the spec helped you during implementation:** The architecture diagram in planning.md laid out each pipeline stage with the specific tool at each step, which made it easy to implement and test each piece in isolation. When writing embed.py, knowing exactly what ingest.py was supposed to output (a list of dicts with `text` and `source` keys) meant there was no ambiguity about the interface between components. Without that pre-defined contract in the spec, it would have been easy to get mismatched data shapes between stages.

**One way your implementation diverged from the spec, and why:** The chunking strategy changed completely. The spec called for 400-character fixed-size chunks with 50-character overlap, but during retrieval testing we found that fixed-size chunking was splitting professor headers from review bodies. An anonymous mid-review chunk from the wrong professor was ranking as the top result for a Shostak query because it opened with "Attendance: Mandatory" and had no professor context. We switched to review-boundary chunking -- one complete review per chunk, always prefixed with the professor/course header -- which fixed the issue. The planning.md was updated to document the original approach, why it failed, and what changed.

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
