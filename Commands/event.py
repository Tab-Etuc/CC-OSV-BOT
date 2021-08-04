from discord.ext import commands
from core.classes import Cog_Extension, Gloable_Data
from core.errors import Errors
import discord
from config import *
import googletrans

tr = googletrans.Translator()
DEFAULT_LANGUAGE = "zh-tw"

class Event(Cog_Extension):
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
          if str(data.emoji.id) in 添加身分組[data.message_id][str(data.emoji.id)+'Emoji']:
                guild = self.bot.get_guild(data.guild_id)
                user = await guild.fetch_member(data.user_id)
                role = guild.get_role(int(添加身分組[data.message_id][str(data.emoji.id)+'(role)']))
                await user.add_roles(role)
                await user.send(添加身分組[data.message_id][str(data.emoji.id) +'(Message_Add)'])    



    @commands.Cog.listener()                
    async def on_raw_reaction_remove(self, data):
        if data.message_id in 添加身分組:
            if str(data.emoji.id) in 添加身分組[data.message_id][str(data.emoji.id)+'Emoji']:
                guild = self.bot.get_guild(data.guild_id)
                user = await guild.fetch_member(data.user_id)
                role = guild.get_role(int(添加身分組[data.message_id][str(data.emoji.id)+'Role']))
                await user.remove_roles(role)
                await user.send(添加身分組[data.message_id][str(data.emoji.id)+'(Message_Delete)'])    



def setup(bot):
  bot.add_cog(Event(bot))
