import configparser
import ctypes
import os
import sys
import time


def detectar_portugues_brasil():
    try:
        return ctypes.windll.kernel32.GetUserDefaultUILanguage() == 0x0416
    except Exception:
        return False


IDIOMA_PT = detectar_portugues_brasil()


def tr(pt, en):
    return pt if IDIOMA_PT else en


print(tr("Fechando Rainmeter...", "Closing Rainmeter..."))

os.system("taskkill /F /IM Rainmeter.exe >nul 2>&1")

time.sleep(2)

base_path = os.path.expanduser(r"~\Documents\Rainmeter")
scripts_path = os.path.join(base_path, "Scripts")
skin_path = os.path.join(base_path, "Skins", "illustro", "NetworkDevices")

os.makedirs(scripts_path, exist_ok=True)
os.makedirs(skin_path, exist_ok=True)

old_files = [
    os.path.join(scripts_path, "check_network.ps1"),
    os.path.join(scripts_path, "check_network.bat"),
    os.path.join(scripts_path, "start_hidden.vbs"),
    os.path.join(scripts_path, "network.lua"),
    os.path.join(base_path, "network_status.txt"),
    os.path.join(skin_path, "SideMeterDevices.ini"),
]

print("")
print(tr("Removendo arquivos antigos...", "Removing old files..."))
print("")

for file in old_files:
    if os.path.exists(file):
        try:
            os.remove(file)
            print(tr(f"REMOVIDO: {file}", f"REMOVED: {file}"))
        except Exception as e:
            print(tr(f"ERRO AO REMOVER {file}: {e}", f"ERROR REMOVING {file}: {e}"))

devices_ini = os.path.join(scripts_path, "devices.ini")

if not os.path.exists(devices_ini):
    config = configparser.ConfigParser()

    config["PC1"] = {"ip": "192.168.0.10"}
    config["PC2"] = {"ip": "192.168.0.20"}

    with open(devices_ini, "w") as f:
        config.write(f)

    print("")
    print(tr("devices.ini criado!", "devices.ini created!"))
    print(tr("Edite o arquivo e execute novamente.", "Edit the file and run it again."))
    print("")

    sys.exit()

config = configparser.ConfigParser()
config.read(devices_ini)

devices = []

for section in config.sections():
    name = section
    ip = config[section]["ip"]

    devices.append((name, ip))

print("")
print(tr("Gerando PowerShell...", "Generating PowerShell..."))
print("")

ps_lines = []

ps_lines.append('$mutex = New-Object System.Threading.Mutex($false, "SideMeterDevicesMutex")')
ps_lines.append("if (-not $mutex.WaitOne(0, $false)) { exit }")
ps_lines.append("")

ps_lines.append("while ($true)")
ps_lines.append("{")

for i, (_, ip) in enumerate(devices, start=1):
    if ":" in ip:
        host, porta = ip.rsplit(":", 1)

        ps_lines.append(
            f'    $pc{i} = if (Test-NetConnection "{host}" -Port {porta} '
            f'-InformationLevel Quiet) {{ "ONLINE" }} else {{ "OFFLINE" }}'
        )

    else:
        ps_lines.append(f'    $pc{i} = "OFFLINE"')
        ps_lines.append(f'    if (Test-Connection "{ip}" -Count 1 -Quiet -ErrorAction SilentlyContinue) {{')
        ps_lines.append(f'        $pc{i} = "ONLINE"')
        ps_lines.append("    } else {")
        ps_lines.append("        try {")
        ps_lines.append(
            f'            $resolvido{i} = [System.Net.Dns]::GetHostAddresses("{ip}") | '
            "Select-Object -First 1 -ExpandProperty IPAddressToString"
        )
        ps_lines.append(
            f"            if ($resolvido{i} -and "
            f"(Test-Connection $resolvido{i} -Count 1 -Quiet -ErrorAction SilentlyContinue)) {{"
        )
        ps_lines.append(f'                $pc{i} = "ONLINE"')
        ps_lines.append("            }")
        ps_lines.append("        } catch {}")
        ps_lines.append("    }")
        ps_lines.append("")

ps_output = "`n".join(f"$pc{i}" for i in range(1, len(devices) + 1))

ps_lines.append("")
ps_lines.append(f'    $status = "{ps_output}"')
ps_lines.append(
    '    $status | Out-File "$env:USERPROFILE\\Documents\\Rainmeter\\network_status.tmp" -Encoding ASCII'
)
ps_lines.append(
    '    Move-Item "$env:USERPROFILE\\Documents\\Rainmeter\\network_status.tmp" '
    '"$env:USERPROFILE\\Documents\\Rainmeter\\network_status.txt" -Force'
)
ps_lines.append("")
ps_lines.append("    Start-Sleep -Seconds 5")
ps_lines.append("}")

ps_script = "\n".join(ps_lines)

ps1_path = os.path.join(scripts_path, "check_network.ps1")

with open(ps1_path, "w", encoding="utf-8-sig", newline="\r\n") as f:
    f.write(ps_script)

