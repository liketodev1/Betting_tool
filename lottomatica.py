try:
    import sys
    from bs4 import BeautifulSoup
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.common.exceptions import TimeoutException
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from common import SECTION, OPTIONS, print_log_msg, Log, configs
except ImportError as exception:
    print("%s - Please install the necessary libraries." % exception)
    sys.exit(1)


def get_lottomatica_content(url, sport, country, tournament):
    """
    Open each URL and get necessary tables with given credentials.
    Args:
        url - lottomatica url from config file
        sport - sport name from config file
        country - country name from config file
        tournament - tournament type from config file
    Returns:
        web_page_and_scores - dictionary with web page name and scores
    """
    content = ''
    web_page_and_scores = {}
    try:
        browser = webdriver.Firefox()
        # makes sure slower connections work as well
        print_log_msg('Open %s url for searching content' % url, Log.DEBUG.value)
        browser.get(url + '/' + sport.lower() + '/' + country.lower() + '/' +tournament.lower())
        browser.implicitly_wait(10)

        timeout = 1
        try:
            element_present = EC.presence_of_element_located((By.ID, 'main'))
            WebDriverWait(browser, timeout).until(element_present)
        except TimeoutException:
            print("Timed out waiting for page to load")
        finally:
            print("Page loaded")

        print_log_msg('Find scores table and scrap infromation', Log.DEBUG.value)
        content = BeautifulSoup(browser.page_source, 'lxml')

    except Exception as exception:
        print (exception)

    finally:
        browser.delete_all_cookies()
        browser.close()

    if content:
        web_page_and_scores = create_scores_dict(url, content)
    else:
        print_log_msg('%s url ERROR while parsing' % url, Log.ERROR.value)
    return web_page_and_scores


def create_scores_dict(url, content):
    """
    Parse content and get scores information, dump to the dict.
    Args:
        url - web page current url.
        content - url parsed content with all information.
    Returns:
        lottomatica_scores_dict - dictionary with all scores fro given options.
    """
    print_log_msg('Create lottomatica dictionary with all teams and scores', Log.DEBUG.value)
    lottomatica_scores_dict = {}
    teams = [item.text for item in content.find_all("div", class_="event-name ng-binding")]
    all_scores = [item.text.strip('\n') for item in content.find_all("div", class_="selection-price")]
    scores = [all_scores[x:x+7] for x in range(0,len(all_scores), 7)]
    for team, score in zip(teams, scores):
        lottomatica_scores_dict[team] = {url : score[:3]}

    return lottomatica_scores_dict
