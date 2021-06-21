import discord
from discord.ext import commands
import json, os, keep_alive


with open('bot_info.json','r', encoding='utf8') as jfile:
    jdata = json.load(jfile) # 讀取設定檔
    
intents = discord.Intents.all() # 啟用所有 intents
bot = commands.Bot(command_prefix= jdata['Prefix'], owner_ids= jdata['Owner_id'], intents = intents)
bot.remove_command("help")

@bot.event
async def on_ready():
    print('CCBot已成功上線！')    



for filename in os.listdir('./cmds'):
    if filename.endswith('.py'):
        bot.load_extension(f'cmds.{filename[:-3]}')

if __name__ == "__main__":
  keep_alive.keep_alive()
  bot.run(jdata['TOKEN'])