from discord.ext import commands
import aiosqlite



class Datenbank(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = "main.db"


    @commands.Cog.listener()
    async def on_ready(self):
        async with aiosqlite.connect(self.db) as db:
            await db.executescript(
                """
                CREATE TABLE IF NOT EXISTS numberguess_setup (
                    guild_id INTEGER PRIMARY KEY,
                    channel_id INTEGER DEFAULT 0,
                    zahl INTEGER DEFAULT 0,
                    gesetzt INTEGER DEFAULT 0,
                    level INTEGER DEFAULT 1,
                    versuche INTEGER DEFAULT 0,
                    löschen INTEGER DEFAULT 0
                )
                """)
            await db.executescript(
                """
                CREATE TABLE IF NOT EXISTS numberguess (
                    guild_id INTEGER,
                    user_id INTEGER,
                    versuche INTEGER DEFAULT 0,
                    versuche3 INTEGER DEFAULT 0,
                    PRIMARY KEY(guild_id, user_id)
                )
                """)


        

        


def setup(bot):
    bot.add_cog(Datenbank(bot))
