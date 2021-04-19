## THIS REQUIRED - TO MAKE IT RUN ON CONSOLE / COMMAND LINE / CLI
import sys
sys.path.extend(['C:\\Users\\cromox\\PycharmProjects\\Trading212', 'C:/Users/cromox/PycharmProjects/Trading212'])

from datetime import datetime
from Forex_CFD.base.webdriverfactory import WebDriverFactory as WebBrowser
from Forex_CFD.features.final_fx_decision import FxFinalDecision

## USER'S PARAMETER
# _USERNAME       = "xixa01@yahoo.co.uk"
# _PASSWORD       = "H0meBase"
_USERNAME     = "mycromox@gmail.com"
_PASSWORD     = "Serverg0d!"
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
    epochstart = int(datetime.strptime(masastart, "%Y-%m-%d %H:%M:%S GMT%z").timestamp())

    ### FOREX AUTO TRADER
    all_currencies = fxfinal.currencies_to_use('major')
    buymark = -6
    sellmark = 6
    closesellpoint = -2
    closebuypoint = 2
    limit_buysell = 3
    # closeloss = -0.85
    hardprofit = 0.51
    exitprofit = 0.11
    delaymins = 1.5             # delay in mins before execute the script
    timemins = 5                # time in mins between every script execution / running

    print()
    print('1) BUYSELL_INSTRUMENT // BUY # IF POINT <', buymark, ' / SELL # IF POINT >', sellmark)
    print(' - > BUYSELL_POINT =', todopoint)
    list_to_buysell = [vv for vv in list(todopoint.keys()) if todopoint[vv] > sellmark or todopoint[vv] < buymark]
    current_number = len(instrument_id)
    to_add_number = len(list_to_buysell)
    avail_number = limit_buysell - current_number
    if 0 < to_add_number <= avail_number:
        list_add_instrument = list_to_buysell
    elif 0 < avail_number < to_add_number:
        list_add_instrument = list_to_buysell[:avail_number]
    else:
        list_add_instrument = []
    print(' -- > LIMIT =', limit_buysell, '// CURRENT_TRADE =', current_number, '// AVAILABLE =', avail_number,
          '// TO_ADD =', to_add_number, ':: LIST = ', list_to_buysell)
    if to_add_number == 0:
        print(' --- > # NOTHING TO ADD - NO Currency MEET the requirement for MACD_Forex_Trading')
    elif to_add_number > avail_number and avail_number > 0:
        print(' --- > Limit_Trader (', limit_buysell, ') nearly reach - Mean only', avail_number, 'Currrency will be Traded',
              '- > LIST =', list_add_instrument)
    else:
        print(' --- > TO_ADD =', len(list_add_instrument), '- > LIST =', list_add_instrument)
    if len(list_add_instrument) > 0:
        for curr in list_add_instrument:
            if todopoint[curr] < buymark and curr not in open_position:
                amount = 541 + all_currencies.index(curr)
                print(' ---- > TO BUY = (Currency)', curr, '(Amount)', amount)
                fxfinal.buy_stock(curr, amount)
            elif todopoint[curr] > sellmark and curr not in open_position:
                amount = 531 + all_currencies.index(curr)
                print(' ---- > TO SELL = (Currency)', curr, '(Amount)', amount)
                fxfinal.sell_stock(curr, amount)
            else:
                print(' ---- > CANNOT ADD (Currency)', curr, '-- Already EXIST in open_position')

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
            if vo > 0:
                print(' # - > WRONG DIRECTION !!! -- URGENT - TO CLOSE POSITION // PROFIT =', vo)
            elif vo <= 0:
                print(' # - > WRONG DIRECTION !!! URGENT BUT CANNOT CLOSE POSITION // NOT_PROFIT =', vo)
        if vo > hardprofit:
            print('    - > TO CLOSE #', ko, '// ACHIEVED Target Hard_Profit ( >', hardprofit, ') =', vo)
            fxfinal.close_position_elementid(id_elem)
        elif buysell == 'BUY' and directionpoint > closebuypoint and vo > exitprofit:
            print('    - > TO CLOSE #', ko, '// CHANGE DIRECTION = BUY to SELL / Point =', directionpoint)
            fxfinal.close_position_elementid(id_elem)
        elif buysell == 'SELL' and directionpoint < closesellpoint and vo > exitprofit:
            print('    - > TO CLOSE #', ko, '// CHANGE DIRECTION = SELL to BUY / Point =', directionpoint)
            fxfinal.close_position_elementid(id_elem)
        # elif vo < closeloss:             -- ## DISABLE FOR TIME BEING
        #     print('    - > TO CLOSE (LOSS) = ', ko, ' / LOSS =', vo)
        #     fxfinal.close_position_elementid(id_elem)

    fxfinal.time_script_running_and_next(masastart, delaymins, timemins)