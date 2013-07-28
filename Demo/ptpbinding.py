import ctypes
dllHandle = ctypes.cdll.LoadLibrary('C:/Python27/Lib/site-packages/ConsoleApplication3.dll')
vulnOverflow = dllHandle[2]
vulnFormat = dllHandle[1]
vulnOverflow.argtypes = [ctypes.c_char_p]
vulnFormat.argtypes = [ctypes.c_char_p]	