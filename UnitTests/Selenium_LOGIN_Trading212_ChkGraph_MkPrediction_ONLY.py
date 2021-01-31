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
import requests

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
    # //*[@id="onfido-upload"]/div[1]/div[2]
    xpath1 = '//div[@id="onfido-upload"]//div[@class="close-icon svg-icon-holder"]'
    try:
        driver.find_element_by_xpath(xpath1).click()
        return driver
    except:
        return driver

def mode_live_or_demo(driver, mode):
    current_url = driver.current_url
    urlmode = current_url.split('//')[-1].split(".")[0]     #  -- > live or demo
    if urlmode == "live" and mode == "Practice":
        elem = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "account-menu-button")))
        elem.click()
        try:
            elem = driver.find_element_by_class_name("green")
            elem.click()
        except:
            return driver
    elif urlmode == "demo" and mode == "Real":
        elem = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "account-menu-button")))
        elem.click()
        try:
            elem = driver.find_element_by_class_name("blue")
            elem.click()
        except:
            return driver
    return driver

##### FUNCTIONS FOR READ DATA FROM GRAPH FOR ALL CURRENCIES

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
    return driver

def change_graph_to_candlestick(driver):
    xp_templatebar = '//*[@class="chart-menu"]//*[@data-dojo-attach-point="templatesArrowNode"]'
    elements = driver.find_elements_by_xpath(xp_templatebar)
    # print('number of elements = ', len(elements))
    element_template = elements[-1]
    element_template.click()
    # xp_pro_tab = '//*[@id="chart-templates"]/div[2]/div/div/div/div'
    xp_pro_tab = '//*[@id="chart-templates"]//*[contains(text(), "PRO")]'
    driver.find_element_by_xpath(xp_pro_tab).click()
    element_template.click()
    # print('-- > END 1 - Candlestick')
    return driver

def set_graph_EMA_value(driver, value_EMA):
    xp_indicator = '//*[@id="chartTabIndicators"]//*[@data-dojo-attach-point="indicatorsArrowNode"]'
    elements = driver.find_elements_by_xpath(xp_indicator)
    element_indicator = elements[-1]
    element_indicator.click()
    driver.find_element_by_xpath("//*[contains(text(),'Trend')]").click()
    # driver.find_element_by_xpath("//*[contains(text(),'EMA')]").click()  # < -- if using EMA
    driver.find_element_by_css_selector(".item-trend-sma").click()         # < -- if using Simple Moving Average (SMA)
    xp_period = '//*[@id="chart-settings"]//*[@class="editable-input"]'
    element_period = driver.find_element_by_xpath(xp_period)
    element_period.clear()
    element_period.send_keys(str(value_EMA))
    if driver.find_element_by_xpath("//div[@id='chart-settings']/div[3]/div[3]/div[2]/div"):
        driver.find_element_by_xpath("//div[@id='chart-settings']/div[3]/div[3]/div[2]/div").click()
        driver.find_element_by_css_selector(".item-colorpicker-be4138").click()
    # confirm button
    driver.find_elements_by_xpath('//div[@class="window-controls"]/div[@class="button confirm-button"]')[0].click()
    # driver.find_element_by_xpath("//*[contains(text(),'Confirm')]").click()
    # print('-- > END 2 -', value_EMA, 'EMA line')
    return driver

def change_graph_time_period(driver, time_period):
    driver.find_elements_by_xpath('//*[@id="chartTabPeriods"]//*[@class="arrow-icon svg-icon-holder"]')[-1].click()
    driver.find_element_by_xpath('//*[contains(text(), "' + time_period + '")]').click()
    # print('-- > END 3 - set time period ' + time_period)
    sleep(1)
    return driver

