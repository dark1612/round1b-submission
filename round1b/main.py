import os
import json
import fitz
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime

def load_persona_job(input_dir):
    # Assumes 'input.json' is the provided challenge1b_input.json
    path = os.path.join(input_dir, 'input.json')
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    persona = data.get("persona", {}).get("role", "")
    job = data.get("job_to_be_done", {}).get("task", "")
    return persona, job, data.get("documents", [])

def get_section_texts(pdf_file, outline):
    doc = fitz.open(pdf_file)
    sections = []
    headings = outline['outline']
    for i, h in enumerate(headings):
        start_page = h['page'] - 1  # fitz 0-based
        end_page = (headings[i+1]['page'] - 2) if i+1 < len(headings) else doc.page_count - 1
        text = ""
        for p in range(start_page, end_page+1):
            text += doc.load_page(p).get_text()
        sections.append({
            'heading': h['text'],
            'level': h['level'],
            'start_page': start_page+1,
            'end_page': end_page+1,
            'text': text,
        })
    return sections

def rank_sections(sections, query, model, filename):
    section_texts = [s['text'] for s in sections]
    section_embs = model.encode(section_texts)
    query_emb = model.encode([query])
    scores = cosine_similarity(section_embs, query_emb).flatten()
    for idx, score in enumerate(scores):
        sections[idx]['score'] = score
        sections[idx]['document'] = filename
    ranked = sorted(sections, key=lambda x: x['score'], reverse=True)
    return ranked

def extract_top_subsections(section, query, model, N=2):
    paras = [p for p in section['text'].split('\n\n') if len(p.strip()) > 30]
    if not paras:
        paras = [section['text']]
    para_embs = model.encode(paras)
    query_emb = model.encode([query])
    scores = cosine_similarity(para_embs, query_emb).flatten()
    top_idxs = np.argsort(-scores)[:N]
    return [paras[i] for i in top_idxs]

def main(input_dir='input', output_dir='output'):
    persona, job, documents = load_persona_job(input_dir)
    query = f"{persona} {job}"
    model = SentenceTransformer('all-MiniLM-L6-v2')
    timestamp = datetime.now().isoformat()

    all_sections = []
    all_documents = [doc["filename"] for doc in documents]
    # Gather and globally rank all sections from all PDFs
    for doc in documents:
        pdf_fn = doc["filename"]
        outline_json_fn = pdf_fn.replace('.pdf', '.json')
        pdf_path = os.path.join(input_dir, pdf_fn)
        outline_json_path = os.path.join(input_dir, outline_json_fn)
        if not os.path.exists(pdf_path) or not os.path.exists(outline_json_path):
            continue
        with open(outline_json_path, 'r', encoding='utf-8') as f:
            outline = json.load(f)
        sections = get_section_texts(pdf_path, outline)
        ranked_sections = rank_sections(sections, query, model, pdf_fn)
        for sec in ranked_sections:
            sec['document'] = pdf_fn
        all_sections.extend(ranked_sections)

    # Sort all sections by their score (global top N)
    all_sections = sorted(all_sections, key=lambda x: x.get('score', 0), reverse=True)
    top_n = 5  # Number of top sections for extracted_sections
    top_sections = all_sections[:top_n]

    # Assign importance rank
    for idx, sec in enumerate(top_sections):
        sec['importance_rank'] = idx + 1

    # Subsection analysis for each top section (can take multiple subsections per section)
    all_subsections = []
    for sec in top_sections:
        refined_subsections = extract_top_subsections(sec, query, model, N=2)
        for refined in refined_subsections:
            all_subsections.append({
                "document": sec['document'],
                "page_number": sec['start_page'],
                "refined_text": refined[:800]
            })

    output = {
        "metadata": {
            "input_documents": all_documents,
            "persona": persona,
            "job_to_be_done": job,
            "processing_timestamp": timestamp
        },
        "extracted_sections": [
            {
                "document": sec['document'],
                "section_title": sec['heading'],
                "importance_rank": sec['importance_rank'],
                "page_number": sec['start_page']
            } for sec in top_sections
        ],
        "subsection_analysis": all_subsections
    }

    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, 'collection_summary.json'), 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()
