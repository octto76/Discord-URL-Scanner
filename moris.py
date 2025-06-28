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


