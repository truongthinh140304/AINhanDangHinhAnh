# ================================================
# SCRIPT RESET POSTGRESQL PASSWORD (Chay voi Admin)
# ================================================

Write-Host "`n======================================" -ForegroundColor Cyan
Write-Host "  RESET POSTGRESQL PASSWORD" -ForegroundColor Cyan
Write-Host "======================================`n" -ForegroundColor Cyan

# Kiem tra Admin
$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "[X] Phai chay voi quyen Admin!" -ForegroundColor Red
    Write-Host "`nCach chay:" -ForegroundColor Yellow
    Write-Host "1. Nhan chuot phai vao PowerShell" -ForegroundColor Yellow
    Write-Host "2. Chon 'Run as Administrator'" -ForegroundColor Yellow
    Write-Host "3. Chay lai script nay`n" -ForegroundColor Yellow
    Read-Host "Nhan Enter de thoat"
    exit
}

# Tim file pg_hba.conf
Write-Host "[1] Tim file pg_hba.conf..." -ForegroundColor Yellow
$pgHbaFile = Get-ChildItem "C:\Program Files\PostgreSQL" -Recurse -Filter "pg_hba.conf" -ErrorAction SilentlyContinue | Select-Object -First 1 -ExpandProperty FullName

if (-not $pgHbaFile) {
    Write-Host "[X] Khong tim thay file pg_hba.conf!" -ForegroundColor Red
    Read-Host "Nhan Enter de thoat"
    exit
}

Write-Host "[OK] Found: $pgHbaFile`n" -ForegroundColor Green

# Backup file
Write-Host "[2] Backup file pg_hba.conf..." -ForegroundColor Yellow
$backupFile = "$pgHbaFile.backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
Copy-Item $pgHbaFile $backupFile
Write-Host "[OK] Backup: $backupFile`n" -ForegroundColor Green

# Doc file
$content = Get-Content $pgHbaFile

# Thay the scram-sha-256 bang trust
Write-Host "[3] Thay doi authentication method..." -ForegroundColor Yellow
$newContent = $content -replace 'scram-sha-256', 'trust' -replace 'md5', 'trust'
$newContent | Set-Content $pgHbaFile
Write-Host "[OK] Da thay doi thanh 'trust' mode`n" -ForegroundColor Green

# Restart PostgreSQL service
Write-Host "[4] Restart PostgreSQL service..." -ForegroundColor Yellow
$service = Get-Service -Name postgresql* | Select-Object -First 1

if ($service) {
    Write-Host "Service name: $($service.Name)" -ForegroundColor Cyan
    Restart-Service $service.Name
    Start-Sleep -Seconds 3
    Write-Host "[OK] Service restarted!`n" -ForegroundColor Green
} else {
    Write-Host "[X] Khong tim thay PostgreSQL service!" -ForegroundColor Red
    Write-Host "Hay restart service thu cong!`n" -ForegroundColor Yellow
}

# Doi password
Write-Host "[5] Doi password cho user postgres..." -ForegroundColor Yellow
Write-Host "Nhap password moi (de trong de dung 'postgres'): " -ForegroundColor Cyan -NoNewline
$newPassword = Read-Host

if ([string]::IsNullOrWhiteSpace($newPassword)) {
    $newPassword = "postgres"
}

Write-Host "`nDang doi password..." -ForegroundColor Yellow

$psqlExe = "C:\Program Files\PostgreSQL\18\bin\psql.exe"
$sqlCommand = "ALTER USER postgres WITH PASSWORD '$newPassword';"

try {
    & $psqlExe -U postgres -d postgres -c $sqlCommand 2>&1 | Out-Null
    Write-Host "[OK] Password da doi thanh: $newPassword`n" -ForegroundColor Green
} catch {
    Write-Host "[X] Loi khi doi password!" -ForegroundColor Red
    Write-Host "Thu chay lenh thu cong:`n" -ForegroundColor Yellow
    Write-Host "psql -U postgres -d postgres" -ForegroundColor Cyan
    Write-Host "ALTER USER postgres WITH PASSWORD 'yourPassword';`n" -ForegroundColor Cyan
}

# Khoi phuc authentication
Write-Host "[6] Khoi phuc authentication..." -ForegroundColor Yellow
$originalContent = Get-Content $backupFile
$originalContent | Set-Content $pgHbaFile
Write-Host "[OK] Da khoi phuc authentication`n" -ForegroundColor Green

# Restart lai service
Write-Host "[7] Restart PostgreSQL service lan 2..." -ForegroundColor Yellow
if ($service) {
    Restart-Service $service.Name
    Start-Sleep -Seconds 3
    Write-Host "[OK] Done!`n" -ForegroundColor Green
}

# Test connection
Write-Host "[8] Test connection voi password moi..." -ForegroundColor Yellow
$env:PGPASSWORD = $newPassword
$testResult = & $psqlExe -U postgres -d postgres -c "SELECT 1;" 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] Connection successful!`n" -ForegroundColor Green
} else {
    Write-Host "[X] Ket noi that bai!" -ForegroundColor Red
    Write-Host "Thu lai voi password khac!`n" -ForegroundColor Yellow
}

# Huong dan update .env
Write-Host "`n======================================" -ForegroundColor Cyan
Write-Host "  BUOC TIEP THEO" -ForegroundColor Cyan
Write-Host "======================================`n" -ForegroundColor Cyan

Write-Host "1. Mo file .env:" -ForegroundColor Yellow
Write-Host "   cd D:\AInhandanghinhanh\backend" -ForegroundColor Cyan
Write-Host "   notepad .env`n" -ForegroundColor Cyan

Write-Host "2. Thay doi dong DATABASE_URL:" -ForegroundColor Yellow
Write-Host "   DATABASE_URL=postgresql://postgres:$newPassword@localhost:5432/nhandanghinhanh`n" -ForegroundColor Cyan

Write-Host "3. Luu file va chay backend:" -ForegroundColor Yellow
Write-Host "   cd D:\AInhandanghinhanh\backend" -ForegroundColor Cyan
Write-Host "   .\venv\Scripts\activate" -ForegroundColor Cyan
Write-Host "   python init_db.py" -ForegroundColor Cyan
Write-Host "   python main.py`n" -ForegroundColor Cyan

Write-Host "======================================`n" -ForegroundColor Cyan
Write-Host "Password moi: $newPassword" -ForegroundColor Green
Write-Host "Backup file: $backupFile" -ForegroundColor Yellow
Write-Host "`n[!] Luu y: Hay nho password nay!`n" -ForegroundColor Yellow

Read-Host "Nhan Enter de thoat"

