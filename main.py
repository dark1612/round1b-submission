import os
import fitz 
import json

def extract_outline(pdf_path):
    doc = fitz.open(pdf_path)
   
    outline = [
        {'level': 'H1', 'text': 'Introduction', 'page': 1},
        {'level': 'H2', 'text': 'Overview', 'page': 2}
        
    ]
    title = doc.metadata.get('title', os.path.basename(pdf_path))
    return {'title': title, 'outline': outline}

def main():
    in_dir = 'input'
    out_dir = 'output'
    for fname in os.listdir(in_dir):
        if fname.endswith('.pdf'):
            outline = extract_outline(os.path.join(in_dir, fname))
            with open(os.path.join(out_dir, fname.replace('.pdf', '.json')), 'w', encoding='utf-8') as f:
                json.dump(outline, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()
