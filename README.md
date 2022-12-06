# MoneyForward　口座情報自動更新ソフト
## 概要
MoneyForwardの口座情報をプログラムで一括更新するためのソフト

## 注意点
MoneyForwardにログインするためには、２段階認証を突破しなければならない
そのため、２段階認証設定時の認証コードをメモし、「.env」ファイルに書く必要がある。

```markdown:.env
TWO_STEP_AUTHENTICATION_SETTING_CODE='XXXX XXXX XXXX XXXX'
```