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
# 可選：設定環境，例如開發模式
# Windows PowerShell 範例：
$env:APP_ENV = 'development'
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

## 密碼重設 / 郵件設定 🔧

此專案支援透過電子郵件寄發「重設密碼」連結。要啟用，請在啟動應用的環境中設定以下環境變數：

- EMAIL_USER — 寄件帳號（例如 Gmail 地址）
- EMAIL_PASS — 寄件帳號密碼或應用程式專用密碼
- （可選）MAIL_SERVER、MAIL_PORT, MAIL_USE_TLS — 覆寫預設值

範例（Windows PowerShell）:

```powershell
$env:EMAIL_USER = 'your.mail@example.com'; $env:EMAIL_PASS = 'supersecret'
# 可選：覆寫預設 sender（預設會使用 EMAIL_USER）
$env:MAIL_DEFAULT_SENDER = 'your.mail@example.com'
python run.py
```

測試說明：

1. 在登入頁點選「忘記密碼？」。
2. 輸入註冊時使用的電子郵件，系統會寄送包含 token 的連結。
3. 點擊郵件中的連結並輸入新密碼即可重設。

注意與常見錯誤：

- Gmail（或部分 SMTP）會要求寄件者與 SMTP 認證帳號相符，或需要使用「應用程式密碼」，否則會出現類似錯誤：
    SMTPSenderRefused: (530, b'5.7.0 Authentication Required...')

- 本地開發時強烈建議改用測試 SMTP（例如 Mailtrap、smtp4dev 或 Papercut）來避免真實發信和認證問題。

詳盡 Mailtrap 測試步驟：

1. 註冊 Mailtrap（https://mailtrap.io）並建立一個 Inbox（免費方案可用於開發測試）。
2. 點開你的 Inbox，找到 SMTP 設定（hostname、port、username、password）。
3. 在本地設定環境變數（PowerShell 範例）：

```powershell
$env:MAIL_SERVER = 'smtp.mailtrap.io'
$env:MAIL_PORT = '2525'
$env:EMAIL_USER = 'YOUR_MAILTRAP_USERNAME'
$env:EMAIL_PASS = 'YOUR_MAILTRAP_PASSWORD'
$env:MAIL_DEFAULT_SENDER = 'noreply@example.com'
# 可選：寄信測試預設收件人
$env:MAIL_TEST_TO = 'your.receiving@example.com'
python run.py
```


4. 登入 Mailtrap 的 Inbox 網頁，應該會看到剛剛發送的測試郵件（或應用發出的 Password Reset 郵件）。

安全提醒：不要把真實使用者密碼或真實 sender 放在公開 repo；在生產使用安全的 secrets 管理方式。

```powershell
$env:MAIL_SERVER = 'smtp.mailtrap.io'
$env:MAIL_PORT = '2525'
$env:EMAIL_USER = 'MAILTRAP_USER'
$env:EMAIL_PASS = 'MAILTRAP_PASS'
# 可選：
$env:MAIL_DEFAULT_SENDER = 'noreply@example.com'
python run.py
```

頻率限制（訊息頻發）說明：

- 系統為了避免濫發重設郵件，對同一個 email 設置了冷卻時間（預設 5 分鐘）。若在冷卻內重複請求，頁面會顯示「訊息頻發：請於 XX 秒後再試」。
- 目前採用記憶體內部緩存記錄重設請求時間（方便本機/開發環境），若要在生產環境使用，建議改用 Redis 或資料庫做全局限流，避免多進程/多實例繞過限制。

要在本機驗證 SMTP 是否正確，建議使用 Mailtrap（或 smtp4dev）並在環境變數中設定 `MAIL_SERVER`/`MAIL_PORT`/`EMAIL_USER`/`EMAIL_PASS` 以及 `MAIL_DEFAULT_SENDER`，然後透過應用的重設流程觸發寄信。

選擇配置（Configuration）：

- 使用 `APP_ENV` 或 `FLASK_ENV` 來選擇設定（`development` / `production` / `testing`）。
- 範例：在 PowerShell 設定 `APP_ENV=development`，`run.py` 會載入 `DevelopmentConfig`。
