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
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs", prefs)

## webdriver section
driver = webdriver.Chrome(chromedriverpath, options=chrome_options)
driver.implicitly_wait(10)

# base_url = "https://www.fxstreet.com/rates-charts"
base_url = "https://www.fxstreet.com/rates-charts/gbpusd"

driver.maximize_window()
driver.get(base_url)

# confirmxpath = '/html/body'
# ## accept Cookie notofication
# if driver.find_element_by_xpath(confirmxpath):
#     driver.find_element_by_xpath(confirmxpath).click()
#
sleep(5)

id_gbpusd = '//*[@id="fxs_data_table_ratestable_60a4f99f-a2ac-459f-a58f-4e5978c5d289"]/tbody/tr[2]'
## //*[@id="fxs_ratedata_6ad64de6-8be8-50a6-da6c-88365665e2e9"]/div/div[2]/small

text1 = driver.find_element_by_id(id_gbpusd).text
print(text1)
