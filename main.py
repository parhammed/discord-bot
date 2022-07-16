from classes import Bot
from cogs import setup

token = "Nzk3ODAzMDA0NjQ0Mjk0Njc3.GRYcsW.s_5PNwJKx9iwAi6xJoxTKIL9dm0rby6p_uFphc"
bot = Bot("db.json")  # path of database

setup(bot)

if __name__ == '__main__':
    bot.run(token)
