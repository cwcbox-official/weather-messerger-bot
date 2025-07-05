from flask import Flask, request
import requests
import os

app = Flask(__name__)

VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN")
PAGE_ACCESS_TOKEN = os.environ.get("PAGE_ACCESS_TOKEN")
CWB_API_KEY = os.environ.get("CWB_API_KEY")

city_map = {
    "台北市": "F-D0047-063",
    "新北市": "F-D0047-071",
    "桃園市": "F-D0047-007",
    "台中市": "F-D0047-075",
    "台南市": "F-D0047-079",
    "高雄市": "F-D0047-083",
    "基隆市": "F-D0047-067",
    "新竹市": "F-D0047-011",
    "嘉義市": "F-D0047-015",
    "新竹縣": "F-D0047-005",
    "苗栗縣": "F-D0047-009",
    "彰化縣": "F-D0047-017",
    "南投縣": "F-D0047-073",
    "雲林縣": "F-D0047-023",
    "嘉義縣": "F-D0047-027",
    "屏東縣": "F-D0047-087",
    "宜蘭縣": "F-D0047-031",
    "花蓮縣": "F-D0047-035",
    "台東縣": "F-D0047-039",
    "澎湖縣": "F-D0047-043",
    "金門縣": "F-D0047-047",
    "連江縣": "F-D0047-051"
}

@app.route("/", methods=['GET'])
def verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return "驗證失敗", 403

@app.route("/", methods=['POST'])
def webhook():
    data = request.get_json()
    for entry in data.get("entry", []):
        for messaging_event in entry.get("messaging", []):
            sender_id = messaging_event["sender"]["id"]
            if messaging_event.get("message"):
                text = messaging_event["message"].get("text")
                if text == "氣象預報":
                    send_message(sender_id, "請輸入縣市名稱（例如：台北市）")
                elif text in city_map:
                    forecast = get_weather(city_map[text])
                    send_message(sender_id, forecast)
                else:
                    send_message(sender_id, "請輸入正確的縣市名稱")
    return "ok", 200

def send_message(recipient_id, message_text):
    params = {"access_token": PAGE_ACCESS_TOKEN}
    headers = {"Content-Type": "application/json"}
    data = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }
    requests.post("https://graph.facebook.com/v13.0/me/messages", params=params, headers=headers, json=data)

def get_weather(location_id):
    url = f"https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-D0047-089?Authorization={CWB_API_KEY}&locationName={city_name}"
    try:
        print("📡 Request URL:", url)
        res = requests.get(url, verify=False)  # disable SSL verify for workaround
        print("📥 Response:", res.text)
        data = res.json()
        elements = data["records"]["locations"][0]["location"][0]["weatherElement"]
        time_slots = elements[0]["time"][:7]
        forecast = ""
        for t in time_slots:
            start = t["startTime"]
            end = t["endTime"]
            desc = t["elementValue"][0]["value"]
            forecast += f"{start} ~ {end}: {desc}\n"
        return forecast
    except Exception as e:
        return f"❌ 取得氣象資料失敗：{e}"
