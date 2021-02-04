__author__ = 'cromox'

"""
@package base
WebDriver Factory class implementation
It creates a webdriver instance based on browser configurations
Example:
    wdf = WebDriverFactory(browser)
    wdf.getWebDriverInstance()
"""
# import traceback
from selenium import webdriver
# import os

class WebDriverFactory():

    def __init__(self, browser):
        """
        Inits WebDriverFactory class
        Returns:
            None
        """
        self.browser = browser
        #"""
        #Set chrome driver and iexplorer environment based on OS
        #
        #chromedriver = "C:/.../chromedriver.exe"
        #os.environ["webdriver.chrome.driver"] = chromedriver
        #self.driver = webdriver.Chrome(chromedriver)
        #
        #PREFERRED: Set the path on the machine where browser will be executed
        #"""

    def getWebDriverInstance(self, baseURL):
        """
        Get WebDriver Instance based on the browser configuration
        Returns:
            'WebDriver Instance'
        """
        driver_version = 'unknown'
        driver_name = 'unknown'
        if self.browser == "iexplorer" or self.browser == "ie" or self.browser == "IE":
            # Set IE driver
            iedriverserver = r'C:\tools\Python36\Scripts\IEDriverServer_x64_2.42.0.exe'
            # iedriverserver = r'C:\tools\Python36\Scripts\IEDriverServer_x64_3.12.0.exe' ## not working
            # iedriverserver = r'C:\tools\Python36\Scripts\IEDriverServer_x32_3.4.0.exe'  ## work but 32bit
            driver = webdriver.Ie(iedriverserver)
        elif self.browser == 'safari':   ### Safari not working on Windows - need Safari 10 on OSX El Capitan
            safaridriver = r'C:\tools\Python36\Scripts\SafariDriver.exe'
            driver = webdriver.Safari(safaridriver)
        elif self.browser == 'opera':
            # OperaDriver - win64 2.36 - https://github.com/operasoftware/operachromiumdriver/releases
            from os import listdir
            from selenium.webdriver.common import desired_capabilities as operacapabilities
            from selenium.webdriver.opera import options as operaoptions
            # OperaDriver - win64 2.36 - https://github.com/operasoftware/operachromiumdriver/releases
            _operaDriverLoc = r'C:\tools\operadriver\operadriver.exe'
            # Opera browser
            _operaInstDir = r'C:\tools\Opera\\'
            listOperaDir = listdir(_operaInstDir)
            listOperaVer = [char for char in listOperaDir if char[0].isdigit() and char[-1].isdigit()]
            # listOperaVer.sort(key=lambda version: [int(ver) for ver in version.split('.')])
            listOperaVer.sort()
            _operacurrentversion = listOperaVer[-1]
            _operaExeLoc = _operaInstDir + _operacurrentversion + r'\opera.exe'
            _operaCaps = operacapabilities.DesiredCapabilities.OPERA.copy()
            _operaOpts = operaoptions.ChromeOptions()
            _operaOpts._binary_location = _operaExeLoc
            # driver = webdriver.Chrome(executable_path = _operaDriverLoc, chrome_options = _operaOpts, desired_capabilities = _operaCaps)
            driver = webdriver.Opera(executable_path = _operaDriverLoc, options = _operaOpts, desired_capabilities = _operaCaps)
            driver_name = 'opera'
            driver_version = _operacurrentversion
        elif self.browser == "firefox" or self.browser == "ff":
            driver = webdriver.Firefox()
        elif self.browser == "headless" or self.browser == "nobrowser" or self.browser == "virtual":
            # This is for running without open Browser UI display - good for Jenkins
            chromedriverpath = r'C:\tools\chromedriver\chromedriver.exe'
            chrome_options = webdriver.ChromeOptions()
            # chrome_options.add_argument('--disable-extensions')
            chrome_options.add_argument("--incognito")
            # chrome_options.add_argument("--disable-plugins-discovery")
            # chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument('--headless')
            chrome_options.add_argument("--proxy-server='direct://'")
            chrome_options.add_argument("--proxy-bypass-list=*")
            driver = webdriver.Chrome(chromedriverpath, options=chrome_options)
        elif self.browser == 'brave':
            brave_exe = r'C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe'
            chromedriverpath = r'C:\tools\chromedriver\chromedriver.exe'
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--ignore-certificate-errors')
            chrome_options.add_argument("--disable-web-security")
            chrome_options.add_argument("--incognito")
            chrome_options.add_argument("--allow-running-insecure-content")
            chrome_options.add_argument("--allow-cross-origin-auth-prompt")
            chrome_options.add_argument("--disable-cookie-encryption")
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument("--test-type")
            chrome_options.binary_location = brave_exe
            ## webdriver section
            driver = webdriver.Chrome(chromedriverpath, options=chrome_options)
            driver_name = 'brave'
        else:
            # Set chrome driver
            # self.browser == "chrome":
            chromedriverpath = r'C:\tools\chromedriver\chromedriver.exe'
            #os.environ["webdriver.chrome.driver"] = chromedriverpath
            chrome_options = webdriver.ChromeOptions()
            # chrome_options.add_argument('--disable-extensions')
            # chrome_options.add_argument('--profile-directory=Default')
            # chrome_options.add_argument("--disable-plugins-discovery")
            # chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument('--ignore-certificate-errors')
            chrome_options.add_argument("--disable-web-security")
            chrome_options.add_argument("--incognito")
            chrome_options.add_argument("--allow-running-insecure-content")
            chrome_options.add_argument("--allow-cross-origin-auth-prompt")
            chrome_options.add_argument("--disable-cookie-encryption")
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument("--test-type")
            driver = webdriver.Chrome(chromedriverpath, options=chrome_options)
            #driver.set_window_size(1440, 900)

        # Setting Driver Implicit Time out for An Element
        driver.implicitly_wait(10)
        # Loading browser with App URL
        driver.get(baseURL)

        if driver_name == 'unknown':
            try:
                driver_name = driver.name
            except:
                driver_name = 'unknown'
        if driver_name == 'chrome':
            driver.maximize_window()  # Maximize the window for chrome

        if driver_version == 'unknown':
            try:
                driver_version = str(driver.capabilities['version']) # Python 3.7 and below
            except:
                driver_version = str(driver.capabilities['browserVersion']) # Python 3.8 & above

        print('Browser ( ' + str(driver_name) + ' ) version = ' + str(driver_version))
        return driver

    def getDriverTruePathFromOS(self, browser='chrome'):
        chromedriverexe = ''; chromedriverbin = ''
        from platform import system as osname
        if (osname() == 'Windows'):
            if (browser == 'chrome'):
                chromedriverexe = r'C:\tools\chromedriver\chromedriver.exe'
            elif (browser == 'brave'):
                chromedriverexe = r'C:\tools\chromedriver\chromedriver.exe'
                brave_exe = r'C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe'
                chromedriverbin = brave_exe
        elif (osname() == 'Linux'):
            if (browser == 'chrome'):
                chromedriverexe = '/opt/google/chromedriver/chromedriver'
            else:
                print('Browser other than Chrome not supported yet')
        else:
            print('OS ' + str(osname()) + ' is not support yet')
            # chromedriverexe = r'C:\tools\chromedriver\chromedriver.exe'

        return chromedriverexe, chromedriverbin