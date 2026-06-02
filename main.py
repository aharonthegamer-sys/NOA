import discord
from discord.ext import commands
import os
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer

# פתיחת כל ערוצי התקשורת והאוזניים של הבוט מול דיסקורד (חובה בשנת 2026!)
intents = discord.Intents.default()
intents.message_content = True  # מאפשר לבוט לשמוע שכתבת !pgif
intents.messages = True
intents.guilds = True

# הקמת הבוט הראשי עם סימן הקריאה המקורי
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f"👑 Bot {bot.user} is live and ready on Discord!")
    
    # טעינת קובץ האתר (bot.py) שבו החלפת את ה-CTX
    try:
        from bot import NsfwCog
        await bot.add_cog(NsfwCog(bot))
        print("👑 Successfully loaded NsfwCog from your bot.py file!")
    except Exception as e:
        print(f"Error loading your file: {e}")

# שרת בריאות חובה עבור הרשת של Render
def run_health_server():
    server = HTTPServer(('0.0.0.0', int(os.environ.get("PORT", 8080))), SimpleHTTPRequestHandler)
    server.serve_forever()

if __name__ == "__main__":
    threading.Thread(target=run_health_server, daemon=True).start()
    token = os.environ.get("DISCORD_TOKEN")
    if token:
        bot.run(token)
