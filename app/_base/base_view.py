
from base_gui_element import BaseGUIElement
from app.utils.logger import Logger

log = Logger(__name__)

class BaseView(BaseGUIElement):
    def __init__(self, parent):
        """
        Base View class that all views inherit from.
        """
        super().__init__(parent=parent)
        log.d(f"{self.tag()} initialising...")

    def destroy(self) -> None:
        """
        Called when the user navigates away from the View.
        Override this method in subclasses to perform cleanup.
        """
        log.d(f"{self.tag()} destroying...")
        return
