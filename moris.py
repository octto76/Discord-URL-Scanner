import discord
import re 
import aiohttp 
import asyncio 
import os 
import time 
from dotenv import load_dotenv 

load_dotenv() # ts hides API keys I believe 

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
URLSCAN_API_KEY = os.getenv('URLSCAN_API_KEY') 

intents = discord.Intents.default()
intents.message_content = True 
client = discord.Client(intents=intents)

URL_REGEX = r"https?://[^\s]+"
user_cooldowns = {} 
COOLDOWN_SECONDS = 20 


@client.event
async def on_message(message):
    if message.author.bot:
        return

    urls = re.findall(URL_REGEX, message.content)
    if not urls:
        return  # Exit early if there are no links

    user_id = message.author.id
    now = time.time()

    # Rate limit only if user is scanning something
    last_used = user_cooldowns.get(user_id, 0)
    if now - last_used < COOLDOWN_SECONDS:
        await message.reply(
            f"⏳ Please wait {int(COOLDOWN_SECONDS - (now - last_used))}s before scanning again.",
            mention_author=False
        )
        return

    user_cooldowns[user_id] = now

    for url in urls:
        # Known domains we skip scanning
        blocked_domains = ["google.com", "facebook.com", "youtube.com", "twitter.com"]
        if any(domain in url for domain in blocked_domains):
            await message.reply(
                f"⚠️ This domain is not scannable via urlscan.io: {url}",
                mention_author=False,
                suppress_embeds=True
            )
            continue

        await message.reply(
            f"🔍 Scanning: {url}",
            mention_author=False,
            suppress_embeds=True
        )

        async with message.channel.typing():
            result_url, verdict, categories = await scan_and_poll_url(url)

        if result_url:
            verdict_emoji = "🟢" if verdict == "clean" else "🔴"
            category_str = f"({', '.join(categories)})" if categories else ""
            response = (
                f"{verdict_emoji} Verdict: **{verdict.upper()}** {category_str}\n"
                f"🔗 {result_url}"
            )
            await message.reply(response, mention_author=False, suppress_embeds=True)
        else:
            await message.reply(
                f"❌ Failed to scan: {url}",
                mention_author=False,
                suppress_embeds=True
            )



async def scan_and_poll_url(url):
    headers = {"API-Key": URLSCAN_API_KEY, "Content-Type": "application/json"}
    payload = {"url": url, "public": "on"}

    async with aiohttp.ClientSession() as session:
        try:
            # Submit the scan
            async with session.post("https://urlscan.io/api/v1/scan/", json=payload, headers=headers) as res:
                if res.status != 200:
                    return None, None, None
                data = await res.json()
                uuid = data.get("uuid")
                result_url = f"https://urlscan.io/result/{uuid}/"

            # Wait before polling result
            await asyncio.sleep(15)

            # Poll for scan result
            async with session.get(f"https://urlscan.io/api/v1/result/{uuid}/") as res:
                if res.status != 200:
                    return result_url, "unknown", None
                result_data = await res.json()

                verdict_obj = result_data.get("verdicts", {}).get("overall", {})
                malicious = verdict_obj.get("malicious", False)
                categories = verdict_obj.get("categories", [])
                verdict = "malicious" if malicious else "clean"

                return result_url, verdict, categories
        except Exception as e:
            print("Error:", e)
            return None, None, None

client.run(DISCORD_TOKEN)