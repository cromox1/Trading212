## THIS REQUIRED - TO MAKE IT RUN ON CONSOLE / COMMAND LINE / CLI
import sys
sys.path.extend(['C:\\Users\\cromox\\PycharmProjects\\Trading212', 'C:/Users/cromox/PycharmProjects/Trading212'])

from datetime import datetime
from pytz import timezone
from Forex_CFD.base.webdriverfactory import WebDriverFactory as WebBrowser
from Forex_CFD.features.final_fx_decision import FxFinalDecision

## USER'S PARAMETER
_USERNAME       = "xixa01@yahoo.co.uk"
_PASSWORD       = "H0meBase"
# _USERNAME     = "mycromox@gmail.com"
# _PASSWORD     = "Serverg0d!"

# Chrome
_CHROME_NAME    = 'chrome'
_CHROME_DRIVER  = r'C:\tools\chromedriver\chromedriver.exe'
# IE
_IE_NAME        = 'ie'
_IE_DRIVER      = r'C:\tools\Python36\Scripts\IEDriverServer_x64_2.42.0.exe'
    # # iedriverserver = r'C:\tools\Python36\Scripts\IEDriverServer_x64_3.12.0.exe' ## not working
    # # iedriverserver = r'C:\tools\Python36\Scripts\IEDriverServer_x32_3.4.0.exe'  ## work but 32bit
# Safari
_SAFARI_NAME    = 'safari'
_SAFARI_DRIVER  = r'C:\tools\Python36\Scripts\SafariDriver.exe'
# Brave
_BRAVE_NAME     = 'brave'
_BRAVE_EXE      = r'C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe'
_BRAVE_DRIVER   = r'C:\tools\chromedriver\chromedriver.exe'       # Brave use ChromeDriver
# Opera
_OPERA_NAME     = 'opera'
_OPERA_DRIVER   = r'C:\tools\operadriver_win64\operadriver.exe'
    # # OperaDriver - win64 2.36 - https://github.com/operasoftware/operachromiumdriver/releases
    # # OperaDriver - win64 2.36 - https://github.com/operasoftware/operachromiumdriver/releases
_OPERA_INST_DIR = r'C:\Program Files\Opera\\'
    # # _operaInstDir = r'C:\tools\Opera\\'
# Firefox
_FIRFEFOX_NAME  = 'firefox'
# (don't need any setup)

##### STEPS BY STEPS running  #########

# 1) start webdriver
base_url = "https://www.trading212.com"
browser_driver = WebBrowser(_CHROME_NAME, driver_path=_CHROME_DRIVER).getWebDriverInstance(base_url)
# browser_driver = WebBrowser(_OPERA_NAME, browser_inst_dir=_OPERA_INST_DIR, driver_path=_OPERA_DRIVER).getWebDriverInstance(base_url)
# browser_driver = WebBrowser(_BRAVE_NAME, driver_path=_BRAVE_DRIVER, browser_exe=_BRAVE_EXE).getWebDriverInstance(base_url)

# 2) login
fxfinal = FxFinalDecision(browser_driver)
fxfinal.autologin_firstwindows(base_url, _USERNAME, _PASSWORD)

# 3) pop-up window (which ask to upload ID documents)
fxfinal.close_popup_ask_upload_docs()

# 4) switch to Practice Mode   # Real or Practice
fxfinal.mode_live_or_demo("Practice")

# 5) go to speficic currency or looping all currencies   # looping_check_all_currencies(driver)
### AUTO RUN SCRIPTS - BUY / SELL / CLOSE POSITION AUTOMATICALLY & CONTINOUSLY

pilihan = 0
while pilihan != 99:
    ## parameter1 - graph parameters
    value_EMA = 25
    list_tperiod = ['1 minute', '10 minutes']
    ## parameter2 - running function parameters
    buymark = 12    # buymark = 14
    sellmark = -12  # sellmark = -14
    buystartprice = 521
    sellstartprice = 511
    closesellpoint = 4
    closebuypoint = -4
    limit_buysell = 3
    hardprofit = 0.51
    exitprofit = 0.09
    delaymins = 0.5  # delay in mins before execute the script
    timemins = 5  # time in mins between every script execution / running
    ## parameter3 - general parameter
    all_currencies = fxfinal.currencies_to_use('major')

    ### EXISTING AUTO TRADER
    epochstart = int(datetime.now(timezone('Europe/London')).timestamp())
    check_cfd_current = fxfinal.close_position_CFD_ANY_auto(value_EMA, list_tperiod, limit_buysell)
    todopoint = check_cfd_current[0]
    open_position = check_cfd_current[1]
    tocloseone = check_cfd_current[2]
    instrument_id = check_cfd_current[3]
    masastart = check_cfd_current[4]

    ### FOREX AUTO TRADER
    print('\n# FINAL_ToDoPoint =', todopoint)
    print('# FINAL_ToCloseOne =', tocloseone)
    print()
    print('1) BUYSELL_INSTRUMENT // BUY # IF POINT >', buymark, ' / SELL # IF POINT <', sellmark)
    print(' - > BUYSELL_POINT =', todopoint)
    current_number = len(instrument_id)
    list_add_instrument = fxfinal.buy_sell_list_add_instrument(
        todopoint, current_number, limit_buysell, buymark, sellmark)
    dict_buy_sell = fxfinal.final_dict_buy_sell_currency(
        list_add_instrument, todopoint, open_position, all_currencies, buymark, buystartprice, sellmark, sellstartprice)
    if len(dict_buy_sell[0]) > 0:
        for k, v in dict_buy_sell[0].items():
            fxfinal.buy_stock(k, v)
    if len(dict_buy_sell[-1]) > 0:
        for k, v in dict_buy_sell[-1].items():
            fxfinal.sell_stock(k, v)

    print('2) CLOSE_POSITION // BECAUSE CHANGE_DIRECTION: BUY <', closebuypoint, '/ SELL >', closesellpoint, 'OR PROFIT >', hardprofit)
    print(' - > OPEN_POSITION =', open_position)
    if len(open_position) > 0:
        for ko,vo in open_position.items():
            id_elem = instrument_id[ko]
            buysell = fxfinal.direction_elementid(id_elem)
            directionpoint = tocloseone[ko]     # only work when all currencies in todopoint
            fxfinal.open_position_printstatus(
                ko, vo, buysell, directionpoint, closebuypoint, closesellpoint)
            elementid_toclose = fxfinal.final_close_position_elemenid(
                ko, vo, buysell, directionpoint, hardprofit, closebuypoint, closesellpoint, exitprofit, id_elem)
            if elementid_toclose != None:
                fxfinal.close_position_elementid(elementid_toclose)

    fxfinal.time_script_running_and_next(masastart, delaymins, timemins)