# ☁️ Facebook Messenger 天氣預報機器人（Render 版）

本專案是部署在 Render 的免費 Facebook Messenger Chatbot，可提供中央氣象局資料的即時 7 天天氣預報。

---

## 📁 專案結構

```
├── app.py              # Flask 主程式
├── cwa_bundle.crt      # 安裝中央氣象局所需憑證
├── requirements.txt    # Python 套件
```

---

## 🚀 Render 部署教學（免費）

### 1️⃣ 註冊與新建 Web Service

1. 前往 https://render.com 註冊帳號
2. 點選「New +」→ Web Service
3. 選擇「Deploy an existing project」→ 點選「Upload .zip」並上傳本專案

### 2️⃣ 選擇設定

- Environment：`Python 3`
- Start Command：`gunicorn app:app`
- Build Command：`pip install -r requirements.txt`

### 3️⃣ 設定環境變數（Environment Variables）

| 名稱 | 說明 |
|------|------|
| `VERIFY_TOKEN` | 自訂驗證字串 |
| `PAGE_ACCESS_TOKEN` | Facebook 粉專金鑰 |
| `CWB_API_KEY` | 中央氣象局 API Key |

---

## 🔒 安裝中央氣象局憑證教學（自動處理）

本程式已自帶憑證 `cwa_bundle.crt`，無需額外安裝。程式會使用：

```python
requests.get(url, verify='cwa_bundle.crt')
```

避免 Render 上出現 `CERTIFICATE_VERIFY_FAILED` 錯誤。

---

## 💬 機器人使用方式

1. 傳送訊息 `氣象預報`
2. 回覆：「請問您想查詢哪個縣市？」
3. 傳送「台中市」→ 機器人會顯示 7 天預報

---

## 📡 Facebook Messenger Webhook 設定

1. 在 Facebook Developer Portal 建立 Messenger App
2. Webhook URL 填寫你的 Render 網址（例如 `https://your-bot.onrender.com`）
3. VERIFY_TOKEN 輸入你部署時設定的 token

---

## ✅ 完成！

部署後你的 bot 就能即時回覆「氣象預報」和天氣查詢了。
