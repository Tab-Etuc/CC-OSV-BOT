import discord
from discord.ext import commands, tasks
import os
from dotenv import load_dotenv
from config import *
from itertools import cycle


load_dotenv()


activity = discord.Game('[C] | Chelp 以資查詢')
bot = commands.Bot(
    command_prefix = Prefix, 
    owner_ids = Owner_id, 
    intents = discord.Intents.all()
)
bot.remove_command("help")
status = cycle([
    "[C] 開發者 CC_#8844", 
    "[C] | Chelp 以資查詢", 
    "指令前綴  `C`"
])

@bot.event
async def on_ready():
  print(f'{bot.user.name}已成功上線！')
  status_swap.start()
  
@tasks.loop(seconds=10)
async def status_swap():
  await bot.change_presence(
      activity = discord.Activity(
          type = discord.ActivityType.watching,
          name = (next(status))
      )
  )

for filename in os.listdir('./Commands'):
    if filename.endswith('.py'):
        bot.load_extension(f'Commands.{filename[:-3]}')
bot.load_extension("Systems.levelsys")

if __name__ == "__main__":
  bot.run(os.getenv("DISCORD_TOKEN"))