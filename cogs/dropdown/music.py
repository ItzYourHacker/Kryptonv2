import discord
from discord.ext import commands


class hacker111(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """Security commands"""
  
    def help_custom(self):
		      emoji = '<:krypton_music:1108591693722300506>'
		      label = "Music Commands"
		      description = "Show You Music Commands"
		      return emoji, label, description

    @commands.group()
    async def __Music__(self, ctx: commands.Context):
        """`play` , `nowplaying` , `shuffle` , `replay` , `loop` , `moveto` , `stop`, `pause` , `resume` , `skip` , `disconnect` , `seek` , `volume` , `forcefix` , `bassboost enable` , `bassboost disable` , `filter` , `filter daycore enable` , `filter daycore disable` , `filter 8d enable` , `filter 8d disable` , `filter damon enable` , `filter damon disable` , `filter slowmode enable` , `filter slowmode disable` , `filter lofi enable` , `filter lofi disable` , `filter nightcore enable` , `filter nightcore disable` , `filter 121 enable` , `filter 121 disable`"""