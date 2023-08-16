import discord
from discord.ext import commands
from discord.commands import slash_command, Option, SlashCommandGroup
from utils import *
import datetime
import ezcord
import aiosqlite
from discord.utils import basic_autocomplete
from cogs.datenbank.guessthenumber import numberguessDB
import random

dba = numberguessDB()

level = ["Leicht", "Mittel", "Schwer"]
delete = ["An", "Aus"]


async def get_level(ctx):
    return level
async def get_delete(ctx):
    return delete

class NummerErraten(ezcord.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.DB = "main.db"

    guessthenumber = SlashCommandGroup("guessthenumber")
    channel = guessthenumber.create_subgroup("channel")

    @channel.command(
        description="🔢 × Setze einen Kanal für das Minigame guess the number!"
    )
    async def set(
        self,
        ctx,
        channel: Option(
            discord.TextChannel, "Wähle einen Text Kanal wo der Game starten soll"
        ),
        level: Option(str, "Wähle die Schwierigkeit aus", autocomplete=basic_autocomplete(get_level)),
        versuche: Option(int, "Wähle aus wie viele versuche ein User hat!"),
        delete: Option(str, "Wähle aus, ob Nachrichten nach dem löschen gelöscht werden sollen oder nicht", autocomplete=basic_autocomplete(get_delete)),
    ):
        if await admin(ctx):
            return
        await ctx.defer(ephemeral=True)
        await dba.check(ctx.guild.id)
        gesetzt = await dba.gesetzt_select(ctx.guild.id)
        if gesetzt == 1:
            await ctx.respond(
                f"× Das Guess the number Game ist schon aktiviert.",
                ephemeral=True,
            )
            return
        await dba.channel_set(channel.id, ctx.guild.id)
        await dba.gesetzt_set(1, ctx.guild.id)
        if level == "Leicht":
            zahl = random.randint(0, 100)
            await dba.zahl_set(zahl, ctx.guild.id)
            await dba.level_set(1, ctx.guild.id)
        if level == "Mittel":
            zahl = random.randint(0, 1000)
            await dba.zahl_set(zahl, ctx.guild.id)
            await dba.level_set(2, ctx.guild.id)
        if level == "Schwer":
            zahl = random.randint(0, 10000)
            await dba.zahl_set(zahl, ctx.guild.id)
            await dba.level_set(3, ctx.guild.id)

        await dba.versuche_set(versuche, ctx.guild.id)
        if delete == "An":
            await dba.delete_set(0, ctx.guild.id)
        if delete == "Aus":
            await dba.delete_set(1, ctx.guild.id)
        level1 = await dba.level_select(ctx.guild.id)
        if level1 is None:
            text = "No"
        if level1 == 1:
            text = "Die gesuchte Zahl ist zwischen 0 und 100"
        if level1 == 2:
            text = "Die gesuchte Zahl ist zwischen 0 und 1000"
        if level1 == 3:
            text = "Die gesuchte Zahl ist zwischen 0 und 10000"
        embed = discord.Embed(
            title=" Errate die Zahl", description=f"{text}", color=COLOR
        )
        embed.timestamp = datetime.datetime.now()
        message = await ctx.respond("Die Nachrichten werden gelöscht!", ephemeral=True)
        await channel.purge()
        await channel.send(embed=embed)
        await message.edit(
            f"× das Sytem wurde erfolgreich in {channel.mention} aktiviert!",
        )

    @channel.command(
        description="🔢 × Entferne einen Kanal für das Minigame guess the number!"
    )
    async def remove(self, ctx):
        if await admin(ctx):
            return

        await ctx.defer(ephemeral=True)
        gesetzt = await dba.gesetzt_select(ctx.guild.id)
        channel = await dba.channel_select(ctx.guild.id)
        if gesetzt == 0:
            return await ctx.respond(
                f"× Das System wurde auf diesem Server noch nicht aktiviert!",
                ephemeral=True,
            )
        if channel is not None:
            channel = ctx.guild.get_channel(channel)
            message = await ctx.respond("Die Nachrichten werden gelöscht!", ephemeral=True)
            await channel.purge(limit=200)
            await dba.gesetzt_set(0, ctx.guild.id)
            users = await dba.versuche2_reset(ctx.guild.id)
            for user_id in users:
                await dba.versuche2_set(0, ctx.guild.id, user_id)
            await dba.channel_set(0, ctx.guild.id)
            await message.edit(content=
                f"× das System wurde auf diesem Server deaktiviert!",
                
            )
        else:
            await dba.gesetzt_set(0, ctx.guild.id)
            users = await dba.versuche2_reset(ctx.guild.id)
            for user_id in users:
                await dba.versuche2_set(0, ctx.guild.id, user_id)
            await ctx.respond(
                f"× das System wurde auf diesem Server deaktiviert!",
                ephemeral=True,
            )

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
    
        await dba.check2(message.author.guild.id, message.author.id)
        gesetzt = await dba.gesetzt_select(message.author.guild.id)
        versuche2 = await dba.versuche2_select(
            message.author.guild.id, message.author.id
        )
        vers = versuche2 + 1
        level = await dba.level_select(message.author.guild.id)
        channel = await dba.channel_select(message.author.guild.id)
        delete = await dba.delete_select(message.author.guild.id)
        verscuhe3 = await dba.versuche3_select(
            message.author.guild.id, message.author.id
        )
        if gesetzt == 0:
            return
        if channel == 0:
            return
        
        zahl = await dba.zahl_select(message.author.guild.id)
        versuche = await dba.versuche_select(message.author.guild.id)
        if message.channel.id == channel:
            channel = message.author.guild.get_channel(channel)
            if message.content.isdigit():
                if versuche2 >= versuche:
                    if verscuhe3 == 0:
                        await dba.versuche3_set(
                            1, message.author.guild.id, message.author.id
                        )
                        embed = discord.Embed(
                            title=f"Versuche verbraucht!",
                            description=f"{message.author.mention} du hast deine Versuche für die Zahl verbraucht!",
                            color=COLOR,
                        )
                        await channel.send(f"{message.author.mention} vielleicht schaffen es die anderen!", embed=embed, delete_after=10)
                        await message.delete()
                        return
                    if verscuhe3 == 1:
                        await message.delete()
                        return
                await dba.versuche2_set(
                    vers, message.author.guild.id, message.author.id
                )
                versuche2 = await dba.versuche2_select(
                    message.author.guild.id, message.author.id
                )
                if message.content == str(zahl):
                    if delete == 0:
                        await message.channel.purge()
                        await channel.send(
                        f"{message.author.mention} hat die Zahl erraten. Die Zahl war {zahl}"
                            )
                    if delete == 1:
                        await message.reply(f"{message.author.mention} hat die Zahl erraten. Die Zahl war {zahl}"
                            )
                    if level == 1:
                        zahl = random.randint(0, 100)
                        text = "Die gesuchte Zahl ist zwischen 0 und 100"
                    if level == 2:
                        zahl = random.randint(0, 1000)
                        text = "Die gesuchte Zahl ist zwischen 0 und 1000"
                    if level == 3:
                        zahl = random.randint(0, 10000)
                        text = "Die gesuchte Zahl ist zwischen 0 und 10000"
                    await dba.zahl_set(zahl, message.author.guild.id)
                    users = await dba.versuche2_reset(message.author.guild.id)
                    for user_id in users:
                        await dba.versuche2_set(0, message.author.guild.id, user_id)
                        await dba.versuche3_set(0, message.author.guild.id, user_id)
                    embed = discord.Embed(
                        title=" Errate die Zahl", description=f"{text}", color=COLOR
                    )
                    embed.timestamp = datetime.datetime.now()
                    await channel.send(embed=embed)
            else:
                await message.delete()


def setup(bot):
    bot.add_cog(NummerErraten(bot))
