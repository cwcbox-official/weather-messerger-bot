
import os
import json
import requests
from flask import Flask, request

app = Flask(__name__)

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")
CWB_API_KEY = os.getenv("CWB_API_KEY")
CWB_API_URL = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-D0047-091"

def get_weather(location_name):
    try:
        params = {
            "Authorization": CWB_API_KEY,
            "format": "JSON",
            "locationName": location_name
        }
        res = requests.get(CWB_API_URL, params=params)
        data = res.json()
        locations = data["records"]["locations"][0]["location"]
        location = next((loc for loc in locations if loc["locationName"] == location_name), None)
        if not location:
            return f"⚠️ 找不到地點 {location_name} 的氣象資料"

        weather_elements = location["weatherElement"]
        weather = [f"📍 {location_name} 7天天氣預報："]
        for i in range(7):
            date = weather_elements[0]["time"][i]["startTime"].split("T")[0]
            wx = weather_elements[0]["time"][i]["elementValue"][0]["value"]
            min_temp = weather_elements[1]["time"][i]["elementValue"][0]["value"]
            max_temp = weather_elements[2]["time"][i]["elementValue"][0]["value"]
            weather.append(f"{date}：{wx}，🌡️ {min_temp}°C - {max_temp}°C")
        return "\n".join(weather)
    except Exception as e:
        return f"❌ 取得氣象資料失敗：{str(e)}"

@app.route("/", methods=["GET"])
def verify():
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if token == VERIFY_TOKEN:
        return challenge
    return "驗證失敗"

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    try:
        for entry in data["entry"]:
            for msg in entry["messaging"]:
                sender_id = msg["sender"]["id"]
                if "message" in msg and "text" in msg["message"]:
                    text = msg["message"]["text"]
                    if "氣象預報" in text:
                        reply = "請告訴我您要查詢的縣市，例如「台北市」"
                    else:
                        reply = get_weather(text)
                    send_message(sender_id, reply)
    except Exception as e:
        print(f"❌ Webhook 發生錯誤：{str(e)}")
    return "ok"

def send_message(recipient_id, text):
    url = "https://graph.facebook.com/v17.0/me/messages"
    headers = {"Content-Type": "application/json"}
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": text},
        "messaging_type": "RESPONSE"
    }
    params = {"access_token": PAGE_ACCESS_TOKEN}
    requests.post(url, headers=headers, params=params, json=payload)
