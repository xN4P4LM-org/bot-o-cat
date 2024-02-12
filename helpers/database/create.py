"""
This file contains the create operations for the mongoDB database.
"""

import logging
from pymongo import MongoClient

logger = logging.getLogger("discord.db.create")


def createDatabase(db_connection: MongoClient, database_name: str) -> bool:
    """
    Create a database in the mongoDB.
    """

    # check if the database already exists
    if database_name in db_connection.list_database_names():
        logger.error("Database %s already exists", database_name)
        return False

    # create the database
    created_db = db_connection.get_database(database_name)

    # check if the database was created
    if created_db.name == database_name:
        logger.info("Database %s created successfully", database_name)
        return True

    logger.error(
        "You shouldn't see this message, check that database %s was created successfully",
        database_name,
    )
    return False


def createCollection(
    db_connection: MongoClient, database_name: str, collection_name: str
) -> bool:
    """
    Create a collection in the mongoDB database.
    """

    # create the collection
    collection = db_connection[database_name].create_collection(collection_name)

    # check if the collection was created
    if collection.database.name == database_name and collection.name == collection_name:
        logger.info("Collection %s created successfully", collection_name)
        return True

    logger.error(
        "You shouldn't see this message, check that collection %s was created successfully",
        collection_name,
    )
    return False


def insertOneDocument(
    db_connection: MongoClient, database_name: str, collection_name: str, document: dict
) -> bool:
    """
    Create a document in the mongoDB collection.
    """

    # check if the collection exists
    if collection_name not in db_connection[database_name].list_collection_names():
        logger.error("Collection %s does not exist", collection_name)
        return False

    # insert the document
    insert = db_connection[database_name][collection_name].insert_one(document)

    # check if the document was created
    if insert.acknowledged:
        logger.info("Document created successfully")
        return True

    logger.error(
        "You shouldn't see this message, check that the document was inserted successfully"
    )
    return False


def insertManyDocuments(
    db_connection: MongoClient,
    database_name: str,
    collection_name: str,
    documents: list,
) -> bool:
    """
    Insert many documents in the mongoDB collection.
    """

    # check if the collection exists
    if collection_name not in db_connection[database_name].list_collection_names():
        logger.error("Collection %s does not exist", collection_name)
        return False

    # insert the documents
    insert = db_connection[database_name][collection_name].insert_many(documents)

    # check if the documents were created
    if insert.acknowledged:
        logger.info("Documents created successfully")
        return True

    logger.error(
        "You shouldn't see this message, check that the documents were inserted successfully"
    )
    return False
