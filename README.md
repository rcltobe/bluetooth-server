# Bluetoothスキャンアプリケーション

## 概要

SpreadSheetに登録されたユーザーに紐づけられたBluetooth端末をスキャンする。  
スキャン結果はSpreadSheetの`attendance`という名前のシートに保存される。

## 必要ファイル

|ファイルの説明|ファイル名|ファイルパス|
|---|---|---|
|サービスアカウントの秘密鍵|credentials.json|<プロジェクトルート>/credentials.json|

## ライブラリのインストール

```sh
# パッケージマネージャの更新
sudo apt update

# Bluetoothスキャンに必要なライブラリのインストール
sudo apt install -y libbluetooth3-dev libglib2.0 libboost-python-dev libboost-thread-dev

# Pythonライブラリのインストール
pip3 install -r requirements.txt
```

## 環境変数

|環境変数名| 説明                                                                                       |
|---|------------------------------------------------------------------------------------------|
|CREDENTIAL_FILE_PATH| サービスアカウントのパス                                                                             |
|SPREADSHEET_KEY| SpreadSheetのキー（URLのXXXとなっている部分 https://docs.google.com/spreadsheets/d/XXXXXX/edit#gid=0) |
|DISCORD_ATTENDANCE_LOG_WEBHOOK| Discordのattending_logのWebhookURL                                                         |

## テスト実行方法
```
python -m unittest discover test
```