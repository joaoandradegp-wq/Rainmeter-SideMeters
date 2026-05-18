import tkinter as tk
from tkinter import ttk, messagebox
import configparser
import os
import subprocess

DIALOG_WIDTH = 420
DIALOG_HEIGHT = 200

# ==========================================
# PATHS
# ==========================================

INI_FILE = os.path.expanduser(
    r"~\Documents\Rainmeter\Scripts\devices.ini"
)

EXE_NAME = "RedeMonitor.exe"

# ==========================================
# ROOT
# ==========================================

root = tk.Tk()

root.title("RedeMonitor - Side Meters Suite 1.0")

root.geometry("750x500")

root.minsize(
    650,
    450
)

# ==========================================
# HEADER
# ==========================================

header = ttk.Frame(
    root,
    padding=10
)

header.pack(
    fill="x"
)

title = ttk.Label(
    header,
    text="RedeMonitor",
    font=(
        "Segoe UI",
        16,
        "bold"
    )
)

title.pack(
    anchor="w"
)

subtitle = ttk.Label(
    header,
    text="Gerenciamento de dispositivos monitorados pelo Rainmeter usando Side Meters Suite"
)

subtitle.pack(
    anchor="w"
)

# ==========================================
# TABLE
# ==========================================

frame_table = ttk.Frame(
    root,
    padding=10
)

frame_table.pack(
    fill="both",
    expand=True
)

columns = (
    "nome",
    "ip"
)

tree = ttk.Treeview(
    frame_table,
    columns=columns,
    show="headings"
)

tree.heading(
    "nome",
    text="Dispositivo"
)

tree.heading(
    "ip",
    text="IP / Host / DDNS"
)

tree.column(
    "nome",
    width=250
)

tree.column(
    "ip",
    width=350
)

scroll = ttk.Scrollbar(
    frame_table,
    orient="vertical",
    command=tree.yview
)

tree.configure(
    yscrollcommand=scroll.set
)

tree.pack(
    side="left",
    fill="both",
    expand=True
)

scroll.pack(
    side="right",
    fill="y"
)

# ==========================================
# LOAD
# ==========================================

def carregar():

    tree.delete(
        *tree.get_children()
    )

    if not os.path.exists(
        INI_FILE
    ):

        return

    cfg = configparser.ConfigParser()

    cfg.read(
        INI_FILE,
        encoding="utf-8"
    )

    for sec in cfg.sections():

        ip = cfg[sec].get(
            "ip",
            ""
        )

        tree.insert(
            "",
            "end",
            values=(
                sec,
                ip
            )
        )

# ==========================================
# ADD
# ==========================================

def adicionar():

    win = tk.Toplevel(root)

    win.title(
        "Adicionar"
    )

    largura = DIALOG_WIDTH
    altura = DIALOG_HEIGHT

    root.update_idletasks()

    x = (
        root.winfo_x()
        + root.winfo_width() // 2
        - largura // 2
    )

    y = (
        root.winfo_y()
        + root.winfo_height() // 2
        - altura // 2
    )

    win.geometry(
        f"{largura}x{altura}+{x}+{y}"
    )

    win.resizable(
        False,
        False
    )

    win.transient(root)

    win.grab_set()

    frame = ttk.Frame(
        win,
        padding=20
    )

    frame.pack(
        fill="both",
        expand=True
    )

    ttk.Label(
        frame,
        text="Nome do dispositivo:"
    ).pack(
        anchor="w"
    )

    en_nome = ttk.Entry(
        frame
    )

    en_nome.pack(
        fill="x",
        pady=(5,8)
    )

    ttk.Label(
        frame,
        text="IP / Host / DDNS:"
    ).pack(
        anchor="w"
    )

    en_ip = ttk.Entry(
        frame
    )

    en_ip.pack(
        fill="x",
        pady=(5,8)
    )

    btns = ttk.Frame(
        win
    )

    btns.pack(
        side="bottom",
        fill="x",
        padx=20,
        pady=12
    )

    def salvar():

        nome = en_nome.get().strip()

        ip = en_ip.get().strip()

        if not nome:

            messagebox.showwarning(
                "Aviso",
                "Informe o nome"
            )

            return

        if not ip:

            messagebox.showwarning(
                "Aviso",
                "Informe IP ou host"
            )

            return

        tree.insert(
            "",
            "end",
            values=(
                nome,
                ip
            )
        )

        win.destroy()

    ttk.Button(
        btns,
        text="Cancelar",
        command=win.destroy
    ).pack(
        side="right"
    )

    ttk.Button(
        btns,
        text="Salvar",
        command=salvar
    ).pack(
        side="right",
        padx=5
    )

    en_nome.focus()

    win.bind(
        "<Return>",
        lambda e: salvar()
    )

    win.bind(
        "<Escape>",
        lambda e: win.destroy()
    )


