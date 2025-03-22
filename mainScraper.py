from selenium import webdriver

nikkiInfoBaseURL = 'https://ln.nikkis.info'

#wardrobeLinks = ['https://ln.nikkis.info/wardrobe/hair', 'https://ln.nikkis.info/wardrobe/dress', 'https://ln.nikkis.info/wardrobe/coat', 'https://ln.nikkis.info/wardrobe/top', 'https://ln.nikkis.info/wardrobe/bottom', 'https://ln.nikkis.info/wardrobe/hosiery', 'https://ln.nikkis.info/wardrobe/shoes', 'https://ln.nikkis.info/wardrobe/makeup', 'https://ln.nikkis.info/wardrobe/accessory', 'https://ln.nikkis.info/wardrobe/soul', 'https://ln.nikkis.info/wardrobe/suit'];
wardrobeLinks = ['https://ln.nikkis.info/wardrobe/hair']






def scrapeIt():
    driver = webdriver.Chrome()
    
    for wardrobeLink in wardrobeLinks:
        driver.get(wardrobeLink)
        
        
        
        
        driver.quit()
    
    
scrapeIt()