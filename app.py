import streamlit as st
import requests
from datetime import datetime

# =========================
# Sayfa Yapılandırması
# =========================
st.set_page_config(
    page_title="DocuMind",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_BASE = "http://127.0.0.1:8000"

# =========================
# Dil Paketi
# =========================
LANG = {
    "tr": {
        "title": "DocuMind",
        "tagline": "Dokümanlarınla konuş",
        "upload_header": "Dosya Yükle",
        "upload_label": "PDF, DOCX veya TXT",
        "upload_btn": "Yükle",
        "uploading": "Yükleniyor…",
        "upload_success": "yüklendi",
        "upload_error": "Yükleme hatası",
        "upload_empty": "Lütfen bir dosya seçin.",
        "upload_too_big": "Dosya çok büyük (max 50 MB).",
        "docs_header": "Dokümanlar",
        "docs_empty": "Henüz doküman yok.",
        "docs_refresh": "Yenile",
        "active": "Aktif",
        "passive": "Pasif",
        "toggle_btn": "Aç/Kapat",
        "delete_btn": "Sil",
        "preview_btn": "Önizle",
        "chat_header": "Sohbet",
        "chat_placeholder": "Bir soru yazın…",
        "ask_btn": "Gönder",
        "asking": "Yanıt aranıyor…",
        "sources": "Kaynaklar",
        "chunks_label": "İlgili parçalar",
        "no_docs": "⚠️ Önce bir doküman yükleyin.",
        "summarize_header": "Özet Al",
        "summarize_btn": "Özetle",
        "summarizing": "Özetleniyor…",
        "summarize_q": "Bu dokümanın tüm içeriğini kapsamlı şekilde özetle. Ana başlıkları, önemli bilgileri ve çıkarımları belirt.",
        "select_docs": "Arama yapılacak dokümanlar",
        "select_docs_hint": "Boş bırakılırsa hepsi aranır",
        "top_k": "Kullanılacak parça sayısı",
        "preview_title": "Önizleme",
        "close": "Kapat",
        "api_error": "Backend'e bağlanılamadı. Sunucunun çalıştığından emin ol.",
        "chunks_count": "parça",
        "lang_label": "Dil / Language",
        "export_btn": "Sohbeti Dışa Aktar",
        "clear_btn": "Sohbeti Temizle",
        "stats_total": "Toplam Doküman",
        "stats_chunks": "Toplam Parça",
        "stats_active": "Aktif",
        "example_q": "Örnek sorular",
        "ex1": "Bu doküman ne hakkında?",
        "ex2": "En önemli konular neler?",
        "ex3": "Kısaca özetle.",
        "settings": "Arama Ayarları",
        "score_label": "Benzerlik skoru",
        "you": "Siz",
        "ai": "DocuMind",
        "copied": "Kopyalandı!",
        "copy": "Kopyala",
        "chunk_from": "Kaynak",
        "chunk_id": "Parça",
        "score": "Skor",
        "gen_suggestions": "Öneri üretiliyor…",
        "suggestions_title": "Bu doküman için önerilen sorular",
        "select_doc_for_suggestions": "Doküman seçin",
    },
    "en": {
        "title": "DocuMind",
        "tagline": "Chat with your documents",
        "upload_header": "Upload File",
        "upload_label": "PDF, DOCX or TXT",
        "upload_btn": "Upload",
        "uploading": "Uploading…",
        "upload_success": "uploaded",
        "upload_error": "Upload error",
        "upload_empty": "Please select a file.",
        "upload_too_big": "File too large (max 50 MB).",
        "docs_header": "Documents",
        "docs_empty": "No documents yet.",
        "docs_refresh": "Refresh",
        "active": "Active",
        "passive": "Paused",
        "toggle_btn": "Toggle",
        "delete_btn": "Delete",
        "preview_btn": "Preview",
        "chat_header": "Chat",
        "chat_placeholder": "Type a question…",
        "ask_btn": "Send",
        "asking": "Searching…",
        "sources": "Sources",
        "chunks_label": "Relevant chunks",
        "no_docs": "⚠️ Upload a document first.",
        "summarize_header": "Summarize",
        "summarize_btn": "Summarize",
        "summarizing": "Summarizing…",
        "summarize_q": "Give a comprehensive summary of this document. Include main topics, key information and conclusions.",
        "select_docs": "Documents to search",
        "select_docs_hint": "Leave empty to search all",
        "top_k": "Chunks to use",
        "preview_title": "Preview",
        "close": "Close",
        "api_error": "Cannot connect to backend. Make sure the server is running.",
        "chunks_count": "chunks",
        "lang_label": "Dil / Language",
        "export_btn": "Export Chat",
        "clear_btn": "Clear Chat",
        "stats_total": "Total Docs",
        "stats_chunks": "Total Chunks",
        "stats_active": "Active",
        "example_q": "Example questions",
        "ex1": "What is this document about?",
        "ex2": "What are the key topics?",
        "ex3": "Give a brief summary.",
        "settings": "Search Settings",
        "score_label": "Similarity score",
        "you": "You",
        "ai": "DocuMind",
        "copied": "Copied!",
        "copy": "Copy",
        "chunk_from": "Source",
        "chunk_id": "Chunk",
        "score": "Score",
        "gen_suggestions": "Generating suggestions…",
        "suggestions_title": "Suggested questions for this document",
        "select_doc_for_suggestions": "Select document",
    }
}

# =========================
# Session State
# =========================
defaults = {
    "lang": "tr",
    "chat_history": [],
    "preview_content": None,
    "preview_filename": None,
    "question_input": "",
    "pending_question": None,
    "suggested_questions": [],
    "suggestions_for_doc": None,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

def t(key):
    return LANG[st.session_state.lang].get(key, key)

# =========================
# CSS
# =========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] > .main {
    background: #F7F5F0 !important;
    font-family: 'DM Sans', sans-serif !important;
    color: #1A1A1A !important;
}

[data-testid="stSidebar"] {
    background: #FFFFFF !important;
    border-right: 1px solid #E8E4DC !important;
    box-shadow: 2px 0 12px rgba(0,0,0,0.04) !important;
    min-width: 360px !important;
    max-width: 360px !important;
}

[data-testid="stSidebar"] > div:first-child {
    width: 360px !important;
}

/* ── Typography ── */
.dm-title {
    font-family: 'Instrument Serif', serif;
    font-size: 1.9rem;
    color: #1A1A1A;
    letter-spacing: -0.5px;
    line-height: 1.1;
    margin-bottom: 2px;
}
.dm-tagline {
    font-size: 0.8rem;
    color: #888;
    font-weight: 400;
    letter-spacing: 0.3px;
    margin-bottom: 0;
}
.dm-section {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    color: #888;
    margin: 1.4rem 0 0.6rem 0;
}
.dm-chat-label {
    font-family: 'Instrument Serif', serif;
    font-size: 1.5rem;
    color: #1A1A1A;
    margin-bottom: 1rem;
}

/* ── Stat Cards ── */
.stat-row {
    display: flex;
    gap: 8px;
    margin-bottom: 1rem;
}
.stat-card {
    flex: 1;
    background: #F7F5F0;
    border: 1px solid #E8E4DC;
    border-radius: 10px;
    padding: 10px 8px;
    text-align: center;
}
.stat-num {
    font-size: 1.3rem;
    font-weight: 600;
    color: #1A1A1A;
    line-height: 1;
}
.stat-lbl {
    font-size: 0.65rem;
    color: #888;
    font-weight: 500;
    letter-spacing: 0.3px;
    margin-top: 3px;
}

/* ── Document Cards ── */
.doc-card {
    background: #FFFFFF;
    border: 1px solid #E8E4DC;
    border-radius: 12px;
    padding: 11px 13px;
    margin-bottom: 8px;
    transition: border-color 0.15s, box-shadow 0.15s;
}
.doc-card:hover {
    border-color: #C8B99A;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
.doc-name {
    font-size: 0.82rem;
    font-weight: 600;
    color: #1A1A1A;
    font-family: 'DM Mono', monospace;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.doc-meta {
    font-size: 0.72rem;
    color: #888;
    margin-top: 3px;
    display: flex;
    align-items: center;
    gap: 6px;
}
.pill-active {
    display: inline-block;
    background: #E8F5E9;
    color: #2E7D32;
    border-radius: 20px;
    padding: 1px 8px;
    font-size: 0.65rem;
    font-weight: 600;
}
.pill-passive {
    display: inline-block;
    background: #F5F5F5;
    color: #888;
    border-radius: 20px;
    padding: 1px 8px;
    font-size: 0.65rem;
    font-weight: 600;
}

/* ── Chat Bubbles ── */
.bubble-wrap {
    margin-bottom: 1rem;
}
.bubble-user {
    background: #1A1A1A;
    color: #F7F5F0;
    border-radius: 18px 18px 4px 18px;
    padding: 12px 16px;
    font-size: 0.9rem;
    line-height: 1.55;
    margin-left: auto;
    max-width: 82%;
    width: fit-content;
}
.bubble-ai {
    background: #FFFFFF;
    color: #1A1A1A;
    border: 1px solid #E8E4DC;
    border-radius: 4px 18px 18px 18px;
    padding: 14px 16px;
    font-size: 0.9rem;
    line-height: 1.65;
    max-width: 92%;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
}
.bubble-label {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.5px;
    color: #AAA;
    margin-bottom: 4px;
    text-transform: uppercase;
}
.bubble-label-right {
    text-align: right;
}

/* ── Source Tags ── */
.source-wrap { margin: 8px 0 4px; }
.source-tag {
    display: inline-block;
    background: #FFF8F0;
    color: #A0522D;
    border: 1px solid #F0D9BC;
    border-radius: 20px;
    padding: 2px 10px;
    font-size: 0.72rem;
    font-family: 'DM Mono', monospace;
    margin: 2px 3px 2px 0;
}

/* ── Chunk Accordion ── */
.chunk-item {
    background: #FAFAF8;
    border: 1px solid #E8E4DC;
    border-left: 3px solid #C8B99A;
    border-radius: 0 8px 8px 0;
    padding: 9px 13px;
    margin: 5px 0;
    font-size: 0.78rem;
    font-family: 'DM Mono', monospace;
    color: #555;
    line-height: 1.5;
}
.chunk-header {
    font-size: 0.7rem;
    color: #888;
    margin-bottom: 5px;
    display: flex;
    gap: 12px;
}
.chunk-score {
    background: #F0EDE8;
    border-radius: 4px;
    padding: 1px 6px;
    font-size: 0.65rem;
    color: #666;
}

/* ── Preview ── */
.preview-box {
    background: #FFFFFF;
    border: 1px solid #E8E4DC;
    border-radius: 12px;
    padding: 18px 20px;
    font-size: 0.82rem;
    font-family: 'DM Mono', monospace;
    color: #444;
    line-height: 1.65;
    max-height: 420px;
    overflow-y: auto;
    white-space: pre-wrap;
}

/* ── Example Questions ── */
.ex-btn-wrap {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin: 10px 0 14px;
}

/* ── Streamlit component overrides ── */
.stButton > button {
    background: #FFFFFF !important;
    color: #1A1A1A !important;
    border: 1px solid #E8E4DC !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    padding: 5px 13px !important;
    transition: all 0.15s !important;
    box-shadow: none !important;
}
.stButton > button:hover {
    border-color: #C8B99A !important;
    background: #FAFAF8 !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06) !important;
}
.stButton > button:active {
    transform: scale(0.98) !important;
}

/* Primary action button */
div[data-testid="column"]:last-child .stButton > button,
.send-btn .stButton > button {
    background: #1A1A1A !important;
    color: #F7F5F0 !important;
    border-color: #1A1A1A !important;
}
div[data-testid="column"]:last-child .stButton > button:hover {
    background: #333 !important;
    border-color: #333 !important;
}

.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: #FFFFFF !important;
    border: 1px solid #E8E4DC !important;
    border-radius: 10px !important;
    color: #1A1A1A !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
    padding: 10px 14px !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #C8B99A !important;
    box-shadow: 0 0 0 3px rgba(200,185,154,0.15) !important;
}

.stSelectbox > div > div {
    background: #FFFFFF !important;
    border: 1px solid #E8E4DC !important;
    border-radius: 10px !important;
    color: #1A1A1A !important;
    font-family: 'DM Sans', sans-serif !important;
}

.stMultiSelect > div > div {
    background: #FFFFFF !important;
    border: 1px solid #E8E4DC !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
}

.stFileUploader > div {
    background: #FFFFFF !important;
    border: 2px dashed #E8E4DC !important;
    border-radius: 12px !important;
    transition: border-color 0.15s !important;
}
.stFileUploader > div:hover {
    border-color: #C8B99A !important;
}

div[data-testid="stExpander"] {
    background: #FFFFFF !important;
    border: 1px solid #E8E4DC !important;
    border-radius: 12px !important;
    box-shadow: none !important;
}
div[data-testid="stExpander"] summary {
    font-size: 0.83rem !important;
    font-weight: 500 !important;
    color: #555 !important;
}

.stSlider > div > div > div > div {
    background: #1A1A1A !important;
}

.stSuccess {
    background: #F0FFF4 !important;
    border: 1px solid #C6E8CC !important;
    color: #2D6A4F !important;
    border-radius: 10px !important;
    font-size: 0.85rem !important;
}
.stError {
    background: #FFF5F5 !important;
    border: 1px solid #FFD1D1 !important;
    color: #C0392B !important;
    border-radius: 10px !important;
    font-size: 0.85rem !important;
}
.stWarning {
    background: #FFFBF0 !important;
    border: 1px solid #FFE9A0 !important;
    border-radius: 10px !important;
    font-size: 0.85rem !important;
}
.stInfo {
    background: #F0F7FF !important;
    border: 1px solid #BDD7F5 !important;
    border-radius: 10px !important;
    font-size: 0.85rem !important;
}

/* Hide Streamlit branding */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* Regen butonu */
.regen-wrap {
    display: flex;
    align-items: flex-end;
    height: 100%;
    padding-top: 4px;
}
.regen-wrap button {
    background: #EEF2FF !important;
    border-color: #C7D2FE !important;
    color: #6366f1 !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    width: 100%;
}
.regen-wrap button:hover {
    background: #E0E7FF !important;
    border-color: #A5B4FC !important;
    color: #4F46E5 !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #D4CFC5; border-radius: 10px; }

hr { border: none; border-top: 1px solid #E8E4DC !important; margin: 1rem 0 !important; }
</style>
""", unsafe_allow_html=True)

# =========================
# API Helpers
# =========================
def api_get(endpoint):
    try:
        r = requests.get(f"{API_BASE}{endpoint}", timeout=10)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.ConnectionError:
        return None
    except Exception as e:
        return {"error": str(e)}

def api_post(endpoint, data=None, files=None):
    try:
        if files:
            r = requests.post(f"{API_BASE}{endpoint}", files=files, timeout=60)
        else:
            r = requests.post(f"{API_BASE}{endpoint}", json=data, timeout=60)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.ConnectionError:
        return None
    except Exception as e:
        return {"error": str(e)}

def api_delete(endpoint):
    try:
        r = requests.delete(f"{API_BASE}{endpoint}", timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"error": str(e)}

def get_documents():
    result = api_get("/documents")
    if result is None:
        return None
    return result.get("documents", {})

def get_stats(docs):
    if not docs:
        return 0, 0, 0
    visible = {fn: info for fn, info in docs.items() if not info.get("deleted", False)}
    total = len(visible)
    active = sum(1 for info in visible.values() if info.get("active", True))
    chunks = sum(info.get("chunks", 0) for info in visible.values())
    return total, active, chunks

def send_question(q, sel_files=None, k=5):
    if not q.strip():
        return
    lang = st.session_state.lang
    lang_instruction = "Cevabını Türkçe ver." if lang == "tr" else "Answer in English."
    q_with_lang = f"{lang_instruction}\n\n{q}"
    st.session_state.chat_history.append({"role": "user", "content": q})
    with st.spinner(LANG[lang].get("asking", "…")):
        result = api_post("/ask", {
            "question": q_with_lang,
            "selected_files": sel_files if sel_files else [],
            "top_k": k
        })
    if result is None:
        content = LANG[st.session_state.lang].get("api_error", "Error")
        sources, chunks = [], []
    elif "error" in result:
        content = f'❌ {result["error"]}'
        sources, chunks = [], []
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

def export_chat():
    lines = [f"DocuMind — Sohbet Geçmişi\n{datetime.now().strftime('%d.%m.%Y %H:%M')}\n{'='*50}\n"]
    for msg in st.session_state.chat_history:
        role = t("you") if msg["role"] == "user" else t("ai")
        lines.append(f"[{role}]\n{msg['content']}\n")
        if msg.get("sources"):
            lines.append(f"Kaynaklar: {', '.join(msg['sources'])}\n")
        lines.append("-" * 40 + "\n")
    return "\n".join(lines)

# =========================
# SIDEBAR
# =========================
with st.sidebar:
    # Logo + dil
    col_logo, col_lang = st.columns([3, 2])
    with col_logo:
        st.markdown("""
        <div style="
            font-family: 'Instrument Serif', serif;
            font-size: 1.75rem;
            letter-spacing: -0.5px;
            line-height: 1.1;
            margin-bottom: 2px;
            background: linear-gradient(135deg, #6c63ff 0%, #ff6b6b 50%, #43e97b 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        ">📚 DocuMind</div>
        <div style="font-size:0.78rem;color:#888;font-weight:400;letter-spacing:0.3px;">
            """ + t("tagline") + """
        </div>
        """, unsafe_allow_html=True)
    with col_lang:
        lang_pick = st.selectbox("", ["🇹🇷 TR", "🇬🇧 EN"],
            index=0 if st.session_state.lang == "tr" else 1,
            label_visibility="collapsed", key="lang_select")
        st.session_state.lang = "tr" if "TR" in lang_pick else "en"

    # Dil değişince önerileri sıfırla
    if "prev_lang" not in st.session_state:
        st.session_state.prev_lang = st.session_state.lang
    if st.session_state.prev_lang != st.session_state.lang:
        st.session_state.suggested_questions = []
        st.session_state.suggestions_for_doc = None
        st.session_state.prev_lang = st.session_state.lang

    st.markdown("---")

    # ── İstatistikler ──
    docs = get_documents()
    total, active_count, chunk_count = get_stats(docs)

    st.markdown(f"""
    <div class="stat-row">
        <div class="stat-card">
            <div class="stat-num">{total}</div>
            <div class="stat-lbl">{t("stats_total")}</div>
        </div>
        <div class="stat-card">
            <div class="stat-num">{active_count}</div>
            <div class="stat-lbl">{t("stats_active")}</div>
        </div>
        <div class="stat-card">
            <div class="stat-num">{chunk_count}</div>
            <div class="stat-lbl">{t("stats_chunks")}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Dosya Yükle ──
    st.markdown(f'<div class="dm-section">{t("upload_header")}</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        t("upload_label"),
        type=["pdf", "docx", "txt"],
        label_visibility="collapsed",
        key="file_uploader"
    )
    if st.button(f"↑ {t('upload_btn')}", use_container_width=True, key="upload_btn"):
        if uploaded_file is None:
            st.warning(t("upload_empty"))
        else:
            with st.spinner(t("uploading")):
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                result = api_post("/upload", files=files)
            if result is None:
                st.error(t("api_error"))
            elif "error" in result:
                st.error(f'{t("upload_error")}: {result["error"]}')
            else:
                st.success(f'✓ **{uploaded_file.name}** {t("upload_success")} — {result.get("chunks", 0)} {t("chunks_count")}')
                st.rerun()

    # ── Doküman Listesi ──
    st.markdown(f'<div class="dm-section">{t("docs_header")}</div>', unsafe_allow_html=True)

    if docs is None:
        st.error(t("api_error"))
    elif not any(not v.get("deleted", False) for v in docs.values()) if docs else True:
        st.caption(t("docs_empty"))
    else:
        for filename, info in docs.items():
            if info.get("deleted", False):
                continue
            is_active = info.get("active", True)
            pill = f'<span class="pill-active">{t("active")}</span>' if is_active else f'<span class="pill-passive">{t("passive")}</span>'

            st.markdown(f"""
            <div class="doc-card">
                <div class="doc-name">📄 {filename}</div>
                <div class="doc-meta">{info.get("chunks", 0)} {t("chunks_count")} &nbsp;·&nbsp; {pill}</div>
            </div>
            """, unsafe_allow_html=True)

            c1, c2, c3 = st.columns(3)
            with c1:
                if st.button(t("toggle_btn"), key=f"tog_{filename}", use_container_width=True):
                    api_post(f"/toggle_file/{filename}")
                    st.rerun()
            with c2:
                if st.button(t("preview_btn"), key=f"prv_{filename}", use_container_width=True):
                    with st.spinner("…"):
                        prv = api_get(f"/preview/{filename}")
                    if prv:
                        st.session_state.preview_content = prv.get("preview", "")
                        st.session_state.preview_filename = filename
                    st.rerun()
            with c3:
                if st.button(t("delete_btn"), key=f"del_{filename}", use_container_width=True):
                    api_delete(f"/remove_file/{filename}")
                    if st.session_state.preview_filename == filename:
                        st.session_state.preview_content = None
                        st.session_state.preview_filename = None
                    st.rerun()


# =========================
# ANA İÇERİK
# =========================
docs = get_documents()
active_docs = []
all_visible_docs = []
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

# ── Özet Al ──
st.markdown(f'<div class="dm-section">{t("summarize_header")}</div>', unsafe_allow_html=True)
if not active_docs:
    st.info(t("no_docs"))
else:
    s_col1, s_col2 = st.columns([4, 1])
    with s_col1:
        sum_file = st.selectbox("", options=active_docs, key="sum_file", label_visibility="collapsed")
    with s_col2:
        if st.button(t("summarize_btn"), use_container_width=True, key="sum_btn"):
            with st.spinner(t("summarizing")):
                lang_instruction = "Cevabını Türkçe ver." if st.session_state.lang == "tr" else "Answer in English."
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
                ans = result.get("answer", "")
                st.session_state.chat_history.append({
                    "role": "user",
                    "content": f'📝 {t("summarize_btn")}: {sum_file}'
                })
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": ans,
                    "sources": result.get("sources", []),
                    "chunks": result.get("chunks", [])
                })
                st.rerun()

st.markdown("---")

# ── Sohbet ──
st.markdown(f'<div class="dm-chat-label">{t("chat_header")}</div>', unsafe_allow_html=True)

# Ayarlar paneli
with st.expander(f"⚙ {t('settings')}", expanded=False):
    selected_files = st.multiselect(
        t("select_docs"),
        options=all_visible_docs,
        default=[],
        help=t("select_docs_hint"),
        key="sel_files"
    )
    top_k = st.slider(t("top_k"), 1, 10, 5, key="top_k_slider")

# Örnek sorular — doküman özelinde, AI üretimli, tıklanınca direkt gönderilir
if active_docs:
    st.markdown(f'<p style="font-size:0.75rem;color:#888;margin:0 0 6px;font-weight:600;letter-spacing:0.5px;">{t("suggestions_title")}</p>', unsafe_allow_html=True)

    sug_col1, sug_col2 = st.columns([4, 1])
    with sug_col1:
        selected_doc_for_sug = st.selectbox(
            t("select_doc_for_suggestions"),
            options=active_docs,
            key="sug_doc_select",
            label_visibility="collapsed"
        )
    with sug_col2:
        st.markdown('<div class="regen-wrap">', unsafe_allow_html=True)
        regen_clicked = st.button(f"↺ {t('gen_suggestions')}", key="regen_sug", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Doküman değiştiyse sıfırla — ama rerun yapma
    if st.session_state.suggestions_for_doc != selected_doc_for_sug:
        st.session_state.suggested_questions = []
        st.session_state.suggestions_for_doc = selected_doc_for_sug

    # Soru üretme — sadece gerçekten gerektiğinde
    should_generate = regen_clicked or not st.session_state.suggested_questions

    if should_generate:
        sug_prompt = (
            "Bu doküman hakkında kullanıcının sorabileceği, içerikle doğrudan ilgili "
            "3 farklı ve özgün soru üret. Soruları Türkçe yaz. "
            "Sadece soruları listele, başka hiçbir şey yazma. "
            "Her soruyu ayrı satıra yaz, numara veya tire kullanma."
        ) if st.session_state.lang == "tr" else (
            "Generate 3 specific, insightful questions a user might ask about this document. "
            "Write the questions in English. "
            "Only list the questions, nothing else. Each question on a new line, no numbers or dashes."
        )
        with st.spinner(t("gen_suggestions")):
            result = api_post("/ask", {
                "question": sug_prompt,
                "selected_files": [selected_doc_for_sug],
                "top_k": 8
            })
        if result and "answer" in result:
            lines = [q.strip() for q in result["answer"].strip().splitlines() if q.strip() and len(q.strip()) > 10]
            st.session_state.suggested_questions = lines[:3]

    # Soruları buton olarak göster
    for i, sq in enumerate(st.session_state.suggested_questions):
        if st.button(f"💬 {sq}", key=f"sug_{i}", use_container_width=True):
            send_question(sq, [selected_doc_for_sug], 5)

    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

# Mesaj geçmişi
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
            tags = "".join([f'<span class="source-tag">📎 {s}</span>' for s in msg["sources"]])
            st.markdown(f'<div class="source-wrap">{t("sources")}: {tags}</div>', unsafe_allow_html=True)

        if msg.get("chunks"):
            with st.expander(f'{t("chunks_label")} ({len(msg["chunks"])})', expanded=False):
                for i, chunk in enumerate(msg["chunks"]):
                    fn = chunk.get("metadata", {}).get("filename", "")
                    cid = chunk.get("metadata", {}).get("chunk_id", i)
                    score = chunk.get("score", 0)
                    content = chunk.get("content", "")
                    preview = content[:280] + ("…" if len(content) > 280 else "")
                    st.markdown(f"""
                    <div class="chunk-item">
                        <div class="chunk-header">
                            <span>{t("chunk_from")}: <b>{fn}</b></span>
                            <span>{t("chunk_id")}: {cid}</span>
                            <span class="chunk-score">{t("score")}: {score:.4f}</span>
                        </div>
                        {preview}
                    </div>
                    """, unsafe_allow_html=True)

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

# ── Soru Giriş Alanı ──
q_col, btn_col = st.columns([6, 1])
with q_col:
    question = st.text_input(
        "q",
        placeholder=t("chat_placeholder"),
        label_visibility="collapsed",
        key="question_field",
        value=st.session_state.pending_question or ""
    )
with btn_col:
    ask_clicked = st.button(f"→ {t('ask_btn')}", use_container_width=True, key="ask_btn")

# Pending question temizle
if st.session_state.pending_question:
    st.session_state.pending_question = None

if ask_clicked and question:
    send_question(question, selected_files if selected_files else [], top_k)

# Enter ile gönder (form trick)
if question and not ask_clicked:
    pass

# ── Alt Butonlar ──
if st.session_state.chat_history:
    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
    bot_c1, bot_c2, bot_c3 = st.columns([2, 2, 4])
    with bot_c1:
        if st.button(f"🗑 {t('clear_btn')}", key="clear_chat"):
            st.session_state.chat_history = []
            st.rerun()
    with bot_c2:
        chat_export = export_chat()
        st.download_button(
            label=f"↓ {t('export_btn')}",
            data=chat_export,
            file_name=f"documind_chat_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain",
            key="export_chat"
        )
