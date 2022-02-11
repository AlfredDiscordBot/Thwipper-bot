# IMPORTS
try:
    import discord
    from discord.utils import get
    from discord.ext import commands, tasks
    from links import *
    from responses import *
    from dotenv import load_dotenv
    import mysql.connector as ms
    import os
    import random
    import calendar
    import pytz
    import datetime
    import asyncio
    import regex
    import praw
    import pytube
    import imdb
    import requests
    import aiohttp
    import urllib.request
    import youtube_dl
    import wikipedia
    from googlesearch import search
    from cryptography.fernet import Fernet
    print("All modules and libraries imported...")
except ImportError as ie:
    print(ie)

# SETUP
prefixes = ["t!", "_", "|"]
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(
    command_prefix=[prefix for prefix in prefixes],
    intents=intents,
    case_insensitive=True,
)
color = discord.Color.lighter_gray()
bot.remove_command("help")
# Enviroment Variables
global auth
load_dotenv(".env")
auth = os.getenv("transformer_auth")
# SNIPE
deleted_messages = {}
# NUMBER OF REQUESTS
num = 0
# MUSIC
server_index = {}
FFMPEG_OPTS = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-vn",
}
ydl_op = {
    "format": "bestaudio/best",
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "128",
        }],}
# DEFAULT TIMEZONE
default_tz = "Asia/Kolkata"
# ENCRYPTER DECRYPTER
key = Fernet.generate_key()
cipher = Fernet(key)
# REDDIT
reddit = praw.Reddit(
    client_id=os.getenv("reddit_client_id"),
    client_secret=os.getenv("reddit_client_secret"),
    user_agent=os.getenv("reddit_user_agent"),
    username=os.getenv("reddit_username"),
    password=os.getenv("reddit_userpass"),
)
default_topic = {}
# HELP MENU
help_toggle = 0
# QUIPS
dialogue_list = []
# SQL
conn = ms.connect(
    user="root",
    host="localhost",
    password=os.getenv("sql_pass"),
    database="discord"
)
cursor = conn.cursor()

# ---------------------------------------------- NON ASYNC FUNCTIONS -----------------------------------------

def help_menu():
    global help_toggle

    embed_help_menu = discord.Embed(title="🕸𝗖𝗼𝗺𝗺𝗮𝗻𝗱 𝗠𝗲𝗻𝘂🕸", description="Prefixes: t! _ |", color=color)
    embed_help_menu.set_thumbnail(url=random.choice(url_thumbnails))
    embed_help_menu.set_footer(text="New Features Coming Soon 🛠")

    if help_toggle == 0 or help_toggle < 0:
        help_toggle = 0
        embed_help_menu.add_field(
            name="𝗦𝘁𝗮𝗻𝗱𝗮𝗿𝗱",
            value="`hello` to greet bot\n`help` to get this menu\n`quips` to get a famous dialogue or plot\n`@Thwipper` to get more info about thwipper",
            inline=False,
        )
        embed_help_menu.set_image(url=bot.user.avatar_url)
    if help_toggle == 1:
        embed_help_menu.add_field(
            name="𝗜𝗻𝘁𝗲𝗿𝗻𝗲𝘁",
            value="w `topic` for wikipedia\ng `topic` to google\nimdb `movie` to get movie details from IMDb\n reddit `topic` to get reddit memes",
            inline=False,
        )
        embed_help_menu.set_image(url=help_page1)
    if help_toggle == 2:
        embed_help_menu.add_field(
            name="𝗗𝗧𝗖",
            value="dt `timezone` to get IST date and time\ncal `year` `month` to get calendar\nNote: The default timezone is set as `Asia/Kolkata`",
            inline=False,
        )
        embed_help_menu.set_image(url=help_page2)
    if help_toggle == 3:
        embed_help_menu.add_field(
            name="𝗦𝗵𝗲𝗹𝗹𝘀",
            value="; `query` to use SQL Shell\npy `expression` for python shell\npydoc `function` to get information about that python function\nNote: The functions, when using `pydoc` command, will not be executed. Try without `()`.",
            inline=False,
        )
        embed_help_menu.set_image(url=help_page3)
    if help_toggle == 4:
        embed_help_menu.add_field(
            name="𝗘𝗻𝗰𝗿𝘆𝗽𝘁𝗲𝗿 𝗗𝗲𝗰𝗿𝘆𝗽𝘁𝗲𝗿",
            value="hush `en` `text` to encrypt message\nhush `dec` `text` to decrypt message\n",
            inline=False,
        )
        embed_help_menu.set_image(url=help_page4)
    if help_toggle == 5:
        embed_help_menu.add_field(
            name="𝗦𝗽𝗶𝗱𝗲𝗿-𝗣𝘂𝗻𝗸 𝗥𝗮𝗱𝗶𝗼™",
            value="🔉 `cn` to get the bot to join voice channel\n🔇 `dc` to remove bot from voice channel\n🎶 p `name` or `index` to play songs\n▶ `res` to resume a song\n⏸ `pause` to pause a song\n⏹ `st` to stop a song\n🔂 `rep` to repeat song\n⏭ `skip` to skip song\n⏮ `prev` for previous song\n*️⃣ `songinfo` to get current song\n🔠 `q` to display queue\n🔼 scroll queue`up`\n🔽scroll queue `down`\n✔ q `name` to add a song to the queue\n❌ rem `index` to remove song from queue\n💥 `cq` to clear queue",
            inline=False,
        )
        embed_help_menu.set_image(url=help_page5)
    if help_toggle == 6:
        embed_help_menu.add_field(
            name="𝗕𝗶𝗿𝘁𝗵𝗱𝗮𝘆𝘀",
            value="addbday `mention` `month` `day` to add a user's birthday from DB\n`bday` to get thwipper to wish the members\nrembday `mention` to remove a member's birthday.",
            inline=False,
        )
        embed_help_menu.set_image(url=help_page6)
    if help_toggle == 7 or help_toggle > 7:
        help_toggle = 7
        embed_help_menu.add_field(
            name="𝗨𝘁𝗶𝗹𝗶𝘁𝘆",
            value="`req` to get number of requests\n`web` to see deleted message\n`ping` to get bot's latency\n`serverinfo` to get server's information\npfp `mention` to get user's profile picture\n`setbit` to set quality of bitrate\n`polls` to see how to conduct a poll",
            inline=False
        )
        embed_help_menu.set_image(url=help_page7)

    return embed_help_menu


def time_converter(seconds):
    mins, secs = divmod(seconds, 60)
    hours, mins = divmod(mins, 60)

    if hours == 0: return "%02d mins %02d secs" % (mins, secs)
    if hours > 0: return "%d hrs %02d mins %02d secs" % (hours, mins, secs)


def youtube_download(ctx, url):
    if True:
        with youtube_dl.YoutubeDL(ydl_op) as ydl:
            URL = ydl.extract_info(url, download=False)["formats"][0]["url"]
    return URL


def requests_query():
    global cursor
    operation = "INSERT INTO requests(number)VALUES({})".format(num)
    cursor.execute(operation)


def number_of_requests():
    global num  # num = 0
    num += 1
    requests_query()

# ----------------------------------------- EVENTS --------------------------------------


@bot.event
async def on_ready():
    print("{0.user} is now online...\nHey Tamonud! How's it going?".format(bot))
    stop = 0

    # QUIPS
    global dialogue_list
    site = (
        requests.get("https://geektrippers.com/spiderman-quotes/")
        .content.decode()
        .replace("<br>", "\n")
        .replace("<strong>", " ")
        .replace("</strong>", " ")
        .replace("<em>", " ")
        .replace("</em>", " ")
        .replace("&#8217;", "'")
        .replace("&#8221;", '"\n\r')
        .replace("&#8230;", "...")
        .replace("&#8220;", '"')
        .replace("&nbsp;", " ")
        .replace("&#8211;", "-")
        .replace("&#8216;", "'")
        .replace("]", "]\n")
        .replace("[", "\n[")
    )

    for i in range(0, 1000):
        q = site.find(
            '<p class="has-background" style="background-color:#dedfe0">', stop) + len('<p class="has-background style="background-color:#dedfe0">')
        w = site.find("</p>", stop)
        stop = w + len("</p>")
        dialogues = ""
        if not site[q:w]: continue
        else:
            dialogues = site[q:w]
            dialogue_list += [dialogues]

    # STATUSES
    @tasks.loop(minutes=10)
    async def multiple_statuses():
        while True:
            for status in status_list:
                await asyncio.sleep(300)
                await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=status))
    multiple_statuses.start()

    # UPDATION
    @tasks.loop(seconds=5.0)
    async def updation():
        # REQUESTS UPDATE
        global cursor
        global num
        op = "SELECT MAX(number) FROM requests"
        cursor.execute(op)
        req1 = cursor.fetchall()
        req2 = str(req1).replace("[(", " ").replace(",)]", " ")
        num = int(req2)
        conn.commit()
    updation.start()


async def transformer(api, header, json):
    async with aiohttp.ClientSession() as session:
        async with session.post(api, headers=header, json=json) as resp:
            return await resp.json()

@bot.event
async def on_message(message):
    headeras = {"Authorization": auth}
    API_URL = ("https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill")

    if message.content.lower().startswith("thwip"):
        past_respose = []
        generated = []
        input_text = message.content.lower().replace("thwip", "")
        payload = {
            "inputs": {
                "past_user_inputs": past_respose,
                "generated_responses": generated,
                "text": input_text,
            },}
        output = await transformer(API_URL, header=headeras, json=payload)
        if len(past_respose) < 100:
            past_respose.append(input_text)
            generated.append(output["generated_text"])
        else:
            past_respose.pop(0)
            generated.pop(0)
            past_respose.append(input_text)
            generated.append(output["generated_text"])
        await message.reply(output["generated_text"])

    if f"<@!{bot.user.id}>" == message.content:
        number_of_requests()
        embed = discord.Embed(
            title="About",
            description=f"Hi {message.author.name}!\nI am Thwipper. I aim to be a multipurpose bot. From music to memes, I have it all 😎",
            color=color,
        )
        embed.add_field(
            name="Made By", value="[Tamonud](https://github.com/spidey711)", inline=True
        )
        embed.add_field(
            name="Source Code",
            value="[Thwipper](https://github.com/spidey711/Thwipper-bot)",
            inline=True,
        )
        embed.set_thumbnail(url=bot.user.avatar_url)
        # embed.set_image(url="https://txt.1001fonts.net/img/txt/dHRmLjcyLjAwMDAwMC5WRWhYU1ZCUVJWSSwuMA,,/lazenby-computer.liquid.png")
        embed.set_footer(
            text="Type _help for command menu",
            icon_url=message.author.avatar_url
        )
        await message.reply(embed=embed)
    else: await bot.process_commands(message)

async def genpost(api, header, json):
    async with aiohttp.ClientSession() as session:
        async with session.post(api, headers=header, json=json) as resp:
            return await resp.json()

@bot.command()
async def gen(ctx, *, text):
    API_URL2 = "https://api-inference.huggingface.co/models/EleutherAI/gpt-neo-2.7B"
    header2 = {"Authorization": auth}
    payload2 = {
        "inputs": text,
        "parameters": {"max_new_tokens": 250, "return_full_text": True},
    }
    output = await genpost(API_URL2, header2, payload2)
    await ctx.send(
        embed=discord.Embed(
            title="Generated text", 
            description=output[0]["generated_text"], 
            color=color
        ))


@bot.event
async def on_message_delete(message):
    if not message.channel.id in list(deleted_messages.keys()): deleted_messages[message.channel.id] = []
    if len(message.embeds) <= 0: deleted_messages[message.channel.id].append((str(message.author.id), message.content))
    else: deleted_messages[message.channel.id].append((str(message.author.id), message.embeds[0], True))