def collecting_data_on_graph(driver, fr_graph_div):
    data_list = []
    EMA_list = []
    lebar = driver.execute_script("return window.innerWidth")
    tinggi = driver.execute_script("return window.innerHeight")
    # print('LEBAR x = ', lebar, ' / TINGGI y = ', tinggi)
    xp_chart_container = '//*[((@class="chart-container") or (@class="chart-container draggable")) and (@tabindex="-1")]'
    elements_chart_container = driver.find_elements_by_xpath(xp_chart_container)
    xdisplay = lebar
    ydisplay = tinggi
    if elements_chart_container[-1].get_attribute('style') != None:
        xdisplay = int(
            elements_chart_container[-1].get_attribute('style').split(';')[0].split('width:')[-1].split('px')[0])
        ydisplay = int(
            elements_chart_container[-1].get_attribute('style').split(';')[1].split('height:')[-1].split('px')[0])
    # print('DISPLAY = ( x y ) ', xdisplay, ydisplay, ' / START_POSITION = ', int(float(xdisplay)/float(fr_graph_div)), int(ydisplay/4))
    xp_tooltip = '//*[@class="chart-tooltip"]'
    toolTip = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xp_tooltip)))
    sleep(1)
    move0 = movearound_showtext(driver, toolTip, int(float(xdisplay)/float(fr_graph_div)), int(ydisplay/4), 'x')
    arrear = move0[0]
    chktext = move0[-1]
    stepadd = 5
    for steppx in range(1, xdisplay, stepadd):
        if int(arrear / 8) % 2 == 0:
            ynum = -11
        else:
            ynum = -19
        move = movearound_showtext(driver, toolTip, -9, ynum, chktext)
        arrear = move[0]
        chktext = move[-1]
        if move[2] != 'duplicate' and move[2].split('/')[0].replace(' ', '') != 'xlocation':
            # print('NEWTEXT = ', move[2])
            data_list = data_list + [move[2].split('Close')[-1].split('/')[1].replace(' ', '')]
            # EMA_list = EMA_list + [move[2].split('EMA')[-1].split('/')[1].replace(' ', '')]
            EMA_list = EMA_list + [move[2].split('SMA')[-1].split('/')[1].replace(' ', '')]
        elif move[2].split('/')[0].replace(' ', '') == 'xlocation':
            # print('NEWTEXT = ', move[2])
            break
        if arrear > xdisplay + 190 - 15:
            print('xlocation = ', arrear, ' / xdisplay = ', xdisplay)
            break
    xp_backbutton = '//*[@id="search-header"]//*[@data-dojo-attach-point="backButtonNode"]'
    driver.find_element_by_xpath(xp_backbutton).click()
    driver.find_element_by_xpath(xp_backbutton).click()
    # print('DATALIST = ', data_list)
    # print('EMALIST = ', EMA_list)
    return data_list, EMA_list

## functions for tooltip value

def movearound_showtext(driver, element, x_value, y_value, prev_text):
    # print('DISPLAY = ( x2 y2 ) ', int(x_value), int(y_value))
    hoover(driver).move_to_element_with_offset(element, int(x_value), int(y_value)).perform()
    chktext = element.text.split('\n')[0].replace(' ', '')
    try:
        if chktext == prev_text:
            text = 'duplicate'
        elif str(element.text.split('\n')[4]) == 'Close':
            text = 'xlocation / ' + str(element.location['x']) + ' / ylocation / ' + str(element.location['y'])
        else:
            text = text_to_display(element.text.split('\n'))
    except:
        text = 'out_of_boundary_or_wrong_value'
    return int(element.location['x']), int(element.location['y']), text, chktext

def text_to_display(list_text):
    if len(list_text) >= 12:
        text = " / ".join(
            list_text[0:1] + list_text[3:7] + list_text[11:13] + list_text[-2:]).replace('Tick volume', 'TickV')
    else:
        text = " / ".join(list_text[0:3])
    return text

