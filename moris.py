import discord
import re
import aiohttp
import asyncio
import os
import time
import base64
import random
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
VIRUSTOTAL_API_KEY = os.getenv("VIRUSTOTAL_API_KEY")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

URL_REGEX = r"https?://[^\s]+"
COOLDOWN_SECONDS = 30
user_cooldowns = {}

# Known IP grabber / logger domains
ip_grabber_domains = [
    "grabify.org", "grabify.link", "bmwforum.co", "catsnthing.com", "catsnthings.fun", "crabrave.pw",
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

    if message.content.strip() == f"<@{client.user.id}>" or message.content.strip() == f"<@!{client.user.id}>":
        cute_responses = [
            "是?",
            "If you don't feed me, it will!",
            "Moris wants blood",
            "Don't tempt moris",
            "I'm gonna eat you"
        ]
        response = random.choice(cute_responses)
        await message.reply(response, mention_author=False)
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
        if any(domain == grabber or domain.endswith(f".{grabber}") for grabber in ip_grabber_domains):
            await message.reply(
                f"🚫 This link is a known IP logger (`{domain}`). Do not click it.",
                mention_author=False,
                suppress_embeds=True
            )
            continue

        # Send initial message and keep reference to edit later
        safe_url = url.replace("://", "://\u200b")
        status_msg = await message.reply(
            f"🔍 Scanning: {safe_url}",
            mention_author=False,
            suppress_embeds=True
        )

        async with message.channel.typing():
            result = await scan_with_virustotal(url)
            if result is None:
                await status_msg.edit(content=f"🔍 Scanning: {safe_url}\n❌ Could not complete scan.")
                return

            verdict, stats, permalink = result
            
        if verdict:
            emoji = {"clean": "🟢", "suspicious": "🟡", "malicious": "🔴"}.get(verdict, "❓")
            report_msg = (
                f"🔍 Scanning: {safe_url}\n"
                f"{emoji} Verdict: **{verdict.upper()}** ({stats['malicious']}/70 engines flagged it)\n"
                f"🔗 <{permalink}>"
            )
            await status_msg.edit(content=report_msg)
        else:
            await status_msg.edit(content=f"🔍 Scanning: {safe_url}\n❌ Could not complete scan.")

async def scan_with_virustotal(url):
    encoded_url = base64.urlsafe_b64encode(url.encode()).decode().strip("=")
    headers = {"x-apikey": VIRUSTOTAL_API_KEY}

    async with aiohttp.ClientSession() as session:
        try:
            # Submit URL for scanning
            async with session.post(
                "https://www.virustotal.com/api/v3/urls",
                headers=headers,
                data={"url": url}
            ) as post_res:
                if post_res.status != 200:
                    return None, None, None
                post_data = await post_res.json()
                analysis_id = post_data["data"]["id"]

            # Poll for result
            for _ in range(6):  # Try for ~15 seconds
                await asyncio.sleep(3)
                async with session.get(
                    f"https://www.virustotal.com/api/v3/analyses/{analysis_id}",
                    headers=headers
                ) as result_res:
                    result_data = await result_res.json()
                    status = result_data["data"]["attributes"]["status"]
                    if status == "completed":
                        stats = result_data["data"]["attributes"]["stats"]
                        positives = stats.get("malicious", 0) + stats.get("suspicious", 0)

                        if positives == 0:
                            verdict = "clean"
                        elif positives <= 4:
                            verdict = "suspicious"
                        else:
                            verdict = "malicious"

                        permalink = f"https://www.virustotal.com/gui/url/{encoded_url}"
                        return verdict, stats, permalink
        except Exception as e:
            print(f"[ERROR] VirusTotal scan failed: {e}")
            return None, None, None
        
if __name__ == "__main__":
    client.run(DISCORD_TOKEN)

