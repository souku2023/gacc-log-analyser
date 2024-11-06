# base_view_model.py

from base_class import BaseClass
from app.utils.logger import Logger

log = Logger(__name__)

class BaseViewModel(BaseClass):
    def __init__(self):
        """
        Base ViewModel class that all view models inherit from.
        """
        super().__init__()
        log.d(f"{self.tag()} initialising...")


    def destroy(self) -> None:
        """
        Called when the ViewModel is no longer needed.
        Override this method in subclasses to perform cleanup.
        """
        return
