// The following ifdef block is the standard way of creating macros which make exporting 
// from a DLL simpler. All files within this DLL are compiled with the CONSOLEAPPLICATION3_EXPORTS
// symbol defined on the command line. This symbol should not be defined on any project
// that uses this DLL. This way any other project whose source files include this file see 
// CONSOLEAPPLICATION3_API functions as being imported from a DLL, whereas this DLL sees symbols
// defined with this macro as being exported.
#ifdef CONSOLEAPPLICATION3_EXPORTS
#define CONSOLEAPPLICATION3_API __declspec(dllexport)
#else
#define CONSOLEAPPLICATION3_API __declspec(dllimport)
#endif

CONSOLEAPPLICATION3_API void overflowFunc(void);
CONSOLEAPPLICATION3_API void formatFunc(void);