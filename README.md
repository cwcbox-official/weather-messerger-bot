
# Messenger 天氣預報機器人（中央氣象局版）

## 📌 功能
- 使用者輸入「氣象預報」→ 機器人詢問縣市名稱
- 使用者輸入縣市名稱（如「台北市」）→ 機器人回傳該地區的 7 天氣象預報

## 🔗 API 資料來源
- 中央氣象局資料開放平台：https://opendata.cwa.gov.tw/
- 使用 API：F-D0047-091（需註冊取得 API 金鑰）

## 📁 專案檔案說明

| 檔案名稱        | 說明                   |
| --------------- | ---------------------- |
| app.py          | 主程式（Flask 架構）  |
| requirements.txt| 所需 Python 套件清單  |
| README.md       | 說明文件               |

## ⚙️ 環境變數設定（Render）

| 名稱             | 說明                            |
| ---------------- | ------------------------------- |
| VERIFY_TOKEN     | Facebook Webhook 驗證 Token     |
| PAGE_ACCESS_TOKEN| Facebook 粉絲專頁權杖           |
| CWB_API_KEY      | 中央氣象局 API 金鑰              |

## 🚀 Render 免費部署教學

1. 前往 https://render.com 並註冊帳號
2. 建立 Web Service → 選擇「Upload .zip」
3. 上傳本專案的壓縮檔（含 app.py 等檔案）
4. 在「Environment」頁籤中設定環境變數：
   - VERIFY_TOKEN
   - PAGE_ACCESS_TOKEN
   - CWB_API_KEY
5. 部署完成後取得網址，例如：https://xxx.onrender.com
6. 回到 Facebook 開發者後台 → 設定 Webhook：
   - 填入網址並加上 `/`
   - 訂閱事件：✅ messages、✅ messaging_postbacks

## 🧪 本地測試方式

```bash
pip install -r requirements.txt
gunicorn app:app
```

## 🌇 支援縣市名稱

台北市、新北市、桃園市、台中市、台南市、高雄市  
基隆市、新竹市、嘉義市  
新竹縣、苗栗縣、彰化縣、南投縣、雲林縣、嘉義縣、屏東縣  
宜蘭縣、花蓮縣、台東縣、澎湖縣、金門縣、連江縣

## 🧯 錯誤處理

- 若找不到資料，會顯示：⚠️ 找不到地點的氣象資料
- 若系統錯誤，會顯示：❌ 取得氣象資料失敗 + 錯誤訊息
