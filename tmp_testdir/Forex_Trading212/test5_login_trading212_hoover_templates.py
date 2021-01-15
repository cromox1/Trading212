__author__ = 'cromox'

from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
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

# ### now need to do drop-down / hoover
# template_dropdown = driver.find_element_by_xpath("//*[contains(text(),'Create Template')]")
# print('ELEMENT TEXT = ', template_dropdown.text)
# template_dropdown.click()
# hoover(driver).move_to_element(template_dropdown).perform()
# pro_template_element = driver.find_element_by_xpath("//*[contains(text(),'PRO')]")
# print('ELEMENT TEXT = ', pro_template_element.text)
# if pro_template_element:
#     pro_template_element.click()
## NOT SUCCESSFULL - LEAVE IT FOR THE TIME BEING

search_section = driver.find_element_by_id("navigation-search-button")
search_section.click()
# search_section.send_keys('GBP/USD' + Keys.ENTER)

driver.find_element_by_xpath("//*[contains(text(),'Currencies')]").click()
driver.find_element_by_xpath("//*[contains(text(),'Major')]").click()

# # # gbpusd_xpath = '//*[@data-code="GBPUSD"]/*[@fill-rule="evenodd"]'
# # gbpusd_xpath = '//*[@data-code="GBPUSD"]/div[@class="has-ellipsed-text"]'
# # driver.find_element_by_xpath(gbpusd_xpath + '/div[2]').click()
# driver.find_element_by_xpath('//*[@data-code="GBPUSD"]/div[2]').click()

valuetofind = '//*[@data-code="GBPUSD"]'
list_ids = driver.find_elements_by_xpath(valuetofind)
print('no of IDX = ', len(list_ids))
if len(list_ids) >= 1:
    print(list_ids[0].text)
    header = list_ids[0]

    # start from your target element, here for example, "header"
    # all_children_by_css = header.find_elements_by_css_selector("*")
    # all_children_by_xpath = header.find_elements_by_xpath(".//*")

    # all_children_by_xpath = header.find_elements_by_class_name('div')
    # print(len(all_children_by_xpath), ': ', str(len(all_children_by_xpath)))
    # # list_ids[0].click()
    all_children = header.find_elements_by_tag_name('div')
    # all_children = header.find_elements_by_xpath('./*/*[@class="ticker"]')
    # all_children = header.find_elements_by_xpath(".//*")
    # all_children = header.find_elements_by_css_selector("*")
    # all_children = header.find_elements_by_css_selector("div.has-ellipsed-text")
    # all_children = header.find_elements_by_xpath('.//*[@class="has-ellipsed-text"]')
    # all_children = header.find_elements_by_class("has-ellipsed-text")
    print('ALL = ', all_children)
    print('ALL COUNT = ', len(all_children))
    if len(all_children) > 1:
        i = 1
        for id in all_children:
            # if id.is_enabled() or id.is_displayed():
            # print(i, ' = ', id.text.replace('\n', ' ## '))
            print(i, ' = ', id.text.replace('\n', ' ## '), end=' ')
            try:
                id.click()
                break
            except:
                print(' / NOT CLICKABLE')
            i += 1
        all_children[-1].click()
            # if id.text == 'GBP/USD':
            #     id.click()
            #     break