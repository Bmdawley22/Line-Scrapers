import requests
import math
import time
from bs4 import BeautifulSoup

url = 'https://www.vsin.com/odds/nfl/'
response = requests.get(url)

reqCount = 0
prevTeams = []
prevLines = []

# while reqCount < 120:

print('\nParsing Circa NFL Spreads data...')

soup = BeautifulSoup(response.content, 'html.parser')

print(soup.find_all('tr', class_='scoresummary-row standings'))
