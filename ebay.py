import os, json, time
import requests
from datetime import datetime
import pytz

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

def flushDriverCookies(driver, path):
    cookies = json.load(open(path, "r"))

    # Enables network tracking so we may use Network.setCookie method
    driver.execute_cdp_cmd('Network.enable', {})

    # # Iterate through pickle dict and add all the cookies
    for cookie in cookies:
        driver.execute_cdp_cmd('Network.setCookie', cookie)

    # # Disable network tracking
    driver.execute_cdp_cmd('Network.disable', {})
    return 1

def isoToEpoch(iso_string):
    # Parse the ISO 8601 string to a datetime object in UTC
    utc_time = datetime.strptime(iso_string, "%Y-%m-%dT%H:%M:%S.%fZ")
    
    # Localize the UTC datetime object to the UTC timezone
    utc_time = utc_time.replace(tzinfo=pytz.UTC)
    
    # Convert the UTC time to local time
    local_time = utc_time.astimezone()
    
    # Return the epoch time of the local time
    return local_time.timestamp()
def _getStartingAt(txt, startsAt):
    at = txt.find(startsAt)
    if at == -1:
        raise ValueError("Can't find `" + startsAt + "` in text blob")
    return txt[at + len(startsAt):]

def verifySignin(driver):
    driver.get("https://www.ebay.com/mye/myebay/summary")
    return "https://www.ebay.com/mye/myebay/summary" == driver.current_url

def getItemState(idd):
    r = requests.get(f"https://www.ebay.com/itemmodules/{idd}?module_groups=AUTO_REFRESH")
    jso = r.json()
    for state in jso["states"]:
        if state["eventName"] != "ux-app__x-bid-price-section__refreshState": continue
        return {
            "price": state["state"]["model"]["bidPrice"]["value"],
            "bids": state["state"]["model"]["bidInfo"]["bidCount"]["value"],
            "endTime": isoToEpoch(state["state"]["model"]["bidInfo"]["endTime"]["endTime"]["value"])
        }

def _waitForBid(driver):
    while True:
        try: 
            driver.find_element(By.CSS_SELECTOR, "#bid-offer-summary")
            break
        except NoSuchElementException as e:
            time.sleep(0.1)
def enterBidMode(driver, idd):
    driver.get(f"https://www.ebay.com/itm/{idd}?bolp=1")
    _waitForBid(driver)
def bidModePriceInfo(driver):
    cprice = driver.find_element(By.XPATH, '//*[@id="bid-offer-summary"]/p[1]/span[1]/span/span').text
    if "\n" in cprice:
        cprice = cprice.split("\n")[-1]
    bidBtns = [e.text for e in driver.find_elements(By.CSS_SELECTOR, ".place-bid-actions__powerbids-wrapper")]

    if len(bidBtns):
        assert bidBtns[0][:4] == "Bid "
        assert bidBtns[1][:4] == "Bid "
        assert bidBtns[2][:4] == "Bid "

    return {
        "current price": cprice,
        "bidBtns": [b[4:] for b in bidBtns]
    }
def _clickBidBtn(driver, i=0):
    driver.find_elements(By.CSS_SELECTOR, ".place-bid-actions__powerbids-wrapper")[i].click()
    _waitForBid(driver)
def bidWhileUnder(driver, amount):
    _waitForBid(driver)
    
    while True:
        priceInfo = bidModePriceInfo(driver)
        if 0 == len(priceInfo["bidBtns"]):
            print("We are in the lead!")
            break
        current = float(priceInfo["bidBtns"][0][1:])
        if amount < current:
            print(f"It's too rich for my blood at {current}")
            break
        print("Bidding ", current, " on item")
        _clickBidBtn(driver, 0)
        
        while True:
            try:
                rbox = driver.find_element(By.CSS_SELECTOR, "span.inline-notice__main > div > span > span")
                if rbox.text.strip() == "":
                    time.sleep(0.1)
                else:
                    break
            except NoSuchElementException as e:
                time.sleep(0.1)
        rboxtxt = rbox.text
        print("Rbox:", rboxtxt.strip())
        if rboxtxt.strip() not in ["Another bidder is winning. Increase your bid.", "Your current bid puts you in the lead."]:
            print(f"Unknown rbox value \"{rboxtxt}\"")
            exit(-1)
        if rboxtxt.strip() != "Another bidder is winning. Increase your bid.":
            break
        


        
    