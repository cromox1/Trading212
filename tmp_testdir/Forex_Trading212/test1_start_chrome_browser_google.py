__author__ = 'cromox'

from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.keys import Keys

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

## webdriver section
driver = webdriver.Chrome(chromedriverpath, options=chrome_options)
driver.implicitly_wait(10)
base_url = "https://www.google.co.uk"

driver.maximize_window()
driver.get(base_url)
# iframe = driver.find_element_by_xpath("//iframe[contains(@id,'introAgreeButton')]")
# iframe = driver.find_element_by_xpath("//iframe[contains(text(),'I agree')]")
# iframe = driver.find_elements_by_link_text("https://consent.google.co.uk/")
# iframe = driver.find_elements_by_xpath("//iframe[contains(text(),'I agree')]")
# iframe = driver.find_elements_by_partial_link_text("consent.google.com")
# iframe = driver.find_element_by_id("cnsw")
# iframe = driver.find_elements_by_name("canonical")
# iframe = driver.find_elements_by_xpath("//*/form/*/span/span")
iframe = driver.find_elements_by_css_selector("iframe")
print("IFRAME = " + str(iframe))
# driver.switch_to.frame(iframe)
driver.switch_to.frame(iframe[-1])
idx="//*[contains(text(),'I agree')]"
sleep(2)
# idall = driver.find_elements_by_xpath(idx)
idall = driver.find_elements_by_id("introAgreeButton")
print("ID ALL = " + str(idall))
# driver.find_element_by_xpath(idx).click()
# driver.switch_to.default_content()

# idx='//*[@id="introAgreeButton/span/span"]'
# idx='//*[@id="introAgreeButton"]/div[2]'
# idx="//*[contains(text(),'I agree')]"
# driver.find_element_by_xpath(idx).click()
# driver.find_element_by_id("introAgreeButton").click()

# driver.find_element_by_name('q').click()
# driver.find_element_by_name('q').send_keys("pixitmedia" + Keys.ENTER)