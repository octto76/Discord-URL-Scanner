# 🛡️ Moris — Discord Link Scanner Bot (VirusTotal-Powered)

Moris is a privacy-first Discord bot that automatically scans messages containing URLs and checks them using [VirusTotal](https://www.virustotal.com/). It flags malicious, suspicious, or known IP logger links and provides a verdict directly in chat.

---

## 🚀 Features

- 🔗 Detects all `http`/`https` links in messages
- 🔍 Submits links to **VirusTotal** and polls for a verdict
- 🚫 Blocks known IP logger domains (e.g., Grabify)
- 🛡️ Displays a clear verdict: Clean, Suspicious, or Malicious
---

## 🧪 Test It
👉 **[Invite Moris to your server](https://discord.com/oauth2/authorize?client_id=1388567819154886737&permissions=93184&integration_type=0&scope=bot+applications.commands)**
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
---

![moris](https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/c9d73b15-5287-4b94-8182-987e5b7b902b/dbg7sof-6f15c751-e56b-4c77-9dc7-aba2e5e18236.jpg/v1/fit/w_828,h_1172,q_70,strp/baby_tarbosaurus_by_hannay1982_dbg7sof-414w-2x.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7ImhlaWdodCI6Ijw9MTQ0OSIsInBhdGgiOiJcL2ZcL2M5ZDczYjE1LTUyODctNGI5NC04MTgyLTk4N2U1YjdiOTAyYlwvZGJnN3NvZi02ZjE1Yzc1MS1lNTZiLTRjNzctOWRjNy1hYmEyZTVlMTgyMzYuanBnIiwid2lkdGgiOiI8PTEwMjQifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6aW1hZ2Uub3BlcmF0aW9ucyJdfQ.39-OSjn1rtiJSh8sSxdn5UO6FzFIV8C8nlLI6CTeUbY)

(Artwork made by Hannay1982)
