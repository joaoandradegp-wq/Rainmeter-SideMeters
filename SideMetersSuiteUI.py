import tkinter as tk
from tkinter import ttk, messagebox

import configparser
import os
import re
import subprocess
import time
import urllib.request
import urllib.error
import webbrowser

DIALOG_WIDTH = 420
DIALOG_HEIGHT = 200

# ==========================================
# PATHS - ABA "SIDEMETERDEVICES" 
# ==========================================

INI_FILE = os.path.expanduser(r"~\Documents\Rainmeter\Scripts\devices.ini")
EXE_NAME = "SideMeterDevices.exe"

# ==================================================================
# PATHS - ABA "SEVASTOLINK"
# ==================================================================

SKINS_ROOT = os.path.expanduser(r"~\Documents\Rainmeter\Skins")
SKIN_DIR = os.path.join(SKINS_ROOT, "ServerMonitor")
SCRIPTS_DIR = os.path.join(SKIN_DIR, "Scripts")
RESOURCES_DIR = os.path.join(SKIN_DIR, "@Resources")

SKIN_INI_PATH = os.path.join(SKIN_DIR, "ServerMonitor.ini")
BAT_PATH = os.path.join(SCRIPTS_DIR, "start_api.bat")
VBS_PATH = os.path.join(SCRIPTS_DIR, "run_hidden.vbs")
PS1_PATH = os.path.join(SCRIPTS_DIR, "update_api.ps1")

RAINMETER_DOWNLOAD_URL = "https://www.rainmeter.net/"

# ==================================================================
# PATHS - NETWORK.ini
# ==================================================================

NETWORK_SKIN_DIR = os.path.join(SKINS_ROOT, "illustro", "Network")
NETWORK_INI_PATH = os.path.join(NETWORK_SKIN_DIR, "Network.ini")
LINKSPEED_PS1_PATH = os.path.join(NETWORK_SKIN_DIR, "LinkSpeed.ps1")
RUNLINKSPEED_VBS_PATH = os.path.join(NETWORK_SKIN_DIR, "RunLinkSpeed.vbs")

# Nome da config para o bang !ActivateConfig do Rainmeter, que espera o
# caminho relativo à pasta Skins (ex.: "illustro\Network").
NETWORK_SKIN_NAME = os.path.join("illustro", "Network")

# ==================================================================
# PATHS - SYSTEM.INI
# ==================================================================

SYSTEM_SKIN_DIR = os.path.join(SKINS_ROOT, "illustro", "System")
SYSTEM_INI_PATH = os.path.join(SYSTEM_SKIN_DIR, "System.ini")
SYSTEM_SKIN_NAME = os.path.join("illustro", "System")

# Campos que o ServerMonitor.ini le do api.txt.
# Servem para validar se o endereço digitado realmente devolve o formato que a skin espera antes de gravar qualquer arquivo.

CAMPOS_ESPERADOS_API = [
    "CPU_USAGE",
    "CPU_TEMP",
    "RAM_PERCENT",
    "SWAP_PERCENT",
    "DISK_PERCENT",
    "DISK_USED",
    "DISK_TOTAL",
    "LAN_IP",
    "DOWNLOAD",
    "UPLOAD",
]

# ------------------------------------------
# TEMPLATES ESTÁTICOS
# ------------------------------------------

START_API_BAT = r"""@echo off
wscript.exe "%~dp0run_hidden.vbs"
"""

RUN_HIDDEN_VBS = r'''' ----------------------------------------------------
' Abre o update_api.ps1 sem janelas visiveis.
' Usa WScript.Shell.Run com o parametro 0, que esconde a janela por completo.
' ----------------------------------------------------
Set fso = CreateObject("Scripting.FileSystemObject")
scriptFolder = fso.GetParentFolderName(WScript.ScriptFullName)

Set WshShell = CreateObject("WScript.Shell")
command = "powershell.exe -ExecutionPolicy Bypass -NoProfile -File """ & scriptFolder & "\update_api.ps1"""

WshShell.Run command, 0, False
'''

UPDATE_API_PS1_TEMPLATE = r"""# ----------------------------------------------------
# Antes de comecar, fecha qualquer instancia anterior
# desse mesmo script que ainda esteja rodando, entao
# so fica UM powershell ativo por vez.
# ----------------------------------------------------
$myPid = $PID

Get-CimInstance Win32_Process -Filter "Name = 'powershell.exe'" |
    Where-Object { $_.CommandLine -match 'update_api\.ps1' -and $_.ProcessId -ne $myPid } |
    ForEach-Object {
        try { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue } catch {}
    }

$url = "__URL__"
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
"""

