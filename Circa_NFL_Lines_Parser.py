import requests
import math
import time
from bs4 import BeautifulSoup

url = 'https://apps.apple.com/us/app/circa-sports-iowa/id1585863833/'
response = requests.get(url)

header = {
    'authorization': "Nzk2MDgxNzg5NTU4NDU2MzUx.GgQdGC.ZCqoFX8tlo7RNB5UgZaLJuuMqh7PvaaX-m1fyo"
}

reqCount = 0
prevTeams = []
prevLines = []

# while reqCount < 120:

print('\nParsing Circa NFL Spreads data...')

soup = BeautifulSoup(response.content, 'html.parser')

print(soup.find_all(string='My Bets'))

# # # Find all the rows in the table
# teams = soup.find_all('div', class_="event-cell__name-text")
# lines = soup.find_all(
#     'span', class_="sportsbook-outcome-cell__line")

# numGames = math.floor(len(teams)/2)

# print('\nData Parsed.\n')

# if reqCount > 0:
#     print('Comparing previous odds...\n')
#     for i in range(numGames):
#         print(
#             f'{i}: {teams[2*i].text}({lines[4*i].text})({lines[4*i+1].text}) || ({prevLines[4*i].text})({prevLines[4*i+1].text})')
#         if lines[4*i].text != prevLines[4*i].text:
#             msg = f'Line Move: {prevTeams[2*i].text}({prevLines[4*i].text}) to ({lines[4*i].text})'
#             print("\n******LINE CHANGE********")
#             print(msg)
#             print("*************************")
#             r = requests.post("https://discord.com/api/v9/channels/1166388909618511894/messages",
#                               data={'content': msg}, headers=header)
#         elif lines[4*i+1].text != prevLines[4*i+1].text:
#             msg = f'Total Move: {prevTeams[2*i].text}({prevLines[4*i+1].text}) to ({lines[4*i+1].text})'
#             print("\n******LINE CHANGE********")
#             print(msg)
#             print("*************************")
#             r = requests.post("https://discord.com/api/v9/channels/1166388909618511894/messages",
#                               data={'content': msg}, headers=header)

# prevTeams = teams
# prevLines = lines

# if reqCount > 0:
#     print('\nNo line changes - will check again in 1 min.')
#     print(f'Runtime: {60*reqCount} seconds')
# else:
#     print('Will check for line changes in 1 min.')

# reqCount = reqCount + 1

# time.sleep(60)
