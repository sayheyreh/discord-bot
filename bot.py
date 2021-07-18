# pyright: reportMissingImports=false, reportUnusedVariable=warning, reportUntypedBaseClass=error
import discord;
import os

from discord import activity;
from dotenv import load_dotenv
#for the environment variables, in this case, the key
load_dotenv();

bot = discord.Client();

key = os.environ['API_KEY']

@bot.event
async def on_ready():
    print('logged in as {0.user}'.format(bot));
    activity = discord.Game(name="testing",type=3)
    await bot.change_presence(status=discord.Status.online, activity=activity);

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return;
    if message.content.startswith('$hello'):
        await message.channel.send('hello');
        print('Said Hello in', message.channel,' of ', message.guild);
    if message.content.startswith('$meme'): 
        await message.channel.send('I\'m still working on this');

bot.run(key)