import requests
import json
import csv
import os
os.getcwd()

if __name__ == '__main__':

    def exportJSON(file, name):
        with open(name + '_data.json', 'w', encoding='utf-8') as jsonfile:
            json.dump(file, jsonfile, ensure_ascii=False, indent=4)

    # To return owned games in STEAM form the URL with the following strings
    steamLink = 'http://api.steampowered.com/'
    ownedGames = 'IPlayerService/GetOwnedGames/v1?'
    # Put in your Steam Key
    steamKey = '&key=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
    # Put in your Steam ID
    steamID = '&steamid=XXXXXXXXXXXXXXXXX'
    textFormat = '&format=json'
    appInfo ='&include_appinfo=True'
    freeGames ='&include_played_free_games=True'

    # Return owned STEAM games in JSON
    getOwnedGames = requests.get(steamLink
                             + ownedGames
                             + steamKey
                             + steamID
                             + textFormat
                             + appInfo
                             + freeGames)
    exportJSON(getOwnedGames.json(), name='owned_games_steam')


    # OPTIONAL: Get the STEAM level and badge level of the user
    steamLevel ='IPlayerService/GetSteamLevel/v1?'
    badgeLevel ='IPlayerService/GetBadges/v1?'

    getSteamLevel = requests.get(steamLink + steamLevel + steamID + steamKey)
    getBadgeLevel = requests.get(steamLink + badgeLevel + steamID + steamKey)
    exportJSON([getSteamLevel.json(),getBadgeLevel.json()], name='user_level_steam')


    # OPTIONAL: Get recently played STEAM games
    recentlyPlayed = 'IPlayerService/GetRecentlyPlayedGames/v1?'

    getRecentlyPlayed = requests.get(steamLink + recentlyPlayed + steamID + steamKey)
    exportJSON(getRecentlyPlayed.json(), name='recently_played_steam')



    # Return reviews of owned STEAM games in JSON
    gameID = '238960'

    getGameReview = requests.get('https://store.steampowered.com/appreviews/' + gameID + '?json=1&language=all&purchase_type=all')
    exportJSON(getGameReview.json(), name='game_review')
    # &review_type=positive

    # getGameDetails = requests.get('https://store.steampowered.com/api/appdetails?appids=' + gameID)


    # with open('data.json') as jsonfile:
    #     jsonData = json.load(jsonfile)
    #
    # dataFileCsv = open('data.csv', 'w', newline='')
    # csvWriter = csv.writer(dataFileCsv)
    #
    # count = 0
    # for data in jsonData:
    #     if count == 0:
    #         header = data.keys()
    #         csvWriter.writerow(header)
    #         count += 1
    #         csvWriter.writerow(data.values())
    # dataFileCsv.close()


    # with open(args.fileCSV, 'w', encoding='utf-8', newline='') as csvfile:
    #     writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=args.delimiter)
    #     writer.writeheader()

