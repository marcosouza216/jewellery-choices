#!/usr/bin/env python3
import json
import os
import pathlib
import sys
import urllib.error
import urllib.parse
import urllib.request


def env(name: str, default: str = "") -> str:
    return os.environ.get(name, default).strip()


SUPABASE_URL = env("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = env("SUPABASE_SERVICE_ROLE_KEY")
SUPABASE_BUCKET = env("SUPABASE_BUCKET", "product-images")
IMAGES_DIR = env("IMAGES_DIR", "image")
PAGES_BASE_URL = env("PAGES_BASE_URL")
GITHUB_REPOSITORY = env("GITHUB_REPOSITORY")
GITHUB_REPOSITORY_OWNER = env("GITHUB_REPOSITORY_OWNER")


def require_env():
    missing = []
    if not SUPABASE_URL:
        missing.append("SUPABASE_URL")
    if not SUPABASE_SERVICE_ROLE_KEY:
        missing.append("SUPABASE_SERVICE_ROLE_KEY")
    if missing:
        print(f"Missing required env: {', '.join(missing)}")
        sys.exit(1)


def get_pages_base_url() -> str:
    if PAGES_BASE_URL:
        return PAGES_BASE_URL.rstrip("/")
    if GITHUB_REPOSITORY and GITHUB_REPOSITORY_OWNER:
        return f"https://{GITHUB_REPOSITORY_OWNER}.github.io/{GITHUB_REPOSITORY}".rstrip("/")
    print("Cannot determine pages base URL. Set PAGES_BASE_URL.")
    sys.exit(1)


def supabase_get(path: str):
    url = f"{SUPABASE_URL.rstrip('/')}{path}"
    req = urllib.request.Request(
        url,
        headers={
            "apikey": SUPABASE_SERVICE_ROLE_KEY,
            "Authorization": f"Bearer {SUPABASE_SERVICE_ROLE_KEY}",
            "Accept": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def supabase_patch(path: str, payload: dict):
    url = f"{SUPABASE_URL.rstrip('/')}{path}"
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        method="PATCH",
        headers={
            "apikey": SUPABASE_SERVICE_ROLE_KEY,
            "Authorization": f"Bearer {SUPABASE_SERVICE_ROLE_KEY}",
            "Content-Type": "application/json",
            "Prefer": "return=minimal",
        },
    )
    with urllib.request.urlopen(req, timeout=60):
        return


def extract_object_path(url: str):
    marker = f"/storage/v1/object/public/{SUPABASE_BUCKET}/"
    idx = url.find(marker)
    if idx == -1:
        return None
    tail = url[idx + len(marker) :]
    if not tail:
        return None
    return urllib.parse.unquote(tail)


def download_if_needed(source_url: str, local_path: pathlib.Path):
    if local_path.exists():
        return False
    local_path.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(source_url, headers={"Accept": "*/*"})
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            local_path.write_bytes(resp.read())
    except urllib.error.HTTPError as e:
        print(f"WARN download failed [{e.code}] {source_url}")
        return False
    except Exception as e:
        print(f"WARN download failed {source_url} ({e})")
        return False
    return True


def main():
    require_env()
    pages_base = get_pages_base_url()
    print(f"Pages base URL: {pages_base}")

    products = supabase_get("/rest/v1/products?select=id,image")
    print(f"Loaded {len(products)} products")

    unique_urls = {}
    for p in products:
        image_csv = (p.get("image") or "").strip()
        if not image_csv:
            continue
        for raw in image_csv.split(","):
            u = raw.strip()
            if u:
                unique_urls[u] = True

    old_urls = list(unique_urls.keys())
    print(f"Found {len(old_urls)} unique image URLs")

    old_to_new = {}
    downloaded_count = 0
    for old_url in old_urls:
        object_path = extract_object_path(old_url)
        if not object_path:
            continue
        rel_path = pathlib.PurePosixPath(IMAGES_DIR) / pathlib.PurePosixPath(object_path)
        local_path = pathlib.Path(str(rel_path))
        if download_if_needed(old_url, local_path):
            downloaded_count += 1
        old_to_new[old_url] = f"{pages_base}/{rel_path.as_posix()}"

    print(f"Downloaded {downloaded_count} new images")

    updated_rows = 0
    for p in products:
        image_csv = (p.get("image") or "").strip()
        if not image_csv:
            continue
        original_parts = [part.strip() for part in image_csv.split(",")]
        new_parts = [old_to_new.get(part, part) for part in original_parts]
        new_csv = ",".join(new_parts)
        if new_csv == image_csv:
            continue
        pid = p.get("id")
        supabase_patch(f"/rest/v1/products?id=eq.{pid}", {"image": new_csv})
        updated_rows += 1

    print(f"Updated image URL in {updated_rows} products")
    print("Sync done")


if __name__ == "__main__":
    main()
