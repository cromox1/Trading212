from Forex_CFD.base.webdriverfactory import WebDriverFactory as webbrowser
from Forex_CFD.features.final_fx_decision import FxFinalDecision

#### test function

def clossee_popup_ask_upload_docs(driver):
    # #upload-popup-3 > div.popup-header > div.close-icon.svg-icon-holder  # CSS selector
    # xpath1 = '//div[@id="onfido-upload"]//div[@class="close-icon svg-icon-holder"]'  # old one
    # xpath2 = '//div[@id="upload-popup-3"]//div[@class="close-icon svg-icon-holder"]'  # new one
    # try:
    #     driver.find_element_by_xpath(xpath1).click()
    # except:
    #     try:
    #         driver.find_element_by_xpath(xpath2).click()
    #     except:
    #         print('no pop-up')
    xpath = '//div[contains(@id, "upload")]//div[@class="close-icon svg-icon-holder"]'
    try:
        driver.find_element_by_xpath(xpath).click()
    except:
        print('no pop-up')

##### STEPS BY STEPS running  #########

# 1) start webdriver
base_url = "https://www.trading212.com"
chromebrowserdriver = webbrowser('chrome').getWebDriverInstance(base_url)

# 2) login
user1 = "mycromox@gmail.com"
pswd1 = "Serverg0d!"
# user1 = "xixa01@yahoo.co.uk"
# pswd1 = "H0meBase"

fxfinal = FxFinalDecision(chromebrowserdriver)
fxfinal.autologin_maxwindows(base_url, user1, pswd1)

# 3) pop-up window (which ask to upload ID documents)
driver2 = fxfinal.driver
clossee_popup_ask_upload_docs(driver2)

# 4) switch to Practice Mode   # Real or Practice
fxfinal.mode_live_or_demo("Practice")