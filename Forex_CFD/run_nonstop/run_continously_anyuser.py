from time import sleep
from Forex_CFD.base.webdriverfactory import WebDriverFactory as webbrowser
from Forex_CFD.features.final_fx_decision import FxFinalDecision

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
fxfinal.close_popup_ask_upload_docs()

# 4) switch to Practice Mode   # Real or Practice
fxfinal.mode_live_or_demo("Practice")

# 5) go to speficic currency or looping all currencies   # looping_check_all_currencies(driver)
### AUTO RUN SCRIPTS - BUY / SELL / CLOSE POSITION AUTOMATICALLY & CONTINOUSLY

pilihan = 0
while pilihan != 99:
    value_EMA = 25
    list_tperiod = ['1 minute', '5 minutes']
    check_cfd_current = fxfinal.close_position_CFD_ANY_auto(value_EMA, list_tperiod)
    todopoint = check_cfd_current[0]
    open_position = check_cfd_current[1]
    instrument_id = check_cfd_current[-1]
    print()
    print('BUYSELLPOINT = ', todopoint)
    print('CLOSEINSTPOINT = ', open_position)
    print()
    ### AUTO TRADING
    for ko,vo in open_position.items():
        if vo < -0.35:
            # print('TO CLOSE/RUGI = ', ko, ' / ID = ', instrument_id[ko])
            print('TO CLOSE (LOSS) = ', ko)
            fxfinal.close_position_elementid(instrument_id[ko])
        if vo > 0.30:
            # print('TO CLOSE/UNTUNG = ', ko, ' / ID = ', instrument_id[ko])
            print('TO CLOSE (PROFIT) = ', ko)
            fxfinal.close_position_elementid(instrument_id[ko])
    for kt,vt in todopoint.items():
        all_currencies = ["GBP/USD", "EUR/USD", "USD/JPY", "USD/CHF", "USD/CAD", "AUD/USD", "NZD/USD"]
        if vt > 0 and kt not in open_position:
            print('TO BUY = (Currency)', kt, '(Amount)', 521 + all_currencies.index(kt))
            fxfinal.buy_stock(kt, 521 + all_currencies.index(kt))
        elif vt < 0 and kt not in open_position:
            print('TO SELL = (Currency)', kt, '(Amount)', 511 + all_currencies.index(kt))
            fxfinal.sell_stock(kt, 511 + all_currencies.index(kt))
    sleep(285)