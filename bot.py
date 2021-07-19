# pyright: reportMissingImports=false, reportUnusedVariable=warning, reportUntypedBaseClass=error
import discord;
import os
import requests;
from dotenv import load_dotenv

#for the environment variables, in this case, the key   
load_dotenv();

bot = discord.Client();

key = os.environ['API_KEY']
meme_api = 'https://meme-api.herokuapp.com/gimme/'


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
        await message.channel.send('hello ' + message.author.mention);
        print('Said Hello in', message.channel,' of ', message.guild);
        
    if message.content.startswith('$reddit'): 
        subreddit = message.content[7:].strip();
        res = requests.get(meme_api+subreddit);
        e=discord.Embed(title=res.json()['title'])
        e.set_image(url=res.json()['preview'][-1])
        e.set_footer(text=res.json()['subreddit'])
        await message.channel.send(embed=e);
        print('picture from',res.json()['subreddit'], 'sent in ', message.guild);
        
bot.run(key)