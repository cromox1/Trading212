from Forex_CFD.base.webdriverfactory import WebDriverFactory as webbrowser
from Forex_CFD.features.final_fx_decision import FxFinalDecision

##### STEPS BY STEPS running  #########

# 1) start webdriver
base_url = "https://www.trading212.com"
chromedriver = webbrowser('chrome').getWebDriverInstance(base_url)

# 2) login
user1 = "mycromox@gmail.com"
pswd1 = "Serverg0d!"

fxfinal = FxFinalDecision(chromedriver)
fxfinal.autologin_maxwindows(base_url, user1, pswd1)

# 3) pop-up window (which ask to upload ID documents)
fxfinal.close_popup_ask_upload_docs()

# 4) switch to Practice Mode   # Real or Practice
fxfinal.mode_live_or_demo("Practice")

# 5) go to speficic currency or looping all currencies   # looping_check_all_currencies(driver)
# 6) Buy/Sell/Close_Position

## NOW COMBINE NO 5) & 6)

pilihan = 0
rerun = 'N'
value_EMA = 25
tperiod = '1 minute'      # tperiod = '1 minute' / '5 minutes' / '10 minutes' / '15 minutes'

while pilihan != 99 :
    penutup = fxfinal.close_position_CFD_ANY(value_EMA, tperiod, rerun)
    pilihan = penutup[0]
    rerun = 'N'