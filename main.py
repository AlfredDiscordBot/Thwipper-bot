# IMPORTS
import nextcord
import os

from utils.assets import DEFAULT_COLOR
from utils.responses import status_list
from utils.functions import embed
from utils.Storage import Variables
from dotenv import load_dotenv
from nextcord.ext import commands, tasks
from random import choice

# LOADING ENVIRONMENT
load_dotenv()

# VARIABLES
var = Variables("storage")
if var.show_data() == {}:
    var.pass_all(
        config_color = {},
        queue_song = {}
    )
    var.save()


# CONFIGURING BOT
prefixes = ["t!", "_"]
intents = nextcord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(
    command_prefix=prefixes,
    intents=intents,
    case_insensitive=True,
)
bot.remove_command("help") # remove auto gen help menu

# BOT VARIABLES
RAW_DATA = var.show_data()
bot.config_color: dict = RAW_DATA.get("config_color", {})
bot.queue_song: dict = RAW_DATA.get("queue_song", {})
bot.color = lambda g: bot.config_color.get(g.id, DEFAULT_COLOR)


@bot.event
async def on_ready():
    print("Thwipper is now online.")

@tasks.loop(minutes=2)
async def loop():
    var.edit(
        config_color = bot.config_color,
        queue_song = bot.queue_song
    )
    var.save()
    await bot.change_presence(
        activity=nextcord.Activity(
            type=nextcord.ActivityType.playing, 
            name=choice(status_list)
        )
    )

# LOAD COGS
for i in os.listdir("cogs/"):
    if i.endswith(".py"): 
        bot.load_extension("cogs."+i[:-3])

# RUN BOT
bot.run(os.getenv("token"))