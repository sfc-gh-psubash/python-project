"""
This module provides utilities for local development and testing.
"""

from pathlib import Path
from os import environ

import configparser
import toml


def get_env_var_config() -> dict:
    """
    Returns a dictionary of the connection parameters using the SnowSQL CLI
    environment variables.
    """
    try:
        return {
            "user": environ["SNOW_USER"],
            "password": environ["SNOW_PASSWORD"],
            "account": environ["SNOW_ACCOUNT"],
            "role": environ["SNOW_ROLE"],
            "warehouse": environ["SNOW_WAREHOUSE"],
            "database": environ["SNOW_DATABASE"],
            "schema": environ["SNOW_SCHEMA"],
        }
    except KeyError as exc:
        raise KeyError(
            "ERROR: Environment variable for Snowflake Connection not found. "
            + "Please set the SNOWSQL_* environment variables"
        ) from exc


def get_dev_config(
    environment: str = "dev",
    app_config_path: Path = Path.cwd().joinpath("app.toml"),
) -> dict:
    """
    Returns a dictionary of the connection parameters using the app.toml
    in the project root.
    """
    try:
        app_config = toml.load(app_config_path)
        config = configparser.ConfigParser(inline_comment_prefixes="#")
        config.read(app_config["snowsql_config_path"])
        session_config = config["connections." + app_config["snowsql_connection_name"]]
        session_config_dict = {
            k.replace("name", ""): v.strip('"') for k, v in session_config.items()
        }
        session_config_dict.update(app_config.get(environment))  # type: ignore
        return session_config_dict
    except Exception as exc:
        raise EnvironmentError(
            "Error creating snowpark session - be sure you've logged into "
            "the SnowCLI and have a valid app.toml file",
        ) from exc
