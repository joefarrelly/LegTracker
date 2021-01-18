from dotenv import load_dotenv
load_dotenv()
import os
import numpy as np

from blizz import *

import pandas as pd
from gspread_pandas import Spread
from gspread_pandas.conf import get_config
from gspread_formatting import *
from ratelimit import limits, sleep_and_retry

import json
import time

wowClasses = [
    '',
    'Warrior',
    'Paladin',
    'Hunter',
    'Rogue',
    'Priest',
    'Death Knight',
    'Shaman',
    'Mage',
    'Warlock',
    'Monk',
    'Druid',
    'Demon Hunter'
]

armour = [
    "Name",
    "Class",
    "Head",
    "Shoulder",
    "Chest",
    "Wrist",
    "Hand",
    "Waist",
    "Legs",
    "Feet"
]

armourCape = armour.copy()
armourCape.insert(4,"Back")
misc = [
    "Name",
    "Class",
    "Neck",
    "Ring"
]

start = time.perf_counter()

class AltClass(object):
    def __init__(self,altId,altName,altRealm,altClass,altRank,altProfession1=None,altProfession1Data=None,altProfession2=None,altProfession2Data=None): 
        DEFAULT_PROF='Missing'
        self.altId=altId
        self.altName=altName
        self.altRealm=altRealm
        self.altClass=altClass
        self.altRank=altRank
        self.altProfession1=altProfession1 if altProfession1 is not None else DEFAULT_PROF
        self.altProfession1Data=altProfession1Data if altProfession1Data is not None else DEFAULT_PROF
        self.altProfession2=altProfession2 if altProfession2 is not None else DEFAULT_PROF
        self.altProfession2Data=altProfession2Data if altProfession2Data is not None else DEFAULT_PROF

try:
    BLIZZ_CLIENT=os.getenv("BLIZZ_CLIENT")
    BLIZZ_SECRET=os.getenv("BLIZZ_SECRET")
    SPREADSHEET_KEY=os.getenv("SPREADSHEET_KEY")
    REALM=os.getenv("REALM")
    GUILD=os.getenv("GUILD")
    RANKS=os.getenv("RANKS").split(".")
except KeyError:
    print("Environment variables not set correctly") 

trackedAlts = []
legCloth = []
legLeather = []
legMail = []
legPlate = []
legJewel = []

token = getToken(BLIZZ_CLIENT,BLIZZ_SECRET)
roster = getRoster(token,REALM,GUILD)
rosterSize = len(roster)

for counter, alt in enumerate(roster, start = 1):
    print(str(counter) + "/" + str(rosterSize))
    tempAlt = AltClass(
        alt['character']['id'],
        alt['character']['name'],
        alt['character']['realm']['slug'],
        wowClasses[alt['character']['playable_class']['id']],
        alt['rank']
        )
    professions = getProfessions(token,alt['character']['name'],alt['character']['realm']['slug'])
    if professions != None:
        for counter, prof in enumerate(professions):
            if counter == 0:
                tempAlt.altProfession1 = prof['profession']['name']
                for expac in prof['tiers']:
                    if "Shadowlands" in expac['tier']['name']:
                        tempAlt.altProfession1Data = expac['known_recipes']
            elif counter == 1:
                tempAlt.altProfession2 = prof['profession']['name']
                for expac in prof['tiers']:
                    if "Shadowlands" in expac['tier']['name']:
                        tempAlt.altProfession2Data = expac['known_recipes']
    trackedAlts.append(tempAlt)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
spread = Spread(SPREADSHEET_KEY,config=get_config(os.getcwd(),'client_secret.json'))

