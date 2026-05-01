import streamlit as st


def inject_styles():
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
    min-width: 300px !important;
    max-width: 300px !important;
}

[data-testid="stSidebar"] > div:first-child {
    width: 300px !important;
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
.bubble-wrap { margin-bottom: 1.5rem; }
.bubble-user {
    background: #1A1A1A;
    color: #F7F5F0;
    border-radius: 18px 18px 4px 18px;
    padding: 12px 18px;
    font-size: 0.95rem;
    line-height: 1.55;
    margin-left: auto;
    max-width: 80%;
    width: fit-content;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}
.bubble-ai {
    background: #FFFFFF;
    color: #1A1A1A;
    border: 1px solid #E8E4DC;
    border-radius: 4px 18px 18px 18px;
    padding: 16px 20px;
    font-size: 0.95rem;
    line-height: 1.65;
    max-width: 90%;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}
.bubble-label {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.8px;
    color: #888;
    margin-bottom: 6px;
    text-transform: uppercase;
}
.bubble-label-right { text-align: right; }

/* ── Source Tags ── */
.source-wrap { 
    margin: 12px 0 6px;
    padding-top: 8px;
    border-top: 1px solid #F0EDE8;
}
.source-tag {
    display: inline-flex;
    align-items: center;
    background: #FDF2F2;
    color: #9B2C2C;
    border: 1px solid #FEB2B2;
    border-radius: 6px;
    padding: 4px 10px;
    font-size: 0.75rem;
    font-family: 'DM Mono', monospace;
    margin: 2px 4px 2px 0;
    font-weight: 500;
}

/* ── Chunk Items ── */
.chunk-item {
    background: #FFFFFF;
    border: 1px solid #E8E4DC;
    border-left: 4px solid #C8B99A;
    border-radius: 4px;
    padding: 12px 16px;
    margin: 8px 0;
    font-size: 0.82rem;
    color: #4A4A4A;
    line-height: 1.6;
}
.chunk-header {
    font-size: 0.72rem;
    color: #999;
    margin-bottom: 8px;
    display: flex;
    justify-content: space-between;
    border-bottom: 1px dashed #E8E4DC;
    padding-bottom: 4px;
}
.chunk-score {
    background: #F7F5F0;
    border-radius: 4px;
    padding: 2px 8px;
    font-weight: 600;
    color: #C8B99A;
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

/* ── Export Button ── */
.export-wrap button,
.export-wrap [data-testid="stDownloadButton"] button,
[data-testid="stDownloadButton"] button {
    background: #F0FDF4 !important;
    border-color: #BBF7D0 !important;
    color: #15803D !important;
    font-weight: 500 !important;
}
.export-wrap button:hover,
.export-wrap [data-testid="stDownloadButton"] button:hover,
[data-testid="stDownloadButton"] button:hover {
    background: #DCFCE7 !important;
    border-color: #86EFAC !important;
    color: #166534 !important;
}

/* ── Regen Button ── */
.regen-wrap {
    display: flex;
    align-items: flex-end;
    height: 100%;
    padding-top: 4px;
}

/* Suggestions satırındaki column gap'i sıfırla */
.suggestions-row [data-testid="stHorizontalBlock"] {
    gap: 0 !important;
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

/* ── Streamlit Overrides ── */
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
.stButton > button:active { transform: scale(0.98) !important; }

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
.stFileUploader > div:hover { border-color: #C8B99A !important; }

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

.stSlider > div > div > div > div { background: #1A1A1A !important; }

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

/* Scrollbar */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #D4CFC5; border-radius: 10px; }

hr { border: none; border-top: 1px solid #E8E4DC !important; margin: 1rem 0 !important; }
</style>
""", unsafe_allow_html=True)
