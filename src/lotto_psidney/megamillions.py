from urllib.error import HTTPError
from config import MEGAMILLIONS_URL
from util import strip_xml

import requests
import json


def get_latest_numbers():
    try:
        http_results = requests.get(MEGAMILLIONS_URL).text
    except:
        raise HTTPError

    json_results = json.loads(strip_xml(http_results))
    drawing_details = json_results['Drawing']

    return {"PlayDate": drawing_details['PlayDate'], "Numbers": [drawing_details['N1'], drawing_details['N2'], drawing_details['N3'], drawing_details['N4'], drawing_details['N5']], 'MegaBall': drawing_details['MBall'], 'Megaplier': drawing_details['Megaplier']}

def get_latest_prize():
    try:
        http_results = requests.get(MEGAMILLIONS_URL).text
    except:
        raise HTTPError

    json_results = json.loads(strip_xml(http_results))
    drawing_details = json_results['Jackpot']['CurrentPrizePool']

    return drawing_details


def determine_prize(ticket_numbers, ticket_megaball, ticket_megaplier=False):
    latest_drawing = get_latest_numbers()
    latest_prize = get_latest_prize()
    winning_numbers = latest_drawing['Numbers']
    megaball = latest_drawing['MegaBall']
    megaplier = latest_drawing['Megaplier']

    matches = 0
    for number in ticket_numbers:
        if number in winning_numbers:
            matches+=1

    prize_table = {'n0': 0, 'm0': 2, 'n1':0, 'm1': 4, 'm2': 10, 'n2': 0, 'n3':10, 'm3': 200, 'n4': 500, 'm4': 10000, 'n5': 1000000, 'm5': latest_prize}
    
    if ticket_megaplier == True:
        for key, value in prize_table:
            prize_table[key] = value * megaplier
    
    lookup_key = ""
    if megaball == ticket_megaball:
        lookup_key += 'm'
    else:
        lookup_key += 'n'
    
    lookup_key += str(matches)
    return prize_table[lookup_key]