def main_collect_data(driver, currency, value_EMA, time_period, grph_div_start, dict_fx):
    arini = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    driver = from_search_goto_specific_currency(driver, currency)
    driver = change_graph_to_candlestick(driver)
    driver = set_graph_EMA_value(driver, value_EMA)
    driver = change_graph_time_period(driver, time_period)
    # collect data from graph
    collectdata = collecting_data_on_graph(driver, grph_div_start)
    datalist = collectdata[0]
    emalist = collectdata[-1]
    # gradient1 = float(datalist[-2]) - ((float(datalist[-3]) + float(datalist[-4])) / 2)
    # gradient2 = float(datalist[-3]) - ((float(datalist[-4]) + float(datalist[-5])) / 2)
    # gradient3 = float(datalist[-4]) - ((float(datalist[-5]) + float(datalist[-6])) / 2)
    gradient1 = float(datalist[-2]) - float(datalist[-3])
    gradient2 = float(datalist[-3]) - float(datalist[-4])
    gradient3 = float(datalist[-4]) - float(datalist[-5])
    ### convert to GBP
    gradient1x = 5000 * gradient1 / float(dict_fx[currency.split('/')[-1]])
    gradient2x = 5000 * gradient2 / float(dict_fx[currency.split('/')[-1]])
    gradient3x = 5000 * gradient3 / float(dict_fx[currency.split('/')[-1]])
    text1 = ''
    # if gradient3x < gradient2x < gradient1x and float(datalist[-5]) <= float(emalist[-5]) and \
    #         abs(gradient1x) > float(0.7) and float(datalist[-1]) >= float(datalist[-2]):
    #     text1 = text1 + ' BUY/LONG1'
    # if gradient3x > gradient2x > gradient1x and float(datalist[-2]) > float(emalist[-2]) + float(0.0001) \
    #         and abs(gradient1x) > float(0.7) and float(datalist[-1]) < float(datalist[-2]):
    #     text1 = text1 + ' SELL/SHORT1'
    # if float(datalist[-4]) < float(datalist[-3]) < float(datalist[-2]) and float(datalist[-5]) <= float(emalist[-5]) \
    #         and abs(gradient1x) > float(0.7) and float(datalist[-1]) >= float(datalist[-2]):
    #     text1 = text1 + ' BUY/LONG2'
    # if float(datalist[-4]) > float(datalist[-3]) > float(datalist[-2]) and float(datalist[-2]) > float(emalist[-2]) \
    #         + float(0.0001) and abs(gradient1x) > float(0.7) and float(datalist[-1]) < float(datalist[-2]):
    #     text1 = text1 + ' SELL/SHORT2'
    # if float(datalist[-5]) <= float(emalist[-5]) and float(datalist[-2]) > float(emalist[-2]) \
    #         and float(datalist[-1]) >= float(datalist[-2]):
    #     text1 = text1 + ' BUY/LONG3'
    # if float(datalist[-5]) > float(emalist[-5]) + float(0.00075) and abs(float(datalist[-2]) - float(emalist[-2])) \
    #         < float(0.00025) and float(datalist[-1]) < float(datalist[-2]):
    #     text1 = text1 + ' SELL/SHORT3'
    if gradient3x < gradient2x < gradient1x and abs(gradient1x) > float(0.7) and \
            float(datalist[-1]) >= float(datalist[-2]):
        text1 = text1 + ' BUY/LONG1 @ ' + str(datalist[-1])
    if gradient3x > gradient2x > gradient1x and abs(gradient1x) > float(0.7) and \
            float(datalist[-1]) < float(datalist[-2]):
        text1 = text1 + ' SELL/SHORT1 @ ' + str(datalist[-1])
    if float(datalist[-4]) < float(datalist[-3]) < float(datalist[-2]) and abs(gradient1x) > float(0.7) \
            and float(datalist[-1]) >= float(datalist[-2]):
        text1 = text1 + ' BUY/LONG2 @ ' + str(datalist[-1])
    if float(datalist[-4]) > float(datalist[-3]) > float(datalist[-2]) and abs(gradient1x) > float(0.7) \
            and float(datalist[-1]) < float(datalist[-2]):
        text1 = text1 + ' SELL/SHORT2 @ ' + str(datalist[-1])
    if float(datalist[-5]) <= float(emalist[-5]) and float(datalist[-2]) > float(emalist[-2]) \
            and float(datalist[-1]) >= float(datalist[-2]):
        text1 = text1 + ' BUY/LONG3 @ ' + str(datalist[-1])
    if float(datalist[-5]) > float(emalist[-5]) + float(0.00075) and abs(float(datalist[-2]) - float(emalist[-2])) \
            < float(0.00025) and float(datalist[-1]) < float(datalist[-2]):
        text1 = text1 + ' SELL/SHORT3 @ ' + str(datalist[-1])
    print('TIME ' + str(arini) + ' # GRADIENT for ' + currency + ' =', str("%.5f" % round(gradient3, 5)), '/', str("%.6f" % round(gradient3x, 6)),
          '//' , str("%.5f" % round(gradient2, 5)), '/', str("%.6f" % round(gradient2x, 6)),
          '//' , str("%.5f" % round(gradient1, 5)), '/', str("%.6f" % round(gradient1x, 6)), '#', text1)
    return driver

