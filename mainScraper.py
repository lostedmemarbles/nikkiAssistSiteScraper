from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import re
import os

nikkiInfoBaseURL = 'https://ln.nikkis.info'
mainTypes = ['hair', 'dress', 'coat', 'top', 'bottom', 'hosiery', 'shoes', 'makeup', 'accessory/hair-ornament', 'accessory/earrings', 'accessory/scarf', 'accessory/necklace', 'accessory/right-hand-ornament', 'accessory/left-hand-ornament', 'accessory/gloves', 'accessory/right-handheld', 'accessory/left-handheld', 'accessory/both-handheld', 'accessory/waist-decoration', 'accessory/veil', 'accessory/face-accessory', 'accessory/brooch', 'accessory/tattoo', 'accessory/wing', 'accessory/tail', 'accessory/foreground', 'accessory/background', 'accessory/hairpin', 'accessory/ear', 'accessory/head-ornament', 'accessory/ground', 'accessory/skin', 'soul', 'suit'];

itemTypeToLinks = {'H': 'hair'}
itemIds = []


def saveIdFile(typeName, itemIdList):
    with open('./itemIds/{}.id'.format(typeName), 'w') as f:
        f.write(itemIdList)

def itemIdFileExists(typeName):
    return os.path.isfile('./itemIds/{}.id'.format(typeName))

def getURLFromItemId(itemId):
    return 'https://ln.nikkis.info/wardrobe/{}/{}'.format(itemTypeToLinks[re.search('[A-Z]+', itemId).group()], re.search('[0-9]+', itemId).group())


def getItemIdFiles():
    driver = webdriver.Chrome()
    
    for mainType in mainTypes:
        if itemIdFileExists(mainType):
            continue
        itemIds = []
        driver.get('https://ln.nikkis.info/wardrobe/{}'.format(mainType))
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
        
    
getItemIdFiles()