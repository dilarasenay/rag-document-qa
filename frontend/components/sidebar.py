import streamlit as st
from api import api_post, api_delete, api_get, get_documents, get_stats
from lang import t


def render_sidebar():
    with st.sidebar:
        # ── Dil Seçimi — üst sol ──
        lang_pick = st.selectbox(
            "",
            ["🇹🇷 TR", "🇬🇧 EN"],
            index=0 if st.session_state.lang == "tr" else 1,
            label_visibility="collapsed",
            key="lang_select"
        )
        new_lang = "tr" if "TR" in lang_pick else "en"
        if st.session_state.get("prev_lang") != new_lang:
            st.session_state.suggested_questions = []
            st.session_state.suggestions_for_doc = None
            st.session_state.prev_lang = new_lang
        st.session_state.lang = new_lang

        # ── Logo ──
        st.markdown(f"""
        <div style="
            font-family: 'Instrument Serif', serif;
            font-size: 1.75rem;
            letter-spacing: -0.5px;
            line-height: 1.1;
            margin: 6px 0 2px 0;
            background: linear-gradient(135deg, #6c63ff 0%, #ff6b6b 50%, #43e97b 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        ">📚 DocuMind</div>
        <div style="font-size:0.78rem;color:#888;font-weight:400;letter-spacing:0.3px;margin-bottom:4px;">
            {t("tagline")}
        </div>
        """, unsafe_allow_html=True)

        # ── İstatistikler ──
        docs = get_documents()
        total, active_count, chunk_count = get_stats(docs or {})

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

        # ── Dosya Yükleme ──
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
        elif not docs or not any(not v.get("deleted", False) for v in docs.values()):
            st.caption(t("docs_empty"))
        else:
            for filename, info in docs.items():
                if info.get("deleted", False):
                    continue

                is_active = info.get("active", True)
                pill = (
                    f'<span class="pill-active">{t("active")}</span>'
                    if is_active else
                    f'<span class="pill-passive">{t("passive")}</span>'
                )

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