@bot.event
async def on_reaction_add(reaction, user):
    number_of_requests()

    if not user.bot:
        if reaction.emoji == "🖱":
            if str(user) != str(bot.user) and reaction.message.author == bot.user:
                await reaction.remove(user)
            try:
                sub = reddit.subreddit(default_topic[str(reaction.message.guild.id)]).random()
                embed = discord.Embed(description=f"**Caption:\n**{sub.title}", color=color)
                embed.set_author(name=f"Post by: {sub.author}", icon_url=url_reddit_author)
                embed.set_thumbnail(url=url_reddit_thumbnail)
                embed.set_image(url=sub.url)
                embed.set_footer(text=f"🔺: {sub.ups}   🔻: {sub.downs}   💬: {sub.num_comments}")
                await reaction.message.edit(embed=embed)
            except Exception:
                embed = discord.Embed(description="Default topic is not set", color=color)
                embed.set_author(name="Uh oh...", icon_url=url_reddit_author)
                await reaction.message.edit(embed=embed)

        global help_toggle
        if reaction.emoji == "➡":
            help_toggle += 1
            if str(user) != str(bot.user) and reaction.message.author == bot.user:
                await reaction.remove(user)
                await reaction.message.edit(embed=help_menu())

        if reaction.emoji == "⬅":
            help_toggle -= 1
            if str(user) != str(bot.user) and reaction.message.author == bot.user:
                await reaction.remove(user)
                await reaction.message.edit(embed=help_menu())

        if reaction.emoji == "🕸":
            if str(user) != str(bot.user) and reaction.message.author == bot.user:
                await reaction.remove(user)
                embed = discord.Embed(title="🕸Mutual Guilds🕸",
                                    description="\n".join([servers.name for servers in user.mutual_guilds]),
                                    color=color)
                embed.set_thumbnail(url=random.choice(url_thumbnails))
                embed.set_footer(text="New Features Coming Soon 🛠")
                await reaction.message.edit(embed=embed)

        # MUSIC PLAYER
        voice = discord.utils.get(bot.voice_clients, guild=reaction.message.guild)
        voice_client = reaction.message.guild.voice_client
        playing = reaction.message.guild.voice_client.is_playing()
        pause = reaction.message.guild.voice_client.is_paused()

        # SERVER QUEUE
        operation_view = f"SELECT * FROM music_queue WHERE server={str(reaction.message.guild.id)}"
        cursor.execute(operation_view)
        server_queue = cursor.fetchall()
        members_in_vc = [str(names) for names in reaction.message.guild.voice_client.channel.members]
        string = ""

        if reaction.emoji == "🔼":
            if str(user) != str(bot.user) and reaction.message.author == bot.user: 
                await reaction.remove(user)
                index = server_index[str(reaction.message.guild.id)]
                try:
                    index -= 10
                    for song in server_queue[index: index + 20]:
                        string += (str(index) + ") " + f"{song[0]}\n".replace(" - YouTube", " "))
                        index += 1
                    embed = discord.Embed(description=string, color=color)
                    embed.set_author(name=f"{reaction.message.guild.name}'s Playlist", icon_url=url_author_music)
                    embed.set_thumbnail(url=random.choice(url_thumbnail_music))
                    embed.set_footer(text=f"Number Of Songs: {len(server_queue)}")
                    await reaction.message.edit(embed=embed)

                except KeyError:
                    embed = discord.Embed(description=random.choice(default_index), color=color)
                    embed.set_author(name="Spider-Punk Radio™", icon_url=url_author_music)
                    await reaction.message.edit(embed=embed)

        if reaction.emoji == "🔽":
            if str(user) != str(bot.user) and reaction.message.author == bot.user:
                await reaction.remove(user)
                index = server_index[str(reaction.message.guild.id)]
                try:
                    for song in server_queue[index: index + 20]:
                        string += (str(index) + ") " + f"{song[0]}\n".replace(" - YouTube", " "))
                        index += 1
                    embed = discord.Embed(description=string, color=color)
                    embed.set_author(name=f"{reaction.message.guild.name}'s Playlist",icon_url=url_author_music,)
                    embed.set_thumbnail(url=random.choice(url_thumbnail_music))
                    embed.set_footer(text=f"Number Of Songs: {len(server_queue)}")
                    index += 10
                    await reaction.message.edit(embed=embed)
                except KeyError:
                        embed = discord.Embed( description=random.choice(default_index), color=color)
                        embed.set_author(name="Spider-Punk Radio™", icon_url=url_author_music)
                        await reaction.message.edit(embed=embed)
                        
        if reaction.emoji == "🔠":
            if str(user) != str(bot.user) and reaction.message.author == bot.user:
                await reaction.remove(user)
                try:
                    index = server_index[str(reaction.message.guild.id)] - 10
                    if server_index[str(reaction.message.guild.id)] > 10:
                        for song in server_queue[index: index + 20]:
                            string += ( str(index) + ") " + f"{song[0]}\n".replace(" - YouTube", " "))
                            index += 1
                        embed = discord.Embed(description=string, color=color)
                        embed.set_author(name=f"{reaction.message.guild.name}'s Playlist", icon_url=url_author_music)
                        embed.set_thumbnail(url=random.choice(url_thumbnail_music))
                        embed.set_footer(text=f"Number Of Songs: {len(server_queue)}")
                        await reaction.message.edit(embed=embed)
                    else:
                        index = server_index[str(reaction.message.guild.id)]
                        for song in server_queue[index: index + 20]:
                            string += (str(index) + ") " + f"{song[0]}\n".replace(" - YouTube", " "))
                            index += 1
                        embed = discord.Embed(description=string, color=color)
                        embed.set_author(name=f"{reaction.message.guild.name}'s Playlist", icon_url=url_author_music)
                        embed.set_thumbnail(url=random.choice(url_thumbnail_music))
                        embed.set_footer(text=f"Number Of Songs: {len(server_queue)}")
                        await reaction.message.edit(embed=embed)

                except KeyError:
                    embed = discord.Embed(description=random.choice(default_index), color=color )
                    embed.set_author(name="Spider-Punk Radio™", icon_url=url_author_music)
                    await reaction.message.edit(embed=embed)

        if reaction.emoji == "▶":
            if str(user) != str(bot.user) and reaction.message.author == bot.user:
                await reaction.remove(user)
                if members_in_vc.count(str(user)) > 0:
                    try:
                        if server_index[str(reaction.message.guild.id)] is not None:
                            if pause == True:
                                voice_client.resume()
                                embed = discord.Embed(description="Song has resumed playing 🎸", color=color)
                                embed.set_author(name="Spider-Punk Radio™", icon_url=url_author_music)
                                embed.set_footer(text=f"Voice Channel Bitrate: {reaction.message.guild.voice_client.channel.bitrate/1000} kbps")
                                await reaction.message.edit(embed=embed)
                            else:
                                if playing == True:
                                    embed = discord.Embed(description="Song is not paused 🤔", color=color)
                                    embed.set_author(name="Spider-Punk Radio™", icon_url=url_author_music)
                                    embed.set_footer(text=f"Voice Channel Bitrate: {reaction.message.guild.voice_client.channel.bitrate/1000} kbps")
                                    await reaction.message.edit(embed=embed)
                                else:
                                    embed = discord.Embed(description="Nothing is playing right now ❗", color=color)
                                    embed.set_author(name="Spider-Punk Radio™", icon_url=url_author_music)
                                    embed.set_footer(text=f"Voice Channel Bitrate: {reaction.message.guild.voice_client.channel.bitrate/1000} kbps")
                                    await reaction.message.edit(embed=embed)
                        else:
                            if playing != True:
                                voice_client.resume()
                                embed = discord.Embed(description="Song has resumed playing ▶", color=color)
                                embed.set_author(name="Spider-Punk Radio™", icon_url=url_author_music)
                                embed.set_footer(text=f"Voice Channel Bitrate: {reaction.message.guild.voice_client.channel.bitrate/1000} kbps")
                                await reaction.message.edit(embed=embed)
                            else:
                                embed = discord.Embed(description="Song is already playing 🎸", color=color)
                                embed.set_author(name="Spider-Punk Radio™", icon_url=url_author_music)
                                embed.set_footer(text=f"Voice Channel Bitrate: {reaction.message.guild.voice_client.channel.bitrate/1000} kbps")
                                await reaction.message.edit(embed=embed)
                    except Exception as e:
                        embed = discord.Embed(description=str(e), color=color)
                        embed.set_author(name="Error", icon_url=url_author_music)
                        await reaction.message.edit(embed=embed)
                else:
                    users = set()
                    message = await reaction.message.channel.fetch_message(reaction.message)
                    for reaction in message.reactions:
                        async for user in reaction.users():
                            users.add(user)
                    str1 = ",".join([str(users)])
                    pre_li = str1.replace("{", "").replace("}", "")
                    li = list(pre_li.split(","))  # li[-1]
                    embed = discord.Embed(description=f"Connect to the voice channel first 🔊", color=color)
                    embed.set_author(name="Spider-Punk Radio™", icon_url=url_author_music)
                    await reaction.message.edit(embed=embed)

        if reaction.emoji == "⏸":
            if str(user) != str(bot.user) and reaction.message.author == bot.user:
                await reaction.remove(user)
                if members_in_vc.count(str(user)) > 0:
                    try:
                        if playing == True:
                            voice_client.pause()
                            embed = discord.Embed(description="Song is paused ⏸", color=color)
                            embed.set_author(name="Spider-Punk Radio™", icon_url=url_author_music)
                            embed.set_footer(text=f"Voice Channel Bitrate: {reaction.message.guild.voice_client.channel.bitrate/1000} kbps")
                            await reaction.message.edit(embed=embed)
                        else:
                            if pause == True:
                                embed = discord.Embed(description="Song is already paused ⏸", color=color)
                                embed.set_author(name="Spider-Punk Radio™", icon_url=url_author_music)
                                embed.set_footer(text=f"Voice Channel Bitrate: {reaction.message.guild.voice_client.channel.bitrate/1000} kbps")
                                await reaction.message.edit(embed=embed)
                            else:
                                embed = discord.Embed(description="No song playing currently ❗", color=color)
                                embed.set_author(name="Spider-Punk Radio™", icon_url=url_author_music)
                                embed.set_footer(text=f"Voice Channel Bitrate: {reaction.message.guild.voice_client.channel.bitrate/1000} kbps")
                                await reaction.message.edit(embed=embed)
                    except Exception as e:
                        embed = discord.Embed(description=str(e), color=color)
                        embed.set_author(name="Error", icon_url=url_author_music)
                        await reaction.message.edit(embed=embed)
                else:
                    embed = discord.Embed(description=f"Connect to the voice channel first 🔊", color=color)
                    embed.set_author(name="Spider-Punk Radio™", icon_url=url_author_music)
                    await reaction.message.edit(embed=embed)

        if reaction.emoji == "⏮":
            if str(user) != str(bot.user) and reaction.message.author == bot.user:
                await reaction.remove(user)
                server_index[str(reaction.message.guild.id)] -= 1
                if members_in_vc.count(str(user)) > 0:
                    try:
                        URL_queue = youtube_download(reaction.message, server_queue[server_index[str(reaction.message.guild.id)]][1])
                        if playing != True:
                            embed = discord.Embed(description="**Song: **{a}\n**Queue Index: **{b}".format(a=server_queue[server_index[str(reaction.message.guild.id)]][0], b=server_index[str(reaction.message.guild.id)],).replace(" - YouTube", " "), color=color,)
                            embed.set_author(name="Now playing", icon_url=url_author_music)
                            embed.set_thumbnail(url=pytube.YouTube(url=server_queue[server_index[str(reaction.message.guild.id)]][1]).thumbnail_url)
                            embed.add_field(name="Uploader", value=pytube.YouTube(url=server_queue[server_index[str(reaction.message.guild.id)]][1]).author, inline=True)
                            embed.add_field(name="Duration", value=time_converter(pytube.YouTube(url=server_queue[server_index[str(reaction.message.guild.id)]][1]).length), inline=True)
                            embed.set_footer(text=f"Voice Channel Bitrate: {reaction.message.guild.voice_client.channel.bitrate/1000} kbps")
                            await reaction.message.edit(embed=embed)
                            voice.play(discord.FFmpegPCMAudio(URL_queue, **FFMPEG_OPTS))
                        else:
                            voice.stop()
                            embed = discord.Embed(description="**Song: **{a}\n**Queue Index: **{b}".format(a=server_queue[server_index[str(reaction.message.guild.id)]][0], b=server_index[str(reaction.message.guild.id)]).replace(" - YouTube", " "), color=color)
                            embed.set_author(name="Now playing", icon_url=url_author_music)
                            embed.set_thumbnail(url=pytube.YouTube(url=server_queue[server_index[str(reaction.message.guild.id)]][1]).thumbnail_url)
                            embed.add_field(name="Uploader", value=pytube.YouTube(url=server_queue[server_index[str(reaction.message.guild.id)]][1]).author, inline=True)
                            embed.add_field(name="Duration", value=time_converter(pytube.YouTube(url=server_queue[server_index[str(reaction.message.guild.id)]][1]).length), inline=True)
                            embed.set_footer(text=f"Voice Channel Bitrate: {reaction.message.guild.voice_client.channel.bitrate/1000} kbps")
                            await reaction.message.edit(embed=embed)
                            voice.play(discord.FFmpegPCMAudio(URL_queue, **FFMPEG_OPTS))
                    except IndexError:
                        embed = discord.Embed(description="Looks like there is no song at this index", color=color)
                        embed.set_author(name="Oops...", icon_url=url_author_music)
                        await reaction.message.edit(embed=embed)
                else:
                    embed = discord.Embed(description=f"Connect to the voice channel first 🔊", color=color)
                    embed.set_author(name="Spider-Punk Radio™", icon_url=url_author_music)
                    await reaction.message.edit(embed=embed)

        if reaction.emoji == "⏭":
            if str(user) != str(bot.user) and reaction.message.author == bot.user:
                await reaction.remove(user)
                server_index[str(reaction.message.guild.id)] += 1
                if members_in_vc.count(str(user)) > 0:
                    try:
                        URL_queue = youtube_download(reaction.message, server_queue[server_index[str(reaction.message.guild.id)]][1])
                        if playing != True:
                            embed = discord.Embed(description="**Song: **{a}\n**Queue Index: **{b}".format(a=server_queue[server_index[str(reaction.message.guild.id)]][0], b=server_index[str(reaction.message.guild.id)]).replace(" - YouTube", " "), color=color,)
                            embed.set_author(name="Now Playing", icon_url=url_author_music)
                            embed.set_thumbnail(url=pytube.YouTube(url=server_queue[server_index[str(reaction.message.guild.id)]][1]).thumbnail_url)
                            embed.add_field(name="Uploader", value=pytube.YouTube(url=server_queue[server_index[str(reaction.message.guild.id)]][1]).author, inline=True)
                            embed.add_field(name="Duration", value=time_converter(pytube.YouTube(url=server_queue[server_index[str(reaction.message.guild.id)]][1]).length), inline=True)
                            embed.set_footer(text=f"Voice Channel Bitrate: {reaction.message.guild.voice_client.channel.bitrate/1000} kbps")
                            await reaction.message.edit(embed=embed)
                            voice.play(discord.FFmpegPCMAudio(URL_queue, **FFMPEG_OPTS))
                        else:
                            voice.stop()
                            embed = discord.Embed(description="**Song: **{a}\n**Queue Index: **{b}".format(a=server_queue[server_index[str(reaction.message.guild.id)]][0], b=server_index[str(reaction.message.guild.id)]).replace(" - YouTube", " "), color=color)
                            embed.set_author(name="Now Playing", icon_url=url_author_music)
                            embed.set_thumbnail(url=pytube.YouTube(url=server_queue[server_index[str(reaction.message.guild.id)]][1]).thumbnail_url)
                            embed.add_field(name="Uploader", value=pytube.YouTube(url=server_queue[server_index[str(reaction.message.guild.id)]][1]).author, inline=True)
                            embed.add_field(name="Duration", value=time_converter(pytube.YouTube(url=server_queue[server_index[str(reaction.message.guild.id)]][1]).length), inline=True)
                            embed.set_footer(text=f"Voice Channel Bitrate: {reaction.message.guild.voice_client.channel.bitrate/1000} kbps")
                            await reaction.message.edit(embed=embed)
                            voice.play(discord.FFmpegPCMAudio(URL_queue, **FFMPEG_OPTS))
                    except IndexError:
                        embed = discord.Embed(description="Looks like there is no song at this index", color=color)
                        embed.set_author(name="Oops...", icon_url=url_author_music)
                        await reaction.message.edit(embed=embed)
                else:
                    embed = discord.Embed(description=f"Connect to the voice channel first 🔊", color=color)
                    embed.set_author(name="Spider-Punk Radio™", icon_url=url_author_music)
                    await reaction.message.edit(embed=embed)

        if reaction.emoji == "⏹":

            if str(user) != str(bot.user) and reaction.message.author == bot.user:
                await reaction.remove(user)

                if members_in_vc.count(str(user)) > 0:

                    try:

                        if playing == True or pause == True:
                            voice_client.stop()
                            embed = discord.Embed(
                                description="Song has been stopped ⏹", color=color
                            )
                            embed.set_author(
                                name="Spider-Punk Radio™", icon_url=url_author_music
                            )
                            embed.set_footer(
                                text="Voice Channel Bitrate: {} kbps".format(
                                    reaction.message.guild.voice_client.channel.bitrate
                                    / 1000
                                )
                            )
                            await reaction.message.edit(embed=embed)

                        else:
                            embed = discord.Embed(
                                description="Nothing is playing at the moment ❗",
                                color=color,
                            )
                            embed.set_author(
                                name="Spider-Punk Radio™", icon_url=url_author_music
                            )
                            embed.set_footer(
                                text="Voice Channel Bitrate: {} kbps".format(
                                    reaction.message.guild.voice_client.channel.bitrate
                                    / 1000
                                )
                            )
                            await reaction.message.edit(embed=embed)

                    except Exception as e:
                        embed = discord.Embed(description=str(e), color=color)
                        embed.set_author(
                            name="Error", icon_url=url_author_music)
                        await reaction.message.edit(embed=embed)

                else:
                    embed = discord.Embed(
                        description=f"Connect to the voice channel first 🔊", color=color
                    )
                    embed.set_author(
                        name="Spider-Punk Radio™", icon_url=url_author_music
                    )
                    await reaction.message.edit(embed=embed)

        if reaction.emoji == "*️⃣":

            if str(user) != str(bot.user) and reaction.message.author == bot.user:
                await reaction.remove(user)

                if len(server_queue) <= 0:
                    embed = discord.Embed(
                        description=random.choice(empty_queue), color=color
                    )
                    embed.set_author(
                        name="Uh oh...", icon_url=url_author_music)
                    await reaction.message.edit(embed=embed)

                else:

                    try:
                        try:
                            embed = discord.Embed(
                                description="**Song: **{a}\n**Index: **{b}\n**Views: **{c}\n**Description: **\n{d}".format(
                                    a=server_queue[
                                        server_index[str(
                                            reaction.message.guild.id)]
                                    ][0],
                                    b=server_index[str(reaction.message.guild.id)],
                                    c=pytube.YouTube(
                                        url=server_queue[
                                            server_index[str(
                                                reaction.message.guild.id)]
                                        ][1]
                                    ).views,
                                    d=pytube.YouTube(
                                        url=server_queue[
                                            server_index[str(
                                                reaction.message.guild.id)]
                                        ][1]
                                    ).description,
                                ),
                                color=color,
                            )
                            embed.set_author(
                                name="Currently Playing",
                                url=server_queue[
                                    server_index[str(reaction.message.guild.id)]
                                ][1],
                                icon_url=url_author_music,
                            )
                            embed.set_footer(
                                text="Voice Channel Bitrate: {} kbps".format(
                                    reaction.message.guild.voice_client.channel.bitrate
                                    / 1000
                                )
                            )
                            embed.set_thumbnail(
                                url=pytube.YouTube(
                                    url=server_queue[
                                        server_index[str(
                                            reaction.message.guild.id)]
                                    ][1]
                                ).thumbnail_url
                            )
                            await reaction.message.edit(embed=embed)
                        except discord.errors.HTTPException:
                            embed = discord.Embed(
                                description="**Song: **{a}\n**Index: **{b}\n**Views: **{c}\n**Description: **\n{d}".format(
                                    a=server_queue[
                                        server_index[str(
                                            reaction.message.guild.id)]
                                    ][0],
                                    b=server_index[str(reaction.message.guild.id)],
                                    c=pytube.YouTube(
                                        url=server_queue[
                                            server_index[str(
                                                reaction.message.guild.id)]
                                        ][1]
                                    ).views,
                                    d=random.choice(description_embed_errors),
                                ),
                                color=color,
                            )
                            embed.set_author(
                                name="Currently Playing",
                                url=server_queue[
                                    server_index[str(reaction.message.guild.id)]
                                ][1],
                                icon_url=url_author_music,
                            )
                            embed.set_footer(
                                text="Voice Channel Bitrate: {} kbps".format(
                                    reaction.message.guild.voice_client.channel.bitrate
                                    / 1000
                                )
                            )
                            embed.set_thumbnail(
                                url=pytube.YouTube(
                                    url=server_queue[
                                        server_index[str(
                                            reaction.message.guild.id)]
                                    ][1]
                                ).thumbnail_url
                            )
                            await reaction.message.edit(embed=embed)
                            
                    except KeyError:
                        embed = discord.Embed(
                            description="Looks like you weren't playing anything before this so there is no current song. Play song from queue to set a current song",
                            color=color,
                        )
                        embed.set_author(
                            name="Uh oh...", icon_url=url_author_music)
                        await reaction.message.edit(embed=embed)

        if reaction.emoji == "🔂":

            if str(user) != str(bot.user) and reaction.message.author == bot.user:
                await reaction.remove(user)

                if members_in_vc.count(str(user)) > 0:

                    try:
                        URL_queue = youtube_download(
                            reaction.message,
                            server_queue[server_index[str(reaction.message.guild.id)]][
                                1
                            ],
                        )

                        if reaction.message.guild.voice_client.is_playing() != True:
                            embed = discord.Embed(
                                description="**Song: **{}".format(
                                    server_queue[
                                        server_index[str(
                                            reaction.message.guild.id)]
                                    ][0]
                                ).replace(" - YouTube", " "),
                                color=color,
                            )
                            embed.set_author(
                                name="Repeating Song", icon_url=url_author_music
                            )
                            embed.set_thumbnail(
                                url=pytube.YouTube(
                                    url=server_queue[
                                        server_index[str(
                                            reaction.message.guild.id)]
                                    ][1]
                                ).thumbnail_url
                            )
                            embed.add_field(
                                name="Uploader",
                                value=pytube.YouTube(
                                    url=server_queue[
                                        server_index[str(
                                            reaction.message.guild.id)]
                                    ][1]
                                ).author,
                                inline=True,
                            )
                            embed.add_field(
                                name="Duration",
                                value=time_converter(
                                    pytube.YouTube(
                                        url=server_queue[
                                            server_index[str(
                                                reaction.message.guild.id)]
                                        ][1]
                                    ).length
                                ),
                                inline=True,
                            )
                            embed.set_footer(
                                text="Voice Channel Bitrate: {} kbps".format(
                                    reaction.message.guild.voice_client.channel.bitrate
                                    / 1000
                                )
                            )
                            await reaction.message.edit(embed=embed)
                            voice.play(discord.FFmpegPCMAudio(
                                URL_queue, **FFMPEG_OPTS))

                        else:
                            voice.stop()
                            embed = discord.Embed(
                                description="**Song: **{}".format(
                                    server_queue[
                                        server_index[str(
                                            reaction.message.guild.id)]
                                    ][0]
                                ).replace(" - YouTube", " "),
                                color=color,
                            )
                            embed.set_author(
                                name="Repeating Song", icon_url=url_author_music
                            )
                            embed.set_thumbnail(
                                url=pytube.YouTube(
                                    url=server_queue[
                                        server_index[str(
                                            reaction.message.guild.id)]
                                    ][1]
                                ).thumbnail_url
                            )
                            embed.add_field(
                                name="Uploader",
                                value=pytube.YouTube(
                                    url=server_queue[
                                        server_index[str(
                                            reaction.message.guild.id)]
                                    ][1]
                                ).author,
                                inline=True,
                            )
                            embed.add_field(
                                name="Duration",
                                value=time_converter(
                                    pytube.YouTube(
                                        url=server_queue[
                                            server_index[str(
                                                reaction.message.guild.id)]
                                        ][1]
                                    ).length
                                ),
                                inline=True,
                            )
                            embed.set_footer(
                                text="Voice Channel Bitrate: {} kbps".format(
                                    reaction.message.guild.voice_client.channel.bitrate
                                    / 1000
                                )
                            )
                            await reaction.message.edit(embed=embed)
                            voice.play(discord.FFmpegPCMAudio(
                                URL_queue, **FFMPEG_OPTS))

                    except Exception as e:
                        embed = discord.Embed(description=str(e), color=color)
                        embed.set_author(
                            name="Error", icon_url=url_author_music)
                        await reaction.message.edit(embed=embed)

                else:
                    embed = discord.Embed(
                        description=f"Connect to the voice channel first 🔊", color=color
                    )
                    embed.set_author(
                        name="Spider-Punk Radio™", icon_url=url_author_music
                    )
                    await reaction.message.edit(embed=embed)

        if reaction.emoji == "🔀":

            if str(user) != str(bot.user) and reaction.message.author == bot.user:
                await reaction.remove(user)

                if members_in_vc.count(str(user)) > 0:
                    random_song = random.choice(server_queue)
                    queue_index = server_index[str(reaction.message.guild.id)]

                    for index in range(len(server_queue)):

                        if random_song == server_queue[index]:
                            queue_index = int(index)

                    server_index[str(reaction.message.guild.id)] = queue_index
                    URL_shuffle = youtube_download(
                        reaction.message, random_song[1])

                    if reaction.message.guild.voice_client.is_playing() == False:
                        embed = discord.Embed(
                            description=f"**Song: **{random_song[0]}\n**Queue Index: **{queue_index}".replace(
                                " - YouTube", " "
                            ),
                            color=color,
                        )
                        embed.set_author(name="Shuffle Play",
                                         icon_url=url_author_music)
                        embed.set_thumbnail(
                            url=pytube.YouTube(
                                url=random_song[1]).thumbnail_url
                        )
                        embed.add_field(
                            name="Uploader",
                            value=pytube.YouTube(url=random_song[1]).author,
                            inline=True,
                        )
                        embed.add_field(
                            name="Duration",
                            value=time_converter(
                                pytube.YouTube(url=random_song[1]).length
                            ),
                            inline=True,
                        )
                        embed.set_footer(
                            text=f"Voice Channel Bitrate: {reaction.message.guild.voice_client.channel.bitrate/1000} kbps"
                        )
                        await reaction.message.edit(embed=embed)
                        voice.play(discord.FFmpegPCMAudio(
                            URL_shuffle, **FFMPEG_OPTS))

                    else:
                        voice.stop()
                        embed = discord.Embed(
                            description=f"**Song: **{random_song[0]}\n**Queue Index: **{queue_index}".replace(
                                " - YouTube", " "
                            ),
                            color=color,
                        )
                        embed.set_author(name="Shuffle Play",
                                         icon_url=url_author_music)
                        embed.set_thumbnail(
                            url=pytube.YouTube(
                                url=random_song[1]).thumbnail_url
                        )
                        embed.add_field(
                            name="Uploader",
                            value=pytube.YouTube(url=random_song[1]).author,
                            inline=True,
                        )
                        embed.add_field(
                            name="Duration",
                            value=time_converter(
                                pytube.YouTube(url=random_song[1]).length
                            ),
                            inline=True,
                        )
                        embed.set_footer(
                            text=f"Voice Channel Bitrate: {reaction.message.guild.voice_client.channel.bitrate/1000} kbps"
                        )
                        await reaction.message.edit(embed=embed)
                        voice.play(discord.FFmpegPCMAudio(
                            URL_shuffle, **FFMPEG_OPTS))

                else:
                    embed = discord.Embed(
                        description=f"{reaction.message.author.name}, connect to a voice channel first 🔊",
                        color=color,
                    )
                    embed.set_author(
                        name="Spider-Punk Radio™", icon_url=url_author_music)
                    await reaction.message.edit(embed=embed)