SERVER_MONITOR_INI = r"""[Rainmeter]
Update=2000
AccurateText=1
DynamicWindowSize=1
BackgroundMode=2
SolidColor=0,0,0,1
OnRefreshAction=["#ROOTCONFIGPATH#Scripts\start_api.bat"]

[Variables]
FontName=Consolas
FontColor=0,255,120
DimColor=120,255,180
LineColor=0,255,120,50

; Layout base
ColLeftX=60
ColRightX=430
ColWidth=300
BarW=300
BarH=8


;=========================
; MEDIDAS
;=========================

[MeasureCPU]
Measure=Plugin
Plugin=WebParser
URL=file://#@#api.txt
ForceReload=1
UpdateRate=1
RegExp="(?si)CPU_USAGE=([0-9.]+)"
StringIndex=1
MinValue=0
MaxValue=100

[MeasureTemp]
Measure=Plugin
Plugin=WebParser
URL=file://#@#api.txt
ForceReload=1
UpdateRate=1
RegExp="(?si)CPU_TEMP=([0-9.]+)"
StringIndex=1

[MeasureRAM]
Measure=Plugin
Plugin=WebParser
URL=file://#@#api.txt
ForceReload=1
UpdateRate=1
RegExp="(?si)RAM_PERCENT=([0-9.]+)"
StringIndex=1
MinValue=0
MaxValue=100

[MeasureSwap]
Measure=Plugin
Plugin=WebParser
URL=file://#@#api.txt
ForceReload=1
UpdateRate=1
RegExp="(?si)SWAP_PERCENT=([0-9.]+)"
StringIndex=1

[MeasureDisk]
Measure=Plugin
Plugin=WebParser
URL=file://#@#api.txt
ForceReload=1
UpdateRate=1
RegExp="(?si)DISK_PERCENT=([0-9.]+)"
StringIndex=1
MinValue=0
MaxValue=100

[MeasureDiskUsed]
Measure=Plugin
Plugin=WebParser
URL=file://#@#api.txt
ForceReload=1
UpdateRate=1
RegExp="(?si)DISK_USED=([0-9.]+)"
StringIndex=1

[MeasureDiskTotal]
Measure=Plugin
Plugin=WebParser
URL=file://#@#api.txt
ForceReload=1
UpdateRate=1
RegExp="(?si)DISK_TOTAL=([0-9.]+)"
StringIndex=1

[MeasureIP]
Measure=Plugin
Plugin=WebParser
URL=file://#@#api.txt
ForceReload=1
UpdateRate=1
RegExp="(?si)IP=([0-9.]+)"
StringIndex=1

[MeasureDown]
Measure=Plugin
Plugin=WebParser
URL=file://#@#api.txt
ForceReload=1
UpdateRate=1
RegExp="(?si)DOWNLOAD=([0-9.]+)"
StringIndex=1

[MeasureUp]
Measure=Plugin
Plugin=WebParser
URL=file://#@#api.txt
ForceReload=1
UpdateRate=1
RegExp="(?si)UPLOAD=([0-9.]+)"
StringIndex=1


;=========================
; DIVISOR SUPERIOR
;=========================

[HeaderLine]
Meter=Shape
Shape=Rectangle 0,0,700,1 | Fill Color #LineColor# | StrokeWidth 0
X=40
Y=20


;=========================
; CPU (coluna esquerda)
;=========================

[CPU_Title]
Meter=String
Text=CPU
X=#ColLeftX#
Y=45
FontFace=#FontName#
FontSize=21
FontColor=#FontColor#
AntiAlias=1

[CPU_Value]
Meter=String
MeasureName=MeasureCPU
Text=%1%
X=(#ColLeftX#+#ColWidth#)
Y=45
W=#ColWidth#
StringAlign=Right
FontFace=#FontName#
FontSize=21
FontColor=#FontColor#
AntiAlias=1

[CPU_Bar]
Meter=Bar
MeasureName=MeasureCPU
X=#ColLeftX#
Y=82
W=#BarW#
H=6
BarOrientation=Horizontal
BarColor=0,255,120
SolidColor=30,60,45,50

[CPU_BarOutline]
Meter=Shape
Shape=Rectangle 0,0,#BarW#,6 | Fill Color 0,0,0,1 | StrokeWidth 1 | Stroke Color #LineColor#
X=#ColLeftX#
Y=82

[Temp]
Meter=String
MeasureName=MeasureTemp
Text=TEMP %1 C
X=#ColLeftX#
Y=104
FontFace=#FontName#
FontSize=16
FontColor=#DimColor#
AntiAlias=1


;=========================
; MEMORY (coluna direita)
;=========================

[Memory_Title]
Meter=String
Text=MEMORY
X=#ColRightX#
Y=45
FontFace=#FontName#
FontSize=21
FontColor=#FontColor#
AntiAlias=1

[RAM_Value]
Meter=String
MeasureName=MeasureRAM
Text=%1%
X=(#ColRightX#+#ColWidth#)
Y=45
W=#ColWidth#
StringAlign=Right
FontFace=#FontName#
FontSize=21
FontColor=#FontColor#
AntiAlias=1

[RAM_Bar]
Meter=Bar
MeasureName=MeasureRAM
X=#ColRightX#
Y=82
W=#BarW#
H=6
BarOrientation=Horizontal
BarColor=0,255,120
SolidColor=30,60,45,50

[RAM_BarOutline]
Meter=Shape
Shape=Rectangle 0,0,#BarW#,6 | Fill Color 0,0,0,1 | StrokeWidth 1 | Stroke Color #LineColor#
X=#ColRightX#
Y=82

[Swap]
Meter=String
MeasureName=MeasureSwap
Text=SWAP %1%
X=#ColRightX#
Y=104
FontFace=#FontName#
FontSize=16
FontColor=#DimColor#
AntiAlias=1

[MidLine]
Meter=Shape
Shape=Rectangle 0,0,700,1 | Fill Color #LineColor# | StrokeWidth 0
X=40
Y=140


;=========================
; STORAGE (coluna esquerda)
;=========================

[Storage_Title]
Meter=String
Text=STORAGE
X=#ColLeftX#
Y=165
FontFace=#FontName#
FontSize=21
FontColor=#FontColor#
AntiAlias=1

[Disk_Value]
Meter=String
MeasureName=MeasureDisk
Text=%1%
X=(#ColLeftX#+#ColWidth#)
Y=165
W=#ColWidth#
StringAlign=Right
FontFace=#FontName#
FontSize=21
FontColor=#FontColor#
AntiAlias=1

[Disk_Bar]
Meter=Bar
MeasureName=MeasureDisk
X=#ColLeftX#
Y=202
W=#BarW#
H=6
BarOrientation=Horizontal
BarColor=0,255,120
SolidColor=30,60,45,50

[Disk_BarOutline]
Meter=Shape
Shape=Rectangle 0,0,#BarW#,6 | Fill Color 0,0,0,1 | StrokeWidth 1 | Stroke Color #LineColor#
X=#ColLeftX#
Y=202

[Disk_Usage]
Meter=String
MeasureName=MeasureDiskUsed
MeasureName2=MeasureDiskTotal
Text=%1 / %2 GB
X=#ColLeftX#
Y=224
FontFace=#FontName#
FontSize=16
FontColor=#DimColor#
AntiAlias=1


;=========================
; NETWORK (coluna direita)
;=========================

[Network_Title]
Meter=String
Text=NETWORK
X=#ColRightX#
Y=165
FontFace=#FontName#
FontSize=21
FontColor=#FontColor#
AntiAlias=1

[IP]
Meter=String
MeasureName=MeasureIP
Text=%1
X=#ColRightX#
Y=202
FontFace=#FontName#
FontSize=16
FontColor=#DimColor#
AntiAlias=1

[Down]
Meter=String
MeasureName=MeasureDown
Text="DL %1 MB/s"
X=#ColRightX#
Y=228
FontFace=#FontName#
FontSize=17
FontColor=#FontColor#
AntiAlias=1

[Up]
Meter=String
MeasureName=MeasureUp
Text="UL %1 MB/s"
X=(#ColRightX#+150)
Y=228
FontFace=#FontName#
FontSize=17
FontColor=#FontColor#
AntiAlias=1

[FooterLine]
Meter=Shape
Shape=Rectangle 0,0,700,1 | Fill Color #LineColor# | StrokeWidth 0
X=40
Y=270

"""

# ------------------------------------------
# TEMPLATES - LINK SPEED
# ------------------------------------------

