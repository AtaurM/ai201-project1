# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

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

**Chunk size:**

**Overlap:**

**Reasoning:**

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**

**Top-k:**

**Production tradeoff reflection:**

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1.

2.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

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

**Milestone 3 — Ingestion and chunking:**

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
