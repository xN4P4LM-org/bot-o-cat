"""
    This is the main file for the bot.
"""

import logging
from os.path import expanduser
import discord
from discord.ext import commands
from helpers.database.connection import getDbConnection
from helpers.get_file import getFile
from helpers.logs import Logger
from helpers.env import getEnvVar
from helpers.terminal_colors import TerminalColors
from helpers.guild.add_guilds import addGuild
from helpers.help_command import getHelpCommand
from helpers.core_cogs import loadCoreCogs

def main():
    """
    Main entry point for the bot.
    """
    # Set up overall logging
    Logger.setup_logging(int(getEnvVar("DISCORD_BOT_LOG_LEVEL")))

    # Set up the logger
    startup_logging = logging.getLogger("discord.bot.startup")

    # check if the bot should use a database
    use_database = getEnvVar("DISCORD_USE_DATABASE")

    # Create a new bot instance
    bot = commands.Bot(
        command_prefix=getEnvVar("DISCORD_BOT_COMMAND_PREFIX"),
        intents=discord.Intents.all(),
        description=getEnvVar("DISCORD_BOT_DESCRIPTION"),
        owner_id=int(getEnvVar("DISCORD_BOT_OWNER_ID")),
        case_insensitive=True,
        help_command=getHelpCommand(),
    )

    if use_database == "True":
        # Test the database connection
        db_conn = getDbConnection()
        if db_conn is not None:
            startup_logging.info("Connected to the database.")
            db_conn.close()

    @bot.event
    async def on_guild_join(guild): # pylint: disable=invalid-name
        """
        Event: Bot joins a guild

        This event is called when the bot joins a new guild and 
        adds the guild to the database.
        """
        if use_database == "True":
            # Add the guild to the database
            db_conn = getDbConnection()
            if db_conn is not None:
                addGuild(db_conn, guild)
                db_conn.close()

    @bot.event
    async def on_ready():  # pylint: disable=invalid-name
        """
        Event: Bot is ready

        This event is called when the bot is ready to be used and 
        prints information about the bot.
        """

        if bot.user is not None:
            startup_logging.info("Logged in as %s", bot.user.name)

            # Print the join URL
            startup_logging.info(
                "Invite URL: \
%shttps://discord.com/api/oauth2/authorize?\
client_id=%s&permissions=8&scope=bot%s",
                TerminalColors.GREEN_BOLD,
                bot.user.id,
                TerminalColors.RESET_COLOR
            )

        # list all servers the bot is connected to
        if bot.user is not None:
            startup_logging.info(
                "%s%s%s is connected to %s%s guilds %s",
                TerminalColors.GREEN_BOLD,
                bot.user.name,
                TerminalColors.RESET_COLOR,
                TerminalColors.GREEN_BOLD,
                len(bot.guilds),
                TerminalColors.RESET_COLOR
            )

        startup_logging.info("Loading core cogs...")
        await loadCoreCogs(bot, "core")

    # check if using root or user ssh key if not set default to root
    use_user = getEnvVar("DISCORD_USE_USER_SSH") or "False"

    if use_user == "True":
        ssh_file = expanduser("~") + "/.ssh/id_ed25519.pub"
    else:
        ssh_file = "/root/.ssh/id_ed25519.pub"

    # Read public ssh key from file and log it
    startup_logging.info(
        "Public SSH key: %s%s%s",
        TerminalColors.GREEN_BOLD,
        getFile(ssh_file).strip("\n"),
        TerminalColors.RESET_COLOR
    )

    # Run the bot
    bot.run(
        getEnvVar("DISCORD_BOT_TOKEN"),
        log_handler=None,
    )


# Run the main function
if __name__ == "__main__":
    main()
