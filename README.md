# MoneyForward　口座情報自動更新ソフト
## 概要
MoneyForwardの口座情報をプログラムで一括更新するためのソフト

## 注意点
MoneyForwardにログインするためには、メールアドレス・パスワード・認証コードが必要であり、「.env」ファイルに書く必要がある。

```markdown:.env
TWO_STEP_AUTHENTICATION_SETTING_CODE='XXXX XXXX XXXX XXXX'
MONEYFORWARD_MAIL_ADDRESS="sample@example.com"
MONEYFORWARD_PASSWORD="p@ssW0rd"
```