"""
This file contains the operations to setup a new guild 
in the database, and is used by the bot when a new guild is added.
"""

import logging
from pymongo import MongoClient
from discord import Guild
from discord.ext import commands
from helpers.database.connection import DatabaseConnection
from helpers.env import getEnvVar

logger = logging.getLogger("discord.guilds")


async def setupGuildEvents(bot: commands.Bot):
    """
    This function sets up the bot events for the guildis
    """

    # get the database connection
    db_connection = DatabaseConnection().get_connection()

    @bot.event
    async def on_guild_join(guild: Guild):  # pylint: disable=invalid-name
        """
        Add the guild to the database when the bot joins a new guild.
        """
        if getEnvVar("DISCORD_USE_DATABASE", "False") == "True":
            # Add the guild to the database
            addGuild(db_connection, guild)

    @bot.event
    async def on_guild_remove(guild: Guild):  # pylint: disable=invalid-name
        """
        Remove the guild from the database when the bot leaves a guild.
        """
        if getEnvVar("DISCORD_USE_DATABASE", "False") == "True":
            # Remove the guild to the database
            removeGuild(db_connection, guild)


def addGuild(db_connection: MongoClient, guild: Guild) -> bool:
    """
    Add a new guild to the database.
    """
    # create the database
    guild_collection = db_connection["guilds"].create_collection(str(guild.id))

    if guild_collection.name == str(guild.id):
        logger.info(
            "Database %s for guild %s created successfully", guild.id, guild.name
        )
        return True

    logger.error(
        "You shouldn't see this message, check that guild %s was created successfully",
        guild.name,
    )

    return False


def removeGuild(db_connection: MongoClient, guild: Guild) -> bool:
    """
    Remove a guild from the database.
    """

    # Connect to the guilds database
    db_connection["guilds"].drop_collection(str(guild.id))

    # check if the database was deleted
    if str(guild.id) not in db_connection["guilds"].list_collection_names():
        logger.info(
            "Database %s for guild %s removed successfully", guild.id, guild.name
        )
        return True

    logger.error(
        "You shouldn't see this message, check that guild %s was removed successfully",
        guild.name,
    )

    return False


def addMissingGuilds(bot: commands.Bot):
    """
    Add the guilds that the bot is already in to the database.
    """
    # get the database connection
    db_connection = DatabaseConnection().get_connection()

    # existing guilds in the database
    guilds = db_connection["guilds"].list_collection_names()

    # add the guilds to the database
    for guild in bot.guilds:
        if str(guild.id) not in guilds:
            addGuild(db_connection, guild)
