# Messenger 天氣預報機器人（中央氣象局版）

## 功能
- 使用者輸入「氣象預報」，機器人會詢問要查詢的縣市
- 回覆有效地名後，顯示中央氣象局 7 天預報資料

## 使用 API
- 中央氣象局 API：F-D0047-089（縣市級 7 天預報）
- https://opendata.cwa.gov.tw/

## 部署方式（Render 免費方案）
1. 註冊 Render 並建立 Web Service，選 Upload .zip
2. 上傳此 zip 並設定三個環境變數：
   - VERIFY_TOKEN
   - PAGE_ACCESS_TOKEN
   - CWB_API_KEY
3. 完成部署後設定 Webhook（網址後面加 `/`）
4. 訂閱事件：✅ messages、✅ messaging_postbacks

## 本機測試
```bash
pip install -r requirements.txt
gunicorn app:app
```

## 支援縣市
台北市、新北市、桃園市、台中市、台南市、高雄市、基隆市、新竹市、嘉義市、
新竹縣、苗栗縣、彰化縣、南投縣、雲林縣、嘉義縣、屏東縣、宜蘭縣、花蓮縣、
台東縣、澎湖縣、金門縣、連江縣

## 錯誤處理
- 錯誤會顯示「取得氣象資料失敗，請稍後再試」或「無效縣市名稱」