for alt in trackedAlts:
    # CLOTH LEGGO
    if ((alt.altProfession1 == "Tailoring") and (alt.altProfession1Data != "Missing")) or ((alt.altProfession2 == "Tailoring") and (alt.altProfession2Data != "Missing")):
        if alt.altProfession1 == "Tailoring":
            searchData = alt.altProfession1Data
        elif alt.altProfession2 == "Tailoring":
            searchData = alt.altProfession2Data
        head = sum(1 if x['name'] == "Grim-Veiled Hood" else 0 for x in searchData)
        shoulder = sum(1 if x['name'] == "Grim-Veiled Spaulders" else 0 for x in searchData)
        back = sum(1 if x['name'] == "Grim-Veiled Cape" else 0 for x in searchData)
        chest = sum(1 if x['name'] == "Grim-Veiled Robe" else 0 for x in searchData)
        wrist = sum(1 if x['name'] == "Grim-Veiled Bracers" else 0 for x in searchData)
        hand = sum(1 if x['name'] == "Grim-Veiled Mittens" else 0 for x in searchData)
        waist = sum(1 if x['name'] == "Grim-Veiled Belt" else 0 for x in searchData)
        legs = sum(1 if x['name'] == "Grim-Veiled Pants" else 0 for x in searchData)
        feet = sum(1 if x['name'] == "Grim-Veiled Sandals" else 0 for x in searchData)
        if head > 0:
            legCloth.append([alt.altName,alt.altClass,head,shoulder,back,chest,wrist,hand,waist,legs,feet])

    # LEATHER AND MAIL LEGGO
    if ((alt.altProfession1 == "Leatherworking") and (alt.altProfession1Data != "Missing")) or ((alt.altProfession2 == "Leatherworking") and (alt.altProfession2Data != "Missing")):
        if alt.altProfession1 == "Leatherworking":
            searchData = alt.altProfession1Data
        elif alt.altProfession2 == "Leatherworking":
            searchData = alt.altProfession2Data
        head = sum(1 if x['name'] == "Umbrahide Helm" else 0 for x in searchData)
        shoulder = sum(1 if x['name'] == "Umbrahide Pauldrons" else 0 for x in searchData)
        chest = sum(1 if x['name'] == "Umbrahide Vest" else 0 for x in searchData)
        wrist = sum(1 if x['name'] == "Umbrahide Armguards" else 0 for x in searchData)
        hand = sum(1 if x['name'] == "Umbrahide Gauntlets" else 0 for x in searchData)
        waist = sum(1 if x['name'] == "Umbrahide Waistguard" else 0 for x in searchData)
        legs = sum(1 if x['name'] == "Umbrahide Leggings" else 0 for x in searchData)
        feet = sum(1 if x['name'] == "Umbrahide Treads" else 0 for x in searchData)
        if head > 0:
            legLeather.append([alt.altName,alt.altClass,head,shoulder,chest,wrist,hand,waist,legs,feet])

        head = sum(1 if x['name'] == "Boneshatter Helm" else 0 for x in searchData)
        shoulder = sum(1 if x['name'] == "Boneshatter Pauldrons" else 0 for x in searchData)
        chest = sum(1 if x['name'] == "Boneshatter Vest" else 0 for x in searchData)
        wrist = sum(1 if x['name'] == "Boneshatter Armguards" else 0 for x in searchData)
        hand = sum(1 if x['name'] == "Boneshatter Gauntlets" else 0 for x in searchData)
        waist = sum(1 if x['name'] == "Boneshatter Waistguard" else 0 for x in searchData)
        legs = sum(1 if x['name'] == "Boneshatter Greaves" else 0 for x in searchData)
        feet = sum(1 if x['name'] == "Boneshatter Treads" else 0 for x in searchData)
        if head > 0:
            legMail.append([alt.altName,alt.altClass,head,shoulder,chest,wrist,hand,waist,legs,feet])

    # PLATE LEGGO
    if ((alt.altProfession1 == "Blacksmithing") and (alt.altProfession1Data != "Missing")) or ((alt.altProfession2 == "Blacksmithing") and (alt.altProfession2Data != "Missing")):
        if alt.altProfession1 == "Blacksmithing":
            searchData = alt.altProfession1Data
        elif alt.altProfession2 == "Blacksmithing":
            searchData = alt.altProfession2Data
        head = sum(1 if x['name'] == "Shadowghast Helm" else 0 for x in searchData)
        shoulder = sum(1 if x['name'] == "Shadowghast Pauldrons" else 0 for x in searchData)
        chest = sum(1 if x['name'] == "Shadowghast Breastplate" else 0 for x in searchData)
        wrist = sum(1 if x['name'] == "Shadowghast Armguards" else 0 for x in searchData)
        hand = sum(1 if x['name'] == "Shadowghast Gauntlets" else 0 for x in searchData)
        waist = sum(1 if x['name'] == "Shadowghast Waistguard" else 0 for x in searchData)
        legs = sum(1 if x['name'] == "Shadowghast Greaves" else 0 for x in searchData)
        feet = sum(1 if x['name'] == "Shadowghast Sabatons" else 0 for x in searchData)
        if head > 0:
            legPlate.append([alt.altName,alt.altClass,head,shoulder,chest,wrist,hand,waist,legs,feet])

    # JEWEL LEGGO
    if ((alt.altProfession1 == "Jewelcrafting") and (alt.altProfession1Data != "Missing")) or ((alt.altProfession2 == "Jewelcrafting") and (alt.altProfession2Data != "Missing")):
        if alt.altProfession1 == "Jewelcrafting":
            searchData = alt.altProfession1Data
        elif alt.altProfession2 == "Jewelcrafting":
            searchData = alt.altProfession2Data
        neck = sum(1 if x['name'] == "Shadowghast Necklace" else 0 for x in searchData)
        ring = sum(1 if x['name'] == "Shadowghast Ring" else 0 for x in searchData)
        if neck > 0:
            legJewel.append([alt.altName,alt.altClass,neck,ring])

# if any category has no data add one row containing '-' characters 
# **allows a dataframe to be created using pandas, avoids errors later on**

if not legCloth:
    legCloth.append(np.full(11,'-'))
if not legLeather:
    legLeather.append(np.full(10,'-'))
if not legMail:
    legMail.append(np.full(10,'-'))
if not legPlate:
    legPlate.append(np.full(10,'-'))
if not legJewel:
    legJewel.append(np.full(4,'-'))