## FUNCTIONS FOR CHANGE CURRENCY

def currency_date_value():
    baseurl = 'https://www.dailyfx.com/'
    dict1 = {}
    for currency in ['gbp-usd', 'gbp-jpy', 'gbp-chf', 'gbp-cad']:
        url = baseurl + currency
        out1 = requests.get(url = url)
        data = []
        for line in out1.text.split('\n'):
            if 'data-value=' in line:
                if 'data-value="--' not in line:
                    data = data + [line]
        datalast = data[-1]
        data_list = [float(x) for x in datalast.split('=')[1].split('"')[1].split(',')]
        average = sum(data_list)/len(data_list)
        dict1[currency.replace('gbp-', '').upper()] = "%.7f" % round(average, 7)
    return dict1

## FUNCTIONS FOR BUY / SELL / CLOSE_POSITION

def buy(driver, amount):
    if driver.find_element_by_xpath("//div[@class='visible-input']//input[contains(@id, 'uniqName')]"):
        # element = WebDriverWait(driver, 5).until(EC.visibility_of_element_located(
        #             (By.XPATH, "//div[@class='visible-input']//input[contains(@id, 'uniqName')]")))
        element = driver.find_elements_by_xpath("//div[@class='visible-input']//input[contains(@id, 'uniqName')]")[0]
        element.clear()
        for character in str(amount):
            element.send_keys(character)
            sleep(0.5)
        # Confirm Button
        if driver.find_element_by_xpath("//div[contains(@class,'confirm-button')]"):
            driver.find_elements_by_xpath("//div[contains(@class,'confirm-button')]")[0].click()
    elif driver.find_element_by_xpath("//*[contains(text(),'Market closed')]"):
        print('Market closed')
        driver.find_elements_by_xpath("//*[@class='header']//*[@class='close-icon']")[0].click()

def sell(driver, amount):
    # Switching to sell
    driver.find_elements_by_xpath("//div[@data-dojo-attach-event='click: setDirectionSell']")[0].click()
    # From there on it's exactly like the buy
    buy(driver, amount)

def script_click_xpath(driver, xpath):
    driver.execute_script(f"document.evaluate(\"{xpath}\", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click()")

def open_stock_dialog(driver, stock):
    WebDriverWait(driver, 5).until(EC.visibility_of_any_elements_located((By.XPATH, "//span[contains(@data-dojo-attach-event, 'onOpenDialogClick')]")))
    elem = driver.find_elements_by_xpath("//span[contains(@data-dojo-attach-event, 'onOpenDialogClick')]")
    # try both elements
    try:
        elem[0].click()
    except:
        elem[1].click()
    # Search the stock
    elem = driver.find_element_by_xpath("//input[@placeholder=\"Instrument search\"]")
    # Setting the max length to 100 so the API'll be able to enter long stocks names
    driver.execute_script("arguments[0].setAttribute('maxlength',arguments[1])", elem, 100)
    elem.send_keys(stock)
    # Open its dialog with JS. Selenium couldn't open the dialog itself.
    script_click_xpath(driver, f"//*[@id='list-results-instruments']//span[contains(@class, 'instrument-name') and .='{stock}']")
    sleep(1)

def buy_stock(driver, stock, amount):
    open_stock_dialog(driver, stock)
    buy(driver, amount)
    sleep(0.5)

def sell_stock(driver, stock, amount):
    # It's just opening a stock and selling it
    open_stock_dialog(driver, stock)
    sell(driver, amount)
    sleep(0.5)

