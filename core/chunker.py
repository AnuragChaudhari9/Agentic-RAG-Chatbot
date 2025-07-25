import textwrap

def smart_chunk(text, max_length=400, min_length=100):
    chunks = []
    paragraphs = text.split("\n\n")
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        if len(para) <= max_length:
            chunks.append(para)
        else:
            wrapped = textwrap.wrap(para, width=max_length)
            chunks.extend(wrapped)
    return [c for c in chunks if len(c) >= min_length]
