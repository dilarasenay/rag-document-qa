import streamlit as st
from config import SESSION_DEFAULTS
from styles import inject_styles
from lang import t
from api import get_documents
from components.sidebar import render_sidebar
from components.summarize import render_summarize
from components.suggestions import render_suggestions
from components.chat import render_input, render_history, send_question

# =========================
# Sayfa Yapılandırması
# =========================
st.set_page_config(
    page_title="DocuMind",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# Session State
# =========================
for k, v in SESSION_DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

# =========================
# Styles
# =========================
inject_styles()

# =========================
# Sidebar
# =========================
render_sidebar()

# =========================
# Ana İçerik
# =========================
docs = get_documents()
active_docs, all_visible_docs = [], []
if docs:
    for fn, info in docs.items():
        if not info.get("deleted", False):
            all_visible_docs.append(fn)
            if info.get("active", True):
                active_docs.append(fn)

# ── Önizleme ──
if st.session_state.preview_content is not None:
    col_hdr, col_close = st.columns([5, 1])
    with col_hdr:
        st.markdown(f'<div class="dm-chat-label">📄 {st.session_state.preview_filename}</div>', unsafe_allow_html=True)
    with col_close:
        if st.button(t("close"), key="close_preview"):
            st.session_state.preview_content = None
            st.session_state.preview_filename = None
            st.rerun()
    st.markdown(f'<div class="preview-box">{st.session_state.preview_content}</div>', unsafe_allow_html=True)
    st.markdown("---")

# ── Özet ──
render_summarize(active_docs)

st.markdown("---")

# ── Önerilen Sorular ──
render_suggestions(active_docs, send_question)

st.markdown("---")

# ── Soru Giriş Alanı ──
render_input(all_visible_docs)

# ── Sohbet Geçmişi ──
render_history()
