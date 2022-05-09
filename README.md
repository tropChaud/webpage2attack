# [webpage2attack.py](https://github.com/tropChaud/webpage2attack/blob/main/app/webpage2attack.py)

## About
Python3 script to generate portable TTP intelligence from a web-based report

Tallies explicit mentions of MITRE ATT&CK (sub)techniques (e.g. T1027 or T1027.001) on a single html webpage, and outputs a .json file compatible for use with the [ATT&CK Navigator](https://mitre-attack.github.io/attack-navigator/) visualization tool.

## Required Python Libraries
* [Python Requests](https://docs.python-requests.org/en/latest/user/install/#install)
* [Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup)

## Run
<code>python3 mitre2attack.py -u [your url]</code>

## Anticipated Use Case
Quickly extract TTP identifiers from a given technical report, for threat intelligence analysis, visualization, and operationalization (e.g. paste the output json content in the Threat Intelligence dropdown [here](https://controlcompass.github.io/risk) to identify potentially relevant controls aligned with each TTP).

*MITRE ATT&CK® is a registered trademark of The MITRE Corporation*
