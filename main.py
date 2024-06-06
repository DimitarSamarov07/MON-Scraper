from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import xpathlist as xpath

runHeadless = False;


def init_driver():
    options = webdriver.ChromeOptions()
    if runHeadless:
        options.add_argument('--headless')

    driver = webdriver.Chrome(options)

    return driver


def sign_in(driver: webdriver.Chrome, username, password):
    driver.get("https://infopriem.mon.bg/login")
    driver.find_element(By.XPATH, xpath.USERNAME_INPUT).send_keys(username)
    driver.find_element(By.XPATH, xpath.PASSWORD_INPUT).send_keys(password)

    sign_in_btn = driver.find_element(By.XPATH, xpath.SIGN_IN_BTN)

    ActionChains(driver).move_to_element(sign_in_btn).perform()

    driver.implicitly_wait(200)


def navigate_to_exams(driver: webdriver.Chrome):
    driver.get("https://infopriem.mon.bg/student/exams")
    table = driver.find_element(By.XPATH, xpath.EXAMS_TABLE)

    tr_elements = table.find_elements(By.CSS_SELECTOR, "tbody > tr")

    for element in tr_elements:
        td_elements = element.find_elements(By.TAG_NAME, "td")
        for td_el in td_elements:
            print(td_el)

    driver.quit()


driver_el = init_driver()
sign_in(driver_el, "test", "test")
navigate_to_exams(driver_el)

