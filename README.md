# fileSystemFlask

Flaskフレームワークを使用してWebアプリケーションを作成しています。このWebアプリケーションでは、ユーザーがコマンドを入力することで、さまざまな機能を利用できます。シェルをGUI的に実現することを目指したものである。

# 環境

Python 3.11.4

Package            Version
------------------ ---------
blinker            1.6.2
certifi            2023.7.22
charset-normalizer 3.2.0
click              8.1.6
colorama           0.4.6
fastjsonschema     2.17.1
Flask              2.3.2
idna               3.4
itsdangerous       2.1.2
Jinja2             3.1.2
MarkupSafe         2.1.3
mistune            2.0.5
nbclient           0.8.0
nbconvert          7.5.0
nbformat           5.9.0
pip                23.2.1
requests           2.31.0
setuptools         68.0.0
tinycss2           1.2.1
urllib3            2.0.4
Werkzeug           2.3.6
wheel              0.38.4

# コマンドの使い方

## restaurans [address]

このコマンドを使用すると、ユーザーが入力した住所の近くにあるレストラン情報を取得します。

## cct currency

現在利用可能な通貨の一覧を取得できる。

## cct convert [destinationLocale] [sourceDenomination] [sourceAmount]

指定した金額をある通貨から別の通貨への金額換算を行える。cct currencyで確認した通貨をもとに、変換してみることを想定している。

# 使用したAPI

## リクルート WEB サービス

https://webservice.recruit.co.jp/

## Geocoding API 

https://www.geocoding.jp/api/

## API Layer Exchange Rates Data API

https://apilayer.com/marketplace/exchangerates_data-api

