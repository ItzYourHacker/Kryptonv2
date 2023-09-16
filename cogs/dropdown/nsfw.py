import discord
from discord.ext import commands


class hacker1111111(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """Security commands"""
  
    def help_custom(self):
		      emoji = '<:krypton_nsfw:1108592050724683828>'
		      label = "Nsfw Commands"
		      description = "Show You Nsfw Commands"
		      return emoji, label, description

    @commands.group()
    async def __Nsfw__(self, ctx: commands.Context):
        """`nsfw` , `nsfw 4k` , `nsfw pussy` , `nsfw boobs` , `nsfw lewd` , `nsfw lesbian` , `nsfw blowjob` , `nsfw cum` , `nsfw gasm` , `nsfw hentai` , `nsfw anal` , `nsfw gonewild` , `nsfw hanal` , `nsfw holo`  , `nsfw neko` , `nsfw hneko` , `nsfw hkitsune` , `nsfw kemonomimi` , `nsfw pgif` , `nsfw kanna` , `nsfw thigh` , `nsfw hthigh` , `nsfw paizuri` , `nsfw tentacle` , `nsfw hboobs` , `nsfw yaoi` , `nsfw hmidriff` , `nsfw hass` , `nsfw randomnsfw` , `nsfw n`"""