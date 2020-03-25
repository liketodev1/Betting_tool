try:
    import os
    import sys
    import logging
    import argparse
    import configparser
    from os import path
    from enum import Enum
except ImportError as exception:
    print ("%s - Please install the necessary libraries." % exception)
    sys.exit(1)

"""
Config file passing as script argument
"""
parser = argparse.ArgumentParser()
parser.add_argument('-c', '--config_file', type=str, help='Configuration file')
args = parser.parse_args()

# Logger name
logger = logging.getLogger('betting_tool')

if not args.config_file:
    print("Configuration file passed to the script as an argument does not exist.")
    sys.exit(0)


def get_configurations(file_name):
    """
    Read file content and create dictionary which with options
    Args:
        file_name - the configuration file
    Returns:
    config - a dict with configuration options
    """
    Config = configparser.ConfigParser()
    Config.read(file_name)
    config = {}
    for each_section in Config.sections():
        config[each_section] = \
                dict((eachKey, eachValue)
                     for eachKey, eachValue in Config.items(each_section))
    return config


configs = get_configurations(args.config_file)


def print_log_msg(msg, level):
    """
    Print and add the message into the log file.
    """
    # Check the log level
    {
        Log.INFO.value: lambda msg: logger.info(msg),
        Log.DEBUG.value: lambda msg: logger.debug(msg),
        Log.WARNING.value: lambda msg: logger.warning(msg),
        Log.ERROR.value: lambda msg: logger.error(msg),
        Log.CRITICAL.value: lambda msg: logger.critical(msg)
    }[level](msg)

    print(msg)

SECTION = Enum('SECTION', (('default'), ('betstars'), ('eurobet'), ('betflag'), ('db'),
                            ('bet365'), ('sport888'), ('lottomatica')))

OPTIONS = Enum('OPTIONS', (('loglevel'), ('log'), ('sport_name'), ('country_name'), ('tournament_type'),
                           ('betstars_url'), ('betstars_username'), ('betstars_password'), ('eurobet_url'),
                           ('eurobet_username'), ('eurobet_password'), ('betflag_url'), ('betflag_username'),
                           ('betflag_password'), ('bet365_url'), ('bet365_username'), ('bet365_password'),
                           ('sport888_url'), ('sport888_username'), ('sport888_password'), ('lottomatica_url'),
                           ('lottomatica_username'), ('lottomatica_password'), ('db_host'), ('db_user'), ('db_password'),
                           ('db_port'), ('db_name')))

Log = Enum('Log', (('INFO'), ('WARNING'), ('ERROR'), ('CRITICAL'), ('DEBUG')), start=0)

