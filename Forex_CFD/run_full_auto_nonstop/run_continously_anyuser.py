## THIS REQUIRED - TO MAKE IT RUN ON CONSOLE / COMMAND LINE / CLI
import sys
sys.path.extend(['C:\\Users\\cromox\\PycharmProjects\\Trading212', 'C:/Users/cromox/PycharmProjects/Trading212'])

from datetime import datetime
from pytz import timezone
from time import sleep
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
    value_EMA = 25
    list_tperiod = ['1 minute', '10 minutes']
    epochstart = int(datetime.now(timezone('Europe/London')).timestamp())
    check_cfd_current = fxfinal.close_position_CFD_ANY_auto(value_EMA, list_tperiod)
    todopoint = check_cfd_current[0]
    open_position = check_cfd_current[1]
    tocloseone = check_cfd_current[2]
    instrument_id = check_cfd_current[3]
    masastart = check_cfd_current[4]

    ### FOREX AUTO TRADER
    buymark = 14
    sellmark = -14
    closesellpoint = 4
    closebuypoint = -4
    # closeloss = -0.75
    hardprofit = 0.51
    exitprofit = 0.11
    delaymins = 0.5  # delay in mins before execute the script
    timemins = 5  # time in mins between every script execution / running

    print()
    print('1) BUYSELL_INSTRUMENT // BUY # IF POINT >', buymark, ' / SELL # IF POINT <', sellmark)
    print(' - > BUYSELL_POINT =', todopoint)
    for kt, vt in todopoint.items():
        all_currencies = ["GBP/USD", "EUR/USD", "USD/JPY", "USD/CHF", "USD/CAD", "AUD/USD", "NZD/USD"]
        if vt > buymark and kt not in open_position:
            amount = 521 + all_currencies.index(kt)
            print('TO BUY = (Currency)', kt, '(Amount)', amount)
            fxfinal.buy_stock(kt, amount)
        elif vt < sellmark and kt not in open_position:
            amount = 511 + all_currencies.index(kt)
            print('TO SELL = (Currency)', kt, '(Amount)', amount)
            fxfinal.sell_stock(kt, amount)
    print('2) CLOSE_POSITION // BECAUSE CHANGE_DIRECTION: BUY <', closebuypoint, '/ SELL >', closesellpoint)
    # print(' - > DIRECTN_POINT =', tocloseone)
    print(' - > OPEN_POSITION =', open_position)
    for ko,vo in open_position.items():
        id_elem = instrument_id[ko]
        buysell = fxfinal.direction_elementid(id_elem)
        directionpoint = tocloseone[ko]     # only work when all currencies in todopoint
        print('  -- > ', ko, ' # DIRECTION =', buysell, '/ CURRENT_DIRECTION_POINT =', directionpoint, end='')
        if buysell == 'BUY' and directionpoint > 0:
            print(' # - > RIGHT DIRECTION')
        elif buysell == 'SELL' and directionpoint < 0:
            print(' # - > RIGHT DIRECTION')
        elif directionpoint == 0:
            print(' # - >', buysell, 'BUT NO DIRECTION CURRENTLY!!!')
        elif buysell == 'BUY' and closebuypoint < directionpoint < 0:
            print(' # - > SLIGHTLY WRONG DIRECTION !!! TO CHECK FOR NEXT RUN')
        elif buysell == 'SELL' and closesellpoint > directionpoint > 0:
            print(' # - > SLIGHTLY WRONG DIRECTION !!! TO CHECK FOR NEXT RUN')
        else:
            print(' # - > WRONG DIRECTION !!! -- URGENT - TO CLOSE POSITION')
        if vo > hardprofit:
            print('    - > TO CLOSE #', ko, '// ACHIEVED Target Hard_Profit ( >', hardprofit, ') =', vo)
            fxfinal.close_position_elementid(id_elem)
        elif buysell == 'BUY' and directionpoint < closebuypoint and vo > exitprofit:
            print('    - > TO CLOSE #', ko, '// CHANGE DIRECTION = BUY to SELL / Point =', directionpoint)
            fxfinal.close_position_elementid(id_elem)
        elif buysell == 'SELL' and directionpoint > closesellpoint and vo > exitprofit:
            print('    - > TO CLOSE #', ko, '// CHANGE DIRECTION = SELL to BUY / Point =', directionpoint)
            fxfinal.close_position_elementid(id_elem)
        # REMOVE closeloss for time being
        # elif vo < closeloss:
        #     print('    - > TO CLOSE (LOSS) = ', ko, ' / LOSS =', vo)
        #     fxfinal.close_position_elementid(id_elem)
    fxfinal.time_script_running_and_next(masastart, delaymins, timemins)