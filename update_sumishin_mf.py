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
from selenium.webdriver.chrome.service import Service

# MoneyForwardの二段階認証を突破するためのもの
load_dotenv()
MONEYFORWARD_MAIL_ADDRESS = os.environ["MONEYFORWARD_MAIL_ADDRESS"]
MONEYFORWARD_PASSWORD = os.environ["MONEYFORWARD_PASSWORD"]


def web_driver_setting() -> WebDriver:
    """ウェブドライバの初期設定

    Returns:
        WebDriver:
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")        
    options.add_argument(f'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36')
    driver = webdriver.Chrome(options=options)
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
    mail_address = driver.find_element(by=By.CSS_SELECTOR, value="#sign_in_session_service_email")
    mail_address.send_keys(MONEYFORWARD_MAIL_ADDRESS)

    password = driver.find_element(by=By.CSS_SELECTOR, value="#sign_in_session_service_password")
    password.send_keys(MONEYFORWARD_PASSWORD)
    login_button = driver.find_element(by=By.CSS_SELECTOR, value="#login-btn-sumit")
    login_button.click()

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
        driver.implicitly_wait(3)


def main():
    web_driver_setting()
    login_moneyforward_url = "https://ssnb.x.moneyforward.com/users/sign_in"
    moneyforward_browser = login_moneyforward(mf_url=login_moneyforward_url)

    update_account(moneyforward_browser)
    print("Complete!!")


if __name__ == "__main__":
    main()
