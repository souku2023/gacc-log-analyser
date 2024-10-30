import logging

# Import Custom Handlers
from .file_handler import FileHandler
from .stream_handler import StreamHandler


class Logger(logging.Logger):

    def __init__(self, name: str, level: int | str = 0) -> None:
        """
        """
        super().__init__(name, level)

        # Handlers
        # Stream
        self.__stream_handler = StreamHandler()
        self.addHandler(self.__stream_handler)
        # File
        self.__file_handler = FileHandler()
        self.addHandler(self.__file_handler)

