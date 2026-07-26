# LinkSpeed.ps1
# Obtem a velocidade da interface Ethernet fisica real (exclui adaptadores virtuais).

$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$outputFile = Join-Path $scriptPath "linkspeed.txt"

# Palavras-chave usadas para descartar adaptadores que NAO sao placas fisicas reais,
# mesmo que o Windows os classifique erroneamente como "fisicos".
$virtualKeywords = @(
    'Virtual', 'Hyper-V', 'VMware', 'VirtualBox', 'VPN', 'TAP',
    'Bluetooth', 'Loopback', 'Miniport', 'WAN Miniport', 'Tunnel',
    'Pseudo', 'Docker', 'Npcap', 'ExpressRoute', 'WSL'
)

try {

    # Busca todos os adaptadores fisicos ativos com padrao Ethernet (802.3)
    $candidatos = Get-NetAdapter -Physical |
        Where-Object {
            $_.Status -eq "Up" -and
            $_.HardwareInterface -eq $true -and
            $_.MediaType -eq "802.3" -and
            $_.ConnectorPresent -eq $true               # so placas com conector fisico real
        }

    # Remove qualquer coisa que combine com nomes/descricoes de adaptadores virtuais
    $adapter = $candidatos |
        Where-Object {
            $desc = "$($_.InterfaceDescription) $($_.Name)"
            -not ($virtualKeywords | Where-Object { $desc -match $_ })
        } |
        # Se sobrar mais de uma, prioriza a de maior velocidade real reportada
        Sort-Object -Property LinkSpeed -Descending |
        Select-Object -First 1

    if ($adapter) {
        # Achou Ethernet cabeada real -> usa ela
        $adapter.LinkSpeed | Out-File $outputFile -Encoding ASCII -Force
    }
    else {
        # Sem cabo -> tenta achar um adaptador Wi-Fi ativo como fallback
        $wifiAdapter = Get-NetAdapter -Physical |
            Where-Object {
                $_.Status -eq "Up" -and
                $_.MediaType -eq "Native 802.11"
            } |
            Sort-Object -Property LinkSpeed -Descending |
            Select-Object -First 1

        if ($wifiAdapter) {
            "$($wifiAdapter.LinkSpeed) (Wi-Fi)" | Out-File $outputFile -Encoding ASCII -Force
        }
        else {
            "No Network" | Out-File $outputFile -Encoding ASCII -Force
        }
    }

}
catch {
    "Unknown" | Out-File $outputFile -Encoding ASCII -Force
}
