import os
from time import sleep
from dotenv import load_dotenv
import subprocess
import re
import random

from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

# MoneyForwardの二段階認証を突破するためのもの
load_dotenv()
TWO_STEP_AUTHENTICATION_SETTING_CODE = os.environ["TWO_STEP_AUTHENTICATION_SETTING_CODE"]
MONEYFORWARD_MAIL_ADDRESS = os.environ["MONEYFORWARD_MAIL_ADDRESS"]
MONEYFORWARD_PASSWORD = os.environ["MONEYFORWARD_PASSWORD"]


def web_driver_setting() -> WebDriver:
    """ウェブドライバの初期設定

    Returns:
        WebDriver:
    """
    driver = webdriver.Chrome()
    driver.implicitly_wait(2)
    return driver


def login_moneyforward(mf_url: str) -> WebDriver:
    """マネーフォワードにログイン

    Args:
        mf_url (str): マネーフォワードのURL

    Returns:
        WebDriver:
    """
    driver = web_driver_setting()
    driver.get(mf_url)
    print("Login moneyforward")
    # ログイン
    driver.find_element(by=By.XPATH, value='//*[@id="login"]/div/div/div[3]/a').click()
    driver.find_element(
        by=By.XPATH, value="/html/body/main/div/div/div/div/div[1]/section/div/div/div[2]/div/a[1]"
    ).click()

    mail_address = driver.find_element(
        by=By.XPATH, value="/html/body/main/div/div/div/div/div[1]/section/form/div[2]/div/input"
    )
    mail_address.send_keys(MONEYFORWARD_MAIL_ADDRESS)
    next_button = driver.find_element(
        by=By.XPATH, value="/html/body/main/div/div/div/div/div[1]/section/form/div[2]/div/div[4]/input"
    )
    next_button.click()
    sleep(1)

    password = driver.find_element(
        by=By.XPATH, value="/html/body/main/div/div/div/div/div[1]/section/form/div[2]/div/input[2]"
    )
    password.send_keys(MONEYFORWARD_PASSWORD)
    login_button = driver.find_element(
        by=By.XPATH, value="/html/body/main/div/div/div/div/div[1]/section/form/div[2]/div/div[3]/input"
    )
    login_button.click()

    two_step_authentication = ["oathtool", "--totp", "--base32", TWO_STEP_AUTHENTICATION_SETTING_CODE]
    auth_code = re.findall(r"\d+", subprocess.check_output(two_step_authentication).decode("utf-8"))

    # Enter auth code
    elem_auth_number = driver.find_element(
        by=By.XPATH, value="/html/body/main/div/div/div/section/div[1]/section/form/div[2]/div/div[1]/input"
    )
    elem_auth_number.send_keys(auth_code[0])

    # Jump to already-logged-in servise list page by Money Foward ID
    elem_auth = driver.find_element(
        by=By.XPATH, value="/html/body/main/div/div/div/section/div[1]/section/form/div[2]/div/div[2]/input"
    )
    elem_auth.click()

    sleep(3)

    return driver


def update_account(driver: WebDriver) -> None:
    """口座情報を更新する

    Args:
        driver (WebDriver): マネーフォワードトップページが表示されている状態
    """
    # 口座タブへ移動
    account_button = driver.find_element(By.CLASS_NAME, "mf-icon-account")
    account_button.click()
    sleep(1)

    # 更新ボタンをクリック
    update_buttons = driver.find_elements(By.CSS_SELECTOR, "input[value='更新']")
    for update_button in update_buttons:
        update_button.click()
        # 更新ボタンを押す間隔をランダムにして、ロボットっぽくさせないようにしている
        wait_time = random.uniform(1.0, 3.0)
        sleep(wait_time)


def main():
    web_driver_setting()
    login_moneyforward_url = "https://moneyforward.com/login"
    moneyforward_browser = login_moneyforward(mf_url=login_moneyforward_url)

    update_account(moneyforward_browser)
    print("Complete!!")


if __name__ == "__main__":
    main()
