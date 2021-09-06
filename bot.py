# pyright: reportMissingImports=false, reportUnusedVariable=warning, reportUntypedBaseClass=error
import asyncio
import discord;
import os
import re
from discord import reaction
from discord import colour
import requests;
import random;
from dotenv import load_dotenv
from logging import exception
from discord.utils import get
from bs4 import BeautifulSoup
#for the environment variables, in this case, the key   
load_dotenv();

bot = discord.Client();
key = os.environ['API_KEY']
meme_api = 'https://meme-api.herokuapp.com/gimme/'
bored_api = 'http://www.boredapi.com/api/'
joke_api = 'https://v2.jokeapi.dev/joke/Any'
another_joke_api = 'https://official-joke-api.appspot.com/jokes/random'
kanye_api = 'https://api.kanye.rest/'
gif_domain = 'https://y.yarn.co/'
gif_url = 'https://yarn.co/yarn-find'
anime_urls = ['https://wall.alphacoders.com/by_category.php?id=3&name=Anime+Wallpapers',\
    'https://wall.alphacoders.com/tag/satoru-gojo-wallpapers']


bad_people=[]

def scrape_query(query):
    link= requests.get(url=gif_url,params={'text':query})
    soup = BeautifulSoup(link.content,'html.parser')
    print(link.url)
    a = soup.find_all('div',attrs={'class':'pure-u-sm-1-2 pure-u-md-1-3 pure-u-lg-1-4 pure-u-xl-1-4'})
    if len(a)==0:
        return -1
    else:
        #20 choices
        weights=[]
        for i in range(0,len(a)):
            if i<4:
                weights.append(100)
            else:
                weights.append(10)
        a = random.choices(a,weights=weights,k=1)
        link_to_gif = gif_domain+a[0].a.get('href')[11:]+'_text.gif'
        title = a[0].find('div',attrs={'class':'transcript db bg-w fwb p05 tal'}).text
        movie = a[0].find('div',attrs={'class':'title ab fw5 p05 tal'}).text
        info = [link_to_gif,title,movie]
        return info

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
    e.set_author(name=(user.name+'#'+user.discriminator),icon_url=user.avatar_url)
    e.set_footer(text=res['type'])
    return e;
def checkRole(user,role):
    return role in user.roles;

async def music(message):
    await message.channel.send('dw')

@bot.event
async def on_ready():
    print('logged in as {0.user}'.format(bot));
    activity = discord.Game(name="type $help",type=3)
    await bot.change_presence(status=discord.Status.online, activity=activity)

@bot.event
async def on_message(message):
    user=message.author;
    if message.author == bot.user:
        return;
    splitted = message.content.split(' ')
#help
    if splitted[0] == '$help':
        e=discord.Embed(title='Commands',color=randColour())
        print(message.content[5:].strip())
        if message.content[5:].strip() == '2':
            e.title='Role Commands'
            e.add_field(name='$add', value='requires the `MANAGE_ROLES` permission,\nusage is `$add <mention> [role_name]`',inline=False)
            e.add_field(name='$remove', value='requires the `MANAGE_ROLES` permission\nusage is `$remove <mention> [role_name]`',inline=False)
            e.add_field(name='$delete',value='requires the `MANAGE_ROLES` permission\nusage is `$delete [role_name]`',inline=False)
        else:
            e.add_field(name='$hello',value='replies with hello',inline=False)
            e.add_field(name='$reddit', value='usage is `$reddit <subreddit>`\nor `$reddit` for default subs',inline=False)
            e.add_field(name='$info',value='usage is `$info` for self\nor `$info <mention1> <mention2>` as many people as you want',inline=False)
            e.add_field(name='$bored', value='after using the command, type any of the given options\n`education`,`recreational`,`social`\
                ,`diy`,`charity`,`cooking`,`relaxation`,`music`,`busywork`\nif you do not have a preference, type `no`')
            e.add_field(name='$joke', value='replied with a random joke',inline=False)
            e.add_field(name='$gif',value='replies with a gif from a movie\nusage is `$gif [quote | word]`',inline=False)
        await message.channel.send(embed=e)
#hello        
    if splitted[0] == '$hello':
        await message.channel.send('hello ' + message.author.mention);
        print(f'Said Hello in {message.channel} of {message.guild}');
#reddit        
    elif splitted[0] == '$reddit': 
        subreddit = message.content[7:].strip();
        res = requests.get(meme_api+subreddit);
        e=discord.Embed(title=res.json()['title'],url=res.json()['postLink'],color=randColour());
        e.set_image(url=res.json()['preview'][-1])
        e.set_footer(text=res.json()['subreddit']);
        await message.channel.send(embed=e)
        print(f"sent image from {res.json()['subreddit']} to {message.guild}, {message.channel}");
    elif splitted[0] == '$meme':
        subreddit = message.content[5:].strip();
        res = requests.get(meme_api+subreddit);
        e=discord.Embed(title=res.json()['title'],url=res.json()['postLink'],color=randColour());
        e.set_image(url=res.json()['preview'][-1])
        e.set_footer(text=res.json()['subreddit']);
        await message.channel.send(embed=e);
        print(f"sent image from {res.json()['subreddit']} to {message.guild}, {message.channel}");
