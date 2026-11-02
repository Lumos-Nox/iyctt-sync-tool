#!/usr/bin/env python3
"""iyctt-sync: mirror a local folder to Iyctt backup storage."""
import argparse, hashlib, json, os, sys, time
from pathlib import Path

import requests

API_BASE = os.environ.get("IYCTT_API_BASE", "https://metrics.iyctt.com/v1")
ENDPOINT = os.environ.get("IYCTT_ENDPOINT", "https://backup-7713.metrics.iyctt.com")
STATE = ".sync-state.json"


def api_key():
    key = os.environ.get("IYCTT_API_KEY", "")
    if not key:
        env_file = Path(__file__).with_name(".env")
        if env_file.exists():
            for line in env_file.read_text().splitlines():
                if line.startswith("IYCTT_API_KEY="):
                    key = line.split("=", 1)[1].strip()
    if not key:
        sys.exit("IYCTT_API_KEY is not set (see .env.example)")
    return key


def manifest(root: Path):
    out = []
    for p in sorted(root.rglob("*")):
        if p.is_file() and p.name != STATE:
            h = hashlib.sha256(p.read_bytes()).hexdigest()
            out.append({"path": str(p.relative_to(root)), "sha256": h, "size": p.stat().st_size})
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("folder")
    ap.add_argument("--watch", action="store_true")
    args = ap.parse_args()
    key = api_key()
    s = requests.Session()
    s.headers["Authorization"] = f"Bearer {key}"
    proj = s.get(f"{API_BASE}/projects", timeout=30).json()
    print("projects:", [p["name"] for p in proj.get("data", [])])
    root = Path(args.folder)
    while True:
        m = manifest(root)
        r = s.post(f"{ENDPOINT}/api/1/store/", json={"manifest": m}, timeout=60)
        print("stored:", r.json().get("id"), f"({len(m)} files)")
        (root / STATE).write_text(json.dumps({"ts": time.time(), "files": len(m)}))
        if not args.watch:
            break
        time.sleep(30)


if __name__ == "__main__":
    main()
