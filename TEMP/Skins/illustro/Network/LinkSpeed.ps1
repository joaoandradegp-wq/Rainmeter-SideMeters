# LinkSpeed.ps1
# Obtém a velocidade do link do adaptador de rede ativo
# e grava em linkspeed.txt para o Rainmeter.

try {
    $scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
    $outputFile = Join-Path $scriptPath "linkspeed.txt"

    # Procura adaptadores ativos
    $adapter = Get-NetAdapter |
        Where-Object { $_.Status -eq "Up" -and $_.LinkSpeed } |
        Sort-Object LinkSpeed -Descending |
        Select-Object -First 1

    if ($adapter) {
        $adapter.LinkSpeed | Out-File -FilePath $outputFile -Encoding ascii -Force
    }
    else {
        "Disconnected" | Out-File -FilePath $outputFile -Encoding ascii -Force
    }
}
catch {
    "Unknown" | Out-File -FilePath $outputFile -Encoding ascii -Force
}