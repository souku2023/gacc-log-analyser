from nicegui import ui
from typing import TYPE_CHECKING
from typing_extensions import Self
if TYPE_CHECKING:
    from app import App
    from app._base.base_view import BaseView

from app._base.base_gui_element import BaseGUIElement
from app.utils.logger import Logger

log = Logger(__name__)

class ViewManager(BaseGUIElement):

    class ViewManagerTypes:
        TAB_PANEL = "TAB_PANEL"
    
    def __init__(self, parent: 'App', type: str = ViewManagerTypes.TAB_PANEL):
        super().__init__(parent=parent)

        self.__current_view = None
        self.__all_views = dict()
        self.__type = type
        self.__layout_manager = None

        self.__build_view_manager()

    def __build_view_manager(self):
        self.__construct_header()

        self.__construct_left_drawer()
        
        if self.__type == ViewManager.ViewManagerTypes.TAB_PANEL:
            self.__construct_tab_panels()
        else:
            self.__construct_tab_panels()
    
    def __construct_tab_panels(self):
        self.__layout_manager = ui.tab_panels()
        log.d("Constructed tab panels view manager.")

    def __construct_header(self):
        """
        """
        self.__header = ui.header()
        log.d("Constructed Header.")

    def __construct_left_drawer(self):
        """
        """
        self.__left_drawer = ui.left_drawer()
        log.d("Constructed Left Drawer.")

    def add_view(self, view: 'BaseView'):
        """Adds a View to the ViewManager and adds it to the Left Drawer Menu 
        to make it easier to navigate

        Args:
            view (BaseView): The View to be added.
        """
        self.__all_views[view.tag()] = view
        # with ui.tab

    def __enter__(self) -> Self:
        if self.__layout_manager is not None:
            self.__layout_manager.__enter__()
        return self

    def __exit__(self, *_) -> None:
        self.__layout_manager.__exit__(*_)

    
        


