__author__ = 'cromox'

from time import sleep
from datetime import datetime
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

def movearound_showtext(driver, element, x_value, y_value, prev_text, value_EMA):
    hoover(driver).move_to_element_with_offset(element, x_value, y_value).perform()
    chktext = element.text.split('\n')[0].replace(' ', '')
    try:
        if chktext == prev_text:
            text = 'duplicate'
        elif str(element.text.split('\n')[4]) == 'Close':
            text = 'xlocation / ' + str(element.location['x']) + ' / ylocation / ' + str(element.location['y'])
        else:
            text = text_to_display(element.text.split('\n'), value_EMA)
    except:
        text = 'out_of_boundary_or_wrong_value'
    return int(element.location['x']), int(element.location['y']), text, chktext

def text_to_display(list_text, value_EMA):
    if len(list_text) >= 12:
        open = list_text[4]
        close = list_text[6]
        ema = list_text[-1]
        fxstatus = forex_status_diffEMA(open, close, ema, value_EMA)
        text = " / ".join(
            list_text[0:7] + list_text[-2:] + [fxstatus[0], fxstatus[1], fxstatus[2], fxstatus[3], fxstatus[-2], fxstatus[-1]])
    else:
        text = " / ".join(list_text[0:3])
    return text

def forex_status_diffEMA(open, close, ema, value_EMA):
    diffopenclose = float(close) - float(open)
    diffema = float(ema) - float(close)
    peratus = str("%.5f" % round(abs(20000 * diffema/(float(ema) + float(close))), 5))
    if diffopenclose <= 0:
        statusfx = 'BEARISH'
    else:
        statusfx = 'BULLISH'
    if diffema > 0:
        statusema = 'UNDER_' + str(value_EMA) + 'EMA'
    elif diffema < 0:
        statusema = 'OVER_' + str(value_EMA) + 'EMA'
    else:
        statusema = '#EQUAL_' + str(value_EMA) + 'EMA'
    return statusfx, str("%.5f" % round(diffopenclose, 5)), statusema, str("%.5f" % round(diffema, 5)), 'PERCENT', peratus

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

currency2 = "GBP/USD"
# currency2 = "EUR/USD"
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
print()

## change graph to candlestick
xp_templatebar = '//*[@class="chart-menu"]//*[@data-dojo-attach-point="templatesArrowNode"]'

elements = driver.find_elements_by_xpath(xp_templatebar)
# print('number of elements = ', len(elements))
element_template = elements[-1]
element_template.click()

xp_pro_tab = '//*[@id="chart-templates"]/div[2]/div/div/div/div'
driver.find_element_by_xpath(xp_pro_tab).click()

element_template.click()

print('-- > END 1 - Candlestick')

xp_indicator = '//*[@id="chartTabIndicators"]//*[@data-dojo-attach-point="indicatorsArrowNode"]'
elements = driver.find_elements_by_xpath(xp_indicator)
# print('number of elements = ', len(elements))
element_indicator = elements[-1]
element_indicator.click()

driver.find_element_by_xpath("//*[contains(text(),'Trend')]").click()
driver.find_element_by_xpath("//*[contains(text(),'EMA')]").click()

value_EMA = 50
xp_period = '//*[@id="chart-settings"]//*[@class="editable-input"]'
element_period = driver.find_element_by_xpath(xp_period)
element_period.clear()
element_period.send_keys(str(value_EMA))
# //*[@id="uniqName_0_463"]/span

driver.find_elements_by_xpath('//*[@class="button confirm-button"]')[-1].click()
# driver.find_element_by_xpath("//*[contains(text(),'Confirm')]").click()
print('-- > END 2 -', value_EMA, 'EMA line')

### time period to 5 mins
tperiod = '5 minutes'
tukar = {'minute':60, 'hour': 3600, 'day': int(24*3600), 'week': int(24*3600*7), 'month': int(24*3600*30),
         'year': int(24*3600*365 + 6*3600)}
timesequence = int(tperiod.split(' ')[0]) * int(tukar[tperiod.split(' ')[-1].replace('s','')])
driver.find_elements_by_xpath('//*[@id="chartTabPeriods"]//*[@class="arrow-icon svg-icon-holder"]')[-1].click()
driver.find_element_by_xpath('//*[contains(text(), "' + tperiod + '")]').click()
print('-- > END 3 - set time period ' + tperiod)

sleep(1)

print()
lebar = driver.execute_script("return window.innerWidth")
tinggi = driver.execute_script("return window.innerHeight")
print('LEBAR x = ', lebar, ' / TINGGI y = ', tinggi)

xp_chart_container = '//*[((@class="chart-container") or (@class="chart-container draggable")) and (@tabindex="-1")]'
elements_chart_container = driver.find_elements_by_xpath(xp_chart_container)
xdisplay = lebar
ydisplay = tinggi
if elements_chart_container[-1].get_attribute('style') != None:
    xdisplay = int(elements_chart_container[-1].get_attribute('style').split(';')[0].split('width:')[-1].split('px')[0])
    ydisplay = int(elements_chart_container[-1].get_attribute('style').split(';')[1].split('height:')[-1].split('px')[0])

print('DISPLAY = ( x y ) ', xdisplay, ydisplay)

xp_tooltip = '//*[@class="chart-tooltip"]'
elements_tooltip = driver.find_elements_by_xpath(xp_tooltip)
for ele in elements_tooltip:
    toolTip = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xp_tooltip)))
    move0 = movearound_showtext(driver, toolTip, int(xdisplay/4), int(ydisplay/4), 'x', value_EMA)
    arrear = move0[0]
    chktext = move0[-1]
    stepadd = 5
    for steppx in range(1, xdisplay, stepadd):
        if int(arrear/8) % 2 == 0:
            ynum = -11
        else:
            ynum = -19
        move = movearound_showtext(driver, toolTip, -9, ynum, chktext, value_EMA)
        arrear = move[0]
        chktext = move[-1]

        if move[2] != 'duplicate' and move[2].split('/')[0].replace(' ', '') != 'xlocation':
            print('NEWTEXT = ', move[2])
        elif move[2].split('/')[0].replace(' ', '') == 'xlocation':
            print('NEWTEXT = ', move[2])
            movearound_showtext(driver, toolTip, -25, -15, chktext, value_EMA)
            movearound_showtext(driver, toolTip, -10, -15, chktext, value_EMA)
            while int(datetime.now().timestamp()) > 0:
                chktext = str(datetime.now().timestamp())
                print('LOOPTEXT = ', movearound_showtext(driver, toolTip, -15, -15, chktext, value_EMA)[2])
                nextexecute = int(datetime.now().timestamp()) + timesequence
                print('  -- > TIME NOW = ', datetime.now(), ' / EPOCHTIME = ',
                      int(datetime.now().timestamp()), ' / NEXT RUN = ',
                      datetime.fromtimestamp(nextexecute).strftime('%Y-%m-%d %H:%M:%S'))
                sleep(timesequence)
            # break

        if arrear > xdisplay + 190 - 15:
            print('xlocation = ', arrear, ' / xdisplay = ', xdisplay)
            break