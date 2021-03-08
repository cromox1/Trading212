## THIS REQUIRED - TO MAKE IT RUN ON CONSOLE / COMMAND LINE / CLI
import sys
sys.path.extend(['C:\\Users\\cromox\\PycharmProjects\\Trading212', 'C:/Users/cromox/PycharmProjects/Trading212'])

from datetime import datetime
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

##### STEPS BY STEPS running  #########

# 1) start webdriver
base_url = "https://www.trading212.com"
browser_driver = WebBrowser(_CHROME_NAME, driver_path=_CHROME_DRIVER).getWebDriverInstance(base_url)

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
    tperiod = '5 minutes'
    check_cfd_current = fxfinal.close_position_CFD_ANY_auto_MACD(value_EMA, tperiod)
    todopoint = check_cfd_current[0]
    open_position = check_cfd_current[1]
    tocloseone = check_cfd_current[2]
    instrument_id = check_cfd_current[3]
    masastart = check_cfd_current[4]
    epochstart = int(datetime.strptime(masastart, "%Y-%m-%d %H:%M:%S").timestamp())

    ### FOREX AUTO TRADER
    buymark = -6
    sellmark = 6
    closesellpoint = -2
    closebuypoint = 2
    limit_buysell = 4
    # closeloss = -0.85

    print()
    print('1) BUYSELL_INSTRUMENT // BUY # IF POINT <', buymark, ' / SELL # IF POINT >', sellmark)
    print(' - > BUYSELL_POINT =', todopoint)
    if len(instrument_id) <= limit_buysell:
        for kt, vt in todopoint.items():
            all_currencies = ["GBP/USD", "EUR/USD", "USD/JPY", "USD/CHF", "USD/CAD", "AUD/USD", "NZD/USD"]
            if vt < buymark and kt not in open_position:
                amount = 541 + all_currencies.index(kt)
                print('TO BUY = (Currency)', kt, '(Amount)', amount)
                fxfinal.buy_stock(kt, amount)
            elif vt > sellmark and kt not in open_position:
                amount = 531 + all_currencies.index(kt)
                print('TO SELL = (Currency)', kt, '(Amount)', amount)
                fxfinal.sell_stock(kt, amount)

    # print('2) CLOSE_POSITION // BECAUSE CHANGE_DIRECTION: BUY >', closebuypoint, '/ SELL <', closesellpoint, '// OR LOSS <', closeloss)
    print('2) CLOSE_POSITION // BECAUSE CHANGE_DIRECTION: BUY >', closebuypoint, '/ SELL <', closesellpoint)
    print(' - > OPEN_POSITION =', open_position)
    for ko,vo in open_position.items():
        id_elem = instrument_id[ko]
        buysell = fxfinal.direction_elementid(id_elem)
        directionpoint = tocloseone[ko]     # only work when all currencies in todopoint
        print('  -- > ', ko, ' # DIRECTION =', buysell, '/ CURRENT_DIRECTION_POINT =', directionpoint, end='')
        if buysell == 'BUY' and directionpoint < 0:
            print(' # - > RIGHT DIRECTION')
        elif buysell == 'SELL' and directionpoint > 0:
            print(' # - > RIGHT DIRECTION')
        elif directionpoint == 0:
            print(' # - >', buysell, ', BUT NO DIRECTION CURRENTLY!!!')
        elif buysell == 'BUY' and closebuypoint >= directionpoint > 0:
            print(' # - > SLIGHTLY WRONG DIRECTION !!! TO CHECK FOR NEXT RUN')
        elif buysell == 'SELL' and closesellpoint <= directionpoint < 0:
            print(' # - > SLIGHTLY WRONG DIRECTION !!! TO CHECK FOR NEXT RUN')
        else:
            print(' # - > WRONG DIRECTION !!! -- URGENT - TO CLOSE POSITION')
        if buysell == 'BUY' and directionpoint > closebuypoint:
            print('    - > TO CLOSE #', ko, '// CHANGE DIRECTION = BUY to SELL / Point =', directionpoint)
            fxfinal.close_position_elementid(id_elem)
        elif buysell == 'SELL' and directionpoint < closesellpoint:
            print('    - > TO CLOSE #', ko, '// CHANGE DIRECTION = SELL to BUY / Point =', directionpoint)
            fxfinal.close_position_elementid(id_elem)
        # elif vo < closeloss:
        #     print('    - > TO CLOSE (LOSS) = ', ko, ' / LOSS =', vo)
        #     fxfinal.close_position_elementid(id_elem)

    print()
    bezamasa = int(5 * 60)
    arini_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    arini_epoch = int(datetime.now().timestamp())
    lamascript = arini_epoch - epochstart
    nanti = int((arini_epoch + bezamasa) / bezamasa) * bezamasa + 61
    tidor = nanti - arini_epoch
    futuretime = datetime.fromtimestamp(nanti).strftime('%Y-%m-%d %H:%M:%S')
    print('SCRIPTS HAS RUN FOR', lamascript, 'secs', end='')
    print(', WILL RUN AGAIN AT :', futuretime, '( NOW =', arini_date, '/ in', tidor, 'secs )')
    sleep(tidor)