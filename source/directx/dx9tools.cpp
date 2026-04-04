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

// متغیرهای سراسری که قبلاً داشتی
extern IDirect3DDevice9* g_dev; 

// ۱. تابع تنظیم کامل دوربین
void set_camera(float posX, float posY, float posZ, float rotX, float rotY, float rotZ, float fovDeg) {
    if (!g_dev) return;

    // ماتریس View (موقعیت و چرخش)
    D3DXMATRIX matView, matRot;
    D3DXVECTOR3 eye(posX, posY, posZ);
    D3DXVECTOR3 lookAt(0, 0, 1); // جهت نگاه پیش‌فرض
    D3DXVECTOR3 up(0, 1, 0);

    // اعمال چرخش
    D3DXMatrixRotationYawPitchRoll(&matRot, rotY, rotX, rotZ);
    D3DXVec3TransformNormal(&lookAt, &lookAt, &matRot);
    lookAt += eye;

    D3DXMatrixLookAtLH(&matView, &eye, &lookAt, &up);
    g_dev->SetTransform(D3DTS_VIEW, &matView);

    // ماتریس Projection (FOV)
    D3DXMATRIX matProj;
    float aspect = 1.33f; // معمولاً باید نسبت عرض به ارتفاع پنجره باشد
    float fovRad = fovDeg * (D3DX_PI / 180.0f); // تبدیل درجه به رادیان
    D3DXMatrixPerspectiveFovLH(&matProj, fovRad, aspect, 1.0f, 1000.0f);
    g_dev->SetTransform(D3DTS_PROJECTION, &matProj);
}

// ۲. لود کردن عکس (Texture)
IDirect3DTexture9* load_texture(const char* filename) {
    IDirect3DTexture9* tex = nullptr;
    D3DXCreateTextureFromFileA(g_dev, filename, &tex);
    return tex;
}

// ۳. نمایش عکس روی صفحه
void draw_texture(IDirect3DTexture9* tex, int x, int y, int w, int h) {
    if (!g_dev || !tex) return;

    ID3DXSprite* sprite;
    D3DXCreateSprite(g_dev, &sprite);

    sprite->Begin(D3DXSPRITE_ALPHABLEND);
    D3DXVECTOR3 pos((float)x, (float)y, 0.0f);
    
    // تنظیم اندازه (Scale) اگر لازم بود اینجا ماتریس اسکیل بدید
    sprite->Draw(tex, NULL, NULL, &pos, 0xFFFFFFFF);
    
    sprite->End();
    sprite->Release();
}