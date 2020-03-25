    # Get sport888 username from config file
    sport888_username = configs.get(SECTION.sport888.name).get(OPTIONS.sport888_username.name)
    # Get sport888 password from config file
    sport888_password = configs.get(SECTION.sport888.name).get(OPTIONS.sport888_password.name)

    if sport888_username and sport888_password:
        sport888_auth(sport888_url, sport888_username, sport888_password)


# User auth
def betstars_auth(url, username, password):
    """
    Try to login to the betstars.in web page.
    Args:
        url - betstars url from config file
        username - betstars login/username from config file
        password - betstars password from config file
    """
    pass
#domain = urlparse(url).netloc.replace('www.','').replace('.com','')
#if configs.get(SECTION.domain.name).values():
#    username = domain + '_username'
#    password = domain + '_password'
#    print (configs.get(SECTION.domain.name).get(OPTIONS.username.name))
#    print (configs.get(SECTION.domain.name).get(OPTIONS.password.name))
#    exit(0)
#    web_page_login(url, )
