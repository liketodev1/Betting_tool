try:
    import re
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


def get_betflag_content(url, sport, country, tournament):
    """
    Open each URL and get necessary tables with given credentials.
    Args:
        url - betflag url from config file
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
        browser.implicitly_wait(10)

        print_log_msg('Open %s url for searching content' % url, Log.DEBUG.value)
        browser.get(url)

        timeout = 1
        try:
            element_present = EC.presence_of_element_located((By.ID, 'main'))
            WebDriverWait(browser, timeout).until(element_present)
        except TimeoutException:
            print("Timed out waiting for page to load")
        finally:
            print("Page loaded")

        print_log_msg('Open all tournaments section for clicking on current tournament(given from config)',
                Log.DEBUG.value)


        print_log_msg('Open sport section(given from config)', Log.DEBUG.value)
        all_sport_countries = browser.find_element_by_xpath("//*[contains(text(), '%s')]" % sport)
        all_sport_countries.click()

        print_log_msg('Open all countries section for clicking on current country(given from config)', Log.DEBUG.value)
        all_countries = browser.find_elements_by_tag_name('li')
        for country_name in all_countries:
            if country_name.text == country:
                country_name.click()

                timeout = 1
                try:
                    element_present = EC.presence_of_element_located((By.ID, 'main'))
                    WebDriverWait(browser, timeout).until(element_present)
                except TimeoutException:
                    print("Timed out waiting for page to load")
                finally:
                    print("Page loaded")

                print_log_msg('Open all tournaments section for clicking on current tournament(given from config)',
                        Log.DEBUG.value)

                for tournament_t in country_name.find_element_by_xpath("//*[@class='collapse show']").find_elements_by_tag_name('li'):
                    if tournament_t.text == tournament:
                        tournament_t.click()

        timeout = 2
        try:
            element_present = EC.presence_of_element_located((By.ID, 'main'))
            WebDriverWait(browser, timeout).until(element_present)
        except TimeoutException:
            print("Timed out waiting for page to load")
        finally:
            print("Page loaded")

        content = [item.text for item in browser.find_elements_by_xpath("//div[@class='RowAvv']")]

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
        betstars_scores_dict - dictionary with all scores fro given options.
    """
    print_log_msg('Create betflag dictionary with all teams and scores', Log.DEBUG.value)
    betflag_scores_dict = {}
    for each_row in content:
        row = each_row.split('\n')
        if each_row:
            digit = re.search('\+\d+(\.*)', row[2]).group(0)
            if digit:
                teams = row[2].replace(digit,'').lower()
                scores = {url : row[3:6]}
                betflag_scores_dict[teams] = scores

    return betflag_scores_dict
