<#
install_dependencies.ps1
- 在 Windows 上自動建立虛擬環境並安裝 requirements.txt 中的套件
- 使用方式 (PowerShell):
    1) 若尚未允許執行腳本，先在 PowerShell 執行：
       Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
    2) 直接執行：
       .\install_dependencies.ps1
    3) 若要跳過建立 venv（直接在系統 Python 安裝）：
       .\install_dependencies.ps1 -SkipVenv

參數：
 -SkipVenv    : 如果指定，將直接使用系統 Python 安裝套件（不建立虛擬環境）
 -VenvName    : 指定虛擬環境名稱 (預設 ".venv")
#>
param(
    [switch]$SkipVenv,
    [string]$VenvName = ".venv"
)

function Write-Info($msg){ Write-Host "[INFO]  $msg" -ForegroundColor Cyan }
function Write-Success($msg){ Write-Host "[OK]    $msg" -ForegroundColor Green }
function Write-ErrorMsg($msg){ Write-Host "[ERROR] $msg" -ForegroundColor Red }

# 檢查執行環境：PowerShell 版本與 Windows 版本 (本專案僅支援 Windows 10 以上)
if ($PSVersionTable.PSVersion.Major -lt 5) {
    Write-ErrorMsg "此腳本需要 PowerShell 5 或以上（Windows 10 內建）。"
    exit 1
}

try {
    $os = Get-CimInstance -ClassName Win32_OperatingSystem -ErrorAction Stop
    $version = $os.Version
    $major = [int]($version.Split('.')[0])
    if ($major -lt 10) {
        Write-ErrorMsg "本專案僅支援 Windows 10 或以上 (偵測到 Windows $version)。"
        exit 1
    } else {
        Write-Info "偵測到 Windows $version，符合需求。"
    }
} catch {
    Write-Info "無法偵測 Windows 版本；若非 Windows 環境或權限不足，請確認您使用的是 Windows 10 或以上。"
}

# 取得專案根目錄（此腳本的所在目錄）
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

# 確認 requirements.txt
$reqFile = Join-Path $ScriptDir 'requirements.txt'
if (-not (Test-Path $reqFile)){
    Write-ErrorMsg "找不到 requirements.txt（路徑: $reqFile）。請確認檔案存在。"
    exit 1
}

# 找 Python
$pythonCmd = $null
if (Get-Command python -ErrorAction SilentlyContinue) {
    $pythonCmd = 'python'
} elseif (Get-Command py -ErrorAction SilentlyContinue) {
    $pythonCmd = 'py -3'
}

if (-not $pythonCmd) {
    Write-ErrorMsg "找不到 Python 可執行檔。請先安裝 Python 3 並將其加入 PATH，或使用 py 啟動器。"
    exit 1
}

if (-not $SkipVenv) {
    Write-Info "建立虛擬環境：$VenvName"
    & $pythonCmd -m venv $VenvName
    if ($LASTEXITCODE -ne 0) {
        Write-ErrorMsg "建立虛擬環境失敗（退碼 $LASTEXITCODE）。請檢查 Python 安裝。"
        exit 1
    }

    $venvPython = Join-Path $ScriptDir "$VenvName\Scripts\python.exe"
    if (-not (Test-Path $venvPython)) {
        Write-ErrorMsg "找不到虛擬環境中的 python（預期路徑：$venvPython）。"
        exit 1
    }

    Write-Info "升級 pip 並安裝套件"
    & $venvPython -m pip install --upgrade pip setuptools wheel
    if ($LASTEXITCODE -ne 0) { Write-ErrorMsg "pip 升級失敗"; exit 1 }
    & $venvPython -m pip install -r $reqFile
    if ($LASTEXITCODE -ne 0) { Write-ErrorMsg "套件安裝失敗"; exit 1 }

    Write-Success "套件已安裝到虛擬環境：$VenvName"
    Write-Info "啟動虛擬環境（PowerShell 範例）："
    Write-Host "  Set-Location $ScriptDir; .\\$VenvName\\Scripts\\Activate.ps1"
} else {
    Write-Info "跳過 venv，直接在系統 Python 上安裝（可能需要管理員權限）"
    & $pythonCmd -m pip install --upgrade pip setuptools wheel
    if ($LASTEXITCODE -ne 0) { Write-ErrorMsg "pip 升級失敗"; exit 1 }
    & $pythonCmd -m pip install -r $reqFile
    if ($LASTEXITCODE -ne 0) { Write-ErrorMsg "套件安裝失敗"; exit 1 }
    Write-Success "套件已安裝到系統 Python"
}

Write-Host "\n完成。建議：在每個專案機器使用虛擬環境，以避免套件衝突。" -ForegroundColor Yellow
