from disnake.ext import commands
import disnake

from typing import TYPE_CHECKING
from classes import TicketMaker

context = disnake.CommandInteraction

if TYPE_CHECKING:
    context = commands.Context | disnake.CommandInteraction


class TicketCog(commands.Cog):
    @commands.cooldown(1, 30, commands.BucketType.guild)
    @commands.bot_has_guild_permissions(manage_channels=True)
    @commands.has_guild_permissions(manage_channels=True)
    async def add_ticket_maker(self, ctx: context, admin_role: disnake.Role, category: disnake.CategoryChannel):
        await ctx.channel.send(embed=disnake.Embed(title="برای ساخت تیکت روی دکمه زیر کلیک کنید", color=0x0000ff),
                               view=TicketMaker(admin_role, category))
        await ctx.send("تیکت ساز شما آمادس")

    prefix_add_ticket_maker = commands.Command(add_ticket_maker, brief="ساخت تیکت ساز")
    slash_add_ticket_make = commands.InvokableSlashCommand(add_ticket_maker, description="ساخت تیکت ساز", dm_permission=False)
