__author__ = 'cromox'

from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
# from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains as hoover
import requests

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
sleep(8)

#### Task1 - pop-up window
xpath1 = '//*[@id="onfido-upload"]/div[1]/div[2]'
if driver.find_element_by_xpath(xpath1):
    driver.find_element_by_xpath(xpath1).click()

template_bar = '//*[@id="chartTabTemplates"]/div'
if driver.find_element_by_id("chartTabTemplates"):
    driver.find_element_by_id("chartTabTemplates").click()

search_section = driver.find_element_by_id("navigation-search-button")
search_section.click()

driver.find_element_by_xpath("//*[contains(text(),'Currencies')]").click()
driver.find_element_by_xpath("//*[contains(text(),'Major')]").click()
sleep(1)

# currency2 = "GBP/USD"
# currency2 = "EUR/USD"
# currency2 = "USD/CAD"
currency2 = "USD/JPY"
# currency2 = "USD/CHF"
# currency2 = "AUD/USD"
# currency2 = "NZD/USD"
currency1 = currency2.replace('/', '')

xp_gbpusd = '//*[@data-code="' + currency1 + '"]//*[@class="ticker"]//*[@class="has-ellipsed-text"]'
element1 = driver.find_element_by_xpath(xp_gbpusd)
# print('ELE1 = ', element1, ' / TXT = ', element1.text.replace('\n', ' ## '))
element1.click()
# driver.execute_script("arguments[0].click();", element1)   # if normal click not working, this is JS click
sleep(1)

xp_sell = '//*[@data-code="' + currency1 + '"]//*[@data-dojo-attach-point="mainViewNode"]//*[@data-dojo-attach-point="sellPriceNode"]'
xp_buy = '//*[@data-code="' + currency1 + '"]//*[@data-dojo-attach-point="mainViewNode"]//*[@data-dojo-attach-point="buyPriceNode"]'

print('SELL = ', driver.find_element_by_xpath(xp_sell).text)
print('BUY = ', driver.find_element_by_xpath(xp_buy).text)

xp_low = '//*[@id="current-status-high-low-view"]//*[@data-dojo-attach-point="lowPriceNode"]'
xp_high = '//*[@id="current-status-high-low-view"]//*[@data-dojo-attach-point="highPriceNode"]'

print('LOW = ', driver.find_element_by_xpath(xp_low).text)
print('HIGH = ', driver.find_element_by_xpath(xp_high).text)

## change graph to candlestick
# xp_templatebar = '//*[@id="chartTabTemplates"]//*[@class="arrow-icon svg-icon-holder"]'    # ok1
# xp_templatebar = '//*[@id="chartTabTemplates"]//*[@data-dojo-attach-point="templatesArrowNode"]'   # ok2
# xp_templatebar = '//*[@id="chartTabTemplates"]/div'    # ok3
# xp_templatebar = '//*[(@data-dojo-attach-point="templatesArrowNode") and (@class="arrow-icon svg-icon-holder")]' # ok4
# xp_templatebar = '//*[@data-dojo-attach-point="templatesArrowNode"]'   # ok5
xp_templatebar = '//*[@class="chart-menu"]//*[@data-dojo-attach-point="templatesArrowNode"]'

elements = driver.find_elements_by_xpath(xp_templatebar)
print('number of elements = ', len(elements))
element_template = elements[-1]
element_template.click()

xp_pro_tab = '//*[@id="chart-templates"]/div[2]/div/div/div/div'
driver.find_element_by_xpath(xp_pro_tab).click()

element_template.click()

print('END 1 - Candlestick')

xp_indicator = '//*[@id="chartTabIndicators"]//*[@data-dojo-attach-point="indicatorsArrowNode"]'
elements = driver.find_elements_by_xpath(xp_indicator)
print('number of elements = ', len(elements))
element_indicator = elements[-1]
element_indicator.click()

driver.find_element_by_xpath("//*[contains(text(),'Trend')]").click()
driver.find_element_by_xpath("//*[contains(text(),'EMA')]").click()

# //*[@id="chart-settings"]/div[3]/div[1]/div[2]/input
value_EMA = 30
xp_period = '//*[@id="chart-settings"]//*[@class="editable-input"]'
element_period = driver.find_element_by_xpath(xp_period)
element_period.clear()
element_period.send_keys(str(value_EMA))

