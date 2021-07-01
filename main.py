import requests
import json
import csv
import os
import math
from hltbapi import HtmlScraper
os.getcwd()

if __name__ == '__main__':

    # Export file to JSON
    def exportJSON(file, name):
        with open(name + '_data.json', 'w', encoding='utf-8') as jsonfile:
            json.dump(file, jsonfile, ensure_ascii=False, indent=4)

    # Return review numbers of owned STEAM games
    def getGameReviews(gameID):
        gameReviews = (requests.get('https://store.steampowered.com/appreviews/'
                            + gameID
                            + '?json=1&language=all&purchase_type=all').json())         # &review_type=positive
        totalVotes = gameReviews['query_summary']['total_reviews']
        totalPositive = gameReviews['query_summary']['total_positive']
        totalNegative = gameReviews['query_summary']['total_negative']
        reviewScore = totalPositive/totalVotes
        rating = reviewScore-(reviewScore-0.5) * math.pow(2, - math.log10(totalVotes + 1))
        return(' Total Votes: ' + str(totalVotes) + ', '
               + ' Total Positive: ' + str(totalPositive) + ', '
               + ' Total Negative: ' + str(totalNegative) + ', '
               + ' Steam Score(%): ' + str(round(reviewScore*100)) + ', '
               + ' Steam db Score(%): ' + str(round(rating*100))
               )

    # Scrap expected game length times per play style from How Long to Beat website
    def getHowLongToBeat(name):
        howLongToBeat = HtmlScraper().search(name)[0]
        gameLengths = 'Main Story(h): ' + str(howLongToBeat.gameplayMain) + ', '\
                      + 'Extra(h): ' + str(howLongToBeat.gameplayMainExtra) + ', '\
                      + 'Complete(h): ' + str(howLongToBeat.gameplayCompletionist) + ', '
        return str(gameLengths)

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

    # Return owned STEAM games list
    getOwnedGames = (requests.get(steamLink + ownedGames + steamKey + steamID + textFormat + appInfo
                                  + freeGames)).json()
    exportJSON(getOwnedGames, name='owned_games_steam')


    # Get the total count of Steam games
    gamesTotal = "Total Steam game count: " + str(getOwnedGames['response']['game_count'])
    # Get the game IDs, names, total playtime per title, total vote numbers, total positive and negative numbers
    gameItems = []

    for count, item in enumerate(getOwnedGames['response']['games'], 1):
        gameItems.append(str(count) + ', '
                         + 'ID: ' + str(item['appid']) + ', '
                         + ' name: ' + str(item['name']) + ', '
                         + ' Steam Playtime(h): ' + str(item['playtime_forever']) + ', '
                         + getHowLongToBeat(name=(str(item['name'])))
                         + str(getGameReviews(str(item['appid'])))
                         )

        print(gameItems)


    # Export to JSON file
    exportJSON((gamesTotal, gameItems), name='game_list')



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

    #OPTIONAL: Get game's Steam page details
    gamePageID = '12370'
    getGameDetails = requests.get('https://store.steampowered.com/api/appdetails?appids=' + gamePageID)
    exportJSON(getGameDetails.json(), name='game_details')




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

