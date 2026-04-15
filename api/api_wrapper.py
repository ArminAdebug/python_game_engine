"""
wraps engine commands without circle import.
"""
from typing import *

if TYPE_CHECKING:
    from source.game_engine import GameEngine
    from source.systems.script_sys import FrameInfo

class Wrapper:
    engine : "GameEngine" = None
    frame_info : "FrameInfo" = None