LINKSPEED_PS1_TEMPLATE = r"""# LinkSpeed.ps1
# Obtem a velocidade da interface Ethernet e WIFI fisica real e exclui adaptadores virtuais.

$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$outputFile = Join-Path $scriptPath "linkspeed.txt"

# Palavras-chave usadas para descartar adaptadores que NAO sao placas fisicas reais.
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
"""

RUNLINKSPEED_VBS_TEMPLATE = r'''Set objShell = CreateObject("Wscript.Shell")
objShell.Run "powershell.exe -ExecutionPolicy Bypass -File """ & Replace(WScript.ScriptFullName,"RunLinkSpeed.vbs","LinkSpeed.ps1") & """", 0, True
'''

NETWORK_INI_TEMPLATE = r"""; ----------------------------------
; NETWORK + LINK SPEED
; ----------------------------------

[Rainmeter]
Update=1000
Background=#@#Background.png
BackgroundMode=3
BackgroundMargins=0,34,0,14

OnRefreshAction=["wscript.exe" "#CURRENTPATH#RunLinkSpeed.vbs"]

[Metadata]
Name=Network
Author=poiru / ChatGPT
Information=Shows IP address, network activity and Ethernet Link Speed.
License=Creative Commons BY-NC-SA 3.0
Version=2.0

[Variables]
fontName=Trebuchet MS
textSize=8
colorBar=235,170,0,255
colorText=255,255,255,205

maxDownload=10485760
maxUpload=10485760

;================================================
; MEASURES
;================================================

[measureIP]
Measure=WebParser
URL=https://checkip.amazonaws.com/
UpdateRate=14400
RegExp=(?s)^(.*)$
StringIndex=1
Substitute="":"N/A"

[measureNetIn]
Measure=NetIn
NetInSpeed=#maxDownload#

[measureNetOut]
Measure=NetOut
NetOutSpeed=#maxUpload#

;================================================
; LINK SPEED
;================================================

[MeasureRun]
Measure=Calc
Formula=Counter % 60
IfEqualValue=0
IfEqualAction=["wscript.exe" "#CURRENTPATH#RunLinkSpeed.vbs"]

[MeasureLink]
Measure=Plugin
Plugin=WebParser
URL=file://#CURRENTPATH#linkspeed.txt
RegExp=(.*)
StringIndex=1
UpdateRate=5
DynamicVariables=1

;================================================
; STYLES
;================================================

[styleTitle]
StringAlign=Center
StringCase=Upper
StringStyle=Bold
StringEffect=Shadow
FontEffectColor=0,0,0,50
FontColor=#colorText#
FontFace=#fontName#
FontSize=10
AntiAlias=1
ClipString=1

[styleLeftText]
StringAlign=Left
StringCase=None
StringStyle=Bold
StringEffect=Shadow
FontEffectColor=0,0,0,20
FontColor=#colorText#
FontFace=#fontName#
FontSize=#textSize#
AntiAlias=1
ClipString=1

[styleRightText]
StringAlign=Right
StringCase=None
StringStyle=Bold
StringEffect=Shadow
FontEffectColor=0,0,0,20
FontColor=#colorText#
FontFace=#fontName#
FontSize=#textSize#
AntiAlias=1
ClipString=1

[styleBar]
BarColor=#colorBar#
BarOrientation=HORIZONTAL
SolidColor=255,255,255,15

[styleSeperator]
SolidColor=255,255,255,15

;================================================
; TITLE
;================================================

[meterTitle]
Meter=String
MeterStyle=styleTitle
X=100
Y=12
W=190
H=18
Text=Network

;================================================
; IP
;================================================

[meterIPLabel]
Meter=String
MeterStyle=styleLeftText
X=10
Y=40
W=190
H=14
Text=IP Address

[meterIPValue]
Meter=String
MeterStyle=styleRightText
MeasureName=measureIP
X=200
Y=0r
W=190
H=14
Text=%1

[meterSeperator]
Meter=Image
MeterStyle=styleSeperator
X=10
Y=52
W=190
H=1

;================================================
; UPLOAD
;================================================

[meterUploadLabel]
Meter=String
MeterStyle=styleLeftText
X=10
Y=60
W=190
H=14
Text=Upload

[meterUploadValue]
Meter=String
MeterStyle=styleRightText
MeasureName=measureNetOut
X=200
Y=0r
W=190
H=14
Text=%1B/s
NumOfDecimals=1
AutoScale=1

[meterUploadBar]
Meter=Bar
MeterStyle=styleBar
MeasureName=measureNetOut
X=10
Y=72
W=190
H=1

;================================================
; DOWNLOAD
;================================================

[meterDownloadLabel]
Meter=String
MeterStyle=styleLeftText
X=10
Y=80
W=190
H=14
Text=Download

[meterDownloadValue]
Meter=String
MeterStyle=styleRightText
MeasureName=measureNetIn
X=200
Y=0r
W=190
H=14
Text=%1B/s
NumOfDecimals=1
AutoScale=1

[meterDownloadBar]
Meter=Bar
MeterStyle=styleBar
MeasureName=measureNetIn
X=10
Y=92
W=190
H=1

;================================================
; LINK SPEED
;================================================

[meterLinkLabel]
Meter=String
MeterStyle=styleLeftText
X=10
Y=100
W=190
H=14
Text=Link Speed

[meterLinkValue]
Meter=String
MeterStyle=styleRightText
MeasureName=MeasureLink
X=200
Y=0r
W=190
H=14
Text=%1

[meterLinkSeparator]
Meter=Image
MeterStyle=styleSeperator
X=10
Y=112
W=190
H=1
"""

# ------------------------------------------
# TEMPLATE - SYSTEM.INI 
# ------------------------------------------

