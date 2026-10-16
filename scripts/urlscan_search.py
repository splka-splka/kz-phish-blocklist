#!/usr/bin/env python3
"""Ищет на urlscan.io страницы с казахстанскими брендами в заголовке на чужих доменах."""
import json
import os
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "sources"
BRANDS = ["kaspi", "halyk", "homebank", "egov", "kazpost", "jusan"]


def load_key():
    env = ROOT / ".env"
    for line in env.read_text().splitlines() if env.exists() else []:
        if line.startswith("URLSCAN_API_KEY="):
            return line.split("=", 1)[1].strip()
    return os.environ.get("URLSCAN_API_KEY")


def read_list(path):
    if not path.exists():
        return []
    lines = (l.split("#")[0].strip().lower() for l in path.read_text().splitlines())
    return [l for l in lines if l]


def search(brand, key):
    q = f'page.title:"{brand}" AND date:>now-30d'
    url = "https://urlscan.io/api/v1/search/?" + urllib.parse.urlencode({"q": q, "size": 100})
    req = urllib.request.Request(url, headers={"API-Key": key, "User-Agent": "kz-phish-blocklist"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r).get("results", [])
    except Exception as e:
        print(f"  [!] {brand}: ошибка ({e})")
        return []


def main():
    key = load_key()
    if not key:
        print("Нет URLSCAN_API_KEY в .env")
        return
    whitelist = set(read_list(SRC / "whitelist.txt"))
    candidates = {}
    for brand in BRANDS:
        results = search(brand, key)
        print(f"  [+] {brand}: {len(results)} страниц")
        for r in results:
            page = r.get("page", {})
            domain = (page.get("domain") or "").lower().removeprefix("www.")
            if not domain or any(domain == w or domain.endswith("." + w) for w in whitelist):
                continue
            candidates.setdefault(domain, (page.get("title") or "")[:80])
    out = SRC / "urlscan-review.txt"
    out.write_text("# Кандидаты с urlscan.io — ПРОВЕРИТЬ ВРУЧНУЮ перед добавлением в manual.txt\n"
                   + "\n".join(f"{d}  # {t}" for d, t in sorted(candidates.items())) + "\n")
    print(f"Кандидатов: {len(candidates)} → {out}")


if __name__ == "__main__":
    main()
