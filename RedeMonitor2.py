import tkinter as tk
from tkinter import ttk, messagebox

import configparser
import os
import re
import subprocess
import urllib.request
import urllib.error

DIALOG_WIDTH = 420
DIALOG_HEIGHT = 200

# ==========================================
# PATHS - ABA "REDEMONITOR" 
# ==========================================

INI_FILE = os.path.expanduser(r"~\Documents\Rainmeter\Scripts\devices.ini")
EXE_NAME = "RedeMonitor.exe"

# ==================================================================
# PATHS - ABA "SEVASTOLINK"
# ==================================================================
# Estrutura de uma skin do Rainmeter: Skins\<NomeDaSkin>\arquivo.ini
# Por isso o ServerMonitor.ini fica dentro de Skins\ServerMonitor,
# e não direto em Skins. 
# Scripts e @Resources seguem a mesma raiz.

SKINS_ROOT = os.path.expanduser(r"~\Documents\Rainmeter\Skins")
SKIN_DIR = os.path.join(SKINS_ROOT, "ServerMonitor")
SCRIPTS_DIR = os.path.join(SKIN_DIR, "Scripts")
RESOURCES_DIR = os.path.join(SKIN_DIR, "@Resources")

SKIN_INI_PATH = os.path.join(SKIN_DIR, "ServerMonitor.ini")
BAT_PATH = os.path.join(SCRIPTS_DIR, "start_api.bat")
VBS_PATH = os.path.join(SCRIPTS_DIR, "run_hidden.vbs")
PS1_PATH = os.path.join(SCRIPTS_DIR, "update_api.ps1")

# Campos que o ServerMonitor.ini le do api.txt (via regex nas [Measure*]).
# Servem para validar se o endereço digitado realmente devolve o formato
# que a skin espera antes de gravar qualquer arquivo.
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
' Abre o update_api.ps1 com zero janelas visiveis.
' Usa WScript.Shell.Run com o parametro 0, que esconde
' a janela por completo - diferente do "-WindowStyle
' Hidden" do PowerShell, que o Windows Terminal as
' vezes ignora.
' ----------------------------------------------------
Set fso = CreateObject("Scripting.FileSystemObject")
scriptFolder = fso.GetParentFolderName(WScript.ScriptFullName)

Set WshShell = CreateObject("WScript.Shell")
command = "powershell.exe -ExecutionPolicy Bypass -NoProfile -File """ & scriptFolder & "\update_api.ps1"""

WshShell.Run command, 0, False
'''

UPDATE_API_PS1_TEMPLATE = r"""# ----------------------------------------------------
# Antes de comecar, mata qualquer instancia anterior
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


;=========================
; SERVICES
;=========================

[Services]
Meter=String
Text="*  FILEBROWSER ONLINE      *  TAILSCALE ONLINE"
X=390
Y=290
W=780
StringAlign=Center
FontFace=#FontName#
FontSize=17
FontColor=#FontColor#
AntiAlias=1
"""

# ==========================================
# ROOT
# ==========================================

root = tk.Tk()

root.title("Side Meters Suite 1.3 - phobosfreeware.blogspot.com")
root.geometry("560x520")
root.minsize(560, 520)

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

aba_redemonitor = ttk.Frame(notebook)
aba_sevastolink = ttk.Frame(notebook)

notebook.add(aba_redemonitor, text="Status de Dispositivos")
notebook.add(aba_sevastolink, text="Status do Servidor")


# ==========================================
# ABA 1 - REDEMONITOR 
# ==========================================

def montar_aba_redemonitor(parent):

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
                "RedeMonitor.exe não encontrado."
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
        text="Configura a skin SEVASTOLINK no Rainmeter, através dos dados disponibilizados pela API do Servidor."
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
            return

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
                "Deseja gravar os arquivos mesmo assim (por exemplo, para "
                "deixar tudo pronto antes de o servidor ser ligado)?"
            )

            if not prosseguir:
                status_label.configure(foreground="#c0392b")
                status_var.set(msg)
                return

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
                return

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
            return

        status_label.configure(foreground="#0a7d2c")
        status_var.set(f"Arquivos gerados com sucesso. API: {url}")

        messagebox.showinfo(
            "Aviso",
            "Skin SEVASTOLINK configurada.\n\n"
            "Carregue/atualize a skin \"ServerMonitor\" pelo Rainmeter "
            "para que a nova configuração tenha efeito."
        )

    def atualizar():

        gerar()

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

    buttons = ttk.Frame(parent, padding=10)
    buttons.pack(fill="x", side="bottom")

    ttk.Button(buttons, text="Atualizar", command=atualizar).pack(side="right")
    ttk.Button(buttons, text="Testar Conexão", command=testar).pack(side="right", padx=5)

    carregar_endereco_atual()


montar_aba_redemonitor(aba_redemonitor)
montar_aba_sevastolink(aba_sevastolink)

# ==========================================
# START
# ==========================================

root.mainloop()
