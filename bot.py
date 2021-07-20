# pyright: reportMissingImports=false, reportUnusedVariable=warning, reportUntypedBaseClass=error
import discord;
import os
from discord import channel
from discord import activity
import requests;
import random;
from dotenv import load_dotenv

#for the environment variables, in this case, the key   
load_dotenv();

bot = discord.Client();

key = os.environ['API_KEY']
meme_api = 'https://meme-api.herokuapp.com/gimme/'
joke_api =  'https://official-joke-api.appspot.com/jokes/random'
bored_api = 'http://www.boredapi.com/api/'

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
activityTypes = ['education','recreational','social','diy','charity','cooking','relaxation','music','busywork']

def boredEmbed(user,res):
    e=discord.Embed(title=res['activity'],color=randColour())
    e.set_author(name=(user.display_name+'#'+user.discriminator),icon_url=user.avatar_url)
    e.set_footer(text=res['type'])
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
    
    if message.content.startswith('$joke'):
        res = requests.get(joke_api);
        e=discord.Embed(title=res.json()['setup'],description=res.json()['punchline'],color=randColour())
        user=message.author;
        e.set_author(name=(user.display_name+'#'+user.discriminator),icon_url=user.avatar_url);
        await message.channel.send(embed=e);
    if message.content.startswith('$bored'):
        def check(m):
            return m.content!=None and m.channel==message.channel and m.author==message.author;
        await message.channel.send('Any type you prefer?\n`education`,`recreational`,`social`,`diy`,`charity`,`cooking`,`relaxation`,`music`,`busywork`\nif you do not have a preference, type `no`');
        msg = await bot.wait_for('message',check=check)
        user=message.author;
        if msg.content.lower() in activityTypes:
            res=requests.get(bored_api+'activity?type='+msg.content).json();
            e=boredEmbed(user,res)
            await message.channel.send(embed=e);
        elif msg.content.lower()=='no':
            res=requests.get(bored_api+'activity').json();
            e=boredEmbed(user,res)
            await message.channel.send(embed=e)
        else:
            await message.channel.send('Sorry Invalid Input')
bot.run(key)