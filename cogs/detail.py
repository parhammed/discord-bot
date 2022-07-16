from disnake.ext import commands, tasks
from jdatetime import date

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from classes import Bot


class DetailCog(commands.Cog):
    def __init__(self, bot: "Bot"):
        self._bot: "Bot" = bot
        self.update_detail.start()
        self.update_date.start()
        self._member_count = 0
        self._today = None

    @tasks.loop(minutes=1)
    async def update_detail(self):
        guild = self._bot.get_guild(self._bot.db["guild"])
        if guild.member_count != self._member_count:
            self._member_count = guild.member_count
            await guild.get_channel(self._bot.db["members_log"]).edit(name=f"😀 member count: {guild.member_count}")

    @tasks.loop(hours=3)
    async def update_date(self):
        today = date.today()
        if today != self._today:
            self._today = today
            await self._bot.get_channel(self._bot.db["date_log"]).edit(name=f"📅 date: {today.year}\\{today.month}\\{today.day}")

    @update_date.before_loop
    @update_detail.before_loop
    async def wait(self):
        await self._bot.wait_until_ready()
