import discord
from discord import utils
from discord.ext import commands
from core.classes import Cog_Extension


class 文字替代(Cog_Extension):

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not message.guild or not message.content:
            return
        if "cl3i" in message.content:
                ret = "好喔"
                webhooks = await message.channel.webhooks()
                webhook = utils.get(webhooks, name = "CC-OSV-NQN ")
                if webhook is None:
                    webhook = await message.channel.create_webhook(name = "CC-OSV-NQN ")

                await webhook.send(ret, username = message.author.nick, avatar_url = message.author.avatar_url, allowed_mentions=discord.AllowedMentions(everyone=False, users=False, roles=False, replied_user=False))
                await message.delete()
                await webhook.delete()
        if "c襖喔"  in message.content:
                ret = "好喔"
                webhooks = await message.channel.webhooks()
                webhook = utils.get(webhooks, name = "CC-OSV-NQN ")
                if webhook is None:
                    webhook = await message.channel.create_webhook(name = "CC-OSV-NQN ")

                await webhook.send(ret, username = message.author.nick, avatar_url = message.author.avatar_url, allowed_mentions=discord.AllowedMentions(everyone=False, users=False, roles=False, replied_user=False))
                await message.delete()
                await webhook.delete()
        if "CL3I"  in message.content:
                ret = "好喔"
                webhooks = await message.channel.webhooks()
                webhook = utils.get(webhooks, name = "CC-OSV-NQN ")
                if webhook is None:
                    webhook = await message.channel.create_webhook(name = "CC-OSV-NQN ")

                await webhook.send(ret, username = message.author.nick, avatar_url = message.author.avatar_url, allowed_mentions=discord.AllowedMentions(everyone=False, users=False, roles=False, replied_user=False))                  
                await message.delete() 
                await webhook.delete()
                
def setup(bot):
    bot.add_cog(文字替代(bot))