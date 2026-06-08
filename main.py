import discord
from discord.ext import commands, tasks
import aiohttp
import os
import random
import threading
from flask import Flask

# ── Flask keep-alive (required for Render free tier) ────────────────────────
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!", 200

def run_flask():
    app.run(host="0.0.0.0", port=10000)

threading.Thread(target=run_flask, daemon=True).start()

# ── Bot setup ────────────────────────────────────────────────────────────────
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="?", intents=intents)

# Replace with your chosen SFW subreddits
SUBREDDITS = ["pics", "EarthPorn", "itookapicture", "photographs"]

# ── Background task ──────────────────────────────────────────────────────────
@tasks.loop(minutes=10)
async def auto_feed():
    subreddit = random.choice(SUBREDDITS)
    # Exact URL string as requested — append subreddit path at runtime
    base_url = "https://reddit.com"
    url = f"{base_url}/r/{subreddit}/random.json"
    headers = {"User-Agent": "DiscordBot/1.0"}

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, allow_redirects=True) as resp:
                if resp.status != 200:
                    return
                data = await resp.json()

        post = data[0]["data"]["children"][0]["data"]
        post_url = post.get("url", "")

        if not any(post_url.lower().endswith(ext) for ext in (".jpg", ".jpeg", ".png", ".gif", ".mp4")):
            return

        for guild in bot.guilds:
            channel = discord.utils.get(guild.text_channels, name="videos")
            if channel and channel.permissions_for(guild.me).send_messages:
                await channel.send(post_url)
                break

    except Exception as e:
        print(f"[auto_feed error] {e}")

@auto_feed.before_loop
async def before_feed():
    await bot.wait_until_ready()

# ── Events ───────────────────────────────────────────────────────────────────
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    auto_feed.start()

# ── ?nsfw command ─────────────────────────────────────────────────────────────
# Allowed SFW categories from purrbot.site — swap path prefix to /api/img/sfw
ALLOWED_CATEGORIES = ["anal", "blowjob", "cum", "fuck", "neko", "pussylick", "threesome_fff", "solo", "yaoi", "threesome_mmf", "yuri"]

@bot.command(name="nsfw")
async def nsfw_cmd(ctx, category: str = "blowjob"):
    if not ctx.channel.is_nsfw():
        await ctx.send("❌ ניתן להשתמש בפקודה זו רק בערוצים המסומנים כ-NSFW!")
        return
        
    if category not in ALLOWED_CATEGORIES:
        await ctx.send(f"❌ בחר קטגוריה תקינה: {', '.join(ALLOWED_CATEGORIES)}")
        return
        
    url = f"https://purrbot.site{category}/gif"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                embed = discord.Embed(title=f"🔥 קטגוריית NOA: {category.upper()}", color=0xff0055)
                embed.set_image(url=data.get("link"))

        await ctx.send(
            f"Unknown category. Available:\n`{'`, `'.join(ALLOWED_CATEGORIES)}`"
        )
        return

    # Exact URL pattern as requested
    api_url = f"https://purrbot.site{category}/gif"

    async with ctx.typing():
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(api_url) as resp:
                    if resp.status != 200:
                        await ctx.send(f"API returned status {resp.status}.")
                        return
                    data = await resp.json()

            gif_url = data.get("link", "")
            if not gif_url:
                await ctx.send("No gif returned from the API.")
                return

            embed = discord.Embed(
                title=category.split("/")[-2],  # e.g. "neko"
                color=discord.Color.purple()
            )
            embed.set_image(url=gif_url)
            embed.set_footer(
                text=f"purrbot.site • requested by {ctx.author.display_name}"
            )
            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"Something went wrong: `{e}`")

# ── Error handler ─────────────────────────────────────────────────────────────
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Missing argument. See `?help {ctx.command}`.")
    elif isinstance(error, commands.CommandNotFound):
        pass
    else:
        print(f"[command error] {error}")

# ── Run ───────────────────────────────────────────────────────────────────────
TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN environment variable is not set.")

bot.run(TOKEN)
