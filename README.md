# Messenger 天氣預報機器人（中央氣象局版）

## 📌 功能說明

使用者輸入 `氣象預報` → 機器人詢問哪個縣市 → 使用者輸入縣市名稱 → 機器人回覆該縣市的 7 天氣象預報

## 🔗 使用 API

- 資料來源：[中央氣象局資料開放平台](https://opendata.cwa.gov.tw/)
- API：F-D0047（縣市級 7 天預報）

## 📁 專案檔案

| 檔案名稱       | 說明                    |
|----------------|-------------------------|
| app.py         | 主程式（Flask 機器人邏輯） |
| requirements.txt | Python 所需套件清單     |
| README.md      | 本說明文件               |

## ⚙️ 環境變數（Render 平台設定）

| 名稱              | 說明                    |
|-------------------|-------------------------|
| `VERIFY_TOKEN`    | Facebook Webhook 驗證用 |
| `PAGE_ACCESS_TOKEN` | 粉專權杖                |
| `CWB_API_KEY`     | 中央氣象局 API 金鑰     |

## 🚀 免費 Render 部署教學

1. 前往 [https://render.com](https://render.com)，註冊帳號
2. 建立 Web Service，選擇「Upload .zip」上傳本專案壓縮檔
3. 在 "Environment" 頁籤設定以下變數：
   - VERIFY_TOKEN
   - PAGE_ACCESS_TOKEN
   - CWB_API_KEY
4. 部署完成後會得到一個網址（例：https://your-bot.onrender.com）

### 🔁 Facebook Webhook 設定

- 回到 Facebook 開發者後台
- Webhook 網址填入：`https://your-bot.onrender.com/`
- 訂閱事件：✅ `messages`、✅ `messaging_postbacks`

## 🧪 本地啟動方式

```bash
pip install -r requirements.txt
gunicorn app:app
```

## 🌇 支援縣市列表

台北市、新北市、桃園市、台中市、台南市、高雄市、基隆市、新竹市、嘉義市、新竹縣、苗栗縣、彰化縣、南投縣、雲林縣、嘉義縣、屏東縣、宜蘭縣、花蓮縣、台東縣、澎湖縣、金門縣、連江縣

---

👉 免費使用，歡迎改作與部署。
