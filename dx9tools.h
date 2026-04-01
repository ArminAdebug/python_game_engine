#pragma once
#include <windows.h>
#include <d3d9.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

__declspec(dllexport) long init_d3d9(HWND hwnd);
__declspec(dllexport) long clear_color(uint32_t argb);
__declspec(dllexport) long fill_rect(int x, int y, int w, int h, uint32_t argb);
__declspec(dllexport) long present(void);
__declspec(dllexport) void shutdown_d3d9(void);

#ifdef __cplusplus
}
#endif
