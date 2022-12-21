# MoneyForward　口座情報自動更新ソフト
## 概要
MoneyForwardの口座情報をプログラムで一括更新するためのソフト
通常版のMoneyForward（https://moneyforward.com/ ）以外に、住信SBIネット銀行用（https://ssnb.x.moneyforward.com/ ）にも対応

## 使い方

### 認証情報の設定
MoneyForwardにログインするためには、メールアドレス・パスワード・認証コードが必要であり、「.env」ファイルを作成し以下の情報を追加しなければならない。
※認証コードは通常版のMoneyForwardのみ

```markdown:.env
TWO_STEP_AUTHENTICATION_SETTING_CODE='XXXX XXXX XXXX XXXX'
MONEYFORWARD_MAIL_ADDRESS="sample@example.com"
MONEYFORWARD_PASSWORD="p@ssW0rd"
```

### 実行方法（通常版のMoneyForwardの場合）
```python
python update_normal_mf.py
```

### 実行方法（MoneyForward for 住信SBIネット銀行の場合）
```python
python update_normal_mf.py
```