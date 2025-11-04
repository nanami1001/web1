# 新光三越台南店資訊系統

一個使用 Flask 建立的網站系統，提供商店資訊、用戶評價、文章發布等功能。

## 功能特點

- 用戶註冊和登入系統
- 兩步驟驗證功能
- 用戶個人檔案管理（包含頭像上傳）
- 文章發布系統（支援圖片上傳）
- 評價系統
- 響應式設計

## 技術架構

- Flask
- SQLAlchemy
- Flask-Login
- Flask-WTF
- Pillow
- PyOTP
- 等其他

## 安裝說明

1. 克隆專案：
```bash
git clone [repository-url]
cd [repository-name]
```

2. 創建虛擬環境：
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. 安裝依賴：
```bash
pip install -r requirements.txt
```

4. 初始化資料庫：
```bash
flask db upgrade
```

5. 運行應用：
```bash
python run.py
```

## 環境要求

- Python 3.8+
- 詳細套件需求請見 requirements.txt

## 目錄結構

```
project/
├── __init__.py
├── config.py
├── models.py
├── forms.py
├── routes/
│   ├── auth.py
│   ├── main.py
│   └── posts.py
├── static/
│   └── style.css
└── templates/
    ├── base.html
    ├── home.html
    └── ...
```

## 授權

MIT License