# ---------------------------------------------- STANDARD ----------------------------------------------------

@bot.command(aliases=["spidey", "spiderman", "webslinger", "webhead", "wallcrawler"])
async def spiderman_signal(ctx):

    number_of_requests()

    calls = [f"{ctx.author.name} is calling you!", f"Your aid has been requested by {ctx.author.name}.", f"{ctx.author.name} has got something for ya.", f"{ctx.author.name} requires your assistance.", f"{ctx.author.name} has called."]
    embed = discord.Embed(description=random.choice(calls), color=color)
    embed.set_image(url=random.choice(hello_urls))
    await ctx.send("<@!622497106657148939>")
    await ctx.send(embed=embed)


@bot.command(aliases=["hello", "hi", "hey", "hey there", "salut", "kon'nichiwa", "hola", "aloha"])
async def greet_bot(ctx):

    number_of_requests()

    greetings = [f"Hey {ctx.author.name}!", f"Hi {ctx.author.name}!", f"How's it going {ctx.author.name}?", f"What can I do for you {ctx.author.name}?", f"What's up {ctx.author.name}?", f"Hello {ctx.author.name}!", f"So {ctx.author.name}, how's your day going?"]
    embed = discord.Embed(color=color)
    embed.set_author(name=random.choice(greetings), icon_url=ctx.author.avatar_url)
    embed.set_image(url=random.choice(hello_urls))
    await ctx.send(embed=embed)


