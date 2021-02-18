from datetime import datetime
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
    list_tperiod = ['1 minute', '10 minutes']
    check_cfd_current = fxfinal.close_position_CFD_ANY_auto(value_EMA, list_tperiod)
    todopoint = check_cfd_current[0]
    open_position = check_cfd_current[1]
    tocloseone = check_cfd_current[2]
    instrument_id = check_cfd_current[-1]

    ### FOREX AUTO TRADER
    buymark = 14
    sellmark = -14
    closesellpoint = 4
    closebuypoint = -4
    closeloss = -0.75

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
    print('2) CLOSE_POSITION // WHEN POSITION CHANGE DIRECTION')
    print(' - > DIRECTN_POINT =', tocloseone)
    print(' - > OPEN_POSITION =', open_position)
    for ko,vo in open_position.items():
        id_elem = instrument_id[ko]
        buysell = fxfinal.direction_elementid(id_elem)
        directionpoint = tocloseone[ko]     # only work when all currencies in todopoint
        if buysell == 'BUY' and directionpoint < closebuypoint:
            print('   - > TO CLOSE #', ko, '// CHANGE DIRECTION = BUY to SELL / Point =', directionpoint)
            fxfinal.close_position_elementid(id_elem)
        elif buysell == 'SELL' and directionpoint > closesellpoint:
            print('   - > TO CLOSE #', ko, '// CHANGE DIRECTION = SELL to BUY / Point =', directionpoint)
            fxfinal.close_position_elementid(id_elem)
        elif vo < closeloss:
            print('   - > TO CLOSE (LOSS) = ', ko, ' / LOSS =', vo)
            fxfinal.close_position_elementid(id_elem)

    print()
    tidor = int(3.65*60)
    arini = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    nanti = int(datetime.now().timestamp()) + tidor
    futuretime = datetime.fromtimestamp(nanti).strftime('%Y-%m-%d %H:%M:%S')
    print('SCRIPT WILL RUN AGAIN AT :', futuretime, '( NOW =', arini, '/ in', tidor, 'secs )')
    sleep(tidor)