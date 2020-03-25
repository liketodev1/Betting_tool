try:
    import sys
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from common import SECTION, OPTIONS, print_log_msg, Log, configs
except ImportError as exception:
    print("%s - Please install the necessary libraries." % exception)
    sys.exit(1)


def get_sport888_content(url, sport, country, tournament):
    """
    Open each URL and get necessary tables with given credentials.
    Args:
        url - sport888 url from config file
        sport - sport name from config file
        country - country name from config file
        tournament - tournament type from config file
    Returns:
        web_page_and_scores - dictionary with web page name and scores
    """
    content = ''
    web_page_and_scores = {}
    translated_country_names = {'Spagna':'Spain', 'Germania':'Germany', 'Francia':'France',
                                'Arabia Saudita':'Saudi Arabia', 'Argentina':'Argentine', 'Australia':'Australia',
                                'Austria':'Austria', 'Azerbaijan':'Azerbaijan', 'Bangladesh':'Bangladesh',
                                'Belgio':'Belgium', 'Bulgaria':'Bulgaria','Cile':'Chile', 'Cipro': 'Cyprus',
                                'Colombia':'Colombia', 'Croazia':'Croatia','Danimarca':'Denmark', 'Ecuador':'Ecuador',
                                'Egitto':'Egypt', 'Emirati Arabi':'United Arab Emirates', 'Finlandia':'Finland',
                                'Francia':'France', 'Galles':'Wales', 'Germania':'Germany', 'Ghana':'Ghana',
                                'India':'India', 'Inghilterra':'England', 'Iran':'Iran', 'Irlanda':'Ireland',
                                'Irlanda del Nord':'northern Ireland', 'Islanda':'Iceland', 'Italia':'Italy',
                                'Kuwait':'Kuwait', 'Malta':'Malta', 'Marocco':'Marocco', 'Messico':'Mexico',
                                'Myanmar':'Myanmar', 'Olanda':'Holland', 'Oman':'Oman', 'Palestine':'Palestine',
                                'Paaguay':'Paaguay', 'Peru':'Peru', 'Polonia':'Poland', 'Portogallo':'Portugal',
                                'Repubblica Ceca':'Czech Republic', 'Romania':'Romania', 'Russia':'Russia',
                                'Scozia':'Scotland', 'Sud Africa':'South Africa', 'Sudan':'', 'Svizzera':'',
                                'Tailandia':'Thailand'}
    try:
        browser = webdriver.Firefox()
        # makes sure slower connections work as well
        browser.implicitly_wait(10)

        print_log_msg('Open %s url for searching content' % url, Log.DEBUG.value)
        country = translated_country_names[country].lower()
        browser.get(url + '/' + sport.lower() + '/#/filter/football/' + country + '/' + tournament.lower())

        score_table = browser.find_elements_by_xpath("//div[@class='KambiBC-event-item__event-wrapper']")
        content = [item.text for item in \
                browser.find_elements_by_xpath("//div[@class='KambiBC-event-item__event-wrapper']")]
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
        url - web page current url
        content - url parsed content with all information.
    Returns:
        sport888_scores_dict - dictionary with all scores fro given options.
    """
    sport888_scores_dict = {}
    for each_row in content:
        row = each_row.split('\n')
        if each_row and len(row) > 11:
            teams = row[2].lower() + ' - ' + row[3].lower()
            scores = [row[7], row[9], row[11]]
            sport888_scores_dict[teams] = {url : scores}

    return sport888_scores_dict
