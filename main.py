import os
from dotenv import load_dotenv
import discord
import ezcord

intents = discord.Intents.all()

status = discord.Status.online


servers = None

bot = ezcord.Bot(
    intents=intents,
    debug_guilds=None,
    language="de",
    status=status

)


if __name__ == "__main__":
    bot.load_cogs(
        subdirectories=True,
        )



load_dotenv()
bot.run(os.getenv("TOKEN"))

