import discord
from discord.ext import commands
import os
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer

# פתיחת כל ערוצי התקשורת והאוזניים של הבוט מול דיסקורד
intents = discord.Intents.default()
intents.message_content = True  # חובה בשביל לשמוע את הפקודה !pgif
intents.messages = True
intents.guilds = True

# הקמת הבוט הראשי עם סימן הקריאה המקורי
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f"👑 המנוע הראשי נדלק! הבוט {bot.user} מחובר רשמית לדיסקורד.")
    
    # טעינת קובץ האתר (bot.py) לתוך הבוט הראשי בלי לשנות בו כלום
    try:
        from bot import NsfwCog
        await bot.add_cog(NsfwCog(bot))
        print("👑 קוד האתר (NsfwCog) נטען בהצלחה ב-100% ללא שינויים!")
    except Exception as e:
        print(f"שגיאה בטעינת קוד האתר: {e}")

# שרת בריאות חובה עבור הרשת של Render
def run_health_server():
    server = HTTPServer(('0.0.0.0', int(os.environ.get("PORT", 8080))), SimpleHTTPRequestHandler)
    server.serve_forever()

if __name__ == "__main__":
    threading.Thread(target=run_health_server, daemon=True).start()
    token = os.environ.get("DISCORD_TOKEN")
    if token:
        bot.run(token)
