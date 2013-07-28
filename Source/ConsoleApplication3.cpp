// ConsoleApplication3.cpp : Defines the exported functions for the DLL application.
//

#include "stdafx.h"
#include "stdio.h"
#include "ConsoleApplication3.h"


CONSOLEAPPLICATION3_API void overflowFunc(char *userInput)
{
	char *handle = new char [32];
	strcpy(handle, userInput);
	return;
}

CONSOLEAPPLICATION3_API void formatFunc(char *userInput)
{
	printf(userInput);
	return;
}