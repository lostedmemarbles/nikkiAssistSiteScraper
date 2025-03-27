from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import re
import os
import sys
import json

done = ['hair', 'coat', 'bottom', 'hosiery/leglet', 'hosiery/hosiery', 'makeup', 'dress', 'top', 'accessory/scarf', 'shoes', 'accessory/earrings', 'accessory/necklace', 'accessory/right-hand-ornament', 'accessory/left-hand-ornament', 'accessory/gloves']
#, 'accessory/both-handheld'
#


#running:, 'accessory/hair-ornament', 'accessory/right-handheld', 'accessory/left-handheld'
#, 'accessory/waist-decoration', 'accessory/veil', 'accessory/face-accessory'
#, 'accessory/brooch', 'accessory/tattoo', 'accessory/wing', 'accessory/hairpin'
#, 'accessory/tail', 'accessory/foreground', 'accessory/background', 'accessory/ear'
#, 'accessory/head-ornament'
#not:
#,
#, 'accessory/ground', 'accessory/skin', 'soul',
#'suit'
nikkiInfoBaseURL = 'https://ln.nikkis.info' #  
mainTypes = sys.argv[1:]#[];
titles = ['tags', 'description', 'rarity', 'attributes', 'suit', 'obtained-from']

itemIds = []

def cleanUpTags(tag):
    return tag.split('#')[1].split('"')[0]
    
def cleanUpSuit(suit):
    suitSplit = suit.split('/')
    return suitSplit[len(suitSplit)-1]

def cleanUpTitle(tit):
    return tit.lower().replace(' ', '-')

def saveIdFile(typeName, itemIdList):
    with open('./itemIds/{}.id'.format(typeName), 'w') as f:
        f.write(itemIdList)

def itemIdFileExists(typeName):
    return os.path.isfile('./itemIds/{}.id'.format(typeName))

def scrapeItemPage(itemId, baseSite, jsonLoc):
    itemDict = {}
    if os.path.isfile(jsonLoc):
        with open(jsonLoc, 'r') as g:
            itemDict = json.loads(g.read())
    if itemId in itemDict:
        return
    op = webdriver.ChromeOptions()
    op.add_argument('headless')
    driver = webdriver.Chrome(options=op)
    fullSite = '{}/{}'.format(baseSite, re.search('[0-9]+', itemId).group())
    print('fullSite')
    print(fullSite)
    driver.get(fullSite)
    
    newItem = {}
    newItem['name'] = driver.find_element(By.CLASS_NAME, 'header.pink-text.text-lighten-2').text.replace('arrow_upward', '')
    newItem['idNum'] = re.search('[0-9]+', itemId).group()
    newItem['idChar'] = re.search('[A-Z]+', itemId).group()
    
    sections = driver.find_elements(By.CLASS_NAME, 'section')
    for sect in sections:
        sectTitle = cleanUpTitle(sect.find_element(By.CLASS_NAME, 'item-section-head').text)
        sectLinks = sect.find_elements(By.TAG_NAME, 'a')
        if sectTitle == 'tags':
            newItem['tags'] = []
            for sectLink in sectLinks:
                newItem['tags'].append(cleanUpTags(sectLink.get_attribute('href')))
            #print('tags')
            #print(newItem['tags'])
            continue
        if sectTitle == 'description':
            newItem['description'] = sect.find_element(By.CLASS_NAME, 'flow-text').text
            continue
        if sectTitle == 'rarity':
            newItem['rarity'] = len(sect.find_elements(By.TAG_NAME, 'i'))
            continue
        if sectTitle == 'attributes':
            attNames = sect.find_elements(By.CLASS_NAME, 'cloth-attr')
            attGrades = sect.find_elements(By.CLASS_NAME, 'cloth-grade')
            newItem['attributes'] = {}
            for i in range(5):
                newItem['attributes'][attNames[i].text.strip()] = attGrades[i].text.strip()
            continue
        if sectTitle == 'suit':
            newItem['suit'] = []
            for sectLink in sectLinks:
                newItem['suit'].append(cleanUpSuit(sectLink.get_attribute('href')))
            continue
        if sectTitle == 'obtained-from':
            newItem['obtained-from'] = []
            sectLinks = sect.find_elements(By.TAG_NAME, 'li')
            for sectLink in sectLinks:
                newItem['obtained-from'].append(sectLink.text)
            continue
        if sectTitle == 'special-attributes':
            newItem['special-attributes'] = []
            sectLinks = sect.find_elements(By.CLASS_NAME, 'special-attr')
            for sectLink in sectLinks:
                newItem['special-attributes'].append(sectLink.text)
            continue
        if sectTitle == 'customization':
            newItem['customization'] = []
            for sectLink in sectLinks:
                newItem['customization'].append(cleanUpSuit(sectLink.get_attribute('href')))
            continue
        if sectTitle == 'used-to-craft':
            sectLinks = sect.find_elements(By.CLASS_NAME,  'collection-item.witem.avatar.icon-room.col.s12.m6.l6')
            newItem['used-to-craft'] = {}
            for sectLink in sectLinks:
                itemIdd = sectLink.get_attribute('wid')
                #print('::')
                #print(itemIdd)
                #print('::')
                newItem['used-to-craft'][itemIdd] = re.search('[0-9]+', sectLink.find_element(By.TAG_NAME, 'p').text).group()
            continue
        if sectTitle == 'crafted-from':
            sectLinks = sect.find_elements(By.CLASS_NAME, 'collection-item.witem.avatar.icon-room.col.s12.m6.l6')
            newItem['crafted-from'] = {}
            for sectLink in sectLinks:
                newItem['crafted-from'][sectLink.get_attribute('wid')] = re.search('[0-9]+', sectLink.find_element(By.CLASS_NAME, 'secondary-content').text).group()
            continue
            
    #print()
    #print(newItem)
    itemDict[itemId] = newItem
    #print()
    
    
    driver.quit()
    with open(jsonLoc, 'w') as g:
        g.write(json.dumps(itemDict))
        

def scrapeItemPages():
    print(mainTypes)
    for mainType in mainTypes:
        filePath = './itemIds/{}.id'.format(mainType)
        jsonFileLocation = './itemJSONs/{}.json'.format(mainType)
        if 'accessory' in mainType:
            mainType = 'accessory'
        baseSite = '{}/wardrobe/{}'.format(nikkiInfoBaseURL, mainType)
        print('baseSite')
        print(baseSite)
        with open(filePath, 'r') as ff:
            itemIdList = eval(ff.read())
        for itemId in itemIdList:
            scrapeItemPage(itemId, baseSite, jsonFileLocation)
            #break
        

def getItemIdFiles():
    driver = webdriver.Chrome()
    
    for mainType in mainTypes:
        if itemIdFileExists(mainType):
            continue
        itemIds = []
        driver.get('{}/wardrobe/{}'.format(nikkiInfoBaseURL, mainType))
        itemDiv = driver.find_element(By.CLASS_NAME, 'collection.row')
        itemLinkEls = itemDiv.find_elements(By.TAG_NAME, 'a')
        print(len(itemLinkEls))
        
        for itemLinkEl in itemLinkEls:
            itemId = itemLinkEl.get_attribute('wid')
            itemIds.append(itemId)
        print()
        print(itemIds)
        print()
        saveIdFile(mainType, str(itemIds))
    driver.quit()
        
    
scrapeItemPages()