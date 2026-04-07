#include <d3d9.h>
#include <stdint.h>
#include <cstring>
#include <windows.h>
#include <iostream>
#include <stdio.h>
#include <fstream>

#pragma comment(lib, "d3d9.lib")
#pragma comment(lib, "user32.lib")
#pragma comment(lib, "gdi32.lib")

void log()
{
    std::ofstream f("debug.txt", std::ios::app);
    f << "hello from dll\n";
    f.close();
}
// --- Globals ---



static IDirect3D9 *g_d3d = nullptr;
static IDirect3DDevice9 *g_dev = nullptr;

struct TLVERTEX
{
    float x, y, z, rhw;
    float u, v;
};

#define FVF (D3DFVF_XYZRHW | D3DFVF_TEX1)

// یک vertex ساده برای quad 2D
struct Vertex2D
{
    float x, y, z, rhw;
    D3DCOLOR color;
    float u, v;
};

template <typename T>
static void SafeRelease(T *&p)
{
    if (p)
    {
        p->Release();
        p = nullptr;
    }
}

static D3DCOLOR to_d3dcolor(uint32_t argb)
{
    return D3DCOLOR_ARGB(
        (argb >> 24) & 0xFF,
        (argb >> 16) & 0xFF,
        (argb >> 8) & 0xFF,
        (argb) & 0xFF);
}

struct Vertex
{
    float x,y,z,rhw;
    float u,v;
};