def list_CFD_open_position(driver):
    instrument_list = driver.find_elements_by_xpath('//table[@data-dojo-attach-point="tableNode"]//tr')
    sleep(1)
    free_fund = driver.find_elements_by_xpath(
        '//*[@id="equity-free"]/span[@data-dojo-attach-point="valueNode"]')[-1].text.replace(' ', '')
    total_fund = driver.find_elements_by_xpath(
        '//*[@id="equity-total"]/span[@data-dojo-attach-point="valueNode"]')[-1].text.replace(' ', '')
    result = driver.find_elements_by_xpath(
        '//*[@id="equity-ppl"]/span[@data-dojo-attach-point="valueNode"]')[-1].text.replace(' ', '')
    print('# No of Instruments = ', len(instrument_list), ' / Total Fund = ', total_fund, ' / Free Fund = ',
          free_fund, ' / Live Result = ', result)
    dict1 = {}
    dict2 = {}
    if len(instrument_list) >= 1:
        i = 1
        for ele in instrument_list:
            id_ele = ele.get_attribute('id')
            print(i, end=' ) ')
            text = ''
            for info in ["name", "quantity", "direction", "averagePrice", "currentPrice", "margin", "ppl"]:
                xpathx = f"//table[@data-dojo-attach-point='tableNode']//tr[@id='{id_ele}']//td[contains(@class,'{info}')]"
                element = driver.find_elements_by_xpath(xpathx)[0]
                print(info, "=", element.text.replace(' ', ''), end=' / ')
                text = text + element.text.replace(' ', '') + ' / '
            dict1[i] = id_ele
            dict2[i] = text
            i += 1
            print()
    return driver, dict1, dict2

def pilihan_to_close_position(num_choice):
    # pilihan = 0
    if num_choice > 3:
        pilihan = input("Your Choice ? CLOSE [ 1 - " + str(num_choice - 2) + " ] or BUY/SELL [ " +
                        str(num_choice - 1) + " / " + str(num_choice) + " ] or QUIT [ x / 99 ] : ")
    elif num_choice == 3:
        pilihan = input("Your Choice ? CLOSE [ 1 ] or BUY/SELL [ " +
                        str(num_choice - 1) + " / " + str(num_choice) + " ] or QUIT [ x / 99 ] : ")
    elif num_choice == 1:
        pilihan = 1
    else:
        pilihan = input("Your Choice ? BUY/SELL [ " + str(num_choice - 1) + " / " + str(num_choice) +
                        " ] or QUIT [ x / 99 ] : ")
    try:
        return int(pilihan)
    except:
        print("Error - '" + str(pilihan) + "' is not an integer  -- >  ", end='')
        if pilihan.lower()[0] == 'b':
            return int(num_choice - 1)
        elif pilihan.lower()[0] == 's':
            return int(num_choice)
        elif pilihan.lower()[0] == 'x':
            return int(99)
        elif pilihan.lower()[0] == 'q':
            return int(99)
        else:
            return int(0)

def pilihan_buy_or_sell(dict_position):
    n = len(dict_position)
    print(n + 1, ") BUY NEW")
    print(n + 2, ") SELL NEW")
    return {'buy' : n + 1 , 'sell' : n + 2 }

def choice_currency(buysell):
    list = ["GBP/USD", "EUR/USD", "USD/JPY", "USD/CHF", "USD/CAD", "AUD/USD", "NZD/USD"]
    for curr in list:
        print(list.index(curr) + 1, ")", curr)
    currency = input("Chose currency to " + str(buysell) + " [ 1 - " + str(len(list)) + " ] : ")
    if currency in list:
        return currency
    elif 0 < int(currency) <= len(list):
        return list[int(currency) - 1]
    else:
        return 'x'