# //*[@id="uniqName_0_383"]/div # TODO - to bold the graph line to no 2
# driver.find_elements_by_xpath('//*[@data-dojo-attach-point="valueNode"]')[-1].click()
# for element in driver.find_elements_by_xpath('//*[@data-dojo-attach-point="valueNode"]'):
#     print('element = ', element, ' / text = ', element.text)
#     if element.text == '2':
#         element.click()
# driver.find_element_by_xpath("//*[contains(text(),'2')]").click()

driver.find_element_by_xpath('//*[@class="button confirm-button"]').click()
print('END 2 - ', value_EMA, ' EMA line')

### time period to 5 mins

driver.find_elements_by_xpath('//*[@id="chartTabPeriods"]//*[@class="arrow-icon svg-icon-holder"]')[-1].click()
driver.find_element_by_xpath("//*[contains(text(),'5 minutes')]").click()
print('END 3 - time period 5 mins')

## baca graph

print('\nTEST123 - baca graf')

# xp_baca = "//*[contains(text(),'31.12.2020 22:00')]"
# xp_baca = '//*[@class="chartLayer"]'
xp_baca = '//*[((@class="chart-container") or (@class="chart-container draggable")) and (@tabindex="-1")]'
list1 = driver.find_elements_by_xpath(xp_baca)
# print()
# print('number of elements = ', len(list1))

features_el = list1[-1]
hoover(driver).move_to_element(features_el).perform()
currenturl = driver.current_url
print('currentURL = ', currenturl)
# datasource = driver.page_source
# print('DATA = \n', datasource)

# powersearch_el = driver.find_element_by_xpath("//*[contains(text(),'31.12.2020 22:00')]")
# print('TEXT', powersearch_el.text)

# element2 = driver.find_element_by_xpath("//*[contains(text(),'31.12.2020 22:00')]")
# driver.execute_script("arguments[0].click();", element2)   # if normal click not working, this is JS click


## NI NOTE JER
# 6) Hoover mouse
#
# basepixitmediaurl = driver.current_url
# print('URL = ' + str(basepixitmediaurl))
# elements_pixstor = driver.find_elements_by_xpath("//*[contains(text(),'PixStor')]")
# element_pixstor = elements_pixstor[0]      # if more than one elements
# hoover(driver).move_to_element(element_pixstor).perform()
# features_el = driver.find_element_by_xpath("//*[contains(text(),'Features')]")
# hoover(driver).move_to_element(features_el).perform()
# powersearch_el = driver.find_element_by_xpath("//*[contains(text(),'Powerful Search')]")
# hoover(driver).move_to_element(powersearch_el).perform()
# powersearch_el.click()

# //*[@id="chart_2"]/div[4]/div[1]/div[5]/div
# #chart_2 > div.chart-container > div:nth-child(1) > div.chart-scroller > div

lebar = driver.execute_script("return window.innerWidth")
print('LEBAR = ', lebar)
tinggi = driver.execute_script("return window.innerHeight")
print('TINGGI = ', tinggi)
driver.execute_script("window.scrollTo(" + str(int(lebar*0.92)) + "," + str(tinggi) + ");")

list2 = driver.find_elements_by_xpath("//*[contains(text(),'19:20')]")
print('Nombo = ', len(list2))

chkelements = driver.find_elements_by_xpath('//*[@class="chart-tooltip"]')   ## chart-scroller  &   scr_slider_container  # "chart-tooltip"
print('number of elements = ', len(chkelements))
# print('ELEMENTS = ', chkelements)
if len(chkelements) >= 1:
    for ele in chkelements:

        # hoover(driver).move_to_element(ele).perform()
        # driver.execute_script("arguments[0].click();", ele)
        # print(driver.execute_script("return arguments[0].text", ele))
        # driver.execute_script('document.getElementsByTagName("05.01.2021 17:00")[0].click();')
        # print(driver.execute_script('return document.getElementsByTagName("05.01.2021 17:00")[0].text'))
        print('\nTEXT = \n\n', ele.text)
        # driver.execute_script("arguments[0].click();", ele)
        # print(driver.execute_script("return arguments[0].text", ele))
        # print(driver.execute_script('return document.getElementsByTagName("05.01.2021 17:00")[0].text'))
