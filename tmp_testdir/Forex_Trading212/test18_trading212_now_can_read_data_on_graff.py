__author__ = 'cromox'

from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains as hoover

chromedriverpath = r'C:\tools\chromedriver\chromedriver.exe'
chrome_options = Options()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-gpu')
# chrome_options.headless = True
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument("--disable-web-security")
chrome_options.add_argument("--incognito")
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
    print('INVESTIGATE')
    for ele in chkelements:
        print('ele, get_attribute_id, get_attribute_class, id, location, location_once_scrolled_into_view, tag_name')
        print('ELE ', chkelements.index(ele) + 1, ele.get_attribute('id'), ele.get_attribute('class'), ele.id, ele.location,
              ele.location_once_scrolled_into_view, ele.tag_name)

    if len(chkelements) >= 1:
        # # chkelements[0].location.update({'x': 950, 'y': 440})
        # hoover(driver).move_to_element(chkelements[0]).move_by_offset(950,440).perform()
        # print('new location = ', chkelements[0].location)
        # return driver.execute_script('return arguments[0].value;', chkelements[0])   ## wrong output
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

def movearound_showtext(driver, element, x_value, y_value):
    hoover(driver).move_to_element_with_offset(element, x_value, y_value).perform()
    print()
    print('x = ', x_value, ' / y = ', y_value)
    print('NEWTEXT = ', " // ".join(element.text.split('\n')[0:3] + element.text.split('\n')[-2:]))
    print('NEWLOCTN = ', element.location)
    # print(' -- > to compare / DISPLAY_SIZE = ', driver.execute_script("return window.innerWidth"), ' x ',
    #       driver.execute_script("return window.innerHeight"))
    print()
    return int(element.location['x']), int(element.location['y'])

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
# currency2 = "USD/JPY"
currency2 = "USD/CHF"
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

baca1 = baca_graff()
print()
print('TEXT1 = \n', " // ".join(baca1.split('\n')[0:3] + baca1.split('\n')[-2:]))

sleep(1)

# javas = "document.getElementsByText('11.01.2021 16:00')[0].click();"
# driver.execute_script(javas)
# print(driver.execute_script('return document.documentElement.innerText'))

print()
lebar = driver.execute_script("return window.innerWidth")
print('LEBAR x = ', lebar)
tinggi = driver.execute_script("return window.innerHeight")
print('TINGGI y = ', tinggi)

test1A = '//*[@class="chart-tooltip"]'
chkelements1A = driver.find_elements_by_xpath(test1A)
print('number of elements chkelements2A = ', len(chkelements1A))
test1B = '//*[((@class="chart-container") or (@class="chart-container draggable")) and (@tabindex="-1")]'
chkelements1B = driver.find_elements_by_xpath(test1B)
print('number of elements chkelements2B = ', len(chkelements1B))
print('size display = ', chkelements1B[-1].get_attribute('style'))
xdisplay = lebar
ydisplay = tinggi
if chkelements1B[-1].get_attribute('style') != None:
    xdisplay = int(chkelements1B[-1].get_attribute('style').split(';')[0].split('width:')[-1].split('px')[0])
    ydisplay = int(chkelements1B[-1].get_attribute('style').split(';')[1].split('height:')[-1].split('px')[0])

print('DISPLAY = (xy) ', xdisplay, ydisplay)

chkelements2 = chkelements1A
for ele in chkelements2:
    test1 = '//*[@class="chart-tooltip"]'
    toolTip = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, test1)))

    hoover(driver).move_to_element(toolTip).perform()
    print('ELE LOCATION ', toolTip.location, ' / y = ', toolTip.location['y'])
    yy1 = toolTip.location['y']
    xx1 = toolTip.location['x']
    print('TEXT2 = \n', " // ".join(toolTip.text.split('\n')[0:3]))

    all_children_by_xpath = toolTip.find_elements_by_xpath(".//*")
    print('len(all_children_by_xpath): ', len(all_children_by_xpath))

    print('TEXT 0 = \n', " // ".join(all_children_by_xpath[0].text.split('\n')[0:3]))

    move1 = movearound_showtext(driver, toolTip, -15, -15)
    arrear = move1[0]
    for steppx in range(xdisplay + 190, 1, -5):
        move = movearound_showtext(driver, toolTip, steppx - arrear - 15, -15)
        arrear = move[0]
        # print('steppx = ', steppx, ' / arrear = ', arrear)
        if move[0] < move1[0]:
            print('move0 = ', move[0], ' / move10 = ', move1[0])
            break

# print('xx0 = ', xx0)
print('xx1 = ', xx1)
print('yy1 = ', yy1)

## LAST VALUE
# x =  412  / y =  -15
# NEWTEXT =  15.01.2021 20:55 // Price // 1.20627
# NEWLOCTN =  {'x': 1345, 'y': 573}
#  -- > to compare / DISPLAY_SIZE =  1920  x  1045

