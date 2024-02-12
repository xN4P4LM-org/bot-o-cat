"""
    This is the main file for the bot.
"""

import asyncio
import logging
import discord
from discord.ext import commands
from helpers.database.connection import DatabaseConnection
from helpers.get_ssh_key import getPubKey
from helpers.logs import Logger
from helpers.env import getEnvVar
from helpers.terminal_colors import TerminalColors
from helpers.help_command import getHelpCommand
from helpers.core_cogs import loadCoreCogs
from event_handlers.guilds import setupGuildEvents
from event_handlers.bot import setupBotEvents


def main():
    """
    Main entry point for the bot.
    """
    # Set up overall logging
    Logger.setup_logging(int(getEnvVar("DISCORD_BOT_LOG_LEVEL", "20")))

    # Set up the logger
    startup_logging = logging.getLogger("discord.bot.startup")

    # Create a new bot instance
    bot = commands.Bot(
        command_prefix=getEnvVar("DISCORD_BOT_COMMAND_PREFIX", "."),
        intents=discord.Intents.all(),
        description=getEnvVar("DISCORD_BOT_DESCRIPTION"),
        owner_id=int(getEnvVar("DISCORD_BOT_OWNER_ID")),
        case_insensitive=True,
        help_command=getHelpCommand(),
    )

    if getEnvVar("DISCORD_USE_DATABASE", "False") == "True":
        database_connection: DatabaseConnection = DatabaseConnection()

    # Read public ssh key from file and log it
    startup_logging.info(
        "Public SSH key: %s%s%s",
        TerminalColors.GREEN_BOLD,
        getPubKey(),
        TerminalColors.RESET_COLOR,
    )

    # instantiate the bot events
    asyncio.run(setupBotEvents(bot))

    # Run the bot
    bot.run(
        getEnvVar("DISCORD_BOT_TOKEN"),
        log_handler=None,
    )

    # Close the database connection before exiting
    database_connection.close_connection()


# Run the main function
if __name__ == "__main__":
    main()
