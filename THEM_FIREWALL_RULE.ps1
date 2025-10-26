# Script thêm Firewall rule cho Backend API
# Chạy với quyền Administrator

Write-Host "`n==================== THEM FIREWALL RULE ====================" -ForegroundColor Cyan
Write-Host "`nScript nay se them rule cho phep ket noi den port 8000" -ForegroundColor Yellow
Write-Host "Ban can chay PowerShell voi quyen Administrator!`n" -ForegroundColor Red

# Kiểm tra quyền Admin
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "[X] Chua co quyen Administrator!" -ForegroundColor Red
    Write-Host "`nCAC BUOC THUC HIEN:" -ForegroundColor Yellow
    Write-Host "1. Click phai vao PowerShell" -ForegroundColor White
    Write-Host "2. Chon 'Run as Administrator'" -ForegroundColor White
    Write-Host "3. Chay lai script nay`n" -ForegroundColor White
    
    Read-Host "Nhan Enter de dong..."
    exit 1
}

Write-Host "[OK] Dang chay voi quyen Administrator`n" -ForegroundColor Green

# Kiểm tra rule đã tồn tại chưa
$existingRule = Get-NetFirewallRule -DisplayName "Python Backend API - Port 8000" -ErrorAction SilentlyContinue

if ($existingRule) {
    Write-Host "[!] Rule da ton tai!" -ForegroundColor Yellow
    Write-Host "    Ban co muon xoa va tao lai? (y/n): " -NoNewline -ForegroundColor White
    $answer = Read-Host
    
    if ($answer -eq 'y') {
        Remove-NetFirewallRule -DisplayName "Python Backend API - Port 8000"
        Write-Host "[OK] Da xoa rule cu`n" -ForegroundColor Green
    } else {
        Write-Host "`n[OK] Giu nguyen rule cu. Thoat...`n" -ForegroundColor Green
        Read-Host "Nhan Enter de dong..."
        exit 0
    }
}

# Tạo rule mới
try {
    Write-Host "Dang tao Firewall rule..." -ForegroundColor Yellow
    
    New-NetFirewallRule `
        -DisplayName "Python Backend API - Port 8000" `
        -Description "Allow inbound connections to Python Backend API on port 8000" `
        -Direction Inbound `
        -LocalPort 8000 `
        -Protocol TCP `
        -Action Allow `
        -Enabled True `
        -Profile Any `
        -ErrorAction Stop | Out-Null
    
    Write-Host "`n[OK] TAO RULE THANH CONG!" -ForegroundColor Green
    Write-Host "`nChi tiet rule:" -ForegroundColor Cyan
    Write-Host "  Ten: Python Backend API - Port 8000" -ForegroundColor White
    Write-Host "  Port: 8000" -ForegroundColor White
    Write-Host "  Protocol: TCP" -ForegroundColor White
    Write-Host "  Direction: Inbound (Cho phep ket noi vao)" -ForegroundColor White
    Write-Host "  Action: Allow" -ForegroundColor White
    Write-Host "  Trang thai: Enabled`n" -ForegroundColor White
    
    Write-Host "=========================================================`n" -ForegroundColor Cyan
    Write-Host "[OK] HOAN THANH! Backend co the nhan ket noi tu dien thoai!" -ForegroundColor Green
    Write-Host "`n" -ForegroundColor White
    
} catch {
    Write-Host "`n[X] LOI TAO RULE!" -ForegroundColor Red
    Write-Host "Loi: $($_.Exception.Message)`n" -ForegroundColor Red
}

Read-Host "Nhan Enter de dong..."

