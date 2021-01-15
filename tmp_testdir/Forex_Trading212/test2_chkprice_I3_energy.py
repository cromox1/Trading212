__author__ = 'cromox'

from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.keys import Keys

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

## webdriver section
driver = webdriver.Chrome(chromedriverpath, options=chrome_options)
driver.implicitly_wait(10)

# base_url = "https://www.londonstockexchange.com/stock/I3E/i3-energy-plc/company-page"
# base_url = "https://www.londonstockexchange.com/stock/KIST/kistos-plc/company-page"
# base_url = "https://www.londonstockexchange.com/stock/ANX/anexo-group-plc/company-page"
base_url = "https://www.londonstockexchange.com/stock/GFS/g4s-plc/company-page"

driver.maximize_window()
driver.get(base_url)

## accept Cookie notofication
if driver.find_element_by_id("ccc-notify-accept"):
    driver.find_element_by_id("ccc-notify-accept").click()

# trade_table = driver.find_element_by_id("trades-table").text
latest_trade = driver.find_element_by_id("slide-0").text
prev_trade = driver.find_element_by_id("slide-1").text
prev2_trade = driver.find_element_by_id("slide-4").text
lt_list = latest_trade.split(' ')
pt_list = prev_trade.split(' ')
pt2_list = prev2_trade.split(' ')
# print(lt_list)
print('NOW  PRICE = ', lt_list[3], lt_list[2], ' AT DATE/TIME ', lt_list[0], lt_list[1])
print('PREV1 PRICE = ', pt_list[3], pt_list[2], ' AT DATE/TIME ', pt_list[0], pt_list[1])
print('PREV2 PRICE = ', pt2_list[3], pt2_list[2], ' AT DATE/TIME ', pt2_list[0], pt2_list[1])

chart_table = driver.find_element_by_id("chart-table")
yesterdayprice = chart_table.text.split('\n')[4]
openprice = chart_table.text.split('\n')[2]
print('YESTERDAY = GBX', yesterdayprice, ' // OPEN PRICE = ', openprice)
# //*[@id="chart-table"]/div[1]/div[2]/app-index-item[2]/div
# document.querySelector("app-index-item > div")
# #chart-table > div.chart-table-price-information > div.flex-wrapper > app-index-item:nth-child(2) > div
# //*[@id="chart-table"]/div[1]/div[2]/app-index-item[2]/div

# //*[@id="trades-table"]/table/tbody

# print(trade_table)