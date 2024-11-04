# base_view.py

from base_class import BaseClass

class BaseView(BaseClass):
    def __init__(self):
        super().__init__()
        """
        Base View class that all views inherit from.
        """

    def destroy(self) -> None:
        """
        Called when the user navigates away from the View.
        Override this method in subclasses to perform cleanup.
        """
        return
