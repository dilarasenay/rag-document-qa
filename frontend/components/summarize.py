import streamlit as st
from api import api_post
from lang import t


def render_summarize(active_docs: list):
    st.markdown(f'<div class="dm-section">{t("summarize_header")}</div>', unsafe_allow_html=True)

    if not active_docs:
        st.info(t("no_docs"))
        return

    s_col1, s_col2 = st.columns([4, 1])
    with s_col1:
        sum_file = st.selectbox(
            "",
            options=active_docs,
            key="sum_file",
            label_visibility="collapsed"
        )
    with s_col2:
        if st.button(t("summarize_btn"), use_container_width=True, key="sum_btn"):
            with st.spinner(t("summarizing")):
                lang_instruction = t("lang_instruction")
                result = api_post("/ask", {
                    "question": f"{lang_instruction}\n\n{t('summarize_q')}",
                    "selected_files": [sum_file],
                    "top_k": 10
                })
            if result is None:
                st.error(t("api_error"))
            elif "error" in result:
                st.error(result["error"])
            else:
                st.session_state.chat_history.append({
                    "role": "user",
                    "content": f'📝 {t("summarize_btn")}: {sum_file}'
                })
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": result.get("answer", ""),
                    "sources": result.get("sources", []),
                    "chunks": result.get("chunks", [])
                })
                st.rerun()
