"""
This is the admin cog for the bot.
"""

from asyncio import sleep
import logging
from discord import Client
from discord.ext import commands

logger = logging.getLogger("discord.command.admin")

class Admin(commands.Cog, name="Admin"):
    """
    This is the admin cog for the bot.
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        """
        Command: ping

        This command is used to test if the bot is running or frozen.
        """
        logger.debug("User %s is pinged the bot.", ctx.author)
        await ctx.send("Pong!")

    @commands.command(hidden=True, aliases=["stop", "exit"])
    async def shutdown(self, ctx: commands.Context):
        """
        Command: shutdown

        This command is used to shutdown the bot.
        """

        if ctx.author.id != ctx.bot.owner_id:
            logger.warning("User %s tried to shutdown the bot.", ctx.author)
            await ctx.send("You are not allowed to use this command!")
            await ctx.message.add_reaction("❌")
            return
        logger.info("User %s is shutting down the bot.", ctx.author)
        await ctx.send("Shutting down...")
        await ctx.message.add_reaction("✅")
        try:
            await Client.close(ctx.bot)
        finally:
            await sleep(1)
            logger.info("Bot is shutdown.")

    async def setup(self, bot: commands.Bot):
        """
        Add the commands to the bot.
        """
        description_short = "This is the ping command for the bot."
        description_long = """
This is the ping command for the bot, and can be used to test if the bot is running or frozen.

If you want to test if the bot is running, use the following command:
.ping
        """

        self.ping.help = description_short
        self.ping.brief = "Ping the bot."
        self.ping.description = description_long

        description_short = "This is the shutdown command for the bot."

        self.shutdown.help = description_short
        self.shutdown.brief = "Shutdown the bot."

        bot.add_command(self.ping)
        bot.add_command(self.shutdown)
