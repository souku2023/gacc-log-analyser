from nicegui import ui, app

from app._base.base_class import BaseClass
from app.view_manager import ViewManager
from app.utils.logger import Logger

log = Logger(__name__)

class App:
    def __init__(self) -> None:
        """
        """
        ui.add_head_html("""<style>:root {
        --nicegui-default-padding: 0rem;
        --nicegui-default-gap: 1rem;
        }</style>
        """)    
        with ui.element() as self.__main_element:
            self.__view_manager = ViewManager(self)
        

    def run(self):
        log.d("Starting App...")
        ui.run(
            title="Log Visualizer App",
        )
        log.d("Started App!")


        