SYSTEM_INI_TEMPLATE = r"""[Rainmeter]
Update=1000
Background=#@#Background.png
BackgroundMode=3
BackgroundMargins=0,34,0,14

[Metadata]
Name=System
Author=poiru / ChatGPT
Information=Displays system information.
Version=2.0

[Variables]
fontName=Trebuchet MS
textSize=8
colorBar=235,170,0,255
colorText=255,255,255,205

;------------------------------------------------
; SYSTEM MEASURES
;------------------------------------------------

[measureCPU]
Measure=CPU
Processor=0

[measureRAM]
Measure=PhysicalMemory
UpdateDivider=20

[measureRAMPercent]
Measure=Calc
Formula=(measureRAM / measureRAMTotal) * 100
DynamicVariables=1

[measureRAMUsed]
Measure=Calc
Formula=(measureRAM/1024/1024/1024)
DynamicVariables=1

[measureRAMTotal]
Measure=PhysicalMemory
Total=1
UpdateDivider=20

[measureRAMTotalGB]
Measure=Calc
Formula=(measureRAMTotal/1024/1024/1024)
DynamicVariables=1

[measureRAMFree]
Measure=Calc
Formula=((measureRAMTotal-measureRAM)/1024/1024/1024)
DynamicVariables=1

;------------------------------------------------
; STYLES
;------------------------------------------------

[styleTitle]
StringAlign=Center
StringCase=Upper
StringStyle=Bold
StringEffect=Shadow
FontEffectColor=0,0,0,50
FontColor=#colorText#
FontFace=#fontName#
FontSize=10
AntiAlias=1
ClipString=1

[styleLeftText]
StringAlign=Left
StringStyle=Bold
StringEffect=Shadow
FontEffectColor=0,0,0,20
FontColor=#colorText#
FontFace=#fontName#
FontSize=#textSize#
AntiAlias=1
ClipString=1

[styleRightText]
StringAlign=Right
StringStyle=Bold
StringEffect=Shadow
FontEffectColor=0,0,0,20
FontColor=#colorText#
FontFace=#fontName#
FontSize=#textSize#
AntiAlias=1
ClipString=1

[styleBar]
BarColor=#colorBar#
BarOrientation=HORIZONTAL
SolidColor=255,255,255,15

[styleSeparator]
SolidColor=255,255,255,15

;------------------------------------------------
; TITLE
;------------------------------------------------

[meterTitle]
Meter=String
MeterStyle=styleTitle
X=100
Y=12
W=190
H=18
Text=SYSTEM
LeftMouseUpAction=["taskmgr.exe"]
ToolTipText=Open Task Manager

;------------------------------------------------
; CPU
;------------------------------------------------

[meterLabelCPU]
Meter=String
MeterStyle=styleLeftText
X=10
Y=40
W=190
H=14
Text=CPU Usage

[meterValueCPU]
Meter=String
MeterStyle=styleRightText
MeasureName=measureCPU
X=200
Y=0r
W=190
H=14
Text=%1%

[meterBarCPU]
Meter=Bar
MeterStyle=styleBar
MeasureName=measureCPU
X=10
Y=52
W=190
H=1

;------------------------------------------------
; RAM
;------------------------------------------------

[meterLabelRAM]
Meter=String
MeterStyle=styleLeftText
X=10
Y=60
W=190
H=14
Text=RAM

[meterValueRAM]
Meter=String
MeterStyle=styleRightText
MeasureName=measureRAMPercent
X=200
Y=0r
W=190
H=14
NumOfDecimals=0
Text=%1%

[meterBarRAM]
Meter=Bar
MeterStyle=styleBar
MeasureName=measureRAM
X=10
Y=72
W=190
H=1

;------------------------------------------------
; AVAILABLE RAM
;------------------------------------------------

[meterLabelFree]
Meter=String
MeterStyle=styleLeftText
X=10
Y=80
W=190
H=14
Text=Available

[meterValueFree]
Meter=String
MeterStyle=styleRightText
MeasureName=measureRAMFree
X=200
Y=0r
W=190
H=14
NumOfDecimals=1
Text=%1 GB

[meterBarFree]
Meter=Bar
MeterStyle=styleBar
MeasureName=measureRAM
InvertMeasure=1
X=10
Y=92
W=190
H=1

;------------------------------------------------
; BOTTOM SEPARATOR
;------------------------------------------------

[meterSeparator]
Meter=Image
MeterStyle=styleSeparator
X=10
Y=97
W=190
H=1
"""

# ==========================================
# HELPERS - ATIVAÇÃO DE SKINS NO RAINMETER
# ==========================================
# Compartilhados entre as abas "Status do Servidor" e "Rainmeter",
# já que ambas precisam localizar o Rainmeter.exe, garantir que ele
# esteja aberto e mandar o !ActivateConfig da skin correspondente.

def localizar_rainmeter():
    # Caminhos padrão onde o instalador do Rainmeter costuma colocar o exe.
    candidatos = [
        os.path.join(os.environ.get("ProgramFiles", r"C:\Program Files"), "Rainmeter", "Rainmeter.exe"),
        os.path.join(os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)"), "Rainmeter", "Rainmeter.exe"),
        os.path.join(os.environ.get("ProgramW6432", r"C:\Program Files"), "Rainmeter", "Rainmeter.exe"),
    ]

    for caminho in candidatos:
        if caminho and os.path.exists(caminho):
            return caminho

    return None


def rainmeter_esta_rodando():
    try:
        resultado = subprocess.run(
            ["tasklist", "/FI", "IMAGENAME eq Rainmeter.exe"],
            capture_output=True,
            text=True,
            timeout=5
        )
        return "Rainmeter.exe" in resultado.stdout

    except (OSError, subprocess.TimeoutExpired):
        # Se não der para checar, segue o fluxo normal e deixa o
        # !ActivateConfig tentar mesmo assim.
        return True


def ativar_skin_rainmeter(skin_name, ini_filename, status_var=None, status_label=None):
    """
    Ativa/atualiza uma skin no Rainmeter via linha de comando (bang
    !ActivateConfig), que carrega a skin se ela ainda não estiver
    ativa, ou recarrega se já estiver - equivalente a clicar em
    "Atualizar" na skin pelo próprio Rainmeter.

    Antes disso, confere se o Rainmeter está instalado (senão abre o
    site oficial para download) e se está aberto (senão abre o
    programa e aguarda antes de mandar o comando).
    """
    rainmeter_exe = localizar_rainmeter()

    if not rainmeter_exe:
        messagebox.showwarning(
            "Rainmeter não instalado",
            "Não encontrei o Rainmeter instalado neste computador.\n\n"
            "Os arquivos da skin já foram gerados. Vou abrir o site "
            "oficial para você baixar e instalar o Rainmeter."
        )
        webbrowser.open(RAINMETER_DOWNLOAD_URL)
        return False

    if not rainmeter_esta_rodando():

        try:
            subprocess.Popen([rainmeter_exe])

        except OSError as e:
            messagebox.showerror("Erro", f"Falha ao abrir o Rainmeter:\n{e}")
            return False

        if status_label is not None and status_var is not None:
            status_label.configure(foreground="#555555")
            status_var.set("Abrindo o Rainmeter...")
            root.update_idletasks()

        # dá tempo do Rainmeter terminar de iniciar antes de mandar o bang
        time.sleep(3)

    try:
        subprocess.Popen([rainmeter_exe, "!ActivateConfig", skin_name, ini_filename])
        return True

    except OSError as e:
        messagebox.showerror("Erro", f"Falha ao acionar o Rainmeter:\n{e}")
        return False


