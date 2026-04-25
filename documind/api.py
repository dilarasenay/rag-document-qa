import requests
from config import API_BASE


def api_get(endpoint: str):
    try:
        r = requests.get(f"{API_BASE}{endpoint}", timeout=10)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.ConnectionError:
        return None
    except Exception as e:
        return {"error": str(e)}


def api_post(endpoint: str, data=None, files=None):
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


def api_delete(endpoint: str):
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


def get_stats(docs: dict):
    if not docs:
        return 0, 0, 0
    visible = {fn: info for fn, info in docs.items() if not info.get("deleted", False)}
    total = len(visible)
    active = sum(1 for info in visible.values() if info.get("active", True))
    chunks = sum(info.get("chunks", 0) for info in visible.values())
    return total, active, chunks
