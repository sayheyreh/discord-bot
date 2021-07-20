# pyright: reportMissingImports=false, reportUnusedVariable=warning, reportUntypedBaseClass=error
import discord;
import os
import requests;
import random;
from dotenv import load_dotenv

#for the environment variables, in this case, the key   
load_dotenv();

bot = discord.Client();

key = os.environ['API_KEY']
meme_api = 'https://meme-api.herokuapp.com/gimme/'

def randColour():
    return discord.Colour.from_rgb(random.randint(128, 255),random.randint(128, 255),random.randint(128, 255));

def getInfo(u):
            e=discord.Embed(title='User Info',colour=randColour())
            e.set_image(url=u.avatar_url);
            e.set_footer(text=u.id);
            e.add_field(name='username',value=(u.name+'#'+u.discriminator),inline=True);
            e.add_field(name='nickname',value=u.display_name,inline=True);
            e.add_field(name='created_on',value=u.created_at,inline=False);
            e.add_field(name='avatar',value=u.avatar_url,inline=False);
            return e;
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
        print(f'Said Hello in {message.channel} of {message.guild}');
        
    if message.content.startswith('$reddit'): 
        subreddit = message.content[7:].strip();
        res = requests.get(meme_api+subreddit);
        e=discord.Embed(title=res.json()['title'],url=res.json()['postLink'],color=randColour());
        e.set_image(url=res.json()['preview'][-1])
        e.set_footer(text=res.json()['subreddit']);
        await message.channel.send(embed=e);
        print(f"sent image from {res.json()['subreddit']} to {message.guild}, {message.channel}");

    if message.content.startswith('$info'):
        if len(message.mentions)==0:
            m = getInfo(message.author);
            await message.channel.send(embed=m);
            print(f'sent {message.author.id}\'s info in {message.guild}, {message.channel}');
        else:
            for user in message.mentions:
                m = getInfo(user);
                await message.channel.send(embed=m);
                print(f'sent {user.id}\'s info in {message.guild}, {message.channel}');
        
bot.run(key)