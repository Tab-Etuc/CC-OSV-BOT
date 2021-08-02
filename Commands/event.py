from discord.ext import commands
from core.classes import Cog_Extension, Gloable_Data
from core.errors import Errors
import discord
from config import *
import googletrans

client = discord.Client()
tr = googletrans.Translator()
DEFAULT_LANGUAGE = "zh-tw"

class Event(Cog_Extension):
    
    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def tr(self,ctx, *,message=None):
        if ctx.message.author == self.bot.user:
            return
        if message is None:
            await ctx.send("請輸入欲翻譯之文字。參見：`Ctr [文字]`")
            return

        srcArg = False			# True if source language was provided
        dst = DEFAULT_LANGUAGE

        # Generate translation, log message details, then send message
        output = tr.translate(message, dest=dst)

        emb = discord.Embed(title="翻譯文字", description=output.text, color=MAIN_COLOR)
        await message.reply(embed=emb, mention_author=False)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        '''指令錯誤觸發事件'''
        Gloable_Data.errors_counter += 1
        error_command = '{0}_error'.format(ctx.command)
        if hasattr(Errors, error_command):  # 檢查是否有 Custom Error Handler
        error_cmd = getattr(Errors, error_command)
        await error_cmd(self, ctx, error)
        return
        else:  # 使用 Default Error Handler
        await Errors.default_error(self, ctx, error)
  


    @commands.Cog.listener()
    async def on_raw_reaction_add(self, data):
        if data.message_id in 添加身分組:
          if str(data.emoji) in 添加身分組[data.message_id]['表情符號(刪除)']:
                guild = self.bot.get_guild(data.guild_id)
                user = await guild.fetch_member(data.user_id)
                role = guild.get_role([data.message_id]['Role'])
                await user.remove_roles(role)
                await user.send([data.message_id]['訊息(加入)'])    



  @commands.Cog.listener()                
  async def on_raw_reaction_remove(self, data):
      if data.message_id in 添加身分組:
          if str(data.emoji) in 添加身分組[data.message_id]['表情符號(刪除)']:
                guild = self.bot.get_guild(data.guild_id)
                user = await guild.fetch_member(data.user_id)
                role = guild.get_role([data.message_id]['Role'])
                await user.remove_roles(role)
                await user.send([data.message_id]['訊息'])    



def setup(bot):
  bot.add_cog(Event(bot))