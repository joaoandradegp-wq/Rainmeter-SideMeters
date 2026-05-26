import os
import time
import configparser

# ==========================================
# FECHA RAINMETER
# ==========================================

print("Fechando Rainmeter...")

os.system("taskkill /F /IM Rainmeter.exe >nul 2>&1")

time.sleep(2)

# ==========================================
# PATHS
# ==========================================

base_path = os.path.expanduser(r"~\Documents\Rainmeter")
scripts_path = os.path.join(base_path, "Scripts")
skin_path = os.path.join(base_path, "Skins", "illustro", "NetworkDevices")

os.makedirs(scripts_path, exist_ok=True)
os.makedirs(skin_path, exist_ok=True)

# ==========================================
# REMOVE ARQUIVOS ANTIGOS
# ==========================================

old_files = [
    os.path.join(scripts_path, "check_network.ps1"),
    os.path.join(scripts_path, "check_network.bat"),
    os.path.join(scripts_path, "start_hidden.vbs"),
    os.path.join(scripts_path, "network.lua"),
    os.path.join(base_path, "network_status.txt"),
    os.path.join(skin_path, "RedeMonitor.ini")
]

print("")
print("Removendo arquivos antigos...")
print("")

for file in old_files:

    if os.path.exists(file):

        try:
            os.remove(file)
            print(f"REMOVIDO: {file}")

        except Exception as e:
            print(f"ERRO AO REMOVER {file}: {e}")

# ==========================================
# DEVICES
# ==========================================

devices_ini = os.path.join(scripts_path, "devices.ini")

if not os.path.exists(devices_ini):

    config = configparser.ConfigParser()

    config["PC1"] = {"ip": "192.168.0.10"}
    config["PC2"] = {"ip": "192.168.0.20"}

    with open(devices_ini, "w") as f:
        config.write(f)

    print("")
    print("devices.ini criado!")
    print("Edite o arquivo e execute novamente.")
    print("")

    exit()

config = configparser.ConfigParser()
config.read(devices_ini)

devices = []

for section in config.sections():

    name = section
    ip = config[section]["ip"]

    devices.append((name, ip))

# ==========================================
# POWERSHELL
# ==========================================

print("")
print("Gerando PowerShell...")
print("")

ps_lines = []

ps_lines.append("while ($true)")
ps_lines.append("{")

for i, (_, ip) in enumerate(devices, start=1):

    ps_lines.append(
        f'    $pc{i} = if (Test-Connection {ip} -Count 1 -Quiet) {{ "ONLINE" }} else {{ "OFFLINE" }}'
    )

ps_output = "`n".join([f"$pc{i}" for i in range(1, len(devices) + 1)])

ps_lines.append("")
ps_lines.append(f'    "{ps_output}" | Out-File "$env:USERPROFILE\\Documents\\Rainmeter\\network_status.txt" -Encoding ASCII')
ps_lines.append("")
ps_lines.append("    Start-Sleep -Seconds 5")
ps_lines.append("}")

ps_script = "\n".join(ps_lines)

ps1_path = os.path.join(scripts_path, "check_network.ps1")

with open(ps1_path, "w", encoding="utf-8-sig", newline="\r\n") as f:
    f.write(ps_script)

# ==========================================
# BAT
# ==========================================

print("Gerando BAT...")

bat_content = r'''@echo off

for /f "tokens=2 delims=," %%a in ('
    tasklist /v /fo csv ^| findstr /i "check_network.ps1"
') do (
    taskkill /F /PID %%~a >nul 2>&1
)

powershell -WindowStyle Hidden -ExecutionPolicy Bypass -File "%USERPROFILE%\Documents\Rainmeter\Scripts\check_network.ps1"
'''

bat_path = os.path.join(scripts_path, "check_network.bat")

with open(bat_path, "w", encoding="utf-8") as f:
    f.write(bat_content)

# ==========================================
# VBS
# ==========================================

print("Gerando VBS...")

vbs_content = r'''Set WshShell = CreateObject("WScript.Shell")

batPath = WshShell.ExpandEnvironmentStrings("%USERPROFILE%") & "\Documents\Rainmeter\Scripts\check_network.bat"

WshShell.Run chr(34) & batPath & chr(34), 0

Set WshShell = Nothing
'''

vbs_path = os.path.join(scripts_path, "start_hidden.vbs")

with open(vbs_path, "w", encoding="utf-8") as f:
    f.write(vbs_content)

# ==========================================
# LUA
# ==========================================

print("Gerando LUA...")

lua_txt_path = (base_path + "\\network_status.txt").replace("\\", "\\\\")

lua_lines = []

lua_lines.append("function Initialize()")
lua_lines.append(f'    path = "{lua_txt_path}"')
lua_lines.append("end")
lua_lines.append("")

lua_lines.append("function Update()")
lua_lines.append('    local file = io.open(path, "r")')

