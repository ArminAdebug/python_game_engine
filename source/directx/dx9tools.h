#pragma once
#include <d3d9.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C"
{
#endif

    __declspec(dllexport) long init_d3d9(HWND hwnd);
    __declspec(dllexport) void shutdown_d3d9();

    // ایجاد تکسچر از پیکسل‌های ARGB32
    __declspec(dllexport)
    IDirect3DTexture9 *
    create_texture_from_pixels(
        const void *pixels,
        int width,
        int height,
        int pitchBytes);

    // آزادسازی تکسچر
    __declspec(dllexport) void release_texture(IDirect3DTexture9 *tex);

    // کشیدن تکسچر روی صفحه
    __declspec(dllexport) void draw_texture(IDirect3DTexture9 *tex, int x, int y, int w, int h);

    // پاک کردن صفحه با رنگ
    __declspec(dllexport) void clear_color(uint32_t argb);

    // سوییچ فریم
    __declspec(dllexport) void present();

#ifdef __cplusplus
}
#endif
