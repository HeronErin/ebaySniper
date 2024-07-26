from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import time
import os, json

import ebay

ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
CONFIG_DIR = os.path.join(ROOT_DIR, "config")
CONFIG_JSON = os.path.join(CONFIG_DIR, "config.json")
COOKIE_JSON = os.path.join(CONFIG_DIR, "cookies.json")




def humanTime(seconds):
    result = []
    for name, count in [
            ("year", 365 * 24 * 3600),
            ("day", 24 * 3600),
            ("hour", 3600),
            ("minute", 60),
            ("second", 1),
        ]:
        value = seconds / count
        if value > 1:
            result.append(f"{round(value, 2) if name == 'second' else int(value)} {name}{'s' if value > 1 else ''}")
            seconds %= count
    return ', '.join(result)






assert os.path.exists(CONFIG_DIR), "Please create a config.json file in the config dir."
assert os.path.exists(COOKIE_JSON), "Please create a cookies.json file in the config dir. See README.md"

f = open(CONFIG_JSON, "r")
CONFIG = json.load(f)
f.close()
for x in ["target", "max", "delay"]:
    if not x in CONFIG:
        print(x, "is required in config.json")
        exit(-1)


options = Options()
options.add_argument('--headless=new')
driver = webdriver.Chrome(options=options)

ebay.flushDriverCookies(driver, COOKIE_JSON)
if not ebay.verifySignin(driver):
    print("ERROR: Can't sign in to ebay, cookies are invalid!")
    exit(-1)
driver.get("about:blank")

try:
    while True:
        data = ebay.getItemState(CONFIG["target"])
        epoc = time.time()
        timeLeft = humanTime(data["endTime"]-epoc)
        print(f'{time.ctime()}: Current price: {data["price"]["value"]} {data["price"]["currency"]} with {timeLeft} time left.')
        if data["price"]["value"] >= CONFIG["max"]:
            print("FAIL: Price got too large.")
            break
        if data["endTime"] <= epoc:
            print("FAIL: Not sure what happened, but the end time for this auction has passed!")
            break

        endDell = data["endTime"] - CONFIG["delay"] - CONFIG.get("predelay", 60)
        waitTill = min(endDell, epoc + CONFIG.get("infoDumpChk", 30*60))
        waitTime = waitTill - epoc

        print("Waiting", humanTime(waitTime), "\n")
        time.sleep(waitTime)

        # ITS GO TIME
        if time.time() >= endDell-1:
            print(f"Checking account before bid at {time.ctime()}.")
            if not ebay.verifySignin(driver):
                print("ERROR: Can't sign in to ebay, cookies are invalid! Sorry for the bad luck :<")
                break
            ebay.enterBidMode(driver, CONFIG["target"])

            time.sleep(data["endTime"] - epoc - CONFIG["delay"])

            ebay.bidWhileUnder(driver, CONFIG["max"])
            print(f"Open ebay here: https://www.ebay.com/itm/{CONFIG['target']}")
            break


finally:
    driver.quit()
