__author__ = 'cromox'

from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
# from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains as hoover
# import requests

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

#### FUNCTION FOR TOOLTIP VALUE

def dapatkan_values():
    chkelements = driver.find_elements_by_xpath('//*[@class="chart-tooltip"]')
    # chkelements = driver.find_elements_by_xpath('//*[@class="tooltip"]')
    if len(chkelements) >= 1:
        return chkelements[0].text

def baca_graff():
    print('\nTEST BACA GRAFF')

    xp_baca = '//*[((@class="chart-container") or (@class="chart-container draggable")) and (@tabindex="-1")]'
    list1 = driver.find_elements_by_xpath(xp_baca)
    print('number of elements = ', len(list1))

    features_el = list1[-1]
    id1 = features_el.get_attribute('class')
    print('ID1 = ', id1)
    hoover(driver).move_to_element(features_el).perform()
    currenturl = driver.current_url
    print('currentURL = ', currenturl)

    # print()
    text123 = dapatkan_values()
    # print(text123)
    return text123

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
currency2 = "EUR/USD"
# currency2 = "USD/CAD"
# currency2 = "USD/JPY"
# currency2 = "USD/CHF"
# currency2 = "AUD/USD"
# currency2 = "NZD/USD"
currency1 = currency2.replace('/', '')

xp_gbpusd = '//*[@data-code="' + currency1 + '"]//*[@class="ticker"]//*[@class="has-ellipsed-text"]'
element1 = driver.find_element_by_xpath(xp_gbpusd)
element1.click()
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

value_EMA = 30
xp_period = '//*[@id="chart-settings"]//*[@class="editable-input"]'
element_period = driver.find_element_by_xpath(xp_period)
element_period.clear()
element_period.send_keys(str(value_EMA))

driver.find_elements_by_xpath('//*[@class="button confirm-button"]')[-1].click()
# driver.find_element_by_xpath("//*[contains(text(),'Confirm')]").click()
print('END 2 - ', value_EMA, ' EMA line')

### time period to 5 mins

driver.find_elements_by_xpath('//*[@id="chartTabPeriods"]//*[@class="arrow-icon svg-icon-holder"]')[-1].click()
driver.find_element_by_xpath("//*[contains(text(),'5 minutes')]").click()
print('END 3 - time period 5 mins')

## baca graph

baca1 = baca_graff()
print()
print('TEXT1 = \n', baca1)

for i in range(10):
    zoom_in = '//*[@id="chartTabZoomIn"]'
    driver.find_elements_by_xpath(zoom_in)[-1].click()

# # zoom_in = '//*[@id="chartTabZoomIn"]'
# # driver.find_elements_by_xpath(zoom_in)[-1].click()
# # driver.find_elements_by_xpath(zoom_in)[-1].click()
# # driver.find_elements_by_xpath(zoom_in)[-1].click()
# # driver.find_elements_by_xpath(zoom_in)[-1].click()
# # driver.find_elements_by_xpath(zoom_in)[-1].click()
#
# # print()
# # lebar = driver.execute_script("return window.innerWidth")
# # print('LEBAR = ', lebar)
# # # tinggi = driver.execute_script("return window.innerHeight")
# # tinggi = 100
# # print('TINGGI = ', tinggi)
# # # print("window.scrollTo(" + str(int(lebar*0.9)) + "," + str(int(tinggi*0.5)) + ");")
# # # driver.execute_script("window.scrollTo(" + str(int(lebar*0.92)) + "," + str(int(tinggi*0.5)) + ");")
# # ### move mouse
# #
# # # xp23_baca = '//*[((@class="chart-container") or (@class="chart-container draggable")) and (@tabindex="-1")]'
# # # xp23_baca = '//*[@class="dragging"]'
# # # list23 = driver.find_elements_by_xpath(xp23_baca)
# # # css23_baca = ".dragging.scr_slider"
# # # list23 = driver.find_elements_by_css_selector(css23_baca)
# #
# # # //*[@id="chart_2"]/div[4]/div[1]/div[5]/div
# # #chart_1 > div.chart-container > div:nth-child(1) > div.layer.svg-layer.unselectable > svg > g:nth-child(4) > line
# #
# # xp34_baca = '//*[@class="chart-scroller"]//*[@class="scr_slider_container"]//*[@class="scr_slider"]'
# xp34_baca = '//*[@class="current-price-line current-sell-price-line"]'
# list34 = driver.find_elements_by_xpath(xp34_baca)
# print('number of elements = ', len(list34))
# print('SLIDER TEXT = ', list34[-1].text)
# #
# features_el34 = list34[-1]
# id34 = features_el34.get_attribute('class')
# print('ID34 = ', id34)
# hoover(driver).move_to_element_with_offset(driver.find_element_by_tag_name('body'), 0,0)
# # # hoover(driver).move_to_element(features_el23).move_by_offset(int(lebar*0.7), int(tinggi*0.5)).click().perform()
# # # print("move_by_offset(" + str(int(lebar*0.2)) + "," + "0)")
# # hoover(driver).move_to_element(features_el23).move_by_offset(int(lebar*0.2), 0).click().perform()
#
# #
# # # slider = //*[@id="chart_1"]/div[4]/div[1]/div[5]/div/div    class="scr_slider"
# #
# # hoover(driver).move_to_element_with_offset(driver.find_element_by_tag_name('body'), 0,0)
# # # nnn = 0.3
# # # print("move_to_element_with_offset(" + "features_el23, " + str(int(lebar*nnn)) + "," + str(int(tinggi*nnn)) + ")")
# # # hoover(driver).move_to_element_with_offset(features_el23, int(lebar*nnn), int(tinggi*nnn)).click().perform()
# # # hoover(driver).move_to_element_with_offset(features_el23, 110, 4).click() # .perform()
# # # hoover(driver).move_to_element_with_offset(driver.find_elements_by_css_selector(".dragging")[0], 110, 4).perform()
# #
# hoover(driver).move_to_element_with_offset(features_el34, 110, 4).click() # .perform()

baca2 = baca_graff()
print()
print('TEXT2 = \n', baca2)