from discord.ext import commands
import discord
from Core.classes import Logger
from config import *

class Errors():
	# 自訂 Error Handler
  ''' #Main.sayd 的指令錯誤處理
	@Main.sayd.error
	async def sayd_error(self, ctx, error):
		
		if isinstance(error, commands.MissingRequiredArgument):
			err = str(error).split(" ")[0]
			await ctx.send(f"遺失必要參數： <`{err}`>")
			await ctx.send_help(ctx.command)
			Logger.log(self, ctx, error)
	'''
  # 預設 Error Handler
  async def default_error(self, ctx, error):
    '''預設錯誤處理'''
      
    # 比對觸發的error是否為 MissingRequiredArgument 的實例
    if isinstance(error, commands.MissingRequiredArgument):
      err = str(error).split(" ")[0]
      await ctx.send(f"遺失必要參數： <`{err}`>")
      await ctx.send_help(ctx.command)
      Logger.log(self, ctx, error)
      
    # error 內容是否為 403 Forbiddden
    elif "403 Forbidden" in str(error): 
      await ctx.send("403 Forbidden，請檢查 Bot 權限")
      Logger.log(self, ctx, error)
    elif "TypeError: object NoneType can't be used in 'await'" in str(error):
      pass
    elif "404 Not Found (error code: 10008): " in str(error):
      embed=discord.Embed(title=":warning: 錯誤！", description=f"Discord伺服器端錯誤，本次操作未成功。", color=ORANGE_COLOR)
      await ctx.send(embed=embed)
    elif "could not be loaded." in str(error):
      embed=discord.Embed(title=":warning: 錯誤！", description=f"查無此檔案，請確認輸入是否正確。", color=ORANGE_COLOR)
      await ctx.send(embed=embed)
    elif "has not been loaded." in str(error):
      embed=discord.Embed(title=":warning: 錯誤！", description=f"查無此檔案，請確認輸入是否正確。", color=ORANGE_COLOR)
      await ctx.send(embed=embed)
    elif "You are missing Administrator permission(s) to run this command." in str(error):
      embed=discord.Embed(title=":warning: 錯誤！", description=f"此指令僅有政府高層得以用之。", color=ORANGE_COLOR)
      await ctx.send(embed=embed)
    elif "You do not own this bot." in str(error):
      embed=discord.Embed(title=":warning: 錯誤！", description=f"此指令僅有政府高層得以用之。", color=ORANGE_COLOR)
      await ctx.send(embed=embed)
    elif "You are on cooldown. Try again in "in str(error):
      embed=discord.Embed(title=":warning: 錯誤！", description="指令還在冷卻中！請於%.2f秒後再次嘗試。"% error.retry_after, color=ORANGE_COLOR)
      await ctx.send(embed=embed)
    elif "is not found"in str(error):
      pass

      
    # 皆不符合
    else:
      embed=discord.Embed(title=":warning: 錯誤！", description=f"{error}", color=ORANGE_COLOR)
      await ctx.send(embed=embed)
      Logger.log(self, ctx, error)
