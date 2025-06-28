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

    user_id = message.author.id
    now = time.time()

    # Rate limit check
    last_used = user_cooldowns.get(user_id, 0)
    if now - last_used < COOLDOWN_SECONDS:
        await message.channel.send(f"⏳ Please wait {int(COOLDOWN_SECONDS - (now - last_used))}s before scanning again.")
        return

    urls = re.findall(URL_REGEX, message.content)
    if urls:
        user_cooldowns[user_id] = now  # Update cooldown
        for url in urls:
            await message.channel.send(f"🔍 Scanning: {url}")
            result_url, verdict, categories = await scan_and_poll_url(url)
            if result_url:
                verdict_emoji = "🟢" if verdict == "clean" else "🔴"
                category_str = f"({', '.join(categories)})" if categories else ""
                await message.channel.send(
                    f"{verdict_emoji} Verdict: **{verdict.upper()}** {category_str}\n🔗 {result_url}"
                )
            else:
                await message.channel.send(f"❌ Failed to scan: {url}")

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