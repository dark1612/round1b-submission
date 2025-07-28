## 🔍 Problem Understanding

In Round 1B of the Adobe Hackathon, we were tasked with building a solution that takes:

* a collection of PDF documents,
* the structured outlines generated in Round 1A,
* a persona definition (role, job-to-be-done),

and returns a *ranked summary* of the most relevant sections across all documents tailored to that persona's needs.

---

## 🧩 Methodology

### 1. *Input Parsing*

Our pipeline begins by reading:

* PDFs and their respective outline JSONs (from Round 1A),
* an input.json file containing persona, job_to_be_done, and documents metadata.

This establishes the context and the search space for our ranking algorithm.

---

### 2. *Section Text Extraction*

Using the headings from Round 1A outlines, we segment each PDF into meaningful sections. These segments are created by grouping text blocks from one heading to the next based on their hierarchical level (H1 → H2 → H3). This provides both section-wise granularity and semantic grouping.

---

### 3. *Semantic Similarity Scoring*

We employed the lightweight yet effective all-MiniLM-L6-v2 model from *SentenceTransformers* to compute semantic embeddings for:

* Each document section
* The combined persona + job-to-be-done context

Cosine similarity is used to rank each section against the user need. This scoring method allows our model to prioritize content not just based on keyword matching, but true semantic relevance.

---

### 4. *Ranking & Filtering*

Sections are sorted by descending similarity score. To avoid redundancy and noise:

* Only top K (configurable) sections are selected
* A minimum similarity threshold filters out off-topic content

Optionally, we enrich the results with metadata such as document title and page number for traceability.

---

### 5. *Summary Generation*

The final collection_summary.json consolidates the selected sections into a persona-centric summary, with the following structure:

json
{
  "persona": { ... },
  "job_to_be_done": { ... },
  "summary": [
    {
      "document": "Doc1.pdf",
      "section_heading": "Travel Restrictions",
      "page_number": 4,
      "relevance_score": 0.84,
      "content": "..."
    },
    ...
  ]
}


---


## Output 

![Round1B](https://github.com/user-attachments/assets/9775021c-c303-4d88-979d-c3085b2c07df)


## ⚙ Design Highlights

* *Lightweight & Efficient*: The solution runs fully on CPU, ensuring low memory usage and fast execution.
* *Robust Across Domains*: Our model-agnostic approach works on guides, handbooks, and marketing PDFs alike.
* *Persona-Aware*: By embedding the persona + job-to-be-done into the relevance calculation, we achieve tailored, context-aware summaries.

---

## 🌟 Future Enhancements

* Use Named Entity Recognition (NER) to further annotate or filter content.
* Add section deduplication across documents.
* Integrate summarization models to create compressed versions of top-ranked sections.

---

This modular, persona-aware pipeline bridges unstructured PDF data with contextual user needs—delivering actionable intelligence from static documents.
