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

##### General function

def google_chrome_browser():
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
    return driver

def autologin_maxwindows(driver, base_url, username, passwd):
    driver.maximize_window()
    driver.get(base_url)
    driver.find_element_by_id("cookie-bar").click()
    driver.find_element_by_id("login-header-desktop").click()
    driver.find_element_by_id("username-real").send_keys(username + Keys.ENTER)
    driver.find_element_by_id("pass-real").send_keys(passwd + Keys.ENTER)
    sleep(5)
    return driver

def close_popup_ask_upload_docs(driver):
    xpath1 = '//*[@id="onfido-upload"]/div[1]/div[2]'
    if driver.find_element_by_xpath(xpath1):
        driver.find_element_by_xpath(xpath1).click()
    return driver

def from_search_goto_specific_currency(driver, currency):
    # if driver.find_element_by_xpath('//*[@id="search-header"]//*[@class="search-input"]'):
    #     driver.find_element_by_xpath('//*[@id="search-header"]//*[@class="search-input"]').click()
    elemlist = driver.find_elements_by_id("navigation-search-button")
    hoover(driver).move_to_element_with_offset(elemlist[0], 10, 0).perform()
    elemlist[0].click()
    driver.find_element_by_xpath("//*[contains(text(),'Currencies')]").click()
    driver.find_element_by_xpath("//*[contains(text(),'Major')]").click()
    sleep(1)
    currency1 = currency.replace('/', '')
    xp_gbpusd = '//*[@data-code="' + currency1 + '"]//*[@class="ticker"]//*[@class="has-ellipsed-text"]'
    element1 = driver.find_element_by_xpath(xp_gbpusd)
    element1.click()
    print('\nCURRENCY = ', currency)
    sleep(1)
    xp_sell = '//*[@data-code="' + currency1 + '"]//*[@data-dojo-attach-point="mainViewNode"]//*[@data-dojo-attach-point="sellPriceNode"]'
    xp_buy = '//*[@data-code="' + currency1 + '"]//*[@data-dojo-attach-point="mainViewNode"]//*[@data-dojo-attach-point="buyPriceNode"]'
    print('SELL = ', driver.find_element_by_xpath(xp_sell).text, ' / BUY = ', driver.find_element_by_xpath(xp_buy).text)
    xp_low = '//*[@id="current-status-high-low-view"]//*[@data-dojo-attach-point="lowPriceNode"]'
    xp_high = '//*[@id="current-status-high-low-view"]//*[@data-dojo-attach-point="highPriceNode"]'
    print('LOW = ', driver.find_element_by_xpath(xp_low).text, ' / HIGH = ', driver.find_element_by_xpath(xp_high).text)
    return driver

def change_graph_to_candlestick(driver):
    xp_templatebar = '//*[@class="chart-menu"]//*[@data-dojo-attach-point="templatesArrowNode"]'
    elements = driver.find_elements_by_xpath(xp_templatebar)
    # print('number of elements = ', len(elements))
    element_template = elements[-1]
    element_template.click()
    xp_pro_tab = '//*[@id="chart-templates"]/div[2]/div/div/div/div'
    driver.find_element_by_xpath(xp_pro_tab).click()
    element_template.click()
    print('-- > END 1 - Candlestick')
    return driver

def set_graph_EMA_value(driver, value_EMA):
    xp_indicator = '//*[@id="chartTabIndicators"]//*[@data-dojo-attach-point="indicatorsArrowNode"]'
    elements = driver.find_elements_by_xpath(xp_indicator)
    # print('number of elements = ', len(elements))
    element_indicator = elements[-1]
    element_indicator.click()
    driver.find_element_by_xpath("//*[contains(text(),'Trend')]").click()
    driver.find_element_by_xpath("//*[contains(text(),'EMA')]").click()
    xp_period = '//*[@id="chart-settings"]//*[@class="editable-input"]'
    element_period = driver.find_element_by_xpath(xp_period)
    element_period.clear()
    element_period.send_keys(str(value_EMA))
    driver.find_elements_by_xpath('//*[@class="button confirm-button"]')[-1].click()
    # driver.find_element_by_xpath("//*[contains(text(),'Confirm')]").click()
    print('-- > END 2 -', value_EMA, 'EMA line')
    return driver

def change_graph_time_period(driver, time_period):
    tukar = {'minute': 60, 'hour': 3600, 'day': int(24 * 3600), 'week': int(24 * 3600 * 7),
             'month': int(24 * 3600 * 30), 'year': int(24 * 3600 * 365 + 6 * 3600)}
    timesequence = int(time_period.split(' ')[0]) * int(tukar[time_period.split(' ')[-1].replace('s', '')]) - 1
    driver.find_elements_by_xpath('//*[@id="chartTabPeriods"]//*[@class="arrow-icon svg-icon-holder"]')[-1].click()
    driver.find_element_by_xpath('//*[contains(text(), "' + time_period + '")]').click()
    print('-- > END 3 - set time period ' + time_period)
    sleep(1)
    return driver, timesequence

