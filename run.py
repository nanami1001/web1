import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from project import create_app

# 讀取啟動設定：可由環境變數 `APP_ENV` 或 `FLASK_ENV` 指定
# 範例：在 PowerShell 先執行 `$env:APP_ENV='development'`，再 `python run.py`
env = os.environ.get('APP_ENV') or os.environ.get('FLASK_ENV')
app = create_app(config_name=env)

if __name__ == "__main__":
    # 使用 config 中的 DEBUG 決定是否啟用開發伺服器的 debug 模式
    app.run(debug=app.config.get('DEBUG', False))
