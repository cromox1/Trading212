__author__ = 'cromox'

from time import sleep
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.action_chains import ActionChains as hoover

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

## FUNCTIONS FOR BUY / SELL / CLOSE_POSITION

def buy(driver, amount):
    if driver.find_element_by_xpath("//*[contains(text(),'Market closed')]"):
        print('Market closed')
        driver.find_elements_by_xpath("//*[@class='header']//*[@class='close-icon']")[0].click()
    else:
        element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
            (By.XPATH, "//div[@class='visible-input']//input[contains(@id, 'uniqName')]")))
        element.clear()
        for character in str(amount):
            element.send_keys(character)
            sleep(0.5)
        # Confirm Button
        if driver.find_element_by_xpath("//div[contains(@class,'confirm-button')]"):
            driver.find_elements_by_xpath("//div[contains(@class,'confirm-button')]")[0].click()


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

def stock_simple_information(driver, stock):
    # position info
    nombor = len(driver.find_elements_by_xpath(f"//td[@class='name' and text()='{stock}']"))
    print()
    if nombor >= 1:
        for i in range(nombor):
            print(i+1, ') name =', stock, end=' / ')
            for info in ["quantity", "direction", "averagePrice", "currentPrice", "margin", "ppl"]:
                element = driver.find_elements_by_xpath(
                    f"//td[@class='name' and text()='{stock}']/following::td[contains(@class,'{info}')]")[i]
                print(info, "=", element.text.replace(' ', ''), end=' / ')
            print()
    else:
        print("No position/stock for", stock)
    return nombor

def list_CFD_open_position(driver):
    instrument_list = driver3.find_elements_by_xpath('//table[@data-dojo-attach-point="tableNode"]//td[@class="name"]')
    dict1 = {}
    ix = 1
    jy = 0
    for ele in instrument_list:
        if ele.text not in [x[0] for x in list(dict1.values())]:
            jy = 0
            dict1[ix] = [ele.text, jy]
        else:
            jy += 1
            dict1[ix] = [ele.text, jy]
        ix += 1
    for kk, vv in dict1.items():
        stock = str(vv[0])
        tlox = int(vv[1])
        print(kk, ') name =', stock, end=' / ')
        for info in ["quantity", "direction", "averagePrice", "currentPrice", "margin", "ppl"]:
            xpathcreate = f"//td[@class='name' and text()='{stock}']/following::td[contains(@class,'{info}')]"
            element = driver.find_elements_by_xpath(xpathcreate)[tlox]
            print(info, "=", element.text.replace(' ', ''), end=' / ')
        print()
    return driver, dict1

def pilihan_to_close_position(num_choice):
    pilihan = 0
    if num_choice > 1:
        pilihan = input("Your Choice ? CLOSE [ 1 - " + str(num_choice - 2) + " ] or BUY/SELL [ " +
                        str(num_choice - 1) + " / " + str(num_choice) + " ] or QUIT [ x / 99 ] : ")
    elif num_choice == 1:
        pilihan = 1
    try:
        return int(pilihan)
    except:
        print("Error - Not an integer =", pilihan)
        if pilihan.lower()[0] == 'b':
            return int(num_choice - 1)
        elif pilihan.lower()[0] == 's':
            return int(num_choice)
        elif pilihan.lower()[0] == 'x':
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
    buy_sell_dict = pilihan_buy_or_sell(dict1)
    number_of_choice = len(dict1) + 2
    pilihan = pilihan_to_close_position(number_of_choice)
    try:
        if 0 < int(pilihan) <= len(dict1):
            confirmation = input("Confirm to CLOSE position [ " + str(pilihan) + " ] ? [ Y / N ] : ")
            stock = str(dict1[int(pilihan)][0])
            iloct = int(dict1[int(pilihan)][1])
            if confirmation.lower() == 'y':
                xpathcreate = f"//td[@class='name' and text()='{stock}']/following::div[@class='close-icon svg-icon-holder']"
                driver.find_elements_by_xpath(xpathcreate)[iloct].click()
                driver.find_elements_by_xpath(f"//span[@class='btn btn-primary' and text()='OK']")[0].click()
                sleep(2)
            else:
                print("CHANGE MIND!! - Didn't CLOSE ", stock)
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
        else:
            print("Out of range")
        return pilihan
    except:
        print("Nothing TODO")
        return pilihan

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

# 4) switch to Practice Mode   # Real or Practice
driver3 = mode_live_or_demo(driver2, "Practice")

# # 5) Buy/Sell/Close_Position
pilihan = 0
while pilihan != 99 :
    print()
    pilihan = close_position_CFD_ANY(driver3)