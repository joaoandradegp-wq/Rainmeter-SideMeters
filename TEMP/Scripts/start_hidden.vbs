Set WshShell = CreateObject("WScript.Shell")

batPath = WshShell.ExpandEnvironmentStrings("%USERPROFILE%") & "\Documents\Rainmeter\Scripts\check_network.bat"

WshShell.Run chr(34) & batPath & chr(34), 0

Set WshShell = Nothing
