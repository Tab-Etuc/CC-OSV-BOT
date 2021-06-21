from discord.ext import commands
from core.classes import Cog_Extension
import asyncio
import pandas as pd
from config import *

class Task(Cog_Extension):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    async def interval():
      await self.bot.wait_until_ready()
      while not self.bot.is_closed():
        df = pd.read_csv('accounts.csv')
        df['Balance'] *= df['課稅']
        df.to_csv('accounts.csv', index=False)
        print('已進行例行性的課稅')
        await asyncio.sleep(7200)
    self.bg_task = self.bot.loop.create_task(interval())
  
  @commands.command()
  @commands.is_owner()
  async def 課稅(self, ctx):
    df = pd.read_csv('accounts.csv')
    df['Balance'] *= df['課稅']
    df.to_csv('accounts.csv', index=False)

def setup(bot):
   bot.add_cog(Task(bot))