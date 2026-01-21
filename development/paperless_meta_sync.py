import requests
from sync_config import SRC_URL, DST_URL, HEADERS_SRC, HEADERS_DST


def fetch_all(url, headers):
    results = []
    while url:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        data = r.json()
        results.extend(data["results"])
        url = data["next"]
    return results


def create_if_not_exists(endpoint, unique_field, objects):
    existing = fetch_all(f"{DST_URL}/api/{endpoint}/", HEADERS_DST)
    existing_map = {obj[unique_field]: obj for obj in existing}

    for obj in objects:
        key = obj[unique_field]
        if key in existing_map:
            print(f"[SKIP] {endpoint}: {key}")
            continue

        payload = {k: v for k, v in obj.items() if k not in ("id", "slug")}
        r = requests.post(
            f"{DST_URL}/api/{endpoint}/",
            headers=HEADERS_DST,
            json=payload,
        )

        if r.status_code not in (200, 201):
            print(f"[ERR ] {endpoint}: {key} -> {r.status_code} {r.text}")
        else:
            print(f"[OK  ] {endpoint}: {key}")


def main():
    print("== Lade Daten aus Quellinstanz ==")

    tags = fetch_all(f"{SRC_URL}/api/tags/", HEADERS_SRC)
    correspondents = fetch_all(f"{SRC_URL}/api/correspondents/", HEADERS_SRC)
    doctypes = fetch_all(f"{SRC_URL}/api/document_types/", HEADERS_SRC)
    storage_paths = fetch_all(f"{SRC_URL}/api/storage_paths/", HEADERS_SRC)

    print("== Übertrage in Zielinstanz ==")

    create_if_not_exists("tags", "name", tags)
    create_if_not_exists("correspondents", "name", correspondents)
    create_if_not_exists("document_types", "name", doctypes)
    create_if_not_exists("storage_paths", "path", storage_paths)

    print("== Fertig ==")


if __name__ == "__main__":
    main()