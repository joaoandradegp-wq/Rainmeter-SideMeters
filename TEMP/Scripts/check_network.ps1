while ($true)
{
    $pc1 = if (Test-Connection 192.168.100.1 -Count 1 -Quiet) { "ONLINE" } else { "OFFLINE" }
    $pc2 = if (Test-Connection 192.168.100.2 -Count 1 -Quiet) { "ONLINE" } else { "OFFLINE" }
    $pc3 = if (Test-Connection pc1.yakalo-trout.ts.net -Count 1 -Quiet) { "ONLINE" } else { "OFFLINE" }
    $pc4 = if (Test-Connection pc2.yakalo-trout.ts.net -Count 1 -Quiet) { "ONLINE" } else { "OFFLINE" }
    $pc5 = if (Test-Connection pc3.yakalo-trout.ts.net -Count 1 -Quiet) { "ONLINE" } else { "OFFLINE" }
    $pc6 = if (Test-Connection noip.ddns.net -Count 1 -Quiet) { "ONLINE" } else { "OFFLINE" }

    "$pc1`n$pc2`n$pc3`n$pc4`n$pc5`n$pc6" | Out-File "$env:USERPROFILE\Documents\Rainmeter\network_status.txt" -Encoding ASCII

    Start-Sleep -Seconds 5
}