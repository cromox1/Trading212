__author__ = 'cromox'

from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
# from selenium.webdriver.common.action_chains import ActionChains as hoover

chromedriverpath = r'C:\tools\chromedriver\chromedriver.exe'
chrome_options = Options()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument("--disable-web-security")
# chrome_options.add_argument("--incognito")
chrome_options.add_argument("--allow-running-insecure-content")
chrome_options.add_argument("--allow-cross-origin-auth-prompt")
chrome_options.add_argument("--disable-cookie-encryption")
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-default-apps')
chrome_options.add_argument('--disable-prompt-on-repost')
chrome_options.add_argument("--disable-zero-browsers-open-for-tests")
chrome_options.add_argument("--no-default-browser-check")
chrome_options.add_argument("--test-type")
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs", prefs)

## webdriver section
driver = webdriver.Chrome(chromedriverpath, options=chrome_options)
driver.implicitly_wait(10)

base_url = "https://www.trading212.com"

driver.maximize_window()
driver.get(base_url)

driver.find_element_by_id("cookie-bar").click()
driver.find_element_by_id("login-header-desktop").click()

user1 = "mycromox@gmail.com"
pswd1 = "Serverg0d!"

driver.find_element_by_id("username-real").send_keys(user1 + Keys.ENTER)
driver.find_element_by_id("pass-real").send_keys(pswd1 + Keys.ENTER)
sleep(10)

# ### Need to find a way to go to pop-up window
# but for now I just use simple solution - find the xpath :-)
xpath1 = '//*[@id="onfido-upload"]/div[1]/div[2]'
driver.find_element_by_xpath(xpath1).click()

template_bar = '//*[@id="chartTabTemplates"]/div'
driver.find_element_by_id("chartTabTemplates").click()

search_section = driver.find_element_by_id("navigation-search-button")
search_section.click()
# search_section.send_keys('GBP/USD' + Keys.ENTER)

driver.find_element_by_xpath("//*[contains(text(),'Currencies')]").click()
driver.find_element_by_xpath("//*[contains(text(),'Major')]").click()

# CSS selector
# valuetofind = 'input[id*="uniqName_"]'
# list_ids = driver.find_elements_by_css_selector(valuetofind)
# # XPATH
valuetofind = '//*[contains(@id, "uniqName_")]'

list_ids = driver.find_elements_by_xpath(valuetofind)
# print('ALL = ', list_ids)
print('ALL uniqName = ', len(list_ids))

if len(list_ids) >= 1:
    i = 1
    for idx in list_ids:
        try:
            idxx = idx.get_attribute('id')
            print(i, idxx, end='')
            try:
                if 'GBP/USD' in driver.find_element_by_id(idxx).text:
                    idx.click()
                    print(' / CLICKABLE')
                else:
                    print(' / # NO GBP/USD')
            except WebDriverException:
                print(' / NOT CLICKABLE')
        except WebDriverException:
            print(i, idx.id, end='')
            try:
                if 'GBP/USD' in idx.text:
                    idx.click()
                    print(' / CLICKABLE')
                else:
                    print(' / # NO GBP/USD')
            except WebDriverException:
                print(' / NOT CLICKABLE')
        i += 1
else:
    print('NO ELEMENT APPEARED !!')