# pyright: reportMissingImports=false, reportUnusedVariable=warning, reportUntypedBaseClass=error
from logging import exception
import discord;
import os
from discord.utils import get
import requests;
import random;
from dotenv import load_dotenv

#for the environment variables, in this case, the key   
load_dotenv();

bot = discord.Client();

key = os.environ['API_KEY']
meme_api = 'https://meme-api.herokuapp.com/gimme/'
bored_api = 'http://www.boredapi.com/api/'
joke_api = 'https://v2.jokeapi.dev/joke/Any'
another_joke_api = 'https://official-joke-api.appspot.com/jokes/random'

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

@bot.event
async def on_ready():
    print('logged in as {0.user}'.format(bot));
    activity = discord.Game(name="testing",type=3)
    await bot.change_presence(status=discord.Status.online, activity=activity);

@bot.event
async def on_message(message):
    user=message.author;
    if message.author == bot.user:
        return;
#hello        
    if message.content.startswith('$hello'):
        await message.channel.send('hello ' + message.author.mention);
        print(f'Said Hello in {message.channel} of {message.guild}');
#reddit        
    elif message.content.startswith('$reddit'): 
        subreddit = message.content[7:].strip();
        res = requests.get(meme_api+subreddit);
        e=discord.Embed(title=res.json()['title'],url=res.json()['postLink'],color=randColour());
        e.set_image(url=res.json()['preview'][-1])
        e.set_footer(text=res.json()['subreddit']);
        await message.channel.send(embed=e);
        print(f"sent image from {res.json()['subreddit']} to {message.guild}, {message.channel}");
#info
    elif message.content.startswith('$info'):
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
    elif message.content.startswith('$bored'):
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
    elif message.content.startswith('$joke'):
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
    if message.content.startswith('$delete'):
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
bot.run(key)