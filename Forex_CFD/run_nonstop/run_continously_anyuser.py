from Forex_CFD.base.webdriverfactory import WebDriverFactory as webbrowser
from Forex_CFD.features.final_fx_decision import FxFinalDecision

##### STEPS BY STEPS running  #########

# 1) start webdriver
base_url = "https://www.trading212.com"
chromebrowserdriver = webbrowser('chrome').getWebDriverInstance(base_url)

# 2) login
user1 = "mycromox@gmail.com"
pswd1 = "Serverg0d!"

fxfinal = FxFinalDecision(chromebrowserdriver)
fxfinal.autologin_maxwindows(base_url, user1, pswd1)

# 3) pop-up window (which ask to upload ID documents)
fxfinal.close_popup_ask_upload_docs()

# 4) switch to Practice Mode   # Real or Practice
fxfinal.mode_live_or_demo("Practice")

# 5) go to speficic currency or looping all currencies   # looping_check_all_currencies(driver)
### AUTO RUN SCRIPTS - BUY / SELL / CLOSE POSITION AUTOMATICALLY & CONTINOUSLY

value_EMA = 25
list_tperiod = ['1 minute', '5 minutes']
check_cfd_current = fxfinal.close_position_CFD_ANY_auto(value_EMA, list_tperiod)
todopoint = check_cfd_current[0]
open_position = check_cfd_current[1]
instrument_id = check_cfd_current[-1]
print('\nBUYSELLPOINT = ', todopoint)
print('\nCLOSEINSTPOINT = ', open_position)
# for k,v in todopoint.items():
#     if v > 0:
#         print('TO BUY Currency = ', k)
#         print('Amount = ', 511 + list(todopoint.keys()).index(k))
#     elif v < 0:
#         print('TO SELL Currency = ', k)
#         print('Amount = ', 501 + list(todopoint.keys()).index(k))