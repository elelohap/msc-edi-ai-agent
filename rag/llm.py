from openai import OpenAI

client = OpenAI()

def _chunk_to_text(chunk) -> str:
    v = chunk.get("text", "")
    if isinstance(v, str):
        return v
    if isinstance(v, dict):
        # common keys in older pipelines
        for k in ("text", "content", "chunk", "page_content"):
            if k in v and isinstance(v[k], str):
                return v[k]
        # last resort: stringify dict (works, but less clean)
        return str(v)
    return str(v)

def ask_llm(question, context_chunks):
    context_text = "\n\n".join(_chunk_to_text(c) for c in context_chunks)

    prompt = f"""
Use ONLY the context below to answer the question.
If the answer is not in the context, say "The answer is not in the provided documents."

Context:
{context_text}

Question:
{question}
"""
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )
    return completion.choices[0].message.content
