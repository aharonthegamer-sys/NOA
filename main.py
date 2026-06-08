import os
import random
import logging
import threading
import aiohttp
import discord
from discord.ext import commands, tasks
from flask import Flask

# --- הגדרת מערכת לוגים בסיסית ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("DiscordBot")

# --- הגדרת שרת Flask עבור פלטפורמת Render ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is running and healthy!"

def run_flask():
    # שרת רץ על פורט 10000 קבוע כדי לעבור את בדיקת הפורטים של רנדר
    app.run(host='0.0.0.0', port=10000)

# הפעלת שרת האינטרנט ברקע באמצעות תהליכון נפרד (Thread)
flask_thread = threading.Thread(target=run_flask)
flask_thread.daemon = True
flask_thread.start()

# --- הגדרת הבוט של דיסקורד ---
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="?", intents=intents)

# רשימת הקהילות עבור הפיד האוטומטי
SUBREDDITS = ["nsfw", "RealGirls", "NSFW_GIF", "holdthemoan"]

# רשימת הקטגוריות המורשות עבור פקודת האנימה
ALLOWED_CATEGORIES = [
    "anal", "blowjob", "cum", "fuck", "neko", "pussylick", 
    "threesome_fff", "solo", "yaoi", "threesome_mmf", "yuri"
]

@bot.event
async def on_ready():
    logger.info(f"Logged in successfully as {bot.user.name} (ID: {bot.user.id})")
    # הפעלת משימת הרקע המחזורית מיד כשהבוט מתחבר
    if not auto_feed.is_running():
        auto_feed.start()

# --- פיצ'ר 1: משימת רקע אוטומטית (רצה כל 10 דקות) ---
@tasks.loop(minutes=10)
async def auto_feed():
    chosen_sub = random.choice(SUBREDDITS)
    logger.info(f"Starting auto-feed pull from subreddit: r/{chosen_sub}")
    
    # הגדרת כותרות דפדפן כדי ש-Reddit לא יחסום את הבקשה
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    url = f"https://reddit.com{chosen_sub}/random.json"
    
    for guild in bot.guilds:
        # מחפש אוטומטית ערוץ בשם "videos" בשרת
        channel = discord.utils.get(guild.text_channels, name="videos")
        
        # בודק שהערוץ קיים ומסומן כערוץ למבוגרים (NSFW)
        if channel and channel.is_nsfw():
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, headers=headers) as response:
                        if response.status == 200:
                            data = await response.json()
                            
                            # ניתוח מבנה ה-JSON: Reddit מחזיר רשימה במקרה של פוסט אקראי
                            if isinstance(data, list) and len(data) > 0:
                                post_data = data[0]["data"]["children"][0]["data"]
                            elif isinstance(data, dict) and "data" in data:
                                post_data = data["data"]["children"][0]["data"]
                            else:
                                logger.warning(f"Unexpected JSON structure from Reddit API: {type(data)}")
                                continue
                            
                            media_url = post_data.get("url")
                            title = post_data.get("title", "Automatic Update")
                            
                            if media_url:
                                # שליחת הקישור הישיר של המדיה לערוץ הדיסקורד
                                await channel.send(f"🔥 **[r/{chosen_sub}] {title}**\n{media_url}")
                                logger.info(f"Successfully sent media from r/{chosen_sub} to channel #{channel.name}")
                        else:
                            logger.error(f"Reddit API returned status code: {response.status}")
            except Exception as e:
                print(f"[auto_feed error] Failed to process media pull: {e}")

# --- פיצ'ר 2: פקודת אנימה ידנית משולבת אימות קטגוריות ---
@bot.command(name="nsfw")
async def nsfw_cmd(ctx, category: str = "blowjob"):
    # אבטחה: מניעת הרצת הפקודה בערוצים רגילים
    if not ctx.channel.is_nsfw():
        await ctx.send("❌ ניתן להשתמש בפקודה זו רק בערוצים המסומנים כ-NSFW!")
        return
        
    category = category.lower()
    if category not in ALLOWED_CATEGORIES:
        await ctx.send(f"❌ קטגוריה לא תקינה. בחר מהרשימה: {', '.join(ALLOWED_CATEGORIES)}")
        return
        
    url = f"https://purrbot.site{category}/gif"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    media_link = data.get("link")
                    
                    if media_link:
                        # יצירת כרטיסייה מעוצבת (Embed) להצגת ה-GIF
                        embed = discord.Embed(
                            title=f"🔥 קטגוריית NOA: {category.upper()}", 
                            color=0xff0055
                        )
                        embed.set_image(url=media_link)
                        await ctx.send(embed=embed)
                    else:
                        await ctx.send("❌ לא נמצא קישור תקין למדיה בתוך תשובת השרת.")
                else:
                    await ctx.send(f"❌ תקלה בתקשורת עם שרת המדיה (סטטוס: {response.status}).")
    except Exception as e:
        await ctx.send(f"❌ שגיאה בהרצת הפקודה.")
        print(f"[nsfw_cmd error] Exception triggered: {e}")

# --- הרצת הבוט באמצעות הטוקן המאובטח ---
token = os.getenv("DISCORD_TOKEN")
if token:
    bot.run(token)
else:
    logger.critical("DISCORD_TOKEN variable is missing from environmental variables!")