# ==========================================
# ROOT
# ==========================================

root = tk.Tk()

root.title("Side Meters Suite 1.4 - phobosfreeware.blogspot.com")
root.geometry("560x520")
root.minsize(560, 520)

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

aba_sidemeterdevices = ttk.Frame(notebook)
aba_sevastolink = ttk.Frame(notebook)
aba_rainmeter = ttk.Frame(notebook)

notebook.add(aba_sidemeterdevices, text="Status de Dispositivos")
notebook.add(aba_sevastolink, text="Status do Servidor")
notebook.add(aba_rainmeter, text="Rainmeter")


# ==========================================
# ABA 1 - SIDEMETERDEVICES 
# ==========================================

def montar_aba_sidemeterdevices(parent):

    header = ttk.Frame(parent, padding=10)
    header.pack(fill="x")

    title = ttk.Label(header, text="Dispositivos", font=("Segoe UI", 16, "bold"))
    title.pack(anchor="w")

    subtitle = ttk.Label(
        header,
        text="Gerenciamento de dispositivos monitorados pelo Rainmeter."
    )

    subtitle.pack(anchor="w")

    frame_table = ttk.Frame(parent, padding=10)
    frame_table.pack(fill="both", expand=True)

    columns = ("nome", "ip")

    tree = ttk.Treeview(frame_table, columns=columns, show="headings")

    tree.heading("nome", text="Dispositivo")
    tree.heading("ip", text="IP / Host / DDNS")

    tree.column("nome", width=220)
    tree.column("ip", width=250)

    scroll = ttk.Scrollbar(frame_table, orient="vertical", command=tree.yview)

    tree.configure(yscrollcommand=scroll.set)

    tree.pack(side="left", fill="both", expand=True)
    scroll.pack(side="right", fill="y")

    def carregar():

        tree.delete(*tree.get_children())

        if not os.path.exists(INI_FILE):
            return

        cfg = configparser.ConfigParser()
        cfg.read(INI_FILE, encoding="utf-8")

        for sec in cfg.sections():

            ip = cfg[sec].get("ip", "")

            tree.insert("", "end", values=(sec, ip))

    def adicionar():

        win = tk.Toplevel(root)

        win.title("Adicionar")

        largura = DIALOG_WIDTH
        altura = DIALOG_HEIGHT

        root.update_idletasks()

        x = root.winfo_x() + root.winfo_width() // 2 - largura // 2
        y = root.winfo_y() + root.winfo_height() // 2 - altura // 2

        win.geometry(f"{largura}x{altura}+{x}+{y}")

        win.resizable(False, False)

        win.transient(root)
        win.grab_set()

        frame = ttk.Frame(win, padding=20)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Nome do dispositivo:").pack(anchor="w")

        en_nome = ttk.Entry(frame)
        en_nome.pack(fill="x", pady=(5, 8))

        ttk.Label(frame, text="IP / Host / DDNS:").pack(anchor="w")

        en_ip = ttk.Entry(frame)
        en_ip.pack(fill="x", pady=(5, 8))

        btns = ttk.Frame(win)
        btns.pack(side="bottom", fill="x", padx=20, pady=12)

        def salvar():

            nome = en_nome.get().strip()
            ip = en_ip.get().strip()

            if not nome:

                messagebox.showwarning("Aviso", "Informe o nome")
                return

            if not ip:

                messagebox.showwarning("Aviso", "Informe IP ou host")
                return

            tree.insert("", "end", values=(nome, ip))

            win.destroy()

        ttk.Button(btns, text="Cancelar", command=win.destroy).pack(side="right")
        ttk.Button(btns, text="Salvar", command=salvar).pack(side="right", padx=5)

        en_nome.focus()

        win.bind("<Return>", lambda e: salvar())
        win.bind("<Escape>", lambda e: win.destroy())

    def editar():

        sel = tree.selection()

        if not sel:
            return

        item = sel[0]

        nome_old, ip_old = tree.item(item)["values"]

        win = tk.Toplevel(root)

        win.title("Editar")

        largura = DIALOG_WIDTH
        altura = DIALOG_HEIGHT

        root.update_idletasks()

        x = root.winfo_x() + root.winfo_width() // 2 - largura // 2
        y = root.winfo_y() + root.winfo_height() // 2 - altura // 2

        win.geometry(f"{largura}x{altura}+{x}+{y}")

        win.resizable(False, False)

        win.transient(root)
        win.grab_set()

        frame = ttk.Frame(win, padding=20)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Nome do dispositivo:").pack(anchor="w")

        en_nome = ttk.Entry(frame)
        en_nome.insert(0, nome_old)
        en_nome.pack(fill="x", pady=(5, 8))

        ttk.Label(frame, text="IP / Host / DDNS:").pack(anchor="w")

        en_ip = ttk.Entry(frame)
        en_ip.insert(0, ip_old)
        en_ip.pack(fill="x", pady=(5, 8))

        btns = ttk.Frame(win)
        btns.pack(side="bottom", fill="x", padx=20, pady=12)

        def salvar():

            tree.item(
                item,
                values=(
                    en_nome.get().strip(),
                    en_ip.get().strip()
                )
            )

            win.destroy()

        ttk.Button(btns, text="Cancelar", command=win.destroy).pack(side="right")
        ttk.Button(btns, text="Salvar", command=salvar).pack(side="right", padx=5)

        en_nome.focus()

        win.bind("<Return>", lambda e: salvar())
        win.bind("<Escape>", lambda e: win.destroy())

    def remover():

        sel = tree.selection()

        for item in sel:
            tree.delete(item)

    def salvar_ini():

        pasta = os.path.dirname(INI_FILE)

        os.makedirs(pasta, exist_ok=True)

        cfg = configparser.ConfigParser()

        for item in tree.get_children():

            nome, ip = tree.item(item)["values"]

            cfg[nome] = {"ip": ip}

        with open(INI_FILE, "w", encoding="utf-8") as f:
            cfg.write(f)

        messagebox.showinfo(
            "Aviso",
            "O Rainmeter irá reiniciar para que sua configuração tenha efeito!"
        )

    def atualizar():

        salvar_ini()

        exe_path = os.path.join(os.getcwd(), EXE_NAME)

        if not os.path.exists(exe_path):

            messagebox.showerror(
                "Erro",
                "SideMeterDevices.exe não encontrado."
            )

            return

        subprocess.Popen([exe_path])

    buttons = ttk.Frame(parent, padding=10)
    buttons.pack(fill="x")

    ttk.Button(buttons, text="Adicionar", command=adicionar).pack(side="left", padx=5)
    ttk.Button(buttons, text="Editar", command=editar).pack(side="left", padx=5)
    ttk.Button(buttons, text="Remover", command=remover).pack(side="left", padx=5)
    ttk.Button(buttons, text="Atualizar", command=atualizar).pack(side="right")

    carregar()


