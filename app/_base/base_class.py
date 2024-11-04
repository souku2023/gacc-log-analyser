class BaseClass:
    
    def __init__(self):
        """
        Base Object of all classes in the project
        """

    def tag(self) -> str:
        """
        """
        try:
            return self.__class__.__qualname__
        except:
            return self.__qualname__
        
    def __repr__(self) -> str:
        """
        """
        s = " | ".join([f"{key}: {value}" for key, value in __dict__.items()])
        return f"{self.tag()}: {s}"