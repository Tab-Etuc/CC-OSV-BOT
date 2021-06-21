import discord
import requests
from discord.ext import commands
from config import *

class Other(commands.Cog):
    def __init__(self, client):
        self.client = client
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(aliases = ['covid-19', 'covid19'])
    async def covid(self, ctx, *, countryName = None):
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
                active = json_stats["active"]
                critical = json_stats["critical"]
                casesPerOneMillion = json_stats["casesPerOneMillion"]
                deathsPerOneMillion = json_stats["deathsPerOneMillion"]
                totalTests = json_stats["totalTests"]
                testsPerOneMillion = json_stats["testsPerOneMillion"]


                embed2 = discord.Embed(title = f"{country}的 **COVID - 19 **疫情狀態", description = f"此信息並不總是實時的，因此可能不准確。", color =  0xFFA500)
                embed2.add_field(name = f"總計確診數", value = f"{totalCases}", inline = True)
                embed2.add_field(name = f"今天確診數", value = f"{todayCases}", inline = True)
                embed2.add_field(name = f"總計死亡數", value = f"{totalDeaths}", inline = True)
                embed2.add_field(name = f"今天死亡數", value = f"{todayDeaths}", inline = True)
                embed2.add_field(name = f"已康復", value = f"{recovered}", inline = True)
                embed2.add_field(name = f"重症", value = f"{critical}", inline = True)
                embed2.add_field(name = f"病例/每百萬人", value = f"{casesPerOneMillion}", inline = True)
                embed2.add_field(name = f"死亡數/每百萬人", value = f"{deathsPerOneMillion}", inline = True)
                embed2.add_field(name = f"總計已檢測數", value = f"{totalTests}", inline = True)
                embed2.set_thumbnail(url = "https://cdn.discordapp.com/attachments/564520348821749766/701422183217365052/2Q.png")
                await ctx.send(embed = embed2)
        except:
            await ctx.send("無效的國家/地區名稱或 API 錯誤。 請再試一次。")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def embed(self, ctx, *, arg=None):
        async def send_error_msg():
            await ctx.send("Invalid args! Correct usage is `e!embed <#hexcolor> | <title> | <description>`")

        if arg == None:
            await send_error_msg()
            return
        if arg.count(" | ") != 2:
            await send_error_msg()
            return

        try:
            args = arg.split(" | ")
            col = int(args[0][1:], 16)
            title = args[1]
            desc = args[2]
            e = discord.Embed(
                title=title,
                description=desc,
                color=col
            )
            await ctx.send(embed=e)
        except:
            await send_error_msg()



def setup(client):
    client.add_cog(Other(client))