#info
    elif splitted[0] == '$info':
        if len(message.mentions)==0:
            m = getInfo(message.author);
            await message.channel.send(embed=m);
            print(f'sent {message.author.id}\'s info in {message.guild}, {message.channel}');
        else:
            for user in message.mentions:
                m = getInfo(user);
                await message.channel.send(embed=m);
                print(f'sent {user.id}\'s info in {message.guild}, {message.channel}');
#bored
    elif splitted[0] == '$bored':
        def check(m):
            return m.content!=None and m.channel==message.channel and m.author==message.author;
        await message.channel.send('Any type you prefer?\n`education`,`recreational`,`social`,`diy`,`charity`,`cooking`,`relaxation`,`music`,`busywork`\nif you do not have a preference, type `no`');
        msg = await bot.wait_for('message',check=check)
        
        if msg.content.lower() in activityTypes:
            res=requests.get(bored_api+'activity?type='+msg.content).json();
            e=boredEmbed(user,res)
            await message.channel.send(embed=e);
            print(f'sent activity in {message.guild}, {message.channel}')
        elif msg.content.lower()=='no':
            res=requests.get(bored_api+'activity').json();
            e=boredEmbed(user,res)
            await message.channel.send(embed=e)
            print(f'sent activity in {message.guild}, {message.channel}')
        else:
            await message.channel.send('Sorry Invalid Input')
            print(f'{user.id} entered the wrong input')
#joke
    elif splitted[0] == '$joke':
        if random.randint(0,10) >=3:
            res=requests.get(joke_api).json()
            if res['type']=='twopart':
                e=discord.Embed(title=res['setup'],description=res['delivery'],color=randColour())
                e.set_author(name=(user.name+'#'+user.discriminator),icon_url=user.avatar_url);
                await message.channel.send(embed=e);
            else:
                e=discord.Embed(description=res['joke'])
                e.set_author(name=(user.name+'#'+user.discriminator),icon_url=user.avatar_url);
                await message.channel.send(embed=e);
        else:
            res = requests.get(another_joke_api).json();
            e=discord.Embed(title=res['setup'],description=res['punchline'],color=randColour())
            e.set_author(name=(user.name+'#'+user.discriminator),icon_url=user.avatar_url);
            await message.channel.send(embed=e);
#add
    elif message.content.startswith('$add') and not user.guild_permissions.manage_roles and not message.mentions[0].guild_permissions.administrator:
        print(f'{user} tried to use the `add` command')
        await message.channel.send('Insufficient Permissions');
    elif message.content.startswith('$add') and user.guild_permissions.manage_roles and not len(message.mentions)==1:
        await message.channel.send('mention one person');
    elif message.content.startswith('$add') and user.guild_permissions.manage_roles and len(message.mentions)==1:
        async def add_role(r,u):
            role_to_add = get(message.guild.roles, name=r);
            if checkRole(u,role_to_add):
                await message.channel.send('User already has the role');
            elif (user.top_role<=u.top_role):
                await message.channel.send('Insufficient Perms')
            else:
                await message.channel.send(f'Would you like to assign {role_to_add} to <@{u.id}>\n`yes` or `no`');
                def check(m2):
                    return m2.content!=None and m2.channel==message.channel and m2.author==message.author;
                m2 = await bot.wait_for('message',check=check);
                if m2.content.lower()=='yes':
                    await u.add_roles(role_to_add);
                    print(f'{user} added {r} to {u.id} in {message.guild}, {message.channel}')
                    await message.channel.send('Role was added')
                elif m2.content.lower()=='no':
                    await message.channel.send('Okay')
                else:
                    await message.channel.send('invalid input')
        msg = message.content.split(' ');
        u = message.mentions[0];
        r='';
        if msg[1] != f'<@!{u.id}>':
            print(msg[1],f'<@!{u.id}>')
            await message.channel.send('the correct usage for the command is\n`$add <mention> [role_name]`')
            print('Incorrect usage of command');
            return 
        for x in msg[2:]:
            r = r+' '+x;
        r = r.strip();
        if not get(message.guild.roles, name=r):
            await message.channel.send('Role doesn\'t exist, should I create it?\n `yes` or `no`')
            def check(m):
                return m.content!=None and m.channel==message.channel and m.author==message.author;
            m = await  bot.wait_for('message',check=check)
            if m.content.lower() =='yes':
                everyonePerms = get(message.guild.roles, name="@everyone")
                await message.guild.create_role(name=r, permissions=everyonePerms.permissions, colour=randColour() ,reason=f'{user.id} created {r}')
                print(f'role \'{r}\' created in {m.guild}, {m.channel}');
                await add_role(r,u)
            elif m.content.lower()=='no':
                await message.channel.send('Okay');
            else:
                await message.channel.send('invalid answer')
        else:
            await add_role(r,u)
