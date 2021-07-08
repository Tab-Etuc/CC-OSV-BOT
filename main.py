import discord
from discord.ext import commands, tasks
import json, os
from dotenv import load_dotenv


load_dotenv()
TOKEN2 = os.getenv("DISCORD_TOKEN")

with open('bot_info.json','r', encoding='utf8') as jfile:
    jdata = json.load(jfile) # 讀取設定檔
    
intents = discord.Intents.all() # 啟用所有 intents
activity = discord.Game('[C] | Chelp 以資查詢')
bot = commands.Bot(command_prefix= jdata['Prefix'], owner_ids= jdata['Owner_id'], intents = intents)
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