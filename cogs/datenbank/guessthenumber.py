from utils import *
from discord.ext import commands
import ezcord


class NumberGessDatenbank(commands.Cog):
    def __init__(self, bot):
        self.bot = bot  


class numberguessDB(ezcord.DBHandler):
    def __init__(self): 
        super().__init__('main.db')

    async def gesetzt_select(self, guild_id):
        return await self.one("SELECT gesetzt FROM numberguess_setup WHERE guild_id = ?", guild_id)
    
    async def zahl_select(self, guild_id):
        return await self.one("SELECT zahl FROM numberguess_setup WHERE guild_id = ?", guild_id)

    async def level_select(self, guild_id):
        return await self.one("SELECT level FROM numberguess_setup WHERE guild_id = ?", guild_id)

    async def channel_select(self, guild_id):
        return await self.one("SELECT channel_id FROM numberguess_setup WHERE guild_id = ?", guild_id)

    async def versuche_select(self, guild_id):
        return await self.one("SELECT versuche FROM numberguess_setup WHERE guild_id = ?", guild_id)
    
    async def versuche2_select(self, guild_id, user_id):
        return await self.one("SELECT versuche FROM numberguess WHERE guild_id = ? AND user_id = ?", guild_id, user_id)

    async def versuche2_reset(self, guild_id):
        return await self.all("SELECT user_id FROM numberguess WHERE guild_id = ?", guild_id)

    async def versuche3_select(self, guild_id, user_id):
        return await self.one("SELECT versuche3 FROM numberguess WHERE guild_id = ? AND user_id = ?", guild_id, user_id)
    
    async def delete_select(self, guild_id):
        return await self.one("SELECT löschen FROM numberguess_setup WHERE guild_id = ?", guild_id)
    

    async def channel_set(self, channel_id, guild_id):
        await self.exec("UPDATE numberguess_setup SET channel_id = ? WHERE guild_id = ?", channel_id, guild_id)

    async def gesetzt_set(self, gestzt, guild_id):
        await self.exec("UPDATE numberguess_setup SET gesetzt = ? WHERE guild_id = ?", gestzt, guild_id)

    async def level_set(self, level, guild_id):
        await self.exec("UPDATE numberguess_setup SET level = ? WHERE guild_id = ?", level, guild_id)
    
    async def zahl_set(self, zahl, guild_id):
        await self.exec("UPDATE numberguess_setup SET zahl = ? WHERE guild_id = ?", zahl, guild_id)
    
    async def versuche_set(self, versuche, guild_id):
        await self.exec("UPDATE numberguess_setup SET versuche = ? WHERE guild_id = ?", versuche, guild_id)

    async def versuche2_set(self, versuche, guild_id, user_id):
        await self.exec("UPDATE numberguess SET versuche = ? WHERE guild_id = ? AND user_id = ?", versuche, guild_id, user_id)
    
    async def versuche3_set(self, versuche, guild_id, user_id):
        await self.exec("UPDATE numberguess SET versuche3 = ? WHERE guild_id = ? AND user_id = ?", versuche, guild_id, user_id)

    async def delete_set(self, delete, guild_id):
        await self.exec("UPDATE numberguess_setup SET löschen = ? WHERE guild_id = ?", delete, guild_id)

    
    async def check(self, guild_id):
        await self.exec("INSERT OR IGNORE INTO numberguess_setup (guild_id) VALUES (?)", guild_id)

    async def check2(self, guild_id, user_id):
        await self.exec("INSERT OR IGNORE INTO numberguess (guild_id, user_id) VALUES (?, ?)", guild_id, user_id)


        
def setup(bot):
    bot.add_cog(NumberGessDatenbank(bot))