// --- C API ---
extern "C"
{
    void PrintHR(const char* msg, HRESULT hr)
    {
        std::cout << msg << hr << "\n";
    }
    // init_d3d9: ایجاد device
    __declspec(dllexport) long init_d3d9(HWND hwnd)
    {

        if (!hwnd)
            return E_INVALIDARG;

        if (g_dev)
        {
            // قبلاً init شده
            return S_OK;
        }

        g_d3d = Direct3DCreate9(D3D_SDK_VERSION);
        if (!g_d3d)
            return E_FAIL;

        D3DPRESENT_PARAMETERS pp = {};
        pp.Windowed = TRUE;
        pp.SwapEffect = D3DSWAPEFFECT_DISCARD;
        pp.hDeviceWindow = hwnd;
        pp.BackBufferFormat = D3DFMT_X8R8G8B8;
        pp.PresentationInterval = D3DPRESENT_INTERVAL_IMMEDIATE;

        HRESULT hr = g_d3d->CreateDevice(
            D3DADAPTER_DEFAULT,
            D3DDEVTYPE_HAL,
            hwnd,
            D3DCREATE_SOFTWARE_VERTEXPROCESSING,
            &pp,
            &g_dev);

        if (FAILED(hr))
        {
            SafeRelease(g_d3d);
            return hr;
        }

        g_dev->SetRenderState(D3DRS_LIGHTING, FALSE);
        g_dev->SetRenderState(D3DRS_ZENABLE, FALSE);
        g_dev->SetRenderState(D3DRS_ALPHABLENDENABLE, TRUE);
        g_dev->SetRenderState(D3DRS_SRCBLEND, D3DBLEND_SRCALPHA);
        g_dev->SetRenderState(D3DRS_DESTBLEND, D3DBLEND_INVSRCALPHA);
        g_dev->SetSamplerState(0, D3DSAMP_MINFILTER, D3DTEXF_LINEAR);
        g_dev->SetSamplerState(0, D3DSAMP_MAGFILTER, D3DTEXF_LINEAR);
        g_dev->SetSamplerState(0, D3DSAMP_MIPFILTER, D3DTEXF_NONE);

        return S_OK;
    }

    __declspec(dllexport) void shutdown_d3d9(void)
    {
        SafeRelease(g_dev);
        SafeRelease(g_d3d);
    }

    __declspec(dllexport) long clear_color(uint32_t argb)
    {
        if (!g_dev)
            return E_FAIL;
        return g_dev->Clear(0, nullptr, D3DCLEAR_TARGET, to_d3dcolor(argb), 1.0f, 0);
    }

    __declspec(dllexport) long fill_rect(int x, int y, int w, int h, uint32_t argb)
    {
        if (!g_dev)
            return E_FAIL;
        D3DRECT r{x, y, x + w, y + h};
        return g_dev->Clear(1, &r, D3DCLEAR_TARGET, to_d3dcolor(argb), 1.0f, 0);
    }

    __declspec(dllexport) long present(void)
    {
        if (!g_dev)
            return E_FAIL;
        return g_dev->Present(nullptr, nullptr, nullptr, nullptr);
    }

    __declspec(dllexport) long begin_scene()
    {
        if (!g_dev)
            return E_FAIL;
        return g_dev->BeginScene();
    }

    __declspec(dllexport) long end_scene()
    {
        if (!g_dev)
            return E_FAIL;
        return g_dev->EndScene();
    }

    // ------------------------------------------------
    // create texture from ARGB numpy
    // ------------------------------------------------
    __declspec(dllexport)
    IDirect3DTexture9 *
    create_texture_argb(
        const uint8_t *pixels,
        int width,
        int height,
        int pitchBytes)
        {


        if (!g_dev || !pixels){
            std::cout << "device or pixels is null\n";
            return nullptr;
        }

        IDirect3DTexture9 *tex = nullptr;

        HRESULT hr = g_dev->CreateTexture(
            width,
            height,
            1,
            0,
            D3DFMT_A8R8G8B8,
            D3DPOOL_MANAGED,
            &tex,
            NULL);

        if (FAILED(hr) || !tex){
            PrintHR("bad input texture", hr);
            return nullptr;
        }

        D3DLOCKED_RECT lr;
        hr = tex->LockRect(0, &lr, nullptr, 0);

        if (FAILED(hr)){
            PrintHR("locking rect failed", hr);
            return nullptr;
        }

        const uint8_t *src = (const uint8_t *)pixels;
        uint8_t *dst = (uint8_t *)lr.pBits;

        int row = width * 4;

        for (int y = 0; y < height; y++)
        {
            memcpy(
                dst + y * lr.Pitch,
                src + y * pitchBytes,
                row);
        }

        hr = tex->UnlockRect(0);
        if (!tex){
            PrintHR("texture pointer is null", hr);

            return nullptr;
        }
        std::cout << "width=" << width
                << " height=" << height
                << " pitch=" << pitchBytes
                << std::endl;

        return tex;
    }

    // ------------------------------------------------
    // draw texture on rectangle
    // ------------------------------------------------
    __declspec(dllexport) void draw_texture_rect(
        IDirect3DTexture9 *tex,
        float x,
        float y,
        float w,
        float h)
{
    if(!tex){
        std::cout << "texture null\n";
        return;
    }
    float x2 = x + w;
    float y2 = y + h;
    Vertex quad[4];

    quad[0] = {x, y, 0, 1, 0, 0};
    quad[1] = {x2, y, 0, 1, 1, 0};
    quad[2] = {x, y2, 0, 1, 0, 1};
    quad[3] = {x2, y2, 0, 1, 1, 1};

    g_dev->SetFVF(FVF);

    g_dev->SetTextureStageState(0, D3DTSS_COLOROP, D3DTOP_SELECTARG1);
    g_dev->SetTextureStageState(0, D3DTSS_COLORARG1, D3DTA_TEXTURE);


    g_dev->SetSamplerState(0, D3DSAMP_MINFILTER, D3DTEXF_LINEAR);
    g_dev->SetSamplerState(0, D3DSAMP_MAGFILTER, D3DTEXF_LINEAR);
    g_dev->SetTexture(0, tex);

    HRESULT hr = g_dev->DrawPrimitiveUP(
        D3DPT_TRIANGLESTRIP,
        2,
        quad,
        sizeof(Vertex)
    );

    if (FAILED(hr)){
        PrintHR("rendering failed", hr);
        return;
    }

    std::cout << "rendering\n";
}

}

