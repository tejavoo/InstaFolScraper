from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from explicit import waiter, XPATH
from numpy import random

from selenium.webdriver.firefox.options import Options

options = Options()


import argparse
parser = argparse.ArgumentParser(description='Parse the followers of ')
parser.add_argument('--username', type=str, help='Input dir for videos')
parser.add_argument('--headless', type=bool, help='Input dir for videos',default=False)
parser.add_argument('--insta_username', type=str, help='Input dir for videos')
parser.add_argument('--insta_password', type=str, help='Input dir for videos')


# parser.add_argument('outdir', type=str, help='Output dir for image')
args = parser.parse_args()

usr_to_scrape = args.username
options.headless = args.headless
insta_username = args.insta_username
insta_password = args.insta_password

import pickle

import itertools
from explicit import waiter, XPATH
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep


driver = webdriver.Firefox(options=options)
driver.get("https://www.instagram.com")

# /html/body/div[5]/div[2]/div/div[2]/div/div/div[1]/div/form/div[1]/div[1]/div/label/input

####### elem = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/span')

print("Code is running Kripaya Sabar Kare !")

driver.implicitly_wait(8)

log_in = driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input')
log_in.clear()
log_in.send_keys(insta_username)

passc = driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input')
passc.clear()
passc.send_keys(insta_password)

log_btn = driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button')
log_btn.click()

driver.implicitly_wait(5)

btn = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button')
btn.click()

driver.get("https://www.instagram.com/{}".format(usr_to_scrape))
driver.implicitly_wait(5)

elem = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/span')

print(elem.text)

elem.click()

waiter.find_element(driver, "//div[@role='dialog']", by=XPATH)
allfoll = driver.find_element_by_xpath("//li[2]/a/span").text
allfoll_tot = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/span').get_attribute("title")
allfoll_tot = int(allfoll_tot.replace(',', ''))

print("Follower count : {},{}".format(allfoll,allfoll_tot))
# scr1 = driver.find_element_by_xpath('/html/body/div[5]/div/div')
# driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scr1)
follower_accounts = []

def scrape_followers(driver,allfoll=allfoll_tot,account="lordsse_design"):
    follower_css = "ul div li:nth-child({}) a.notranslate"  # Taking advange of CSS's nth-child functionality
    for group in itertools.count(start=1, step=12):
        for follower_index in range(group, group + 12):
            if follower_index > allfoll:
                raise StopIteration
            yield waiter.find_element(driver, follower_css.format(follower_index)).text

        # Instagram loads followers 12 at a time. Find the last follower element
        # and scroll it into view, forcing instagram to load another 12
        # Even though we just found this elem in the previous for loop, there can
        # potentially be large amount of time between that call and this one,
        # and the element might have gone stale. Lets just re-acquire it to avoid
        # tha
        last_follower = waiter.find_element(driver, follower_css.format(group+11))
        driver.execute_script("arguments[0].scrollIntoView();", last_follower)

try:
    for count, follower in enumerate(scrape_followers(driver,allfoll=allfoll_tot,account=usr_to_scrape), 1):
        if count%500 == 0:
            print("\t{:>3}: {}".format(count, follower))
            sleep(random.uniform(0,1))
        if count%10 == 0:
            sleep(random.uniform(0,1))
        follower_accounts.append(follower)
except:
    pass

driver.close()

# Save using pickle
filename = 'follower_accounts_array.pkl'
with open(filename, 'wb') as filehandler:
    pickle.dump(follower_accounts, filehandler)

# /html/body/div[5]/div






# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys

# driver = webdriver.Firefox()
# driver.get("http://www.python.org")

# assert "Python" in driver.title
# elem = driver.find_element_by_name("q")

# elem.clear()
# elem.send_keys("pycon")
# elem.send_keys(Keys.RETURN)

# assert "No results found." not in driver.page_source

# driver.close()

# /html/body/div[5]/div/div/div[2]/ul/div/li[1]/div/div[1]/div[2]/div[1]/span/a
# /html/body/div[5]/div/div/div[2]/ul/div/li[2]/div/div[1]/div[2]/div[1]/span/a
# //*[@id="f1a2cf9baef211"]/div/div/span/a
# //*[@id="fd7b9076699374"]/div/div/span/a


# /html/body/div[5]/div/div/div[2]
