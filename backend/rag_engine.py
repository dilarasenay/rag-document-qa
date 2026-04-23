from openai import OpenAI
from embeddings import search
from config import OPENAI_API_KEY, LLM_MODEL, MAX_TOKENS

client = OpenAI(api_key=OPENAI_API_KEY)

def ask_question(question: str):
    relevant_chunks = search(question)

    if not relevant_chunks:
        return {
            "answer": "Henüz doküman yüklenmedi.",
            "sources": []
        }

    context = "\n\n".join([c["content"] for c in relevant_chunks])

    system_prompt = """
Sen bir doküman analiz asistanısın.
Sadece verilen bağlama göre cevap ver.
Eğer cevap bağlamda yoksa 'Bu bilgi dokümanda yok' de.
Türkçe cevap ver.
"""

    user_prompt = f"Bağlam:\n{context}\n\nSoru: {question}"

    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        max_tokens=MAX_TOKENS
    )

    answer = response.choices[0].message.content
    sources = list(set([c["metadata"]["filename"] for c in relevant_chunks]))

    return {
        "answer": answer,
        "sources": sources,
        "chunks": relevant_chunks
    }