from time import sleep

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

import xpathlist as xpath

runHeadless = True;


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

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

    sign_in_btn.click()

    return sign_in_btn


def navigate_to_exams(driver: webdriver.Chrome, element_disappeared):
    WebDriverWait(driver, 20).until(EC.invisibility_of_element_located(element_disappeared))
    driver.get("https://infopriem.mon.bg/student/marks")
    table = driver.find_element(By.XPATH, xpath.EXAMS_TABLE)

    tr_elements = table.find_elements(By.CSS_SELECTOR, "tbody > tr")

    exams = {}
    counter = 0

    for element in tr_elements:
        td_elements = element.find_elements(By.TAG_NAME, "td")
        exams[td_elements[0].get_attribute("innerHTML")] = td_elements[2].get_attribute("innerHTML")
        counter += 1

    print(exams)
    driver.quit()


driver_el = init_driver()
disappear = sign_in(driver_el, "test", "test")
navigate_to_exams(driver_el, disappear)