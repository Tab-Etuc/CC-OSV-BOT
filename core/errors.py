from discord.ext import commands
from core.classes import Logger
import json

with open('bot_info.json', 'r', encoding='utf8') as jfile:
   jdata = json.load(jfile)

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
    elif "is not found" in str(error):
        pass
    elif "error code: 50006" in str(error):
      pass
    elif "TypeError: object NoneType can't be used in 'await'" in str(error):
      pass
    elif "404 Not Found (error code: 10008): " in str(error):
      await ctx.send("Discord伺服器端錯誤，本次操作未成功。")
    elif "could not be loaded." in str(error):
      await ctx.send("查無此檔案，請確認輸入是否正確。")
    elif "has not been loaded." in str(error):
      await ctx.send("此檔案並無讀取，請確認輸入是否正確。")
    # 皆不符合
    else:
      await ctx.send(f'發生未知錯誤: {error}')
      Logger.log(self, ctx, error)
