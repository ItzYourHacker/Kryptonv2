from __future__ import annotations
from core import Astroz

#____________ Commands ___________

#####################3
#from .commands.Verification import Verification
from .commands.Own import Owner1
#from .commands.Embed import Embed
#from .commands.Afk import afk
#from .commands.Media import Media
from .commands.help import Help
from .commands.general import General
from .commands.moderation import Moderation
from .commands.anti import Security
from .commands.giveaway import Giveaways
from .commands.raidmode import Raidmode
from .commands.welcome import Welcomer
from .commands.premium import Premium
#from .commands.fun import Fun
from .commands.music import Music
from .commands.extra import Extra
from .commands.owner import Owner
from .commands.vcroles import Voice
from .commands.role import Server
from .commands.nsfw import Nsfw
from .commands.ignore import Ignore

from .commands.vcrole import Invcrole
#from .commands.logging import Logging
from .commands.AutoPfp import AutoPfp
#from .commands.ai import Ai
from .commands.selfrole import Selfroles
#____________ Events _____________
from .events.antiban import antiban
from .events.antichannel import antichannel
from .events.antiguild import antiguild
from .events.antirole import antirole
from .events.antibot import antibot
from .events.antikick import antikick
from .events.antiprune import antiprune
from .events.antiwebhook import antiwebhook
from .events.antiping import antipinginv
from .events.antiemostick import antiemostick
#from .events.antintegration import antintegration
from .events.autoblacklist import AutoBlacklist
from .events.antiemojid import antiemojid
from .events.antiemojiu import antiemojiu
from .events.Errors import Errors
from .events.on_guild import Guild
from .events.autorole import Autorole2
from .events.auto import Autorole
from .events.greet2 import greet
from .events.voiceupdate import Vcroles2
from .events.member_update import member_update
from .events.automodevent import automodevent








######################
from .dropdown.general import hacker1
from .dropdown.Moderation import hacker11
from .dropdown.music import hacker111
from .dropdown.raidmode import hacker1111
from .dropdown.anti1 import hacker11111
from .dropdown.welcomer import hacker111111
from .dropdown.loggingdrop import loggingdrop
from .dropdown.nsfw import hacker1111111
from .dropdown.voice import hacker11111111
from .dropdown.extra import hacker111111111

from .dropdown.hacker import Hacker121


#3###################################3




async def setup(bot: Astroz):
  
  await bot.add_cog(Help(bot))
  await bot.add_cog(General(bot))
  await bot.add_cog(Moderation(bot))
  await bot.add_cog(Security(bot))
 # await bot.add_cog(Giveaways(bot))
  await bot.add_cog(Raidmode(bot))
  await bot.add_cog(Welcomer(bot))
  await bot.add_cog(Owner1(bot))
  await bot.add_cog(Extra(bot))
  await bot.add_cog(Voice(bot))
  await bot.add_cog(Owner(bot))
  await bot.add_cog(Server(bot))
  await bot.add_cog(Nsfw(bot))
  

  await bot.add_cog(Premium(bot))
  await bot.add_cog(Ignore(bot))
  await bot.add_cog(Invcrole(bot))
 # await bot.add_cog(Logging(bot))
 # await bot.add_cog(afk(bot))
  await bot.add_cog(Selfroles(bot))
  await bot.add_cog(Music(bot))
  await bot.add_cog(AutoPfp(bot))
#  await bot.add_cog(Ai(bot))

  ####################




  ###########################events################3

  await bot.add_cog(antiban(bot))
  await bot.add_cog(antichannel(bot))
  await bot.add_cog(antiguild(bot))
  await bot.add_cog(antirole(bot))
  await bot.add_cog(antibot(bot))
  await bot.add_cog(antikick(bot))
  await bot.add_cog(antiprune(bot))
  await bot.add_cog(antiwebhook(bot))
  await bot.add_cog(antipinginv(bot))
  await bot.add_cog(antiemostick(bot))
  await bot.add_cog(automodevent(bot))
  await bot.add_cog(AutoBlacklist(bot))
  await bot.add_cog(antiemojid(bot))
  await bot.add_cog(antiemojiu(bot))
  await bot.add_cog(Guild(bot))
  await bot.add_cog(Errors(bot))
  await bot.add_cog(Autorole2(bot))
  await bot.add_cog(Autorole(bot))
  await bot.add_cog(greet(bot))
  await bot.add_cog(Vcroles2(bot))
 # await bot.add_cog(member_update(bot))
   
  
  

 
#########################
  await bot.add_cog(hacker1(bot))
  await bot.add_cog(hacker11(bot))
  await bot.add_cog(hacker111(bot))
  await bot.add_cog(hacker1111(bot))
  await bot.add_cog(hacker11111(bot))
  await bot.add_cog(hacker111111(bot))
 # await bot.add_cog(loggingdrop(bot))  
  await bot.add_cog(hacker1111111(bot))
  await bot.add_cog(hacker11111111(bot))
  await bot.add_cog(hacker111111111(bot))

  await bot.add_cog(Hacker121(bot))