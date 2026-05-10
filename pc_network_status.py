import os

# ==========================================
# PATHS
# ==========================================

base_path = os.path.expanduser(r"~\Documents\Rainmeter")

scripts_path = os.path.join(base_path, "Scripts")

skin_path = os.path.join(
    base_path,
    "Skins",
    "illustro",
    "NetworkDevices"
)

os.makedirs(scripts_path, exist_ok=True)
os.makedirs(skin_path, exist_ok=True)

# ==========================================
# REMOVE ARQUIVOS ANTIGOS
# ==========================================

old_files = [
    os.path.join(scripts_path, "check_network.ps1"),
    os.path.join(scripts_path, "check_network.bat"),
    os.path.join(scripts_path, "network.lua"),
    os.path.join(base_path, "network_status.txt"),
    os.path.join(skin_path, "RedeMonitor.ini"),
]

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

devices = [
    ("VIVIANE", "192.168.100.190"),
    ("JULIA", "192.168.100.4"),
    ("SERVER", "192.168.100.34"),
]

# ==========================================
# POWERSHELL
# EXECUÇÃO ÚNICA (SEM LOOP)
# ==========================================

ps_lines = []

for i, (_, ip) in enumerate(devices, start=1):

    ps_lines.append(
        f'$pc{i} = if (Test-Connection {ip} -Count 1 -Quiet) {{ "ONLINE" }} else {{ "OFFLINE" }}'
    )

ps_output = "`n".join(
    [f"$pc{i}" for i in range(1, len(devices) + 1)]
)

ps_lines.append("")

ps_lines.append(
    f'"{ps_output}" | Out-File "$env:USERPROFILE\\Documents\\Rainmeter\\network_status.txt" -Encoding ASCII'
)

ps_script = "\n".join(ps_lines)

ps1_path = os.path.join(
    scripts_path,
    "check_network.ps1"
)

with open(ps1_path, "w", encoding="utf-8") as f:
    f.write(ps_script)

# ==========================================
# BAT
# SEM START
# ==========================================

bat_content = r'''@echo off
powershell -WindowStyle Hidden -ExecutionPolicy Bypass -File "%USERPROFILE%\Documents\Rainmeter\Scripts\check_network.ps1"
'''

bat_path = os.path.join(
    scripts_path,
    "check_network.bat"
)

with open(bat_path, "w", encoding="utf-8") as f:
    f.write(bat_content)

# ==========================================
# LUA
# ==========================================

lua_txt_path = (
    base_path + "\\network_status.txt"
).replace("\\", "\\\\")

lua_lines = []

lua_lines.append("function Initialize()")
lua_lines.append(f'    path = "{lua_txt_path}"')
lua_lines.append("end")
lua_lines.append("")

lua_lines.append("function Update()")

lua_lines.append('    local file = io.open(path, "r")')

lua_lines.append("    if not file then")
lua_lines.append("        return")
lua_lines.append("    end")

lua_lines.append("")

lua_lines.append("    local lines = {}")

lua_lines.append("")

lua_lines.append("    for line in file:lines() do")
lua_lines.append("        table.insert(lines, line)")
lua_lines.append("    end")

lua_lines.append("")

lua_lines.append("    file:close()")
lua_lines.append("")

for i in range(1, len(devices) + 1):

    lua_lines.append(f"    if lines[{i}] then")

    lua_lines.append(
        f'        SKIN:Bang("!SetOption", "meterPC{i}Status", "Text", lines[{i}])'
    )

    lua_lines.append(
        f'        if lines[{i}] == "ONLINE" then'
    )

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

lua_path = os.path.join(
    scripts_path,
    "network.lua"
)

with open(lua_path, "w", encoding="utf-8") as f:
    f.write("\n".join(lua_lines))

# ==========================================
# INI
# ==========================================

ini_lines = []

ini_lines.append("[Rainmeter]")
ini_lines.append("Update=1000")
ini_lines.append("AccurateText=1")
ini_lines.append("DynamicWindowSize=1")

ini_lines.append("Background=#@#Background.png")
ini_lines.append("BackgroundMode=3")
ini_lines.append("BackgroundMargins=0,34,0,14")

ini_lines.append("Draggable=1")
ini_lines.append("ClickThrough=0")