# ==========================================
# ABA 2 - SEVASTOLINK 
# ==========================================

def montar_aba_sevastolink(parent):

    header = ttk.Frame(parent, padding=10)
    header.pack(fill="x")

    title = ttk.Label(header, text="Monitoramento do Servidor", font=("Segoe UI", 16, "bold"))
    title.pack(anchor="w")

    subtitle = ttk.Label(
        header,
        text="Configura a skin SEVASTOLINK no Rainmeter, através dos dados disponibilizados pelo Servidor."
    )
    subtitle.pack(anchor="w")

    form = ttk.Frame(parent, padding=10)
    form.pack(fill="x")

    ttk.Label(form, text="Endereço do Servidor (IP/host e porta, ex: 192.168.100.121:8181):").pack(anchor="w")

    en_endereco = ttk.Entry(form)
    en_endereco.pack(fill="x", pady=(5, 10))

    info = ttk.Label(
        form,
        text=(
            "Arquivos gerados em:\n"
            f"  {SKIN_INI_PATH}\n"
            f"  {BAT_PATH}\n"
            f"  {VBS_PATH}\n"
            f"  {PS1_PATH}\n\n"
            f"Pasta de dados:\n {RESOURCES_DIR}"
        ),
        foreground="#555555",
        justify="left"
    )
    info.pack(anchor="w", pady=(0, 10))

    status_var = tk.StringVar(value="")
    status_label = ttk.Label(form, textvariable=status_var, foreground="#0a7d2c")
    status_label.pack(anchor="w")

    def montar_url(endereco_bruto):
        # remove protocolo e barra final, caso o usuário tenha digitado
        endereco = re.sub(r'^https?://', '', endereco_bruto.strip()).rstrip('/')
        return endereco, f"http://{endereco}/api/rainmeter"

    def testar_conexao(url, timeout=5):
        """
        Busca a URL informada e confere se o conteúdo devolvido tem o
        formato CHAVE=VALOR que o ServerMonitor.ini espera (CPU_USAGE=,
        RAM_PERCENT= etc). Retorna (ok, mensagem, campos_faltando).
        """
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Sevastolink/1.0"})

            with urllib.request.urlopen(req, timeout=timeout) as resp:
                corpo = resp.read().decode("utf-8", errors="replace")

        except urllib.error.HTTPError as e:
            return False, f"O servidor respondeu com erro HTTP {e.code}.", []

        except urllib.error.URLError as e:
            return False, f"Não foi possível conectar ao endereço ({e.reason}).", []

        except (OSError, ValueError) as e:
            return False, f"Não foi possível conectar ao endereço ({e}).", []

        encontrados = set(re.findall(r'([A-Z_]+)\s*=', corpo))
        faltando = [c for c in CAMPOS_ESPERADOS_API if c not in encontrados]

        if faltando:
            return True, "O servidor respondeu, mas faltam campos esperados: " + ", ".join(faltando), faltando

        return True, "O servidor respondeu com todos os campos esperados pela skin.", []

    def testar():

        endereco_bruto = en_endereco.get().strip()

        if not endereco_bruto:
            messagebox.showwarning("Aviso", "Informe o endereço do servidor")
            return

        _, url = montar_url(endereco_bruto)

        status_label.configure(foreground="#555555")
        status_var.set(f"Testando {url} ...")
        parent.update_idletasks()

        ok, msg, faltando = testar_conexao(url)

        if ok and not faltando:
            status_label.configure(foreground="#0a7d2c")
        elif ok:
            status_label.configure(foreground="#b8860b")
        else:
            status_label.configure(foreground="#c0392b")

        status_var.set(msg)

    def carregar_endereco_atual():
        # Se já existir um update_api.ps1 gerado antes, recupera o endereço
        # atual para preencher o campo (extrai host:porta da URL salva).
        if not os.path.exists(PS1_PATH):
            return

        try:
            with open(PS1_PATH, "r", encoding="utf-8") as f:
                conteudo = f.read()

            m = re.search(r'\$url\s*=\s*"http://([^/"]+)', conteudo)

            if m:
                en_endereco.delete(0, "end")
                en_endereco.insert(0, m.group(1))

        except OSError:
            pass

    def gerar():

        endereco_bruto = en_endereco.get().strip()

        if not endereco_bruto:
            messagebox.showwarning("Aviso", "Informe o endereço do servidor")
            return False

        endereco, url = montar_url(endereco_bruto)

        status_label.configure(foreground="#555555")
        status_var.set(f"Verificando {url} ...")
        parent.update_idletasks()

        ok, msg, faltando = testar_conexao(url)

        if not ok:

            prosseguir = messagebox.askyesno(
                "Servidor não respondeu",
                f"{msg}\n\n"
                "Isso normalmente significa que o endereço está errado ou "
                "o servidor da API ainda não está no ar.\n\n"
                "Deseja gravar os arquivos mesmo assim?"
            )

            if not prosseguir:
                status_label.configure(foreground="#c0392b")
                status_var.set(msg)
                return False

        elif faltando:

            prosseguir = messagebox.askyesno(
                "Formato de resposta inesperado",
                f"{msg}\n\n"
                "A skin usa esses campos para montar CPU, memória, disco e "
                "rede. Os medidores correspondentes podem ficar em branco.\n\n"
                "Deseja continuar mesmo assim?"
            )

            if not prosseguir:
                status_label.configure(foreground="#b8860b")
                status_var.set(msg)
                return False

        try:
            os.makedirs(SKIN_DIR, exist_ok=True)
            os.makedirs(SCRIPTS_DIR, exist_ok=True)
            os.makedirs(RESOURCES_DIR, exist_ok=True)

            with open(SKIN_INI_PATH, "w", encoding="utf-8") as f:
                f.write(SERVER_MONITOR_INI)

            with open(BAT_PATH, "w", encoding="utf-8") as f:
                f.write(START_API_BAT)

            with open(VBS_PATH, "w", encoding="utf-8") as f:
                f.write(RUN_HIDDEN_VBS)

            ps1_conteudo = UPDATE_API_PS1_TEMPLATE.replace("__URL__", url)

            with open(PS1_PATH, "w", encoding="utf-8") as f:
                f.write(ps1_conteudo)

        except OSError as e:
            messagebox.showerror("Erro", f"Falha ao gravar os arquivos:\n{e}")
            return False

        status_label.configure(foreground="#0a7d2c")
        status_var.set(f"Arquivos gerados com sucesso. API: {url}")

        messagebox.showinfo(
            "Aviso",
            "Skin SEVASTOLINK configurada.\n\n"
            "O Rainmeter irá reiniciar a skin \"ServerMonitor\" "
            "para que a nova configuração tenha efeito."
        )

        return True

    def atualizar():

        gerado = gerar()

        if not gerado:
            return

        # Dispara o start_api.bat para iniciar (ou reiniciar) a coleta de
        # dados em segundo plano, do mesmo jeito que o Rainmeter faria
        # via OnRefreshAction ao carregar a skin.
        if os.path.exists(BAT_PATH):
            try:
                subprocess.Popen(
                    [BAT_PATH],
                    cwd=SCRIPTS_DIR,
                    shell=True
                )
            except OSError as e:
                messagebox.showerror("Erro", f"Falha ao iniciar o script:\n{e}")

        # Ativa/recarrega a skin no Rainmeter, igual ao comportamento do botão Atualizar da aba SideMeterDevices.
        ativar_skin_rainmeter("ServerMonitor", "ServerMonitor.ini", status_var, status_label)

    buttons = ttk.Frame(parent, padding=10)
    buttons.pack(fill="x", side="bottom")

    ttk.Button(buttons, text="Atualizar", command=atualizar).pack(side="right")
    ttk.Button(buttons, text="Testar Conexão", command=testar).pack(side="right", padx=5)

    carregar_endereco_atual()


