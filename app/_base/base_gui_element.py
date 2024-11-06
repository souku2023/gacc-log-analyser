from typing_extensions import Self
from .base_class import BaseClass
from app.utils.logger import Logger

log = Logger(__name__)

class BaseGUIElement(BaseClass): 

    def __init__(self, parent = None):
        """The base class for UI elements"""
        super().__init__()
        parent: BaseGUIElement | None
        if parent is None:
            self.__hierarchy = 0
        else:
            self.__hierarchy = parent.hierarchy + 1
        self.__parent = parent

    @property
    def parent(self):
        return self.__parent
    
    @property
    def hierarchy(self):
        return self.__hierarchy