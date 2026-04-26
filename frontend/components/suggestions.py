import streamlit as st
from api import api_post
from lang import t


def render_suggestions(active_docs: list, send_question_fn):
    if not active_docs:
        return

    st.markdown(
        f'<p style="font-size:0.75rem;color:#888;margin:0 0 6px;font-weight:600;letter-spacing:0.5px;">'
        f'{t("suggestions_title")}</p>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="suggestions-row">', unsafe_allow_html=True)
    sug_col1, sug_col2 = st.columns([4, 1], vertical_alignment="bottom")
    with sug_col1:
        selected_doc = st.selectbox(
            t("select_doc_for_suggestions"),
            options=active_docs,
            key="sug_doc_select",
            label_visibility="collapsed"
        )
    with sug_col2:
        st.markdown('<div class="regen-wrap">', unsafe_allow_html=True)
        regen_clicked = st.button(
            f"↺ {t('gen_suggestions')}",
            key="regen_sug",
            use_container_width=True
        )
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Doküman değiştiyse cache'i sıfırla
    if st.session_state.suggestions_for_doc != selected_doc:
        st.session_state.suggested_questions = []
        st.session_state.suggestions_for_doc = selected_doc

    should_generate = regen_clicked or not st.session_state.suggested_questions

    if should_generate:
        with st.spinner(t("gen_suggestions_spinner")):
            result = api_post("/ask", {
                "question": t("sug_prompt"),
                "selected_files": [selected_doc],
                "top_k": 8
            })
        if result and "answer" in result:
            lines = [
                q.strip()
                for q in result["answer"].strip().splitlines()
                if q.strip() and len(q.strip()) > 10
            ]
            st.session_state.suggested_questions = lines[:3]

    for i, sq in enumerate(st.session_state.suggested_questions):
        if st.button(f"💬 {sq}", key=f"sug_{i}", use_container_width=True):
            send_question_fn(sq, [selected_doc], 5)

    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
