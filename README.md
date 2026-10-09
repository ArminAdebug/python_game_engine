# Python Game Engine

A personal game-engine experiment built around a Python runtime and a
small native C++ rendering backend. I started this project to explore
engine architecture hands-on: how game objects own components, how
systems process those components, how scripts run during the frame loop,
and how Python can communicate with a native graphics API.

This is an experimental learning project, not a finished or
production-ready engine.

## Project Goals

The project explores the connections between several layers that are
often hidden behind an existing engine:

-   A scene and game-object model.
-   A component-based approach to attaching behavior and renderable
    data.
-   Separate systems for rendering and user scripts.
-   Transform and 3D math primitives.
-   Image loading and conversion into a GPU texture.
-   A Python-to-C++ boundary for native rendering.
-   A frame loop with timing information and a small user-script API.

The main value of the project is the implementation and integration
work, rather than a claim that it already has the breadth or stability
of a mature engine.

## Technology

-   **Python** for engine orchestration, objects, components, systems,
    and asset preparation.
-   **C++** for the native graphics bridge.
-   **Direct3D 9** for the experimental rendering backend.
-   **Win32 API** for native window creation and the window handle
    (`HWND`).
-   **`ctypes`** for calling exported functions in the native DLL.
-   **PyQt6** for the timer-driven runtime loop and Qt signal used to
    notify UI code.
-   **Pillow and NumPy** for loading images and converting pixel data.

The current implementation is Windows-specific because it uses Win32,
`ctypes.WinDLL`, and Direct3D 9.

## Architecture

``` text
GameEngine
├── Window (Win32 HWND)
├── DirectX (Python ctypes wrapper)
│   └── Native C++ DLL
│       └── Direct3D 9 device and texture drawing
├── AssetManager
│   └── Pillow -> NumPy pixel array -> GPU texture
├── Scene
│   └── GameObject
│       ├── Transform
│       ├── Sprite
│       └── Script
├── System Registry
│   ├── RenderSys
│   └── ScriptSys
└── Frame loop
    ├── ScriptSys.render() -> ScriptBehaviour.update()
    ├── RenderSys.render() -> draw sprites
    └── FrameInfo (delta time, elapsed time, frame count, FPS)
```

## Main Systems and Features

### 1. Scene and GameObject Model

A `Scene` stores its game objects and provides methods to create, list,
and search them. `GameObject` instances are intended to be created
through `Scene.new_gameobject()`, rather than constructed directly.

Each game object receives a `Transform` automatically and can have
additional components attached to it. When a component is added, it is
associated with its owning game object and passed to the system
registry.

This gives the project a foundation for separating object identity and
composition from the systems that process objects.

### 2. Component-Based Design

The base `Component` stores a reference to its owning game object. The
current component types include:

-   **`Transform`** --- position, rotation, and scale.
-   **`Sprite`** --- a texture, size, image mode, and visibility flag.
-   **`Script`** --- a path to a user-provided Python script.

The `Transform` uses a `Vector3` for position and scale, and a
`Quaternion` for rotation. It supports relative movement and rotation
updates.

### 3. System Registry

The registry maps component types to the systems that need to process
them. A `Sprite` component registers its owning game object with
`RenderSys`, while a `Script` component is registered with `ScriptSys`.

This is an early implementation of a component-to-system routing
mechanism. The registration and removal lifecycle is still an area for
improvement.

### 4. Rendering System

`RenderSys` tracks game objects that contain renderable components.
During rendering, it walks each object's components and dispatches
sprite components to the sprite-rendering path.

The sprite renderer:

1.  Checks whether the sprite is visible.
2.  Builds the four local corners from the sprite dimensions and
    transform scale.
3.  Rotates those corners using quaternion multiplication.
4.  Adds the object's position to produce the final corner positions.
5.  Passes the texture and four positions to the native Direct3D
    wrapper.

This is a useful experiment in connecting object transforms and
component data to actual rendering calls.

### 5. Python-to-C++ Rendering Bridge

The Python `DirectX` class loads a native DLL using `ctypes.WinDLL` and
declares the argument and return types of exported functions. The native
C++ layer creates a Direct3D 9 device from the Win32 window handle.

The exposed rendering operations include:

-   Initializing and shutting down the Direct3D 9 device.
-   Clearing the render target.
-   Beginning and ending a scene.
-   Presenting a frame.
-   Creating a texture from pixel memory.
-   Drawing a textured quad from four supplied vertices.

The texture upload path accepts a NumPy pixel buffer, image dimensions,
and row pitch. The native side creates a Direct3D texture, locks it,
copies the pixel rows, and unlocks it. This makes the Python/native data
boundary an explicit part of the project.

### 6. Asset Loading and Pixel Conversion

`AssetManager` uses Pillow to open an image, converts it to RGBA, and
uses NumPy to construct a BGRA-ordered array for the native texture
upload path. It then wraps the returned texture handle and image
metadata in a `Texture` object.

