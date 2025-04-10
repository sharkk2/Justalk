### REQUIRED DATA ###

import discord
import logging
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv("shh.env")

cd = datetime.now().strftime('%Y-%m-%d %I.%M.%S')

### BOT CONFIG ###

version = '1.0.0'
prefix = 'jt.'

dbcollection = "Justalk"
auto_init = True # auto intilizes db for new servers

owner_ids = [1092548532180877415]

embedcolor = discord.Color.blurple()

embederrorcolor = discord.Color.red()

mongouri = os.getenv("mongouri")
token = os.getenv("token")
client_secret = os.getenv("client_secret")

log_channel = 1186322386241474611



### ENV CONFIG ###

directory = 'src/commands'

edirectory = 'src/core/events'

tdirectory = 'src/core/loops'


folder_blacklist = [
    "views",
    "functions",

]

file_blacklist = [
    'registry.py',
    '__init__.py'
]

### STARTUP SETTINGS ###

maintainance = False

log_msgs = True 

log_file = f"debug/boot_{cd}.log"

logging_file_mode = 'w'

logging_level = logging.DEBUG

logging_format = '%(asctime)s - %(levelname)s - %(message)s'

INFO_COLOR = "purple"
ERROR_COLOR = "red"
DEBUG_COLOR = "green"
WARNING_COLOR = "yellow"
FATAL_COLOR = "red2"


# EMOJIS

no = "<:no:1296811045444255755>"
error = "<:no:1296811045444255755>"
tick = "<:tick:1296811053119705118>"
yes = "<:tick:1296811053119705118>"
right = "<:right:1296811051488378930>"
left = "<:left:1296811043531784323>"
reply = "<:reply:1296811047419904091>"
replycont = "<:replycont:1296811049323860020>"


# STATUSES

statuses = [
    {"text": "(g) Guilds", "type": "dnd", "activity": "watching", "url": ""},
    {"text": "(c) Commands", "type": "idle", "activity": "listening", "url": ""},
] # a Listening to (chats) chats??
