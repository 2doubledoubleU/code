import discord
from discord.ext import commands
import ast
import random
import redditVideoConverter
import asyncio
import re
from datetime import datetime, date
import time
from pytz import utc
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
import sqlite3

with open('discordBot.secret', 'r') as secretFile:
	secrets = ast.literal_eval(secretFile.read())
	botAuthToken = secrets['botAuthToken']

scheduler = AsyncIOScheduler(jobstores={'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')})
scheduler.start()

async def sendMessage(guildId,channelId,message):
    guild = bot.get_guild(guildId)
    channel = guild.get_channel(channelId)
    await channel.send(message)

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
@commands.has_permissions(administrator=True)
async def delayedEcho(ctx, delay: str, channel: discord.TextChannel):
    isoIsh = re.search('^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$',delay)
    if isoIsh:
        a = datetime.strptime(isoIsh.group(0), "%Y-%m-%dT%H:%M:%S")
        seconds = (a-datetime.now()).total_seconds()
    else:
        await ctx.send('Please check your format ```$delay 2000-01-30T01:59:59 #general <message>```')
        return
    if seconds <= 0:
        await ctx.send('Time given is not in the future')
        return
    message = ctx.message.content.split(" ",3)[3]
    channelId = channel.id
    guildId = ctx.guild.id
    scheduler.add_job(sendMessage, 'date', run_date=delay, args=(guildId,channelId,message))
    await ctx.message.add_reaction('✅')

@bot.command()
@commands.has_permissions(administrator=True)
async def echo(ctx, channel: discord.TextChannel):
    message = ctx.message.content.split(" ",2)[2]
    await channel.send(message)
    await ctx.message.add_reaction('✅')

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