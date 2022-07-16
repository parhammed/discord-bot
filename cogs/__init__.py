from typing import TYPE_CHECKING
from .mod import ModCog
from .detail import DetailCog
from .role_reaction import RoleReactionCog
from .ticket import TicketCog

if TYPE_CHECKING:
    from classes import Bot


def setup(bot: "Bot"):
    bot.add_cog(ModCog(bot))
    bot.add_cog(DetailCog(bot))
    bot.add_cog(RoleReactionCog(bot))
    bot.add_cog(TicketCog(bot))
