from helper import *
from typing import Callable
from window import Window


class Core:
    def __init__(self, dwindow : Window):
        self.directx_window = dwindow
    
    def loop(funcs : list, exiting : Callable) -> int:
        """_summary_

        Args:
            funcs (list): functions to run in loop
            exiting (func): funcs must be a function and if exiting return True loop will end.

        Returns:
            int: loop exit status
        """
        
        """_summary_

        Args:
            

        Returns:
            
            
        ****
        """
        for func in funcs:
            if not isinstance(func, Callable):
                # all funcs are not actually Function
                return 2

        while True:
            if exiting():
                break
                    
            for func in funcs:
                try:
                    func()
                    
                except Exception as e:
                    log(e)
                    
        
        return 0