import os
from time import sleep, time

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import xpathlist as xpath
from mail import do_alert_mail

RUN_HEADLESS = False
LOGIN_REFRESH_IN_MINUTES = 55
PAGE_REFRESH_IN_SECONDS = 50

# It is recommended that you use a .env file and let dotenv do the work.
USERNAME = ""
PASSWORD = ""

start_time = 0
last_result = None


def init_driver():
    options = webdriver.ChromeOptions()
    if RUN_HEADLESS:
        options.add_argument('--headless')

    driver = webdriver.Chrome(options)

    return driver


def sign_in(driver: webdriver.Chrome, username, password):
    driver.get("https://infopriem.mon.bg/login")
    driver.find_element(By.XPATH, xpath.USERNAME_INPUT).send_keys(username)
    driver.find_element(By.XPATH, xpath.PASSWORD_INPUT).send_keys(password)

    sleep(1)
    sign_in_btn = driver.find_element(By.XPATH, xpath.SIGN_IN_BTN)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    sign_in_btn.click()
    WebDriverWait(driver, 20).until(EC.invisibility_of_element_located(sign_in_btn))


def log_out(driver: webdriver.Chrome):
    driver.get("https://infopriem.mon.bg/logout")


def navigate_to_exams(driver: webdriver.Chrome):
    driver.get("https://infopriem.mon.bg/student/marks")
    table = driver.find_element(By.XPATH, xpath.EXAMS_TABLE)

    tr_elements = table.find_elements(By.CSS_SELECTOR, "tbody > tr")

    exams = {}
    counter = 0

    for element in tr_elements:
        td_elements = element.find_elements(By.TAG_NAME, "td")
        exams[td_elements[0].get_attribute("innerHTML")] = td_elements[2].get_attribute("innerHTML")
        counter += 1

    return exams, table


def do_check(driver: webdriver.Chrome, username, password):
    global start_time
    global last_result

    if time() >= start_time + (LOGIN_REFRESH_IN_MINUTES * 60):
        log_out(driver)
        sign_in(driver, username, password)
        start_time = time()

    result, table = navigate_to_exams(driver)
    print(result)
    if last_result is None:
        last_result = result
    elif result != last_result:
        execute_alert(driver, result, table)
        last_result = result


def scheduler(driver: webdriver.Chrome, username, password):
    while True:
        do_check(driver, username, password)
        sleep(PAGE_REFRESH_IN_SECONDS)


def execute_alert(driver: webdriver.Chrome, new_result, table_el):
    global last_result
    print("Alert fired!")

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    binary_screenshot = table_el.screenshot_as_png
    do_alert_mail(new_result, last_result, binary_screenshot)


def import_from_env():
    global USERNAME, PASSWORD

    load_dotenv()

    USERNAME = os.getenv("USERNAME")
    PASSWORD = os.getenv("PASSWORD_USER")


import_from_env()
driver_el = init_driver()
scheduler(driver_el, USERNAME, PASSWORD)
