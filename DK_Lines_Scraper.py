import sys
import requests
import math
import time
from bs4 import BeautifulSoup

# Determine sport selected and set Draftkings URL and which channel to webhook url to send notifications to
sportOptions = ['nfl', 'ncaaf', 'nba', ]
# make sure sport is entered in command line when script is ran
if len(sys.argv) == 2:
    sport = sys.argv[1].lower()
    # Makes sure sport entered matches designated sports for script
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

# initialize variables
reqCount = 0
maxRunTimeInMin = 600  # 10 hours
repRateInS = 10
numLineMoves = 0
prevTeams = []
prevLines = []
prevNumTotalsInTables = []
noCopyCount = 0
tableLineChanges = 0  # variable to keep track of the line changes for each table

# Function called when line movement identified
# Prints notification to command line and sends message to Discord channel


def sendNotificationToDiscord(msg):
    print("\n******LINE CHANGE********")
    print(msg)
    print("*************************")
    r = requests.post(webhook_url, data={'content': msg})


# While loop that runs until designated timeout to loop parsing of DK data
while reqCount < (maxRunTimeInMin * (60 / repRateInS)):

    print(f'\nParsing DK {sport.upper()} Spreads data...')
    # Request data from DK webpage
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    # Finds all of the tables on the web page
    tables = soup.find_all('tbody', class_='sportsbook-table__body')
    numTables = len(tables)  # Number of different tables on web page
    numLiveTeams = int(
        len(soup.find_all('span', class_='event-cell__period')))  # Number of teams in live games
    # Initialize variables
    teams = []
    lines = []
    numTeamsInTable = []
    numLinesInTable = []
    numTotalsinTables = []

    # Populate webpage data into variables
    for i in range(numTables):  # Loop through each web page table found
        # Adds row to each variable for each table
        teams.append([])
        lines.append([])
        numTeamsInTable.append(
            len(tables[i].find_all('div', class_='event-cell__name-text')))
        numLinesInTable.append(
            len(tables[i].find_all('span', class_='sportsbook-outcome-cell__line')))
        numTotalsinTables.append(0)
        # loop through each team (j) in each table (i)
        for j in range(numTeamsInTable[i]):
            teams[i].append(tables[i].find_all(
                'div', class_='event-cell__name-text')[j].text)  # adds team to teams[i] variable
        for j in range(numLinesInTable[i]):
            lines[i].append(tables[i].find_all(
                'span', class_='sportsbook-outcome-cell__line')[j].text)  # adds lines to lines[i] variable
            # checks if current line is a total by checking for "+" or "-" for the first character
            if lines[i][j][0] != '-' and lines[i][j][0] != '+':
                # count for number of totals in current table
                numTotalsinTables[i] = numTotalsinTables[i] + 1

    # print(numLiveTeams)
    if len(teams) > 0 and len(lines) > 0:
        # removes live teams, lines, and number of totals from variables
        teams[0] = teams[0][numLiveTeams:]
        lines[0] = lines[0][(2*numLiveTeams):]
        if len(numTotalsinTables) > 0:
            numTotalsinTables[0] = numTotalsinTables[0] - numLiveTeams

    print('\nData Parsed.\n')
    # Check to see if we have previous data
    if reqCount > 0:
        print('Comparing previous odds...\n')
        # Loop through current table
        for i in range(numTables):
            tableLineChanges = 0  # reset the counter for # of line changes for each table to 0
            # calculate # of games in current table
            numGames = math.floor(len(teams[i])/2)-1
            try:
                # assures the table is filled with totals
                if numTotalsinTables[i] == len(teams[i]):
                    # makes sure we're comparing equally long teams/lines variables
                    if (len(prevTeams[i]) == len(teams[i])) and (len(prevLines[i]) == len(lines[i])):
                        for j in range(numGames):  # Loop through each game in current table
                            print(
                                f'{i}{j}: {teams[i][2*j]}({lines[i][4*j]})({lines[i][4*j+1]}) || ({prevLines[i][4*j]})({prevLines[i][4*j+1]})')
                            # checks that we're comparing correct teams and compares LINE values
                            if teams[i][2*j] == prevTeams[i][2*j] and lines[i][4*j] != prevLines[i][4*j]:
                                # limits amt of notifications sent per table each iteration (for when removing live lines doesn't work)
                                if tableLineChanges < 3:
                                    msg = f'Line Move: {prevTeams[i][2*j]}: ({prevLines[i][4*j]}) to ({lines[i][4*j]})'
                                    sendNotificationToDiscord(msg)
                                    numLineMoves = numLineMoves + 1
                                    tableLineChanges = tableLineChanges + 1
                            # checks that we're comparing correct teams and compares TOTAL values
                            if teams[i][2*j] == prevTeams[i][2*j] and lines[i][4*j+1] != prevLines[i][4*j+1]:
                                if tableLineChanges < 3:
                                    msg = f'Total Move: {prevTeams[i][2*j]}: ({prevLines[i][4*j+1]}) to ({lines[i][4*j+1]})'
                                    sendNotificationToDiscord(msg)
                                    numLineMoves = numLineMoves + 1
                                    tableLineChanges = tableLineChanges + 1

                # Check to make sure no totals are in current table
                if numTotalsinTables[i] == 0:
                    if (len(prevTeams[i]) == len(teams[i])) and (len(prevLines[i]) == len(lines[i])):
                        for j in range(numGames):
                            # print(
                            #     f'{i}{j}: {teams[i][2*j]}({lines[i][2*j]}) || ({prevLines[i][2*j]})')
                            if teams[i][2*j] == prevTeams[i][2*j] and lines[i][2*j] != prevLines[i][2*j]:
                                if tableLineChanges < 3:
                                    msg = f'Line Move: {prevTeams[i][2*j]}: ({prevLines[i][2*j]}) to ({lines[i][2*j]})'
                                    sendNotificationToDiscord(msg)
                                    numLineMoves = numLineMoves + 1
                                    tableLineChanges = tableLineChanges + 1
            except Exception as e:
                sendNotificationToDiscord(e)
                sendNotificationToDiscord(
                    'Script errored out.  Attempting to reset.')
                noCopyCount = noCopyCount + 1

                time.sleep(repRateInS)

    if noCopyCount == 0 or noCopyCount > 1:
        # Copy current lines to "previos" variables for check on next iteration
        prevTeams = teams[:]
        prevLines = lines[:]
        prevNumTotalsInTables = numTotalsinTables[:]
        if noCopyCount > 1:
            noCopyCount = 0

    if reqCount > 0:
        print(
            f'\nNumber of Line Moves: {numLineMoves}\n  Will check again in {round(repRateInS, 2)} s')
        print(f'Runtime: {round(repRateInS*reqCount,2)} seconds')
        print('\n///////////////////////////////////////////////////////')
    else:
        print(f'Will check for line changes in {round(repRateInS, 2)} s.')
        print('\n///////////////////////////////////////////////////////')

    reqCount = reqCount + 1
    time.sleep(repRateInS)  # delay for the while loop