# create a pandas dataframe for each legendary category 
clothFrame = pd.DataFrame(data=legCloth,columns=armourCape)
leatherFrame = pd.DataFrame(data=legLeather,columns=armour)
mailFrame = pd.DataFrame(data=legMail,columns=armour)
plateFrame = pd.DataFrame(data=legPlate,columns=armour)
jewelFrame = pd.DataFrame(data=legJewel,columns=misc)

#use spread to upload the dataframes to the corresponding worksheets
print("Uploading 1/5")
spread.df_to_sheet(clothFrame, index=False, sheet='Cloth', replace=True)
print("Uploading 2/5")
spread.df_to_sheet(leatherFrame, index=False, sheet='Leather', replace=True)
print("Uploading 3/5")
spread.df_to_sheet(mailFrame, index=False, sheet='Mail', replace=True)
print("Uploading 4/5")
spread.df_to_sheet(plateFrame, index=False, sheet='Plate', replace=True)
print("Uploading 5/5")
spread.df_to_sheet(jewelFrame, index=False, sheet='Jewel', replace=True)

#cellFormat object for the heading of the table in each worksheet
head = cellFormat(
    backgroundColor=color.fromHex('#999999'),
    textFormat=textFormat(bold=True, foregroundColor=color.fromHex('#000000')),
    horizontalAlignment='CENTER',
    borders=borders(border('solid'),border('solid'),border('solid'),border('solid'))
    )

'''
cellFormat object for the rest of the table in each worksheet
'''
body = cellFormat(
    backgroundColor=color.fromHex('#ffffff'),
    textFormat=textFormat(bold=False,foregroundColor=color.fromHex('#000000')),
    horizontalAlignment='CENTER',
    borders=borders(border('solid'),border('solid'),border('solid'),border('solid'))
    )

conditions = [
    ['rank','NUMBER_EQ','0','#ea9999'],                         # not learned
    ['rank','NUMBER_EQ','1','#f9cb9c'],                         # rank 1
    ['rank','NUMBER_EQ','2','#ffe599'],                         # rank 2
    ['rank','NUMBER_EQ','3','#b6d7a8'],                         # rank 3
    ['rank','NUMBER_EQ','4','#a2c4c9'],                         # rank 4
    ['name','CUSTOM_FORMULA','=$B2="Death Knight"','#c41e3a'],  # death knight
    ['name','CUSTOM_FORMULA','=$B2="Demon Hunter"','#a330c9'],  # demon hunter
    ['name','CUSTOM_FORMULA','=$B2="Druid"','#ff7c0a'],         # druid
    ['name','CUSTOM_FORMULA','=$B2="Hunter"','#aad372'],        # hunter
    ['name','CUSTOM_FORMULA','=$B2="Mage"','#3fc7eb'],          # mage
    ['name','CUSTOM_FORMULA','=$B2="Monk"','#00ff98'],          # monk
    ['name','CUSTOM_FORMULA','=$B2="Paladin"','#f48cba'],       # paladin
    ['name','CUSTOM_FORMULA','=$B2="Priest"','#f3f3f3'],        # priest
    ['name','CUSTOM_FORMULA','=$B2="Rogue"','#fff468'],         # rogue
    ['name','CUSTOM_FORMULA','=$B2="Shaman"','#0070dd'],        # shaman
    ['name','CUSTOM_FORMULA','=$B2="Warlock"','#8788ee'],       # warlock
    ['name','CUSTOM_FORMULA','=$B2="Warrior"','#c69b6d']        # warrior

]

# create a list of conditional format rule objects and return the list
def createRules(ranks,names):
    rules = []
    for rule in conditions:
        if rule[0] == 'rank':
            tempRange = ranks
        elif rule[0] == 'name':
            tempRange = names
        newRule = ConditionalFormatRule(
            ranges=[tempRange],
            booleanRule=BooleanRule(
                condition=BooleanCondition(rule[1],[rule[2]]),
                format=CellFormat(backgroundColor=color.fromHex(rule[3]))
                )
            )
        rules.append(newRule)
    return rules

# format worksheets and add conditional format rules
for leggo in ['Cloth','Leather','Mail','Plate','Jewel']:
    worksheet = spread.find_sheet(leggo)
    format_cell_ranges(worksheet, [('1', head), ('2:100', body)])
    set_column_widths(worksheet, [ ('A:B', 100), ('C:K', 65) ])
    sheetRules = get_conditional_format_rules(worksheet)
    if len(sheetRules) == 0:
        ranks = GridRange.from_a1_range('C2:K100', worksheet)
        names = GridRange.from_a1_range('A2:B100', worksheet)
        rules = createRules(ranks,names)
        sheetRules.clear()
        for rule in rules:
            sheetRules.append(rule)
        sheetRules.save()
        print("Conditional formatting has been added")
    else:
        print("Conditional formatting has already been applied")

end = time.perf_counter()
finalTime = end - start
print("Spreadhseet has been updated!")
print("Total time to complete was " + str(finalTime) + " seconds!")