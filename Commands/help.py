import discord 
from discord.ext import commands 
from config import *
from disputils import BotEmbedPaginator, BotConfirmation, BotMultipleChoice
from help import *
from Core.classes import Cog_Extension

category_list = ""
total_cmds = 0
Supervisor_cmds = 9

for category in help_categories:
    total_cmds += len(category)

class HelpX(Cog_Extension):

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command()
    async def help(self, ctx, *, hmm_category = None):
        if hmm_category == None:
            embeds = [
                discord.Embed(
                    title = "此為前導介面",
                    description = f"""
使用下方表情符號切換頁數

**總計指令數：** {total_cmds}
**政府高層專用指令：** {Supervisor_cmds}


**上次更新內容：** 
{CHANGE_LOG}
""",
                    color = MAIN_COLOR
                ).set_author(name="CC-OSV 系統說明", url="https://youtube.com", icon_url="https://imgur.com/IrttPgS.png")
            ]

            i = 0

            for title in help_category_titles:
                embed=discord.Embed(
                    title=title,
                    description=f"更多詳細資訊：`Chelp {cmd_categories[i]}`",
                    color = MAIN_COLOR
                ).add_field(
                    name=f"Commands({len(help_categories[i])})",
                    value=help_emoji_categories[i]
                )
                if not ctx.channel.is_nsfw() and title == "🔞 • NSFW Commands (第 10 頁)":
                    pass
                else:
                    embeds.append(embed)

                i += 1

            paginator = BotEmbedPaginator(ctx, embeds)
            await paginator.run()
            return
        # checks if its a category uwu vote epicbot
        if hmm_category.lower() in cmd_categories:

            embed_description = ""

            i = 0

            for category_ in cmd_categories:
                if category_ == hmm_category.lower():
                    break
                i += 1

            for cmd in help_categories[i]:
                embed_description += f"`{cmd}` - {help_categories[i][cmd]}\n"

            if hmm_category.lower() == "nsfw" and not ctx.channel.is_nsfw():
                embed=discord.Embed(
                    title = "錯誤!",
                    description = "此指令只能使用在NFSW頻道",
                    color = RED_COLOR
                )
                await ctx.message.reply(embed=embed)
                return


            embed=discord.Embed(
                title = f"{hmm_category.lower().title()} 指令數：({len(help_categories[i])})",
                description=embed_description,
                color = MAIN_COLOR
            )

            await ctx.message.reply(embed=embed)
            return
        if hmm_category.lower() in all_cmds:
            if hmm_category.lower() in nsfw and not ctx.channel.is_nsfw():
                embed=discord.Embed(
                        title = "Go away horny!",
                        description = "This can only be used in a NSFW channel.",
                        color = RED_COLOR
                    )
                await ctx.message.reply(embed=embed)
                return

            embed=discord.Embed(
                title=f"{hmm_category.lower().title()}",
                description=f"""
**用法：** `C{all_cmds[hmm_category.lower()][2]}`
別名：{all_cmds[hmm_category.lower()][1]}

- {all_cmds[hmm_category.lower()][0]}
""",
                color=MAIN_COLOR
            )

            await ctx.message.reply(embed=embed)
            return

        else:

            embed=discord.Embed(
                title = "錯誤！",
                description = f"沒有這個類別 `{hmm_category}`",
                color = RED_COLOR
            )

            await ctx.message.reply(embed=embed)



def setup(bot):
    bot.add_cog(HelpX(bot))
