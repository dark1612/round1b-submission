# Adobe India Hackathon – Round 1A: PDF Outline Extractor

## 🚀 Challenge Theme
**Connecting the Dots Through Docs**

This solution extracts a structured outline from a given PDF file by identifying the document **title** and hierarchical **headings (H1, H2, H3)** with page numbers.

It is designed to run inside a Docker container and process all PDFs in the `/app/input` directory, outputting JSON results in `/app/output`.

---

## 📄 Output Format

```json
{
  "title": "Understanding AI",
  "outline": [
    { "level": "H1", "text": "Introduction", "page": 1 },
    { "level": "H2", "text": "What is AI?", "page": 2 },
    { "level": "H3", "text": "History of AI", "page": 3 }
  ]
}

Technologies Used

-Python 3.9

-PyMuPDF (fitz)

-Docker (AMD64 platform)