# ==========================================
# EDIT
# ==========================================

def editar():

    sel = tree.selection()

    if not sel:
        return

    item = sel[0]

    nome_old, ip_old = tree.item(
        item
    )["values"]

    win = tk.Toplevel(root)

    win.title(
        "Editar"
    )

    largura = DIALOG_WIDTH
    altura = DIALOG_HEIGHT

    root.update_idletasks()

    x = (
        root.winfo_x()
        + root.winfo_width() // 2
        - largura // 2
    )

    y = (
        root.winfo_y()
        + root.winfo_height() // 2
        - altura // 2
    )

    win.geometry(
        f"{largura}x{altura}+{x}+{y}"
    )

    win.resizable(
        False,
        False
    )

    win.transient(root)

    win.grab_set()

    frame = ttk.Frame(
        win,
        padding=20
    )

    frame.pack(
        fill="both",
        expand=True
    )

    ttk.Label(
        frame,
        text="Nome do dispositivo:"
    ).pack(
        anchor="w"
    )

    en_nome = ttk.Entry(
        frame
    )

    en_nome.insert(
        0,
        nome_old
    )

    en_nome.pack(
        fill="x",
        pady=(5,8)
    )

    ttk.Label(
        frame,
        text="IP / Host / DDNS:"
    ).pack(
        anchor="w"
    )

    en_ip = ttk.Entry(
        frame
    )

    en_ip.insert(
        0,
        ip_old
    )

    en_ip.pack(
        fill="x",
        pady=(5,8)
    )

    btns = ttk.Frame(
        win
    )

    btns.pack(
        side="bottom",
        fill="x",
        padx=20,
        pady=12
    )

    def salvar():

        tree.item(
            item,
            values=(
                en_nome.get().strip(),
                en_ip.get().strip()
            )
        )

        win.destroy()

    ttk.Button(
        btns,
        text="Cancelar",
        command=win.destroy
    ).pack(
        side="right"
    )

    ttk.Button(
        btns,
        text="Salvar",
        command=salvar
    ).pack(
        side="right",
        padx=5
    )

    en_nome.focus()

    win.bind(
        "<Return>",
        lambda e: salvar()
    )

    win.bind(
        "<Escape>",
        lambda e: win.destroy()
    )

# ==========================================
# REMOVE
# ==========================================

def remover():

    sel = tree.selection()

    for item in sel:

        tree.delete(
            item
        )

# ==========================================
# SAVE
# ==========================================

def salvar_ini():

    pasta = os.path.dirname(
        INI_FILE
    )

    os.makedirs(
        pasta,
        exist_ok=True
    )

    cfg = configparser.ConfigParser()

    for item in tree.get_children():

        nome, ip = tree.item(
            item
        )["values"]

        cfg[nome] = {
            "ip": ip
        }

    with open(
        INI_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        cfg.write(f)

    messagebox.showinfo(
        "OK",
        "Configuração salva."
    )

# ==========================================
# EXEC
# ==========================================

def atualizar():

    salvar_ini()

    exe_path = os.path.join(
        os.getcwd(),
        EXE_NAME
    )

    if not os.path.exists(
        exe_path
    ):

        messagebox.showerror(
            "Erro",
            "RedeMonitor.exe não encontrado."
        )

        return

    subprocess.Popen(
        [exe_path]
    )

# ==========================================
# BUTTONS
# ==========================================

buttons = ttk.Frame(
    root,
    padding=10
)

buttons.pack(
    fill="x"
)

ttk.Button(
    buttons,
    text="Adicionar",
    command=adicionar
).pack(
    side="left",
    padx=5
)

ttk.Button(
    buttons,
    text="Editar",
    command=editar
).pack(
    side="left",
    padx=5
)

ttk.Button(
    buttons,
    text="Remover",
    command=remover
).pack(
    side="left",
    padx=5
)

ttk.Button(
    buttons,
    text="Atualizar",
    command=atualizar
).pack(
    side="right"
)

# ==========================================
# START
# ==========================================

carregar()

root.mainloop()
