"""coding api for user codes
"""
# pylint: disable=invalid-name
from typing import TYPE_CHECKING

from source.object.scene import Scene
from source.object.gameobject import GameObject
from source.components import (
    Component,
    Transform,
    Script,
    Sprite
)
from source.math import (
    Vector3,
    Quaternion
)
from api.script_behaviour import ScriptBehaviour
from api.api_wrapper import Wrapper as _Wrapper
from source.asset.asset_manager import AssetManager

if TYPE_CHECKING:
    from source.systems.script_sys import FrameInfo

asset_manager: AssetManager = _Wrapper.engine.asset_manager
frame_info: "FrameInfo" = _Wrapper.frame_info
new_scene = _Wrapper.engine.new_scene

__all__ = [
    "Component",
    "Transform",
    "Script",
    "Sprite",
    "GameObject",
    "Scene",
    "ScriptBehaviour",
    "Vector3",
    "Quaternion",
    "asset_manager",
    "frame_info",
    "new_scene",

]
