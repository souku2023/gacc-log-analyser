# base_model.py

from base_class import BaseClass

class BaseModel(BaseClass):
    def __init__(self):
        super().__init__()
        """
        Base Model class that all models inherit from.
        """

    def destroy(self) -> None:
        """
        Called when the Model is no longer needed.
        Override this method in subclasses to perform cleanup.
        """
        return