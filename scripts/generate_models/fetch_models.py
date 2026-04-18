#!/usr/bin/env python3
"""
fetch_models.py

Download model files defined in `models_to_fetch.json` and place them at the configured paths.

Usage:
  python scripts/generate_models/fetch_models.py --config scripts/generate_models/models_to_fetch.json

The JSON is an array of objects with keys: name, url, path, optional sha256.
"""
import argparse
import json
import os
import sys
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import hashlib


def parse_args():
    p = argparse.ArgumentParser(description="Fetch configured model files")
    p.add_argument("--config", "-c", default="scripts/generate_models/models_to_fetch.json")
    p.add_argument("--skip-verify", action="store_true", help="Skip sha256 verification if present")
    p.add_argument("--timeout", type=int, default=60, help="Download timeout seconds")
    return p.parse_args()


def sha256_of_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def download(url, dest, timeout=60):
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    req = Request(url, headers={"User-Agent": "fetch-models/1.0"})
    try:
        with urlopen(req, timeout=timeout) as r, open(dest + ".part", "wb") as out:
            chunk_size = 1024 * 1024
            while True:
                chunk = r.read(chunk_size)
                if not chunk:
                    break
                out.write(chunk)
        os.replace(dest + ".part", dest)
    except HTTPError as e:
        raise RuntimeError(f"HTTP error: {e.code} {e.reason}")
    except URLError as e:
        raise RuntimeError(f"URL error: {e.reason}")


def main():
    args = parse_args()
    if not os.path.exists(args.config):
        print(f"Config not found: {args.config}")
        sys.exit(2)

    with open(args.config, "r", encoding="utf-8") as f:
        try:
            items = json.load(f)
        except Exception as e:
            print("Failed to parse config:", e)
            sys.exit(2)

    for it in items:
        url = it.get("url")
        dest = it.get("path")
        sha256 = it.get("sha256")
        name = it.get("name") or os.path.basename(dest)

        if not url or not dest:
            print(f"Skipping invalid entry: {it}")
            continue

        if os.path.exists(dest):
            if sha256 and not args.skip_verify:
                local_sha = sha256_of_file(dest)
                if local_sha.lower() == sha256.lower():
                    print(f"{name}: already exists and sha256 matches; skipping")
                    continue
                else:
                    print(f"{name}: exists but sha256 mismatch; re-downloading")
            else:
                print(f"{name}: already exists; skipping (use --skip-verify to override)")
                continue

        print(f"Downloading {name} from {url} -> {dest}")
        try:
            download(url, dest, timeout=args.timeout)
        except Exception as e:
            print(f"Failed to download {name}: {e}")
            continue

        if sha256 and not args.skip_verify:
            local_sha = sha256_of_file(dest)
            if local_sha.lower() != sha256.lower():
                print(f"SHA256 verification failed for {name} (expected {sha256}, got {local_sha})")
                try:
                    os.remove(dest)
                except Exception:
                    pass
                continue

        print(f"{name}: done")


if __name__ == "__main__":
    main()
