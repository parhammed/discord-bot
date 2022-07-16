from typing import TYPE_CHECKING

from disnake.ext import commands
import disnake

from utils import check_access

context = disnake.CommandInteraction
if TYPE_CHECKING:
    from classes import Bot

    context = commands.Context | disnake.CommandInteraction


class ModCog(commands.Cog):
    def __init__(self, bot: "Bot"):
        self._bot: "Bot" = bot

    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.bot_has_guild_permissions(kick_members=True)
    @commands.has_guild_permissions(kick_members=True)
    async def kick(self, ctx: context, member: disnake.Member, *, reason: str = ''):
        check_access(member, ctx.author, ctx.guild.me, ctx.guild.owner_id)
        await member.kick(reason=f"{reason} by {ctx.author.name}#{ctx.author.discriminator}")

        await ctx.send(f"باموفقیت {member.name}#{member.discriminator} از سرور بیرون انداخته شد")

    prefix_kick = commands.Command(kick, brief="کیک کردن ممبر", usage="t!kick <member> [reason]")
    slash_kick = commands.InvokableSlashCommand(kick, description="کیک کردن ممبر", dm_permission=False)

    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.bot_has_guild_permissions(ban_members=True)
    @commands.has_guild_permissions(ban_members=True)
    async def ban(self, ctx: context, member: disnake.Member, *, reason: str = ''):
        check_access(member, ctx.author, ctx.guild.me, ctx.guild.owner_id)
        await member.ban(reason=f"{reason} by {ctx.author.name}#{ctx.author.discriminator}")

        await ctx.send(f"باموفقیت {member.name}#{member.discriminator} از سرور  بن شد")

    prefix_ban = commands.Command(ban, brief="بن کردن ممبر", usage="t!ban <member> [reason]")
    slash_ban = commands.InvokableSlashCommand(ban, description="بن کردن ممبر", dm_permission=False)

    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.bot_has_guild_permissions(ban_members=True)
    @commands.has_guild_permissions(ban_members=True)
    async def unban(self, ctx: context, user: disnake.User, *, reason: str = ''):
        try:
            ban = await ctx.guild.fetch_ban(user)
        except disnake.NotFound:
            await ctx.send(f"متاسفانه {user.id} بین افراد بن شده یافت نشد")
            return

        await ctx.guild.unban(user, reason=f"{reason} by {ctx.author.name}#{ctx.author.discriminator}")
        await ctx.send(f"باموفقیت {ban.user.name}#{ban.user.discriminator} از سرور  آنبن شد")

    prefix_unban = commands.Command(unban, brief="آنبن کردن ممبر", usage="t!unban <user_id> [reason]")
    slash_unban = commands.InvokableSlashCommand(unban, description="آنبن کردن ممبر", dm_permission=False)

    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.bot_has_guild_permissions(moderate_members=True)
    @commands.has_guild_permissions(moderate_members=True)
    async def timeout(self, ctx: context, member: disnake.Member, duration: float, *, reason: str = ''):
        check_access(member, ctx.author, ctx.guild.me, ctx.guild.owner_id)
        if duration <= 0:
            await ctx.send(f"متاسفانه duration باید بیشتر از 0 باشد")
            return

        await member.timeout(duration=duration, reason=f"{reason} by {ctx.author.name}#{ctx.author.discriminator}")
        await ctx.send(f"باموفقیت {member.name}#{member.discriminator} تایم اوت شد")

    prefix_timeout = commands.Command(timeout, brief="تایم اوت کردن ممبر", usage="t!timeout <user_id> <duration> [reason]")
    slash_timeout = commands.InvokableSlashCommand(timeout, description="تایم اوت کردن ممبر", dm_permission=False)

    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.bot_has_guild_permissions(moderate_members=True)
    @commands.has_guild_permissions(moderate_members=True)
    async def untimeout(self, ctx: context, member: disnake.Member, *, reason: str = ''):
        check_access(member, ctx.author, ctx.guild.me, ctx.guild.owner_id)
        await member.timeout(duration=None, reason=f"{reason} by {ctx.author.name}#{ctx.author.discriminator}")
        await ctx.send(f"باموفقیت {member.name}#{member.discriminator} از حالت تایم اوت حارج شد")

    prefix_untimeout = commands.Command(untimeout, brief="خارج کردن ممبر از حالت تایم اوت", usage="t!untimeout <user_id> <duration> [reason]")
    slash_untimeout = commands.InvokableSlashCommand(untimeout, description="خارج کردن ممبر از حالت تایم اوت", dm_permission=False)
