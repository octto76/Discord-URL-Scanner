import discord
import re
import aiohttp
import asyncio
import os
import time
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
URLSCAN_API_KEY = os.getenv("URLSCAN_API_KEY")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

URL_REGEX = r"https?://[^\s]+"
COOLDOWN_SECONDS = 30
user_cooldowns = {}

# Known IP grabber / logger domains
ip_grabber_domains = [
    "grabify.link", "bmwforum.co", "catsnthing.com", "catsnthings.fun", "crabrave.pw",
    "curiouscat.club", "datasig.io", "datauth.io", "dateing.club", "discörd.com",
    "disçordapp.com", "fortnight.space", "fortnitechat.site", "freegiftcards.co", "gaming-at-my.best",
    "gamingfun.me", "headshot.monster", "imageshare.best", "joinmy.site", "leancoding.co",
    "locations.quest", "lovebird.guru", "minecräft.com", "mypic.icu", "otherhalf.life",
    "partpicker.shop", "progaming.monster", "quickmessage.us", "screenshare.host", "screenshot.best",
    "shrekis.life", "sportshub.bar", "spottyfly.com", "stopify.co", "särahah.eu", "särahah.pl",
    "trulove.guru", "xda-developers.us", "yourmy.monster", "youshouldclick.us", "yoütu.be"
]

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user.name}")

@client.event
async def on_message(message):
    if message.author.bot:
        return

    urls = re.findall(URL_REGEX, message.content)
    if not urls:
        return

    user_id = message.author.id
    now = time.time()

    last_used = user_cooldowns.get(user_id, 0)
    if now - last_used < COOLDOWN_SECONDS:
        wait_time = int(COOLDOWN_SECONDS - (now - last_used))
        await message.reply(f"⏳ Please wait {wait_time}s before scanning again.", mention_author=False)
        return

    user_cooldowns[user_id] = now

    for url in urls:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()

        # Block known IP logger domains
        if any(grabber in domain for grabber in ip_grabber_domains):
            await message.reply(
                f"🚫 This link is a known IP logger (`{domain}`). Do not click it.",
                mention_author=False,
                suppress_embeds=True
            )
            continue

        # Send initial message and keep reference to edit later
        status_msg = await message.reply(
            f"🔍 Scanning: {url}",
            mention_author=False,
            suppress_embeds=True
        )

        async with message.channel.typing():
            result_url, verdict, score, categories = await scan_and_poll_url(url)

        if result_url:
            verdict_emoji = "🟢"
            if verdict == "malicious":
                verdict_emoji = "🔴"
            elif score >= 60:
                verdict_emoji = "🟡"
                verdict = "suspicious"

            categories_str = f"({', '.join(categories)})" if categories else ""
            final_msg = (
                f"🔍 Scanning: {url}\n"
                f"{verdict_emoji} Verdict: **{verdict.upper()}** {categories_str}\n"
                f"🔗 <{result_url}>"
            )
            await status_msg.edit(content=final_msg)
        else:
            await status_msg.edit(
                content=f"🔍 Scanning: {url}\n❌ Failed to scan this link.",
                suppress_embeds=True
            )

async def scan_and_poll_url(url):
    headers = {"API-Key": URLSCAN_API_KEY, "Content-Type": "application/json"}
    payload = {"url": url, "public": "on"}

    async with aiohttp.ClientSession() as session:
        try:
            # Submit scan
            async with session.post("https://urlscan.io/api/v1/scan/", json=payload, headers=headers) as res:
                if res.status != 200:
                    return None, None, None, None
                data = await res.json()
                uuid = data.get("uuid")
                result_url = f"https://urlscan.io/result/{uuid}/"

            # Wait for scan to complete
            await asyncio.sleep(15)

            # Fetch scan result
            async with session.get(f"https://urlscan.io/api/v1/result/{uuid}/") as res:
                if res.status != 200:
                    return result_url, "unknown", 0, []
                result = await res.json()
                verdict_obj = result.get("verdicts", {}).get("overall", {})

                malicious = verdict_obj.get("malicious", False)
                score = verdict_obj.get("score", 0) or 0
                categories = verdict_obj.get("categories", [])
                verdict = "malicious" if malicious else "clean"

                return result_url, verdict, score, categories
        except Exception as e:
            print("Error:", e)
            return None, None, None, None

client.run(DISCORD_TOKEN)
