#include <windows.h>
#include <d3d9.h>
#include <wincodec.h>
#include <iostream>

#pragma comment(lib,"d3d9.lib")
#pragma comment(lib,"windowscodecs.lib")



LPDIRECT3D9 g_d3d;
LPDIRECT3DDEVICE9 g_device;
LPDIRECT3DTEXTURE9 g_texture;

struct Vertex
{
    float x,y,z,rhw;
    float u,v;
};

#define FVF (D3DFVF_XYZRHW | D3DFVF_TEX1)

Vertex quad[4];


// ============================
// Direct3D initialization
// ============================

bool InitD3D(HWND hwnd)
{
    g_d3d = Direct3DCreate9(D3D_SDK_VERSION);

    D3DPRESENT_PARAMETERS pp = {};
    pp.Windowed = TRUE;
    pp.SwapEffect = D3DSWAPEFFECT_DISCARD;
    pp.BackBufferFormat = D3DFMT_UNKNOWN;

    if(FAILED(
        g_d3d->CreateDevice(
            D3DADAPTER_DEFAULT,
            D3DDEVTYPE_HAL,
            hwnd,
            D3DCREATE_SOFTWARE_VERTEXPROCESSING,
            &pp,
            &g_device)))
    {
        return false;
    }

    return true;
}


// ============================
// IMAGE LOADING (WIC)
// ============================
bool LoadTexture(LPCWSTR filename)
{
    HRESULT hr;

    IWICImagingFactory* factory = NULL;
    IWICBitmapDecoder* decoder = NULL;
    IWICBitmapFrameDecode* frame = NULL;
    IWICFormatConverter* converter = NULL;

    std::wcout << L"Loading texture: " << filename << std::endl;

    hr = CoInitialize(NULL);
    if(FAILED(hr))
    {
        std::cout << "CoInitialize failed\n";
        return false;
    }

    hr = CoCreateInstance(
        CLSID_WICImagingFactory,
        NULL,
        CLSCTX_INPROC_SERVER,
        IID_PPV_ARGS(&factory)
    );

    if(FAILED(hr))
    {
        std::cout << "WIC factory creation failed\n";
        return false;
    }

    hr = factory->CreateDecoderFromFilename(
        filename,
        NULL,
        GENERIC_READ,
        WICDecodeMetadataCacheOnLoad,
        &decoder
    );

    if(FAILED(hr))
    {
        std::cout << "Image file not found or cannot open\n";
        factory->Release();
        return false;
    }

    hr = decoder->GetFrame(0,&frame);
    if(FAILED(hr))
    {
        std::cout << "Failed to get image frame\n";
        decoder->Release();
        factory->Release();
        return false;
    }

    hr = factory->CreateFormatConverter(&converter);
    if(FAILED(hr))
    {
        std::cout << "Format converter creation failed\n";
        frame->Release();
        decoder->Release();
        factory->Release();
        return false;
    }

    hr = converter->Initialize(
        frame,
        GUID_WICPixelFormat32bppBGRA,
        WICBitmapDitherTypeNone,
        NULL,
        0.0,
        WICBitmapPaletteTypeCustom
    );

    if(FAILED(hr))
    {
        std::cout << "Image format conversion failed\n";
        converter->Release();
        frame->Release();
        decoder->Release();
        factory->Release();
        return false;
    }

    UINT width,height;

    hr = converter->GetSize(&width,&height);

    if(FAILED(hr))
    {
        std::cout << "Failed to get image size\n";
        converter->Release();
        frame->Release();
        decoder->Release();
        factory->Release();
        return false;
    }

    std::cout << "Image loaded: " << width << " x " << height << std::endl;

    hr = g_device->CreateTexture(
        width,
        height,
        1,
        0,
        D3DFMT_A8R8G8B8,
        D3DPOOL_MANAGED,
        &g_texture,
        NULL
    );

    if(FAILED(hr))
    {
        std::cout << "Direct3D texture creation failed\n";
        converter->Release();
        frame->Release();
        decoder->Release();
        factory->Release();
        return false;
    }

    D3DLOCKED_RECT rect;

    hr = g_texture->LockRect(0,&rect,NULL,0);

    if(FAILED(hr))
    {
        std::cout << "Texture lock failed\n";
        converter->Release();
        frame->Release();
        decoder->Release();
        factory->Release();
        return false;
    }

    hr = converter->CopyPixels(
        NULL,
        rect.Pitch,
        rect.Pitch * height,
        (BYTE*)rect.pBits
    );

    g_texture->UnlockRect(0);

    if(FAILED(hr))
    {
        std::cout << "CopyPixels failed\n";
        converter->Release();
        frame->Release();
        decoder->Release();
        factory->Release();
        return false;
    }

    converter->Release();
    frame->Release();
    decoder->Release();
    factory->Release();

    std::cout << "Texture created successfully\n";

    return true;
}


