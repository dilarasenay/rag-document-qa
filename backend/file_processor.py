import fitz  # PyMuPDF
from docx import Document
import os


# =========================
# TEXT TEMİZLEME
# =========================
def fix_spaced_chars(text: str) -> str:
    """
    PDF'lerde 'P R O J E' gibi ayrılmış karakterleri düzeltir.
    """
    fixed_lines = []

    for line in text.splitlines():
        tokens = line.split()

        if len(tokens) >= 6:
            single_chars = [t for t in tokens if len(t) == 1 and t.isalpha()]
            ratio = len(single_chars) / len(tokens)

            if ratio > 0.6:
                line = "".join(tokens)

        fixed_lines.append(line)

    return "\n".join(fixed_lines)


def clean_text(text: str) -> str:
    """
    Boş satırları temizler ve metni düzenler.
    """
    text = fix_spaced_chars(text)

    lines = text.splitlines()
    lines = [line.strip() for line in lines if line.strip()]

    return "\n".join(lines)


# =========================
# PDF
# =========================
def extract_text_from_pdf(file_path: str) -> str:
    try:
        doc = fitz.open(file_path)
        text = ""

        for page in doc:
            text += page.get_text()

        doc.close()

        return clean_text(text)

    except Exception as e:
        print(f"PDF okuma hatası: {e}")
        return ""


# =========================
# DOCX
# =========================
def extract_text_from_docx(file_path: str) -> str:
    try:
        doc = Document(file_path)
        text = ""

        for para in doc.paragraphs:
            if para.text.strip():
                text += para.text + "\n"

        return clean_text(text)

    except Exception as e:
        print(f"DOCX okuma hatası: {e}")
        return ""


# =========================
# TXT
# =========================
def extract_text_from_txt(file_path: str) -> str:
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return clean_text(f.read())

    except Exception as e:
        print(f"TXT okuma hatası: {e}")
        return ""


# =========================
# GENEL FONKSİYON
# =========================
def extract_text(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext == ".docx":
        return extract_text_from_docx(file_path)
    elif ext == ".txt":
        return extract_text_from_txt(file_path)
    else:
        raise ValueError(f"Desteklenmeyen dosya türü: {ext}")