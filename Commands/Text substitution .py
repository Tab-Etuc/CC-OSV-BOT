import discord
from discord import utils
from discord.ext import commands
from Core.classes import Cog_Extension


class Text(Cog_Extension):

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not message.guild or not message.content:
            return
        if "cl3i" in message.content or "c襖喔" in message.content or "CL3I" in message.content:
                webhooks = await message.channel.webhooks()
                webhook = utils.get(
                        webhooks, 
                        name = "CC-OSV-NQN "
                )
                if webhook is None:
                    webhook = await message.channel.create_webhook(name = "CC-OSV-NQN ")

                await webhook.send(
                        '好喔', 
                        username = message.author.nick, 
                        avatar_url = message.author.avatar_url, 
                        allowed_mentions = discord.AllowedMentions(
                                everyone = False, 
                                users = False, 
                                roles = False, 
                                replied_user = False
                        )
                )
                await message.delete()
                await webhook.delete()


                
def setup(bot):
    bot.add_cog(Text(bot))