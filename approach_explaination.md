# Round 1B: Approach Explanation

## Overview

The goal of Round 1B in the Adobe "Connecting the Dots" Hackathon is to design a scalable solution for multi-document PDF analysis. The task focuses on extracting contextually relevant information for different user personas and their specific needs across three separate document collections.

## Methodology

Our approach is designed around **semantic relevance scoring**, combining PDF parsing, text vectorization, and intelligent filtering to extract the most meaningful information tailored to the provided persona and task description. The pipeline involves the following key steps:

### 1. Input Handling

Each collection contains a set of PDFs and a JSON input file specifying:

* `persona`: who the user is
* `job_to_be_done`: what they are trying to achieve
* `documents`: a list of files with associated metadata

This JSON acts as the task driver, providing semantic context to compare against document content.

### 2. PDF Parsing

We use **PyMuPDF (fitz)** to extract structured text from each document along with page-level metadata. For every page, we:

* Extract blocks of text
* Detect and retain structural elements (e.g., headings)
* Clean and normalize content

### 3. Embedding for Semantic Understanding

We use `sentence-transformers` with the **MiniLM** model to encode:

* The task description (persona + job)
* Section headers or full paragraphs from each page

These embeddings allow us to measure the **semantic similarity** between the persona’s needs and document content.

### 4. Relevance Scoring and Ranking

We compute **cosine similarity scores** between the encoded task and document sections:

* Sections with the highest similarity scores are ranked as more relevant
* Top-ranked sections are selected for inclusion in the output
* We track page numbers and original titles

### 5. Output Generation

The final JSON output includes:

* `metadata`: reflecting the input context
* `extracted_sections`: top matches with document, section, page number, and rank
* `subsection_analysis`: deeper text content from matched pages

This structure ensures traceability while providing concise, actionable results.

## Why This Approach Works

* **Modular**: Works across varied PDF types (travel, recipes, technical)
* **Contextual**: Uses embeddings rather than keyword matching
* **Offline-Ready**: Can run fully containerized without internet
* **Scalable**: Easily extendable to new personas or use cases

## Docker Support

The solution is fully containerized using Docker. The Dockerfile sets up:

* Python environment
* Required libraries (`PyMuPDF`, `sentence-transformers`)
* Volume mounts to input/output directories

This ensures a consistent and portable execution setup across environments.

## Conclusion

By combining semantic embeddings, robust PDF parsing, and clean JSON formatting, our solution efficiently maps unstructured PDFs to persona-driven outcomes. It is flexible, context-aware, and built to handle real-world variability in documents.

---

**Word Count**: \~490
