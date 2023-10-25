import requests
import math
import time
from bs4 import BeautifulSoup

from scraperParameters import params

login_url = 'https://myaccount.draftkings.com/login?intendedSiteExp=US-IA-SB&returnPath=%2F'
data = {'username': 'dawleyb11@gmail.com', 'password': params['pass']}

url = 'https://sportsbook.draftkings.com/leagues/football/nfl'


webhook_url = 'https://discord.com/api/webhooks/1166457905717968896/asJ74kScehP8BmzfekpRQ-XqVFaHiyvSJITX2UR3aGpoto_h1aeIeMZ_EA7yzQmeb6dj'

reqCount = 0
prevTeams = []
prevLines = []
numLineMoves = 0

def sendNotificationToDiscord(msg):
    print("\n******LINE CHANGE********")
    print(msg)
    print("*************************")
    r = requests.post(webhook_url, data={'content': msg})


while reqCount < (params['maxRunTimeInMin'] * (60 / params['repRateInS'])):

    print('\nParsing DK NFL Spreads data...')

    # # Perform the login
    # session = requests.Session()    
    # session.post(login_url, data=data)  

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
        for i in range(16):
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

    prevTeams = teams[:]
    prevLines = lines[:]

    # if params['test'] == True:
    #     if reqCount == 0:
    #         prevLines[0] = BeautifulSoup(
    #             '<span class="sportsbook-outcome-cell__line">+Test</span>', 'html.parser')

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