print(tr("Gerando BAT...", "Generating BAT..."))

bat_content = r"""@echo off

start "" /B powershell -WindowStyle Hidden -ExecutionPolicy Bypass -File "%USERPROFILE%\Documents\Rainmeter\Scripts\check_network.ps1"
"""

bat_path = os.path.join(scripts_path, "check_network.bat")

with open(bat_path, "w", encoding="utf-8") as f:
    f.write(bat_content)

print(tr("Gerando VBS...", "Generating VBS..."))

vbs_content = r"""Set WshShell = CreateObject("WScript.Shell")

batPath = WshShell.ExpandEnvironmentStrings("%USERPROFILE%") & "\Documents\Rainmeter\Scripts\check_network.bat"

WshShell.Run chr(34) & batPath & chr(34), 0

Set WshShell = Nothing
"""

vbs_path = os.path.join(scripts_path, "start_hidden.vbs")

with open(vbs_path, "w", encoding="utf-8") as f:
    f.write(vbs_content)

print(tr("Gerando LUA...", "Generating LUA..."))

lua_txt_path = (base_path + "\\network_status.txt").replace("\\", "\\\\")

lua_lines = [
    "function Initialize()",
    f'    path = "{lua_txt_path}"',
    "end",
    "",
    "function Update()",
    '    local file = io.open(path, "r")',
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
    "",
]

for i in range(1, len(devices) + 1):
    lua_lines.extend([
        f"    if lines[{i}] then",
        f'        SKIN:Bang("!SetOption", "meterPC{i}Status", "Text", lines[{i}])',
        f'        if lines[{i}] == "ONLINE" then',
        f'            SKIN:Bang("!SetOption", "meterPC{i}Status", "FontColor", "0,255,0,255")',
        "        else",
        f'            SKIN:Bang("!SetOption", "meterPC{i}Status", "FontColor", "255,80,80,255")',
        "        end",
        "    end",
        "",
    ])

lua_lines.extend([
    '    SKIN:Bang("!UpdateMeter", "*")',
    '    SKIN:Bang("!Redraw")',
    "end",
])

lua_path = os.path.join(scripts_path, "network.lua")

with open(lua_path, "w", encoding="utf-8") as f:
    f.write("\n".join(lua_lines))

print(tr("Gerando INI...", "Generating INI..."))

ini_lines = [
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
    "",
    "[Metadata]",
    "Name=Network Devices",
    "Author=Phobos",
    "Version=FINAL-PERSISTENT",
    "",
    "[Variables]",
    "fontName=Segoe UI",
    "textSize=8",
    "colorText=255,255,255,205",
    "",
    "[LuaScript]",
    "Measure=Script",
    f"ScriptFile={lua_path}",
    "UpdateDivider=1",
    "",
    "[styleTitle]",
    "StringAlign=Center",
    "StringCase=Upper",
    "StringStyle=Bold",
    "FontColor=#colorText#",
    "FontFace=#fontName#",
    "FontSize=10",
    "AntiAlias=1",
    "",
    "[styleLeftText]",
    "StringAlign=Left",
    "StringStyle=Bold",
    "FontColor=#colorText#",
    "FontFace=#fontName#",
    "FontSize=#textSize#",
    "AntiAlias=1",
    "",
    "[styleRightText]",
    "StringAlign=Right",
    "StringStyle=Bold",
    "FontFace=#fontName#",
    "FontSize=#textSize#",
    "AntiAlias=1",
    "",
    "[meterTitle]",
    "Meter=String",
    "MeterStyle=styleTitle",
    "X=100",
    "Y=12",
    "W=190",
    f"Text={tr('Dispositivos', 'Devices')}",
    "",
]

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
        "",
    ])

    y += 20

ini_path = os.path.join(skin_path, "SideMeterDevices.ini")

with open(ini_path, "w", encoding="utf-8") as f:
    f.write("\n".join(ini_lines))

print("")
print(tr("Abrindo Rainmeter...", "Opening Rainmeter..."))
print("")

rainmeter_path = r"C:\Program Files\Rainmeter\Rainmeter.exe"

if os.path.exists(rainmeter_path):
    os.startfile(rainmeter_path)

    time.sleep(3)

    os.system(f'"{rainmeter_path}" !ActivateConfig "illustro\\NetworkDevices" "SideMeterDevices.ini"')

print("")
print("====================================")
print(tr("✅ SideMeterDevices gerado com sucesso!", "✅ SideMeterDevices generated successfully!"))
print("====================================")
print("")

print(f"INI : {ini_path}")
print(f"LUA : {lua_path}")
print(f"PS1 : {ps1_path}")
print(f"BAT : {bat_path}")
print(f"VBS : {vbs_path}")

print("")
print(tr("⚠ IMPORTANTE ⚠", "⚠ IMPORTANT ⚠"))
print("")
print(tr(
    "O monitor agora roda continuamente em background.",
    "The monitor now runs continuously in the background.",
))
print(tr(
    "O Rainmeter inicia automaticamente o monitor.",
    "Rainmeter starts the monitor automatically.",
))
print("")
