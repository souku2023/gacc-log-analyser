# base_view_model.py

from base_class import BaseClass

class BaseViewModel(BaseClass):
    def __init__(self):
        super().__init__()
        """
        Base ViewModel class that all view models inherit from.
        """

    def destroy(self) -> None:
        """
        Called when the ViewModel is no longer needed.
        Override this method in subclasses to perform cleanup.
        """
        return
