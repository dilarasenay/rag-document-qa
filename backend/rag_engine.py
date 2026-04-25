from openai import OpenAI
from embeddings import search
from config import OPENAI_API_KEY, LLM_MODEL, MAX_TOKENS, TEMPERATURE, DEFAULT_TOP_K


def ask_question(question: str, selected_files=None, top_k: int = DEFAULT_TOP_K):
    """
    Kullanıcının sorusuna, yüklenen dokümanlardan bulunan ilgili parçaları kullanarak cevap üretir.
    """

    if not question or not question.strip():
        return {
            "answer": "Lütfen geçerli bir soru giriniz.",
            "sources": [],
            "chunks": []
        }

    if not OPENAI_API_KEY:
        return {
            "answer": "OpenAI API anahtarı bulunamadı. Lütfen .env dosyasını kontrol edin.",
            "sources": [],
            "chunks": []
        }

    try:
        client = OpenAI(api_key=OPENAI_API_KEY)

        relevant_chunks = search(
            query=question,
            selected_files=selected_files,
            top_k=top_k
        )

        if not relevant_chunks:
            return {
                "answer": "Henüz aktif doküman yok veya soruyla ilgili içerik bulunamadı.",
                "sources": [],
                "chunks": []
            }

        context = "\n\n---\n\n".join(
            [
                f"Kaynak: {chunk['metadata']['filename']} | Parça: {chunk['metadata']['chunk_id']}\n{chunk['content']}"
                for chunk in relevant_chunks
            ]
        )

        system_prompt = """
Sen bir doküman analiz asistanısın.
Sadece verilen bağlamdaki bilgilere dayanarak cevap ver.
Bağlamda olmayan bilgileri uydurma.
Eğer cevap bağlam içinde yoksa sadece "Bu bilgi dokümanda yok." de.
Cevabını açık, anlaşılır ve Türkçe ver.
"""

        user_prompt = f"""
Bağlam:
{context}

Soru:
{question}
"""

        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": system_prompt.strip()},
                {"role": "user", "content": user_prompt.strip()}
            ],
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE
        )

        answer = response.choices[0].message.content

        sources = list(
            {
                chunk["metadata"]["filename"]
                for chunk in relevant_chunks
            }
        )

        return {
            "answer": answer,
            "sources": sources,
            "chunks": relevant_chunks
        }

    except Exception as e:
        return {
            "answer": f"Soru cevaplama sırasında bir hata oluştu: {str(e)}",
            "sources": [],
            "chunks": []
        }