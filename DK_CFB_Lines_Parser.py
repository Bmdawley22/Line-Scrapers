import requests
import math
import time
from bs4 import BeautifulSoup

from scraperParameters import params

url = 'https://sportsbook.draftkings.com/leagues/football/ncaaf'

reqCount = 0
prevTeams = []
prevLines = []
numLineMoves = 0

webhook_url = 'https://discordapp.com/api/webhooks/1166481866497462352/gisnsogwAcGVwTJN8my6gTzjtRhAzB05NPhO1_TQ2UWUO0yz25oGjcGXZxgipGCkwNzw'


def sendNotificationToDiscord(msg):
    print("\n******LINE CHANGE********")
    print(msg)
    print("*************************")
    r = requests.post(webhook_url, data={'content': msg})


while reqCount < (params['maxRunTimeInMin'] * (60 / params['repRateInS'])):

    print('\nParsing DK CFB Spreads data...')
    response = requests.get(url)
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
            if lines[4*i].text != prevLines[4*i].text and teams[2*i].text == prevTeams[2*i].text:
                msg = f'Line Move: {prevTeams[2*i].text}:({prevLines[4*i].text}) to ({lines[4*i].text})'
                sendNotificationToDiscord(msg)
                numLineMoves = numLineMoves + 1

            elif lines[4*i+1].text != prevLines[4*i+1].text and teams[2*i].text == prevTeams[2*i].text:
                msg = f'Total Move: {prevTeams[2*i].text}:({prevLines[4*i+1].text}) to ({lines[4*i+1].text})'
                sendNotificationToDiscord(msg)
                numLineMoves = numLineMoves + 1

    prevTeams = teams[:]
    prevLines = lines[:]

    if params['test'] == True:
        if reqCount == 0:
            prevLines[0] = BeautifulSoup(
                '<span class="sportsbook-outcome-cell__line">+Test</span>', 'html.parser')

    if reqCount > 0:
        print(f'\nNo line changes - will check again in {round(params['repRateInS']/60, 2)} min.')
        print(f'\nNumber of Line Moves: {numLineMoves}')
        print(f'Runtime: {round(params['repRateInS']*reqCount,2)} seconds')
        print('\n//////////////////////////////////////////////////////////////////////')
    else:
        print(f'Will check for line changes in {round(params['repRateInS']/60, 2)} min.')
        print('\n//////////////////////////////////////////////////////////////////////')

    reqCount = reqCount + 1

    time.sleep(params['repRateInS'])
