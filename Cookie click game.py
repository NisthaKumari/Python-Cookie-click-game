from selenium import webdriver
from selenium.webdriver.common.by import By
import  time

#keep the chrome open after programme finished
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://orteil.dashnet.org/experiments/cookie/")

cookie_place = driver.find_element(By.ID, value="cookie")

#Get upgrade time ids
items = driver.find_elements(By.CSS_SELECTOR, value="#store div")
item_ids = [item.get_attribute("id") for item in items]

time_out = time.time() + 5
five_min = time.time() + 60*5

while True:
    cookie_place.click()

    #every 5 minutes
    if time.time() > time_out:

        #get updates of all prices of items
        all_prices = driver.find_elements(By.CSS_SELECTOR, value="#store b")
        item_prices = []

        for price in all_prices:
            element_text = price.text
            if element_text != "" :
                cost = int(element_text.split("-")[1].strip().replace(",",""))
                cost= int(cost)
                item_prices.append(cost)

        #create a dict of store items and prices
        cookie_upgrade = {}
        for n in range(len(item_prices)):
            cookie_upgrade[item_prices[n]] = item_ids[n]


        #get cookies count
        money_element = driver.find_element(By.ID, value="money").text
        if "," in money_element:
            money_element = money_element.replace(",", "")
        cookie_count = int(money_element)

        #find upgrades that we can afford
        affordable_items = {}
        for cost, upgrade_id in cookie_upgrade.items():
            if cookie_count > cost:
                affordable_items[cost] = upgrade_id

        #but the most  expensive items for upgrades
        highest_price_affordable_upgrades= max(affordable_items)
        print(highest_price_affordable_upgrades)
        to_purchase_id = affordable_items[highest_price_affordable_upgrades]

        driver.find_element(By.ID,value= to_purchase_id).click()

        #add another 5 sec until the next check
        time_out = time.time() +5

    #after 5 mins  stop the bot and check the count of cookie
    if time.time() > five_min:
        cookie_per_sec = driver.find_element(By.ID, value= "cps").text
        print(cookie_per_sec)
        break

driver.quit()

