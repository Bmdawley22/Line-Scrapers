import sys
import requests
import math
import time
from bs4 import BeautifulSoup

sportOptions = ['nfl', 'ncaaf', 'nba', ]
if len(sys.argv) == 2:
    sport = sys.argv[1].lower()
    if sport in sportOptions:
        if sport == 'nfl':
            url = f'https://sportsbook.draftkings.com/leagues/football/nfl'
            webhook_url = 'https://discord.com/api/webhooks/1166457905717968896/asJ74kScehP8BmzfekpRQ-XqVFaHiyvSJITX2UR3aGpoto_h1aeIeMZ_EA7yzQmeb6dj'
        if sport == 'ncaaf':
            url = f'https://sportsbook.draftkings.com/leagues/football/ncaaf'
            webhook_url = 'https://discordapp.com/api/webhooks/1166481866497462352/gisnsogwAcGVwTJN8my6gTzjtRhAzB05NPhO1_TQ2UWUO0yz25oGjcGXZxgipGCkwNzw'
        elif sport == 'nba':
            url = f'https://sportsbook.draftkings.com/leagues/basketball/nba'
            webhook_url = 'https://discordapp.com/api/webhooks/1166835230963937353/BplFeDDwc139dYtDJUC1cjUPRQX3n_hVtjVjJaSUcMgqj75_KNk22Z7KoHtnrg9McVg9'
    else:
        print('\nEnter valid sport as argument')
        print('\nExample command: python DK_Lines_Scraper.py nfl\n')
        sys.exit
else:
    print('\nEnter argument. Example command: pyhton DK_Lines_Scraper.py nfl\n')
    sys.exit

reqCount = 0
maxRunTimeInMin = 600  # 10 hours
repRateInS = 10
numLineMoves = 0
prevTeams = []
prevLines = []
prevNumTotalsInTables = []


def sendNotificationToDiscord(msg):
    print("\n******LINE CHANGE********")
    print(msg)
    print("*************************")
    r = requests.post(webhook_url, data={'content': msg})


while reqCount < (maxRunTimeInMin * (60 / repRateInS)):

    print(f'\nParsing DK {sport.upper()} Spreads data...')

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    tables = soup.find_all('tbody', class_='sportsbook-table__body')
    numTables = len(tables)
    numLiveTeams = int(
        len(soup.find_all('span', class_='event-cell__period'))/2)

    teams = []
    lines = []
    numTeamsInTable = []
    numLinesInTable = []
    numTotalsinTables = []

    for i in range(numTables):

        teams.append([])
        lines.append([])
        numTeamsInTable.append(
            len(tables[i].find_all('div', class_='event-cell__name-text')))
        numLinesInTable.append(
            len(tables[i].find_all('span', class_='sportsbook-outcome-cell__line')))
        numTotalsinTables.append(0)

        for j in range(numTeamsInTable[i]):
            teams[i].append(tables[i].find_all(
                'div', class_='event-cell__name-text')[j].text)
        for j in range(numLinesInTable[i]):
            lines[i].append(tables[i].find_all(
                'span', class_='sportsbook-outcome-cell__line')[j].text)
            if lines[i][j][0] != '-' and lines[i][j][0] != '+':
                numTotalsinTables[i] = numTotalsinTables[i] + 1

    teams[0] = teams[0][numLiveTeams:]
    lines[0] = lines[0][(2*numLiveTeams):]
    numTotalsinTables[0] = numTotalsinTables[0] - numLiveTeams

    print('\nData Parsed.\n')

    if reqCount > 0:

        print('Comparing previous odds...\n')

        for i in range(numTables):
            numGames = math.floor(len(teams[i])/2)
            if numTotalsinTables[i] == len(teams[i]):
                if (len(prevTeams[i]) == len(teams[i])) and (len(prevLines[i]) == len(lines[i])):
                    for j in range(numGames):
                        # print(
                        #     f'{i}{j}: {teams[i][2*j]}({lines[i][4*j]})({lines[i][4*j+1]}) || ({prevLines[i][4*j]})({prevLines[i][4*j+1]})')
                        if teams[i][2*j] == prevTeams[i][2*j] and lines[i][4*j] != prevLines[i][4*j]:
                            msg = f'Line Move: {prevTeams[i][2*j]}: ({prevLines[i][4*j]}) to ({lines[i][4*j]})'
                            sendNotificationToDiscord(msg)
                            numLineMoves = numLineMoves + 1

            if numTotalsinTables[i] == 0:
                if (len(prevTeams[i]) == len(teams[i])) and (len(prevLines[i]) == len(lines[i])):
                    for j in range(numGames):
                        # print(
                        #     f'{i}{j}: {teams[i][2*j]}({lines[i][2*j]}) || ({prevLines[i][2*j]})')
                        if teams[i][2*j] == prevTeams[i][2*j] and lines[i][2*j] != prevLines[i][2*j]:
                            msg = f'Line Move: {prevTeams[i][2*j]}: ({prevLines[i][2*j]}) to ({lines[i][2*j]})'
                            sendNotificationToDiscord(msg)
                            numLineMoves = numLineMoves + 1

    prevTeams = teams[:]
    prevLines = lines[:]
    prevNumTotalsInTables = numTotalsinTables[:]

    if reqCount > 0:
        print(
            f'\nNumber of Line Moves: {numLineMoves}\n  Will check again in {round(repRateInS, 2)} s')
        print('\n//////////////////////////////////////////////////////////////////////')
    else:
        print(f'Will check for line changes in {round(repRateInS, 2)} s.')
        print('\n//////////////////////////////////////////////////////////////////////')

    reqCount = reqCount + 1
    time.sleep(repRateInS)