lua_lines.extend([
    "    if not file then",
    "        return",
    "    end",
    "",
    "    local lines = {}",
    "",
    "    for line in file:lines() do",
    "        table.insert(lines, line)",
    "    end",
    "",
    "    file:close()",
    ""
])

for i in range(1, len(devices) + 1):

    lua_lines.append(f"    if lines[{i}] then")

    lua_lines.append(f'        SKIN:Bang("!SetOption", "meterPC{i}Status", "Text", lines[{i}])')
    lua_lines.append(f'        if lines[{i}] == "ONLINE" then')

    lua_lines.append(
        f'            SKIN:Bang("!SetOption", "meterPC{i}Status", "FontColor", "0,255,0,255")'
    )

    lua_lines.append("        else")

    lua_lines.append(
        f'            SKIN:Bang("!SetOption", "meterPC{i}Status", "FontColor", "255,80,80,255")'
    )

    lua_lines.append("        end")
    lua_lines.append("    end")
    lua_lines.append("")

lua_lines.append('    SKIN:Bang("!UpdateMeter", "*")')
lua_lines.append('    SKIN:Bang("!Redraw")')
lua_lines.append("end")

lua_path = os.path.join(scripts_path, "network.lua")

with open(lua_path, "w", encoding="utf-8") as f:
    f.write("\n".join(lua_lines))

# ==========================================
# INI
# ==========================================

print("Gerando INI...")

ini_lines = []

ini_lines.extend([
    "[Rainmeter]",
    "Update=1000",
    "AccurateText=1",
    "DynamicWindowSize=1",
    "Background=#@#Background.png",
    "BackgroundMode=3",
    "BackgroundMargins=0,34,0,14",
    "Draggable=1",
    "ClickThrough=0",
    f'OnRefreshAction=["{vbs_path}"]',
    ""
])

ini_lines.extend([
    "[Metadata]",
    "Name=Network Devices",
    "Author=Phobos",
    "Version=FINAL-PERSISTENT",
    ""
])

ini_lines.extend([
    "[Variables]",
    "fontName=Trebuchet MS",
    "textSize=8",
    "colorText=255,255,255,205",
    ""
])

ini_lines.extend([
    "[LuaScript]",
    "Measure=Script",
    f"ScriptFile={lua_path}",
    "UpdateDivider=1",
    ""
])

ini_lines.extend([
    "[styleTitle]",
    "StringAlign=Center",
    "StringCase=Upper",
    "StringStyle=Bold",
    "FontColor=#colorText#",
    "FontFace=#fontName#",
    "FontSize=10",
    "AntiAlias=1",
    ""
])

ini_lines.extend([
    "[styleLeftText]",
    "StringAlign=Left",
    "FontColor=#colorText#",
    "FontFace=#fontName#",
    "FontSize=#textSize#",
    "AntiAlias=1",
    ""
])

ini_lines.extend([
    "[styleRightText]",
    "StringAlign=Right",
    "FontFace=#fontName#",
    "FontSize=#textSize#",
    "AntiAlias=1",
    ""
])

ini_lines.extend([
    "[meterTitle]",
    "Meter=String",
    "MeterStyle=styleTitle",
    "X=100",
    "Y=12",
    "W=190",
    "Text=Dispositivos",
    ""
])

y = 40

for i, (name, _) in enumerate(devices, start=1):

    ini_lines.extend([
        f"[meterPC{i}]",
        "Meter=String",
        "MeterStyle=styleLeftText",
        "X=10",
        f"Y={y}",
        f"Text={name}",
        "",
        f"[meterPC{i}Status]",
        "Meter=String",
        "MeterStyle=styleRightText",
        "X=200",
        f"Y={y}",
        "Text=...",
        "DynamicVariables=1",
        ""
    ])

    y += 20

# ==========================================
# SAVE INI
# ==========================================

ini_path = os.path.join(skin_path, "RedeMonitor.ini")

with open(ini_path, "w", encoding="utf-8") as f:
    f.write("\n".join(ini_lines))

# ==========================================
# ABRE RAINMETER
# ==========================================

print("")
print("Abrindo Rainmeter...")
print("")

rainmeter_path = r"C:\Program Files\Rainmeter\Rainmeter.exe"

if os.path.exists(rainmeter_path):

    os.startfile(rainmeter_path)

    time.sleep(3)

    os.system(f'"{rainmeter_path}" !ActivateConfig "illustro\\NetworkDevices" "RedeMonitor.ini"')

# ==========================================
# DONE
# ==========================================

print("")
print("====================================")
print("✅ RedeMonitor gerado com sucesso!")
print("====================================")
print("")

print(f"INI : {ini_path}")
print(f"LUA : {lua_path}")
print(f"PS1 : {ps1_path}")
print(f"BAT : {bat_path}")
print(f"VBS : {vbs_path}")

print("")
print("⚠ IMPORTANTE ⚠")
print("")
print("O monitor agora roda continuamente em background.")
print("O Rainmeter inicia automaticamente o monitor.")
print("")
