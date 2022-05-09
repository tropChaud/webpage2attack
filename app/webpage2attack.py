import argparse
import requests
from bs4 import BeautifulSoup
import re
from collections import Counter
import json
import sys

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--url', dest='url', required=True,
                    help='Input webpage URL, e.g. https://thedfirreport.com/2022/04/25/quantum-ransomware/')

# Get webpage
url = parser.parse_args().url
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
title = soup.title.string

# Regex for ATT&CK sub-techniques & techniques (e.g. T1027 or T1027.001)
reg = re.compile('(T1\d{3}\.\d{3}|T1\d{3})')

# Matches for regex
match = re.findall(reg, soup.get_text())

tech_list = []
for i in match:
    tech_list.append(i)

# If any matches are found, continue the program
if tech_list:

    # Base formatting for the MITRE ATT&CK Navigator "layer" json file. Configured according to the author's
    # preferences, but many modification options exist:
    # https://github.com/mitre-attack/attack-navigator/blob/master/USAGE.md#layer-controls
    layer = {
        'name': title,
        'versions': {
            'attack': '11',
            'navigator': '4.6.1',
            'layer': '4.3'
        },
        'domain': 'enterprise-attack',
        'description': 'Heatmap of (sub)techniques mentioned in "' + title + '".\n\nSource: ' + url,
        'techniques': [],
        'layout': {
            'layout': 'side',
            'aggregateFunction': 'max',
            'showID': False,
            'showName': True,
            'showAggregateScores': True,
            'countUnscored': False
        },
    }

    # Tally the number of times each (sub)technique was mentioned
    for techID, count in Counter(tech_list).items():
        # Populate the layer file with the mentioned techniques and their tallies
        technique = {
            'techniqueID': techID,
            'score': int(count)
        }
        layer['techniques'].append(technique)

    # Layer file color gradient formatting
    layer['gradient'] = {
        'colors': [
            '#ffffff',
            '#ff6666'
        ],
        'minValue': 0,
        'maxValue': max([technique['score'] for technique in layer['techniques']])
    }

    # Account for the most common special characters in webpage titles that create errors when creating the
    # output json file
    specialChars = '<>:"/\|?*'
    for specialChar in specialChars:
        title = title.replace(specialChar, '')
    try:
        layerOut_name = title + '.json'
        layerOut = open(layerOut_name, 'w')
    # If there are other characters present that create errors creating the file, use a generic filename
    except OSError:
        layerOut_name = 'webpage2attack_heatmap.json'
        layerOut = open(layerOut_name, 'w')

    # Write the processed data to the output json file
    json.dump(layer, layerOut, indent=4)
    print('\nHeatmap file "' + layerOut_name + '" created. Done')
    sys.exit(0)

# If no regex matches for techniques are found on the webpage, end the program
else:
    print('\nNo techniques extracted from webpage. Ending program')
    sys.exit(0)
