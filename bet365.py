try:
    import sys
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.common.exceptions import TimeoutException
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from common import SECTION, OPTIONS, print_log_msg, Log, configs
except ImportError as exception:
    print("%s - Please install the necessary libraries." % exception)
    sys.exit(1)


def get_bet365_content(url, sport, country, tournament):
    """
    Open each URL and get necessary tables with given credentials.
    Args:
        url - bet365 url from config file
        sport - sport name from config file
        country - country name from config file
        tournament - tournament type from config file
    Returns:
        web_page_and_scores - dictionary with web page name and scores
    """
    score_table = ''
    web_page_and_scores = {}
    try:
        browser = webdriver.Firefox()
        # makes sure slower connections work as well

        print_log_msg('Open %s url for searching content' % url, Log.DEBUG.value)
        browser.get(url + '/AS/B1/')
        browser.implicitly_wait(10)

        print_log_msg('Open all countries section for clicking on current country(given from config)', Log.DEBUG.value)
        browser.find_element_by_xpath("//div[contains(text(), '%s')]" % country).click()
        timeout = 1
        try:
            element_present = EC.presence_of_element_located((By.ID, 'main'))
            WebDriverWait(browser, timeout).until(element_present)
        except TimeoutException:
            print("Timed out waiting for page to load")
        finally:
            print("Page loaded")
        browser.find_element_by_xpath("//*[contains(text(), '%s')]" % (country + ' - '+ tournament)).click()
        print_log_msg('Open all tournaments section for clicking on current tournament(given from config)',
                Log.DEBUG.value)
        timeout = 1
        try:
            element_present = EC.presence_of_element_located((By.ID, 'main'))
            WebDriverWait(browser, timeout).until(element_present)
        except TimeoutException:
            print("Timed out waiting for page to load")
        finally:
            print("Page loaded")

        print_log_msg('Find scores table and scrap infromation', Log.DEBUG.value)
        score_table = browser.find_element_by_xpath("//div[@class='gll-MarketGroupContainer gll-MarketGroupContainer_HasLabels ']")
        columns = score_table.find_elements_by_xpath("//div[@class='sl-MarketCouponValuesExplicit33 gll-Market_General gll-Market_PWidth-12-3333 ']")
        teams = score_table.find_elements_by_xpath("//div[@class='sl-CouponParticipantWithBookCloses_NameContainer ']")

        # Get each score column from columns list
        teams_list = [team.text for team in teams]
        first_column = [item for item in columns[0].text.split('\n') if item != '1']
        second_column = [item for item in columns[1].text.split('\n') if item != 'X']
        third_column = [item for item in columns[2].text.split('\n') if item != '2']
    except Exception as exception:
        print (exception)

    finally:
        browser.delete_all_cookies()
        browser.close()

    if score_table:
        web_page_and_scores = create_scores_dict(url, teams_list, first_column, second_column, third_column)
    else:
        print_log_msg('%s url ERROR while parsing' % url, Log.ERROR.value)
    return web_page_and_scores


def create_scores_dict(url, teams_list, first_column, second_column, third_column):
    """
    Parse content and get scores information, dump to the dict.
    Args:
        url - web page current url
        teams_list - list with all teams from  score table
        first_column - first list with all score for table
        second_column - second list with all score for table
        third_column - third list with all score for table
    Returns:
        bet365_scores_dict - dictionary with all scores fro given options.
    """
    print_log_msg('Create bet365 dictionary with all teams and scores', Log.DEBUG.value)
    bet365_scores_dict = {}
    for team, column1, column2, column3 in zip(teams_list, first_column, second_column, third_column):
        bet365_scores_dict[team.replace(' v ', ' - ').lower()] = {url : [column1, column2, column3]}

    return bet365_scores_dict
