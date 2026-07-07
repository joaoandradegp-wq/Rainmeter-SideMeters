$mutex = New-Object System.Threading.Mutex($false, "RedeMonitorMutex")
if (-not $mutex.WaitOne(0, $false)) { exit }

while ($true)
{
    $pc1 = if (Test-Connection "VIVIANE" -Count 1 -Quiet) { "ONLINE" } else { "OFFLINE" }
    $pc2 = if (Test-Connection "JULIA" -Count 1 -Quiet) { "ONLINE" } else { "OFFLINE" }
    $pc3 = if (Test-Connection "server.yakalo-trout.ts.net" -Count 1 -Quiet) { "ONLINE" } else { "OFFLINE" }
    $pc4 = if (Test-Connection "nin" -Count 1 -Quiet) { "ONLINE" } else { "OFFLINE" }
    $pc5 = if (Test-Connection "dell.yakalo-trout.ts.net" -Count 1 -Quiet) { "ONLINE" } else { "OFFLINE" }
    $pc6 = if (Test-Connection "marly.ddns.net" -Count 1 -Quiet) { "ONLINE" } else { "OFFLINE" }
    $pc7 = if (Test-NetConnection "server.yakalo-trout.ts.net" -Port 8080 -InformationLevel Quiet) { "ONLINE" } else { "OFFLINE" }

    $status = "$pc1`n$pc2`n$pc3`n$pc4`n$pc5`n$pc6`n$pc7"
    $status | Out-File "$env:USERPROFILE\Documents\Rainmeter\network_status.tmp" -Encoding ASCII
    Move-Item "$env:USERPROFILE\Documents\Rainmeter\network_status.tmp" "$env:USERPROFILE\Documents\Rainmeter\network_status.txt" -Force

    Start-Sleep -Seconds 5
}