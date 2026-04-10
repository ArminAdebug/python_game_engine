
from test import G, key_g

class S:

    key = key_g

    def new_g():
        return G(__class__.key)


#from __future__ import annotations
#from typing import TYPE_CHECKING
#
#if TYPE_CHECKING:
#    from .scene import Scene


S.new_g()
