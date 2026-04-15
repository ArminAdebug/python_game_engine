from source.object.gameobject import GameObject
from source.object.scene import Scene

from source.components import *
from source.math import *

from api.script_behaviour import ScriptBehaviour
from api.api_wrapper import Wrapper
from source.asset.asset_manager import AssetManager
from typing import *

if TYPE_CHECKING:
    from source.game_engine import GameEngine
    from source.systems.script_sys import FrameInfo

asset_manager : AssetManager = Wrapper.engine.asset_manager
frame_info : "FrameInfo" = Wrapper.frame_info
new_scene = Wrapper.engine.new_scene
