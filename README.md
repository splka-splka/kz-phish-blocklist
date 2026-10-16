# 🛡️ KZ Phish Blocklist

**English** | [Русский](README.ru.md)

An open blocklist of phishing and scam domains related to Kazakhstan: fakes of Kaspi, Halyk, eGov, Kazpost and other Kazakhstani services.

## Inclusion criteria

A domain is added if it meets **at least one** of these conditions:

1. **Impersonates a Kazakhstani brand** — a bank, government service, marketplace or delivery service (name, logo, design, or a domain resembling the official one)
2. **Targets residents of Kazakhstan** — Kazakh or Russian language with local specifics, prices in tenge, Kazakhstani phone numbers or payment details

**And** the malicious nature is confirmed: via urlscan.io, VirusTotal, Google Safe Browsing, a KZ-CERT report, or manual analysis.

### Not included

- name coincidences without brand impersonation (e.g. "Kaspi" meaning "Caspian")
- global scam sites unrelated to Kazakhstan — please report those to [Google Safe Browsing](https://safebrowsing.google.com/safebrowsing/report_phish/) and [Phishing.Database](https://github.com/Phishing-Database/Phishing.Database)
- official domains (see `sources/whitelist.txt`)

## Why this list exists

The largest open phishing database (Phishing.Database, ~386,000 domains) contains almost no fakes of Kazakhstani banks or government services. Kazakhstan-targeted phishing rarely reaches global feeds, and some of these sites are not flagged even by Google Safe Browsing.

## Usage

| Where | File |
|---|---|
| AdGuard / AdGuard Home | `dist/adguard.txt` |
| Pi-hole / hosts | `dist/hosts.txt` |
| Plain domain list | `dist/domains.txt` |

## Sources

- [Phishing.Database](https://github.com/Phishing-Database/Phishing.Database) and [OpenPhish](https://openphish.com), filtered for Kazakhstani brands
- [urlscan.io](https://urlscan.io) search with manual verification
- [KZ-CERT](https://kz-cert.kz) reports and manual additions

## Found a phishing site?

Open an issue with the site address, and report it to KZ-CERT: **1400** (24/7) or [t.me/kzcert](https://t.me/kzcert).

⚠️ Do not open suspicious sites yourself — check them via [urlscan.io](https://urlscan.io).

## False positive?

If a legitimate site was blocked by mistake, open an issue — we will check and remove it.

## License

MIT
