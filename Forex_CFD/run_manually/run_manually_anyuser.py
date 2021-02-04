from Forex_CFD.utilities.util import Util


class RunManually():

    def __init__(self, driver):
        super(RunManually, self).__init__(driver)
        self.driver = driver
        self.util = Util()



    ##### STEPS BY STEPS running  #########

    # 1) start webdriver
    chromebrowserdriver = google_chrome_browser()

    # 2) login
    base_url = "https://www.trading212.com"
    # user1 = "roslitalib2017@gmail.com"
    # pswd1 = "Malaysia123"
    user1 = "mycromox@gmail.com"
    pswd1 = "Serverg0d!"
    # user1 = "xixa01@yahoo.co.uk"
    # pswd1 = "H0meBase"
    driver = autologin_maxwindows(chromebrowserdriver, base_url, user1, pswd1)

    # 3) pop-up window (which ask to upload ID documents)
    driver = close_popup_ask_upload_docs(driver)

    # 4) switch to Practice Mode   # Real or Practice
    driver = mode_live_or_demo(driver, "Practice")

    # 5) go to speficic currency or looping all currencies   # looping_check_all_currencies(driver)
    # 6) Buy/Sell/Close_Position

    ## NOW COMBINE NO 5) & 6)

    pilihan = 0
    rerun = 'Y'
    value_EMA = 25
    tperiod = '1 minute'  # tperiod = '1 minute' / '5 minutes' / '10 minutes' / '15 minutes'

    while pilihan != 99:
        penutup = close_position_CFD_ANY(driver, value_EMA, tperiod, rerun)
        pilihan = penutup[0]
        rerun = penutup[-1]