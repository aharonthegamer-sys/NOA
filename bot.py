import discord
from discord.ext import commands
import aiohttp
import os
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer

# פתיחת האוזניים של הבוט מול דיסקורד
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# הקמת הבוט הראשי עם סימן קריאה
bot = commands.Bot(command_prefix='!', intents=intents)

# מזהה החדר המדויק שלך מהדיסקורד
CHANNEL_ID = 1503853432992305172

@bot.event
async def on_ready():
    print(f"👑 Bot {bot.user} is live and operational!")
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        try:
            await channel.send("🚀 **הבוט מחובר ומוכן! רשום !pgif או !hentai כדי להתחיל...**")
        except Exception as e:
            print(f"Startup message failed: {e}")

# פקודה 1: סרטונים וגיפים מונפשים (הפקודה מהקוד של האתר)
@bot.command(name='pgif')
async def pgif(ctx):
    if not ctx.channel.nsfw:
        await ctx.send("❌ פקודה זו זמינה רק בערוצי NSFW!")
        return
        
    url = "https://nekobot.xyz"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    file_url = data.get("message", "")
                    if file_url:
                        # שליחה ישירה לחדר הפיזי שלך בצאט
                        await bot.get_channel(CHANNEL_ID).send(file_url)
        except Exception as e:
            print(f"Error in pgif command: {e}")

# פקודה 2: תמונות ואנימציות
@bot.command(name='hentai')
async def hentai(ctx):
    if not ctx.channel.nsfw:
        await ctx.send("❌ פקודה זו זמינה רק בערוצי NSFW!")
        return
        
    url = "https://nekobot.xyz"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    file_url = data.get("message", "")
                    if file_url:
                        await bot.get_channel(CHANNEL_ID).send(file_url)
        except Exception as e:
            print(f"Error in hentai command: {e}")

# שרת רשת חובה עבור ה-Free Tier של Render שלא יכבה את הבוט
def run_health_server():
    server = HTTPServer(('0.0.0.0', int(os.environ.get("PORT", 8080))), SimpleHTTPRequestHandler)
    server.serve_forever()

if __name__ == "__main__":
    threading.Thread(target=run_health_server, daemon=True).start()
    token = os.environ.get("DISCORD_TOKEN")
    if token:
        bot.run(token)
