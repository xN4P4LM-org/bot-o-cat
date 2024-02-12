"""
Class for the database configuration for the bot and all cogs.
"""

import sys
import logging
from typing import Any
from pymongo import MongoClient
from helpers.env import getEnvVar


class MongoClientOptions:
    """
    Class for the configuration of the mongoDB client.
    """

    options = {}

    def __init__(self, host: str):
        self.options["enabled"] = True
        self.options["host"] = host

        # get the authentication method
        self.add_option(
            "authMechanism",
            getEnvVar("DISCORD_MONGO_DB_AUTHENTICATION_METHOD", "SCRAM-SHA-256"),
        )

        # get the port if set
        port = getEnvVar("DISCORD_MONGO_DB_PORT", "27017")
        if port is not None:
            self.add_option("port", port)

        if self.get_option("authMechanism") == "SCRAM-SHA-256":
            # get the username and password
            self.add_option(
                "username", getEnvVar("DISCORD_MONGO_DB_USERNAME", "bot-o-cat")
            )
            self.add_option("password", getEnvVar("DISCORD_MONGO_DB_PASSWORD", "None"))

            self.add_option(
                "authSource",
                getEnvVar("DISCORD_MONGO_DB_AUTHENTICATION_DATABASE", "admin"),
            )

        if self.get_option("authMechanism") == "MONGODB-X509":

            self.add_option("authSource", "$external")
            self.add_option("tls", True)
            self.add_option(
                "tlsAllowInvalidCertificates",
                getEnvVar("DISCORD_MONGO_DB_TLS_ALLOW_INVALID_CERTIFICATES", "false"),
            )
            crl = getEnvVar("DISCORD_MONGO_DB_CRL_FILE_PATH", "None")

            if crl != "None":
                self.add_option("tlsCAFile", crl)

            # get the client certificate
            self.add_option(
                "tlsCertificateKeyFile",
                getEnvVar("DISCORD_MONGO_DB_CERTIFICATE_FILE_PATH"),
            )

    def add_option(self, option: str, value: str | bool | None) -> None:
        """
        Add an option to the mongoDB client configuration.
        """
        self.options[option] = value

    def return_options(self) -> dict:
        """
        Return the options as a dictionary.
        """
        return self.options

    def get_option(self, option: str) -> str:
        """
        Get an option from the configuration.
        """
        return self.options.get(option, None)

    def remove_option(self, option: str) -> None:
        """
        Remove an option from the configuration.
        """
        self.options.pop(option, None)

    def use_option(self, option: str, default: Any) -> Any:
        """
        Get and remove an option from the configuration.
        """
        value = self.options.get(option, default)
        logging.debug("Using option: %s = %s", option, value)
        self.remove_option(option)
        return value


class DatabaseConnection:
    """
    This class contains the database connection for the bot and all cogs.
    """

    init = False

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(DatabaseConnection, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        if self.init is False:
            self.connection = self._start_database_connection()
            self.init = True
            logging.info("Database connection established")

        logging.debug("Database connection already established")

    def get_connection(self) -> MongoClient:
        """
        Return the database connection.
        """
        return self.connection

    def close_connection(self) -> None:
        """
        Close the database connection.
        """
        self.connection.close()

    def _start_database_connection(self) -> MongoClient:
        """
        Connects and returns a mongoDB Client.

        Using either the following environment variables or default values:
            - DISCORD_MONGO_DB_HOST_NAME
            - DISCORD_MONGO_DB_PORT
            - DISCORD_MONGO_DB_DATABASE_NAME
        """

        db_options = MongoClientOptions(getEnvVar("DISCORD_MONGO_DB_HOST_NAME"))

        if db_options.get_option("enabled") is not None:
            db_options.remove_option("enabled")

            logging.debug("Connecting to the database with the following options:")

            if db_options.get_option("authMechanism") == "SCRAM-SHA-256":
                db_conn = MongoClient(
                    host=db_options.use_option("host", "localhost"),
                    port=int(db_options.use_option("port", "27017")),
                    username=db_options.use_option("username", "bot-o-cat"),
                    password=db_options.use_option("password", "None"),
                    authSource=db_options.use_option("authSource", "admin"),
                    authMechanism=db_options.use_option(
                        "authMechanism", "SCRAM-SHA-256"
                    ),
                )

            if db_options.get_option("authMechanism") == "MONGODB-X509":
                db_conn = MongoClient(
                    host=db_options.use_option("host", "localhost"),
                    port=int(db_options.use_option("port", "27017")),
                    authMechanism=db_options.use_option(
                        "authMechanism", "MONGODB-X509"
                    ),
                    tls=True,
                    tlsAllowInvalidCertificates=db_options.use_option(
                        "tlsAllowInvalidCertificates", "false"
                    ),
                    tlsCertificateKeyFile=db_options.use_option(
                        "tlsCertificateKeyFile", None
                    ),
                    authSource=db_options.use_option("authSource", "$external"),
                )
        if db_conn is not None:
            logging.debug("Connected to the database.")
            return db_conn

        logging.critical("Failed to connect to the database.")
        sys.exit(1)
