import discord
from discord.ext import commands

class Music(commands.Cog):
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name='join', aliases=['leave','volume','stop','skip','queue','remove','loop','play'])
    async def all(self, ctx: commands.Context):
      await ctx.send("我把音樂機器人功能刪掉ㄌ，欸嘿")

def setup(bot):
   bot.add_cog(Music(bot))
