from classes import Bot
from cogs import setup

token = "Token"  # the token (on past commit) was changed
bot = Bot("db.json")  # path of database

setup(bot)

if __name__ == '__main__':
    bot.run(token)
