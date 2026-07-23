' ----------------------------------------------------
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
