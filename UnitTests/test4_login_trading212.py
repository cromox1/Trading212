__author__ = 'cromox'

from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

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
# 1)
# main_window_handle = driver.current_window_handle
# # driver.find_element_by_xpath(u'//a[text()="Identity verification"]').click()
# signin_window_handle = None
# while not signin_window_handle:
#     for handle in driver.window_handles:
#         if handle != main_window_handle:
#             signin_window_handle = handle
#             print('got it yeah!!')
#             break
#
# driver.switch_to.window(signin_window_handle)
#
# 2)
# iframe = driver.find_elements_by_css_selector("iframe")
# print("IFRAME = " + str(iframe))
# # driver.switch_to.frame(iframe)
# driver.switch_to.frame(iframe[-1])
#
## but now I just use simple solution - find the xpath :-)
xpath1 = '//*[@id="onfido-upload"]/div[1]/div[2]'
driver.find_element_by_xpath(xpath1).click()

template_bar = '//*[@id="chartTabTemplates"]/div'
driver.find_element_by_id("chartTabTemplates").click()
driver.find_element_by_partial_link_text("PRO").click()
# driver.find_element_by_xpath(u'//a[text()="PRO"]').click()

### now need to do drop-down

valuetofind = '//*[@id]'
attribute = 'id'

list_ids = driver.find_elements_by_xpath(valuetofind)

i = 1
for idx in list_ids:
    print(str(i) + ') ' + str(idx._id) + ' / ' + attribute + ' = ' + str(idx.get_attribute(attribute)))
    i += 1