// ============================
// Quad setup
// ============================

void SetupQuad()
{
    quad[0] = {100,100,0,1,0,0};
    quad[1] = {500,100,0,1,1,0};
    quad[2] = {100,500,0,1,0,1};
    quad[3] = {500,500,0,1,1,1};
}


// ============================
// Rendering
// ============================

void Render()
{

    g_device->Clear(
        0,NULL,
        D3DCLEAR_TARGET,
        D3DCOLOR_XRGB(30,30,30),
        1.0f,
        0
    );

    g_device->BeginScene();

    g_device->SetFVF(FVF);

    // bind texture

    g_device->SetTextureStageState(0, D3DTSS_COLOROP, D3DTOP_MODULATE);
    g_device->SetTextureStageState(0, D3DTSS_COLORARG1, D3DTA_TEXTURE);
    g_device->SetTextureStageState(0, D3DTSS_COLORARG2, D3DTA_DIFFUSE);

    g_device->SetSamplerState(0, D3DSAMP_MINFILTER, D3DTEXF_LINEAR);
    g_device->SetSamplerState(0, D3DSAMP_MAGFILTER, D3DTEXF_LINEAR);
    g_device->SetTexture(0, g_texture);

    g_device->DrawPrimitiveUP(
        D3DPT_TRIANGLESTRIP,
        2,
        quad,
        sizeof(Vertex)
    );

    g_device->EndScene();

    g_device->Present(NULL,NULL,NULL,NULL);
    std::cout << "rendering\n";
}


// ============================
// Window proc
// ============================

LRESULT CALLBACK WndProc(HWND h,UINT m,WPARAM w,LPARAM l)
{
    if(m==WM_DESTROY)
        PostQuitMessage(0);

    return DefWindowProc(h,m,w,l);
}


// ============================
// main
// ============================

int WINAPI WinMain(
    HINSTANCE hInst,
    HINSTANCE,
    LPSTR,
    int)
{
    WNDCLASS wc={};
    wc.lpfnWndProc=WndProc;
    wc.hInstance=hInst;
    wc.lpszClassName="DX9";

    RegisterClass(&wc);

    AllocConsole();
    freopen("CONOUT$", "w", stdout);

    std::cout << "started\n";

    HWND hwnd=CreateWindow(
        "DX9",
        "Direct3D9 Texture",
        WS_OVERLAPPEDWINDOW,
        100,100,
        800,600,
        NULL,NULL,
        hInst,NULL
    );

    ShowWindow(hwnd,1);

    InitD3D(hwnd);

    if(!LoadTexture(L"F:\\docc\\armin\\+Dev\\Code\\Python\\3d test\\w\\test.png"))
    {
        std::cout << "not loaded !!!!!!!!!!!!!!\n";
    }


    SetupQuad();

    MSG msg = {};

    while(msg.message != WM_QUIT)
    {
        std::cout << "start\n";
        if(PeekMessage(&msg,NULL,0,0,PM_REMOVE))
        {
            TranslateMessage(&msg);
            DispatchMessage(&msg);
        }
        else
        {
            Render();
        }
    }

    return 0;
}