def close_position_CFD_ANY(driver):
    list_choice = list_CFD_open_position(driver)
    driver = list_choice[0]
    dict1 = list_choice[1]
    dict2 = list_choice[-1]
    buy_sell_dict = pilihan_buy_or_sell(dict1)
    number_of_choice = len(dict1) + 2
    pilihan = pilihan_to_close_position(number_of_choice)
    try:
        if  len(dict1) > 0 and len(dict1) >= int(pilihan) > 0:
            print(' -- > Close Position [', str(pilihan), '] =', dict2[int(pilihan)])
            confirmation = input("Confirm to CLOSE position [ " + str(pilihan) + " ] ? [ Y / N ] : ")
            id_ele = dict1[int(pilihan)]
            if confirmation.lower() == 'y':
                xpathto = f"//table[@data-dojo-attach-point='tableNode']//tr[@id='{id_ele}']//div[@class='close-icon svg-icon-holder']"
                driver.find_elements_by_xpath(xpathto)[0].click()
                driver.find_elements_by_xpath(f"//span[@class='btn btn-primary' and text()='OK']")[0].click()
                sleep(2)
            else:
                print("CHANGE MIND!! - Didn't CLOSE [", str(pilihan), '] =', dict2[int(pilihan)])
        elif int(pilihan) == buy_sell_dict['buy']:
            currency = choice_currency("BUY")
            amount = input('Amount to BUY (min 500) : ')
            try:
                if currency != 'x':
                    buy_stock(driver, currency, int(amount))
                else:
                    print('Wrong currency')
            except:
                print('ERROR on BUY')
        elif int(pilihan) == buy_sell_dict['sell']:
            currency = choice_currency("SELL")
            amount = input('Amount to SELL (min 500) : ')
            try:
                if currency != 'x':
                    sell_stock(driver, currency, int(amount))
                else:
                    print('Wrong currency')
            except:
                print('ERROR on SELL')
        elif int(pilihan) == 99:
            print("You choose - QUIT/EXIT !!")
            driver.close()
        else:
            print("Out of range")
        return pilihan
    except:
        print("Nothing TODO")
        return pilihan

##### STEPS BY STEPS running  #########

# 1) start webdriver
chromebrowserdriver = google_chrome_browser()

# 2) login
base_url = "https://www.trading212.com"
# user1 = "roslitalib2017@gmail.com"
# pswd1 = "Malaysia123"
user1 = "mycromox@gmail.com"
pswd1 = "Serverg0d!"
driver = autologin_maxwindows(chromebrowserdriver, base_url, user1, pswd1)

# 3) pop-up window (which ask to upload ID documents)
driver = close_popup_ask_upload_docs(driver)

# 4) switch to Practice Mode   # Real or Practice
driver = mode_live_or_demo(driver, "Practice")

# 5) go to speficic currency or looping all currencies
# value_EMA = 21
# # tperiod = '5 minutes'
# tperiod = '10 minutes'
# grph_div_start_point = 1.328  # division graph of starting point? ( value = 1.28 to infinity)
#
# fxconvert = currency_date_value()
# # print(fxconvert)
#
# for currency in ["GBP/USD", "EUR/USD", "USD/JPY", "USD/CHF", "USD/CAD", "AUD/USD", "NZD/USD"]:
#     driver = main_collect_data(driver, currency, value_EMA, tperiod, grph_div_start_point, fxconvert)

# driver = main_collect_data(driver, "GBP/USD", value_EMA, tperiod, grph_div_start_point, fxconvert)

# # 6) Buy/Sell/Close_Position
#
# pilihan = 0
# while pilihan != 99 :
#     print()
#     pilihan = close_position_CFD_ANY(driver)

#### LOOP PRODUCE DATA

tt = 1
while tt != 99:
    value_EMA = 25
    # tperiod = '1 minute'
    tperiod = '5 minutes'
    # tperiod = '10 minutes'
    # tperiod = '15 minutes'
    grph_div_start_point = 1.329  # division graph of starting point? ( value = 1.28 to infinity)
    fxconvert = currency_date_value()
    for currency in ["GBP/USD", "EUR/USD", "USD/JPY", "USD/CHF", "USD/CAD", "AUD/USD", "NZD/USD"]:
        driver = main_collect_data(driver, currency, value_EMA, tperiod, grph_div_start_point, fxconvert)
    # sleep(60)
    print()
    ttt = input('CHOICE [ OTHERS - TO RERUN ] / [ x / 99 - TO STOP ] : ')
    try:
        tt = int(ttt)
    except:
        if ttt.lower()[0] == 'x':
            tt = int(99)
        else:
            tt = int(0)
    if tt == 99:
        driver.close()