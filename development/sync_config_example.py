# ========= KONFIG =========
SRC_URL = "http://paperless-source:8000"
SRC_TOKEN = "SOURCE_API_TOKEN"

DST_URL = "http://paperless-target:8000"
DST_TOKEN = "TARGET_API_TOKEN"
# ==========================

HEADERS_SRC = {
    "Authorization": f"Token {SRC_TOKEN}",
    "Accept": "application/json",
}

HEADERS_DST = {
    "Authorization": f"Token {DST_TOKEN}",
    "Accept": "application/json",
    "Content-Type": "application/json",
}
