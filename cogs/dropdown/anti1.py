import discord
from discord.ext import commands


class hacker11111(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """Security commands"""
  
    def help_custom(self):
		      emoji = '<:krypton_security:1108591905857622077>'
		      label = "Security Commands"
		      description = "Show You Security Commands"
		      return emoji, label, description

    @commands.group()
    async def __Security__(self, ctx: commands.Context):
        """`antinuke` , `antinuke enable` , `antinuke disable` , `antinuke antirole-create` , `antinuke antirole-delete` , `antinuke antirole-update` , `antinuke antichannel-create` , `antinuke antichannel-delete` , `antinuke antichannel-update` , `antinuke antiban` , `antinuke antikick` , `antinuke antiwebhook` , `antinuke antibot` , `antinuke antiserver` , `antinuke antiping` , `antiemoji-delete` , `antinuke antiemoji-create` , `antinuke antiemoji-update` , `antinuke antimemberrole-update` , `antinuke show` , `antinuke punishment set` , `antinuke whitelist add` , `antinuke whitelist remove` , `antinuke whitelist show` , `antinuke whitelist reset` , `antinuke channelclean` , `antinuke roleclean` , `antinuke owner add` , `antinuke owner remove` , `antinuke owner show` , `antinuke owner reset`"""

