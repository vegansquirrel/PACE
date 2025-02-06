def dynamic_chunker(text, chunk_size=3000, overlap=500):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size - overlap)]