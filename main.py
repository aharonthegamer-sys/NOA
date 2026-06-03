import discord
from discord.ext import commands, tasks
import requests
import os

token = os.getenv("DISCORD_TOKEN")
prefix = "?"
intents = discord.Intents.all()
client = commands.Bot(command_prefix=prefix, intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user.name}")
    # הפעלת הלולאה האוטומטית ברגע שהבוט נדלק
    auto_real_videos.start()

# משימה אוטומטית שרצה כל 10 דקות ושולחת סרטון/תמונה אמיתיים מ-Reddit
@tasks.loop(minutes=10)
async def auto_real_videos():
    # הבוט יחפש ערוץ בשם videos בשרת שלך וישלח אליו אוטומטית
    for guild in client.guilds:
        channel = discord.utils.get(guild.text_channels, name="videos")
        if channel and channel.is_nsfw():
            url = "https://reddit.com"
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
            try:
                response = requests.get(url, headers=headers).json()
                post_data = response[0]["data"]["children"][0]["data"]
                video_url = post_data.get("url")
                title = post_data.get("title", "Real IRL Media")
                
                if video_url:
                    await channel.send(f"🔥 **סרטון אוטומטי חדש (IRL):** {title}\n{video_url}")
            except Exception:
                pass

@client.command(name="nsfw")
async def nsfw(ctx, category: str = None):
    if not ctx.channel.is_nsfw():
        await ctx.send("❌ ניתן להשתמש בפקודה זו רק בערוצים המסומנים כ-NSFW!")
        return
    valid_categories = ["anal", "blowjob", "cum", "fuck", "neko", "pussylick", "threesome_fff", "solo", "yaoi", "threesome_mmf", "yuri"]
    if category not in valid_categories:
        await ctx.send(f"❌ בחר קטגוריה תקינה מהרשימה: {', '.join(valid_categories)}")
        return
    url = f"https://purrbot.site{category}/gif"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers).json()
        image_url = response.get("link")
        embed = discord.Embed(title=f"🔥 קטגוריית NOA: {category.upper()}", color=0xff0055)
        embed.set_image(url=image_url)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ תקלה במשיכת המדיה. שגיאה: {str(e)}")

client.run(token)
