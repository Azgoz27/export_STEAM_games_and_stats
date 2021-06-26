import requests
import json
import csv
import os
os.getcwd()

if __name__ == '__main__':

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

    # Export in JSON file
    with open('owned_games_steam_data.json', 'w', encoding='utf-8') as jsonfile:
        json.dump(getOwnedGames.json(), jsonfile, ensure_ascii=False, indent=4)


    # # Return reviews of owned STEAM games in JSON
    # response2 = requests.get('https://store.steampowered.com/appreviews/252950?json=1&language=all')


    # OPTIONAL: Get the STEAM level and badge level of the user
    steamLevel ='IPlayerService/GetSteamLevel/v1?'
    badgeLevel ='IPlayerService/GetBadges/v1?'

    getSteamLevel = requests.get(steamLink + steamLevel + steamID + steamKey)
    getBadgeLevel = requests.get(steamLink + badgeLevel + steamID + steamKey)

    # Export in JSON file
    with open('user_level_steam_data.json', 'w', encoding='utf-8') as jsonfile:
        json.dump([getSteamLevel.json(),getBadgeLevel.json()], jsonfile, ensure_ascii=False, indent=4)


    # OPTIONAL: Get recently played STEAM games
    recentlyPlayed = 'IPlayerService/GetRecentlyPlayedGames/v1?'

    getRecentlyPlayed = requests.get(steamLink + recentlyPlayed + steamID + steamKey)

    # Export in JSON file
    with open('recently_played_steam_data.json', 'w', encoding='utf-8') as jsonfile:
        json.dump(getRecentlyPlayed.json(), jsonfile, ensure_ascii=False, indent=4)



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

