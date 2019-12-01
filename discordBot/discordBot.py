import discord
from discord.ext import commands
import ast
import random
import redditVideoConverter

with open('discordBot.secret', 'r') as secretFile:
	secrets = ast.literal_eval(secretFile.read())
	botAuthToken = secrets['botAuthToken']

bot = commands.Bot(command_prefix='$')

@bot.event
async def on_ready():
    activity = discord.Activity(name='out for $info', type=discord.ActivityType.watching)
    await bot.change_presence(activity=activity)
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def info(ctx):
    await ctx.send('Currently I only have two fundtions:\n```$roll NdN - this rolls dice for you' \
        '\n$convert <redditvideolink> -this pulls the video from reddit and links it via streamable```')

@bot.command()
async def birthday(ctx, user: str):
    await ctx.send('```Happy Birthday to you\n' \
        'Happy Birthday to you\n' \
        'Happy Birthday dear ' + user + '\n' \
        'Happy Birthday to you```')

@bot.command()
async def roll(ctx, dice: str):
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN: https://wikipedia.org/wiki/Dice_notation')
        return

    dice = list(random.randint(1, limit) for r in range(rolls))
    try:
        await ctx.send(', '.join(str(die) for die in dice) + '\ntotal: ' + str(sum(dice)))
    except:
        await ctx.send("Too many dice results to show. How many dice do you need!?")

@bot.command()
async def convert(ctx, video: str):
    author = ctx.message.author
    try:
        origConfirmation = await ctx.send('Video uploading - waiting for streamable to process')
        videoLink = redditVideoConverter.videoConvert(video)
    except Exception:
        try:
            await ctx.send('Unable to convert your video {0.author.mention}. This could be because' \
                'it is not a v.reddit link or because streamable is experiencing issues.'.format(ctx.message))
            await origConfirmation.delete()
        except:
            pass
        return    

    await ctx.send(videoLink + ' was posted to discord by {0.author.mention}'.format(ctx.message))

    try:
        await origConfirmation.delete()
        await ctx.message.delete()
    except:
        pass

bot.run(botAuthToken)