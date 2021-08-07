import discord
from discord.ext import commands
from Core.classes import Cog_Extension
import datetime, psutil, requests, json , os
from config import *
import requests



class Main(Cog_Extension):

    @commands.command(aliases=['weather'.casefold()])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _weather(self, ctx, *, location = None):
        if location == None:
            await ctx.send("請輸入位置。用法： `Cweather <地區>`")
            return
        def parse_weather_data(data):
                data = data['main']
                del data['humidity']
                del data['pressure']
                return data

        def 氣象_嵌入訊息(data, location):
                location = location.title()
                embed = discord.Embed(
                title = f"{location} 的氣象",
                description = f"這裡列出了今日 **{location}**的氣象。",
                color = 0x00FFFF
                )
                embed.add_field(
                name = f"**溫度**",
                value = f"`{str(data['temp'])}° C`",
                inline = True
                )
                embed.add_field(
                name = f"**最低溫度**",
                value = f"`{str(data['temp_min'])}° C`",
                inline = True
                )
                embed.add_field(
                name = f"**最高溫度**",
                value = f"`{str(data['temp_max'])}° C`",
                inline = True
                )
                embed.add_field(
                name = f"**體感溫度**",
                value = f"`{str(data['feels_like'])}° C`",
                inline = True
                )
                embed.set_footer(
                text = f'由{ctx.author}請求的鏈接✨'
                )
                return embed

        def error_message(location):
                location = location.title()
                return discord.Embed(
                title = f":warning: 錯誤！",
                description = f"查找**{location}**之天氣數據時發生錯誤。",
                color = ORANGE_COLOR
                )

        API_KEY = os.environ.get("WEATHER_API_KEY")
        URL = f"http://api.openweathermap.org/data/2.5/weather?q={location.lower()}&appid={API_KEY}&units=metric"
        try:
            data = json.loads(requests.get(URL).content)
            data = parse_weather_data(data)
            await ctx.send(embed = 氣象_嵌入訊息(data, location))
        except KeyError:
            await ctx.send(embed = error_message(location))



    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(aliases=['FTR'.casefold()])
    async def 翻譯(self, ctx, *, message = None):
        def dict_key_val_reverse(D):
            # 將字典的鍵-值互換，例: {'a': 1, 'b': 2}-> {1: 'a', 2: 'b'}
            return dict(zip(D.values(), D.keys()))

        def strConvert(s):
            restring = ""
            convertDict = dict(zip(range(33, 127), range(65281, 65375)))
            convertDict.update({32: 12288})
            convertDict = dict_key_val_reverse(convertDict)
            for uchar in s:
                u_code = ord(uchar)
                if u_code in convertDict:
                    u_code = convertDict[u_code]
                restring += chr(u_code)
            return restring

        if message is not None:
            message = strConvert(message)
            message = message + ' '
            message = message.replace(' ', '=')
            URL = f'https://www.google.com/inputtools/request?text={message}&ime=zh-hant-t-i0&cb=?'
            message = requests.post(url=URL)
            message = message.json()
            await ctx.send((message[1][0][1][0]))
        else:
            await ctx.send('欲翻譯之訊息不可為負')





    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(aliases=['covid'.casefold(), 'covid19'.casefold(), 'covid-19'.casefold()])
    async def _covid(self, ctx, *, countryName = None):
        try:
            if countryName is None:
                await ctx.send(f"你沒有輸入國家/地區名稱，請參照 - `Ccovid [country]` ")
            else:
                url = f"https://coronavirus-19-api.herokuapp.com/countries/{countryName.lower()}"
                stats = requests.get(url)
                json_stats = stats.json()
                country = json_stats["country"]
                totalCases = json_stats["cases"]
                todayCases = json_stats["todayCases"]
                totalDeaths = json_stats["deaths"]
                todayDeaths = json_stats["todayDeaths"]
                recovered = json_stats["recovered"]
                critical = json_stats["critical"]
                casesPerOneMillion = json_stats["casesPerOneMillion"]
                deathsPerOneMillion = json_stats["deathsPerOneMillion"]
                totalTests = json_stats["totalTests"]

                embed2 = discord.Embed(
                        title = f"{country}的 **COVID - 19 **疫情狀態", 
                        description = f"此信息並不總是實時的，因此可能不准確。", 
                        color =  0xFFA500
                )
                embed2.add_field(
                        name = f"總計確診數", 
                        value = f"{totalCases}", 
                        inline = True
                )
                embed2.add_field(
                        name = f"今天確診數", 
                        value = f"{todayCases}", 
                        inline = True
                )
                embed2.add_field(
                        name = f"總計死亡數", 
                        value = f"{totalDeaths}", 
                        inline = True
                )
                embed2.add_field(
                        name = f"今天死亡數", 
                        value = f"{todayDeaths}", 
                        inline = True
                )
                embed2.add_field(
                        name = f"已康復", 
                        value = f"{recovered}", 
                        inline = True
                )
                embed2.add_field(
                        name = f"重症", 
                        value = f"{critical}", 
                        inline = True
                )
                embed2.add_field(
                        name = f"病例/每百萬人", 
                        value = f"{casesPerOneMillion}", 
                        inline = True
                )
                embed2.add_field(
                        name = f"死亡數/每百萬人", 
                        value = f"{deathsPerOneMillion}", 
                        inline = True
                )
                embed2.add_field(
                        name = f"總計已檢測數", 
                        value = f"{totalTests}", 
                        inline = True
                )
                embed2.set_thumbnail(url = "https://cdn.discordapp.com/attachments/564520348821749766/701422183217365052/2Q.png")
                await ctx.send(embed = embed2)
        except:
            await ctx.send("無效的國家/地區名稱或 API 錯誤。 請再試一次。")

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(aliases=['embed'.casefold()])
    async def _embed(self, ctx, *, arg=None):
        async def send_error_msg():
            await ctx.send("無效args！正確的用法是 `Cembed <#hexcolor> , <標題> , <內容>`")

        if arg == None:
            await send_error_msg()
            return
        if arg.count(" , ") != 2:
            await send_error_msg()
            return

        try:
            args = arg.split(" , ")
            col = int(args[0][1:], 16)
            title = args[1]
            desc = args[2]
            embed = discord.Embed(
                title=title,
                description=desc,
                color=col
            )
            await ctx.send(embed=embed)
        except:
            await send_error_msg()

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name='join', aliases=['leave','volume','stop','skip','queue','remove','loop','play'])
    async def music(self, ctx: commands.Context):
      await ctx.send("我把音樂機器人功能刪掉ㄌ，欸嘿")



    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(aliases=['who'.casefold()])
    async def _who(self, ctx):
      await ctx.send("你是**{}**！".format(ctx.message.author))



    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(aliases=['message'.casefold(), 'msg'.casefold()])
    async def _messages(self, ctx):
        await ctx.send('正在計算訊息...')
        counter = 0
        counter2 = 0
        async for log in ctx.history(limit=100000): #如果該頻道訊息超過10w會出錯，可嘗試提高此數字
            counter2 += 1
            if log.author == ctx.message.author:
                counter += 1
        embed = discord.Embed(color=MAIN_COLOR)
        embed.add_field(name="成功計算！", value='你在{}則訊息中，發送了{}則訊息。這佔了其中{}%。'.format(counter2, counter, (counter * 100) // counter2))    
        embed.set_footer(text=f'由{ctx.author}請求的指令✨')
        await ctx.send(embed=embed)



    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(aliases=['python'.casefold(), 'botinfo'.casefold(), 'bot'.casefold()])
    async def _bot(self, ctx):
        values = psutil.virtual_memory()
        val2 = values.available * 0.001
        val3 = val2 * 0.001
        val4 = val3 * 0.001

        values2 = psutil.virtual_memory()
        value21 = values2.total
        values22 = value21 * 0.001
        values23 = values22 * 0.001
        values24 = values23 * 0.001

        embed = discord.Embed(
                title = "CC-OSV資訊", 
                color = 0x9370DB
        )
        embed.add_field(
                name = "延遲", 
                value = f"延遲 - {round(self.bot.latency * 1000)}ms", 
                inline = False
        )
        embed.add_field(
                name = '終端機統計數據', 
                value = f'CPU使用率 {psutil.cpu_percent(1)}%'
                             f'\n(實際的CPU使用率可能有些許差異)'
                             f'\n'

                             f'\nCPU邏輯核心數 - {psutil.cpu_count()} '
                             f'\nCPU物理核心數 - {psutil.cpu_count(logical=False)}'
                             f'\n'

                             f'\nRAM 總數 - {round(values24, 2)} GB'
                             f'\n可用的 RAM 數 - {round(val4, 2)} GB'
        )

        await ctx.send(embed=embed)



    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(aliases=['server'.casefold(), 'serverinfo'.casefold()])
    async def _serverinfo(self, ctx, *, name:str = ""):
        if name:
            server = None
            try:
                server = self.bot.get_guild(int(name))
                if not server:
                    return await ctx.send('找不到服務器 :satellite_orbital:')
            except:
                for i in self.bot.guilds:
                    if i.name.lower() == name.lower():
                        server = i
                        break
                if not server:
                    return await ctx.send("找不到服務器 :satellite_orbital: 或者也許我不在其中")
        else:
            server = ctx.guild
        # 計算在線成員數
        online = 0
        for i in server.members:
            if str(i.status) == 'online' or str(i.status) == 'idle' or str(i.status) == 'dnd':
                online += 1
        # 計算頻道數
        tchannel_count = len([x for x in server.channels if type(x) == discord.channel.TextChannel])
        vchannel_count = len([x for x in server.channels if type(x) == discord.channel.VoiceChannel])
        # 計算身分組數
        role_count = len(server.roles)

        # 定義嵌入訊息
        embed = discord.Embed(color=0x00CC99)
        embed.add_field(
                name = '國名', 
                value = f'`{server.name}`'
        )
        embed.add_field(
                name = '總統', 
                value = f'`桐生大學哲學碩士#6400`', 
                inline = False
        )
        embed.add_field(
                name = '國民數', 
                value = f'`{server.member_count-6}`',
                inline = True
        )
        embed.add_field(
                name = '表情符號數', 
                value = f'`60`',
                inline = True
        )
        embed.add_field(
                name = '文字頻道數', 
                value = f'`{tchannel_count}`',
                inline = True
        )
        embed.add_field(
                name = '語音頻道數', 
                value = f'`{vchannel_count}`',
                inline = True
        )
        embed.add_field(
                name = '驗證級別', 
                value = f'`無`',
                inline = True
        )
        embed.add_field(
                name = '身分組數', 
                value = f'`{role_count}`',
                inline = True
        )
        embed.add_field(
                name = '建立於', 
                value = f"`{server.created_at.__format__('%Y 4月20號 星期二 @ %H:%M:%S')}`", 
                inline = False
        )
        embed.set_thumbnail(url = server.icon_url)
        embed.set_footer(text = 'Server ID: %s' % server.id)

        try:
            await ctx.send(embed = embed)
        except Exception:
            await ctx.send("我沒有在這裡發送嵌入的權限 :disappointed_relieved:")
  


    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(aliases=['ping'.casefold()])
    async def _ping(self, ctx):
        ping = abs(
                int(
                    self.bot.latency*1000
                )
        )
        embed=discord.Embed(
                title = f'`{ping}(ms)`', 
                color = 0x73ff00, 
                timestamp = datetime.datetime.now(
                        datetime.timezone.utc
                )
        )
        embed.set_author(name = '延遲') 
        embed.set_footer(text = f'由{ctx.author}請求的指令✨')
        await ctx.send(embed = embed)



    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(aliases=['nitro'.casefold()])
    async def _Nitro(self, ctx):
        await ctx.message.delete()
        embed=discord.Embed(
                    title = '**Nitro Classic**', 
                    url = 'https://www.youtube.com/watch?v=rTgj1HxmUbg', 
                    description = 'Expires in 48 hours', 
                    color = 0x9089da
        )
        embed.set_author(name = 'A WILD GIFT APPEARS!')
        embed.set_thumbnail(url = 'https://i.imgur.com/yQyZ24F.png')
        await ctx.send(embed = embed)  



def setup(bot):
    bot.add_cog(Main(bot))