This separates image-file handling from the Direct3D-specific upload
code.

### 7. User Script API

The `Script` component points to a Python file. `ScriptSys` loads the
module dynamically, finds classes derived from `ScriptBehaviour`,
instantiates them, and injects references to:

-   `this` --- the associated script component.
-   `game_object` --- the owning game object.
-   `transform` --- the object's transform.

The base `ScriptBehaviour` defines `start()` for initialization and
`update()` for repeated frame updates. This is an experiment in
providing game-side behavior without embedding every behavior directly
into the engine implementation.

### 8. Frame Timing

`FrameInfo` tracks the start time, elapsed time, previous-frame time,
frame count, delta time, and estimated FPS. The engine updates this data
during the frame loop and exposes it through the script API wrapper.

The current loop is timer-driven through PyQt6. Timing, frame pacing,
and separation between UI and game-loop responsibilities remain areas
for further refinement.

### 9. Math Primitives

The project includes small custom math types:

-   `Vector3` supports vector addition and subtraction, scalar
    multiplication, length, normalization, dot product, and a
    zero-vector factory.
-   `Quaternion` supports quaternion multiplication and conversion from
    Euler angles.
-   `Transform` uses these types for spatial state.

Implementing these primitives directly makes the math used by the engine
easier to inspect and experiment with.

## Repository Guide

The main modules in the current source tree include:

  --------------------------------------------------------------------------
  Path                                   Responsibility
  -------------------------------------- -----------------------------------
  `source/game_engine.py`                Engine setup, system creation,
                                         scene creation, and frame-loop
                                         orchestration.

  `source/raw_window.py`                 Native Windows window creation and
                                         access to its `HWND`.

  `source/directx/directx.py`            Python wrapper around the native
                                         graphics DLL.

  `source/directx/dx9tools.cpp`          Direct3D 9 device, texture upload,
                                         and textured-quad rendering
                                         implementation.

  `source/directx/dx9tools.h`            Native graphics function
                                         declarations.

  `source/object/scene.py`               Scene storage and game-object
                                         creation/search.

  `source/object/gameobject.py`          Game objects and component
                                         attachment.

  `source/components/`                   Component base class, `Transform`,
                                         `Sprite`, and `Script`.

  `source/systems/system_registery.py`   Component-to-system registration.

  `source/systems/render_sys.py`         Sprite discovery and rendering
                                         dispatch.

  `source/systems/script_sys.py`         Dynamic script loading, lifecycle
                                         calls, and frame timing.

  `source/asset/asset_manager.py`        Image loading, pixel conversion,
                                         and GPU texture creation.

  `source/asset/texture.py`              Texture handle and image metadata.

  `source/math/`                         `Vector3` and `Quaternion`
                                         implementations.

  `api/script_behaviour.py`              Base class for user-defined script
                                         behavior.

  `api/api_wrapper.py`                   Shared access to engine and frame
                                         information for scripts.
  --------------------------------------------------------------------------

## Current Status and Limitations

This repository is a work in progress. Some important limitations in the
current implementation are:

-   The runtime depends on Windows and Direct3D 9.
-   The native DLL build process is not yet a complete, reproducible
    build workflow.
-   The engine contains development/test setup in `GameEngine.test()`,
    including a machine-specific script path that should be moved to a
    sample or configuration.
-   Component registration and removal need a clearer lifecycle
    contract.
-   Script-loading and error-handling paths need more robust recovery
    behavior.
-   Frame pacing and resource lifetime management need further
    refinement.
-   Public APIs and module structure may change as the architecture
    evolves.

These are not claims that the project is production-ready; they are the
current boundaries of an ongoing experiment.

## Running It

The project currently expects a compatible Windows environment, a Python
installation with the required packages, and a native DLL built for the
same architecture as Python.

The source tree's current DLL path is relative to the working directory
(`source/directx/dxtools.dll`). The native library must be built from
the C++ source with a Windows C++ toolchain and Direct3D 9 development
support.

The repository does not yet provide a fully reproducible setup/build
procedure, so running a fresh clone may require manual environment and
DLL setup. A future improvement would be to document exact dependencies
and add a repeatable native build command.

## Why This Project Is Worth Exploring

The project brings together several non-trivial areas of software
development in one place:

-   A component-based object model and system dispatch.
-   Custom spatial math using vectors and quaternions.
-   Dynamic loading and lifecycle execution of user scripts.
-   Image decoding and pixel-format conversion.
-   Native DLL integration across Python and C++.
-   Direct3D device initialization, texture upload, and textured-quad
    rendering.
-   Runtime timing and separation of engine subsystems.

For a personal project, these are meaningful systems to investigate
because they force the design of interfaces between layers, not just the
implementation of isolated features.

## Project Status

**Personal project --- experimental and evolving.**

The aim is to learn by building, testing, and restructuring engine
systems. The code and architecture are expected to change.

## License

No license is specified here. Until a license is added, users should not
assume that the project is available for unrestricted reuse.
