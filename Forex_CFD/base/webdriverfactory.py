__author__ = 'cromox'

"""
@package base
WebDriver Factory class implementation
It creates a webdriver instance based on browser configurations
Example:
    wdf = WebDriverFactory(browser)
    wdf.getWebDriverInstance()
"""
from selenium import webdriver

class WebDriverFactory():

    def __init__(self, browser, browser_exe=None, driver_path=None, browser_inst_dir=None):
        #"""
        #Set chrome driver based on OS
        #chromedriver = "C:/.../chromedriver.exe"
        #os.environ["webdriver.chrome.driver"] = chromedriver
        #self.driver = webdriver.Chrome(chromedriver)
        #PREFERRED: Set the path on the machine where browser will be executed
        #"""
        self.browser = browser
        self.browser_exe = browser_exe
        self.driver_path = driver_path
        self.browser_inst_dir = browser_inst_dir

    def browserDriverExe(self, name):
        driver_version = 'unknown'
        driver_name = 'unknown'
        if name == 'safari':   ### Safari not working on Windows - need Safari 10 on OSX El Capitan
            safaridriver = self.driver_path
            driver = webdriver.Safari(safaridriver)
        elif name == "iexplorer" or name == "ie" or name == "IE":
            iedriverserver = self.driver_path
            driver = webdriver.Ie(iedriverserver)
        elif name == "firefox" or name == "ff":
            driver = webdriver.Firefox()
        elif name == 'brave':
            brave_exe = self.browser_exe
            chromedriverpath = self.driver_path
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
        elif name == 'opera':
            from os import listdir
            from selenium.webdriver.common import desired_capabilities as operacapabilities
            from selenium.webdriver.opera import options as operaoptions
            _operaDriverLoc = self.driver_path
            # Opera browser
            _operaInstDir = self.browser_inst_dir
            listOperaDir = listdir(_operaInstDir)
            listOperaVer = [char for char in listOperaDir if char[0].isdigit() and char[-1].isdigit()]
            # listOperaVer.sort(key=lambda version: [int(ver) for ver in version.split('.')])
            listOperaVer.sort()
            _operacurrentversion = listOperaVer[-1]
            _operaExeLoc = _operaInstDir + _operacurrentversion + r'\opera.exe'
            _operaCaps = operacapabilities.DesiredCapabilities.OPERA.copy()
            _operaOpts = operaoptions.ChromeOptions()
            _operaOpts._binary_location = _operaExeLoc
            driver = webdriver.Opera(executable_path = _operaDriverLoc, options = _operaOpts, desired_capabilities = _operaCaps)
            driver_name = 'opera'
            driver_version = _operacurrentversion

        elif name == "headless" or name == "nobrowser" or name == "virtual":
            # This is for running without open Browser UI display - good for Jenkins
            chromedriverpath = self.driver_path
            chrome_options = webdriver.ChromeOptions()
            # chrome_options.add_argument('--disable-extensions')
            chrome_options.add_argument("--incognito")
            # chrome_options.add_argument("--disable-plugins-discovery")
            # chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument('--headless')
            chrome_options.add_argument("--proxy-server='direct://'")
            chrome_options.add_argument("--proxy-bypass-list=*")
            driver = webdriver.Chrome(chromedriverpath, options=chrome_options)
        else:
            # Set chrome driver
            # name == "chrome":
            chromedriverpath = self.driver_path
            #os.environ["webdriver.chrome.driver"] = chromedriverpath
            chrome_options = webdriver.ChromeOptions()
            #### headless - but not working at the moment
            # chrome_options.add_argument('--headless')
            # chrome_options.add_argument('--disable-gpu')
            # chrome_options.headless = True
            chrome_options.add_argument('--ignore-certificate-errors')
            chrome_options.add_argument("--disable-web-security")
            chrome_options.add_argument("--incognito")
            chrome_options.add_argument("--allow-running-insecure-content")
            chrome_options.add_argument("--allow-cross-origin-auth-prompt")
            chrome_options.add_argument("--disable-cookie-encryption")
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument("--test-type")
            chrome_options.add_argument('--disable-default-apps')
            chrome_options.add_argument('--disable-prompt-on-repost')
            chrome_options.add_argument("--disable-zero-browsers-open-for-tests")
            chrome_options.add_argument("--no-default-browser-check")
            prefs = {"profile.default_content_setting_values.notifications": 2}
            chrome_options.add_experimental_option("prefs", prefs)
            ## webdriver section
            driver = webdriver.Chrome(chromedriverpath, options=chrome_options)

        return driver, driver_name, driver_version

    def getWebDriverInstance(self, baseURL):
        """
        Get WebDriver Instance based on the browser configuration
        Returns:
            'WebDriver Instance'
        """
        browserdriver = self.browserDriverExe(self.browser)
        driver = browserdriver[0]
        driver_name = browserdriver[1]
        driver_version = browserdriver[-1]

        # Setting Driver Implicit Time out for An Element
        driver.implicitly_wait(10)
        # Loading browser with App URL
        driver.get(baseURL)
        if driver_name == 'unknown':
            try:
                driver_name = driver.name
            except:
                driver_name = 'unknown'

        driver.maximize_window()

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