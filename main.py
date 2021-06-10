import os
import topgg
import asyncio
from pyrandmeme import *
from discord.ext import tasks
from discord.ext import commands
from discord_slash import SlashCommand

# Intents
intents = discord.Intents.default()
intents.members = True

# Bot Info Setup
client = commands.Bot(command_prefix="#", intents=intents)
slash = SlashCommand(client, sync_commands=True, sync_on_cog_reload=True)
client.remove_command("help")

# Load TOPGG

dbl_token = os.environ["TOPTOKEN"]
client.topggpy = topgg.DBLClient(client, dbl_token, autopost=True)

# Loop
async def status_task():
    while True:
        await client.change_presence(activity=discord.Game(name="/help | #help"))
        await asyncio.sleep(10)
        await client.change_presence(
            activity=discord.Game(name=f"{len(client.guilds)} servers!")
        )
        await asyncio.sleep(10)


@client.event
async def on_ready():
    print("Bot Is Online")
    client.loop.create_task(status_task())


@client.command()
@commands.is_owner()
async def load(ctx, folder, extension):
    client.load_extension(f"{folder}.{extension}")


@client.command()
@commands.is_owner()
async def unload(ctx, folder, extension):
    client.unload_extension(f"{folder}.{extension}")


for filename in os.listdir("./cogs/help"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.help.{filename[:-3]}")

for filename in os.listdir("./cogs/automated"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.automated.{filename[:-3]}")

for filename in os.listdir("./cogs/economy"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.economy.{filename[:-3]}")

for filename in os.listdir("./cogs/games"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.games.{filename[:-3]}")

for filename in os.listdir("./cogs/moderation"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.moderation.{filename[:-3]}")

for filename in os.listdir("./cogs/search"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.search.{filename[:-3]}")

for filename in os.listdir("./cogs/text"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.text.{filename[:-3]}")

for filename in os.listdir("./cogs/owner"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.owner.{filename[:-3]}")


@tasks.loop(minutes=30)
async def update_stats():
    """This function runs every 30 minutes to automatically update your server count."""
    try:
        await client.topggpy.post_guild_count()
        print(f"Posted server count ({client.topggpy.guild_count})")
    except Exception as e:
        print("Failed to post server count\n{}: {}".format(type(e).__name__, e))



@client.command()
@commands.is_owner()
async def update(ctx, news):
    await ctx.send(news)


@client.event
async def on_message(message):
    if client.user in message.mentions:
        embed = discord.Embed(
            title="Hey! Im DisSlash",
            description="Use `#help` Or `/help` For More Info!",
        )
        await message.channel.send(embed=embed)
    await client.process_commands(message)


update_stats.start()

TOKEN = os.environ["TOKEN"]
client.run(TOKEN)
