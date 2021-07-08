import discord
from discord.ext import commands
from core.classes import Cog_Extension, Global_Func
import json, asyncio, os
from config import *

with open('bot_info.json', 'r', encoding='utf8') as jfile:
   jdata = json.load(jfile)

class Owner(Cog_Extension):
  @commands.command(aliases=['cc'])
  @commands.has_permissions(administrator=True)
  async def clear(self, ctx, num: int, reason=None):
        '''清理指定數量訊息'''
        await ctx.channel.purge(limit=num + 1)
        
        levels = {
            "a": "非對應頻道內容",
            "b": "使用禁忌詞彙"
        }

        if reason is not None:
            if reason in levels.keys():
                await ctx.send(Global_Func.code(lang='fix', msg=f'已清理 {num} 則訊息.\nReason: {levels[reason]}'))
        else:
            await ctx.send(content=Global_Func.code(lang='fix', msg=f'已清理 {num} 則訊息.\nReason: {reason}'), delete_after=5.0)
            
  @commands.command()
  @commands.has_permissions(administrator=True)
  async def load(self, ctx, extension):
    '''裝載 Cog'''
    self.bot.load_extension(f'cmds.{extension}')
    await ctx.send(f'Loaded {extension} done.')

  @commands.command()
  @commands.has_permissions(administrator=True)
  async def unload(self, ctx, extension):
    '''卸載 Cog'''
    self.bot.unload_extension(f'cmds.{extension}')
    await ctx.send(f'Un - Loaded {extension} done.')

  @commands.command()
  @commands.has_permissions(administrator=True)
  async def reload(self, ctx, extension):
    '''重新裝載 Cog'''
    if extension == '*':
      for filename in os.listdir('./cmds'):
        if filename.endswith('.py'):
          self.bot.reload_extension(f'cmds.{filename[:-3]}')
      await ctx.send(f'Re - Loaded All done.')
    else:
      self.bot.reload_extension(f'cmds.{extension}')
      await ctx.send(f'Re - Loaded {extension} done.')

  @commands.command()
  @commands.has_permissions(administrator=True)
  async def shutdown(self, ctx):
    await ctx.send("Shutting down...")
    await asyncio.sleep(1)
    await self.bot.logout()

def setup(bot):
   bot.add_cog(Owner(bot))