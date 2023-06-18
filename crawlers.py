from requests_html import HTMLSession
from dotenv import dotenv_values

config = dotenv_values('.env')


def justTry(func) :
    def wrapper(*args, **kwargs) :
        try :
            return func(*args, **kwargs)
        except Exception as e :
            print(f'Error in the {func.__name__} function. Error : {e}')
    return wrapper


@justTry
def bitcoinPrice(s : HTMLSession) :
    url = 'https://www.google.com/search?q=bitcoin+price'
    r = s.get(url, headers={'User-Agent': config['USER_AGENT']})
    price = r.html.find('div.card-section > div + div > span', first = True).text
    return price
      

@justTry
def ethereumPrice(s : HTMLSession) :
    url = 'https://www.google.com/search?q=ethereum+price'
    r = s.get(url, headers={'User-Agent': config['USER_AGENT']})
    price = r.html.find('div.card-section > div + div > span', first = True).text
    return price