@bot.command(aliases=["help", "use"])
async def embed_help(ctx):

    number_of_requests()
    message = await ctx.send(embed=help_menu())

    await message.add_reaction("⬅")
    await message.add_reaction("🕸")
    await message.add_reaction("➡")


@bot.command(aliases=["quips"])
async def get_quips(ctx):

    number_of_requests()

    try:
        embed = discord.Embed(title=random.choice(titles), description=random.choice(dialogue_list), color=color)
        embed.set_thumbnail(url=random.choice(url_thumbnails))
        embed.set_footer(text=random.choice(footers), icon_url=bot.user.avatar_url)
        await ctx.send(embed=embed)
        print("Quip successfully sent!")
    except Exception as e:
        embed = discord.Embed(title="Error", description=str(e), color=color)

# ----------------------------------------------- INTERNET ---------------------------------------------

@bot.command(aliases=["imdb"])
async def IMDb_movies(ctx, *, movie_name=None):

    number_of_requests()

    if movie_name is None:
        embed = discord.Embed(description=random.choice(imdb_responses), color=color)
        embed.set_author(name="Ahem ahem", icon_url=url_imdb_author)
        await ctx.send(embed=embed)

    if movie_name is not None:
        try:
            db = imdb.IMDb()
            movie = db.search_movie(movie_name)
            title = movie[0]["title"]
            movie_summary = (
                db.get_movie(movie[0].getID()).summary()
                .replace("=", "")
                .replace("Title", "**Title**")
                .replace("Movie", "")
                .replace("Genres", "**Genres**")
                .replace("Director", "**Director**")
                .replace("Writer", "**Writer(s)**")
                .replace("Cast", "**Cast**")
                .replace("Country", "**Country**")
                .replace("Language", "**Language**")
                .replace("Rating", "**Rating**")
                .replace("Plot", "**Plot**")
                .replace("Runtime", "**Runtime**")
            )
            movie_cover = movie[0]["full-size cover url"]
            embed = discord.Embed(title="🎬 {} 🍿".format(title), description=movie_summary, color=color)
            embed.set_thumbnail(url=url_imdb_thumbnail)  # 🎥 🎬 📽
            embed.set_image(url=movie_cover)
            await ctx.send(embed=embed)
        except Exception:
            embed = discord.Embed(description="I couldn't find `{}`.\nTry again and make sure you enter the correct movie name.".format(movie_name), color=color)
            embed.set_author(name="Movie Not Found 💬", icon_url=url_imdb_author)
            await ctx.send(embed=embed)


@bot.command(aliases=["reddit", "rd"])
async def reddit_memes(ctx, *, topic):

    number_of_requests()
    sub = reddit.subreddit(topic).random()

    if str(ctx.guild.id) not in default_topic:
        default_topic[str(ctx.guild.id)] = str(topic)
    else: pass
    if str(ctx.guild.id) in default_topic:
        default_topic[str(ctx.guild.id)] = str(topic)

    try:
        embed = discord.Embed(description="**Caption:\n**{}".format(sub.title), color=color)
        embed.set_author(name="Post by: {}".format(sub.author), icon_url=url_reddit_author)
        embed.set_thumbnail(url=url_reddit_thumbnail)
        embed.set_image(url=sub.url)
        embed.set_footer(text="🔺: {}   🔻: {}   💬: {}".format(sub.ups, sub.downs, sub.num_comments))
        message = await ctx.send(embed=embed)
        await message.add_reaction("🖱")
    except Exception:
        default_topic[str(ctx.guild.id)] = ""
        embed = discord.Embed(description="Looks like the subreddit is either banned or does not exist 🤔", color=color)
        embed.set_author(name="Subreddit Not Found", icon_url=url_reddit_author)
        await ctx.send(embed=embed)


