import discord
from discord.ext import commands
from core.classes import Cog_Extension
import json

with open('bot_info.json','r', encoding='utf8') as jfile:
    jdata = json.load(jfile) # 讀取設定檔

class Help(Cog_Extension):
  @commands.command(name='helpX', aliases=['hX'])
  async def helpX(self, ctx, arg: str=''):
        """Display help"""
        embed = discord.Embed(colour=discord.Colour(0xff3d33))

        avatar_url = str(self.bot.user.avatar_url)
        embed.set_thumbnail(url=avatar_url)
        embed.set_author(name="CC-OSV 系統說明", url="https://youtube.com", icon_url=avatar_url)
        embed.set_footer(text=f'由{ctx.author}請求的鏈接✨')

        if arg.strip().lower() == '-a':
           # Short version
            embed.title = '這是所有命令及其用途的列表'
            embed.description = '請使用前綴 `C`\n輸入`$help -指令` 得到更進階的說明(ex.`$help 2048`)\n請注意輸入正確文字及大小寫。\n註：`help|h`表`help`也可以別名`h`代替。'
            with open('help.json', 'r') as help_file:
                data = json.load(help_file)
            data = data['full']
            for key in data:
                value = '\n'.join(x for x in data[key])
                embed.add_field(name=key, value=f"```{value}```", inline=False)
        elif arg.strip().lower() == 'bank':
          embed.title = 'Bank'
          embed.description = '查看銀行餘額\n用法有二：\n`Cbank` - 查看自身餘額。\n`Cbank @提及某人` - 查看@提及之人餘額。'
        elif arg.strip().lower() == 'register':
          embed.title = 'Register'
          embed.description = '銀行開戶\n別名：`register`, `reg`, `開戶`\n用法：\n`Cregister` - 開戶。'
        elif arg.strip().lower() == 'reg':
          embed.title = 'Register'
          embed.description = '銀行開戶\n別名：`register`, `reg`, `開戶`\n用法：\n`Cregister` - 開戶。'
        elif arg.strip().lower() == '開戶':
          embed.title = 'Register'
          embed.description = '銀行開戶\n別名：`register`, `reg`, `開戶`\n用法：\n`Cregister` - 開戶。'          
        elif arg.strip().lower() == 'pay':
          embed.title = 'Pay'
          embed.description = '轉帳\n用法：\n`Cpay @提及某人 金額` - 轉帳該金額予 @此人。'  
        elif arg.strip().lower() == 'salary':
          embed.title = 'Salary'
          embed.description = '薪資表\n別名：`salary`, `SY`, `薪水`\n用法：\n`Csalary` - 展示本國各公職薪資表。'     
        elif arg.strip().lower() == 'SY':
          embed.title = 'Salary'
          embed.description = '薪資表\n別名：`salary`, `SY`, `薪水`\n用法：\n`Csalary` - 展示本國各公職薪資表。'   
        elif arg.strip().lower() == '薪資':
          embed.title = 'Salary'
          embed.description = '薪資表\n別名：`salary`, `SY`, `薪水`\n用法：\n`Csalary` - 展示本國各公職薪資表。'    
        elif arg.strip().lower() == 'count':
          embed.title = 'Count'
          embed.description = '已開戶人數\n用法：\n`Ccount` - 展示已於簡明銀行開戶人數。'   
        elif arg.strip().lower() == 'top':
          embed.title = 'Top'
          embed.description = '排行榜\n用法：\n`Ctop` - 顯示本銀行前五名富豪。'           
        elif arg.strip().lower() == 'help':
          embed.title = 'Help'
          embed.description = '幫助欄\n別名：`help`, `h`, `menu`, `m`\n用法有三：\n`Chelp` - 展示幫助總表。\n`Chelp -a` -展示幫助概覽。\n`Chelp 指令` - 展示該指令進階說明。 '   
        elif arg.strip().lower() == 'who':
          embed.title = 'Who'
          embed.description = '~~幫助失智老人~~\n用法：\n`Cwho` - 說出你是誰。'  
        elif arg.strip().lower() == 'messages':
          embed.title = 'Messages'
          embed.description = '訊息統計\n別名：`messages`, `msg`\n用法：\n`Cmessages` - 計算你在該頻道傳送之訊息佔比。' 
        elif arg.strip().lower() == 'server':
          embed.title = 'Server'
          embed.description = '伺服器資訊\n用法：\n`Cserver` - 顯示伺服器資訊。'       
        elif arg.strip().lower() == 'user':
          embed.title = 'User'
          embed.description = '用戶資訊\n用法：\n`Cuser` - 顯示用戶資訊。'                       
        elif arg.strip().lower() == 'ping':
          embed.title = 'Ping'
          embed.description = 'BOT延遲\n用法：\n`Cping` - 顯示BOT延遲。'  
        elif arg.strip().lower() == 'Nitro':
          embed.title = 'Nitro'
          embed.description = '假訊息\n用法：\n`CNitro` - 發送一個Disocrd Nitro 免費領取的假連結。' 
        elif arg.strip().lower() == 'wiki':
          embed.title = 'Wiki'
          embed.description = '維基百科\n用法：\n`Cwiki 關鍵字` - 於維基百科查詢`關鍵字`' 
        elif arg.strip().lower() == 'google':
          embed.title = 'Google'
          embed.description = '用法：\n`Cgoogle 關鍵字` - 於GOOGLE查詢`關鍵字`'     
        elif arg.strip().lower() == 'numgame':
          embed.title = 'Numgame'
          embed.description = '數字遊戲\n\n別名：`numgame`, `num`, `nungame`\n用法：\n`Cnumgame` - 開始一局數字遊戲。\n\n**遊戲玩法**：\n當遊戲開始時，輸入1~100間的整數\n當數字非正確答案，將會提示\n`數字再高點...`或`數字再低點...`等字眼\n玩家若在六個數字內未猜到答案則遊戲失敗\n而在1~6個數字內猜到答案者，鼓勵分別為\n`10000,9900,8750,7600,6450, 5300`簡明幣。'  
        elif arg.strip().lower() == 'rob':
          embed.title = 'Rob'
          embed.description = '賭博\n用法有二：\n`Crob 金額` - 賭博`金額`金額越高失敗率越高，伴隨而來的也是巨量的財富。\n`Csrob` - 用最大上限的金額賭博。' 
        elif arg.strip().lower() == 'roulette':
          embed.title = 'Roulette'
          embed.description = '輪盤\n別名：`roulette`, `RL`, `輪盤`\n用法：`Croulette`\n\n**遊戲玩法：**\n輪盤共有七個格子\n僅有轉到唯有的一個將能使玩家餘額翻六倍\n反之則將餘額歸零。'     
        elif arg.strip().lower() == '2048':
          embed.title = '2048'
          embed.description = '遊玩2048\n用法：\n`C2048` - 開始一場2048遊戲\n\n**遊戲玩法：**\n該遊戲使用方向鍵(表情符號)讓方塊整體上下左右移動。\n 如果兩個帶有相同數字的方塊在移動中碰撞，則它們會合併為一個方塊，且所帶數字變為兩者之和。\n每次移動時，會有一個值為2或者4的新方塊出現，所出現的數字都是2的冪。\n當值為2048的方塊出現時，遊戲即勝利，該遊戲因此得名。  '     
        elif arg.strip().lower() == '8ball':
          embed.title = '8ball'
          embed.description = '八號球\n用法：\n`C8ball 問句` - 詢問8ball問題\n\n**遊戲玩法：**\n神奇八號球（Magic 8 ball）是一種用來玩占卜的玩具，外型就跟撞球的黑色八號球一樣，會有20種內建的預設答案，是西方人在派對中時常會玩到的打趣小玩具，甚至連日常生活裡的大小事也可以問它。(截自優秀ㄉ網路)'
        elif arg.strip().lower() == 'minesweeper':
          embed.title = 'Minesweeper'
          embed.description = '踩地雷\n用法：\n`Cminesweeper` - 開始一場踩地雷遊戲。\n\n**遊戲玩法：**\n找出所有沒有地雷的方格，完成遊戲；要是按了有地雷的方格，則遊戲失敗。'      
        elif arg.strip().lower() == 'rps':
          embed.title = 'RPS'
          embed.description = '剪刀、石頭、布\n用法：\n`Crps` - 開始一場猜拳遊戲。\n\n**遊戲玩法：**\n使用表情符號石頭、布、剪刀和BOT進行猜拳。'
        elif arg.strip().lower() == 'toss':
          embed.title = 'TOSS'
          embed.description = '擲硬幣\n用法：\n`Ctoss` - 擲硬幣。'      
        elif arg.strip().lower() == 'ttt':
          embed.title = 'TTT'
          embed.description = '遊玩井字旗\n用法：\n`Cttt` - 開始一場井字旗遊戲。\n輸入`數字,數字`可在該座標上下棋。\n`e.g.3,3 即在右下角下棋。\n`ps.不會有超過3的數字，畢竟格子也才3乘3`\n\n**遊戲玩法：**\n兩個玩家，一個打圈(◯)，一個打叉（✗），輪流在3乘3的格上打自己的符號，最先以橫、直、斜連成一線則為勝。如果雙方都下得正確無誤，將得和局。'    
        elif arg.strip().lower() == 'wumpus':
          embed.title = 'Wumpus'
          embed.description = 'wumpus\n用法：\n`Cwumpus` - 開始一場wumpus遊戲。\n\n**遊戲玩法：**\n參見https://zh.wikipedia.org/wiki/Hunt_the_Wumpus 。'                     
        else:
            # Full version
            embed.title = '這是所有命令及其用途的列表'
            embed.description = '請使用前綴 `C`\n輸入`Chelp -a`得到概覽訊息。\n輸入`Chelp -指令` 得到更進階的說明(ex.`Chelp 2048`)\n請注意輸入正確文字及大小寫。 '
            with open('help.json', 'r') as help_file:
                data = json.load(help_file)
            data = data['short']
            for key in data:
                embed.add_field(name=key, value=data[key])
        try:
            await ctx.send(embed=embed)
        except Exception:
            await ctx.send("我無權在此處發送嵌入內容 :disappointed_relieved: ")

def setup(bot):
    bot.add_cog(Help(bot))