# ==========================================
# ABA 3 - RAINMETER (LINK SPEED)
# ==========================================

def montar_aba_rainmeter(parent):

    sub_notebook = ttk.Notebook(parent)
    sub_notebook.pack(fill="both", expand=True)

    sub_aba_network = ttk.Frame(sub_notebook)
    sub_aba_system = ttk.Frame(sub_notebook)

    sub_notebook.add(sub_aba_network, text="Network")
    sub_notebook.add(sub_aba_system, text="System")

    montar_subaba_network(sub_aba_network)
    montar_subaba_system(sub_aba_system)


# ------------------------------------------------------------
# SUB-ABA - NETWORK.ini
# ------------------------------------------------------------

def montar_subaba_network(parent):

    header = ttk.Frame(parent, padding=10)
    header.pack(fill="x")

    title = ttk.Label(header, text="Link Speed", font=("Segoe UI", 16, "bold"))
    title.pack(anchor="w")

    subtitle = ttk.Label(
        header,
        text="Adiciona o medidor de velocidade do link ao bloco \"Network\" já existente no Rainmeter."
    )
    subtitle.pack(anchor="w")

    form = ttk.Frame(parent, padding=10)
    form.pack(fill="both", expand=True)

    status_ini_var = tk.StringVar(value="")
    status_ini_label = ttk.Label(form, textvariable=status_ini_var, justify="left")
    status_ini_label.pack(anchor="w", pady=(0, 5))

    status_link_var = tk.StringVar(value="")
    status_link_label = ttk.Label(form, textvariable=status_link_var, justify="left")
    status_link_label.pack(anchor="w", pady=(0, 10))

    info = ttk.Label(
        form,
        text=(
            "Arquivos envolvidos:\n"
            f"  {NETWORK_INI_PATH}\n"
            f"  {LINKSPEED_PS1_PATH}\n"
            f"  {RUNLINKSPEED_VBS_PATH}"
        ),
        foreground="#555555",
        justify="left"
    )
    info.pack(anchor="w", pady=(0, 10))

    status_var = tk.StringVar(value="")
    status_label = ttk.Label(form, textvariable=status_var, foreground="#0a7d2c")
    status_label.pack(anchor="w")

    def link_speed_configurado():

        if not os.path.exists(NETWORK_INI_PATH):
            return False

        try:
            with open(NETWORK_INI_PATH, "r", encoding="utf-8") as f:
                conteudo = f.read()

        except OSError:
            return False

        return "MeasureLink" in conteudo

    def verificar_status():

        if os.path.exists(NETWORK_INI_PATH):
            status_ini_label.configure(foreground="#0a7d2c")
            status_ini_var.set(f"Network.ini original encontrado em:\n  {NETWORK_INI_PATH}")
        else:
            status_ini_label.configure(foreground="#c0392b")
            status_ini_var.set(
                "Network.ini original não encontrado.\n"
                f"  Esperado em: {NETWORK_INI_PATH}"
            )

        if link_speed_configurado():
            status_link_label.configure(foreground="#0a7d2c")
            status_link_var.set("Link Speed já está configurado neste bloco.")
            botao_adicionar.state(["disabled"])
            botao_atualizar.state(["disabled"])
        else:
            status_link_label.configure(foreground="#b8860b")
            status_link_var.set("Link Speed ainda não foi adicionado a este bloco.")
            botao_adicionar.state(["!disabled"])
            botao_atualizar.state(["!disabled"])

    def adicionar_link_speed():

        if not os.path.exists(NETWORK_INI_PATH):

            messagebox.showwarning(
                "Aviso",
                "O Network.ini original não foi encontrado.\n\n"
                f"Esperado em:\n{NETWORK_INI_PATH}\n\n"
                "Instale/carregue o bloco \"Network\" do Rainmeter antes de continuar."
            )
            return

        if link_speed_configurado():

            prosseguir = messagebox.askyesno(
                "Link Speed já configurado",
                "O Link Speed já parece estar configurado neste bloco.\n\n"
                "Deseja sobrescrever o Network.ini e os scripts mesmo assim?"
            )

            if not prosseguir:
                return

        else:

            prosseguir = messagebox.askyesno(
                "Adicionar Link Speed",
                "Isso vai sobrescrever o Network.ini atual por uma versão que "
                "já inclui o medidor de Link Speed, e criar os scripts "
                "LinkSpeed.ps1 e RunLinkSpeed.vbs na mesma pasta.\n\n"
                "Deseja continuar?"
            )

            if not prosseguir:
                return

        try:
            os.makedirs(NETWORK_SKIN_DIR, exist_ok=True)

            with open(NETWORK_INI_PATH, "w", encoding="utf-8") as f:
                f.write(NETWORK_INI_TEMPLATE)

            with open(LINKSPEED_PS1_PATH, "w", encoding="utf-8") as f:
                f.write(LINKSPEED_PS1_TEMPLATE)

            with open(RUNLINKSPEED_VBS_PATH, "w", encoding="utf-8") as f:
                f.write(RUNLINKSPEED_VBS_TEMPLATE)

        except OSError as e:
            messagebox.showerror("Erro", f"Falha ao gravar os arquivos:\n{e}")
            return

        status_label.configure(foreground="#0a7d2c")
        status_var.set("Link Speed adicionado com sucesso ao Network.ini.")

        verificar_status()

        messagebox.showinfo(
            "Aviso",
            "Link Speed configurado na skin \"Network\".\n\n"
            "O Rainmeter irá reiniciar para que a nova configuração tenha efeito."
        )

    def atualizar():
        ativar_skin_rainmeter(NETWORK_SKIN_NAME, "Network.ini", status_var, status_label)

    buttons = ttk.Frame(parent, padding=10)
    buttons.pack(fill="x", side="bottom")

    botao_atualizar = ttk.Button(buttons, text="Atualizar", command=atualizar)
    botao_atualizar.pack(side="right")

    botao_adicionar = ttk.Button(buttons, text="Adicionar", command=adicionar_link_speed)
    botao_adicionar.pack(side="right", padx=5)

    verificar_status()


