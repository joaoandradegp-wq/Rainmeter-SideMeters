import tkinter as tk
from tkinter import ttk, messagebox

import configparser
import ctypes
import glob
import os
import re
import shutil
import subprocess
import threading
import time
import urllib.request
import urllib.error
import webbrowser
import xml.etree.ElementTree as ET

DIALOG_WIDTH = 420
DIALOG_HEIGHT = 250


def detectar_portugues_brasil():
    try:
        return ctypes.windll.kernel32.GetUserDefaultUILanguage() == 0x0416
    except Exception:
        return False


IDIOMA_PT = detectar_portugues_brasil()


def tr(pt, en):
    return pt if IDIOMA_PT else en


INI_FILE = os.path.expanduser(r"~\Documents\Rainmeter\Scripts\devices.ini")
EXE_NAME = "SideMeterDevices.exe"


SKINS_ROOT = os.path.expanduser(r"~\Documents\Rainmeter\Skins")
SKIN_DIR = os.path.join(SKINS_ROOT, "ServerMonitor")
SCRIPTS_DIR = os.path.join(SKIN_DIR, "Scripts")
RESOURCES_DIR = os.path.join(SKIN_DIR, "@Resources")

SKIN_INI_PATH = os.path.join(SKIN_DIR, "ServerMonitor.ini")
BAT_PATH = os.path.join(SCRIPTS_DIR, "start_api.bat")
VBS_PATH = os.path.join(SCRIPTS_DIR, "run_hidden.vbs")
PS1_PATH = os.path.join(SCRIPTS_DIR, "update_api.ps1")

RAINMETER_DOWNLOAD_URL = "https://www.rainmeter.net/"


NETWORK_SKIN_DIR = os.path.join(SKINS_ROOT, "illustro", "Network")
NETWORK_INI_PATH = os.path.join(NETWORK_SKIN_DIR, "Network.ini")
LINKSPEED_PS1_PATH = os.path.join(NETWORK_SKIN_DIR, "LinkSpeed.ps1")
RUNLINKSPEED_VBS_PATH = os.path.join(NETWORK_SKIN_DIR, "RunLinkSpeed.vbs")

NETWORK_SKIN_NAME = os.path.join("illustro", "Network")


SYSTEM_SKIN_DIR = os.path.join(SKINS_ROOT, "illustro", "System")
SYSTEM_INI_PATH = os.path.join(SYSTEM_SKIN_DIR, "System.ini")
SYSTEM_SKIN_NAME = os.path.join("illustro", "System")

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


START_API_BAT = r"""@echo off
wscript.exe "%~dp0run_hidden.vbs"
"""

RUN_HIDDEN_VBS = r'''Set fso = CreateObject("Scripting.FileSystemObject")
scriptFolder = fso.GetParentFolderName(WScript.ScriptFullName)

Set WshShell = CreateObject("WScript.Shell")
command = "powershell.exe -ExecutionPolicy Bypass -NoProfile -File """ & scriptFolder & "\update_api.ps1"""

WshShell.Run command, 0, False
'''

UPDATE_API_PS1_TEMPLATE = r"""$myPid = $PID

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

ColLeftX=60
ColRightX=430
ColWidth=300
BarW=300
BarH=8

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

[HeaderLine]
Meter=Shape
Shape=Rectangle 0,0,700,1 | Fill Color #LineColor# | StrokeWidth 0
X=40
Y=20

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


LINKSPEED_PS1_TEMPLATE = r"""$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$outputFile = Join-Path $scriptPath "linkspeed.txt"

$virtualKeywords = @(
    'Virtual', 'Hyper-V', 'VMware', 'VirtualBox', 'VPN', 'TAP',
    'Bluetooth', 'Loopback', 'Miniport', 'WAN Miniport', 'Tunnel',
    'Pseudo', 'Docker', 'Npcap', 'ExpressRoute', 'WSL'
)

