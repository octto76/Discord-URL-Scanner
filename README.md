# Moris — Discord URL Scanner Bot 🔍

**Moris** is a self-hosted Discord bot that automatically scans any URLs posted in your server using [urlscan.io](https://urlscan.io), and reports whether they are **malicious**, **phishing**, or **clean** — right in the chat.

> Lightweight, private, and open source. Designed to be run only when you need it.

---

## ✅ Features

- ✅ Automatically detects and scans links in messages
- 🕵️ Polls urlscan.io and shows verdict (malicious / clean)
- 🛡️ Shows threat categories (e.g. `phishing`, `malware`)
- 🧠 Rate-limits each user to prevent abuse (30s cooldown)
- 🔒 Easy to self-host and keep private

---

## 📦 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/moris-bot.git
cd moris-bot
````

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create your `.env` file

Then create and edit `.env` with your credentials:

```env
DISCORD_TOKEN=your_discord_bot_token_here
URLSCAN_API_KEY=your_urlscan_api_key_here
```

> You can get your free urlscan.io API key:
>
> * Log in at [https://urlscan.io/user/login](https://urlscan.io/user/login)
> * Visit your [user dashboard](https://urlscan.io/user/overview/)
> * Scroll down to "API Key" section and copy it

---

## 🚀 Running Moris

Once everything is set up, just run:

```bash
python moris.py
```

Moris will:

* Log into your Discord server
* Scan all new messages for URLs
* Return a result and verdict link within 15 seconds

---

## 🧪 Example

User sends:

```
Check this out: http://badsite.example
```

Moris replies:

```
🔍 Scanning: http://badsite.example
🔴 Verdict: MALICIOUS (phishing, malware)
🔗 https://urlscan.io/result/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/
```

---

## 🛠 Configuration

* Default cooldown: `20` seconds per user
* All scans are public (default for urlscan free tier)
