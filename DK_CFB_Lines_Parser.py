import requests
import math
import time
from bs4 import BeautifulSoup

from scraperParameters import params

url = 'https://sportsbook.draftkings.com/leagues/football/ncaaf'
response = requests.get(url)

header = {
    'authorization': "Nzk2MDgxNzg5NTU4NDU2MzUx.GgQdGC.ZCqoFX8tlo7RNB5UgZaLJuuMqh7PvaaX-m1fyo"
}

reqCount = 0
prevTeams = []
prevLines = []
numLineMoves = 0


def sendNotificationToDiscord(msg):
    print("\n******LINE CHANGE********")
    print(msg)
    print("*************************")
    r = requests.post(f'https://discord.com/api/v9/channels/{params["CFBChannelID"]}/messages',
                      data={'content': msg}, headers=header)


while reqCount < (params['maxRunTimeInMin'] * (60 / params['repRateInS'])):

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
        for i in range(numGames):
            if params['test'] == True:
                print(
                    f'{i}: {teams[2*i].text}({lines[4*i].text})({lines[4*i+1].text}) || ({prevLines[4*i].text})({prevLines[4*i+1].text})')
            if lines[4*i].text != prevLines[4*i].text:
                msg = f'Line Move: {prevTeams[2*i].text}({prevLines[4*i].text}) to ({lines[4*i].text})'
                sendNotificationToDiscord(msg)
                numLineMoves = numLineMoves + 1

            elif lines[4*i+1].text != prevLines[4*i+1].text:
                msg = f'Total Move: {prevTeams[2*i].text}({prevLines[4*i+1].text}) to ({lines[4*i+1].text})'
                sendNotificationToDiscord(msg)
                numLineMoves = numLineMoves + 1

    prevTeams = teams
    prevLines = lines

    if params['test'] == True:
        if reqCount == 0:
            prevLines[0] = BeautifulSoup(
                '<span class="sportsbook-outcome-cell__line">+Test</span>', 'html.parser')

    if reqCount > 0:
        print('\nNo line changes - will check again in 1 min.')
        print(f'\nNumber of Line Moves: {numLineMoves}')
        print(f'Runtime: {60*reqCount} seconds')
    else:
        print('Will check for line changes in 1 min.')

    reqCount = reqCount + 1

    time.sleep(params['repRateInS'])
