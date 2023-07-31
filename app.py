from flask import Flask, render_template, request, jsonify
import urllib.request
import urllib.parse
from xml.etree.ElementTree import ElementTree
import json
import requests
import os
from dotenv import load_dotenv

# .envファイルのパスを指定して読み込み
load_dotenv('.env')

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def main_page():
    if request.method == "POST":
        input_command = request.form.get("shellInput")
        user_input = input_command.split()
        # restaurants 住所
        if user_input[0] == "restaurants":
            result = getRestaurants(user_input[1:])
            return jsonify(input=input_command, result=result)
        
        # cct 為替
        if user_input[0] == "cct":
            # cct 1 の場合
            if user_input[1] == "currency":
                result = get_available_currencies()
                return jsonify(input=input_command, result=result)
            # cct 2 の場合
            elif len(user_input) == 5 and user_input[1] == "convert":
                result = convert(user_input[2], user_input[3], user_input[4])
                return jsonify(input=input_command, result=result)
            # cct を使おうとしたが、入力ミスがあった場合
            else:
                return jsonify(input=input_command, error="Usage: cct currency or cct convert [destinationLocale] [sourceDenomination] [sourceAmount]")
            
        # bashコマンド
        return jsonify(input=input_command, error="Invalid command")
    return render_template('index.html')

# restaurants 
# 住所の入力から、近くレストランをmax_number件以下取得できる
#
# 書式:
#   restaurants [address]
def getRestaurants(address):
    # 表示するレストランの最大件数
    max_number = 3

    if len(address) != 1:
        return "Usage: restaurants [address]<br>"

    ADRS = address[0].strip()

    KEYID = os.getenv('hotpapper_API')

    URL1 = "https://www.geocoding.jp/api/?q={}".format(urllib.parse.quote(ADRS))
    URL2 = "http://webservice.recruit.co.jp/hotpepper/gourmet/v1/?key={}&format=json".format(KEYID)

    # 住所から緯度経度の取得（Geocoding API）
    f = urllib.request.urlopen(URL1)
    et = ElementTree()
    et.parse(f)
    lat_element = et.find("./coordinate/lat")
    lng_element = et.find("./coordinate/lng")

    if lat_element is None or lng_element is None:
        return "Error: The address entered is incorrect.<br>"

    lat = lat_element.text
    lng = lng_element.text

    res = "{}({:.3f}, {:.3f})の近くのレストランは<br>".format(ADRS, float(lat), float(lng))

    # 緯度経度からレストラン情報取得（Hotpepper API）
    url2 = '{}&lat={}&lng={}&count={}'.format(URL2, lat, lng, max_number)
    f = urllib.request.urlopen(url2)
    parsed = json.loads(f.read())['results']

    for (count, rest) in enumerate(parsed.get('shop')):
        res += "- {}<br>  {}<br>  <a href='{}'>{}</a><br>".format(rest['name'],
                                        rest['genre']['name'],
                                        rest['urls']['pc'], 
                                        rest['urls']['pc'])
    return res

# cct 1 
# 現在利用可能な通貨の一覧を取得する
#
# 書式:
#   cct currency   
def get_available_currencies():
    URL3 = "https://api.apilayer.com/exchangerates_data/symbols"

    payload = {}
    headers= {
        "apikey": os.getenv('APILayer_API')
    }

    try:
        response = requests.request("GET", URL3, headers=headers, data=payload)
        response.raise_for_status()  # レスポンスが正常でない場合、例外を発生させる
        parsed = json.loads(response.text)['symbols']
        res = ""

        for key, value in parsed.items():
            res += key + ": " + value + "<br>"
        return res
    except requests.exceptions.RequestException as e:
        return "エラーが発生しました。詳細: " + str(e)
    except json.JSONDecodeError as e:
        return "APIからのデータを解析できませんでした。詳細: " + str(e)

# cct 2 
# 指定金額をある通貨から別の通貨への金額換算をする
#
# 書式:
#   cct convert [destinationLocale] [sourceDenomination] [sourceAmount]
def convert(destination, source, amount):
    URL4 = "https://api.apilayer.com/exchangerates_data/convert?to={}&from={}&amount={}".format(destination, source, amount)

    payload = {}
    headers= {
        "apikey": os.getenv('APILayer_API')
    }

    response = requests.request("GET", URL4, headers=headers, data = payload)

    
    # APIから取得した結果を解析して、変換結果を取得
    try:
        # APIからのレスポンスをJSON形式として解析
        parsed_response = response.json()

        # 変換結果を取得
        result = parsed_response.get('result')
        if result is not None:
            return "変換結果: {} は {} {} です。<br>".format(source, result, destination)
        else:
            return "<span style='color: red'>Error</span>: 通貨の変換に失敗しました。変換結果が取得できませんでした。<br>"
    
    except json.JSONDecodeError:
        return "<span style='color: red'>Error</span>: 通貨の変換に失敗しました。APIからのデータを解析できませんでした。<br>"
