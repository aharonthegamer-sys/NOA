from discord.ext import commands
from discord import Embed as AkagiEmbed
from AkagiModules.Config.Config import reddit_client_id as RedditAkagiClientID
from AkagiModules.Config.Config import reddit_client_secret as RedditAkagiClientSecret
from AkagiModules.Config.Config import reddit_user_agent as RedditAkagiUserAgent
import discord
import datetime
import aiohttp
import random
import praw 
from discord.ext import tasks
# לופ אוטומטי שרץ בכל 20 שניות ושולח קליפים ישירות לחדר שלך
@tasks.loop(seconds=20)
async def auto_nsfw_stream():
    await client.wait_until_ready()
    channel = client.get_channel(1503853432992305172)
    if not channel or not channel.is_nsfw():
        return
        
    url = "https://nekobot.xyz"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    file_url = data.get("message", "")
                    if file_url:
                        await channel.send(file_url)
                        print("Auto video sent successfully!")
        except Exception as e:
            print(f"Error: {e}")

# פקודה שמפעילה את הלופ אוטומטית ברגע שהבוט מתחבר
@client.event
async def on_ready():
    print(f"Bot {client.user} is live and auto-streaming!")
    if not auto_nsfw_stream.is_running():
        auto_nsfw_stream.start()


reddit = praw.Reddit(client_id=RedditAkagiClientID,
                     client_secret=RedditAkagiClientSecret,
                     user_agent=RedditAkagiUserAgent, check_for_async=False)

class NsfwCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(no_pm=True)
    @commands.is_nsfw()
    async def pawg(self, ctx):
        subreddit = reddit.subreddit('pawg')
        all_subs = []		
        top = subreddit.top(limit=5)
        for submission in top:
           all_subs.append(submission)			
        random_sub = random.choice(all_subs)		   

        name = random_sub.title		
        url = random_sub.url
        embed = AkagiEmbed(title=f"Pawg!",
                               description=f'[*{name}*]({url})',
                               timestamp=datetime.datetime.utcnow(),
                               color=discord.Color.red())
        embed.set_image(url=url)
        embed.set_author(name=ctx.me.display_name, icon_url=ctx.me.avatar_url)
        embed.set_footer(text="{}".format(ctx.author.display_name),
                         icon_url=ctx.author.avatar_url)
        (embed=embed)

    @pawg.error
    async def pawg_error_handler(self, ctx, error):
        if isinstance(error, commands.NSFWChannelRequired):
            embed = AkagiEmbed(
                title=f"Error",
                description='*This command is Only for NSFW Channels!*',
                timestamp=datetime.datetime.utcnow(),
                color=discord.Color.red())
            embed.set_author(name=ctx.me.display_name,
                             icon_url=ctx.me.avatar_url)
            embed.set_footer(text="{}".format(ctx.author.display_name),
                             icon_url=ctx.author.avatar_url)
            return (embed=embed)

    @commands.command(no_pm=True)
    @commands.is_nsfw()
    async def ass(self, ctx):
        subreddit = reddit.subreddit('ass')
        all_subs = []		
        top = subreddit.top(limit=5)
        for submission in top:
           all_subs.append(submission)			
        random_sub = random.choice(all_subs)		   

        name = random_sub.title		
        url = random_sub.url
        embed = AkagiEmbed(title=f"Ass!",
                               description=f'[*{name}*]({url})',
                               timestamp=datetime.datetime.utcnow(),
                               color=discord.Color.red())
        embed.set_image(url=url)
        embed.set_author(name=ctx.me.display_name, icon_url=ctx.me.avatar_url)
        embed.set_footer(text="{}".format(ctx.author.display_name),
                         icon_url=ctx.author.avatar_url)
        (embed=embed)

    @ass.error
    async def ass_error_handler(self, ctx, error):
        if isinstance(error, commands.NSFWChannelRequired):
            embed = AkagiEmbed(
                title=f"Error",
                description='*This command is Only for NSFW Channels!*',
                timestamp=datetime.datetime.utcnow(),
                color=discord.Color.red())
            embed.set_author(name=ctx.me.display_name,
                             icon_url=ctx.me.avatar_url)
            embed.set_footer(text="{}".format(ctx.author.display_name),
                             icon_url=ctx.author.avatar_url)
            return (embed=embed)
    
    @commands.command(no_pm=True)
    @commands.is_nsfw()
    async def pussy(self, ctx):
        subreddit = reddit.subreddit('pussy')
        all_subs = []		
        top = subreddit.top(limit=5)
        for submission in top:
           all_subs.append(submission)			
        random_sub = random.choice(all_subs)		   

        name = random_sub.title		
        url = random_sub.url
        embed = AkagiEmbed(title=f"Pussy!",
                               description=f'[*{name}*]({url})',
                               timestamp=datetime.datetime.utcnow(),
                               color=discord.Color.red())
        embed.set_image(url=url)
        embed.set_author(name=ctx.me.display_name, icon_url=ctx.me.avatar_url)
        embed.set_footer(text="{}".format(ctx.author.display_name),
                         icon_url=ctx.author.avatar_url)
                await client.get_channel(1503853432992305172).send(embed=embed)

    @pussy.error
    async def pussy_error_handler(self, ctx, error):
        if isinstance(error, commands.NSFWChannelRequired):
            embed = AkagiEmbed(
                title=f"Error",
                description='*This command is Only for NSFW Channels!*',
                timestamp=datetime.datetime.utcnow(),
                color=discord.Color.red())
            embed.set_author(name=ctx.me.display_name,
                             icon_url=ctx.me.avatar_url)
            embed.set_footer(text="{}".format(ctx.author.display_name),
                             icon_url=ctx.author.avatar_url)
            return (embed=embed)
    
    @commands.command(no_pm=True)
    @commands.is_nsfw()
    async def boobs(self, ctx):
        subreddit = reddit.subreddit('boobs')
        all_subs = []		
        top = subreddit.top(limit=5)
        for submission in top:
           all_subs.append(submission)			
        random_sub = random.choice(all_subs)		   

        name = random_sub.title		
        url = random_sub.url
        embed = AkagiEmbed(title=f"Boobs!",
                               description=f'[*{name}*]({url})',
                               timestamp=datetime.datetime.utcnow(),
                               color=discord.Color.red())
        embed.set_image(url=url)
        embed.set_author(name=ctx.me.display_name, icon_url=ctx.me.avatar_url)
        embed.set_footer(text="{}".format(ctx.author.display_name),
                         icon_url=ctx.author.avatar_url)
        await client.get_channel(1503853432992305172).send(embed=embed)(embed=embed)

    @boobs.error
    async def boobs_error_handler(self, ctx, error):
        if isinstance(error, commands.NSFWChannelRequired):
            embed = AkagiEmbed(
                title=f"Error",
                description='*This command is Only for NSFW Channels!*',
                timestamp=datetime.datetime.utcnow(),
                color=discord.Color.red())
            embed.set_author(name=ctx.me.display_name,
                             icon_url=ctx.me.avatar_url)
            embed.set_footer(text="{}".format(ctx.author.display_name),
                             icon_url=ctx.author.avatar_url)
            return await client.get_channel(1503853432992305172).send(embed=embed)(embed=embed)
    
    @commands.command(no_pm=True)
    @commands.is_nsfw()
    async def bdsm(self, ctx):
        subreddit = reddit.subreddit('bdsm')
        all_subs = []		
        top = subreddit.top(limit=5)
        for submission in top:
           all_subs.append(submission)			
        random_sub = random.choice(all_subs)		   

        name = random_sub.title		
        url = random_sub.url
        embed = AkagiEmbed(title=f"Bdsm!",
                               description=f'[*{name}*]({url})',
                               timestamp=datetime.datetime.utcnow(),
                               color=discord.Color.red())
        embed.set_image(url=url)
        embed.set_author(name=ctx.me.display_name, icon_url=ctx.me.avatar_url)
        embed.set_footer(text="{}".format(ctx.author.display_name),
                         icon_url=ctx.author.avatar_url)
        await client.get_channel(1503853432992305172).send(embed=embed)(embed=embed)

    @bdsm.error
    async def bdsm_error_handler(self, ctx, error):
        if isinstance(error, commands.NSFWChannelRequired):
            embed = AkagiEmbed(
                title=f"Error",
                description='*This command is Only for NSFW Channels!*',
                timestamp=datetime.datetime.utcnow(),
                color=discord.Color.red())
            embed.set_author(name=ctx.me.display_name,
                             icon_url=ctx.me.avatar_url)
            embed.set_footer(text="{}".format(ctx.author.display_name),
                             icon_url=ctx.author.avatar_url)
            return await client.get_channel(1503853432992305172).send(embed=embed)(embed=embed)
    
    @commands.command(no_pm=True)
    @commands.is_nsfw()
    async def kinky(self, ctx):
        subreddit = reddit.subreddit('kinky')
        all_subs = []		
        top = subreddit.top(limit=5)
        for submission in top:
           all_subs.append(submission)			
        random_sub = random.choice(all_subs)		   

        name = random_sub.title		
        url = random_sub.url
        embed = AkagiEmbed(title=f"Kinky!",
                               description=f'[*{name}*]({url})',
                               timestamp=datetime.datetime.utcnow(),
                               color=discord.Color.red())
        embed.set_image(url=url)
        embed.set_author(name=ctx.me.display_name, icon_url=ctx.me.avatar_url)
        embed.set_footer(text="{}".format(ctx.author.display_name),
                         icon_url=ctx.author.avatar_url)
        await client.get_channel(1503853432992305172).send(embed=embed)(embed=embed)

    @kinky.error
    async def kinky_error_handler(self, ctx, error):
        if isinstance(error, commands.NSFWChannelRequired):
            embed = AkagiEmbed(
                title=f"Error",
                description='*This command is Only for NSFW Channels!*',
                timestamp=datetime.datetime.utcnow(),
                color=discord.Color.red())
            embed.set_author(name=ctx.me.display_name,
                             icon_url=ctx.me.avatar_url)
            embed.set_footer(text="{}".format(ctx.author.display_name),
                             icon_url=ctx.author.avatar_url)
            return await client.get_channel(1503853432992305172).send(embed=embed)(embed=embed)
    
    @commands.command(no_pm=True)
    @commands.is_nsfw()
    async def collared(self, ctx):
        subreddit = reddit.subreddit('collared')
        all_subs = []		
        top = subreddit.top(limit=5)
        for submission in top:
           all_subs.append(submission)			
        random_sub = random.choice(all_subs)		   

        name = random_sub.title		
        url = random_sub.url
        embed = AkagiEmbed(title=f"Collared!",
                               description=f'[*{name}*]({url})',
                               timestamp=datetime.datetime.utcnow(),
                               color=discord.Color.red())
        embed.set_image(url=url)
        embed.set_author(name=ctx.me.display_name, icon_url=ctx.me.avatar_url)
        embed.set_footer(text="{}".format(ctx.author.display_name),
                         icon_url=ctx.author.avatar_url)
        await client.get_channel(1503853432992305172).send(embed=embed)(embed=embed)

    @collared.error
    async def collared_error_handler(self, ctx, error):
        if isinstance(error, commands.NSFWChannelRequired):
            embed = AkagiEmbed(
                title=f"Error",
                description='*This command is Only for NSFW Channels!*',
                timestamp=datetime.datetime.utcnow(),
                color=discord.Color.red())
            embed.set_author(name=ctx.me.display_name,
                             icon_url=ctx.me.avatar_url)
            embed.set_footer(text="{}".format(ctx.author.display_name),
                             icon_url=ctx.author.avatar_url)
            return await client.get_channel(1503853432992305172).send(embed=embed)(embed=embed)
    
    @commands.command(no_pm=True)
    @commands.is_nsfw()
    async def bottomless(self, ctx):
        subreddit = reddit.subreddit('Bottomless')
        all_subs = []		
        top = subreddit.top(limit=5)
        for submission in top:
           all_subs.append(submission)			
        random_sub = random.choice(all_subs)		   

        name = random_sub.title		
        url = random_sub.url
        embed = AkagiEmbed(title=f"Bottomless!",
                               description=f'[*{name}*]({url})',
                               timestamp=datetime.datetime.utcnow(),
                               color=discord.Color.red())
        embed.set_image(url=url)
        embed.set_author(name=ctx.me.display_name, icon_url=ctx.me.avatar_url)
        embed.set_footer(text="{}".format(ctx.author.display_name),
                         icon_url=ctx.author.avatar_url)
        await client.get_channel(1503853432992305172).send(embed=embed)(embed=embed)

    @bottomless.error
    async def bottomless_error_handler(self, ctx, error):
        if isinstance(error, commands.NSFWChannelRequired):
            embed = AkagiEmbed(
                title=f"Error",
                description='*This command is Only for NSFW Channels!*',
                timestamp=datetime.datetime.utcnow(),
                color=discord.Color.red())
            embed.set_author(name=ctx.me.display_name,
                             icon_url=ctx.me.avatar_url)
            embed.set_footer(text="{}".format(ctx.author.display_name),
                             icon_url=ctx.author.avatar_url)
            return await client.get_channel(1503853432992305172).send(embed=embed)(embed=embed)
    
    @commands.command(no_pm=True)
    @commands.is_nsfw()
    async def dick(self, ctx):
        subreddit = reddit.subreddit('penis')
        all_subs = []		
        top = subreddit.top(limit=5)
        for submission in top:
           all_subs.append(submission)			
        random_sub = random.choice(all_subs)		   

        name = random_sub.title		
        url = random_sub.url
        embed = AkagiEmbed(title=f"Dick!",
                               description=f'[*{name}*]({url})',
                               timestamp=datetime.datetime.utcnow(),
                               color=discord.Color.red())
        embed.set_image(url=url)
        embed.set_author(name=ctx.me.display_name, icon_url=ctx.me.avatar_url)
        embed.set_footer(text="{}".format(ctx.author.display_name),
                         icon_url=ctx.author.avatar_url)
        await client.get_channel(1503853432992305172).send(embed=embed)(embed=embed)

    @dick.error
    async def dick_error_handler(self, ctx, error):
        if isinstance(error, commands.NSFWChannelRequired):
            embed = AkagiEmbed(
                title=f"Error",
                description='*This command is Only for NSFW Channels!*',
                timestamp=datetime.datetime.utcnow(),
                color=discord.Color.red())
            embed.set_author(name=ctx.me.display_name,
                             icon_url=ctx.me.avatar_url)
            embed.set_footer(text="{}".format(ctx.author.display_name),
                             icon_url=ctx.author.avatar_url)
            return await client.get_channel(1503853432992305172).send(embed=embed)(embed=embed)
            
    @commands.command(no_pm=True)
    @commands.is_nsfw()
    async def redhead(self, ctx):
        subreddit = reddit.subreddit('redhead')
        all_subs = []		
        top = subreddit.top(limit=5)
        for submission in top:
           all_subs.append(submission)			
        random_sub = random.choice(all_subs)		   

        name = random_sub.title		
        url = random_sub.url
        embed = AkagiEmbed(title=f"Redhead!",
                               description=f'[*{name}*]({url})',
                               timestamp=datetime.datetime.utcnow(),
                               color=discord.Color.red())
        embed.set_image(url=url)
        embed.set_author(name=ctx.me.display_name, icon_url=ctx.me.avatar_url)
        embed.set_footer(text="{}".format(ctx.author.display_name),
                         icon_url=ctx.author.avatar_url)
        await client.get_channel(1503853432992305172).send(embed=embed)(embed=embed)

    @redhead.error
    async def redhead_error_handler(self, ctx, error):
        if isinstance(error, commands.NSFWChannelRequired):
            embed = AkagiEmbed(
                title=f"Error",
                description='*This command is Only for NSFW Channels!*',
                timestamp=datetime.datetime.utcnow(),
                color=discord.Color.red())
            embed.set_author(name=ctx.me.display_name,
                             icon_url=ctx.me.avatar_url)
            embed.set_footer(text="{}".format(ctx.author.display_name),
                             icon_url=ctx.author.avatar_url)
            return await client.get_channel(1503853432992305172).send(embed=embed)(embed=embed)
            
    @commands.command(no_pm=True)
    @commands.is_nsfw()
    async def chubby(self, ctx):
        subreddit = reddit.subreddit('chubby')
        all_subs = []		
        top = subreddit.top(limit=5)
        for submission in top:
           all_subs.append(submission)			
        random_sub = random.choice(all_subs)		   

        name = random_sub.title		
        url = random_sub.url
        embed = AkagiEmbed(title=f"Chubby!",
                               description=f'[*{name}*]({url})',
                               timestamp=datetime.datetime.utcnow(),
                               color=discord.Color.red())
        embed.set_image(url=url)
        embed.set_author(name=ctx.me.display_name, icon_url=ctx.me.avatar_url)
        embed.set_footer(text="{}".format(ctx.author.display_name),
                         icon_url=ctx.author.avatar_url)
        await client.get_channel(1503853432992305172).send(embed=embed)(embed=embed)

    @chubby.error
    async def chubby_error_handler(self, ctx, error):
        if isinstance(error, commands.NSFWChannelRequired):
            embed = AkagiEmbed(
                title=f"Error",
                description='*This command is Only for NSFW Channels!*',
                timestamp=datetime.datetime.utcnow(),
                color=discord.Color.red())
            embed.set_author(name=ctx.me.display_name,
                             icon_url=ctx.me.avatar_url)
            embed.set_footer(text="{}".format(ctx.author.display_name),
                             icon_url=ctx.author.avatar_url)
            return await client.get_channel(1503853432992305172).send(embed=embed)(embed=embed)
            
    @commands.command(no_pm=True)
    @commands.is_nsfw()
    async def nsfw(self, ctx):
        subreddit = reddit.subreddit('nsfw')
        all_subs = []		
        top = subreddit.top(limit=5)
        for submission in top:
           all_subs.append(submission)			
        random_sub = random.choice(all_subs)		   

        name = random_sub.title		
        url = random_sub.url
        embed = AkagiEmbed(title=f"Random Nsfw!",
                               description=f'[*{name}*]({url})',
                               timestamp=datetime.datetime.utcnow(),
                               color=discord.Color.red())
        embed.set_image(url=url)
        embed.set_author(name=ctx.me.display_name, icon_url=ctx.me.avatar_url)
        embed.set_footer(text="{}".format(ctx.author.display_name),
                         icon_url=ctx.author.avatar_url)
        await client.get_channel(1503853432992305172).send(embed=embed)(embed=embed)

    @nsfw.error
    async def nsfw_error_handler(self, ctx, error):
        if isinstance(error, commands.NSFWChannelRequired):
            embed = AkagiEmbed(
                title=f"Error",
                description='*This command is Only for NSFW Channels!*',
                timestamp=datetime.datetime.utcnow(),
                color=discord.Color.red())
            embed.set_author(name=ctx.me.display_name,
                             icon_url=ctx.me.avatar_url)
            embed.set_footer(text="{}".format(ctx.author.display_name),
                             icon_url=ctx.author.avatar_url)
            return await client.get_channel(1503853432992305172).send(embed=embed)(embed=embed)
            
    @commands.command(no_pm=True)
    @commands.is_nsfw()
    async def hentai(self, ctx):
        subreddit = reddit.subreddit('hentai')
        all_subs = []		
        top = subreddit.top(limit=5)
        for submission in top:
           all_subs.append(submission)			
        random_sub = random.choice(all_subs)		   

        name = random_sub.title		
        url = random_sub.url
        embed = AkagiEmbed(title=f"Random Hentai!",
                               description=f'[*{name}*]({url})',
                               timestamp=datetime.datetime.utcnow(),
                               color=discord.Color.red())
        embed.set_image(url=url)
        embed.set_author(name=ctx.me.display_name, icon_url=ctx.me.avatar_url)
        embed.set_footer(text="{}".format(ctx.author.display_name),
                         icon_url=ctx.author.avatar_url)
        await client.get_channel(1503853432992305172).send(embed=embed)(embed=embed)

    @hentai.error
    async def nsfw_error_handler(self, ctx, error):
        if isinstance(error, commands.NSFWChannelRequired):
            embed = AkagiEmbed(
                title=f"Error",
                description='*This command is Only for NSFW Channels!*',
                timestamp=datetime.datetime.utcnow(),
                color=discord.Color.red())
            embed.set_author(name=ctx.me.display_name,
                             icon_url=ctx.me.avatar_url)
            embed.set_footer(text="{}".format(ctx.author.display_name),
                             icon_url=ctx.author.avatar_url)
            return await client.get_channel(1503853432992305172).send(embed=embed)(embed=embed)

    async def on_message(self, message):
        print(message.content)


def setup(bot):
    bot.add_cog(NsfwCog(bot))
