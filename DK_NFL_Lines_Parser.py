import requests
import math
import time
from bs4 import BeautifulSoup

url = 'https://sportsbook.draftkings.com/leagues/football/nfl'
response = requests.get(url)

header = {
    'authorization': "Nzk2MDgxNzg5NTU4NDU2MzUx.GgQdGC.ZCqoFX8tlo7RNB5UgZaLJuuMqh7PvaaX-m1fyo"
}


reqCount = 0
prevTeams = []
prevLines = []

while reqCount < 120:
    print('\n')
    print('parsing data...')
    soup = BeautifulSoup(response.content, 'html.parser')

    # # Find all the rows in the table
    teams = soup.find_all('div', class_="event-cell__name-text")
    lines = soup.find_all(
        'span', class_="sportsbook-outcome-cell__line")

    numGames = math.floor(len(teams)/2)
    print('Comparing previous odds')

    if reqCount > 0:
        for i in range(numGames):
            if lines[math.floor(4*i)].text != prevLines[math.floor(4*i)].text:
                msg = f'Game {i+1}: {prevTeams[math.floor(2*i)].text}({prevLines[math.floor(4*i)].text}) to ({lines[math.floor(4*i)].text})')
                print("******LINE CHANGE********")
                print(msg)
                print("*************************")
                r = requests.post("https://discord.com/api/v9/channels/1166388909618511894/messages",
                                  data={'content': msg}, headers=header)

    reqCount = reqCount + 1

    prevTeams = teams
    prevLines = lines
    time.sleep(30)

    print(f'{30*reqCount} seconds')
