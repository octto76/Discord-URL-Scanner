# 🛡️ Moris — Discord Link Scanner Bot (VirusTotal-Powered)

Moris is a privacy-first Discord bot that automatically scans messages containing URLs and checks them using [VirusTotal](https://www.virustotal.com/). It flags malicious, suspicious, or known IP logger links and provides a verdict directly in chat.

---

## 🚀 Features

- 🔗 Detects all `http`/`https` links in messages
- 🔍 Submits links to **VirusTotal** and polls for a verdict
- 🚫 Blocks known IP logger domains (e.g., Grabify)
- 🛡️ Displays a clear verdict: Clean, Suspicious, or Malicious
- 🧼 Prevents link previews for stealth/scam links
- 🕒 Per-user rate limiting to avoid spam

---
## 🧪 Test It
In any server where Moris is added, send a message like:

```
Check this out: https://www.someurl.com
```
Moris will reply:

```
🚫 This link is a known IP logger (`https://www.someurl.com`). Do not click it.
```

Or 

```
🔍 Scanning: https://www.someurl.com
🟢 Verdict: CLEAN (0/70 engines flagged it)
🔗 https://www.scannedurl.com
```

