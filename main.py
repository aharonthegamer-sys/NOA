import discord
from discord.ext import commands, tasks
import requests
import os
import random
from flask import Flask
from threading import Thread

# שרת Flask לעקיפת הפורט של רנדר בחינם
app = Flask('')
@app.route('/')
def home(): return "Bot is alive!"
def run_flask(): app.run(host='0.0.0.0', port=10000)

t = Thread(target=run_flask)
t.daemon = True
t.start()

token = os.getenv("DISCORD_TOKEN")
prefix = "?"
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=prefix, intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    auto_feed.start()

# משימה אוטומטית שרצה ברקע מקהילות Reddit
@tasks.loop(minutes=10)
async def auto_feed():
    subreddits = ["nsfw", "RealGirls", "NSFW_GIF", "holdthemoan"]
    chosen_sub = random.choice(subreddits)
    for guild in bot.guilds:
        channel = discord.utils.get(guild.text_channels, name="videos")
        if channel and channel.is_nsfw():
            url = f"https://reddit.com{chosen_sub}/random.json"
            headers = {"User-Agent": "Mozilla/5.0"}
            try:
                response = requests.get(url, headers=headers).json()
                if isinstance(response, list) and len(response) > 0:
                    post = response[0]["data"]["children"][0]["data"]
                elif isinstance(response, dict):
                    post = response["data"]["children"][0]["data"]
                else:
                    continue
                video_url = post.get("url")
                if video_url:
                    await channel.send(video_url)
            except Exception:
                pass

ALLOWED_CATEGORIES = ["anal", "blowjob", "cum", "fuck", "neko", "pussylick", "threesome_fff", "solo", "yaoi", "threesome_mmf", "yuri"]

# פקודת האנימה הידנית המתוקנת והבטוחה
@bot.command(name="nsfw")
async def nsfw_cmd(ctx, category: str = "blowjob"):
    if not ctx.channel.is_nsfw():
        await ctx.send("❌ ניתן להשתמש בפקודה זו רק בערוצים המסומנים כ-NSFW!")
        return
    if category not in ALLOWED_CATEGORIES:
        await ctx.send(f"❌ בחר קטגוריה תקינה: {', '.join(ALLOWED_CATEGORIES)}")
        return
    url = f"https://purrbot.site{category}/gif"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers).json()
        media_link = response.get("link")
        if media_link:
            embed = discord.Embed(title=f"🔥 קטגוריית NOA: {category.upper()}", color=0xff0055)
            embed.set_image(url=media_link)
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ שגיאה: הקישור לא התקבל מהאתר.")
    except Exception:
        await ctx.send("❌ שגיאה בהרצת הפקודה.")

bot.run(token)
