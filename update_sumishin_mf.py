import os
from dotenv import load_dotenv

from playwright.sync_api import sync_playwright, Page

load_dotenv()
MONEYFORWARD_MAIL_ADDRESS = os.environ["MONEYFORWARD_MAIL_ADDRESS"]
MONEYFORWARD_PASSWORD = os.environ["MONEYFORWARD_PASSWORD"]


def login_moneyforward(page: Page, mf_url: str) -> None:
    """マネーフォワードにログイン

    Args:
        page (Page): Playwright の Page オブジェクト
        mf_url (str): マネーフォワードのURL
    """
    page.goto(mf_url)
    print("Login moneyforward")

    page.fill("#sign_in_session_service_email", MONEYFORWARD_MAIL_ADDRESS)
    page.fill("#sign_in_session_service_password", MONEYFORWARD_PASSWORD)
    page.click("#login-btn-sumit")

    page.wait_for_load_state("networkidle")


def update_account(page: Page) -> None:
    """口座情報を更新する

    Args:
        page (Page): マネーフォワードトップページが表示されている状態
    """
    # 口座タブへ移動
    page.click(".mf-icon-account")
    page.wait_for_load_state("domcontentloaded")

    # 各フォームの情報を収集し、fetch() で更新リクエストを送信する
    # （ボタンクリックだとフォーム送信でページ遷移が発生し、
    #   事前に収集した action URL が無効になるため fetch を使用）
    results: list[str] = page.evaluate("""
        async () => {
            const buttons = Array.from(
                document.querySelectorAll("input[value='更新']:not([disabled])")
            );
            const results = [];
            for (const btn of buttons) {
                const form = btn.closest('form');
                try {
                    await fetch(form.action, {
                        method: form.method || 'POST',
                        body: new FormData(form),
                    });
                    results.push(form.action.split('/').pop().slice(0, 8));
                } catch (e) {
                    results.push('error: ' + e.message);
                }
            }
            return results;
        }
    """)
    print(f"更新対象: {len(results)} 件")
    for r in results:
        print(f"更新リクエスト送信: {r}...")


def main():
    login_moneyforward_url = "https://ssnb.x.moneyforward.com/users/sign_in"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        try:
            login_moneyforward(page, mf_url=login_moneyforward_url)
            update_account(page)
            print("Complete!!")
        finally:
            browser.close()


if __name__ == "__main__":
    main()
