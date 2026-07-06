Set objShell = CreateObject("Wscript.Shell")
objShell.Run "powershell.exe -ExecutionPolicy Bypass -File """ & Replace(WScript.ScriptFullName,"RunLinkSpeed.vbs","LinkSpeed.ps1") & """", 0, True