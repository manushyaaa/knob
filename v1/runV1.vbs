Dim WinScriptHost
Set WinScriptHost = CreateObject("WScript.Shell")
WinScriptHost.Run Chr(34) & "G:\arduino_serial_testing\volcon\volcon_intiator.bat" & Chr(34), 0
Set WinScriptHost = Nothing