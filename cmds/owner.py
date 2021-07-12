import discord 
from discord import Embed
from discord.ext import commands
from core.classes import Cog_Extension
import json, asyncio, os, re
from config import *

class Owner(Cog_Extension):
  def __init__(self, bot: commands.Bot):
        self.regex = re.compile(r"(\w*)\s*(?:```)(\w*)?([\s\S]*)(?:```$)")

  @property
  def session(self):
        return self.bot.http._HTTPClient__session

  async def _run_code(self, *, lang: str, code: str):
        res = await self.session.post(
            "https://emkc.org/api/v1/piston/execute",
            json={"language": lang, "source": code},
        )
        return await res.json()

  @commands.cooldown(1, 10, commands.BucketType.user)
  @commands.command()
  async def run(self, ctx: commands.Context, *, codeblock: str = None):
        if codeblock == None:
            await ctx.reply(embed = discord.Embed(
                title = "Incorrect Usage!",
                description = "Please use it like this: `e!run <codeblock>`",
                color = RED_COLOR))
            return
        matches = self.regex.findall(codeblock)
        if not matches:
            return await ctx.reply(
                embed=Embed(
                    title="Error!",
                    description="Please use codeblocks to run the code.",
                    color = RED_COLOR))
        lang = matches[0][0] or matches[0][1]
        if not lang:
            return await ctx.reply(
                embed=Embed(
                    title="Error!",
                    description="Please mention a language in your codeblock.",
                    color=RED_COLOR
                ).set_image(url="https://windows.is-super-sexy.xyz/15l759.png"))
        message = await ctx.reply("Executing your code... <a:loading:820988150813949982>")
        code = matches[0][2]
        result = await self._run_code(lang=lang, code=code)

        await self._send_result(message, result)

  async def _send_result(self, message, result: dict):
        if "message" in result:
            return await message.edit(
                embed=Embed(
                    title="Error!",
                    description=result["message"],
                    color=RED_COLOR),
                content="Pain.")
        output = result["output"]
        #        if len(output) > 2000:
        #            url = await create_guest_paste_bin(self.session, output)
        #            return await message.edit("Your output was too long, so here's the pastebin link " + url)
        embed = Embed(
            title=f"Ran your `{result['language']}` code",
            color=MAIN_COLOR)
        output = output[:500]
        shortened = len(output) > 500
        lines = output.splitlines()
        shortened = shortened or (len(lines) > 15)
        output = "\n".join(lines[:15])
        output += shortened * "\n\n**Output shortened**"
        if output == "":
            output = "<No output>"
        embed.add_field(name="Output", value=f"```{output}```")

        await message.edit(
            content="Done!",
            embed=embed)

  @commands.command(aliases=['cc'])
  @commands.has_permissions(administrator=True)
  async def clear(self, ctx, num: int, reason=None):
        '''清理指定數量訊息'''
        await ctx.channel.purge(limit=num + 1)
        
        levels = {
            "a": "非對應頻道內容",
            "b": "使用禁忌詞彙"
        }

        if reason is not None:
            if reason in levels.keys():
                await ctx.send(msg=f'已清理 {num} 則訊息.\nReason: {levels[reason]}')
        else:
            await ctx.send(msg=f'已清理 {num} 則訊息.\nReason: {reason}', delete_after=5.0)
            
  @commands.command()
  @commands.has_permissions(administrator=True)
  async def load(self, ctx, extension):
    self.bot.load_extension(f'cmds.{extension}')
    await ctx.send(f'Loaded {extension} done.')

  @commands.command()
  @commands.has_permissions(administrator=True)
  async def unload(self, ctx, extension):
    self.bot.unload_extension(f'cmds.{extension}')
    await ctx.send(f'Un - Loaded {extension} done.')

  @commands.command()
  @commands.has_permissions(administrator=True)
  async def reload(self, ctx, extension):
    if extension == '*':
      for filename in os.listdir('./cmds'):
        if filename.endswith('.py'):
          self.bot.reload_extension(f'cmds.{filename[:-3]}')
      await ctx.send(f'Re - Loaded All done.')
    else:
      self.bot.reload_extension(f'cmds.{extension}')
      await ctx.send(f'Re - Loaded {extension} done.')

  @commands.command()
  @commands.has_permissions(administrator=True)
  async def shutdown(self, ctx):
    await ctx.send("Shutting down...")
    await asyncio.sleep(1)
    await self.bot.logout()

def setup(bot):
   bot.add_cog(Owner(bot))