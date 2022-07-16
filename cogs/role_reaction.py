from typing import TYPE_CHECKING
from disnake.ext import commands
import disnake

from utils import check_role_access

context = disnake.CommandInteraction

if TYPE_CHECKING:
    from classes import Bot

    context = disnake.CommandInteraction | commands.Context


class RoleReactionCog(commands.Cog):
    def __init__(self, bot: "Bot"):
        self._bot: "Bot" = bot

    @commands.cooldown(5, 20, commands.BucketType.channel)
    @commands.bot_has_guild_permissions(manage_roles=True)
    @commands.has_guild_permissions(manage_roles=True)
    async def add_role_reaction(self, ctx: context, message: disnake.Message, role: disnake.Role, emoji: str):
        emoji = disnake.PartialEmoji.from_str(emoji)
        check_role_access(role, ctx.author, ctx.guild.me, ctx.guild.owner_id)
        self._bot.db["role_reaction"].setdefault(str(message.channel.id), {}).setdefault(str(message.id), {})[
            str(emoji.id or emoji.name)] = role.id
        self._bot.db.save()
        await message.add_reaction(emoji)
        await ctx.send("ری اکشن رول با موفقیت اضافه شد")

    prefix_add_role_reaction = commands.Command(add_role_reaction, brief="اضافه کردن رول ری اکشن")
    slash_add_role_reaction = commands.InvokableSlashCommand(add_role_reaction, description="اضافه کردن رول ری اکشن", dm_permission=False)

    @commands.cooldown(5, 20, commands.BucketType.channel)
    @commands.bot_has_guild_permissions(manage_roles=True)
    @commands.has_guild_permissions(manage_roles=True)
    async def remove_role_reaction(self, ctx: context, message: disnake.Message, emoji: disnake.PartialEmoji = None):
        if str(message.channel.id) not in self._bot.db["role_reaction"].keys():
            await ctx.send("پیام مورد نظر شما در سیستم ثبت نشده است")
            return
        if str(message.id) not in self._bot.db["role_reaction"][str(message.channel.id)].keys():
            await ctx.send("پیام مورد نظر شما در سیستم ثبت نشده است")
            return

        if emoji is None:
            for role in self._bot.db["role_reaction"][str(message.channel.id)][str(message.id)]:
                check_role_access(message.guild.get_role(role), ctx.author, ctx.guild.me, ctx.guild.owner_id)
            del self._bot.db["role_reaction"][str(message.channel.id)][str(message.id)]
            await message.clear_reactions()
        else:
            role = self._bot.db["role_reaction"][str(message.channel.id)][str(message.id)].pop(emoji.id or emoji.name, None)
            if role is None:
                await ctx.send("ری اکشن مورد نظر شما در سیستم ثبت نشده است")
                return
            check_role_access(message.guild.get_role(role), ctx.author, ctx.guild.me, ctx.guild.owner_id)
            await message.clear_reaction(emoji)
        self._bot.db.save()
        await ctx.send("ری اکشن رول با موفقیت حذف شد")

    prefix_remove_role_reaction = commands.Command(remove_role_reaction, brief="حذف کردن رول ری اکشن")
    slash_remove_role_reaction = commands.InvokableSlashCommand(remove_role_reaction, description="حذف کردن رول ری اکشن",
                                                                dm_permission=False)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: disnake.RawReactionActionEvent):
        if payload.user_id == self._bot.user.id:
            return
        x = self._bot.db["role_reaction"].get(str(payload.channel_id), None)
        if x is None:
            return
        x = x.get(str(payload.message_id), None)
        if x is None:
            return
        x = x.get(str(payload.emoji.id or payload.emoji.name), None)
        if x is not None:
            try:
                await self._bot.get_guild(payload.guild_id).get_member(payload.user_id).add_roles(disnake.Object(x))
            except (disnake.Forbidden, disnake.HTTPException):
                pass

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: disnake.RawReactionActionEvent):
        if payload.user_id == self._bot.user.id:
            return
        x = self._bot.db["role_reaction"].get(str(payload.channel_id), None)
        if x is None:
            return
        x = x.get(str(payload.message_id), None)
        if x is None:
            return
        x = x.get(str(payload.emoji.id or payload.emoji.name), None)
        if x is not None:
            try:
                await self._bot.get_guild(payload.guild_id).get_member(payload.user_id).remove_roles(disnake.Object(x))
            except (disnake.Forbidden, disnake.HTTPException, AttributeError):
                pass
