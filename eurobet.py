try:
    import sys
    from time import sleep
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.common.exceptions import TimeoutException
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from common import SECTION, OPTIONS, print_log_msg, Log, configs
except ImportError as exception:
    print("%s - Please install the necessary libraries." % exception)
    sys.exit(1)


def get_eurobet_content(url, sport, country, tournament):
    """
    Open each URL and get necessary tables with given credentials.
    Args:
        url - eurobet url from config file
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
        wait = WebDriverWait(browser, 10)

        print_log_msg('Open %s url for searching content' % url, Log.DEBUG.value)
        browser.get(url +  '/' + sport.lower() + '/')

        # Scrol page until string in visible
        countries_alphabet = None
        scroll_from = 0
        scroll_limit = 500
        while not countries_alphabet:
            sleep(1)
            browser.execute_script("window.scrollTo(%s, %s);" % (scroll_from, scroll_from + scroll_limit))
            scroll_from += scroll_limit
            try:
                countries_alphabet = browser.find_element_by_xpath("//*[contains(text(), 'Mostra altri paesi A-Z')]")
            except TimeoutException:
                pass

        sleep(1)
        countries_alphabet.click()

        print_log_msg('Open all countries section for clicking on current country(given from config)', Log.DEBUG.value)
        all_countires = browser.find_element_by_xpath("//div[@class='sidebar-sx-mobile  open']")
        for li_tag in all_countires.find_elements_by_tag_name('li'):
            country_name = li_tag.text.split('\n')[0]
            if country_name == country:
                li_tag.click()

        print_log_msg('Open all tournaments section for clicking on current tournament(given from config)',
                Log.DEBUG.value)
        sleep(1)

        for li_tag in all_countires.find_elements_by_tag_name('li'):
            tournament_type = li_tag.text.split('\n')[0]
            if tournament_type == tournament:
                li_tag.click()

        timeout = 1
        try:
            element_present = EC.presence_of_element_located((By.ID, 'main'))
            WebDriverWait(browser, timeout).until(element_present)
        except TimeoutException:
            print("Timed out waiting for page to load")
        finally:
            print("Page loaded")

        print_log_msg('Get page content', Log.DEBUG.value)
        score_table = browser.find_element_by_xpath("//div[contains(@style,'position: relative;')]")
        content = [item.text for item in score_table.find_elements_by_xpath("//div[@class='event-row']")]

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
        eurobet_scores_dict - dictionary with all scores fro given options.
    """
    print_log_msg('Create eurobet dictionary with all teams and scores', Log.DEBUG.value)
    eurobet_scores_dict = {}
    for each_row in content:
        row = each_row.split('\n')
        if len(row) < 10:
            teams = row[2].replace('-','- ').lower()
            scores = {url : row[3:6]}
        else:
            teams = row[3].replace('-','- ').lower()
            scores = {url : row[3:6]}
        eurobet_scores_dict[teams] = scores

    return eurobet_scores_dict
