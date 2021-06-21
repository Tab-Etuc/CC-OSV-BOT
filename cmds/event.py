from discord.ext import commands
from core.classes import Cog_Extension, Gloable_Data
from core.errors import Errors
import json
import googletrans
import discord
import re


client = discord.Client()
tr = googletrans.Translator()
DEFAULT_LANGUAGE = "zh-tw"
LOGGING = False	

with open('bot_info.json', 'r', encoding='utf8') as jfile:
   jdata = json.load(jfile)

class Event(Cog_Extension):
  '''
  @commands.Cog.listener()
  async def on_message(self, message):
    try:
      if message.author == self.bot.user:
        # Dont respond to own messages
        return

      elif message.content == "[tr help]":
        print("Reached")
        # Help message
        HELP_MESSAGE =  "Syntax: [tr]\n"
        HELP_MESSAGE += "Arguments (optional): s (source language), d (destination language)\n\n"
        HELP_MESSAGE += "Example: [tr s=en d=fr] I am hungry.\n"
        HELP_MESSAGE += "Another Example: [tr] Tu es mon ami.\n\n"
        HELP_MESSAGE += "[tr languages] for a list of languages and codes"
        await message.reply(HELP_MESSAGE, mention_author=True)

      elif message.content == "[tr languages]":
        # List of languages
        output = "code: language\n\n"
        for key in googletrans.LANGUAGES:
          output += key
          output += ": "
          output += googletrans.LANGUAGES.get(key).capitalize()
          output += "\n"
        await message.reply(output, mention_author=False)

      elif (message.content.startswith('[tr ') and ']' in message.content) or message.content.startswith('[tr]'):
        # Split message into command and text
        end = message.content.index(']')
        args = message.content[1: end]
        text = message.content[end + 2:]

        # Check if text is valid (non empty)
        if text == None or text.isspace() or text == "":
          emb = discord.Embed(title="Error", description='Please include a message to translate. Use [tr help] for help.', color=0x00ff00)
          await message.reply(embed=emb, mention_author=False)
          return

        # Split command into arguments
        args = re.split(" |=", args)
        while "" in args: args.remove("")

        srcArg = False			# True if source language was provided

        # Check if source langauge given as argument, if not try to detect
        try:
          srcind = args.index("s")
          src = args[srcind + 1]
          srcArg = True
        except ValueError:
          src = tr.detect(text)
          src = src.lang
          if type(src) == list:
            src = src[0]
          src = src.lower()

        # Check if destination language given as argument, if not set to DEFAULT_LANGUAGE
        try:
          dstind = args.index("d")
          dst = args[dstind + 1]
          dstArg = True
        except ValueError:
          dst = DEFAULT_LANGUAGE

        # Check if source language is valid, if not send error
        if src in googletrans.LANGUAGES:
          srcLang = googletrans.LANGUAGES.get(src).capitalize()
        else:
          emb = discord.Embed(title="Error", description='Invalid Source Language.', color=0x00ff00)
          await message.reply(embed=emb, mention_author=False)
          return

        # Check if destination language is invalid, if yes send error
        if not dst in googletrans.LANGUAGES:
          emb = discord.Embed(title="Error", description='Invalid Destination Language.', color=0x00ff00)
          await message.reply(embed=emb, mention_author=False)
          return

        # Generate translation, log message details, then send message
        output = tr.translate(text, src=src, dest=dst)
        if LOGGING:
          print(src, "|", dst, "|", text, "|", output.text)

        emb = discord.Embed(title="Translated Text", description=output.text, color=0x00ff00)
        if not srcArg: emb.add_field(name="Source Language", value=src, inline=False)
        await message.reply(embed=emb, mention_author=False)
    except discord.errors.Forbidden:
      if LOGGING:
        print("Bot missing permissions in", message.channel)
  '''

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
      if data.message_id == 837974875875311628:
          if str(data.emoji) == '<:emoji_13:837971561725952020>': 
              guild = self.bot.get_guild(data.guild_id)
              role = guild.get_role(837975201915994153)
              await data.member.add_roles(role)
              await data.member.send(f"你已獲得進入紅燈區之通行證。")
      elif data.message_id == 837963992982880266:
          if str(data.emoji) == '<:emoji_7:835137032300003348>': 
              guild = self.bot.get_guild(data.guild_id)
              role = guild.get_role(834430171171258417)
              await data.member.add_roles(role)
              await data.member.send(f"你已取得普通公民身分，正式進入我國國境。")
      elif data.message_id == 837968124204679170:
          if str(data.emoji) == '<:emoji_7:835137032300003348>': 
              guild = self.bot.get_guild(data.guild_id)
              role = guild.get_role(837968327014875177)
              await data.member.add_roles(role)
              await data.member.send(f"你已獲大同國民黨黨籍。")
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
      elif data.message_id == 853487725276954625:  
        if str(data.emoji) == '<a:756908393699999895:840493545034481684>':
            guild = self.bot.get_guild(data.guild_id)
            role = guild.get_role(853484122924515350)
            await data.member.add_roles(role)
            await data.member.send(f"你已成功入教。願蘿神保佑你。")  
        
  @commands.Cog.listener()                
  async def on_raw_reaction_remove(self, data):
      if data.message_id == 837974875875311628:
          if str(data.emoji) == '<:emoji_13:837971561725952020>':
                guild = self.bot.get_guild(data.guild_id)
                user = await guild.fetch_member(data.user_id)
                role = guild.get_role(837975201915994153)
                await user.remove_roles(role)
                await user.send(f"你已被禁止進入紅燈區。")    
      elif data.message_id == 837963992982880266:
        if str(data.emoji) == '<:emoji_7:835137032300003348>':
                guild = self.bot.get_guild(data.guild_id)
                user = await guild.fetch_member(data.user_id)
                role = guild.get_role(834430171171258417)
                await user.remove_roles(role)
                await user.send(f"你已喪失普通公民身分，被驅逐我國國境。")
      elif data.message_id == 837968124204679170:
            if str(data.emoji) == '<:emoji_7:835137032300003348>':
                guild = self.bot.get_guild(data.guild_id)
                user = await guild.fetch_member(data.user_id)
                role = guild.get_role(837968327014875177)
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
      elif data.message_id == 853487725276954625:  
        if str(data.emoji) == '<:756908393699999895:840493545034481684>':
            guild = self.bot.get_guild(data.guild_id)
            user = await guild.fetch_member(data.user_id)
            role = guild.get_role(853484122924515350)
            await user.remove_roles(role)
            await user.send(f"你已退教。")    

def setup(bot):
  bot.add_cog(Event(bot))