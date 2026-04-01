#include "dx9tools.h"

static IDirect3D9*       g_d3d  = nullptr;
static IDirect3DDevice9* g_dev  = nullptr;

static D3DCOLOR to_d3dcolor(uint32_t argb) {
    return D3DCOLOR_ARGB(
        (argb >> 24) & 0xFF,
        (argb >> 16) & 0xFF,
        (argb >> 8)  & 0xFF,
        (argb)       & 0xFF
    );
}

template<typename T>
static void SafeRelease(T*& p) { if (p) { p->Release(); p=nullptr; } }

extern "C" {

long init_d3d9(HWND hwnd) {
    if (!hwnd) return E_INVALIDARG;

    g_d3d = Direct3DCreate9(D3D_SDK_VERSION);
    if (!g_d3d) return E_FAIL;

    D3DPRESENT_PARAMETERS pp = {};
    pp.Windowed = TRUE;
    pp.SwapEffect = D3DSWAPEFFECT_DISCARD;
    pp.hDeviceWindow = hwnd;
    pp.BackBufferFormat = D3DFMT_X8R8G8B8;
    pp.PresentationInterval = D3DPRESENT_INTERVAL_IMMEDIATE;

    HRESULT hr = g_d3d->CreateDevice(
        D3DADAPTER_DEFAULT, D3DDEVTYPE_HAL, hwnd,
        D3DCREATE_SOFTWARE_VERTEXPROCESSING, &pp, &g_dev
    );

    if (FAILED(hr)) {
        SafeRelease(g_d3d);
        return hr;
    }
    return S_OK;
}

long clear_color(uint32_t argb) {
    if (!g_dev) return E_FAIL;
    return g_dev->Clear(0, nullptr, D3DCLEAR_TARGET, to_d3dcolor(argb), 1.0f, 0);
}

long fill_rect(int x, int y, int w, int h, uint32_t argb) {
    if (!g_dev) return E_FAIL;
    D3DRECT r{ x, y, x+w, y+h };
    return g_dev->Clear(1, &r, D3DCLEAR_TARGET, to_d3dcolor(argb), 1.0f, 0);
}

long present(void) {
    if (!g_dev) return E_FAIL;
    return g_dev->Present(nullptr, nullptr, nullptr, nullptr);
}

void shutdown_d3d9(void) {
    SafeRelease(g_dev);
    SafeRelease(g_d3d);
}

}
