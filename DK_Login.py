import requests
from bs4 import BeautifulSoup
from scraperParameters import params

login_url = 'https://myaccount.draftkings.com/login?intendedSiteExp=US-IA-SB&returnPath=%2F'
data = {'username': 'dawleyb11@gmail.com', 'password': params['pass']}

# Perform the login
session = requests.Session()
session.post(login_url, data=data)

# # Access authenticated content
url = 'https://sportsbook.draftkings.com/leagues/football/nfl'

response = session.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

brady = soup.find('text', 'Sign out')
print(brady)
