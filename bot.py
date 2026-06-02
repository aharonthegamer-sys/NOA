import discord
from discord.ext import tasks
import aiohttp
import os
import random
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer

intents = discord.Intents.default()
client = discord.Client(intents=intents)

# מזהה החדר המדויק שלך מדיסקורד
CHANNEL_ID = 1503853432992305172

# משימה מחזורית שרצה כל 45 שניות (קצב יציב ומאוזן לענן)
@tasks.loop(seconds=45)
async def send_nsfw_video():
    channel = client.get_channel(CHANNEL_ID)
    if not channel or not channel.is_nsfw():
        return

    # פנייה ל-API הציבורי של Gelbooru לקבלת פוסטים מונפשים (סרטונים)
    url = "https://gelbooru.com"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    async with aiohttp.ClientSession(headers=headers) as session:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    posts = data.get("post", [])
                    
                    if posts:
                        # בחירת פוסט אקראי מתוך תוצאות ה-API
                        random_post = random.choice(posts)
                        file_url = random_post.get("file_url", "")
                        
                        # וידוא שהקובץ הוא סרטון MP4 ישיר שדיסקורד יפתח כנגן (Play)
                        if file_url and file_url.endswith(('.mp4', '.webm')):
                            await channel.send(file_url)
                            print(f"[Booru-Engine] Video player successfully sent to channel {CHANNEL_ID}")
                else:
                    print(f"[Booru-Engine] API returned error status: {response.status}")
        except Exception as e:
            print(f"[Booru-Engine] Network request error: {e}")

@client.event
async def on_ready():
    print(f"Bot {client.user} is online and fully authenticated!")
    
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        try:
            await channel.send("👑 **ליבת ה-Booru המקצועית הופעלה בהצלחה בפרויקט החדש! הזרמת הנגנים מתחילה...**")
        except Exception as e:
            print(f"Startup prompt failed: {e}")
            
    if not send_nsfw_video.is_running():
        send_nsfw_video.start()

# שרת רשת מובנה (Health Check) חובה עבור Render כדי שהבוט לא ייכבה
def run_health_server():
    class HealthHandler(SimpleHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"Bot Engine Live")

    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), HealthHandler)
    server.serve_forever()

if __name__ == "__main__":
    threading.Thread(target=run_health_server, daemon=True).start()
    
    token = os.environ.get("DISCORD_TOKEN")
    if token:
        client.run(token)
    else:
        print("Error: DISCORD_TOKEN variable is missing.")

