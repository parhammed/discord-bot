from sys import stderr

from disnake.ext import commands
from disnake import Member, Embed, Role
from traceback import format_exc


def check_access(member: Member, author: Member, me: Member, owner_id: int):
    if owner_id == member.id:
        raise commands.MissingPermissions(["این شخص اونر سرور است"])

    if owner_id != author.id and author.top_role.position <= member.top_role.position:
        raise commands.MissingPermissions(["شما به این شخص دسترسی ندارید"])

    if me.top_role.position <= member.top_role.position:
        raise commands.BotMissingPermissions(["من به این شخص دسترسی ندارم"])


def check_role_access(role: Role, author: Member, me: Member, owner_id: int):
    if owner_id != author.id and author.top_role.position <= role.position:
        raise commands.MissingPermissions(["شما به این رول دسترسی ندارید"])

    if me.top_role.position <= role.position:
        raise commands.BotMissingPermissions(["من به این رول دسترسی ندارم"])


_no_private_embed = Embed(
    title="کامند مورد نظر شما در پی وی کار نمیکند❌",
    description="لطفا در سرور مورد نظر خود امتحان کنید",
    color=0xffff00
)


def error_handler(error: Exception) -> Embed | None:
    if isinstance(error, commands.CommandInvokeError):
        error: Exception = error.original

    if isinstance(error, commands.CommandNotFound):
        return

    if isinstance(error, commands.CommandOnCooldown):
        embed = Embed(
            title="کامند مورد نظر در حالت استراحت است😴",
            description=f"لطفا بعد از {round(error.retry_after, 2)} مجددا تلاش کنید",
            color=0x00ffff)
        return embed

    if isinstance(error, commands.NoPrivateMessage):
        return _no_private_embed

    if isinstance(error, commands.MissingPermissions):
        embed = Embed(
            title="شما دسترسی های لازم را ندارید",
            description="نیازمندی ها:\n{}".format('\n'.join(error.missing_permissions)),
            color=0xffff00)
        return embed

    if isinstance(error, commands.BotMissingPermissions):
        embed = Embed(
            title="بات دسترسی های لازم را ندارد درصورتی که شما نمیتوانید به بات دسترسی های خواسته شده را بدهید به اونر سرور اطلاع دهید",
            description="نیازمندی ها:\n{}".format('\n'.join(error.missing_permissions)),
            color=0xff0000)
        return embed

    if isinstance(error, commands.MissingRequiredArgument):
        embed = Embed(
            title=f"شما پارامتر {error.param.name} را وارد نکرده اید",
            description=str(error.param.annotation),
            color=0xffff00
        )
        return embed

    if isinstance(error, commands.MemberNotFound):
        embed = Embed(
            title=f"ممبر {error.argument} یافت نشد",
            description="لطفا آیدی شخص مورد نظر را بنویسید یا آن را منشن کنید",
            color=0xffff00
        )
        return embed

    print(error.__traceback__, file=stderr, flush=True)
    embed = Embed(title="❌متاسفانه خطایی رخ داده", description=str(error), color=0xff0000)
    return embed