#remove
    elif message.content.startswith('$remove') and not user.guild_permissions.manage_roles and not message.mentions[0].guild_permissions.administrator:
        print(f'{user} tried to use the `remove` command')
        await message.channel.send('Insufficient Permissions');
    elif message.content.startswith('$remove') and user.guild_permissions.manage_roles and not len(message.mentions)==1:
        await message.channel.send('mention one person');
    elif message.content.startswith('$remove') and user.guild_permissions.manage_roles and len(message.mentions)==1:
        msg = message.content.split(' ');
        u = message.mentions[0];
        r='';
        if msg[1] != f'<@!{u.id}>':
            print(msg[1],f'<@!{u.id}>')
            await message.channel.send('the correct usage for the command is\n`$remove <mention> [role_name]`')
            print('Incorrect usage of command');
            return 
        for x in msg[2:]:
            r = r+' '+x;
        r = r.strip();
        role_to_remove = get(message.guild.roles, name=r);
        if checkRole(u,role_to_remove):
            await u.remove_roles(role_to_remove);
            print('Role was removed');
            await message.channel.send('Role was removed');
        else:
            await message.channel.send('User doesn\'t have the role');
#delete
    if message.content.startswith('$delete') and not user.guild_permissions.manage_roles:
        await message.channel.send('You do not have the permission to delete roles')
    elif message.content.startswith('$delete') and user.guild_permissions.manage_roles:
        role = message.content[7:].strip();
        role_to_del = get(message.guild.roles, name=role);
        if role_to_del in message.guild.roles:
            try:
                await role_to_del.delete();
                await message.channel.send('Role deleted')
                print(f'{role_to_del.id} was deleted');
            except discord.Forbidden: 
                await message.channel.send('I do not have the permission to delete this role')
                print(f'Could not delete the role: {role_to_del}');
        else:
            await message.channel.send('Role does not exist');  
#kanye
    if 'kanye' in message.content.lower(): 
        res = requests.get(kanye_api).json();
        manual_quotes=['i like ur tiddies because they prove i can focus on two things at once',\
            'none of us would be here without cum']
        e=discord.Embed(title=res['quote'],color=randColour())
        e.set_footer(text='kanye')
        if random.randint(0,100)>=90:
            e.title=random.choice(manual_quotes)
        await message.channel.send(embed=e);
        print('sent kanye quote')
#gif
    if message.content.startswith('$gif'):
        q = message.content[4:].strip()
        gif_info = scrape_query(q)
        if gif_info==-1:
            await message.channel.send('No gifs were found')
        else:
            #0-url, 1-title, 2-movie 
            e = discord.Embed(title=gif_info[1],color=randColour())
            e.set_image(url=gif_info[0])
            e.set_footer(text=gif_info[2])
            await message.channel.send(embed=e)
            print(gif_info[0]) 
    if message.author.id in bad_people:
        if random.randint(0,1000) >=500:
            await message.add_reaction('🤮')
            print('reacted')
    if message.author.id == 224425803306369034 and splitted[0] == '$loser':
        if message.mentions==None:
            await message.channel.send('Mention someone')
        else:
            bad_people.append(message.mentions[0].id)
            await message.channel.send('added')
            print(bad_people)
    if message.author.id==224425803306369034 and splitted[0]=='$notloser':
        if len(message.mentions)==0:
            await  message.channel.send('Mention someone')
        else:
            bad_people.remove(message.mentions[0].id)
            await message.channel.send('removed')
            print(bad_people)
    if splitted[0] == 'checkList':
        await message.channel.send(str(bad_people))
    if splitted[0]=='$pp':
        def find_pp_size():
            pp='8'
            for i in range(0,random.randint(0,10)):
                pp+='='
            pp+='D'
            return pp
        async def send_pp(message,person):
            e=discord.Embed(title='pp machine',colour=randColour())
            if person.id==224425803306369034:
                e.add_field(name=f'{person}\' pp size', value='8=========================D')
            else:
                e.add_field(name=f'{person}\' pp size', value=find_pp_size())
            await message.channel.send(embed=e)
        if not message.mentions:
            print('test')
            await send_pp(message,message.author)
        else:
            print('test2')
            print(message.mentions)
            for i in message.mentions:
                await send_pp(message,i)
#Temp Command
    if splitted[0]=='$kaf':
        res = requests.get(random.choice(anime_urls))
        soup = BeautifulSoup(res.content,'html.parser')

        pictures = soup.find_all('picture')

        p = random.choice(pictures)

        e = p.find('img').get('src')
        await message.delete()
        await message.channel.send(e)
        print('sent kaf')

# hard coded for my server
# react_roles_id='875390612642336821'
# @bot.event
# async def on_raw_reaction_add(payload):
#     react = await bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
#     #get the role the emoji is linked to
#     emoji = payload.emoji
#     role_to_add = get(react.guild.roles, name=emoji)
#     user = react.author
#     await user.add_roles(role_to_add)
#     print('reaction was added',user)
# @bot.event
# async def on_raw_reaction_remove(payload):
#     react = await bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
#     #get the role the emoji is linked to
#     emoji = payload.emoji
#     role_to_remove = get(react.guild.roles, name=emoji)
    
#     print('reaction was removed',react.author)
bot.run(key)

#add event listener to see if people have reacted to the message, if they reacted then add the role for them