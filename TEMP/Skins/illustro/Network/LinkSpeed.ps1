# LinkSpeed.ps1
# Obtém a velocidade da interface Ethernet física.

$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$outputFile = Join-Path $scriptPath "linkspeed.txt"

try {

    # Procura adaptadores Ethernet físicos ativos
    $adapter = Get-NetAdapter -Physical |
        Where-Object {
            $_.Status -eq "Up" -and
            $_.HardwareInterface -eq $true -and
            $_.MediaType -eq "802.3"
        } |
        Select-Object -First 1

    if ($adapter) {
        $adapter.LinkSpeed | Out-File $outputFile -Encoding ASCII -Force
    }
    else {
        "No Ethernet" | Out-File $outputFile -Encoding ASCII -Force
    }

}
catch {
    "Unknown" | Out-File $outputFile -Encoding ASCII -Force
}