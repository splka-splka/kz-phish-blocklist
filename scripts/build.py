#!/usr/bin/env python3
"""KZ Phish Blocklist — сборка списка фишинговых доменов, нацеленных на Казахстан."""
import re
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "sources"
DIST = ROOT / "dist"

FEEDS = {
    "Phishing.Database": "https://raw.githubusercontent.com/Phishing-Database/Phishing.Database/master/phishing-domains-ACTIVE.txt",
    "OpenPhish": "https://openphish.com/feed.txt",
}

DOMAIN_RE = re.compile(r"^(?=.{1,253}$)([a-z0-9-]{1,63}\.)+[a-z]{2,63}$")


def read_list(path):
    if not path.exists():
        return []
    lines = (l.split("#")[0].strip().lower() for l in path.read_text().splitlines())
    return [l for l in lines if l]


def to_domain(entry):
    entry = entry.strip().lower()
    if not entry or entry.startswith("#"):
        return None
    if "://" in entry:
        entry = urlparse(entry).hostname or ""
    entry = entry.split("/")[0].split(":")[0].lstrip("*.").removeprefix("www.")
    return entry if DOMAIN_RE.match(entry) else None


def fetch(name, url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "kz-phish-blocklist"})
        with urllib.request.urlopen(req, timeout=60) as r:
            text = r.read().decode("utf-8", errors="ignore")
    except Exception as e:
        print(f"  [!] {name}: не удалось скачать ({e})")
        return set()
    domains = {d for line in text.splitlines() if (d := to_domain(line))}
    print(f"  [+] {name}: {len(domains)} доменов")
    return domains


def is_whitelisted(domain, whitelist):
    return any(domain == w or domain.endswith("." + w) for w in whitelist)


def write_list(path, title, domains, fmt, comment="#"):
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    header = [title, f"Обновлено: {now}", f"Доменов: {len(domains)}",
              "https://github.com/splka-splka/kz-phish-blocklist"]
    path.write_text("\n".join(f"{comment} {h}" for h in header) + "\n"
                    + "\n".join(fmt.format(d) for d in domains) + "\n")


def main():
    whitelist = set(read_list(SRC / "whitelist.txt"))
    patterns = [re.compile(p) for p in read_list(SRC / "brands.txt")]
    manual = {d for l in read_list(SRC / "manual.txt") if (d := to_domain(l))}

    print("Скачиваю глобальные базы...")
    all_domains = set()
    for name, url in FEEDS.items():
        all_domains |= fetch(name, url)

    brand_hits = {d for d in all_domains if any(p.search(d) for p in patterns)}
    kz_hosted = {d for d in all_domains if d.endswith(".kz")} - brand_hits

    result = sorted(d for d in (brand_hits | manual) if not is_whitelisted(d, whitelist))
    review = sorted(d for d in kz_hosted if not is_whitelisted(d, whitelist))

    print(f"Подделки под казахстанские бренды: {len(brand_hits)}")
    print(f"Итого в основном списке: {len(result)} (вручную: {len(manual)})")
    print(f"Фишинг на .kz-доменах (на проверку): {len(review)}")

    DIST.mkdir(exist_ok=True)
    title = "KZ Phish Blocklist — фишинговые домены, нацеленные на Казахстан"
    write_list(DIST / "domains.txt", title, result, "{}")
    write_list(DIST / "hosts.txt", title, result, "0.0.0.0 {}")
    write_list(DIST / "adguard.txt", title, result, "||{}^", comment="!")
    write_list(DIST / "kz-hosted-review.txt",
               "Фишинг на .kz-доменах — НЕ блокировать без ручной проверки", review, "{}")
    print("Готово.")


if __name__ == "__main__":
    main()
