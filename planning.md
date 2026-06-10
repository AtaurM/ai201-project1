# Project 1 Planning: The Unofficial Guide

<!-- > Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features. -->

---

## Domain

Student reviews of CS professors at Hunter College, covering the intro and core courses: CSCI127 (Intro to CS), CSCI135 (Software Analysis & Design 1), CSCI150 (Discrete Mathematics), CSCI160 (Computer Architecture 1), and CSCI260 (Computer Architecture 2). Official course descriptions don't tell you anything useful before picking a class. They won't tell you if the professor is hard to understand, if the TAs grade fairly, how much you'll need to self-study, or what the final actually looks like. Students figure this out through word of mouth and Rate My Professors, but that info is spread out and hard to search through.

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Melissa Lynch - CSCI127 | 14 student reviews of Lynch's Intro to CS section | documents/prof_lynch_csci127.txt |
| 2 | Melissa Lynch - CSCI160 | 15 student reviews of Lynch's Computer Architecture section | documents/prof_lynch_csci160.txt |
| 3 | Katherine St. John - CSCI127 | 15 student reviews of St. John's Intro to CS section | documents/prof_stjohn_csci127.txt |
| 4 | Tong Yi - CSCI135 | 15 student reviews of Yi's Software Analysis & Design 1 section | documents/prof_yi_csci135.txt |
| 5 | Gennadi Maryash - CSCI135 | 15 student reviews of Maryash's Software Analysis & Design 1 section | documents/prof_maryash_csci135.txt |
| 6 | Saad Mneimneh - CSCI150 | 15 student reviews of Mneimneh's Discrete Math section | documents/prof_mneimneh_csci150.txt |
| 7 | Susan Epstein - CSCI150 | 15 student reviews of Epstein's Discrete Math section | documents/prof_epstein_csci150.txt |
| 8 | Gennadi Maryash - CSCI160 | 15 student reviews of Maryash's Computer Architecture section | documents/prof_maryash_csci160.txt |
| 9 | Eric Schweitzer - CSCI160 | 13 student reviews of Schweitzer's Computer Architecture section | documents/prof_schweitzer_csci160.txt |
| 10 | Shostak - CSCI260 | 15 student reviews of Shostak's Computer Architecture 2 section | documents/prof_shostak_csci260.txt |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:** One review per chunk (no fixed character limit)

**Overlap:** None

**Reasoning:** Originally planned 400-character chunks with 50-character overlap. During testing, fixed-size chunking caused a retrieval failure where a mid-review chunk from Maryash's CSCI160 file ranked as the top result for a Shostak CSCI260 attendance query. The chunk had been split such that the professor header landed in the previous chunk, leaving an anonymous "Attendance: Mandatory" fragment that matched the query on surface keywords alone. Switching to review-boundary chunking fixes this: every chunk starts with the professor/course header line and contains exactly one complete review, so attribution context is always present. This reduced the total chunk count from 204 to 147.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:** all-MiniLM-L6-v2 via sentence-transformers (runs locally, no API key needed)

**Top-k:** 5

**Production tradeoff reflection:** all-MiniLM-L6-v2 is fast and free but it's a general-purpose model, not tuned for student reviews or CS course discussion. For a real deployment you'd weigh a few things: a larger model like text-embedding-3-large would probably rank review-specific phrasing better but adds API cost and latency per query. If the user base included a lot of non-native English speakers (which is realistic at Hunter), a multilingual model like multilingual-e5 would be worth considering. For this project the tradeoff is straightforward: local speed over raw accuracy.

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | What do students say about Melissa Lynch's grading in CSCI160? | Mixed reviews; recurring complaints about lateness, slow grading, and no email responses, but some students say she gives good partial credit and is fair |
| 2 | Is Maryash good for CSCI135 if you have no C++ experience? | Mixed; several reviews warn it's very tough without prior C++ background, others say he's fair |
| 3 | How important is attendance for Shostak's CSCI260? | Very important; he doesn't post slides online so missing class means missing content |
| 4 | What do students say about Mneimneh's teaching style in CSCI150? | Highly praised lecturer; students consistently say he explains proofs clearly and makes the material interesting |
| 5 | Do recent reviews recommend taking St. John for CSCI127? | Mostly negative in recent reviews; students cite cheating accusations, heavy workload, and poorly structured lectures |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. Review text is noisy and inconsistent. Students write in fragments, use slang, mix in personal anecdotes, and sometimes reference the course by nickname (e.g., "discrete" instead of CSCI150). The embedding model may rank these poorly or return off-topic chunks when the query uses formal course names.

2. Chunk boundaries may split a professor's name or course code from the actual review opinion. The metadata header (Quality, Difficulty, Course, Date) sits right above the review body with no blank line gap, so a chunk that starts mid-header won't have enough context to be useful for attribution.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

```
documents/*.txt
      |
      v
 ingest.py
 (load + strip blank lines)
      |
      v
 chunk_text()
 (400 char chunks, 50 char overlap)
      |
      v
 embed.py
 (all-MiniLM-L6-v2 via sentence-transformers)
      |
      v
 ChromaDB
 (local persistent vector store, collection: unofficial_guide)
      |
      v
 query.py -- retrieve top-5 chunks by cosine similarity
      |
      v
 Groq API
 (llama-3.3-70b-versatile, grounded system prompt)
      |
      v
 app.py
 (Gradio UI -- question in, answer + sources out)
```

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:** I'll give Claude the Chunking Strategy section and the Documents section and ask it to implement ingest.py with a chunk_text() function using the specified size and overlap. I'll verify by printing a sample of chunks and checking they're readable, not empty, and not merging reviews from different professors.

**Milestone 4 — Embedding and retrieval:** I'll give Claude the Retrieval Approach section and the ingest.py output and ask it to implement embed.py that stores embeddings in ChromaDB. I'll verify by running a manual retrieval query before wiring up the LLM, checking that the top results are actually relevant to the question.

**Milestone 5 — Generation and interface:** I'll give Claude the Architecture diagram and the system prompt I want to use and ask it to implement query.py and app.py. I'll verify by running a test question through the Gradio UI and confirming the answer cites sources and doesn't hallucinate outside the documents.
