"""
This file contains the operations to setup a new guild 
in the database, and is used by the bot when a new guild is added.
"""

import logging
from discord.ext import commands
from event_handlers.guilds import addMissingGuilds, setupGuildEvents
from helpers.env import getEnvVar
from helpers.terminal_colors import TerminalColors
from helpers.core_cogs import loadCoreCogs


logger = logging.getLogger("discord.bot.events")


async def setupBotEvents(bot: commands.Bot):
    """
    This function sets up the bot events
    """

    @bot.event
    async def on_ready():  # pylint: disable=invalid-name
        """
        Event: Bot is ready

        This event is called when the bot is ready to be used and
        prints information about the bot.
        """

        if bot.user is not None:

            # Print the join URL
            logger.info(
                "Invite URL: \
%shttps://discord.com/api/oauth2/authorize?\
client_id=%s&permissions=8&scope=bot%s",
                TerminalColors.GREEN_BOLD,
                bot.user.id,
                TerminalColors.RESET_COLOR,
            )

            logger.info(
                "%s%s%s is connected to %s%s guilds %s",
                TerminalColors.GREEN_BOLD,
                bot.user.name,
                TerminalColors.RESET_COLOR,
                TerminalColors.GREEN_BOLD,
                len(bot.guilds),
                TerminalColors.RESET_COLOR,
            )

        logger.info("Loading core cogs...")
        await loadCoreCogs(bot, "core")

        if getEnvVar("DISCORD_USE_DATABASE", "False") == "True":
            await setupGuildEvents(bot)
            addMissingGuilds(bot)

        logger.info("Bot is ready")
