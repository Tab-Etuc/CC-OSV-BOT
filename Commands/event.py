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
      if data.message_id == 858140566268411924:
          if str(data.emoji) == '<:E13:837971561725952020>': 
              guild = self.bot.get_guild(data.guild_id)
              role = guild.get_role(837975201915994153)
              await data.member.add_roles(role)
              await data.member.send(f"你已獲得進入紅燈區之通行證。")
          elif str(data.emoji) == '🌻':
              guild = self.bot.get_guild(data.guild_id)
              role = guild.get_role(863628692802240522)
              await data.member.add_roles(role)
              await data.member.send(f"你已獲得進入墓園之通行證。")
          elif str(data.emoji) == '🆙':
              guild = self.bot.get_guild(data.guild_id)
              role = guild.get_role(863629520719839242)
              await data.member.add_roles(role)
              await data.member.send(f"你已獲得進入練等專區之通行證。")
          elif str(data.emoji) == '🍔':
              guild = self.bot.get_guild(data.guild_id)
              role = guild.get_role(863630245630443551)
              await data.member.add_roles(role)
              await data.member.send(f"你已獲得進入晚餐揪揪群之通行證。")
          elif str(data.emoji) == '<:diamond:861185706336845834>':
              guild = self.bot.get_guild(data.guild_id)
              role = guild.get_role(863639159461773322)
              await data.member.add_roles(role)
              await data.member.send(f"你已獲得進入CC-OSV待辦事項區之通行證。")                            
      elif data.message_id == 858138565967085649:
          if str(data.emoji) == '<a:gif1:840492057009324073>': 
              guild = self.bot.get_guild(data.guild_id)
              role = guild.get_role(837968327014875177)
              await data.member.add_roles(role)
              await data.member.send(f"你已獲大同國民黨黨籍。")
          elif str(data.emoji) == '<a:c_star:858138565967085649>': 
              guild = self.bot.get_guild(data.guild_id)
              role = guild.get_role(860396953551634432)
              await data.member.add_roles(role)
              await data.member.send(f"你已獲星曌黨黨籍。")            
      elif data.message_id == 847029838546993163:
        if str(data.emoji) == '<a:emoji2:847026711064346655>':
            guild = self.bot.get_guild(data.guild_id)
            role = guild.get_role(846317257990733855)
            await data.member.add_roles(role)
            await data.member.send(f"你已成功變更名稱顏色。")
        elif str(data.emoji) == '<a:emoji1:847026710780051477>':
            guild = self.bot.get_guild(data.guild_id)
            role = guild.get_role(846317182577278998)
            await data.member.add_roles(role)
            await data.member.send(f"你已成功變更名稱顏色。")
      elif data.message_id == 847031310358544394:
        if str(data.emoji) == '<a:emoji1:847026710780051477>':
            guild = self.bot.get_guild(data.guild_id)
            role = guild.get_role(846317273244762142)
            await data.member.add_roles(role)
            await data.member.send(f"你已成功變更名稱顏色。")    
        elif str(data.emoji) == '<a:emoji2:847026711064346655>':
            guild = self.bot.get_guild(data.guild_id)
            role = guild.get_role(846317375346704445)
            await data.member.add_roles(role)
            await data.member.send(f"你已成功變更名稱顏色。")
      elif data.message_id == 847031700969095188:
        if str(data.emoji) == '<a:emoji1:847026710780051477>':
            guild = self.bot.get_guild(data.guild_id)
            role = guild.get_role(846317390551842846)
            await data.member.add_roles(role)
            await data.member.send(f"你已成功變更名稱顏色。")    
        elif str(data.emoji) == '<a:emoji2:847026711064346655>':
            guild = self.bot.get_guild(data.guild_id)
            role = guild.get_role(846317401469485116)
            await data.member.add_roles(role)
            await data.member.send(f"你已成功變更名稱顏色。")      
      elif data.message_id == 847033542990626816:
        if str(data.emoji) == '<a:emoji1:847026710780051477>':
            guild = self.bot.get_guild(data.guild_id)
            role = guild.get_role(846317443924361246)
            await data.member.add_roles(role)
            await data.member.send(f"你已成功變更名稱顏色。")    
        elif str(data.emoji) == '<a:emoji2:847026711064346655>':
            guild = self.bot.get_guild(data.guild_id)
            role = guild.get_role(846317486235582485)
            await data.member.add_roles(role)
            await data.member.send(f"你已成功變更名稱顏色。")      
        elif str(data.emoji) == '<a:emoji3:847026710850568243>':
            guild = self.bot.get_guild(data.guild_id)
            role = guild.get_role(846317533912891403)
            await data.member.add_roles(role)
            await data.member.send(f"你已成功變更名稱顏色。")
        elif str(data.emoji) == '<a:emoji4:847026711106420776>':
            guild = self.bot.get_guild(data.guild_id)
            role = guild.get_role(846317418540302416)
            await data.member.add_roles(role)
            await data.member.send(f"你已成功變更名稱顏色。")
        elif str(data.emoji) == '<a:emoji5:847026710842179585>':
            guild = self.bot.get_guild(data.guild_id)
            role = guild.get_role(846317429466595348)
            await data.member.add_roles(role)
            await data.member.send(f"你已成功變更名稱顏色。")    
      elif data.message_id == 858139579172651028:  
        if str(data.emoji) == '<a:756908393699999895:840493545034481684>':
            guild = self.bot.get_guild(data.guild_id)
            role = guild.get_role(853484122924515350)
            await data.member.add_roles(role)
            await data.member.send(f"你已成功入教。願蘿神保佑你。")
        elif str(data.emoji) == '<:E35:845572996089249792>':
            guild = self.bot.get_guild(data.guild_id)
            role = guild.get_role(858139056843915264)
            await data.member.add_roles(role)
            await data.member.send(f"你已入哲♂學會。")   
      elif data.message_id == 858160262606880818:  
        if str(data.emoji) == '<a:V_:858154997640331274>':
            guild = self.bot.get_guild(data.guild_id)
            role = guild.get_role(834430171171258417)
            await data.member.add_roles(role)
            await data.member.send(f"你已成功進入我國國境")

  @commands.Cog.listener()                
  async def on_raw_reaction_remove(self, data):
      if data.message_id in 添加身分組:
          if str(data.emoji) in 添加身分組[data.message_id][刪除]:
                guild = self.bot.get_guild(data.guild_id)
                user = await guild.fetch_member(data.user_id)
                role = guild.get_role(837975201915994153)
                await user.remove_roles(role)
                await user.send(f"123。")    
      elif data.message_id == 858140566268411924:
          if str(data.emoji) == '<:E13:837971561725952020>':
                guild = self.bot.get_guild(data.guild_id)
                user = await guild.fetch_member(data.user_id)
                role = guild.get_role(837975201915994153)
                await user.remove_roles(role)
                await user.send(f"你已被禁止進入紅燈區。")    
          elif str(data.emoji) == '🌻':
                guild = self.bot.get_guild(data.guild_id)
                user = await guild.fetch_member(data.user_id)
                role = guild.get_role(863628692802240522)
                await user.remove_roles(role)
                await user.send(f"你已被禁止進入墓園。")    
          elif str(data.emoji) == '🆙':
                guild = self.bot.get_guild(data.guild_id)
                user = await guild.fetch_member(data.user_id)
                role = guild.get_role(863629520719839242)
                await user.remove_roles(role)
                await user.send(f"你已被禁止進入練等專區。")    
          elif str(data.emoji) == '🍔':
                guild = self.bot.get_guild(data.guild_id)
                user = await guild.fetch_member(data.user_id)
                role = guild.get_role(863630245630443551)
                await user.remove_roles(role)
                await user.send(f"你已被禁止進入晚餐揪揪群。")    
          elif str(data.emoji) == '<:diamond:861185706336845834>':
                guild = self.bot.get_guild(data.guild_id)
                user = await guild.fetch_member(data.user_id)
                role = guild.get_role(863639159461773322)
                await user.remove_roles(role)
                await user.send(f"你已被禁止進入紅燈區。")                                                                    
      elif data.message_id == 858138565967085649:
            if str(data.emoji) == '<:gif1:840492057009324073>':
                guild = self.bot.get_guild(data.guild_id)
                user = await guild.fetch_member(data.user_id)
                role = guild.get_role(837968327014875177)
                await user.remove_roles(role)
                await user.send(f"你已退黨。")
            elif str(data.emoji) == '<:c_star:858138565967085649>':
                guild = self.bot.get_guild(data.guild_id)
                user = await guild.fetch_member(data.user_id)
                role = guild.get_role(860396953551634432)
                await user.remove_roles(role)
                await user.send(f"你已退黨。")                
      elif data.message_id == 847029838546993163:
                if str(data.emoji) == '<:emoji1:847026710780051477>':
                    guild = self.bot.get_guild(data.guild_id)
                    user = await guild.fetch_member(data.user_id)
                    role = guild.get_role(846317182577278998)
                    await user.remove_roles(role)
                    await user.send(f"你已成功移除名稱顏色。")
                elif str(data.emoji) == '<:emoji2:847026711064346655>':
                    guild = self.bot.get_guild(data.guild_id)
                    user = await guild.fetch_member(data.user_id)
                    role = guild.get_role(846317257990733855)
                    await user.remove_roles(role)
                    await user.send(f"你已成功移除名稱顏色。")   
      elif data.message_id == 847031310358544394:
                if str(data.emoji) == '<:emoji1:847026710780051477>':
                    guild = self.bot.get_guild(data.guild_id)
                    user = await guild.fetch_member(data.user_id)
                    role = guild.get_role(846317273244762142)
                    await user.remove_roles(role)
                    await user.send(f"你已成功移除名稱顏色。")
                elif str(data.emoji) == '<:emoji2:847026711064346655>':
                    guild = self.bot.get_guild(data.guild_id)
                    user = await guild.fetch_member(data.user_id)
                    role = guild.get_role(846317375346704445)
                    await user.remove_roles(role)
                    await user.send(f"你已成功移除名稱顏色。")     
      elif data.message_id == 847031700969095188:
                if str(data.emoji) == '<:emoji1:847026710780051477>':
                    guild = self.bot.get_guild(data.guild_id)
                    user = await guild.fetch_member(data.user_id)
                    role = guild.get_role(846317390551842846)
                    await user.remove_roles(role)
                    await user.send(f"你已成功移除名稱顏色。")
                elif str(data.emoji) == '<:emoji2:847026711064346655>':
                    guild = self.bot.get_guild(data.guild_id)
                    user = await guild.fetch_member(data.user_id)
                    role = guild.get_role(846317401469485116)
                    await user.remove_roles(role)
                    await user.send(f"你已成功移除名稱顏色。")  
      elif data.message_id == 847033542990626816:
                if str(data.emoji) == '<:emoji1:847026710780051477>':
                    guild = self.bot.get_guild(data.guild_id)
                    user = await guild.fetch_member(data.user_id)
                    role = guild.get_role(846317443924361246)
                    await user.remove_roles(role)
                    await user.send(f"你已成功移除名稱顏色。")
                elif str(data.emoji) == '<:emoji2:847026711064346655>':
                    guild = self.bot.get_guild(data.guild_id)
                    user = await guild.fetch_member(data.user_id)
                    role = guild.get_role(846317486235582485)
                    await user.remove_roles(role)
                    await user.send(f"你已成功移除名稱顏色。")  
                elif str(data.emoji) == '<:emoji3:847026710850568243>':
                    guild = self.bot.get_guild(data.guild_id)
                    user = await guild.fetch_member(data.user_id)
                    role = guild.get_role(846317533912891403)
                    await user.remove_roles(role)
                    await user.send(f"你已成功移除名稱顏色。")
                elif str(data.emoji) == '<:emoji4:847026711106420776>':
                    guild = self.bot.get_guild(data.guild_id)
                    user = await guild.fetch_member(data.user_id)
                    role = guild.get_role(846317418540302416)
                    await user.remove_roles(role)
                    await user.send(f"你已成功移除名稱顏色。")
                elif str(data.emoji) == '<:emoji5:847026710842179585>':
                    guild = self.bot.get_guild(data.guild_id)
                    user = await guild.fetch_member(data.user_id)
                    role = guild.get_role(846317429466595348)
                    await user.remove_roles(role)
                    await user.send(f"你已成功移除名稱顏色。")  
      elif data.message_id == 858139579172651028:  
        if str(data.emoji) == '<:756908393699999895:840493545034481684>':
            guild = self.bot.get_guild(data.guild_id)
            user = await guild.fetch_member(data.user_id)
            role = guild.get_role(853484122924515350)
            await user.remove_roles(role)
            await user.send(f"你已退教。")    
        elif str(data.emoji) == '<:E35:845572996089249792>':
            guild = self.bot.get_guild(data.guild_id)
            user = await guild.fetch_member(data.user_id)
            role = guild.get_role(858139056843915264)
            await user.remove_roles(role)
            await user.send(f"你已退會。")                

def setup(bot):
  bot.add_cog(Event(bot))