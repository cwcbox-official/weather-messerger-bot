import os
import requests
from flask import Flask, request

app = Flask(__name__)

VERIFY_TOKEN = os.getenv('VERIFY_TOKEN')
PAGE_TOKEN = os.getenv('PAGE_ACCESS_TOKEN')
CWB_API_KEY = os.getenv('CWB_API_KEY')

CWB_BASE = 'https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-089'

SUPPORTED = ["台北市","新北市","桃園市","台中市","台南市","高雄市",
             "基隆市","新竹市","嘉義市","新竹縣","苗栗縣","彰化縣","南投縣",
             "雲林縣","嘉義縣","屏東縣","宜蘭縣","花蓮縣","台東縣",
             "澎湖縣","金門縣","連江縣"]

def get_forecast(city):
    params = {
        'Authorization': CWB_API_KEY,
        'locationName': city,
        'format': 'JSON'
    }
    try:
        r = requests.get(CWB_BASE, params=params, timeout=5)
        r.raise_for_status()
        j = r.json()
        locs = j['records']['locations'][0]['location'][0]['weatherElement']
        out = f"{city} 未來 7 天預報：\n"
        for idx in ['MinT','MaxT','WeatherDescription']:
            for tm in locs[idx]['time']:
                start, end = tm['startTime'], tm['endTime']
                val = tm['elementValue'][0]['value']
                out += f"{start[:10]} 至 {end[:10]} — {idx}: {val}\n"
        return out
    except Exception as e:
        return f"❌ 取得氣象資料失敗：{str(e)}"

@app.route('/', methods=['GET'])
def verify():
    if request.args.get('hub.verify_token') == VERIFY_TOKEN:
        return request.args.get('hub.challenge')
    return '驗證失敗', 403

@app.route('/', methods=['POST'])
def webhook():
    data = request.json
    for entry in data.get('entry', []):
        for msg in entry.get('messaging', []):
            sender = msg['sender']['id']
            if 'message' in msg:
                text = msg['message'].get('text', '')
                if text == '氣象預報':
                    send_msg(sender, "請輸入縣市名稱（例如：台北市）")
                elif text in SUPPORTED:
                    forecast = get_forecast(text)
                    send_msg(sender, forecast)
                else:
                    send_msg(sender, "無效縣市名稱，請輸入有效名稱")
    return 'OK', 200

def send_msg(uid, txt):
    requests.post(
        f"https://graph.facebook.com/v11.0/me/messages?access_token={PAGE_TOKEN}",
        json={'recipient': {'id': uid}, 'message': {'text': txt}}
    )

if __name__ == '__main__':
    app.run()