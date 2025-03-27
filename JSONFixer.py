import os, json


fixType = 'accessory/scarf'
done = ['hair', 'coat', 'bottom', 'leglet', 'hosiery', 'makeup', 'dress', 'top', 'accessory/scarf', 'shoes', 'accessory/earrings', 'accessory/necklace', 'accessory/right-hand-ornament', 'accessory/left-hand-ornament', 'accessory/gloves']
fixFile = './itemJSONs/{}.json'.format(fixType)
itemDict = {}

def sortType():
    leglets = {}
    hosierys = {}
    if os.path.isfile(fixFile):
        with open(fixFile, 'r') as f:
            itemDict = json.loads(f.read())
    else:
        print('{} is not a valid file'.format(fixFile))
        return
    for itemId in itemDict:
        indItem = itemDict[itemId]
        if 'leglet' in indItem['tags']:
            indItem['itemSubType'] = 'leglet'
            indItem['itemType'] = 'hosiery'
            leglets[itemId] = indItem
            print(indItem)
        else:
            indItem['itemSubType'] = 'hosiery'
            indItem['itemType'] = 'hosiery'
            hosierys[itemId] = indItem
    with open('./itemJSONs/hosiery2.json', 'w') as f:
        f.write(json.dumps(hosierys))
    with open('./itemJSONs/leglet.json', 'w') as f:
        f.write(json.dumps(leglets))
        
def addSubType(fixT=None):
    if not fixT:
        fixT = fixType
    fixFile = './itemJSONs/{}.json'.format(fixT)
    print('fixFile {}'.format(fixFile))
    if os.path.isfile(fixFile):
        with open(fixFile, 'r', encoding='utf-8') as f:
            itemDict = json.loads(f.read())
    else:
        print('{} is not a valid file'.format(fixFile))
        return
    if '/' in fixT:
        fixTypes = fixT.split('/')
        itemType = fixTypes[0]
        itemSubType = fixTypes[1]
    else:
        itemType = fixT
        itemSubType = fixT
    for itemId in itemDict:
        itemDict[itemId]['itemType'] = itemType
        itemDict[itemId]['itemSubType'] = itemSubType
        #print(itemDict[itemId])
    
    with open(fixFile, 'w', encoding='utf-8') as f:
        f.write(json.dumps(itemDict))
        
def craftingCharToNum():
    if os.path.isfile(fixFile):
        with open(fixFile, 'r', encoding='utf-8') as f:
            itemDict = json.loads(f.read())
    else:
        print('{} is not a valid file'.format(fixFile))
        return
    for itemId in itemDict:
        if 'used-to-craft' in itemDict[itemId]:
            for craftItemId in itemDict[itemId]['used-to-craft']:
                numOfItems = itemDict[itemId]['used-to-craft'][craftItemId]
                itemDict[itemId]['used-to-craft'][craftItemId] = int(numOfItems)
        if 'crafted-from' in itemDict[itemId]:
            for craftItemId in itemDict[itemId]['crafted-from']:
                numOfItems = itemDict[itemId]['crafted-from'][craftItemId]
                itemDict[itemId]['crafted-from'][craftItemId] = int(numOfItems)
    
    
    with open(fixFile, 'w', encoding='utf-8') as f:
        f.write(json.dumps(itemDict))

craftingCharToNum()
for don in done:
    print(don)
    addSubType(don)