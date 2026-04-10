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
        print(f"Missing required env: {', '.join(missing)}", flush=True)
        sys.exit(1)


def get_pages_base_url() -> str:
    if PAGES_BASE_URL:
        return PAGES_BASE_URL.rstrip("/")
    if GITHUB_REPOSITORY and GITHUB_REPOSITORY_OWNER:
        return f"https://{GITHUB_REPOSITORY_OWNER}.github.io/{GITHUB_REPOSITORY}".rstrip("/")
    print("Cannot determine pages base URL. Set PAGES_BASE_URL.", flush=True)
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
    headers = {
        "apikey": SUPABASE_SERVICE_ROLE_KEY,
        "Authorization": f"Bearer {SUPABASE_SERVICE_ROLE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal",
    }
    req = urllib.request.Request(url, data=data, method="PATCH", headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=60):
            return
    except urllib.error.HTTPError as e:
        # Some Supabase projects may 301 from /table?query to /table/?query.
        if e.code in (301, 302, 307, 308):
            redirected_url = e.headers.get("Location")
            if redirected_url:
                redirected_url = urllib.parse.urljoin(url, redirected_url)
                print(f"PATCH redirect: {url} -> {redirected_url}", flush=True)
                redirected_req = urllib.request.Request(
                    redirected_url,
                    data=data,
                    method="PATCH",
                    headers=headers,
                )
                with urllib.request.urlopen(redirected_req, timeout=60):
                    return
        print(f"PATCH failed: {url} [{e.code}] {e.reason}", flush=True)
        raise


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
        print(f"WARN download failed [{e.code}] {source_url}", flush=True)
        return False
    except Exception as e:
        print(f"WARN download failed {source_url} ({e})", flush=True)
        return False
    return True


def main():
    require_env()
    pages_base = get_pages_base_url()
    print(f"Pages base URL: {pages_base}", flush=True)

    products = supabase_get("/rest/v1/products?select=id,image")
    print(f"Loaded {len(products)} products", flush=True)

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
    print(f"Found {len(old_urls)} unique image URLs", flush=True)

    old_to_new = {}
    downloaded_count = 0
    total_urls = len(old_urls)
    for i, old_url in enumerate(old_urls, start=1):
        object_path = extract_object_path(old_url)
        if not object_path:
            continue
        rel_path = pathlib.PurePosixPath(IMAGES_DIR) / pathlib.PurePosixPath(object_path)
        local_path = pathlib.Path(str(rel_path))
        if download_if_needed(old_url, local_path):
            downloaded_count += 1
        old_to_new[old_url] = f"{pages_base}/{rel_path.as_posix()}"
        if i % 20 == 0 or i == total_urls:
            print(
                f"Image sync progress: {i}/{total_urls}, downloaded new: {downloaded_count}",
                flush=True,
            )

    print(f"Downloaded {downloaded_count} new images", flush=True)

    updated_rows = 0
    total_products = len(products)
    for i, p in enumerate(products, start=1):
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
        if updated_rows % 20 == 0 or i == total_products:
            print(
                f"DB rewrite progress: checked {i}/{total_products}, updated {updated_rows}",
                flush=True,
            )

    print(f"Updated image URL in {updated_rows} products", flush=True)
    print("Sync done", flush=True)


if __name__ == "__main__":
    main()
