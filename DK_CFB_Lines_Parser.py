import requests
import math
import time
from bs4 import BeautifulSoup

url = 'https://sportsbook.draftkings.com/leagues/football/ncaaf'
response = requests.get(url)

header = {
    'authorization': "Nzk2MDgxNzg5NTU4NDU2MzUx.GgQdGC.ZCqoFX8tlo7RNB5UgZaLJuuMqh7PvaaX-m1fyo"
}


reqCount = 0
prevTeams = []
prevLines = []

while reqCount < 120:

    print('\nParsing DK CFB Spreads data...')

    soup = BeautifulSoup(response.content, 'html.parser')

    # # Find all the rows in the table
    teams = soup.find_all('div', class_="event-cell__name-text")
    lines = soup.find_all(
        'span', class_="sportsbook-outcome-cell__line")

    numGames = math.floor(len(teams)/2)

    print('\nData Parsed.\n')

    if reqCount > 0:
        print('Comparing previous odds...\n')
        for i in range(1):
            if lines[math.floor(4*i)].text != prevLines[math.floor(4*i)].text:
                msg = f'Game {i+1}: {prevTeams[math.floor(2*i)].text}({prevLines[math.floor(4*i)].text}) to ({lines[math.floor(4*i)].text})'
                print("\n******LINE CHANGE********")
                print(msg)
                print("*************************")
                r = requests.post("https://discord.com/api/v9/channels/1166410287453319250/messages",
                                  data={'content': msg}, headers=header)

    prevTeams = teams
    prevLines = lines

    if reqCount > 0:
        print('No line changes - will check again in 1 min.')
        print(f'Runtime: {60*reqCount} seconds')
    else:
        print('Will check for line changes in 1 min.')

    reqCount = reqCount + 1

    time.sleep(60)
