import streamlit as st
import requests
import json

# =========================
# Sayfa Yapılandırması
# =========================
st.set_page_config(
    page_title="DocuMind | Doküman Asistanı",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# Sabitler
# =========================
API_BASE = "http://127.0.0.1:8000"

# =========================
# Dil Desteği
# =========================
LANG = {
    "tr": {
        "title": "📚 DocuMind",
        "subtitle": "Akıllı Doküman Asistanı",
        "upload_header": "📁 Dosya Yükle",
        "upload_label": "PDF, DOCX veya TXT yükleyin",
        "upload_btn": "Yükle",
        "uploading": "Yükleniyor...",
        "upload_success": "✅ başarıyla yüklendi!",
        "upload_error": "❌ Yükleme hatası",
        "upload_empty": "Lütfen bir dosya seçin.",
        "docs_header": "📂 Yüklü Dokümanlar",
        "docs_empty": "Henüz doküman yüklenmedi.",
        "docs_refresh": "🔄 Yenile",
        "toggle_active": "✅ Aktif",
        "toggle_passive": "⏸ Pasif",
        "toggle_btn": "Değiştir",
        "delete_btn": "🗑 Sil",
        "preview_btn": "👁 Önizle",
        "chat_header": "💬 Soru-Cevap",
        "chat_placeholder": "Dokümanlar hakkında bir soru sorun...",
        "ask_btn": "Sor",
        "asking": "Cevap aranıyor...",
        "sources_label": "📌 Kaynaklar",
        "chunks_label": "🔍 İlgili Parçalar",
        "no_docs_warning": "⚠️ Önce bir doküman yükleyin.",
        "summarize_header": "📝 Özet Al",
        "summarize_btn": "Özet Oluştur",
        "summarizing": "Özetleniyor...",
        "summarize_prompt": "Bu dokümanı kısaca özetle.",
        "select_files": "Arama yapılacak dokümanları seçin (boş = hepsi):",
        "top_k": "Kaç parça kullanılsın?",
        "preview_header": "📄 Doküman Önizlemesi",
        "preview_close": "Kapat",
        "api_error": "❌ Backend'e bağlanılamadı. Sunucunun çalıştığından emin olun.",
        "chunks_count": "parça",
        "status": "Durum",
        "language_label": "🌐 Dil / Language",
        "ask_empty": "Lütfen bir soru girin.",
    },
    "en": {
        "title": "📚 DocuMind",
        "subtitle": "Intelligent Document Assistant",
        "upload_header": "📁 Upload File",
        "upload_label": "Upload PDF, DOCX or TXT",
        "upload_btn": "Upload",
        "uploading": "Uploading...",
        "upload_success": "✅ uploaded successfully!",
        "upload_error": "❌ Upload error",
        "upload_empty": "Please select a file.",
        "docs_header": "📂 Uploaded Documents",
        "docs_empty": "No documents uploaded yet.",
        "docs_refresh": "🔄 Refresh",
        "toggle_active": "✅ Active",
        "toggle_passive": "⏸ Passive",
        "toggle_btn": "Toggle",
        "delete_btn": "🗑 Delete",
        "preview_btn": "👁 Preview",
        "chat_header": "💬 Q&A Chat",
        "chat_placeholder": "Ask a question about your documents...",
        "ask_btn": "Ask",
        "asking": "Searching for answer...",
        "sources_label": "📌 Sources",
        "chunks_label": "🔍 Relevant Chunks",
        "no_docs_warning": "⚠️ Please upload a document first.",
        "summarize_header": "📝 Summarize",
        "summarize_btn": "Generate Summary",
        "summarizing": "Summarizing...",
        "summarize_prompt": "Briefly summarize this document.",
        "select_files": "Select documents to search (empty = all):",
        "top_k": "How many chunks to use?",
        "preview_header": "📄 Document Preview",
        "preview_close": "Close",
        "api_error": "❌ Cannot connect to backend. Make sure the server is running.",
        "chunks_count": "chunks",
        "status": "Status",
        "language_label": "🌐 Dil / Language",
        "ask_empty": "Please enter a question.",
    }
}

# =========================
# Session State
# =========================
if "lang" not in st.session_state:
    st.session_state.lang = "tr"
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "preview_content" not in st.session_state:
    st.session_state.preview_content = None
if "preview_filename" not in st.session_state:
    st.session_state.preview_filename = None

def t(key):
    return LANG[st.session_state.lang][key]

# =========================
# CSS Stilleri
# =========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg: #0f0f13;
    --surface: #17171f;
    --surface2: #1e1e2a;
    --border: #2a2a3a;
    --accent: #6c63ff;
    --accent2: #ff6b6b;
    --accent3: #43e97b;
    --text: #e8e8f0;
    --text-muted: #7a7a9a;
    --radius: 12px;
}

