import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from config import *


load_dotenv()
TOKEN2 = os.getenv("DISCORD_TOKEN")

    
intents = discord.Intents.all() # 啟用所有 intents
activity = discord.Game('[C] | Chelp 以資查詢')
bot = commands.Bot(command_prefix=Prefix, owner_ids=Owner_id, intents = intents)
bot.remove_command("help")


@bot.event
async def on_ready():
  await bot.change_presence(activity=discord.Game(activity))
  print('CCBot已成功上線！')
    


for filename in os.listdir('./cmds'):
    if filename.endswith('.py'):
        bot.load_extension(f'cmds.{filename[:-3]}')

if __name__ == "__main__":
  bot.run(TOKEN2)