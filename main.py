import requests
import json
import csv
import os
os.getcwd()

import sys

if __name__ == '__main__':

    response = requests.get('http://api.steampowered.com/IPlayerService/GetOwnedGames/v1?key=49FE5495F87DA18C0AAD77FC98F79032&steamid=76561198116938509&format=json&include_appinfo=True')
    # response = requests.get('http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v1?key=49FE5495F87DA18C0AAD77FC98F79032&steamid=76561198116938509&format=json')
    with open('game_data.json', 'w', encoding='utf-8') as jsonfile:
        jsondata = json.dump(response.json(), jsonfile, ensure_ascii=False, indent=4)
    # jsonData =

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

