import os
from flask import Flask, request
import requests

app = Flask(__name__)

VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN")
PAGE_ACCESS_TOKEN = os.environ.get("PAGE_ACCESS_TOKEN")
CWB_API_KEY = os.environ.get("CWB_API_KEY")

@app.route("/", methods=['GET'])
def verify():
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if token == VERIFY_TOKEN:
        return challenge, 200
    return "驗證失敗", 403

@app.route("/", methods=['POST'])
def webhook():
    data = request.get_json()
    if data['object'] == 'page':
        for entry in data['entry']:
            for event in entry.get('messaging', []):
                sender_id = event['sender']['id']
                if 'message' in event and 'text' in event['message']:
                    message = event['message']['text'].strip()
                    reply = get_weather_reply(message)
                    send_message(sender_id, reply)
    return "ok", 200

def get_weather_reply(message):
    if message == "氣象預報":
        return "請問您想查詢哪個縣市？"
    else:
        return fetch_weather(message)

def fetch_weather(city_name):
    url = f"https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-D0047-091?Authorization={CWB_API_KEY}&locationName={city_name}"
    try:
        res = requests.get(url, verify=False)
        data = res.json()

if not data.get("success", False):
    return f"❌ API 失敗，請檢查金鑰或伺服器狀態"

records = data.get("records", {})
locations_list = records.get("locations", [])

if not locations_list:
    return f"❌ 查無地區「{city_name}」資料，請確認名稱或稍後再試"

location_data = locations_list[0].get("location", [])
if not location_data:
    return f"❌ 地區資料無法解析，可能氣象局尚未提供該地區資料"

        if not locations:
            return f"找不到「{city_name}」的氣象資料。請輸入正確縣市名。"

        result = f"📍 {city_name} 7 天預報：\n"
        weather_elements = locations[0]['weatherElement']
        descs = [w for w in weather_elements if w['elementName'] == 'WeatherDescription'][0]['time']
        for d in descs[:7]:
            result += f"🗓️ {d['startTime'][:10]}：{d['elementValue'][0]['value']}\n"
        return result.strip()
    except Exception as e:
        return f"❌ 取得氣象資料失敗：{e}"

def send_message(recipient_id, message_text):
    url = "https://graph.facebook.com/v18.0/me/messages"
    headers = {"Content-Type": "application/json"}
    data = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text},
        "messaging_type": "RESPONSE"
    }
    params = {"access_token": PAGE_ACCESS_TOKEN}
    requests.post(url, headers=headers, json=data, params=params)
