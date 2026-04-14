from source.object.gameobject import GameObject
from source.object.scene import Scene

from source.components import *
from source.math import *

from api.script_behaviour import ScriptBehaviour
from api.api_wrapper import EngineWrapper
from source.asset.asset_manager import AssetManager

asset_manager : AssetManager = EngineWrapper.engine.asset_manager
new_scene = EngineWrapper.engine.new_scene
