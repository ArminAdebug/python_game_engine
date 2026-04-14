from source.components.component import Component
import os
from pathlib import Path


class Script(Component):
    type = "script"

    def __init__(self, file_path: Path | str):
        super().__init__()

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"file {file_path} does not exists.")

        self.file_path: Path = file_path if isinstance(
            file_path, Path) else Path(file_path).absolute()
