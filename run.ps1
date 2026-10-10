# Detecta la pantalla secundaria (auxiliar), muestra su resolucion y abre el dashboard en kiosco ahi.
Add-Type -AssemblyName System.Windows.Forms
$screens = [System.Windows.Forms.Screen]::AllScreens
$screens | ForEach-Object { "{0} primary={1} {2}x{3} en ({4},{5})" -f $_.DeviceName,$_.Primary,$_.Bounds.Width,$_.Bounds.Height,$_.Bounds.X,$_.Bounds.Y }
$s = $screens | Where-Object { -not $_.Primary } | Select-Object -First 1
if (-not $s) { Write-Host "No hay segunda pantalla; usando la principal."; $s = $screens[0] }
$o = if ($s.Bounds.Height -gt $s.Bounds.Width) { "VERTICAL" } else { "horizontal" }
Write-Host ("Usando {0}x{1} ({2})" -f $s.Bounds.Width,$s.Bounds.Height,$o)

Start-Process pythonw -ArgumentList "server.py" -WorkingDirectory $PSScriptRoot -WindowStyle Hidden
Start-Sleep 2

$cands = @("$env:ProgramFiles\Google\Chrome\Application\chrome.exe",
           "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe",
           "${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe",
           "$env:ProgramFiles\Microsoft\Edge\Application\msedge.exe")
$b = $cands | Where-Object { Test-Path $_ } | Select-Object -First 1
Start-Process $b -ArgumentList @("--user-data-dir=$env:TEMP\dash-profile","--new-window",
  "--window-position=$($s.Bounds.X),$($s.Bounds.Y)","--window-size=$($s.Bounds.Width),$($s.Bounds.Height)",
  "--kiosk","http://localhost:8000")
