"""
This file contains the delete operations for the database.
"""

import logging
from typing import Any
from pymongo import MongoClient
from validation import validateInDatabase

logger = logging.getLogger("discord.db.delete")


def deleteDatabase(db_connection: MongoClient, database_name: str) -> bool:
    """
    Delete a database in the mongoDB.
    """

    # check if the database exists
    if validateInDatabase(db_connection, logger, database_name=database_name):
        return False

    # delete the database
    db_connection.drop_database(database_name)

    # check if the database was deleted
    if validateInDatabase(db_connection, logger, database_name=database_name):
        return True

    logger.error(
        "You shouldn't see this message, check that database %s was deleted successfully",
        database_name,
    )
    return False


def deleteCollection(
    db_connection: MongoClient, database_name: str, collection_name: str
) -> bool:
    """
    Delete a collection in the mongoDB database.
    """

    # check if the collection exists
    if validateInDatabase(
        db_connection,
        logger,
        database_name=database_name,
        collection_name=collection_name,
    ):
        return False

    # delete the collection
    db_connection[database_name].drop_collection(collection_name)

    # check if the collection was deleted
    if validateInDatabase(
        db_connection,
        logger,
        database_name=database_name,
        collection_name=collection_name,
    ):
        return True

    logger.error(
        "You shouldn't see this message, check that collection %s was deleted successfully",
        collection_name,
    )
    return False


def deleteOneDocument(
    db_connection: MongoClient, database_name: str, collection_name: str, document: Any
) -> bool:
    """
    Delete a document in the mongoDB database.
    """
    # check if the collection exists
    if not validateInDatabase(
        db_connection,
        logger,
        database_name=database_name,
        collection_name=collection_name,
    ):
        return False

    # delete the document
    deleted_item = db_connection[database_name][collection_name].delete_one(document)

    # check if the document was deleted
    if deleted_item.deleted_count > 0:
        logger.info("Document %s deleted successfully", document)
        return True

    logger.error(
        "You shouldn't see this message, check that document %s was deleted successfully",
        document,
    )
    return False