html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Sora', sans-serif !important;
}

[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}

.main-title {
    font-size: 2.6rem;
    font-weight: 700;
    background: linear-gradient(135deg, #6c63ff 0%, #ff6b6b 50%, #43e97b 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -1px;
    margin-bottom: 0;
}

.subtitle {
    color: var(--text-muted);
    font-size: 0.95rem;
    font-weight: 300;
    margin-top: 4px;
    letter-spacing: 0.5px;
}

.section-header {
    font-size: 1rem;
    font-weight: 600;
    color: var(--text);
    letter-spacing: 0.5px;
    padding: 10px 0 8px 0;
    border-bottom: 1px solid var(--border);
    margin-bottom: 14px;
}

.doc-card {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 12px 14px;
    margin-bottom: 10px;
    transition: border-color 0.2s;
}

.doc-card:hover {
    border-color: var(--accent);
}

.doc-name {
    font-size: 0.88rem;
    font-weight: 600;
    color: var(--text);
    font-family: 'JetBrains Mono', monospace;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.doc-meta {
    font-size: 0.75rem;
    color: var(--text-muted);
    margin-top: 2px;
}

.badge-active {
    display: inline-block;
    background: rgba(67, 233, 123, 0.15);
    color: #43e97b;
    border: 1px solid rgba(67, 233, 123, 0.3);
    border-radius: 20px;
    padding: 2px 10px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.5px;
}

.badge-passive {
    display: inline-block;
    background: rgba(122, 122, 154, 0.15);
    color: var(--text-muted);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 2px 10px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.5px;
}

.chat-bubble-user {
    background: linear-gradient(135deg, #6c63ff22, #6c63ff11);
    border: 1px solid #6c63ff44;
    border-radius: var(--radius) var(--radius) 4px var(--radius);
    padding: 12px 16px;
    margin: 8px 0;
    font-size: 0.92rem;
    color: var(--text);
}

.chat-bubble-ai {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 4px var(--radius) var(--radius) var(--radius);
    padding: 14px 16px;
    margin: 8px 0;
    font-size: 0.92rem;
    color: var(--text);
    line-height: 1.6;
}

.source-tag {
    display: inline-block;
    background: rgba(108, 99, 255, 0.15);
    color: #a09af0;
    border: 1px solid rgba(108, 99, 255, 0.3);
    border-radius: 20px;
    padding: 3px 12px;
    font-size: 0.75rem;
    font-family: 'JetBrains Mono', monospace;
    margin: 3px 3px 3px 0;
}

.chunk-box {
    background: var(--surface);
    border: 1px solid var(--border);
    border-left: 3px solid var(--accent);
    border-radius: 0 var(--radius) var(--radius) 0;
    padding: 10px 14px;
    margin: 6px 0;
    font-size: 0.82rem;
    font-family: 'JetBrains Mono', monospace;
    color: var(--text-muted);
    line-height: 1.5;
}

.preview-box {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 16px;
    font-size: 0.85rem;
    font-family: 'JetBrains Mono', monospace;
    color: var(--text-muted);
    line-height: 1.6;
    max-height: 400px;
    overflow-y: auto;
    white-space: pre-wrap;
}

.stButton > button {
    background: var(--surface2) !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    font-family: 'Sora', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    padding: 6px 14px !important;
    transition: all 0.2s !important;
}

.stButton > button:hover {
    border-color: var(--accent) !important;
    color: #a09af0 !important;
}

.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-family: 'Sora', sans-serif !important;
}

.stSelectbox > div > div {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
}

.stFileUploader > div {
    background: var(--surface2) !important;
    border: 1px dashed var(--border) !important;
    border-radius: var(--radius) !important;
}

.stMultiSelect > div > div {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
}

.stSpinner > div {
    border-top-color: var(--accent) !important;
}

div[data-testid="stExpander"] {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
}

.stSuccess {
    background: rgba(67, 233, 123, 0.1) !important;
    border: 1px solid rgba(67, 233, 123, 0.3) !important;
    color: #43e97b !important;
    border-radius: 8px !important;
}

.stError {
    background: rgba(255, 107, 107, 0.1) !important;
    border: 1px solid rgba(255, 107, 107, 0.3) !important;
    color: #ff6b6b !important;
    border-radius: 8px !important;
}

.stWarning {
    background: rgba(255, 193, 7, 0.1) !important;
    border: 1px solid rgba(255, 193, 7, 0.3) !important;
    border-radius: 8px !important;
}

.stSlider > div > div > div > div {
    background: var(--accent) !important;
}

hr {
    border-color: var(--border) !important;
}
</style>
""", unsafe_allow_html=True)


# =========================
# API Yardımcı Fonksiyonlar
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
            r = requests.post(f"{API_BASE}{endpoint}", files=files, timeout=30)
        else:
            r = requests.post(f"{API_BASE}{endpoint}", json=data, timeout=30)
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


# =========================
# Sidebar
# =========================
with st.sidebar:
    # Dil seçimi
    lang_choice = st.selectbox(
        t("language_label"),
        options=["Türkçe", "English"],
        index=0 if st.session_state.lang == "tr" else 1,
        key="lang_select"
    )
    st.session_state.lang = "tr" if lang_choice == "Türkçe" else "en"

    st.markdown("---")

    # Başlık
    st.markdown(f'<div class="main-title">{t("title")}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="subtitle">{t("subtitle")}</div>', unsafe_allow_html=True)

    st.markdown("---")

    # =========================
    # Dosya Yükleme
    # =========================
    st.markdown(f'<div class="section-header">{t("upload_header")}</div>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        t("upload_label"),
        type=["pdf", "docx", "txt"],
        label_visibility="collapsed"
    )

    if st.button(t("upload_btn"), use_container_width=True):
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
                st.success(f'`{uploaded_file.name}` {t("upload_success")} ({result.get("chunks", 0)} {t("chunks_count")})')
                st.rerun()

    st.markdown("---")

    # =========================
    # Doküman Listesi
    # =========================
    st.markdown(f'<div class="section-header">{t("docs_header")}</div>', unsafe_allow_html=True)

    docs = get_documents()

    if docs is None:
        st.error(t("api_error"))
    elif not docs:
        st.caption(t("docs_empty"))
    else:
        for filename, info in docs.items():
            if info.get("deleted", False):
                continue

            is_active = info.get("active", True)
            badge = f'<span class="badge-active">{t("toggle_active")}</span>' if is_active else f'<span class="badge-passive">{t("toggle_passive")}</span>'

            st.markdown(f"""
            <div class="doc-card">
                <div class="doc-name">📄 {filename}</div>
                <div class="doc-meta">{info.get("chunks", 0)} {t("chunks_count")} &nbsp;|&nbsp; {badge}</div>
            </div>
            """, unsafe_allow_html=True)

            col1, col2, col3 = st.columns([1, 1, 1])

            with col1:
                if st.button(t("toggle_btn"), key=f"toggle_{filename}", use_container_width=True):
                    api_post(f"/toggle_file/{filename}")
                    st.rerun()

            with col2:
                if st.button(t("preview_btn"), key=f"preview_{filename}", use_container_width=True):
                    with st.spinner("..."):
                        preview = api_get(f"/preview/{filename}")
                    if preview:
                        st.session_state.preview_content = preview.get("preview", "")
                        st.session_state.preview_filename = filename
                    st.rerun()

            with col3:
                if st.button(t("delete_btn"), key=f"delete_{filename}", use_container_width=True):
                    api_delete(f"/remove_file/{filename}")
                    st.rerun()


# =========================
# Ana İçerik
# =========================
docs = get_documents()
active_docs = []
if docs:
    active_docs = [fn for fn, info in docs.items() if not info.get("deleted", False) and info.get("active", True)]

# Önizleme Modal
if st.session_state.preview_content is not None:
    st.markdown(f'<div class="section-header">{t("preview_header")}: <code>{st.session_state.preview_filename}</code></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="preview-box">{st.session_state.preview_content}</div>', unsafe_allow_html=True)
    if st.button(t("preview_close")):
        st.session_state.preview_content = None
        st.session_state.preview_filename = None
        st.rerun()
    st.markdown("---")

# =========================
# Özet Alma
# =========================
st.markdown(f'<div class="section-header">{t("summarize_header")}</div>', unsafe_allow_html=True)

if not active_docs:
    st.warning(t("no_docs_warning"))
else:
    sum_col1, sum_col2 = st.columns([3, 1])
    with sum_col1:
        sum_file = st.selectbox(
            "Doküman seçin / Select document",
            options=active_docs,
            key="sum_file",
            label_visibility="collapsed"
        )
    with sum_col2:
        if st.button(t("summarize_btn"), use_container_width=True):
            with st.spinner(t("summarizing")):
                prompt = t("summarize_prompt")
                result = api_post("/ask", {
                    "question": prompt,
                    "selected_files": [sum_file],
                    "top_k": 10
                })

            if result is None:
                st.error(t("api_error"))
            elif "error" in result:
                st.error(result["error"])
            else:
                st.markdown(f'<div class="chat-bubble-ai">📝 {result.get("answer", "")}</div>', unsafe_allow_html=True)

st.markdown("---")

# =========================
# Soru-Cevap Bölümü
# =========================
st.markdown(f'<div class="section-header">{t("chat_header")}</div>', unsafe_allow_html=True)

# Filtre & Ayarlar
with st.expander("⚙️ Ayarlar / Settings", expanded=False):
    if docs:
        all_docs = [fn for fn, info in docs.items() if not info.get("deleted", False)]
        selected_files = st.multiselect(
            t("select_files"),
            options=all_docs,
            default=[],
            key="selected_files"
        )
    else:
        selected_files = []

    top_k = st.slider(t("top_k"), min_value=1, max_value=10, value=5, key="top_k")

# Geçmiş Mesajlar
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.markdown(f'<div class="chat-bubble-user">👤 {msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-bubble-ai">🤖 {msg["content"]}</div>', unsafe_allow_html=True)

        if msg.get("sources"):
            sources_html = "".join([f'<span class="source-tag">📎 {s}</span>' for s in msg["sources"]])
            st.markdown(f'<div style="margin: 4px 0 8px 0">{t("sources_label")}: {sources_html}</div>', unsafe_allow_html=True)

        if msg.get("chunks"):
            with st.expander(f'{t("chunks_label")} ({len(msg["chunks"])})'):
                for i, chunk in enumerate(msg["chunks"]):
                    fn = chunk.get("metadata", {}).get("filename", "")
                    cid = chunk.get("metadata", {}).get("chunk_id", i)
                    score = chunk.get("score", 0)
                    content = chunk.get("content", "")[:300]
                    st.markdown(f"""
                    <div class="chunk-box">
                        <strong style="color:#a09af0">#{cid} — {fn}</strong>
                        <span style="color:#7a7a9a; font-size:0.75rem; margin-left:8px">score: {score:.4f}</span><br/>
                        {content}{"..." if len(chunk.get("content","")) > 300 else ""}
                    </div>
                    """, unsafe_allow_html=True)

# Soru Girişi
st.markdown("<br>", unsafe_allow_html=True)
q_col1, q_col2 = st.columns([5, 1])

with q_col1:
    question = st.text_input(
        "question_input",
        placeholder=t("chat_placeholder"),
        label_visibility="collapsed",
        key="question_input"
    )

with q_col2:
    ask_clicked = st.button(t("ask_btn"), use_container_width=True)

if ask_clicked:
    if not question.strip():
        st.warning(t("ask_empty"))
    elif not active_docs and not selected_files:
        st.warning(t("no_docs_warning"))
    else:
        st.session_state.chat_history.append({"role": "user", "content": question})

        with st.spinner(t("asking")):
            result = api_post("/ask", {
                "question": question,
                "selected_files": selected_files if selected_files else [],
                "top_k": top_k
            })

        if result is None:
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": t("api_error"),
                "sources": [],
                "chunks": []
            })
        elif "error" in result:
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": f'❌ {result["error"]}',
                "sources": [],
                "chunks": []
            })
        else:
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": result.get("answer", ""),
                "sources": result.get("sources", []),
                "chunks": result.get("chunks", [])
            })

        st.rerun()

# Geçmişi Temizle
if st.session_state.chat_history:
    if st.button("🗑 Sohbeti Temizle / Clear Chat", use_container_width=False):
        st.session_state.chat_history = []
        st.rerun()