ini_lines.append("")

# ==========================================
# METADATA
# ==========================================

ini_lines.append("[Metadata]")

ini_lines.append("Name=Network Devices")
ini_lines.append("Author=Phobos")
ini_lines.append("Version=FINAL-STABLE")

ini_lines.append("")

# ==========================================
# VARIABLES
# ==========================================

ini_lines.append("[Variables]")

ini_lines.append("fontName=Trebuchet MS")
ini_lines.append("textSize=8")

ini_lines.append(
    "colorText=255,255,255,205"
)

ini_lines.append("")

# ==========================================
# RUN SCRIPT
# ==========================================

ini_lines.append("[RunScriptTimer]")

ini_lines.append("Measure=Plugin")
ini_lines.append("Plugin=RunCommand")

ini_lines.append(
    f'Program="{bat_path}"'
)

ini_lines.append("RunCommand=1")

# EXECUTA A CADA 5 SEGUNDOS
ini_lines.append("UpdateDivider=5")

ini_lines.append("DynamicVariables=1")

ini_lines.append("")

# ==========================================
# LUA
# ==========================================

ini_lines.append("[LuaScript]")

ini_lines.append("Measure=Script")

ini_lines.append(
    f"ScriptFile={lua_path}"
)

ini_lines.append("UpdateDivider=1")

ini_lines.append("")

# ==========================================
# STYLES
# ==========================================

ini_lines.append("[styleTitle]")

ini_lines.append("StringAlign=Center")
ini_lines.append("StringCase=Upper")
ini_lines.append("StringStyle=Bold")

ini_lines.append(
    "FontColor=#colorText#"
)

ini_lines.append("FontFace=#fontName#")
ini_lines.append("FontSize=10")
ini_lines.append("AntiAlias=1")

ini_lines.append("")

ini_lines.append("[styleLeftText]")

ini_lines.append("StringAlign=Left")

ini_lines.append(
    "FontColor=#colorText#"
)

ini_lines.append("FontFace=#fontName#")

ini_lines.append(
    "FontSize=#textSize#"
)

ini_lines.append("AntiAlias=1")

ini_lines.append("")

ini_lines.append("[styleRightText]")

ini_lines.append("StringAlign=Right")

ini_lines.append("FontFace=#fontName#")

ini_lines.append(
    "FontSize=#textSize#"
)

ini_lines.append("AntiAlias=1")

ini_lines.append("")

# ==========================================
# TITLE
# ==========================================

ini_lines.append("[meterTitle]")

ini_lines.append("Meter=String")
ini_lines.append("MeterStyle=styleTitle")

ini_lines.append("X=100")
ini_lines.append("Y=12")
ini_lines.append("W=190")

ini_lines.append("Text=Dispositivos")

ini_lines.append("")

# ==========================================
# PCS
# ==========================================

y = 40

for i, (name, _) in enumerate(devices, start=1):

    ini_lines.append(f"[meterPC{i}]")

    ini_lines.append("Meter=String")

    ini_lines.append(
        "MeterStyle=styleLeftText"
    )

    ini_lines.append("X=10")

    ini_lines.append(
        f"Y={y}"
    )

    ini_lines.append(
        f"Text={name}"
    )

    ini_lines.append("")

    ini_lines.append(
        f"[meterPC{i}Status]"
    )

    ini_lines.append("Meter=String")

    ini_lines.append(
        "MeterStyle=styleRightText"
    )

    ini_lines.append("X=200")

    ini_lines.append(
        f"Y={y}"
    )

    ini_lines.append("Text=...")

    ini_lines.append(
        "DynamicVariables=1"
    )

    ini_lines.append("")

    y += 20

# ==========================================
# SAVE INI
# ==========================================

ini_path = os.path.join(
    skin_path,
    "RedeMonitor.ini"
)

with open(
    ini_path,
    "w",
    encoding="utf-8"
) as f:

    f.write("\n".join(ini_lines))

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

print("")
print("⚠ IMPORTANTE ⚠")
print("")
print("1. FECHE COMPLETAMENTE o Rainmeter")
print("2. Execute este Python")
print("3. Abra o Rainmeter")
print("4. Load RedeMonitor.ini")
print("")