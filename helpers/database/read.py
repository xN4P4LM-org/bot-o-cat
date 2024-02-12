"""
This file contains the read operations for the database.
"""

import logging
from typing import Any
from pymongo import MongoClient

logger = logging.getLogger("discord.db.read")


def fetchOneDocument(
    db: MongoClient, database_name: str, collection_name: str, query: Any
) -> dict:
    """
    Fetch one document from the collection in the mongoDB database.
    """

    # fetch one document
    document = db[database_name][collection_name].find_one(query)

    if document:
        logger.info("Document fetched successfully")
        return document

    logger.error("Document not found")
    return {}


def fetchAllDocuments(
    db: MongoClient, database_name: str, collection_name: str, query: Any
) -> list | bool:
    """
    Fetch all documents from the collection in the mongoDB database.
    """

    # fetch all documents
    documents = list(db[database_name][collection_name].find(query))

    if documents:
        logger.info("Documents fetched successfully")
        return documents

    logger.error("Documents not found")
    return False
