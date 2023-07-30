from flask import Flask, render_template, request, url_for, jsonify
import urllib.request
import urllib.parse
from xml.etree.ElementTree import ElementTree
import json
import os
import sys
import subprocess

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def main_page():
    if request.method == "POST":
        # user_input = request.form.get("shellInput").split()
        
        # # restaurant 住所
        # if user_input[0] == "restaurants":
        #     result = rastaurants(user_input[1:])
        # # cct 為替
        # # bashコマンド
        # return render_template('index.html') 
        user_input = request.form.get("shellInput").split()
        
        # restaurants 住所
        if user_input[0] == "restaurants":
            result = getRestaurants(user_input[1:])
            return jsonify(result=result)
        # cct 為替
        # bashコマンド
        return jsonify(error="Invalid command")
    return render_template('index.html')

def getRestaurants(address):
    if len(address) != 1:
        return "Usage: restaurants [address]<br>"

    ADRS = address[0].strip()

    # Recruit_API_KEY 環境変数においている
    KEYID = 'fb8fe7e452eedc87'
    # KEYID = os.getenv('Recruit_API_KEY')

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
    url2 = '{}&lat={}&lng={}&count={}'.format(URL2, lat, lng, 3)
    f = urllib.request.urlopen(url2)
    parsed = json.loads(f.read())['results']

    for (count, rest) in enumerate(parsed.get('shop')):
        res += "- {}<br>  {}<br>  <a href='{}'>{}</a><br><br>".format(rest['name'],
                                        rest['genre']['name'],
                                        rest['urls']['pc'], 
                                        rest['urls']['pc'])
    return res