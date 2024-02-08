"""
This file contains the update operations for the database.
"""
import logging
from typing import Any
from pymongo import MongoClient

logger = logging.getLogger("discord.db.update")

def updateDocument(
        db_connection: MongoClient,
        database_name: str,
        collection_name: str,
        query: Any,
        new_values: Any) -> bool:
    """
    Update a document in the collection in the mongoDB database.
    """

    # update the document
    updated_document = db_connection[database_name][collection_name].update_one(
        query, new_values)

    # check if the document was updated
    if updated_document.modified_count:
        logger.info("Document updated successfully")
        return True

    logger.error("Document not updated")
    return False
