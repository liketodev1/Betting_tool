try:
    import sys
    import time
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.common.exceptions import TimeoutException
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from common import SECTION, OPTIONS, print_log_msg, Log, configs
except ImportError as exception:
    print("%s - Please install the necessary libraries." % exception)
    sys.exit(1)


def get_betstars_content(url, country, tournament):
    """
    Open each URL and get necessary tables with given credentials.
    Args:
        url - betstars url from config file
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
        browser.get(url + '#/soccer/competitions')

        timeout = 1
        try:
            element_present = EC.presence_of_element_located((By.ID, 'main'))
            WebDriverWait(browser, timeout).until(element_present)
        except TimeoutException:
            print("Timed out waiting for page to load")
        finally:
            print("Page loaded")

        browser.find_element_by_xpath("//div[@id='sideAZRegions']").click()

        print_log_msg('Open all countries section for clicking on current country(given from config)', Log.DEBUG.value)
        all_countires = browser.find_elements_by_xpath("//div[@class='competitionListItem listItem']")
        for country_name in all_countires:
            if country_name.text == country.upper():
                country_name.click()
                found_country = country_name

        print_log_msg('Open all tournaments section for clicking on current tournament(given from config)',
                Log.DEBUG.value)
        time.sleep(1)

        for li_tag in found_country.find_elements_by_tag_name('li'):
            if li_tag.text == country + ' - ' + tournament:
                score_url = li_tag.find_element_by_tag_name('a').get_attribute('href')

        print_log_msg('Get page content', Log.DEBUG.value)
        browser.get(score_url)

        timeout = 1
        try:
            element_present = EC.presence_of_element_located((By.ID, 'main'))
            WebDriverWait(browser, timeout).until(element_present)
        except TimeoutException:
            print("Timed out waiting for page to load")
        finally:
            print("Page loaded")

        score_table = browser.find_element_by_xpath("//div[@class='market-content']")
        content = [item.text for item in score_table.find_elements_by_tag_name('li')]
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
    print_log_msg('Create betstars dictionary with all teams and scores', Log.DEBUG.value)
    betstars_scores_dict = {}
    for each_row in content:
        scores = []
        row = each_row.split('\n')
        if len(row) > 10:
            teams = row[4].lower() + ' - ' + row[5].lower()
            scores = {url : row[6:9]}
        else:
            teams = row[0].lower() + ' - ' + row[1].lower()
            scores = {url : row[2:5]}
        betstars_scores_dict[teams] = scores

    return betstars_scores_dict
