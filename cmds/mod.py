from discord.ext import commands
from core.classes import Cog_Extension, Global_Func
import json
from config import *
with open('bot_info.json', 'r', encoding='utf8') as jfile:
   jdata = json.load(jfile)

class Mod(Cog_Extension):
    @commands.command()
    async def who(self, ctx):
      '''說出你是誰'''
      await ctx.send("你是**{}**！".format(ctx.message.author))

    @commands.command(aliases=['msg'])
    async def messages(self, ctx):
        tmp = await ctx.send('正在計算訊息...')
        counter = 0
        counter2 = 0
        async for log in ctx.history(limit=50000):
            counter2 += 1
            if log.author == ctx.message.author:
                counter += 1

        await tmp.edit(content='你在{}則訊息中，發送了{}則訊息。這佔了其中{}%。'.format(counter2, counter, (counter * 100) // counter2))

def setup(bot):
   bot.add_cog(Mod(bot))