"""
This file contains the operations to setup a new guild 
in the database, and is used by the bot when a new guild is added.
"""

import logging
from pymongo import MongoClient
from discord import Guild
from helpers.database.create import createDatabase

logger = logging.getLogger("discord.guilds.add")

def addGuild(
        db_connection: MongoClient,
        guild: Guild) -> bool:
    """
    Add a new guild to the database.
    """

    database_name = str(guild.id) + "_db"

    # create the database
    guild_created = createDatabase(db_connection, database_name)

    if guild_created:
        logger.info("Database %s for guild %s added successfully",
                    database_name,
                    guild.name)
        return True

    logger.error(
        "You shouldn't see this message, check that guild %s was added successfully",
        guild.name)

    return False