@bot.command(aliases=["wiki", "w"])
async def wikipedia_results(ctx, *, thing_to_search):

    number_of_requests()

    try:
        try:
            title = wikipedia.page(thing_to_search)
            embed = discord.Embed(description=wikipedia.summary(thing_to_search), color=color)
            embed.set_author(name=title.title, icon_url=url_wiki)
            embed.add_field(name="Search References", value=", ".join([x for x in wikipedia.search(thing_to_search)][:5]), inline=False)
            embed.set_footer(text="Searched by: {}".format(ctx.author.name), icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            print("Results for wikipedia search sent...")
        except wikipedia.PageError as pe:
            embed = discord.Embed(description=str(pe), color=color)
            embed.set_author(name="Error", icon_url=url_wiki)
            await ctx.send(embed=embed)    
    except wikipedia.DisambiguationError as de:
        embed = discord.Embed(description=str(de), color=color)
        embed.set_author(name="Hmm...", icon_url=url_wiki)
        await ctx.send(embed=embed)


@bot.command(aliases=["google", "g"])
async def google_results(ctx, *, thing_to_search):

    number_of_requests()
    results = ""

    for result in search(thing_to_search, tld="com", lang="en", safe="off", num=6, start=0, stop=10, pause=1.0):
        results += result + "\n"

    await ctx.send("Search results for: **{}**".format(thing_to_search))
    await ctx.send(results)
    print("Results for google search sent...")

# ------------------------------------------------- UTILITY -------------------------------------------------

@bot.command(aliases=["delete", "del"])
async def clear(ctx, text, num=10000000000000):

    number_of_requests()
    await ctx.channel.purge(limit=1)

    if str(text) == "WEB":
        await ctx.channel.purge(limit=num)
    else:
        await ctx.send("Incorrect Password")


@bot.command(aliases=["[X]"])
async def stop_program(ctx):

    number_of_requests()
    msgs = [f"Bye {ctx.author.name}!", f"See ya {ctx.author.name}!", f"Till next time {ctx.author.name}!"]

    if ctx.author.id == 622497106657148939:
        try:
            voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
            voice.stop()
            await voice.disconnect()
        except:
            pass
        conn.commit()
        await ctx.send(random.choice(msgs))
        print(random.choice(msgs))
        exit()
    else:
        await ctx.send("Access Denied")


@bot.command(aliases=["say"])
async def replicate_user_text(ctx, *, text):

    number_of_requests()

    await ctx.channel.purge(limit=1)
    await ctx.send(text)


@bot.command(aliases=["polls", "poll"])
async def conduct_poll(ctx, ems=None, title=None, *, description=None):

    number_of_requests()
    poll_channel = None

    for i in ctx.guild.channels:
        for j in poll_channels:
            if i.name == j:
                send_to = i.name = j
                poll_channel = discord.utils.get(
                    ctx.guild.channels, name=send_to)
                
    if title is not None:
        if "_" in title:
            title = title.replace("_", " ")
            
    if ems is not None and title is not None and description is not None:
        embed = discord.Embed(title=f"Topic: {title}", description=description, color=color)
        embed.set_footer(text=f"Conducted by: {ctx.author.name}", icon_url=ctx.author.avatar_url)
        message = await poll_channel.send(embed=embed)

        if ems == "y/n" or ems == "yes/no":
            await message.add_reaction("✅")
            await message.add_reaction("❌")
        elif ems == "t/t" or ems == "this/that":
            await message.add_reaction("👈🏻")
            await message.add_reaction("👉🏻")
        else:
            emojis = list(ems.split(","))
            for emoji in emojis:
                await message.add_reaction(emoji)
        if ctx.channel.name != poll_channel:
            await ctx.send(embed=discord.Embed(description="Poll Sent Successfully 👍🏻", color=color))
    
    elif title is None and description is None and ems is None:
        embed = discord.Embed( title="Polls", description="Command: `_polls emojis title description`", color=color)
        embed.add_field(name="Details", value="`emojis:` enter emojis for the poll and they will be added as reactions\n`title:` give a title to your poll.\n`description:` tell everyone what the poll is about.", inline=False)
        embed.add_field(name="Notes", value="To add reactions to poll the multiple emojis should be separated by a `,`.\nIf you wish to use default emojis, `y/n` for yes or no and `t/t` for this or that.\nIf the title happens to be more than one word long, use `_` in place of spaces as demonstrated below.\nExample: `The_Ultimate_Choice` will be displayed in the title of poll as `The Ultimate Choice`.", inline=False)
        embed.set_thumbnail(url=random.choice(url_thumbnails))
        await ctx.send(embed=embed)


@bot.command(aliases=["req", "requests"])
async def total_requests(ctx):

    number_of_requests()

    operation = "SELECT MAX(number) FROM requests"
    cursor.execute(operation)
    total = cursor.fetchall()
    embed = discord.Embed(description=f"""**Requests Made:\n**{str(total).replace("[(", " ").replace(",)]", " ")}""", color=color)
    await ctx.send(embed=embed)


@bot.command(aliases=["troll"])
async def troll_snipe(ctx):

    await ctx.channel.purge(limit=1)
    await ctx.send(random.choice(troll_links))
    await ctx.channel.purge(limit=1)


@bot.command(aliases=["web"])
async def snipe(ctx):

    number_of_requests()

    try:
        message = deleted_messages[ctx.channel.id][-1]
    
        if len(message) < 3:
            embed = discord.Embed(title="Deleted Message", description=message[1], color=color)
            embed.set_footer(text=f"Sent by: {bot.get_user(int(message[0]))}", icon_url=bot.get_user(int(message[0])).avatar_url,)
            await ctx.send(embed=embed)
    
        else:
            embed = discord.Embed(description="Embed deleted 👇🏻", color=color)
            embed.set_author(name=bot.get_user(int(message[0])), icon_url=bot.get_user(int(message[0])).avatar_url)
            await ctx.send(embed=embed)
            await ctx.send(embed=message[1])
    
    except KeyError:
        await ctx.send(embed=discord.Embed(description="There is nothing to web up 🕸", color=color))


@bot.command(aliases=["pfp"])
async def user_pfp(ctx, member: discord.Member = None):

    number_of_requests()

    if member is None:
        embed = discord.Embed(title="Profile Picture : {}".format(ctx.author.name), color=color)
        embed.set_image(url=ctx.author.avatar_url)
    else:
        embed = discord.Embed(title="Profile Picture : {}".format(member.name), color=color)
        embed.set_image(url=member.avatar_url)
    embed.set_footer(text=random.choice(compliments))
    await ctx.send(embed=embed)


@bot.command(aliases=["ping"])
async def get_ping(ctx):

    number_of_requests()

    ping = round(bot.latency * 1000)
    c1 = "🟢"
    c2 = "🟡"
    c3 = "🔴"
    if ping >= 350:
        embed = discord.Embed(description=f"{c3} {ping} ms", color=color)
        await ctx.send(embed=embed)
    elif ping <= 320:
        embed = discord.Embed(description=f"{c1} {ping} ms", color=color)
        await ctx.send(embed=embed)
    elif ping > 320 and ping < 350:
        embed = discord.Embed(description=f"{c2} {ping} ms", color=color)
        await ctx.send(embed=embed)


@bot.command(aliases=["serverinfo", "si"])
async def server_information(ctx):

    number_of_requests()

    name = str(ctx.guild.name)
    ID = str(ctx.guild.id)
    description = str(ctx.guild.description)
    owner = str(ctx.guild.owner)
    region = str(ctx.guild.region)
    num_mem = str(ctx.guild.member_count)
    icon = str(ctx.guild.icon_url)
    role_count = len(ctx.guild.roles)
    # bots_list = [bot.mention for bot in ctx.guild.members if bot.bot]

    embed = discord.Embed(title=f"📚 {name} 📚", color=color)
    embed.add_field(name="Owner", value=f"`{owner}`", inline=True)
    embed.add_field(name="Member Count", value=f"`{num_mem}`", inline=True)
    embed.add_field(name="Role Count", value=f"`{role_count}`", inline=True)
    embed.add_field(name="Region", value=f"`{region}`", inline=True)
    embed.add_field(name="Server ID", value=f"`{ID}`", inline=False)
    embed.add_field(name="Description", value=f"```{description}```", inline=False)
    embed.set_footer(text=f"Created on {ctx.guild.created_at.__format__('%A, %B %d, %Y @ %H:%M:%S')}", icon_url=ctx.author.avatar_url)
    embed.set_image(url=icon)
    await ctx.send(embed=embed)

# --------------------------------------- ENCRYPER DECRYPTER ---------------------------------


@bot.command(aliases=["hush"])
async def encrypt_data(ctx, mode, *, message):

    number_of_requests()

    res = message.encode()

    try:

        if mode == "en":
            embed = discord.Embed(
                title="Message Encrpyted",
                description="```{}```".format(str(cipher.encrypt(res)))
                .replace("b'", "")
                .replace("'", ""),
                color=color,
            )
            embed.set_thumbnail(url=url_en_dec)
            await ctx.channel.purge(limit=1)
            await ctx.send(embed=embed)

        if mode == "dec":
            embed = discord.Embed(
                title="Message Decrypted",
                description="```{}```".format(str(cipher.decrypt(res)))
                .replace("b'", "")
                .replace("'", ""),
                color=color,
            )
            embed.set_thumbnail(url=url_en_dec)
            await ctx.channel.purge(limit=1)
            await ctx.send(embed=embed)

    except Exception as e:
        embed = discord.Embed(title="Error", description=str(e), color=color)
        embed.set_thumbnail(url=url_en_dec)
        await ctx.send(embed=embed)


# ------------------------------------- DATE TIME CALENDAR ---------------------------------------------


@bot.command(aliases=["dt"])
async def date_time_ist(ctx, timezone=None):

    number_of_requests()

    if timezone is None:
        tzinfo = pytz.timezone(default_tz)
        dateTime = datetime.datetime.now(tz=tzinfo)
        embed = discord.Embed(color=color)
        embed.add_field(
            name="Date",
            value="%s/%s/%s" % (dateTime.day, dateTime.month, dateTime.year),
            inline=True,
        )
        embed.add_field(
            name="Time",
            value="%s:%s:%s" % (
                dateTime.hour, dateTime.minute, dateTime.second),
            inline=True,
        )
        embed.set_footer(text=f"Timezone : {default_tz}")
        # embed.set_thumbnail(url=url_dtc)
        await ctx.send(embed=embed)

    else:
        tzinfo = pytz.timezone(timezone)
        dateTime = datetime.datetime.now(tz=tzinfo)
        embed = discord.Embed(color=color)
        embed.add_field(
            name="Date",
            value="%s/%s/%s" % (dateTime.day, dateTime.month, dateTime.year),
            inline=True,
        )
        embed.add_field(
            name="Time",
            value="%s:%s:%s" % (
                dateTime.hour, dateTime.minute, dateTime.second),
            inline=True,
        )
        # embed.set_thumbnail(url=url_dtc)
        embed.set_footer(text=f"Timezone : {timezone}")
        await ctx.send(embed=embed)


@bot.command(aliases=["cal"])
async def get_calendar(ctx, year, month):

    number_of_requests()

    try:
        embed = discord.Embed(
            title="Calendar",
            description="```{}```".format(
                calendar.month(int(year), int(month))),
            color=color,
        )
        embed.set_thumbnail(url=url_dtc)
        await ctx.send(embed=embed)

    except IndexError:
        embed = discord.Embed(
            description="{}, this month doesn't exist 📆".format(
                ctx.author.name),
            color=color,
        )
        embed.set_author(name="Calendar", icon_url=url_dtc)
        await ctx.send(embed=embed)


# ------------------------------------------ SHELLS --------------------------------------------


@bot.command(aliases=[";"])
async def sql_shell(ctx, *, expression):

    number_of_requests()

    try:
        output = ""
        cursor.execute(expression)

        for item in cursor.fetchall():
            output += str(item) + "\n"

        conn.commit()
        embed = discord.Embed(
            title=str(expression), description=str(output), color=color
        )
        embed.set_author(name="MySQL Shell", icon_url=url_author_sql)
        await ctx.send(embed=embed)

    except Exception as e:
        embed_err = discord.Embed(
            title="Error", description=str(e), color=color)
        embed_err.set_author(name="MySQL Shell", icon_url=url_author_sql)
        await ctx.send(embed=embed_err)


@bot.command(aliases=["py"])
async def python_shell(ctx, *, expression):

    number_of_requests()

    if expression in denied or denied[-2] in expression or denied[-1] in expression:
        embed = discord.Embed(description=random.choice(
            denied_responses), color=color)
        embed.set_author(name="Access Denied", icon_url=url_author_python)
        await ctx.send(embed=embed)

    else:
        try:
            embed_acc = discord.Embed(
                description=f"**Input**\n{str(expression)}\n**Output**\n{str(eval(expression))}", color=color
            )
            embed_acc.set_author(name="Python Shell",
                                 icon_url=url_author_python)
            await ctx.send(embed=embed_acc)

        except Exception as e:
            embed_err = discord.Embed(
                title="Error", description=str(e), color=color)
            embed_err.set_author(name="Python Shell",
                                 icon_url=url_author_python)
            await ctx.send(embed=embed_err)


@bot.command(aliases=["pydoc"])
async def function_info(ctx, func):

    number_of_requests()

    try:

        if "(" in [char for char in func] and ")" in [char for char in func]:
            embed = discord.Embed(
                description=random.choice(no_functions), color=color)
            embed.set_author(name="Access Denied", icon_url=url_author_python)
            await ctx.send(embed=embed)

        else:
            function = eval(func)
            embed = discord.Embed(description=function.__doc__, color=color)
            embed.set_author(name="Info: {}".format(
                func), icon_url=url_author_python)
            await ctx.send(embed=embed)

    except Exception as e:
        embed = discord.Embed(description=str(e), color=color)
        embed.set_author(name="Error", icon_url=url_author_python)
        await ctx.send(embed=embed)


# ----------------------------------------------- MUSIC ----------------------------------------------------


@bot.command(aliases=["cn", "connect"])
async def join_vc(ctx):

    number_of_requests()

    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    try:

        if not ctx.message.author.voice:
            embed = discord.Embed(
                description="{}, connect to a voice channel first 🔊".format(
                    ctx.author.name
                ),
                color=color,
            )
            embed.set_author(name="Spider-Punk Radio™",
                             icon_url=url_author_music)
            await ctx.send(embed=embed)

        if voice == None:
            channel = ctx.message.author.voice.channel
            await channel.connect()
            embed = discord.Embed(
                description=f"Connected to {ctx.guild.voice_client.channel.name}",
                color=color,
            )
            embed.set_author(name="Spider-Punk Radio™",
                             icon_url=url_author_music)
            embed.set_footer(text=random.choice(connections))
            await ctx.send(embed=embed)

        if voice != None:
            embed = discord.Embed(
                description="Already connected to a voice channel ✅", color=color
            )
            embed.set_author(name="Spider-Punk Radio™",
                             icon_url=url_author_music)
            await ctx.send(embed=embed)

    except Exception as e:
        embed = discord.Embed(description="Error:\n" + str(e), color=color)
        embed.set_author(name="Error", icon_url=url_author_music)
        await ctx.send(embed=embed)


@bot.command(aliases=["dc", "disconnect"])
async def leave_vc(ctx):

    number_of_requests()

    try:

        if ctx.author.id in [member.id for member in ctx.voice_client.channel.members]:
            voice_client = ctx.message.guild.voice_client

            try:

                if voice_client.is_connected():
                    embed = discord.Embed(
                        description=f"Disconnected from {ctx.guild.voice_client.channel.name}",
                        color=color,
                    )
                    embed.set_author(
                        name="Spider-Punk Radio™", icon_url=url_author_music
                    )
                    embed.set_footer(text=random.choice(disconnections))
                    await ctx.send(embed=embed)
                    await voice_client.disconnect()

            except AttributeError:
                embed = discord.Embed(
                    description="I am not connected to a voice channel", color=color
                )
                embed.set_author(name="Spider-Punk Radio™",
                                 icon_url=url_author_music)
                await ctx.send(embed=embed)

        else:
            embed = discord.Embed(
                description="{}, buddy, connect to the voice channel first 🔊".format(
                    ctx.author.name
                ),
                color=color,
            )
            embed.set_author(name="Spider-Punk Radio™",
                             icon_url=url_author_music)
            await ctx.send(embed=embed)

    except AttributeError:
        embed = discord.Embed(
            description="I am not connected to a voice channel", color=color
        )
        embed.set_author(name="Spider-Punk Radio™", icon_url=url_author_music)
        await ctx.send(embed=embed)


@bot.command(aliases=["setbit", "bit"])
async def set_bitrate(ctx, kbps):

    number_of_requests()

    for items in ydl_op["postprocessors"]:
        items["preferredquality"] = str(kbps)
        embed = discord.Embed(
            description="**Bitrate:** {} kbps".format(kbps), color=color
        )
        embed.set_author(name="Audio Quality", icon_url=url_author_music)
        await ctx.send(embed=embed)


@bot.command(aliases=["queue", "q"])
async def queue_song(ctx, *, name=None):

    number_of_requests()

    if ctx.author.id not in [
        member.id for member in ctx.guild.voice_client.channel.members
    ]:
        embed = discord.Embed(
            description="{}, buddy, connect to a voice channel first 🔊".format(
                ctx.author.name
            ),
            color=color,
        )
        embed.set_author(name="Spider-Punk Radio™", icon_url=url_author_music)
        await ctx.send(embed=embed)

    else:

        if name is not None:
            # WEB SCRAPE
            name = name.replace(" ", "+")
            htm = urllib.request.urlopen(
                "https://www.youtube.com/results?search_query=" + name
            )
            video = regex.findall(r"watch\?v=(\S{11})", htm.read().decode())
            url = "https://www.youtube.com/watch?v=" + video[0]
            htm_code = str(urllib.request.urlopen(url).read().decode())
            starting = htm_code.find("<title>") + len("<title>")
            ending = htm_code.find("</title>")
            name_of_the_song = (
                htm_code[starting:ending].replace(
                    "&#39;", "'").replace("&amp;", "&")
            )
            # check if song is already queued
            operation_check = (
                f"SELECT song_url FROM music_queue WHERE server={str(ctx.guild.id)}"
            )
            cursor.execute(operation_check)
            index, check_list, links = None, [], cursor.fetchall()
            for link in links:
                link = str(link).replace(
                    "(", "").replace(",)", "").replace("'", "")
                check_list.append(link)
            if url in check_list:

                def song_position():
                    for position in range(len(check_list)):
                        if url == check_list[position]:
                            return position

                embed = discord.Embed(
                    description=f"{random.choice(already_queued)}\nSong Postion: {song_position()}",
                    color=color,
                )
                embed.set_author(name="Already Queued",
                                 icon_url=url_author_music)
                await ctx.send(embed=embed)
            else:
                operation_add_song = f"""INSERT INTO music_queue(song_name, song_url, server)VALUES("{name_of_the_song}","{url}","{str(ctx.guild.id)}")"""
                cursor.execute(operation_add_song)
                embed = discord.Embed(
                    description=f"{name_of_the_song}".replace(
                        " - YouTube", " "),
                    color=color,
                )
                embed.set_author(name="Song added", icon_url=url_author_music)
                await ctx.send(embed=embed)

        else:
            operation_view = (
                "SELECT song_name, song_url FROM music_queue WHERE server={}".format(
                    str(ctx.guild.id)
                )
            )
            cursor.execute(operation_view)
            songs = cursor.fetchall()

            if len(songs) > 0:

                try:
                    string = ""
                    if server_index[str(ctx.guild.id)] > 10:
                        index = server_index[str(ctx.guild.id)] - 10
                        for song in songs[index: index + 20]:
                            string += (
                                str(index)
                                + ") "
                                + f"{song[0]}\n".replace(" - YouTube", " ")
                            )
                            index += 1

                        embed = discord.Embed(description=string, color=color)
                        embed.set_author(
                            name=f"{ctx.guild.name}'s Playlist",
                            icon_url=url_author_music,
                        )
                        embed.set_thumbnail(
                            url=random.choice(url_thumbnail_music))
                        embed.set_footer(text=f"Number Of Songs: {len(songs)}")
                        player = await ctx.send(embed=embed)

                        await player.add_reaction("⏮")  # previous track
                        await player.add_reaction("▶")  # resume
                        await player.add_reaction("⏸")  # pause
                        await player.add_reaction("⏭")  # next
                        await player.add_reaction("🔂")  # repeat
                        await player.add_reaction("⏹")  # stop
                        await player.add_reaction("🔀")  # shuffle
                        await player.add_reaction("*️⃣")  # current song
                        await player.add_reaction("🔠")  # display queue
                        await player.add_reaction("🔼")  # scroll
                        await player.add_reaction("🔽")  # scroll

                    else:
                        index = server_index[str(ctx.guild.id)]
                        for song in songs[index: index + 20]:
                            string += (
                                str(index)
                                + ") "
                                + f"{song[0]}\n".replace(" - YouTube", " ")
                            )
                            index += 1

                        embed = discord.Embed(description=string, color=color)
                        embed.set_author(
                            name=f"{ctx.guild.name}'s Playlist",
                            icon_url=url_author_music,
                        )
                        embed.set_thumbnail(
                            url=random.choice(url_thumbnail_music))
                        embed.set_footer(text=f"Number Of Songs: {len(songs)}")
                        player = await ctx.send(embed=embed)

                        await player.add_reaction("⏮")  # previous track
                        await player.add_reaction("▶")  # resume
                        await player.add_reaction("⏸")  # pause
                        await player.add_reaction("⏭")  # next
                        await player.add_reaction("🔂")  # repeat
                        await player.add_reaction("⏹")  # stop
                        await player.add_reaction("🔀")  # shuffle
                        await player.add_reaction("*️⃣")  # current song
                        await player.add_reaction("🔠")  # display queue
                        await player.add_reaction("🔼")  # scroll
                        await player.add_reaction("🔽")  # scroll

                except KeyError:
                    embed = discord.Embed(
                        description=random.choice(default_index), color=color
                    )
                    embed.set_author(
                        name="Spider-Punk Radio™", icon_url=url_author_music
                    )
                    await ctx.send(embed=embed)

            else:
                embed = discord.Embed(
                    description=random.choice(empty_queue), color=color
                )
                embed.set_author(
                    name=f"{ctx.guild.name}'s Playlist", icon_url=url_author_music
                )
                embed.set_thumbnail(url=random.choice(url_thumbnail_music))
                embed.set_footer(
                    text="Queue songs by using _q song, t!q song, |q song")
                await ctx.send(embed=embed)


@bot.command(aliases=["play", "p"])
async def play_music(ctx, *, char):

    number_of_requests()

    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    try:

        if ctx.author.id in [member.id for member in ctx.voice_client.channel.members]:

            try:

                if char.isdigit() == False:

                    if str(ctx.guild.id) not in server_index:
                        server_index[str(ctx.guild.id)] = 0

                    else:
                        pass

                    # Web Scrape
                    char = char.replace(" ", "+")
                    htm = urllib.request.urlopen(
                        "https://www.youtube.com/results?search_query=" + char
                    )
                    video = regex.findall(
                        r"watch\?v=(\S{11})", htm.read().decode())
                    url = "https://www.youtube.com/watch?v=" + video[0]
                    htm_code = str(urllib.request.urlopen(url).read().decode())
                    starting = htm_code.find("<title>") + len("<title>")
                    ending = htm_code.find("</title>")
                    name_of_the_song = (
                        htm_code[starting:ending]
                        .replace("&#39;", "'")
                        .replace("&amp;", "&")
                        .replace(" - YouTube", " ")
                    )
                    URL_direct = youtube_download(ctx, url)

                    if ctx.voice_client.is_playing() != True:
                        embed = discord.Embed(
                            description="**Song: **{}".format(name_of_the_song).replace(
                                " - YouTube", " "
                            ),
                            color=color,
                        )
                        embed.set_author(
                            name="Now playing", url=url, icon_url=url_author_music
                        )
                        embed.set_thumbnail(
                            url=pytube.YouTube(url=url).thumbnail_url)
                        embed.add_field(
                            name="Uploader",
                            value=pytube.YouTube(url=url).author,
                            inline=True,
                        )
                        embed.set_footer(
                            text="Voice Channel Bitrate: {} kbps".format(
                                ctx.guild.voice_client.channel.bitrate / 1000
                            )
                        )
                        embed.add_field(
                            name="Duration",
                            value=time_converter(
                                pytube.YouTube(url=url).length),
                            inline=True,
                        )
                        player = await ctx.send(embed=embed)
                        voice.play(discord.FFmpegPCMAudio(
                            URL_direct, **FFMPEG_OPTS))

                        await player.add_reaction("▶")  # resume
                        await player.add_reaction("⏸")  # pause
                        await player.add_reaction("⏹")  # stop

                    else:
                        voice.stop()
                        embed = discord.Embed(
                            description="**Song: **{}".format(name_of_the_song).replace(
                                " - YouTube", " "
                            ),
                            color=color,
                        )
                        embed.set_author(
                            name="Now playing", url=url, icon_url=url_author_music
                        )
                        embed.set_footer(
                            text="Voice Channel Bitrate: {} kbps".format(
                                ctx.guild.voice_client.channel.bitrate / 1000
                            )
                        )
                        embed.set_thumbnail(
                            url=pytube.YouTube(url=url).thumbnail_url)
                        embed.add_field(
                            name="Uploader",
                            value=pytube.YouTube(url=url).author,
                            inline=True,
                        )
                        embed.add_field(
                            name="Duration",
                            value=time_converter(
                                pytube.YouTube(url=url).length),
                            inline=True,
                        )
                        player = await ctx.send(embed=embed)
                        voice.play(discord.FFmpegPCMAudio(
                            URL_direct, **FFMPEG_OPTS))

                        await player.add_reaction("▶")  # resume
                        await player.add_reaction("⏸")  # pause
                        await player.add_reaction("⏹")  # stop

                if char.isdigit() == True:
                    # Server Specific Queue
                    operation = (
                        f"SELECT * FROM music_queue WHERE server={str(ctx.guild.id)}"
                    )
                    cursor.execute(operation)
                    server_queue = cursor.fetchall()

                    if str(ctx.guild.id) not in server_index:
                        server_index[str(ctx.guild.id)] = int(char)

                    if str(ctx.guild.id) in server_index:
                        server_index[str(ctx.guild.id)] = int(char)

                    try:
                        URL_queue = youtube_download(
                            ctx, server_queue[int(char)][1])

                        if ctx.voice_client.is_playing() != True:
                            embed = discord.Embed(
                                description="**Song: **{a}\n**Queue Index: **{b}".format(
                                    a=server_queue[int(char)][0], b=char
                                ).replace(
                                    " - YouTube", " "
                                ),
                                color=color,
                            )
                            embed.set_author(
                                name="Now playing", icon_url=url_author_music
                            )
                            embed.set_thumbnail(
                                url=pytube.YouTube(
                                    url=server_queue[int(char)][1]
                                ).thumbnail_url
                            )
                            embed.set_footer(
                                text="Voice Channel Bitrate: {} kbps".format(
                                    ctx.guild.voice_client.channel.bitrate / 1000
                                )
                            )
                            embed.add_field(
                                name="Uploader",
                                value=pytube.YouTube(
                                    url=server_queue[int(char)][1]
                                ).author,
                                inline=True,
                            )
                            embed.add_field(
                                name="Duration",
                                value=time_converter(
                                    pytube.YouTube(
                                        url=server_queue[int(char)][1]
                                    ).length
                                ),
                                inline=True,
                            )
                            voice.play(discord.FFmpegPCMAudio(
                                URL_queue, **FFMPEG_OPTS))
                            player = await ctx.send(embed=embed)

                            await player.add_reaction("⏮")  # previous track
                            await player.add_reaction("▶")  # resume
                            await player.add_reaction("⏸")  # pause
                            await player.add_reaction("⏭")  # next
                            await player.add_reaction("🔂")  # repeat
                            await player.add_reaction("⏹")  # stop
                            await player.add_reaction("🔀")  # shuffle
                            await player.add_reaction("*️⃣")  # current song
                            await player.add_reaction("🔠")  # display queue
                            await player.add_reaction("🔼")  # scroll
                            await player.add_reaction("🔽")  # scroll

                        else:
                            voice.stop()
                            embed = discord.Embed(
                                description="**Song: **{a}\n**Queue Index: **{b}".format(
                                    a=server_queue[int(char)][0], b=char
                                ).replace(
                                    " - YouTube", " "
                                ),
                                color=color,
                            )
                            embed.set_author(
                                name="Now playing", icon_url=url_author_music
                            )
                            embed.set_thumbnail(
                                url=pytube.YouTube(
                                    url=server_queue[int(char)][1]
                                ).thumbnail_url
                            )
                            embed.set_footer(
                                text="Voice Channel Bitrate: {} kbps".format(
                                    ctx.guild.voice_client.channel.bitrate / 1000
                                )
                            )
                            embed.add_field(
                                name="Uploader",
                                value=pytube.YouTube(
                                    url=server_queue[int(char)][1]
                                ).author,
                                inline=True,
                            )
                            embed.add_field(
                                name="Duration",
                                value=time_converter(
                                    pytube.YouTube(
                                        url=server_queue[int(char)][1]
                                    ).length
                                ),
                                inline=True,
                            )
                            player = await ctx.send(embed=embed)
                            voice.play(discord.FFmpegPCMAudio(
                                URL_queue, **FFMPEG_OPTS))

                            # previous track
                            await player.add_reaction("⏮")
                            await player.add_reaction("▶")  # resume
                            await player.add_reaction("⏸")  # pause
                            await player.add_reaction("⏭")  # next
                            await player.add_reaction("🔂")  # repeat
                            await player.add_reaction("⏹")  # stop
                            await player.add_reaction("🔀")  # shuffle
                            await player.add_reaction("*️⃣")  # current song
                            await player.add_reaction("🔠")  # display queue
                            await player.add_reaction("🔼")  # scroll
                            await player.add_reaction("🔽")  # scroll

                    except IndexError:
                        embed = discord.Embed(
                            description="Looks like there is no song at this index",
                            color=color,
                        )
                        embed.set_author(
                            name="Oops...", icon_url=url_author_music)
                        await ctx.send(embed=embed)

            except AttributeError:
                embed = discord.Embed(
                    description="I am not connected to a voice channel".format(
                        ctx.author.name
                    ),
                    color=color,
                )
                embed.set_author(name="Voice", icon_url=url_author_music)
                await ctx.send(embed=embed)

        else:
            embed = discord.Embed(
                description="{}, buddy, connect to a voice channel first 🔊".format(
                    ctx.author.name
                ),
                color=color,
            )
            embed.set_author(name="Spider-Punk Radio™",
                             icon_url=url_author_music)
            await ctx.send(embed=embed)

    except AttributeError:
        embed = discord.Embed(
            description="I am not connected to a voice channel".format(
                ctx.author.name),
            color=color,
        )
        embed.set_author(name="Voice", icon_url=url_author_music)
        await ctx.send(embed=embed)


@bot.command(aliases=["songinfo"])
async def fetch_current_song(ctx):

    number_of_requests()

    global server_index
    operation = "SELECT * FROM music_queue WHERE server={}".format(
        str(ctx.guild.id))
    cursor.execute(operation)
    server_queue = cursor.fetchall()

    if len(server_queue) <= 0:
        embed = discord.Embed(
            description="There are no songs in the queue currently 🤔")
        embed.set_author(name="Uh oh...", icon_url=url_author_music)
        await ctx.send(embed=embed)

    else:

        try:
            embed = discord.Embed(
                description="**Song: **{a}\n**Index: **{b}\n**Views: **{c}\n**Description: **\n{d}".format(
                    a=server_queue[server_index[str(ctx.guild.id)]][0],
                    b=server_index[str(ctx.guild.id)],
                    c=pytube.YouTube(
                        url=server_queue[server_index[str(ctx.guild.id)]][1]
                    ).views,
                    d=pytube.YouTube(
                        url=server_queue[server_index[str(ctx.guild.id)]][1]
                    ).description,
                ),
                color=color,
            )
            embed.set_thumbnail(
                url=pytube.YouTube(
                    url=server_queue[server_index[str(ctx.guild.id)]][1]
                ).thumbnail_url
            )
            embed.set_footer(
                text="Voice Channel Bitrate: {} kbps".format(
                    ctx.guild.voice_client.channel.bitrate / 1000
                )
            )
            embed.set_author(name="Currently Playing",
                             icon_url=url_author_music)
            player = await ctx.send(embed=embed)
            await player.add_reaction("⏮")  # previous track
            await player.add_reaction("▶")  # resume
            await player.add_reaction("⏸")  # pause
            await player.add_reaction("⏭")  # next
            await player.add_reaction("🔂")  # repeat
            await player.add_reaction("⏹")  # stop
            await player.add_reaction("🔀")  # shuffle
            await player.add_reaction("*️⃣")  # current song
            await player.add_reaction("🔠")  # display queue
            await player.add_reaction("🔼")  # scroll
            await player.add_reaction("🔽")  # scroll

        except KeyError:
            embed = discord.Embed(
                description=random.choice(default_index), color=color)
            embed.set_author(name="Spider-Punk Radio™",
                             icon_url=url_author_music)
            await ctx.send(embed=embed)


@bot.command(aliases=["prev", "previous"])
async def previous_song(ctx):

    number_of_requests()

    global server_index
    server_index[str(ctx.guild.id)] -= 1
    operation = "SELECT * FROM music_queue WHERE server={}".format(
        str(ctx.guild.id))
    cursor.execute(operation)
    server_queue = cursor.fetchall()
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    if ctx.author.id in [member.id for member in ctx.voice_client.channel.members]:

        try:
            URL_queue = youtube_download(
                ctx, server_queue[server_index[str(ctx.guild.id)]][1]
            )

            if ctx.voice_client.is_playing() != True:
                embed = discord.Embed(
                    description="**Song: **{}".format(
                        server_queue[server_index[str(ctx.guild.id)]][0]
                    ).replace(" - YouTube", " "),
                    color=color,
                )
                embed.set_author(name="Now playing", icon_url=url_author_music)
                embed.set_thumbnail(
                    url=pytube.YouTube(
                        url=server_queue[server_index[str(ctx.guild.id)]][1]
                    ).thumbnail_url
                )
                embed.add_field(
                    name="Uploader",
                    value=pytube.YouTube(
                        url=server_queue[server_index[str(ctx.guild.id)]][1]
                    ).author,
                    inline=True,
                )
                embed.add_field(
                    name="Duration",
                    value=time_converter(
                        pytube.YouTube(
                            url=server_queue[server_index[str(
                                ctx.guild.id)]][1]
                        ).length
                    ),
                    inline=True,
                )
                embed.set_footer(
                    text="Voice Channel Bitrate: {} kbps".format(
                        ctx.guild.voice_client.channel.bitrate / 1000
                    )
                )
                player = await ctx.send(embed=embed)
                voice.play(discord.FFmpegPCMAudio(URL_queue, **FFMPEG_OPTS))

                await player.add_reaction("⏮")  # previous track
                await player.add_reaction("▶")  # resume
                await player.add_reaction("⏸")  # pause
                await player.add_reaction("⏭")  # next
                await player.add_reaction("🔂")  # repeat
                await player.add_reaction("⏹")  # stop
                await player.add_reaction("🔀")  # shuffle
                await player.add_reaction("*️⃣")  # current song
                await player.add_reaction("🔠")  # display queue
                await player.add_reaction("🔼")  # scroll
                await player.add_reaction("🔽")  # scroll

            else:
                voice.stop()
                embed = discord.Embed(
                    description="**Song: **{}".format(
                        server_queue[server_index[str(ctx.guild.id)]][0]
                    ).replace(" - YouTube", " "),
                    color=color,
                )
                embed.set_author(name="Now playing", icon_url=url_author_music)
                embed.set_thumbnail(
                    url=pytube.YouTube(
                        url=server_queue[server_index[str(ctx.guild.id)]][1]
                    ).thumbnail_url
                )
                embed.add_field(
                    name="Uploader",
                    value=pytube.YouTube(
                        url=server_queue[server_index[str(ctx.guild.id)]][1]
                    ).author,
                    inline=True,
                )
                embed.add_field(
                    name="Duration",
                    value=time_converter(
                        pytube.YouTube(
                            url=server_queue[server_index[str(
                                ctx.guild.id)]][1]
                        ).length
                    ),
                    inline=True,
                )
                embed.set_footer(
                    text="Voice Channel Bitrate: {} kbps".format(
                        ctx.guild.voice_client.channel.bitrate / 1000
                    )
                )
                player = await ctx.send(embed=embed)
                voice.play(discord.FFmpegPCMAudio(URL_queue, **FFMPEG_OPTS))

                await player.add_reaction("⏮")  # previous track
                await player.add_reaction("▶")  # resume
                await player.add_reaction("⏸")  # pause
                await player.add_reaction("⏭")  # next
                await player.add_reaction("🔂")  # repeat
                await player.add_reaction("⏹")  # stop
                await player.add_reaction("🔀")  # shuffle
                await player.add_reaction("*️⃣")  # current song
                await player.add_reaction("🔠")  # display queue
                await player.add_reaction("🔼")  # scroll
                await player.add_reaction("🔽")  # scroll

        except IndexError:
            embed = discord.Embed(
                description="Looks like there is no song at this index", color=color
            )
            embed.set_author(name="Oops...", icon_url=url_author_music)
            embed.set_footer(
                text="Voice Channel Bitrate: {} kbps".format(
                    ctx.guild.voice_client.channel.bitrate / 1000
                )
            )
            await ctx.send(embed=embed)

    else:
        embed = discord.Embed(
            description="{}, buddy, connect to a voice channel first 🔊".format(
                ctx.author.name
            ),
            color=color,
        )
        embed.set_author(name="Spider-Punk Radio™", icon_url=url_author_music)
        await ctx.send(embed=embed)


@bot.command(aliases=["rep", "repeat"])
async def repeat_song(ctx):

    operation = "SELECT * FROM music_queue WHERE server={}".format(
        str(ctx.guild.id))
    cursor.execute(operation)
    server_queue = cursor.fetchall()
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    try:
        URL_queue = youtube_download(
            ctx, server_queue[server_index[str(ctx.guild.id)]][1]
        )

        if ctx.voice_client.is_playing() != True:
            embed = discord.Embed(
                description="**Song: **{}".format(
                    server_queue[server_index[str(ctx.guild.id)]][0]
                ).replace(" - YouTube", " "),
                color=color,
            )
            embed.set_author(name="Repeating Song", icon_url=url_author_music)
            embed.set_thumbnail(
                url=pytube.YouTube(
                    url=server_queue[server_index[str(ctx.guild.id)]][1]
                ).thumbnail_url
            )
            embed.add_field(
                name="Uploader",
                value=pytube.YouTube(
                    url=server_queue[server_index[str(ctx.guild.id)]][1]
                ).author,
                inline=True,
            )
            embed.add_field(
                name="Duration",
                value=time_converter(
                    pytube.YouTube(
                        url=server_queue[server_index[str(ctx.guild.id)]][1]
                    ).length
                ),
                inline=True,
            )
            embed.set_footer(
                text="Voice Channel Bitrate: {} kbps".format(
                    ctx.guild.voice_client.channel.bitrate / 1000
                )
            )
            player = await ctx.send(embed=embed)
            voice.play(discord.FFmpegPCMAudio(URL_queue, **FFMPEG_OPTS))

            await player.add_reaction("⏮")  # previous track
            await player.add_reaction("▶")  # resume
            await player.add_reaction("⏸")  # pause
            await player.add_reaction("⏭")  # next
            await player.add_reaction("🔂")  # repeat
            await player.add_reaction("⏹")  # stop
            await player.add_reaction("🔀")  # shuffle
            await player.add_reaction("*️⃣")  # current song
            await player.add_reaction("🔠")  # display queue
            await player.add_reaction("🔼")  # scroll
            await player.add_reaction("🔽")  # scroll

        else:
            voice.stop()
            embed = discord.Embed(
                description="**Song: **{}".format(
                    server_queue[server_index[str(ctx.guild.id)]][0]
                ).replace(" - YouTube", " "),
                color=color,
            )
            embed.set_author(name="Repeating Song", icon_url=url_author_music)
            embed.set_thumbnail(
                url=pytube.YouTube(
                    url=server_queue[server_index[str(ctx.guild.id)]][1]
                ).thumbnail_url
            )
            embed.add_field(
                name="Uploader",
                value=pytube.YouTube(
                    url=server_queue[server_index[str(ctx.guild.id)]][1]
                ).author,
                inline=True,
            )
            embed.add_field(
                name="Duration",
                value=time_converter(
                    pytube.YouTube(
                        url=server_queue[server_index[str(ctx.guild.id)]][1]
                    ).length
                ),
                inline=True,
            )
            embed.set_footer(
                text="Voice Channel Bitrate: {} kbps".format(
                    ctx.guild.voice_client.channel.bitrate / 1000
                )
            )
            player = await ctx.send(embed=embed)
            voice.play(discord.FFmpegPCMAudio(URL_queue, **FFMPEG_OPTS))

            await player.add_reaction("⏮")  # previous track
            await player.add_reaction("▶")  # resume
            await player.add_reaction("⏸")  # pause
            await player.add_reaction("⏭")  # next
            await player.add_reaction("🔂")  # repeat
            await player.add_reaction("⏹")  # stop
            await player.add_reaction("🔀")  # shuffle
            await player.add_reaction("*️⃣")  # current song
            await player.add_reaction("🔠")  # display queue
            await player.add_reaction("🔼")  # scroll
            await player.add_reaction("🔽")  # scroll

    except Exception as e:
        embed = discord.Embed(description=str(e), color=color)
        embed.set_author(name="Error", icon_url=url_author_music)
        await ctx.send(embed=embed)


@bot.command(aliases=["skip", "next"])
async def skip_song(ctx):

    number_of_requests()

    global server_index
    server_index[str(ctx.guild.id)] += 1
    operation = "SELECT * FROM music_queue WHERE server={}".format(
        str(ctx.guild.id))
    cursor.execute(operation)
    server_queue = cursor.fetchall()
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    if ctx.author.id in [member.id for member in ctx.voice_client.channel.members]:

        try:
            URL_queue = youtube_download(
                ctx, server_queue[server_index[str(ctx.guild.id)]][1]
            )

            if ctx.voice_client.is_playing() != True:
                embed = discord.Embed(
                    description="**Song: **{}".format(
                        server_queue[server_index[str(ctx.guild.id)]][0]
                    ).replace(" - YouTube", " "),
                    color=color,
                )
                embed.set_author(name="Now Playing", icon_url=url_author_music)
                embed.set_thumbnail(
                    url=pytube.YouTube(
                        url=server_queue[server_index[str(ctx.guild.id)]][1]
                    ).thumbnail_url
                )
                embed.add_field(
                    name="Uploader",
                    value=pytube.YouTube(
                        url=server_queue[server_index[str(ctx.guild.id)]][1]
                    ).author,
                    inline=True,
                )
                embed.add_field(
                    name="Duration",
                    value=time_converter(
                        pytube.YouTube(
                            url=server_queue[server_index[str(
                                ctx.guild.id)]][1]
                        ).length
                    ),
                    inline=True,
                )
                embed.set_footer(
                    text="Voice Channel Bitrate: {} kbps".format(
                        ctx.guild.voice_client.channel.bitrate / 1000
                    )
                )
                player = await ctx.send(embed=embed)
                voice.play(discord.FFmpegPCMAudio(URL_queue, **FFMPEG_OPTS))

                await player.add_reaction("⏮")  # previous track
                await player.add_reaction("▶")  # resume
                await player.add_reaction("⏸")  # pause
                await player.add_reaction("⏭")  # next
                await player.add_reaction("🔂")  # repeat
                await player.add_reaction("⏹")  # stop
                await player.add_reaction("🔀")  # shuffle
                await player.add_reaction("*️⃣")  # current song
                await player.add_reaction("🔠")  # display queue
                await player.add_reaction("🔼")  # scroll
                await player.add_reaction("🔽")  # scroll

            else:
                voice.stop()
                embed = discord.Embed(
                    description="**Song: **{}".format(
                        server_queue[server_index[str(ctx.guild.id)]][0]
                    ).replace(" - YouTube", " "),
                    color=color,
                )
                embed.set_author(name="Now playing", icon_url=url_author_music)
                embed.set_thumbnail(
                    url=pytube.YouTube(
                        url=server_queue[server_index[str(ctx.guild.id)]][1]
                    ).thumbnail_url
                )
                embed.add_field(
                    name="Uploader",
                    value=pytube.YouTube(
                        url=server_queue[server_index[str(ctx.guild.id)]][1]
                    ).author,
                    inline=True,
                )
                embed.add_field(
                    name="Duration",
                    value=time_converter(
                        pytube.YouTube(
                            url=server_queue[server_index[str(
                                ctx.guild.id)]][1]
                        ).length
                    ),
                    inline=True,
                )
                embed.set_footer(
                    text="Voice Channel Bitrate: {} kbps".format(
                        ctx.guild.voice_client.channel.bitrate / 1000
                    )
                )
                player = await ctx.send(embed=embed)
                voice.play(discord.FFmpegPCMAudio(URL_queue, **FFMPEG_OPTS))

                await player.add_reaction("⏮")  # previous track
                await player.add_reaction("▶")  # resume
                await player.add_reaction("⏸")  # pause
                await player.add_reaction("⏭")  # next
                await player.add_reaction("🔂")  # repeat
                await player.add_reaction("⏹")  # stop
                await player.add_reaction("🔀")  # shuffle
                await player.add_reaction("*️⃣")  # current song
                await player.add_reaction("🔠")  # display queue
                await player.add_reaction("🔼")  # scroll
                await player.add_reaction("🔽")  # scroll

        except IndexError:
            embed = discord.Embed(
                description="Looks like there is no song at this index", color=color
            )
            embed.set_author(name="Oops...", icon_url=url_author_music)
            embed.set_footer(
                text="Voice Channel Bitrate: {} kbps".format(
                    ctx.guild.voice_client.channel.bitrate / 1000
                )
            )
            await ctx.send(embed=embed)

    else:
        embed = discord.Embed(
            description="{}, buddy, connect to a voice channel first 🔊".format(
                ctx.author.name
            ),
            color=color,
        )
        embed.set_author(name="Spider-Punk Radio™", icon_url=url_author_music)
        await ctx.send(embed=embed)


@bot.command(aliases=["pause"])
async def pause_song(ctx):

    number_of_requests()

    voice_client = ctx.message.guild.voice_client
    pause = ctx.voice_client.is_paused()
    playing = ctx.voice_client.is_playing()

    if ctx.author.id in [mem.id for mem in ctx.voice_client.channel.members]:

        try:

            if playing == True:
                voice_client.pause()
                message = await ctx.send("Song paused")
                await message.add_reaction("⏸")

            else:

                if pause == True:
                    embed = discord.Embed(
                        description="Song is already paused ❗", color=color
                    )
                    embed.set_footer(
                        text="Voice Channel Bitrate: {} kbps".format(
                            ctx.guild.voice_client.channel.bitrate / 1000
                        )
                    )
                    await ctx.send(embed=embed)

                else:
                    embed = discord.Embed(
                        description="No song playing currently ❗", color=color
                    )
                    embed.set_footer(
                        text="Voice Channel Bitrate: {} kbps".format(
                            ctx.guild.voice_client.channel.bitrate / 1000
                        )
                    )
                    await ctx.send(embed=embed)

        except Exception as e:
            embed = discord.Embed(description=str(e), color=color)
            embed.set_author(name="Error", icon_url=url_author_music)
            await ctx.send(embed=embed)

    else:
        embed = discord.Embed(
            description="{}, buddy, connect to a voice channel first 🔊".format(
                ctx.author.name
            ),
            color=color,
        )
        embed.set_author(name="Spider-Punk Radio™", icon_url=url_author_music)
        await ctx.send(embed=embed)


@bot.command(aliases=["resume", "res"])
async def resume_song(ctx):

    number_of_requests()

    voice_client = ctx.message.guild.voice_client
    pause = ctx.voice_client.is_paused()
    playing = ctx.voice_client.is_playing()

    if ctx.author.id in [member.id for member in ctx.voice_client.channel.members]:

        try:

            if pause == True:
                voice_client.resume()
                message = await ctx.send("Song resumed")
                await message.add_reaction("▶")

            else:

                if playing == True:
                    embed = discord.Embed(
                        description="Song is not paused 🤔", color=color
                    )
                    embed.set_author(
                        name="Spider-Punk Radio™", icon_url=url_author_music
                    )
                    embed.set_footer(
                        text="Voice Channel Bitrate: {} kbps".format(
                            ctx.guild.voice_client.channel.bitrate / 1000
                        )
                    )
                    await ctx.send(embed=embed)

                else:
                    embed = discord.Embed(
                        description="Nothing is playing right now", color=color
                    )
                    embed.set_author(
                        name="Spider-Punk Radio™", icon_url=url_author_music
                    )
                    embed.set_footer(
                        text="Voice Channel Bitrate: {} kbps".format(
                            ctx.guild.voice_client.channel.bitrate / 1000
                        )
                    )
                    await ctx.send(embed=embed)

        except Exception as e:
            embed = discord.Embed(description=str(e), color=color)
            embed.set_author(name="Error", icon_url=url_author_music)
            await ctx.send(embed=embed)

    else:
        embed = discord.Embed(
            description="{}, buddy, connect to a voice channel first 🔊".format(
                ctx.author.name
            ),
            color=color,
        )
        embed.set_author(name="Spider-Punk Radio™", icon_url=url_author_music)
        await ctx.send(embed=embed)


@bot.command(aliases=["stop", "st"])
async def stop_song(ctx):

    number_of_requests()

    voice_client = ctx.message.guild.voice_client
    pause = ctx.voice_client.is_paused()
    playing = ctx.voice_client.is_playing()

    if ctx.author.id in [member.id for member in ctx.voice_client.channel.members]:

        try:

            if playing == True or pause == True:
                voice_client.stop()
                message = await ctx.send("Song stopped")
                await message.add_reaction("⏹")

            else:
                embed = discord.Embed(
                    description="Nothing is playing right now", color=color
                )
                embed.set_author(name="Spider-Punk Radio™",
                                 icon_url=url_author_music)
                embed.set_footer(
                    text="Voice Channel Bitrate: {} kbps".format(
                        ctx.guild.voice_client.channel.bitrate / 1000
                    )
                )
                await ctx.send(embed=embed)

        except Exception as e:
            embed = discord.Embed(description=str(e), color=color)
            embed.set_author(name="Error", icon_url=url_author_music)
            await ctx.send(embed=embed)

    else:
        embed = discord.Embed(
            description="{}, buddy, connect to a voice channel first 🔊".format(
                ctx.author.name
            ),
            color=color,
        )
        embed.set_author(name="Spider-Punk Radio™", icon_url=url_author_music)
        await ctx.send(embed=embed)


@bot.command(aliases=["rem", "remove"])
async def remove_song(ctx, index):

    number_of_requests()

    operation_view = 'SELECT * FROM music_queue WHERE server="{}"'.format(
        str(ctx.guild.id)
    )
    cursor.execute(operation_view)
    songs = cursor.fetchall()

    embed = discord.Embed(description="{}".format(
        songs[int(index)][0]), color=color)
    embed.set_author(name="Song removed", icon_url=url_author_music)

    await ctx.send(embed=embed)
    operation_remove = (
        "DELETE FROM music_queue WHERE song_url = '{a}' AND server='{b}'".format(
            a=songs[int(index)][1], b=str(ctx.guild.id)
        )
    )
    cursor.execute(operation_remove)


@bot.command(aliases=["clear_queue", "cq"])
async def clear_song_queue(ctx):

    number_of_requests()

    operation_queue = "SELECT * FROM music_queue WHERE server={}".format(
        str(ctx.guild.id)
    )
    cursor.execute(operation_queue)
    songs = cursor.fetchall()

    if len(songs) > 0:
        operation_clear_song = "DELETE FROM music_queue WHERE server={}".format(
            str(ctx.guild.id)
        )
        cursor.execute(operation_clear_song)
        message = await ctx.send("Queue Cleared")
        await message.add_reaction("✅")

    else:
        embed_empty = discord.Embed(
            description=random.choice(empty_queue), color=color)
        embed_empty.set_author(name="Hmm...", icon_url=url_author_music)
        await ctx.send(embed=embed_empty)


# -------------------------------------------------- EXTRA ---------------------------------------------------------


@bot.command(aliases=["thwip"])
async def thwipper(ctx):

    number_of_requests()

    await ctx.send(embed=discord.Embed(title="*Thwip!*", color=color))


@bot.command(aliases=["addbday"])
async def add_user_bday(ctx, member: discord.Member, month, day):

    number_of_requests()

    op_check = "SELECT mem_id FROM birthdays"
    cursor.execute(op_check)
    memIDs = cursor.fetchall()

    try:
        a = str([memID for memID in memIDs]).replace(
            "('", "").replace("',)", "")

        if str(member.id) not in a:
            op_insert = "INSERT INTO birthdays(mem_id, mem_month, mem_day)VALUES('{a}',{b},{c})".format(
                a=member.id, b=month, c=day
            )
            cursor.execute(op_insert)
            await ctx.send(
                embed=discord.Embed(
                    description="{}'s birthday added to database".format(
                        member.display_name
                    ),
                    color=color,
                )
            )

        else:
            await ctx.send(
                embed=discord.Embed(
                    description="{}'s birthday is already added in my database".format(
                        member.display_name
                    ),
                    color=color,
                )
            )

    except Exception as e:
        await ctx.send(str(e))


@bot.command(aliases=["rembday"])
async def remove_user_bday(ctx, member: discord.Member):

    number_of_requests()

    op_check = "SELECT mem_id FROM birthdays"
    cursor.execute(op_check)
    memIDs = cursor.fetchall()

    try:
        a = str([memID for memID in memIDs]).replace(
            "('", "").replace("',)", "")

        if str(member.id) in a:
            op_insert = "DELETE FROM birthdays WHERE mem_id={}".format(
                member.id)
            cursor.execute(op_insert)
            await ctx.send(
                embed=discord.Embed(
                    description="{}'s birthday removed from database".format(
                        member.display_name
                    ),
                    color=color,
                )
            )

        else:
            await ctx.send(
                embed=discord.Embed(
                    description="{}'s birthday does not exist in my database".format(
                        member.display_name
                    ),
                    color=color,
                )
            )

    except Exception as e:
        await ctx.send(str(e))


@bot.command(aliases=["bday"])
async def check_user_bdays_and_wish(ctx):

    number_of_requests()

    await ctx.channel.purge(limit=1)

    op_check = "SELECT * FROM birthdays"
    cursor.execute(op_check)
    bdays = cursor.fetchall()
    channel = None
    toggle = 0

    for i in ctx.guild.channels:
        for j in announcement_channels:
            if i.name == j:
                send_to = i.name = j
                channel = discord.utils.get(ctx.guild.channels, name=send_to)

    for bday in bdays:  # bday[0]   bday[1]  bday[2]

        if (
            datetime.datetime.today().month == bday[1]
            and datetime.datetime.today().day == bday[2]
        ):
            name = bot.get_user(int(bday[0])).name
            wishes = [
                f"🎊 Happy Birthday {name} 🎊",
                f"🎉 Happy Birthday {name} 🎉",
                f"✨ Happy Birthday {name} ✨",
                f"🎇 Happy Birthday {name} 🎇",
            ]
            embed = discord.Embed(
                title=random.choice(wishes),
                description=random.choice(descriptions),
                color=color,
            )
            embed.set_image(url=random.choice(url_bdays_spiderman))
            embed.set_thumbnail(url=bot.get_user(int(bday[0])).avatar_url)
            await channel.send(f"<@!{bot.get_user(int(bday[0])).id}>")
            message = await channel.send(embed=embed)

            await ctx.send(embed=discord.Embed(description="Wish Sent 🥳", color=color))
            await message.add_reaction("🎁")
            await message.add_reaction("🎈")
            await message.add_reaction("🎂")
            await message.add_reaction("🎆")
            await message.add_reaction("🎉")
            toggle = 1

    if toggle == 0:
        await ctx.send(
            embed=discord.Embed(
                description=random.choice(none_today), color=color)
        )


# --------------------------------------------------------------------------------------------------------------------------------------