try {
    $candidatos = Get-NetAdapter -Physical |
        Where-Object {
            $_.Status -eq "Up" -and
            $_.HardwareInterface -eq $true -and
            $_.MediaType -eq "802.3" -and
            $_.ConnectorPresent -eq $true
        }

    $adapter = $candidatos |
        Where-Object {
            $desc = "$($_.InterfaceDescription) $($_.Name)"
            -not ($virtualKeywords | Where-Object { $desc -match $_ })
        } |
        Sort-Object -Property LinkSpeed -Descending |
        Select-Object -First 1

    if ($adapter) {
        $adapter.LinkSpeed | Out-File $outputFile -Encoding ASCII -Force
    }
    else {
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

NETWORK_INI_TEMPLATE = r"""[Rainmeter]
Update=1000
Background=#@#Background.png
AccurateText=1
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
fontName=Segoe UI Variable Text
textSize=8
colorBar=235,170,0,255
colorText=255,255,255,205

maxDownload=10485760
maxUpload=10485760

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

[styleTitle]
StringAlign=Center
StringCase=Upper
StringStyle=Bold
StringEffect=None
FontColor=#colorText#
FontFace=#fontName#
FontSize=10
AntiAlias=1
ClipString=1

[styleLeftText]
StringAlign=Left
StringCase=None
StringStyle=Bold
StringEffect=None
FontColor=#colorText#
FontFace=#fontName#
FontSize=#textSize#
AntiAlias=1
ClipString=1

[styleRightText]
StringAlign=Right
StringCase=None
StringStyle=Bold
StringEffect=None
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

[meterTitle]
Meter=String
MeterStyle=styleTitle
X=100
Y=12
W=190
H=18
Text=Network

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
Y=55
W=190
H=1

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
Y=75
W=190
H=1

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
Y=95
W=190
H=1

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
Y=115
W=190
H=1
"""


SYSTEM_INI_TEMPLATE = r"""[Rainmeter]
Update=1000
Background=#@#Background.png
AccurateText=1
BackgroundMode=3
BackgroundMargins=0,34,0,14

[Metadata]
Name=System
Author=poiru / ChatGPT
Information=Displays system information.
Version=2.0

[Variables]
fontName=Segoe UI Variable Text
textSize=8
colorBar=235,170,0,255
colorText=255,255,255,205

colorGood=90,200,90,255
colorWarn=235,200,0,255
colorHot=230,60,60,255

cpuWarn=60
cpuHot=75
gpuWarn=65
gpuHot=80

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

[measureCPUWeb]
Measure=WebParser
URL=http://localhost:8085/data.json
UpdateRate=2
RegExp=(?s)"Text":"CPU Package"[^}]*?"Value":"(\d+)[^"]*C"

[measureCPUTemp]
Measure=WebParser
URL=[measureCPUWeb]
StringIndex=1
IfConditionMode=1
IfCondition=(measureCPUTemp < 1)
IfTrueAction=[!SetOption meterValueCPUTemp FontColor "#colorText#"][!UpdateMeter meterValueCPUTemp][!Redraw]
IfCondition2=(measureCPUTemp >= 1) && (measureCPUTemp < #cpuWarn#)
IfTrueAction2=[!SetOption meterValueCPUTemp FontColor "#colorGood#"][!UpdateMeter meterValueCPUTemp][!Redraw]
IfCondition3=(measureCPUTemp >= #cpuWarn#) && (measureCPUTemp < #cpuHot#)
IfTrueAction3=[!SetOption meterValueCPUTemp FontColor "#colorWarn#"][!UpdateMeter meterValueCPUTemp][!Redraw]
IfCondition4=(measureCPUTemp >= #cpuHot#)
IfTrueAction4=[!SetOption meterValueCPUTemp FontColor "#colorHot#"][!UpdateMeter meterValueCPUTemp][!Redraw]

[measureCPUNameWeb]
Measure=WebParser
URL=http://localhost:8085/data.json
UpdateRate=60
RegExp=(?s)"Text":"([^"]+)"[^}]*?"HardwareId":"/(?:intel|amd)cpu/[^"]*"

[measureCPUName]
Measure=WebParser
URL=[measureCPUNameWeb]
StringIndex=1

[measureGPUWeb]
Measure=WebParser
URL=http://localhost:8085/data.json
UpdateRate=2
RegExp=(?s)"Text":"GPU Core"[^}]*?"Value":"(\d+)[^"]*C"

[measureGPUTemp]
Measure=WebParser
URL=[measureGPUWeb]
StringIndex=1
IfConditionMode=1
IfCondition=(measureGPUTemp < 1)
IfTrueAction=[!SetOption meterValueGPUTemp FontColor "#colorText#"][!UpdateMeter meterValueGPUTemp][!Redraw]
IfCondition2=(measureGPUTemp >= 1) && (measureGPUTemp < #gpuWarn#)
IfTrueAction2=[!SetOption meterValueGPUTemp FontColor "#colorGood#"][!UpdateMeter meterValueGPUTemp][!Redraw]
IfCondition3=(measureGPUTemp >= #gpuWarn#) && (measureGPUTemp < #gpuHot#)
IfTrueAction3=[!SetOption meterValueGPUTemp FontColor "#colorWarn#"][!UpdateMeter meterValueGPUTemp][!Redraw]
IfCondition4=(measureGPUTemp >= #gpuHot#)
IfTrueAction4=[!SetOption meterValueGPUTemp FontColor "#colorHot#"][!UpdateMeter meterValueGPUTemp][!Redraw]

[measureGPUNameWeb]
Measure=WebParser
URL=http://localhost:8085/data.json
UpdateRate=60
RegExp=(?s)"Text":"([^"]+)"[^}]*?"HardwareId":"/gpu-[^"]*"

[measureGPUName]
Measure=WebParser
URL=[measureGPUNameWeb]
StringIndex=1
Substitute="NVIDIA GeForce ":""

[styleTitle]
StringAlign=Center
StringCase=Upper
StringStyle=Bold
StringEffect=None
FontColor=#colorText#
FontFace=#fontName#
FontSize=10
AntiAlias=1
ClipString=1

[styleLeftText]
StringAlign=Left
StringStyle=Bold
StringEffect=None
FontColor=#colorText#
FontFace=#fontName#
FontSize=#textSize#
AntiAlias=1
ClipString=1

[styleRightText]
StringAlign=Right
StringStyle=Bold
StringEffect=None
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

[meterLabelCPUTemp]
Meter=String
MeterStyle=styleLeftText
MeasureName=measureCPUName
X=10
Y=40
W=190
H=14
Text=%1

[meterValueCPUTemp]
Meter=String
MeterStyle=styleRightText
MeasureName=measureCPUTemp
X=200
Y=0r
W=190
H=14
NumOfDecimals=0
Text=%1°C

[meterLabelCPU]
Meter=String
MeterStyle=styleLeftText
X=10
Y=60
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
Y=75
W=190
H=1

[meterLabelRAM]
Meter=String
MeterStyle=styleLeftText
X=10
Y=80
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
Y=95
W=190
H=1

[meterLabelFree]
Meter=String
MeterStyle=styleLeftText
X=10
Y=100
W=190
H=14
Text=RAM Available

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
Y=115
W=190
H=1

[meterLabelGPUTemp]
Meter=String
MeterStyle=styleLeftText
MeasureName=measureGPUName
X=10
Y=120
W=190
H=14
Text=%1

[meterValueGPUTemp]
Meter=String
MeterStyle=styleRightText
MeasureName=measureGPUTemp
X=200
Y=0r
W=190
H=14
Text=%1°C

[meterSeparator]
Meter=Image
MeterStyle=styleSeparator
X=10
Y=137
W=190
H=1
"""


def ler_texto(caminho):
    with open(caminho, "rb") as f:
        dados = f.read()

    if dados.startswith((b"\xff\xfe", b"\xfe\xff")):
        return dados.decode("utf-16")

    if dados.startswith(b"\xef\xbb\xbf"):
        return dados.decode("utf-8-sig")

    try:
        return dados.decode("utf-8")
    except UnicodeDecodeError:
        return dados.decode("cp1252", errors="replace")


def localizar_rainmeter():
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
        return True


def ativar_skin_rainmeter(skin_name, ini_filename, status_var=None, status_label=None):
    rainmeter_exe = localizar_rainmeter()

    if not rainmeter_exe:
        messagebox.showwarning(
            tr("Rainmeter não instalado", "Rainmeter not installed"),
            tr(
                "Não encontrei o Rainmeter instalado neste computador.\n\n"
                "Os arquivos do bloco já foram gerados. Vou abrir o site "
                "oficial para você baixar e instalar o Rainmeter.",
                "I could not find Rainmeter installed on this computer.\n\n"
                "The block files have already been generated. I will open the "
                "official website so you can download and install Rainmeter."
            )
        )
        webbrowser.open(RAINMETER_DOWNLOAD_URL)
        return False

    if not rainmeter_esta_rodando():
        try:
            subprocess.Popen([rainmeter_exe])

        except OSError as e:
            messagebox.showerror(tr("Erro", "Error"), tr(f"Falha ao abrir o Rainmeter:\n{e}", f"Failed to open Rainmeter:\n{e}"))
            return False

        if status_label is not None and status_var is not None:
            status_label.configure(foreground="#555555")
            status_var.set(tr("Abrindo o Rainmeter...", "Opening Rainmeter..."))
            root.update_idletasks()

        time.sleep(3)

    try:
        subprocess.Popen([rainmeter_exe, "!ActivateConfig", skin_name, ini_filename])
        subprocess.Popen([rainmeter_exe, "!Refresh", skin_name])
        return True

    except OSError as e:
        messagebox.showerror(tr("Erro", "Error"), tr(f"Falha ao acionar o Rainmeter:\n{e}", f"Failed to trigger Rainmeter:\n{e}"))
        return False


LHM_WINGET_ID = "LibreHardwareMonitor.LibreHardwareMonitor"
LHM_URL = "http://localhost:8085/data.json"

ATUALIZADORES_UI = []


def localizar_lhm():
    candidatos = []

    local = os.environ.get("LOCALAPPDATA", "")

    if local:
        candidatos += glob.glob(os.path.join(
            glob.escape(local), "Microsoft", "WinGet", "Packages",
            "LibreHardwareMonitor.LibreHardwareMonitor_*", "LibreHardwareMonitor.exe"
        ))

    for var in ("ProgramFiles", "ProgramFiles(x86)"):
        base = os.environ.get(var)

        if base:
            candidatos.append(os.path.join(base, "LibreHardwareMonitor", "LibreHardwareMonitor.exe"))

    alias = shutil.which("LibreHardwareMonitor")

    if alias:
        candidatos.append(os.path.realpath(alias))

    for caminho in candidatos:
        if os.path.exists(caminho):
            return caminho

    return None


def lhm_esta_rodando():
    try:
        resultado = subprocess.run(
            ["tasklist", "/FI", "IMAGENAME eq LibreHardwareMonitor.exe"],
            capture_output=True,
            text=True,
            timeout=5,
            creationflags=0x08000000
        )
        return "LibreHardwareMonitor.exe" in resultado.stdout

    except (OSError, subprocess.TimeoutExpired):
        return False


def lhm_servidor_ativo():
    try:
        with urllib.request.urlopen(LHM_URL, timeout=2) as resposta:
            return resposta.status == 200

    except (OSError, urllib.error.URLError, ValueError):
        return False


def habilitar_webserver_lhm(exe):
    config_path = os.path.join(os.path.dirname(exe), "LibreHardwareMonitor.config")

    try:
        arvore = ET.parse(config_path)
        raiz = arvore.getroot()

    except (OSError, ET.ParseError):
        raiz = ET.Element("configuration")
        arvore = ET.ElementTree(raiz)

    app_settings = raiz.find("appSettings")

    if app_settings is None:
        app_settings = ET.SubElement(raiz, "appSettings")

    valores = {
        "runWebServerMenuItem": "true",
        "listenerPort": "8085",
        "startMinMenuItem": "true",
        "minTrayMenuItem": "true",
        "minCloseMenuItem": "true",
    }

    for chave, valor in valores.items():
        for item in app_settings.findall("add"):
            if item.get("key") == chave:
                item.set("value", valor)
                break
        else:
            ET.SubElement(app_settings, "add", {"key": chave, "value": valor})

    arvore.write(config_path, encoding="utf-8", xml_declaration=True)


LHM_TASK_NAME = "Libre Hardware Monitor"


def registrar_lhm_na_inicializacao(exe):
    params = (
        f'/Create /TN "{LHM_TASK_NAME}" '
        f'/TR "\\"{exe}\\"" /SC ONLOGON /RL HIGHEST /F'
    )
    resultado = ctypes.windll.shell32.ShellExecuteW(
        None, "runas", "schtasks", params, None, 0
    )
    return resultado > 32


def abrir_lhm_como_admin(exe):
    resultado = ctypes.windll.shell32.ShellExecuteW(
        None, "runas", exe, None, os.path.dirname(exe), 1
    )
    return resultado > 32


root = tk.Tk()

root.title("Side Meters Suite 1.5 - phobosfreeware.blogspot.com")
root.geometry("560x455")
root.minsize(560, 455)

barra_inferior = ttk.Frame(root, padding=(8, 4))
barra_inferior.pack(side="bottom", fill="x")

botao_reset = ttk.Button(barra_inferior, text=tr(
    "Redefinir Tudo",
    "Reset All"
), command=lambda: resetar_tudo())
botao_reset.pack(side="right")

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

aba_sidemeterdevices = ttk.Frame(notebook)
aba_apimonitor = ttk.Frame(notebook)
aba_rainmeter = ttk.Frame(notebook)

notebook.add(aba_sidemeterdevices, text=tr("Status de Dispositivos", "Devices Status"))
notebook.add(aba_apimonitor, text=tr("Status do Servidor", "Server Status"))
notebook.add(aba_rainmeter, text="Rainmeter")


def montar_aba_sidemeterdevices(parent):
    header = ttk.Frame(parent, padding=10)
    header.pack(fill="x")

    title = ttk.Label(header, text=tr("Dispositivos", "Devices"), font=("Segoe UI", 16, "bold"))
    title.pack(anchor="w")

    subtitle = ttk.Label(
        header,
        text=tr(
            "Gerenciamento de dispositivos monitorados pelo Rainmeter.",
            "Management of the devices monitored by Rainmeter."
        )
    )

    subtitle.pack(anchor="w")

    frame_table = ttk.Frame(parent, padding=10)
    frame_table.pack(fill="both", expand=True)

    columns = ("nome", "ip")

    tree = ttk.Treeview(frame_table, columns=columns, show="headings")

    tree.heading("nome", text=tr("Dispositivo", "Device"))
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

        win.title(tr("Adicionar", "Add"))

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

        ttk.Label(frame, text=tr("Nome do dispositivo:", "Device name:")).pack(anchor="w")

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
                messagebox.showwarning(tr("Aviso", "Notice"), tr("Informe o nome", "Enter the name"))
                return

            if not ip:
                messagebox.showwarning(tr("Aviso", "Notice"), tr("Informe IP ou host", "Enter the IP or host"))
                return

            tree.insert("", "end", values=(nome, ip))

            win.destroy()

        ttk.Button(btns, text=tr("Cancelar", "Cancel"), command=win.destroy).pack(side="right")
        ttk.Button(btns, text=tr("Salvar", "Save"), command=salvar).pack(side="right", padx=5)

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

        win.title(tr("Editar", "Edit"))

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

        ttk.Label(frame, text=tr("Nome do dispositivo:", "Device name:")).pack(anchor="w")

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

        ttk.Button(btns, text=tr("Cancelar", "Cancel"), command=win.destroy).pack(side="right")
        ttk.Button(btns, text=tr("Salvar", "Save"), command=salvar).pack(side="right", padx=5)

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
            tr("Aviso", "Notice"),
            tr(
                "O Rainmeter irá reiniciar para que sua configuração tenha efeito!",
                "Rainmeter will restart for your configuration to take effect!"
            )
        )

    def atualizar():
        salvar_ini()

        exe_path = os.path.join(os.getcwd(), EXE_NAME)

        if not os.path.exists(exe_path):
            messagebox.showerror(
                tr("Erro", "Error"),
                tr("SideMeterDevices.exe não encontrado.", "SideMeterDevices.exe not found.")
            )

            return

        subprocess.Popen([exe_path])

    buttons = ttk.Frame(parent, padding=10)
    buttons.pack(fill="x")

    ttk.Button(buttons, text=tr("Adicionar", "Add"), command=adicionar).pack(side="left", padx=5)
    ttk.Button(buttons, text=tr("Editar", "Edit"), command=editar).pack(side="left", padx=5)
    ttk.Button(buttons, text=tr("Remover", "Remove"), command=remover).pack(side="left", padx=5)
    ttk.Button(buttons, text=tr("Atualizar", "Update"), command=atualizar).pack(side="right")

    carregar()


def montar_aba_apimonitor(parent):
    header = ttk.Frame(parent, padding=10)
    header.pack(fill="x")

    title = ttk.Label(header, text=tr(
        "Monitoramento do Servidor",
        "Server Monitoring"
    ), font=("Segoe UI", 16, "bold"))
    title.pack(anchor="w")

    subtitle = ttk.Label(
        header,
        text=tr(
            "Configura um bloco no estilo CRT TERMINAL no Rainmeter, através dos dados disponibilizados pelo Servidor.",
            "Configures a CRT TERMINAL style block in Rainmeter, using the data provided by the Server."
        )
    )
    subtitle.pack(anchor="w")

    form = ttk.Frame(parent, padding=10)
    form.pack(fill="x")

    ttk.Label(form, text=tr(
        "Endereço do Servidor (IP/host e porta, ex: 192.168.100.121:8181):",
        "Server address (IP/host and port, e.g. 192.168.100.121:8181):"
    )).pack(anchor="w")

    en_endereco = ttk.Entry(form)
    en_endereco.pack(fill="x", pady=(5, 10))

    info = ttk.Label(
        form,
        text=tr(
            "Arquivos gerados em:\n"
            f"  {SKIN_INI_PATH}\n"
            f"  {BAT_PATH}\n"
            f"  {VBS_PATH}\n"
            f"  {PS1_PATH}\n\n"
            f"Pasta de dados:\n {RESOURCES_DIR}",
            "Files generated at:\n"
            f"  {SKIN_INI_PATH}\n"
            f"  {BAT_PATH}\n"
            f"  {VBS_PATH}\n"
            f"  {PS1_PATH}\n\n"
            f"Data folder:\n {RESOURCES_DIR}"
        ),
        foreground="#555555",
        justify="left"
    )
    info.pack(anchor="w", pady=(0, 10))

    status_var = tk.StringVar(value="")
    status_label = ttk.Label(form, textvariable=status_var, foreground="#0a7d2c")
    status_label.pack(anchor="w")

    def montar_url(endereco_bruto):
        endereco = re.sub(r'^https?://', '', endereco_bruto.strip()).rstrip('/')
        return endereco, f"http://{endereco}/api/monitor"

    def testar_conexao(url, timeout=5):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "monitor/1.0"})

            with urllib.request.urlopen(req, timeout=timeout) as resp:
                corpo = resp.read().decode("utf-8", errors="replace")

        except urllib.error.HTTPError as e:
            return False, tr(
                f"O servidor respondeu com erro HTTP {e.code}.",
                f"The server responded with HTTP error {e.code}."
            ), []

        except urllib.error.URLError as e:
            return False, tr(
                f"Não foi possível conectar ao endereço ({e.reason}).",
                f"Could not connect to the address ({e.reason})."
            ), []

        except (OSError, ValueError) as e:
            return False, tr(
                f"Não foi possível conectar ao endereço ({e}).",
                f"Could not connect to the address ({e})."
            ), []

        encontrados = set(re.findall(r'([A-Z_]+)\s*=', corpo))
        faltando = [c for c in CAMPOS_ESPERADOS_API if c not in encontrados]

        if faltando:
            return True, tr(
                "O servidor respondeu, mas faltam campos esperados: ",
                "The server responded, but expected fields are missing: "
            ) + ", ".join(faltando), faltando

        return True, tr(
            "O servidor respondeu com todos os campos esperados pelo bloco.",
            "The server responded with all the fields expected by the block."
        ), []

    def testar():
        endereco_bruto = en_endereco.get().strip()

        if not endereco_bruto:
            messagebox.showwarning(tr("Aviso", "Notice"), tr("Informe o endereço do servidor", "Enter the server address"))
            return

        _, url = montar_url(endereco_bruto)

        status_label.configure(foreground="#555555")
        status_var.set(tr(f"Testando {url} ...", f"Testing {url} ..."))
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
            messagebox.showwarning(tr("Aviso", "Notice"), tr("Informe o endereço do servidor", "Enter the server address"))
            return False

        endereco, url = montar_url(endereco_bruto)

        status_label.configure(foreground="#555555")
        status_var.set(tr(f"Verificando {url} ...", f"Checking {url} ..."))
        parent.update_idletasks()

        ok, msg, faltando = testar_conexao(url)

        if not ok:
            prosseguir = messagebox.askyesno(
                tr("Servidor não respondeu", "Server did not respond"),
                f"{msg}\n\n" + tr(
                    "Isso normalmente significa que o endereço está errado ou "
                    "o servidor da API ainda não está no ar.\n\n"
                    "Deseja gravar os arquivos mesmo assim?",
                    "This usually means the address is wrong or "
                    "the API server is not online yet.\n\n"
                    "Do you want to write the files anyway?"
                )
            )

            if not prosseguir:
                status_label.configure(foreground="#c0392b")
                status_var.set(msg)
                return False

        elif faltando:
            prosseguir = messagebox.askyesno(
                tr("Formato de resposta inesperado", "Unexpected response format"),
                f"{msg}\n\n" + tr(
                    "O bloco usa esses campos para montar todas as configurações. "
                    "Os medidores correspondentes podem ficar em branco.\n\n"
                    "Deseja continuar mesmo assim?",
                    "The block uses these fields to build all its settings. "
                    "The corresponding meters may be left blank.\n\n"
                    "Do you want to continue anyway?"
                )
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
            messagebox.showerror(tr("Erro", "Error"), tr(f"Falha ao gravar os arquivos:\n{e}", f"Failed to write the files:\n{e}"))
            return False

        status_label.configure(foreground="#0a7d2c")
        status_var.set(tr(
            f"Arquivos gerados com sucesso. API: {url}",
            f"Files generated successfully. API: {url}"
        ))

        messagebox.showinfo(
            tr("Aviso", "Notice"),
            tr(
                "Bloco CRT TERMINAL configurado!\n\n"
                "O Rainmeter irá reiniciar o bloco \"ServerMonitor\" "
                "para que a nova configuração tenha efeito.",
                "CRT TERMINAL block configured!\n\n"
                "Rainmeter will restart the \"ServerMonitor\" block "
                "for the new configuration to take effect."
            )
        )

        return True

    def atualizar():
        gerado = gerar()

        if not gerado:
            return

        if os.path.exists(BAT_PATH):
            try:
                subprocess.Popen(
                    [BAT_PATH],
                    cwd=SCRIPTS_DIR,
                    shell=True
                )
            except OSError as e:
                messagebox.showerror(tr("Erro", "Error"), tr(f"Falha ao iniciar o script:\n{e}", f"Failed to start the script:\n{e}"))

        ativar_skin_rainmeter("ServerMonitor", "ServerMonitor.ini", status_var, status_label)

    buttons = ttk.Frame(parent, padding=10)
    buttons.pack(fill="x", side="bottom")

    ttk.Button(buttons, text=tr("Atualizar", "Update"), command=atualizar).pack(side="right")
    ttk.Button(buttons, text=tr(
        "Testar Conexão",
        "Test Connection"
    ), command=testar).pack(side="right", padx=5)

    carregar_endereco_atual()


def montar_aba_rainmeter(parent):
    sub_notebook = ttk.Notebook(parent)
    sub_notebook.pack(fill="both", expand=True)

    sub_aba_network = ttk.Frame(sub_notebook)
    sub_aba_system = ttk.Frame(sub_notebook)

    sub_notebook.add(sub_aba_network, text="Network")
    sub_notebook.add(sub_aba_system, text="System")

    montar_subaba_network(sub_aba_network)
    montar_subaba_system(sub_aba_system)


def criar_cabecalho_subaba(parent, titulo, subtitulo):
    cabecalho = ttk.Frame(parent, padding=(10, 10, 10, 0))
    cabecalho.pack(fill="x")

    ttk.Label(cabecalho, text=titulo, font=("Segoe UI", 13, "bold")).pack(anchor="w")
    ttk.Label(cabecalho, text=subtitulo).pack(anchor="w")

    return cabecalho


def montar_subaba_network(parent):
    criar_cabecalho_subaba(
        parent,
        "Link Speed",
        tr(
            "Adiciona um medidor de velocidade da rede ao bloco \"Network\" já existente no Rainmeter.",
            "Adds a network speed meter to the existing Rainmeter \"Network\" block."
        )
    )

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
        text=tr(
            "Arquivos envolvidos:\n"
            f"  {NETWORK_INI_PATH}\n"
            f"  {LINKSPEED_PS1_PATH}\n"
            f"  {RUNLINKSPEED_VBS_PATH}",
            "Files involved:\n"
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
            status_ini_var.set(tr(
                f"Network.ini original encontrado em:\n  {NETWORK_INI_PATH}",
                f"Original Network.ini found at:\n  {NETWORK_INI_PATH}"
            ))
        else:
            status_ini_label.configure(foreground="#c0392b")
            status_ini_var.set(tr(
                "Network.ini original não encontrado.\n"
                f"  Esperado em: {NETWORK_INI_PATH}",
                "Original Network.ini not found.\n"
                f"  Expected at: {NETWORK_INI_PATH}"
            ))

        if link_speed_configurado():
            status_link_label.configure(foreground="#0a7d2c")
            status_link_var.set(tr(
                "Link Speed já está configurado neste bloco.",
                "Link Speed is already configured in this block."
            ))
            botao_adicionar.state(["disabled"])
            botao_atualizar.state(["disabled"])
        else:
            status_link_label.configure(foreground="#b8860b")
            status_link_var.set(tr(
                "Link Speed ainda não foi adicionado a este bloco.",
                "Link Speed has not been added to this block yet."
            ))
            botao_adicionar.state(["!disabled"])
            botao_atualizar.state(["!disabled"])

    def adicionar_link_speed():
        if not os.path.exists(NETWORK_INI_PATH):
            messagebox.showwarning(
                tr("Aviso", "Notice"),
                tr(
                    "O Network.ini original não foi encontrado.\n\n"
                    f"Esperado em:\n{NETWORK_INI_PATH}\n\n"
                    "Instale/carregue o bloco \"Network\" do Rainmeter antes de continuar.",
                    "The original Network.ini was not found.\n\n"
                    f"Expected at:\n{NETWORK_INI_PATH}\n\n"
                    "Install/load the Rainmeter \"Network\" block before continuing."
                )
            )
            return

        if link_speed_configurado():
            prosseguir = messagebox.askyesno(
                tr("Link Speed já configurado", "Link Speed already configured"),
                tr(
                    "O Link Speed já parece estar configurado neste bloco.\n\n"
                    "Deseja sobrescrever o Network.ini e os scripts mesmo assim?",
                    "Link Speed already seems to be configured in this block.\n\n"
                    "Do you want to overwrite Network.ini and the scripts anyway?"
                )
            )

            if not prosseguir:
                return

        else:
            prosseguir = messagebox.askyesno(
                tr("Adicionar Link Speed", "Add Link Speed"),
                tr(
                    "Isso vai sobrescrever o Network.ini atual por uma versão que "
                    "já inclui o medidor de Link Speed, e criar os scripts "
                    "LinkSpeed.ps1 e RunLinkSpeed.vbs na mesma pasta.\n\n"
                    "Deseja continuar?",
                    "This will overwrite the current Network.ini with a version that "
                    "already includes the Link Speed meter, and create the scripts "
                    "LinkSpeed.ps1 and RunLinkSpeed.vbs in the same folder.\n\n"
                    "Do you want to continue?"
                )
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
            messagebox.showerror(tr("Erro", "Error"), tr(f"Falha ao gravar os arquivos:\n{e}", f"Failed to write the files:\n{e}"))
            return

        status_label.configure(foreground="#0a7d2c")
        status_var.set(tr(
            "Link Speed adicionado com sucesso ao Network.ini.",
            "Link Speed successfully added to Network.ini."
        ))

        verificar_status()

        messagebox.showinfo(
            tr("Aviso", "Notice"),
            tr(
                "Link Speed configurado no bloco \"Network\".\n\n"
                "O Rainmeter irá reiniciar para que a nova configuração tenha efeito.",
                "Link Speed configured in the \"Network\" block.\n\n"
                "Rainmeter will restart for the new configuration to take effect."
            )
        )

    def atualizar():
        ativar_skin_rainmeter(NETWORK_SKIN_NAME, "Network.ini", status_var, status_label)

    buttons = ttk.Frame(parent, padding=10)
    buttons.pack(fill="x", side="bottom")

    botao_atualizar = ttk.Button(buttons, text=tr("Atualizar", "Update"), command=atualizar)
    botao_atualizar.pack(side="right")

    botao_adicionar = ttk.Button(buttons, text=tr("Adicionar", "Add"), command=adicionar_link_speed)
    botao_adicionar.pack(side="right", padx=5)

    verificar_status()
    ATUALIZADORES_UI.append(verificar_status)


def montar_subaba_system(parent):
    criar_cabecalho_subaba(
        parent,
        "System Update",
        tr(
            "Aplica uma configuração atualizada ao bloco \"System\" já existente no Rainmeter.",
            "Applies an updated configuration to the existing Rainmeter \"System\" block."
        )
    )

    form_sistema = ttk.Frame(parent, padding=(10, 4))
    form_sistema.pack(fill="both", expand=True)

    status_sistema_ini_var = tk.StringVar(value="")
    status_sistema_ini_label = ttk.Label(form_sistema, textvariable=status_sistema_ini_var, justify="left")
    status_sistema_ini_label.pack(anchor="w", pady=(0, 2))

    status_sistema_config_var = tk.StringVar(value="")
    status_sistema_config_label = ttk.Label(form_sistema, textvariable=status_sistema_config_var, justify="left")
    status_sistema_config_label.pack(anchor="w", pady=(0, 6))

    quadro_lhm = ttk.LabelFrame(form_sistema, text="LibreHardwareMonitor (\u00b0C)", padding=(8, 4))
    quadro_lhm.pack(fill="x", pady=(14, 4))

    status_lhm_var = tk.StringVar(value="")
    status_lhm_label = ttk.Label(quadro_lhm, textvariable=status_lhm_var, justify="left", wraplength=470)
    status_lhm_label.pack(anchor="w", pady=(0, 4))

    botoes_lhm = ttk.Frame(quadro_lhm)
    botoes_lhm.pack(fill="x")

    botao_instalar_lhm = ttk.Button(botoes_lhm, text=tr("Instalar", "Install"))
    botao_instalar_lhm.pack(side="left")

    botao_abrir_lhm = ttk.Button(botoes_lhm, text=tr("Ativar", "Enable"))
    botao_abrir_lhm.pack(side="left", padx=5)

    status_sistema_var = tk.StringVar(value="")
    status_sistema_label = ttk.Label(form_sistema, textvariable=status_sistema_var, foreground="#0a7d2c")
    status_sistema_label.pack(anchor="w")

    def sistema_configurado():
        if not os.path.exists(SYSTEM_INI_PATH):
            return False

        try:
            conteudo = ler_texto(SYSTEM_INI_PATH)

        except OSError:
            return False

        return "measureGPUTemp" in conteudo

    def verificar_status_sistema():
        if os.path.exists(SYSTEM_INI_PATH):
            status_sistema_ini_label.configure(foreground="#0a7d2c")
            status_sistema_ini_var.set(tr("System.ini original encontrado.", "Original System.ini found."))
        else:
            status_sistema_ini_label.configure(foreground="#c0392b")
            status_sistema_ini_var.set(tr(
                "System.ini original não encontrado.",
                "Original System.ini not found."
            ))

        if sistema_configurado():
            status_sistema_config_label.configure(foreground="#0a7d2c")
            status_sistema_config_var.set(tr(
                "A atualização já está configurada.",
                "The update is already configured."
            ))
            botao_aplicar_sistema.state(["disabled"])
            botao_atualizar_sistema.state(["disabled"])
        else:
            status_sistema_config_label.configure(foreground="#b8860b")
            status_sistema_config_var.set(tr(
                "O bloco ainda não está configurado.",
                "The block is not configured yet."
            ))
            botao_aplicar_sistema.state(["!disabled"])
            botao_atualizar_sistema.state(["!disabled"])

    def aplicar_system_ini():
        if not os.path.exists(SYSTEM_INI_PATH):
            messagebox.showwarning(
                tr("Aviso", "Notice"),
                tr(
                    "O System.ini original não foi encontrado.\n\n"
                    f"Esperado em:\n{SYSTEM_INI_PATH}\n\n"
                    "Instale/carregue o bloco \"System\" do Rainmeter antes de continuar.",
                    "The original System.ini was not found.\n\n"
                    f"Expected at:\n{SYSTEM_INI_PATH}\n\n"
                    "Install/load the Rainmeter \"System\" block before continuing."
                )
            )
            return

        if sistema_configurado():
            messagebox.showinfo(
                tr("Aviso", "Notice"),
                tr(
                    "O System.ini já está configurado. Nenhuma alteração foi necessária.",
                    "System.ini is already configured. No changes were needed."
                )
            )
            return

        prosseguir = messagebox.askyesno(
            tr("Aplicar System.ini", "Apply System.ini"),
            tr(
                "Isso vai sobrescrever o System.ini atual pela versão configurada "
                "(CPU, RAM, disponível em GB e temperaturas de CPU/GPU).\n\n"
                "Para as temperaturas, o LibreHardwareMonitor precisa estar aberto "
                "com o Remote Web Server ligado (porta 8085).\n\n"
                "Deseja continuar?",
                "This will overwrite the current System.ini with the configured version "
                "(CPU, RAM, available GB and CPU/GPU temperatures).\n\n"
                "For the temperatures, LibreHardwareMonitor must be open "
                "with the Remote Web Server running (port 8085).\n\n"
                "Do you want to continue?"
            )
        )

        if not prosseguir:
            return

        try:
            os.makedirs(SYSTEM_SKIN_DIR, exist_ok=True)

            with open(SYSTEM_INI_PATH, "w", encoding="utf-16") as f:
                f.write(SYSTEM_INI_TEMPLATE)

        except OSError as e:
            messagebox.showerror(tr("Erro", "Error"), tr(f"Falha ao gravar o arquivo:\n{e}", f"Failed to write the file:\n{e}"))
            return

        status_sistema_label.configure(foreground="#0a7d2c")
        status_sistema_var.set(tr("Atualização configurada com sucesso.", "Update configured successfully."))

        verificar_status_sistema()

        messagebox.showinfo(
            tr("Aviso", "Notice"),
            tr(
                "Bloco \"System\" configurado.\n\n"
                "O Rainmeter irá reiniciar o bloco para que a "
                "nova configuração tenha efeito.",
                "\"System\" block configured.\n\n"
                "Rainmeter will restart the block for the "
                "new configuration to take effect."
            )
        )

        ativar_skin_rainmeter(SYSTEM_SKIN_NAME, "System.ini", status_sistema_var, status_sistema_label)

    def atualizar_sistema():
        ativar_skin_rainmeter(SYSTEM_SKIN_NAME, "System.ini", status_sistema_var, status_sistema_label)

    estado_lhm = {
        "ocupado": False,
        "pronto": False,
        "resultado": None,
        "ultima": 0.0,
        "forcar": True,
        "operacao": False,
    }

    def coletar_lhm():
        try:
            exe = localizar_lhm()
            rodando = lhm_esta_rodando() if exe else False
            ativo = lhm_servidor_ativo() if exe else False
            estado_lhm["resultado"] = (exe, rodando, ativo)

        except Exception:
            estado_lhm["resultado"] = None

        finally:
            estado_lhm["pronto"] = True

    def renderizar_lhm(exe, rodando, ativo):
        if not exe:
            status_lhm_label.configure(foreground="#c0392b")
            status_lhm_var.set(tr(
                "Não instalado. Clique em Instalar (usa o winget e pede permissão de administrador).",
                "Not installed. Click Install (uses winget and asks for administrator permission)."
            ))
            botao_instalar_lhm.state(["!disabled"])
            botao_abrir_lhm.state(["disabled"])
            return

        botao_instalar_lhm.state(["disabled"])

        if ativo:
            status_lhm_label.configure(foreground="#0a7d2c")
            status_lhm_var.set(tr(
                "Instalado e com o servidor ativo na porta 8085.",
                "Installed and with the server active on port 8085."
            ))
            botao_abrir_lhm.state(["disabled"])

        elif rodando:
            status_lhm_label.configure(foreground="#b8860b")
            status_lhm_var.set(
                tr(
                    "Aberto, mas sem o servidor. Clique em Ativar para reiniciá-lo com o servidor ligado.",
                    "Open, but without the server. Click Enable to restart it with the server on."
                )
            )
            botao_abrir_lhm.state(["!disabled"])

        else:
            status_lhm_label.configure(foreground="#b8860b")
            status_lhm_var.set(tr(
                "Instalado, mas fechado. Clique em Ativar.",
                "Installed, but closed. Click Enable."
            ))
            botao_abrir_lhm.state(["!disabled"])

    def tick_lhm():
        if estado_lhm["pronto"]:
            estado_lhm["pronto"] = False
            estado_lhm["ocupado"] = False

            if estado_lhm["resultado"] and not estado_lhm["operacao"]:
                renderizar_lhm(*estado_lhm["resultado"])

        agora = time.time()

        if not estado_lhm["ocupado"] and (estado_lhm["forcar"] or agora - estado_lhm["ultima"] >= 4):
            estado_lhm["forcar"] = False
            estado_lhm["ocupado"] = True
            estado_lhm["ultima"] = agora
            threading.Thread(target=coletar_lhm, daemon=True).start()

        root.after(500, tick_lhm)

    def atualizar_status_lhm():
        estado_lhm["forcar"] = True

    def iniciar_operacao_lhm(mensagem):
        estado_lhm["operacao"] = True
        botao_instalar_lhm.state(["disabled"])
        botao_abrir_lhm.state(["disabled"])
        status_lhm_label.configure(foreground="#555555")
        status_lhm_var.set(mensagem)

    def encerrar_operacao_lhm():
        estado_lhm["operacao"] = False
        estado_lhm["forcar"] = True

    def aplicar_system_e_recarregar():
        try:
            if not sistema_configurado():
                os.makedirs(SYSTEM_SKIN_DIR, exist_ok=True)

                with open(SYSTEM_INI_PATH, "w", encoding="utf-16") as f:
                    f.write(SYSTEM_INI_TEMPLATE)

        except OSError as e:
            messagebox.showerror(tr("Erro", "Error"), tr(f"Falha ao gravar o System.ini:\n{e}", f"Failed to write System.ini:\n{e}"))
            return

        verificar_status_sistema()

        if ativar_skin_rainmeter(SYSTEM_SKIN_NAME, "System.ini", status_sistema_var, status_sistema_label):
            status_sistema_label.configure(foreground="#0a7d2c")
            status_sistema_var.set(tr(
                "System atualizado com medidores de temperatura.",
                "System updated with temperature meters."
            ))

    def instalar_lhm():
        if localizar_lhm():
            atualizar_status_lhm()
            return

        if not shutil.which("winget"):
            if messagebox.askyesno(
                tr("winget não encontrado", "winget not found"),
                tr(
                    "Não encontrei o winget neste computador.\n\n"
                    "Deseja abrir a página de downloads do LibreHardwareMonitor "
                    "para instalar manualmente?",
                    "I could not find winget on this computer.\n\n"
                    "Do you want to open the LibreHardwareMonitor downloads page "
                    "to install it manually?"
                )
            ):
                webbrowser.open("https://github.com/LibreHardwareMonitor/LibreHardwareMonitor/releases")
            return

        if not messagebox.askyesno(
            tr("Instalar LibreHardwareMonitor", "Install LibreHardwareMonitor"),
            tr(
                "Vou instalar o LibreHardwareMonitor e o driver PawnIO (usado para ler os sensores) "
                "pelo winget.\n\nO Windows vai pedir permissão de administrador. Deseja continuar?",
                "I will install LibreHardwareMonitor and the PawnIO driver (used to read the sensors) "
                "through winget.\n\nWindows will ask for administrator permission. Do you want to continue?"
            )
        ):
            return

        iniciar_operacao_lhm(tr(
            "Instalando... aguarde (pode demorar um minuto).",
            "Installing... please wait (it may take a minute)."
        ))

        resultado = {}

        def trabalho():
            try:
                proc = subprocess.run(
                    [
                        "winget", "install", "--id", LHM_WINGET_ID, "-e",
                        "--accept-package-agreements", "--accept-source-agreements",
                    ],
                    capture_output=True,
                    creationflags=0x08000000
                )
                resultado["codigo"] = proc.returncode

            except OSError as e:
                resultado["erro"] = str(e)

        thread = threading.Thread(target=trabalho, daemon=True)
        thread.start()

        def aguardar():
            if thread.is_alive():
                root.after(500, aguardar)
                return

            encerrar_operacao_lhm()

            if "erro" in resultado:
                messagebox.showerror(tr("Erro", "Error"), tr(f"Falha ao executar o winget:\n{resultado['erro']}", f"Failed to run winget:\n{resultado['erro']}"))

            elif not localizar_lhm():
                messagebox.showerror(
                    tr("Erro", "Error"),
                    tr(
                        "A instalação não foi concluída (código "
                        f"{resultado.get('codigo')}).\n\n"
                        "Se você recusou a permissão de administrador, tente novamente.",
                        "The installation was not completed (code "
                        f"{resultado.get('codigo')}).\n\n"
                        "If you declined the administrator permission, try again."
                    )
                )

            else:
                messagebox.showinfo(tr("Aviso", "Notice"), tr("LibreHardwareMonitor instalado.\n\nAgora clique em Ativar.", "LibreHardwareMonitor installed.\n\nNow click Enable."))

        root.after(500, aguardar)

    def ativar_lhm():
        exe = localizar_lhm()

        if not exe:
            atualizar_status_lhm()
            return

        ultimo = estado_lhm["resultado"]
        rodando = bool(ultimo and ultimo[1])

        if rodando:
            if not messagebox.askyesno(
                tr("Ativar servidor", "Enable server"),
                tr(
                    "O LibreHardwareMonitor está aberto, mas sem o servidor.\n\n"
                    "Vou fechá-lo e abri-lo novamente com o servidor ligado "
                    "(o Windows pode pedir permissão de administrador). Deseja continuar?",
                    "LibreHardwareMonitor is open, but without the server.\n\n"
                    "I will close it and open it again with the server enabled "
                    "(Windows may ask for administrator permission). Do you want to continue?"
                )
            ):
                return

        iniciar_operacao_lhm(tr("Ativando o servidor... aguarde.", "Enabling the server... please wait."))

        resultado = {}

        def trabalho():
            try:
                if lhm_esta_rodando():
                    ctypes.windll.shell32.ShellExecuteW(
                        None, "runas", "taskkill", "/F /IM LibreHardwareMonitor.exe", None, 0
                    )

                    for _ in range(40):
                        if not lhm_esta_rodando():
                            break
                        time.sleep(0.5)

                    if lhm_esta_rodando():
                        resultado["erro"] = tr(
                            "Não consegui fechar o LibreHardwareMonitor. "
                            "Feche-o manualmente e tente novamente.",
                            "I could not close LibreHardwareMonitor. "
                            "Close it manually and try again."
                        )
                        return

                try:
                    habilitar_webserver_lhm(exe)
                    registrar_lhm_na_inicializacao(exe)

                except OSError as e:
                    resultado["aviso_config"] = str(e)

                if not abrir_lhm_como_admin(exe):
                    resultado["erro"] = tr(
                        "Não foi possível abrir o LibreHardwareMonitor como administrador.",
                        "Could not open LibreHardwareMonitor as administrator."
                    )
                    return

                for _ in range(60):
                    if lhm_servidor_ativo():
                        resultado["ok"] = True
                        return
                    time.sleep(0.5)

            except OSError as e:
                resultado["erro"] = str(e)

        thread = threading.Thread(target=trabalho, daemon=True)
        thread.start()

        def aguardar():
            if thread.is_alive():
                root.after(500, aguardar)
                return

            encerrar_operacao_lhm()

            if "erro" in resultado:
                messagebox.showerror(tr("Erro", "Error"), resultado["erro"])

            elif resultado.get("ok"):
                aplicar_system_e_recarregar()

            else:
                messagebox.showinfo(
                    tr("Aviso", "Notice"),
                    tr(
                        "O LibreHardwareMonitor foi aberto, mas o servidor não respondeu.\n\n"
                        "No programa, vá em Options > Remote Web Server > Run.",
                        "LibreHardwareMonitor was opened, but the server did not respond.\n\n"
                        "In the program, go to Options > Remote Web Server > Run."
                    )
                )

        root.after(500, aguardar)

    botao_instalar_lhm.configure(command=instalar_lhm)
    botao_abrir_lhm.configure(command=ativar_lhm)

    buttons_sistema = ttk.Frame(parent, padding=(10, 4))
    buttons_sistema.pack(fill="x", side="bottom")

    botao_atualizar_sistema = ttk.Button(buttons_sistema, text=tr(
        "Atualizar",
        "Update"
    ), command=atualizar_sistema)
    botao_atualizar_sistema.pack(side="right")

    botao_aplicar_sistema = ttk.Button(buttons_sistema, text=tr(
        "Adicionar",
        "Add"
    ), command=aplicar_system_ini)
    botao_aplicar_sistema.pack(side="right", padx=5)

    verificar_status_sistema()
    ATUALIZADORES_UI.append(verificar_status_sistema)
    tick_lhm()


def backup_arquivo(caminho):
    if os.path.exists(caminho):
        carimbo = time.strftime("%Y%m%d-%H%M%S")
        shutil.copy2(caminho, f"{caminho}.{carimbo}.bak")


def fechar_rainmeter_e_scripts():
    flags = 0x08000000

    subprocess.run(["taskkill", "/F", "/IM", "Rainmeter.exe"], capture_output=True, creationflags=flags)

    for _ in range(20):
        if not rainmeter_esta_rodando():
            break
        time.sleep(0.5)

    comando = (
        "Get-CimInstance Win32_Process | Where-Object { "
        "$_.CommandLine -like '*check_network.ps1*' -or $_.CommandLine -like '*LinkSpeed.ps1*' "
        "} | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }"
    )

    try:
        subprocess.run(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", comando],
            capture_output=True, timeout=20, creationflags=flags
        )

    except (OSError, subprocess.TimeoutExpired):
        pass

    time.sleep(1)


def remover_com_backup(caminho):
    if not os.path.exists(caminho):
        return

    backup_arquivo(caminho)
    os.remove(caminho)


def resetar_tudo():
    exe_devices = os.path.join(os.getcwd(), EXE_NAME)
    regenera_devices = os.path.exists(INI_FILE) and os.path.exists(exe_devices)

    if not messagebox.askyesno(
        "Reset",
        tr(
            "Isso vai FECHAR o Rainmeter, apagar as configurações antigas e recriá-las "
            "no modelo desta versão do app:\n\n"
            "  - System (CPU, RAM e Temperaturas)\n"
            "  - Network (com Link Speed)\n"
            "  - Status de Dispositivos\n\n"
            "Os dispositivos de rede cadastrados serão mantidos.\n"
            "Os arquivos atuais ganham uma cópia .bak antes de serem substituídos.\n\n"
            "Deseja continuar?",
            "This will CLOSE Rainmeter, delete the old settings and recreate them "
            "using this version of the app:\n\n"
            "  - System (CPU, RAM and Temperatures)\n"
            "  - Network (with Link Speed)\n"
            "  - Devices Status\n\n"
            "The registered network devices will be kept.\n"
            "The current files get a .bak copy before being replaced.\n\n"
            "Do you want to continue?"
        )
    ):
        return

    botao_reset.state(["disabled"])
    resultado = {"avisos": []}

    def trabalho():
        try:
            fechar_rainmeter_e_scripts()

            if rainmeter_esta_rodando():
                resultado["erro"] = tr(
                    "Não consegui fechar o Rainmeter. Feche-o manualmente "
                    "(ou rode este app como administrador) e tente novamente.",
                    "I could not close Rainmeter. Close it manually "
                    "(or run this app as administrator) and try again."
                )
                return

            for antigo in (
                SYSTEM_INI_PATH, NETWORK_INI_PATH,
                LINKSPEED_PS1_PATH, RUNLINKSPEED_VBS_PATH,
            ):
                remover_com_backup(antigo)

            os.makedirs(SYSTEM_SKIN_DIR, exist_ok=True)

            with open(SYSTEM_INI_PATH, "w", encoding="utf-16") as f:
                f.write(SYSTEM_INI_TEMPLATE)

            os.makedirs(NETWORK_SKIN_DIR, exist_ok=True)

            with open(NETWORK_INI_PATH, "w", encoding="utf-8") as f:
                f.write(NETWORK_INI_TEMPLATE)

            with open(LINKSPEED_PS1_PATH, "w", encoding="utf-8") as f:
                f.write(LINKSPEED_PS1_TEMPLATE)

            with open(RUNLINKSPEED_VBS_PATH, "w", encoding="utf-8") as f:
                f.write(RUNLINKSPEED_VBS_TEMPLATE)

        except OSError as e:
            resultado["erro"] = str(e)
            return

        if regenera_devices:
            try:
                subprocess.run([exe_devices], timeout=90, creationflags=0x08000000)

            except (OSError, subprocess.TimeoutExpired) as e:
                resultado["avisos"].append(tr(
                    f"Não consegui regenerar os Dispositivos: {e}",
                    f"Could not regenerate the Devices: {e}"
                ))

        else:
            resultado["avisos"].append(
                tr(
                    "Dispositivos: não regenerado (SideMeterDevices.exe ou devices.ini não encontrado).",
                    "Devices: not regenerated (SideMeterDevices.exe or devices.ini not found)."
                )
            )

    thread = threading.Thread(target=trabalho, daemon=True)
    thread.start()

    def aguardar():
        if thread.is_alive():
            root.after(500, aguardar)
            return

        botao_reset.state(["!disabled"])

        if "erro" in resultado:
            messagebox.showerror(tr("Erro", "Error"), tr(f"Falha no reset:\n{resultado['erro']}", f"Reset failed:\n{resultado['erro']}"))
            return

        for atualizador in ATUALIZADORES_UI:
            atualizador()

        ativar_skin_rainmeter(SYSTEM_SKIN_NAME, "System.ini")
        ativar_skin_rainmeter(NETWORK_SKIN_NAME, "Network.ini")

        mensagem = tr(
            "As configurações foram recriadas e recarregadas.",
            "The settings were recreated and reloaded."
        )

        if resultado["avisos"]:
            mensagem += "\n\n" + "\n".join(resultado["avisos"])

        messagebox.showinfo("Reset", mensagem)

    root.after(500, aguardar)


montar_aba_sidemeterdevices(aba_sidemeterdevices)
montar_aba_apimonitor(aba_apimonitor)
montar_aba_rainmeter(aba_rainmeter)


root.mainloop()