# ------------------------------------------------------------
# SUB-ABA - SYSTEM.INI
# ------------------------------------------------------------

def montar_subaba_system(parent):

    header_sistema = ttk.Frame(parent, padding=10)
    header_sistema.pack(fill="x")

    ttk.Label(header_sistema, text="System CPU/RAM Update", font=("Segoe UI", 16, "bold")).pack(anchor="w")

    ttk.Label(
        header_sistema,
        text="Aplica uma configuração atualizada de CPU/RAM no bloco \"System\" já existente no Rainmeter."
    ).pack(anchor="w")

    form_sistema = ttk.Frame(parent, padding=10)
    form_sistema.pack(fill="both", expand=True)

    status_sistema_ini_var = tk.StringVar(value="")
    status_sistema_ini_label = ttk.Label(form_sistema, textvariable=status_sistema_ini_var, justify="left")
    status_sistema_ini_label.pack(anchor="w", pady=(0, 5))

    status_sistema_config_var = tk.StringVar(value="")
    status_sistema_config_label = ttk.Label(form_sistema, textvariable=status_sistema_config_var, justify="left")
    status_sistema_config_label.pack(anchor="w", pady=(0, 10))

    info_sistema = ttk.Label(
        form_sistema,
        text=f"Arquivo:\n  {SYSTEM_INI_PATH}",
        foreground="#555555",
        justify="left"
    )
    info_sistema.pack(anchor="w", pady=(0, 10))

    status_sistema_var = tk.StringVar(value="")
    status_sistema_label = ttk.Label(form_sistema, textvariable=status_sistema_var, foreground="#0a7d2c")
    status_sistema_label.pack(anchor="w")

    def sistema_configurado():

        if not os.path.exists(SYSTEM_INI_PATH):
            return False

        try:
            with open(SYSTEM_INI_PATH, "r", encoding="utf-8") as f:
                conteudo = f.read()

        except OSError:
            return False

        return "measureRAMTotalGB" in conteudo

    def verificar_status_sistema():

        if os.path.exists(SYSTEM_INI_PATH):
            status_sistema_ini_label.configure(foreground="#0a7d2c")
            status_sistema_ini_var.set(f"System.ini original encontrado em:\n  {SYSTEM_INI_PATH}")
        else:
            status_sistema_ini_label.configure(foreground="#c0392b")
            status_sistema_ini_var.set(
                "System.ini original não encontrado.\n"
                f"  Esperado em: {SYSTEM_INI_PATH}"
            )

        if sistema_configurado():
            status_sistema_config_label.configure(foreground="#0a7d2c")
            status_sistema_config_var.set("A atualização já está configurada.")
            botao_aplicar_sistema.state(["disabled"])
            botao_atualizar_sistema.state(["disabled"])
        else:
            status_sistema_config_label.configure(foreground="#b8860b")
            status_sistema_config_var.set("O bloco ainda não está configurado.")
            botao_aplicar_sistema.state(["!disabled"])
            botao_atualizar_sistema.state(["!disabled"])

    def aplicar_system_ini():

        if not os.path.exists(SYSTEM_INI_PATH):

            messagebox.showwarning(
                "Aviso",
                "O System.ini original não foi encontrado.\n\n"
                f"Esperado em:\n{SYSTEM_INI_PATH}\n\n"
                "Instale/carregue o bloco \"System\" do Rainmeter antes de continuar."
            )
            return

        if sistema_configurado():

            messagebox.showinfo(
                "Aviso",
                "O System.ini já está configurado. Nenhuma alteração foi necessária."
            )
            return

        prosseguir = messagebox.askyesno(
            "Aplicar System.ini",
            "Isso vai sobrescrever o System.ini atual pela versão configurada "
            "(CPU, RAM, total e disponível em GB).\n\n"
            "Deseja continuar?"
        )

        if not prosseguir:
            return

        try:
            os.makedirs(SYSTEM_SKIN_DIR, exist_ok=True)

            with open(SYSTEM_INI_PATH, "w", encoding="utf-8") as f:
                f.write(SYSTEM_INI_TEMPLATE)

        except OSError as e:
            messagebox.showerror("Erro", f"Falha ao gravar o arquivo:\n{e}")
            return

        status_sistema_label.configure(foreground="#0a7d2c")
        status_sistema_var.set("Atualização configurada com sucesso.")

        verificar_status_sistema()

        messagebox.showinfo(
            "Aviso",
            "Bloco \"System\" configurado.\n\n"
            "O Rainmeter irá reiniciar (ou carregar) o bloco para que a "
            "nova configuração tenha efeito."
        )

        ativar_skin_rainmeter(SYSTEM_SKIN_NAME, "System.ini", status_sistema_var, status_sistema_label)

    def atualizar_sistema():
        ativar_skin_rainmeter(SYSTEM_SKIN_NAME, "System.ini", status_sistema_var, status_sistema_label)

    buttons_sistema = ttk.Frame(parent, padding=10)
    buttons_sistema.pack(fill="x", side="bottom")

    botao_atualizar_sistema = ttk.Button(buttons_sistema, text="Atualizar", command=atualizar_sistema)
    botao_atualizar_sistema.pack(side="right")

    botao_aplicar_sistema = ttk.Button(buttons_sistema, text="Adicionar", command=aplicar_system_ini)
    botao_aplicar_sistema.pack(side="right", padx=5)

    verificar_status_sistema()


montar_aba_sidemeterdevices(aba_sidemeterdevices)
montar_aba_sevastolink(aba_sevastolink)
montar_aba_rainmeter(aba_rainmeter)

# ==========================================
# START
# ==========================================

root.mainloop()
