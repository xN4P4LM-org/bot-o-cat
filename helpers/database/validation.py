"""
This file contains validation functions for database operations.
"""

import logging
from pymongo import MongoClient

logger = logging.getLogger("discord.db.validation")


def validateInDatabase(
    db: MongoClient,
    db_command_loggeer: logging.Logger,
    database_name: str | None = None,
    collection_name: str | None = None,
) -> bool:
    """
    Validate the collection exists in the database.

    Arguments:
        db: The database connection.
        database_name: The name of the database.
        collection_name: The name of the collection.

    Returns:
        bool: True if the collection exists, False otherwise.
    """

    # check if the database exists
    if database_name is not None and collection_name is None:
        if database_name not in db.list_database_names():
            db_command_loggeer.error("Database %s does not exist", database_name)
            return False

    # check if the collection exists
    if collection_name is not None and database_name is not None:
        if collection_name not in db[database_name].list_collection_names():
            db_command_loggeer.error("Collection %s does not exist", collection_name)
            return False

    return True