def collecting_data_on_graph(driver, fr_graph_div, cont_or_stop, timesequence):
    lebar = driver.execute_script("return window.innerWidth")
    tinggi = driver.execute_script("return window.innerHeight")
    print('LEBAR x = ', lebar, ' / TINGGI y = ', tinggi)
    xp_chart_container = '//*[((@class="chart-container") or (@class="chart-container draggable")) and (@tabindex="-1")]'
    elements_chart_container = driver.find_elements_by_xpath(xp_chart_container)
    xdisplay = lebar
    ydisplay = tinggi
    if elements_chart_container[-1].get_attribute('style') != None:
        xdisplay = int(
            elements_chart_container[-1].get_attribute('style').split(';')[0].split('width:')[-1].split('px')[0])
        ydisplay = int(
            elements_chart_container[-1].get_attribute('style').split(';')[1].split('height:')[-1].split('px')[0])
    print('DISPLAY = ( x y ) ', xdisplay, ydisplay, ' / START_POSITION = ', int(float(xdisplay)/float(fr_graph_div)), int(ydisplay/3))
    xp_tooltip = '//*[@class="chart-tooltip"]'
    toolTip = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xp_tooltip)))
    move0 = movearound_showtext(driver, toolTip, int(float(xdisplay)/float(fr_graph_div)), int(ydisplay/3), 'x', value_EMA)
    arrear = move0[0]
    chktext = move0[-1]
    stepadd = 5
    for steppx in range(1, xdisplay, stepadd):
        if int(arrear / 8) % 2 == 0:
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
            if cont_or_stop == 'Y' or cont_or_stop == 1:
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
            else:
                break
        if arrear > xdisplay + 190 - 15:
            print('xlocation = ', arrear, ' / xdisplay = ', xdisplay)
            break
    xp_backbutton = '//*[@id="search-header"]//*[@data-dojo-attach-point="backButtonNode"]'
    driver.find_element_by_xpath(xp_backbutton).click()
    driver.find_element_by_xpath(xp_backbutton).click()

def main_collect_data(driver, currency, value_EMA, time_period, grph_div_start, cont_or_stop):
    driver = from_search_goto_specific_currency(driver, currency)
    driver = change_graph_to_candlestick(driver)
    driver = set_graph_EMA_value(driver, value_EMA)
    graph_timeperiod = change_graph_time_period(driver, time_period)
    driver = graph_timeperiod[0]
    timesequence = graph_timeperiod[-1]
    # collect data from graph
    collecting_data_on_graph(driver, grph_div_start, cont_or_stop, timesequence)
    return driver

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
            list_text[0:1] + list_text[3:7] + list_text[11:13] + list_text[-2:] +
            [fxstatus[0], fxstatus[1], fxstatus[2], fxstatus[3], fxstatus[-2],
             fxstatus[-1]]).replace('Tick volume', 'TickV')
    else:
        text = " / ".join(list_text[0:3])
    return text

def forex_status_diffEMA(open, close, ema, value_EMA):
    diffopenclose = float(close) - float(open)
    diffema = float(ema) - float(close)
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
    hampir = abs(20000 * diffema / (float(ema) + float(close)))
    if hampir < 0.5:
        peratus = str("%.5f" % round(hampir, 5)) + '_###X'
    elif int(hampir) == 0:
        peratus = str("%.5f" % round(hampir, 5)) + '_#X'
    else:
        peratus = str("%.5f" % round(hampir, 5))
    return statusfx, str("%.5f" % round(diffopenclose, 5)), statusema, str("%.5f" % round(diffema, 5)), 'NEAR', peratus

### STEPS BY STEPS running

# 1) start webdriver
chromebrowserdriver = google_chrome_browser()

# 2) login
base_url = "https://www.trading212.com"
user1 = "mycromox@gmail.com"
pswd1 = "Serverg0d!"
driver1 = autologin_maxwindows(chromebrowserdriver, base_url, user1, pswd1)

# 3) pop-up window (which ask to upload ID documents)
driver2 = close_popup_ask_upload_docs(driver1)

# 4) go to speficic currency or looping all currencies
value_EMA = 75
tperiod = '15 minutes'
grph_div_start_point = 2  # division graph of starting point? ( value = 1.28 to infinity)
cont_or_stop = 'N'  # at end of the graph - wait&collecting newdata 'Y' or stop/break 'N'?

# currency2 = "GBP/USD"
# currency2 = "EUR/USD"
# currency2 = "USD/CAD"
# currency2 = "USD/JPY"
# currency2 = "USD/CHF"
# currency2 = "AUD/USD"
# currency2 = "NZD/USD"

# main_collect_data(driver2, "EUR/USD", value_EMA, tperiod, grph_div_start_point, cont_or_stop)

for currency in ["GBP/USD", "EUR/USD", "USD/JPY", "USD/CHF", "USD/CAD", "AUD/USD", "NZD/USD"]:
    main_collect_data(driver2, currency, value_EMA, tperiod, grph_div_start_point, cont_or_stop)