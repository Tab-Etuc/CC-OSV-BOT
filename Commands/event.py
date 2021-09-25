from discord.ext import commands
from Core.classes import Cog_Extension, Gloable_Data
from Core.errors import Errors
import discord
from config import *



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
      try:   
        if data.message_id in 添加身分組:
          if str(data.emoji.id) in 添加身分組[data.message_id][str(data.emoji.id)+'Emoji']:
                guild = self.bot.get_guild(data.guild_id)
                user = await guild.fetch_member(data.user_id)
                role = guild.get_role(int(添加身分組[data.message_id][str(data.emoji.id)+'(role)']))
                await user.add_roles(role)
                await user.send(添加身分組[data.message_id][str(data.emoji.id) +'(Message_Add)'])    
      except KeyError:
           pass                   
      if data.message_id == 858140566268411924:
           if str(data.emoji) =='🌻':
                guild = self.bot.get_guild(data.guild_id)
                user = await guild.fetch_member(data.user_id)
                role = guild.get_role(863628692802240522)
                await user.add_roles(role)
                await user.send('您已獲得進入墓園之通行證。')    
           elif str(data.emoji) =='🆙':
                guild = self.bot.get_guild(data.guild_id)
                user = await guild.fetch_member(data.user_id)
                role = guild.get_role(863629520719839242)
                await user.add_roles(role)
                await user.send('您已獲得進入練等專區之通行證。')                    
           elif str(data.emoji) =='🍔':
                guild = self.bot.get_guild(data.guild_id)
                user = await guild.fetch_member(data.user_id)
                role = guild.get_role(863630245630443551)
                await user.add_roles(role)
                await user.send('您已獲得進入晚餐揪揪群之通行證。')   
      if data.message_id = 858160262606880818: 
            if str(data.emoji) == '858154997640331274':
                guild = self.bot.get_guild(data.guild_id)
                user = await guild.fetch_member(data.user_id)
                role = guild.get_role(863629520719839242)
                await user.add_roles(role)
                rol2 = guild.get_role(834430171171258417)
                await user.add_roles(rol2)
                await user.send('您已成功進入我國國境。')             


    @commands.Cog.listener()                
    async def on_raw_reaction_remove(self, data):
      try:        
        if data.message_id in 添加身分組:
            if str(data.emoji.id) in 添加身分組[data.message_id][str(data.emoji.id)+'Emoji']:
                guild = self.bot.get_guild(data.guild_id)
                user = await guild.fetch_member(data.user_id)
                role = guild.get_role(int(添加身分組[data.message_id][str(data.emoji.id)+'(role)']))
                await user.remove_roles(role)
                await user.send(添加身分組[data.message_id][str(data.emoji.id)+'(Message_Delete)']) 
      except KeyError:
           pass                      
      if data.message_id == 858140566268411924:
           if str(data.emoji) =='🌻':
                guild = self.bot.get_guild(data.guild_id)
                user = await guild.fetch_member(data.user_id)
                role = guild.get_role(863628692802240522)
                await user.remove_roles(role)
                await user.send('您已被禁止進入墓園。')    
           elif str(data.emoji) =='🆙':
                guild = self.bot.get_guild(data.guild_id)
                user = await guild.fetch_member(data.user_id)
                role = guild.get_role(863629520719839242)
                await user.remove_roles(role)
                await user.send('您已被禁止進入練等專區。')                    
           elif str(data.emoji) =='🍔':
                guild = self.bot.get_guild(data.guild_id)
                user = await guild.fetch_member(data.user_id)
                role = guild.get_role(863630245630443551)
                await user.remove_roles(role)
                await user.send('您已被禁止進入晚餐揪揪群。')          



def setup(bot):
  bot.add_cog(Event(bot))
