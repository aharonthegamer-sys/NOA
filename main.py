import discord
from discord.ext import commands
import os
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# הגדרת הבוט והסימן קריאה המקורי של הפרויקט
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f"👑 Bot {bot.user} is live and ready!")
    # טעינת קובץ הפקודות המקורי של האתר שהעתקת (הקובץ bot.py שלך)
    try:
        from bot import NsfwCog
        await bot.add_cog(NsfwCog(bot))
        print("Successfully loaded NsfwCog from your file!")
    except Exception as e:
        print(f"Error loading your file: {e}")

# שרת רשת חובה עבור Render שלא יכבה את הבוט בתוכנית החינמית
def run_health_server():
    server = HTTPServer(('0.0.0.0', int(os.environ.get("PORT", 8080))), SimpleHTTPRequestHandler)
    server.serve_forever()
if __name__ == "__main__":
    threading.Thread(target=run_health_server, daemon=True).start()
    token = os.environ.get("DISCORD_TOKEN")
    if token:
        bot.run(token)
    else:
        print("Error: DISCORD_TOKEN is missing in Environment Variables.")
