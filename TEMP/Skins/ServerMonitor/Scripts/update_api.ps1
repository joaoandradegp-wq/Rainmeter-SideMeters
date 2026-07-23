# ----------------------------------------------------
# Antes de comecar, mata qualquer instancia anterior
# desse mesmo script que ainda esteja rodando, entao
# so fica UM powershell ativo por vez.
# ----------------------------------------------------
$myPid = $PID

Get-CimInstance Win32_Process -Filter "Name = 'powershell.exe'" |
    Where-Object { $_.CommandLine -match 'update_api\.ps1' -and $_.ProcessId -ne $myPid } |
    ForEach-Object {
        try { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue } catch {}
    }

$url = "http://192.168.100.121:8181/api/rainmeter"
$apiFile = "$PSScriptRoot\..\@Resources\api.txt"
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)

while ($true)
{
    try
    {
        $response = Invoke-WebRequest `
            -Uri $url `
            -UseBasicParsing `
            -TimeoutSec 5

        [System.IO.File]::WriteAllText($apiFile, $response.Content, $utf8NoBom)
    }
    catch
    {
        [System.IO.File]::WriteAllText($apiFile, "ERROR=API OFFLINE", $utf8NoBom)
    }

    Start-Sleep -Seconds 5
}
