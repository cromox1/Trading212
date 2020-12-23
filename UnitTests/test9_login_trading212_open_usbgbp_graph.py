__author__ = 'cromox'

from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
# from selenium.webdriver.common.action_chains import ActionChains as hoover

chromedriverpath = r'C:\tools\chromedriver\chromedriver.exe'
chrome_options = Options()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument("--disable-web-security")
# chrome_options.add_argument("--incognito")
chrome_options.add_argument("--allow-running-insecure-content")
chrome_options.add_argument("--allow-cross-origin-auth-prompt")
chrome_options.add_argument("--disable-cookie-encryption")
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-default-apps')
chrome_options.add_argument('--disable-prompt-on-repost')
chrome_options.add_argument("--disable-zero-browsers-open-for-tests")
chrome_options.add_argument("--no-default-browser-check")
chrome_options.add_argument("--test-type")
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs", prefs)

## webdriver section
driver = webdriver.Chrome(chromedriverpath, options=chrome_options)
driver.implicitly_wait(10)

base_url = "https://www.trading212.com"

driver.maximize_window()
driver.get(base_url)

driver.find_element_by_id("cookie-bar").click()
driver.find_element_by_id("login-header-desktop").click()

user1 = "mycromox@gmail.com"
pswd1 = "Serverg0d!"

driver.find_element_by_id("username-real").send_keys(user1 + Keys.ENTER)
driver.find_element_by_id("pass-real").send_keys(pswd1 + Keys.ENTER)
sleep(10)

# ### Need to find a way to go to pop-up window
# but for now I just use simple solution - find the xpath :-)
xpath1 = '//*[@id="onfido-upload"]/div[1]/div[2]'
driver.find_element_by_xpath(xpath1).click()

template_bar = '//*[@id="chartTabTemplates"]/div'
driver.find_element_by_id("chartTabTemplates").click()

search_section = driver.find_element_by_id("navigation-search-button")
search_section.click()
# search_section.send_keys('GBP/USD' + Keys.ENTER)

driver.find_element_by_xpath("//*[contains(text(),'Currencies')]").click()
driver.find_element_by_xpath("//*[contains(text(),'Major')]").click()
sleep(2)

# xpath_gbpusd = '//*[@id="uniqName_0_344"]'
# //*[@id="uniqName_0_341"]/div[2]/div[1]
# xpath_gbpusd = '//*[@data-code="GBPUSD"]'
# element1 = driver.find_element_by_xpath(xpath_gbpusd)

css_gbpusd = "#uniqName_0_344 > .ticker > .has-ellipsed-text"
element1 = driver.find_element_by_css_selector(css_gbpusd)
# print('ELE1 = ', element1, ' / TXT = ', element1.text.replace('\n', ' ## '))
element1.click()
# driver.execute_script("arguments[0].click();", element1)
sleep(2)

##  #uniqName_0_372-main-view > div.tradebox-trade-container > div.tradebox-button.tradebox-sell > div.tradebox-price.tradebox-price-sell
##  //*[@id="uniqName_0_372-main-view"]/div[1]/div[1]/div[2]
##  document.querySelector("#uniqName_0_372-main-view > div.tradebox-trade-container > div.tradebox-button.tradebox-sell > div.tradebox-price.tradebox-price-sell")
##  <div class="tradebox-price tradebox-price-sell" data-dojo-attach-point="sellPriceNode">1.33<span>82</span><label>6</label></div>
##  //*[@id="current-status-high-low-view"]/div[1]/span[1]

xp_sell = '//*[@id="uniqName_0_372-main-view"]//*[@data-dojo-attach-point="sellPriceNode"]'
xp_buy = '//*[@id="uniqName_0_372-main-view"]//*[@data-dojo-attach-point="buyPriceNode"]'

print('SELL = ', driver.find_element_by_xpath(xp_sell).text)
print('BUY = ', driver.find_element_by_xpath(xp_buy).text)

xp_low = '//*[@id="current-status-high-low-view"]//*[@data-dojo-attach-point="lowPriceNode"]'
xp_high = '//*[@id="current-status-high-low-view"]//*[@data-dojo-attach-point="highPriceNode"]'

print('LOW = ', driver.find_element_by_xpath(xp_low).text)
print('HIGH = ', driver.find_element_by_xpath(xp_high).text)