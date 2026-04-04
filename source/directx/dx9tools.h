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

#include <d3d9.h>
#include <d3dx9.h> // حتماً باید D3DX نصب و لینک شده باشد

extern "C" {
    // تنظیم دوربین
    __declspec(dllexport) void set_camera(float posX, float posY, float posZ, 
                                         float rotX, float rotY, float rotZ, 
                                         float fovDeg);

    // کار با تصویر (Texture)
    __declspec(dllexport) IDirect3DTexture9* load_texture(const char* filename);
    __declspec(dllexport) void draw_texture(IDirect3DTexture9* tex, int x, int y, int w, int h);
}