快速安裝說明
================

注意：本專案僅支援 Windows 10 或更新版本（PowerShell 5+）。安裝腳本會在執行前檢查作業系統版本，若不符合條件會停止執行。

目的：讓其他開發者或測試機器能快速安裝本專案所需的 Python 套件。

檔案：
- `install_dependencies.ps1`：PowerShell 安裝腳本（Windows 10+）。
- `requirements.txt`：套件清單（已包含在 repository）。

使用方法（Windows PowerShell）：
1. 打開 PowerShell（以一般使用者權限即可），切換到專案資料夾（包含 `install_dependencies.ps1`）：

```powershell
cd "C:\Users\user\Downloads\1 (2) (1)\1 (2)\1 (1)"
```

2. 若尚未允許執行本地腳本（預設可能被阻擋），在該視窗暫時允許：

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

3. 直接執行安裝腳本（會檢查 Windows 版本、建立 `.venv` 並安裝套件）：

```powershell
.\install_dependencies.ps1
```

4. 若希望跳過建立虛擬環境，直接安裝到系統 Python（可能需要管理員權限）：

```powershell
.\install_dependencies.ps1 -SkipVenv
```

5. 若建立了虛擬環境，啟用虛擬環境（PowerShell）並啟動應用：

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
python run.py
```

注意事項：
- 若系統上沒有 `python` 指令，腳本會嘗試使用 `py -3` 啟動器。
- 建議使用虛擬環境來隔離套件。
- 若網路或 pip 有問題，請先手動安裝 `pip` 或確認網路能連外。

如需在 macOS / Linux 上使用，建議使用等效的 bash 腳本：
- python3 -m venv .venv
- source .venv/bin/activate
- pip install -r requirements.txt

聯絡開發者以支援其他平台或 CI 自動化腳本。