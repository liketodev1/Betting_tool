#!/usr/bin/env python3.7
"""
Implemented by Artavazd Mnatsakanyan.

Description:

    Script gets betting site URLs from config. Scrap's all football information, Adds all score's to DB,
    Compare's all scores. Start betting based on users input.

Dependencies & Supported Versions:

    Python 3.5.x

Libraries:

    os, re, sys, json, logging, requests, bs4, selenium, argparse, configparser, enum,
    pymysql, pymysql.cursors, difflib.

Revision:

    v0.1 alpha (10/02/2020)
        Initial version

Usage:  betting_tool.py -c config.ini
"""
try:
    import os
    import re
    import sys
    import json
    import logging
    import requests
    from database import Database
    from difflib import SequenceMatcher
    from bet365 import get_bet365_content
    from betflag import get_betflag_content
    from eurobet import get_eurobet_content
    from sport888 import get_sport888_content
    from betstars import get_betstars_content
    from lottomatica import get_lottomatica_content
    from common import SECTION, OPTIONS, print_log_msg, Log, configs
except ImportError as exception:
    print("%s - Please install the necessary libraries." % exception)
    sys.exit(1)


def internet_connection():
    try:
        requests.get('http://216.58.192.142', timeout=1)
        return True
    except ConnectionError as ce:
        return False
    except Exception:
        return False


def join_dictionaries(all_scores_list):
    """
    Get same teams from all dictionaries, then create new dictionary with combined score information.
    Args:
        all_scores_list - list with all web page dictionaries
    Returns:
        final_scores - merged dictionary with team names and scores.
    """
    final_scores = {}
    for score_dict in all_scores_list:
        for current_team in score_dict:
            copy_of_final_scores = final_scores.copy()
            if final_scores:
                for final_dict_team in copy_of_final_scores:
                    if SequenceMatcher(None, final_dict_team, current_team).ratio() > 0.7:
                        if score_dict[current_team] not in final_scores[final_dict_team]:
                            final_scores[final_dict_team].append(score_dict[current_team])
                            break
                else:
                    final_scores[current_team] = [score_dict[current_team]]
            else:
                final_scores[current_team] = [score_dict[current_team]]

    return final_scores

def main():
    """
    Main function
    """
    # For logging debug, warning, error and info mesaages into log file
    log_file = configs.get(SECTION.default.name).get(OPTIONS.log.name)
    level = configs.get(SECTION.default.name).get(OPTIONS.loglevel.name)
    logging.basicConfig(filename=log_file, level=level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            filemode='w')

    # Get sport name from config file
    sport = configs.get(SECTION.default.name).get(OPTIONS.sport_name.name)
    # Get country name from config file
    country = configs.get(SECTION.default.name).get(OPTIONS.country_name.name)
    # Get tournament type from config file
    tournament = configs.get(SECTION.default.name).get(OPTIONS.tournament_type.name)

    # Check internet connection, than go further
    if not internet_connection():
        print_log_msg('Please check internet connection, than try again', Log.ERROR.value)
        sys.exit(0)

    # Get betstars url from config file
    betstars_url = configs.get(SECTION.betstars.name).get(OPTIONS.betstars_url.name)
    # Get team names and scores from web page
    betstars_scores = get_betstars_content(betstars_url, country, tournament)

    # Get eurobet url from config file
    eurobet_url = configs.get(SECTION.eurobet.name).get(OPTIONS.eurobet_url.name)
    # Get team names and scores from web page
    eurobet_scores = get_eurobet_content(eurobet_url, sport, country, tournament)

    # Get betflag url from config file
    betflag_url = configs.get(SECTION.betflag.name).get(OPTIONS.betflag_url.name)
    # Get team names and scores from web page
    betflag_scores = get_betflag_content(betflag_url, sport, country, tournament)

    # Get bet365 url from config file
    bet365_url = configs.get(SECTION.bet365.name).get(OPTIONS.bet365_url.name)
    # Get team names and scores from web page
    bet365_scores = get_bet365_content(bet365_url, sport, country, tournament)

    # Get lottomatica url from config file
    lottomatica_url = configs.get(SECTION.lottomatica.name).get(OPTIONS.lottomatica_url.name)
    # Get team names and scores from web page
    lottomatica_scores = get_lottomatica_content(lottomatica_url, sport, country, tournament)

    # Get sport888 url from config file
    sport888_url = configs.get(SECTION.sport888.name).get(OPTIONS.sport888_url.name)
    # Get team names and scores from web page
    sport888_scores = get_sport888_content(sport888_url, sport, country, tournament)

    # Merge all scores and get final dictionary
    final_scores = join_dictionaries([betstars_scores, eurobet_scores, betflag_scores, bet365_scores,
        lottomatica_scores, sport888_scores])

    with open('django/result', "w") as res:
        json.dump(final_scores, res)

    # Dump all scores in to the DB.
#    database = Database()
#    database.run_query(final_scores)


if __name__ == "__main__":
    main()
