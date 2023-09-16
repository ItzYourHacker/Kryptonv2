import discord
from discord.ext import commands


class loggingdrop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """Security commands"""
  
    def help_custom(self):
		      emoji = '<:kryopton_logging:1102921522412261416>'
		      label = "Logging Commands"
		      description = "Show You Logging Commands"
		      return emoji, label, description

    @commands.group()
    async def __Logging__(self, ctx: commands.Context):
        """`msglog` , `memberlog` , `serverlog` , `channellog` , `rolelog` , `modlog`"""