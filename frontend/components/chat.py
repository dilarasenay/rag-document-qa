import streamlit as st
from datetime import datetime
from api import api_post
from lang import t


def send_question(q: str, sel_files=None, k: int = 5):
    if not q.strip():
        return
    lang_instruction = t("lang_instruction")
    q_with_lang = f"{lang_instruction}\n\n{q}"

    st.session_state.chat_history.append({"role": "user", "content": q})

    with st.spinner(t("asking")):
        result = api_post("/ask", {
            "question": q_with_lang,
            "selected_files": sel_files if sel_files else [],
            "top_k": k
        })

    if result is None:
        content, sources, chunks = t("api_error"), [], []
    elif "error" in result:
        content, sources, chunks = f'❌ {result["error"]}', [], []
    else:
        content = result.get("answer", "")
        sources = result.get("sources", [])
        chunks = result.get("chunks", [])

    st.session_state.chat_history.append({
        "role": "assistant",
        "content": content,
        "sources": sources,
        "chunks": chunks
    })
    st.rerun()


def _export_chat() -> str:
    lines = [f"DocuMind — Sohbet Geçmişi\n{datetime.now().strftime('%d.%m.%Y %H:%M')}\n{'='*50}\n"]
    for msg in st.session_state.chat_history:
        role = t("you") if msg["role"] == "user" else t("ai")
        lines.append(f"[{role}]\n{msg['content']}\n")
        if msg.get("sources"):
            lines.append(f"Kaynaklar: {', '.join(msg['sources'])}\n")
        lines.append("-" * 40 + "\n")
    return "\n".join(lines)


def render_input(all_visible_docs: list):
    """Ayarlar paneli + soru giriş alanı."""
    st.markdown(f'<div class="dm-chat-label">{t("chat_header")}</div>', unsafe_allow_html=True)

    with st.expander(f"⚙ {t('settings')}", expanded=False):
        selected_files = st.multiselect(
            t("select_docs"),
            options=all_visible_docs,
            default=[],
            help=t("select_docs_hint"),
            key="sel_files"
        )
        top_k = st.slider(t("top_k"), 1, 10, 5, key="top_k_slider")

    q_col, btn_col = st.columns([6, 1])
    with q_col:
        question = st.text_input(
            "q",
            placeholder=t("chat_placeholder"),
            label_visibility="collapsed",
            key="question_field",
            value=st.session_state.get("pending_question") or ""
        )
    with btn_col:
        ask_clicked = st.button(f"→ {t('ask_btn')}", use_container_width=True, key="ask_btn")

    if st.session_state.get("pending_question"):
        st.session_state.pending_question = None

    if ask_clicked and question:
        send_question(question, selected_files if selected_files else [], top_k)


def render_history():
    """Sohbet geçmişi + temizle/dışa aktar butonları."""
    if not st.session_state.chat_history:
        return

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="bubble-wrap">
                <div class="bubble-label bubble-label-right">{t("you")}</div>
                <div style="display:flex;justify-content:flex-end;">
                    <div class="bubble-user">{msg["content"]}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="bubble-wrap">
                <div class="bubble-label">{t("ai")}</div>
                <div class="bubble-ai">{msg["content"]}</div>
            </div>
            """, unsafe_allow_html=True)

            if msg.get("sources"):
                tags = "".join([f'<span class="source-tag">📂 {s}</span>' for s in msg["sources"]])
                st.markdown(f'<div class="source-wrap"><span style="font-size:0.7rem;color:#888;font-weight:600;margin-right:8px;">{t("sources").upper()}</span> {tags}</div>', unsafe_allow_html=True)

            if msg.get("chunks"):
                with st.expander(f'🔍 {t("chunks_label")} ({len(msg["chunks"])})', expanded=False):
                    for i, chunk in enumerate(msg["chunks"]):
                        fn = chunk.get("metadata", {}).get("filename", "")
                        cid = chunk.get("metadata", {}).get("chunk_id", i)
                        score = chunk.get("score", 0)
                        content = chunk.get("content", "")
                        # Daha akıllı bir önizleme (ilk 300 karakter)
                        preview = content[:300] + ("..." if len(content) > 300 else "")
                        st.markdown(f"""
                        <div class="chunk-item">
                            <div class="chunk-header">
                                <span><b>{fn}</b> — {t("chunk_id")} #{cid}</span>
                                <span class="chunk-score">Relevance: {1/(1+score):.2%}</span>
                            </div>
                            <div style="font-style: italic; color: #666;">"{preview}"</div>
                        </div>
                        """, unsafe_allow_html=True)

    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
    bot_c1, bot_c2, _ = st.columns([2, 2, 4])
    with bot_c1:
        if st.button(f"🗑 {t('clear_btn')}", key="clear_chat"):
            st.session_state.chat_history = []
            st.rerun()
    with bot_c2:
        st.markdown('<div class="export-wrap">', unsafe_allow_html=True)
        st.download_button(
            label=f"↓ {t('export_btn')}",
            data=_export_chat(),
            file_name=f"documind_chat_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain",
            key="export_chat"
        )
        st.markdown('</div>', unsafe_allow_html=True)
