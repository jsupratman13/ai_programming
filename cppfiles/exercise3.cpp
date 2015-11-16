//exercise3: using windows header file
#include <windows.h>
#include "wiiuse.h"

int WinMain(HINSTANCE, HINSTANCE, LPSTR, int)
{
	MessageBox(0, "Hello, Windows", "MinGW Test Program", MB_OK);
	return 0;
}
