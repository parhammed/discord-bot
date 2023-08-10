import json

import disnake
from disnake.ext import commands, tasks
from jdatetime import datetime

from utils import error_handler

_default = {
    "prefix": "t!",
    "guild": 840477615546302474,
    "members_log": 997463755292147772,
    "date_log": 997463596386754580,
    "role_reaction": {}
}

__all__ = ("Database", "Bot", "TicketMaker")


class Database(dict):
    def __init__(self, filename: str):
        super(Database, self).__init__(_default)
        self._filename = filename

        try:
            with open(filename, "r", encoding="utf-8") as file:
                self.update(json.load(file))
        except FileNotFoundError:
            pass

        self.save()

    def save(self) -> None:
        with open(self._filename, "w", encoding="utf-8") as file:
            json.dump(self, file, indent=2)


class Bot(commands.Bot):
    def __init__(self, db_path: str):
        self.db: Database = Database(db_path)
        super(Bot, self).__init__(self.prefix_getter, intents=disnake.Intents.all(), test_guilds=[self.db["guild"]])
        self.save.start()

    def prefix_getter(self, bot: commands.Bot, message: disnake.Message):
        prefix = self.db["prefix"]
        return prefix, prefix + ' ', *commands.when_mentioned(bot, message)

    @staticmethod
    async def on_ready():
        print("ready")

    @staticmethod
    async def on_connect():
        print("connected")

    @staticmethod
    async def on_disconnect():
        print("disconnected")

    @staticmethod
    async def on_resumed():
        print("resumed")

    @tasks.loop(minutes=10)
    async def save(self):
        self.db.save()

    async def on_command_error(self, ctx: commands.Context, exception: commands.CommandError) -> None:
        embed = error_handler(exception)
        if embed is not None:
            await ctx.reply(embed=embed)

    async def on_slash_command_error(self, inter: disnake.ApplicationCommandInteraction, exc: commands.CommandError) -> None:
        embed = error_handler(exc)
        await inter.response.send_message(embed=embed)


class TicketMaker(disnake.ui.View):
    def __init__(self, admin_role: disnake.Role, category: disnake.CategoryChannel):
        self._admin_role = admin_role
        self._category = category
        super(TicketMaker, self).__init__(timeout=None)

    @disnake.ui.button(label="ساخت تیکت", emoji="✉", style=disnake.ButtonStyle.primary, custom_id="Ticket")
    async def create_ticket(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        await interaction.response.defer(with_message=True, ephemeral=True)

        channel = await self._category.create_text_channel(f"ticket-{interaction.author.name}", overwrites={
            self._category.guild.default_role: disnake.PermissionOverwrite(view_channel=False),
            self._admin_role: disnake.PermissionOverwrite(view_channel=True),
            interaction.author: disnake.PermissionOverwrite(view_channel=True),
        })
        await channel.send(f"تیکت شما با موفقیت ساخته شد\n{interaction.author.mention}")
        await interaction.followup.send("تیکت شما با موفقیت ساخته شد", ephemeral=True)
