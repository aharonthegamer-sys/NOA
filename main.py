import discord
from discord.ext import commands
import requests
import os

token = os.getenv("DISCORD_TOKEN")
prefix = "?"
intents = discord.Intents.all()
client = commands.Bot(command_prefix=prefix, intents=intents)

client.remove_command("help") #to remove the default boring help command


@client.event
async def on_ready():
    print("We have logged in as {0.user} ".format(client)) 
    activity = discord.Game(name=".help", type=3)               # this is to writing prefix in playing a game.(optional)
    await client.change_presence(status=discord.Status.online, activity=activity) # this is for making the status as an online and writing prefix in playing a game.(optional)  
                            
                            
                            
                            
#Help commands
@client.group(invoke_without_command=True)
async def help(ctx):
    embed = discord.Embed(title="IndianDesiMemer Help Center ✨",color=0xF49726)
    embed.add_field(name="Command Categories :",value="🐸 `memes    :` Image generation with a memey twist.\n" + "🔧 `utility  :` Bot utility zone\n😏 `nsfw     :` Image generation with a memey twist.\n\nTo view the commands of a category, send `.help <category>`" ,inline=False)
    embed.set_footer(icon_url=ctx.author.avatar_url,text="Help requested by: {}".format(ctx.author.display_name))
    await ctx.send(embed=embed)
                            

#Sub-help command of memes
@help.command ()
async def memes(ctx):
    embed=discord.Embed(title="IndianDesiMemer Help Center ✨", description="Commands of **meme** \n`.meme:`Memes",inline=False)
    embed.set_footer(icon_url=ctx.author.avatar_url,text="Command requested by: {}".format(ctx.author.display_name))
    await ctx.send(embed=embed)
                            

#Sub-help commands of nsfw                           
@help.command ()
async def nsfw(ctx) :
    embed=discord.Embed(title="IndianDesiMemer Help Center ✨", description="Commands of **nsfw** \n`.nsfw:`NSFW", color=0xF49726)
    embed.set_footer(icon_url=ctx.author.avatar_url,text="Command requested by: {}".format(ctx.author.display_name))
    await ctx.send(embed=embed)


#Sub-help commands of utility                           
@help.command ()
async def utility(ctx) :
    embed=discord.Embed(title="IndianDesiMemer Help Center ✨", description="Commands of **utility** \n`.ping:`Latency", color=0xF49726)
    embed.set_footer(icon_url=ctx.author.avatar_url,text="Command requested by: {}".format(ctx.author.display_name))
    await ctx.send(embed=embed)                            


# it is used for the cooldown to prevent the bot from spam attack                             
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send("**Try after {0} second ".format(round(error.retry_after, 2)))                            
                            
                            
#meme command                            
@client.command()
@commands.cooldown(1, 10, commands.BucketType.channel) # it is used for the cooldown to prevent the bot from spam attack                            
async def meme(ctx):
    
    response = requests.get("https://meme-api.herokuapp.com/gimme/"+"memes"+"memes"+"?t=all?hot")
    
    m = response.json()
    postLink = (m["postLink"])
    subreddit = (m["subreddit"])
    title = (m["title"])
    imageUrl =  (m["url"])
    upVote = (m["ups"])
    uv = str(upVote)

    embed=discord.Embed(title= title, url=postLink,color=0xF49726)
    embed.set_image(url=imageUrl)
    embed.set_footer(text="\n👍\t"+ uv+ "  By :r/"+subreddit)
    await ctx.send(embed=embed)                            
                            
#nsfw command
@client.command(name="nsfw")
async def nsfw(ctx, category: str = None):
    if not ctx.channel.is_nsfw():
        await ctx.send("❌ ניתן להשתמש בפקודה זו רק בערוצים המסומנים כ-NSFW!")
        return

    valid_categories = ["anal", "blowjob", "cum", "fuck", "neko", "pussylick", "threesome_fff", "solo", "yaoi", "threesome_mmf", "yuri"]

    if category not in valid_categories:
        await ctx.send(f"❌ בחר קטגוריה תקינה מהרשימה: {', '.join(valid_categories)}")
        return

    url = f"https://purrbot.site/api/img/nsfw/{category}/gif"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers).json()
        image_url = response.get("link")
        
        embed = discord.Embed(title=f"🔥 קטגוריית NOA: {category.upper()}", color=0xff0055)
        embed.set_image(url=image_url)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ תקלה: {str(e)}")

 
        @client.command(name="real")
    async def real(ctx):
        if not ctx.channel.is_nsfw():
            await ctx.send("❌ ניתן להשתמש בפקודה זו רק בערוצים המסומנים כ-NSFW!")
            return

        # פנייה ישירה לצינור הפתוח של Reddit לשליפת סרטון או תמונה אמיתיים
        url = "https://reddit.com"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        
        try:
            response = requests.get(url, headers=headers).json()
            # Reddit מחזיר רשימה, אנחנו שולפים את הפוסט האקראי
            post_data = response[0]["data"]["children"][0]["data"]
            
            video_url = post_data.get("url")
            title = post_data.get("title", "Real IRL Media")
            
            if not video_url:
                await ctx.send("❌ לא נמצאה מדיה, נסה שוב.")
                return
                
            # שליחת הקישור ישירות לצ'אט (דיסקורד פותח את זה בנגן מלא)
            await ctx.send(f"🔥 **{title}**\n{video_url}")
        except Exception as e:
            await ctx.send(f"❌ תקלה במשיכת המדיה מ-Reddit. שגיאה: {str(e)}")

client.run(token)
