import logging
import traceback

# Import Custom Handlers
from .file_handler import FileHandler
from .stream_handler import StreamHandler

def     format_traceback(e: Exception):
    """
    Format e.__traceback__ for Log message.
    """
    return "\nTraceback:" + "\n\t".join(traceback.format_tb(e.__traceback__))

class Logger(logging.Logger):

    def __init__(self, name: str, level: int | str = 0) -> None:
        """Class for Logging service for this app."""
        super().__init__(name, level)

        # Handlers
        # Stream
        self.__stream_handler = StreamHandler()
        self.addHandler(self.__stream_handler)

        # File
        self.__file_handler = FileHandler()
        self.addHandler(self.__file_handler)

    def d(self, msg, *args, **kwargs):
        """
        Log 'msg % args' with severity 'DEBUG'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.d("Houston, we have a %s", "thorny problem", exc_info=True)
        """
        if self.isEnabledFor(logging.DEBUG):
            self._log(logging.DEBUG, msg, args, **kwargs)

    def i(self, msg, *args, **kwargs):
        """
        Log 'msg % args' with severity 'INFO'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.i("Houston, we have a %s", "notable problem", exc_info=True)
        """
        if self.isEnabledFor(logging.INFO):
            self._log(logging.INFO, msg, args, **kwargs)


    def w(self, msg, *args, **kwargs):
        """
        Log 'msg % args' with severity 'WARNING'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.w("Houston, we have a %s", "bit of a problem", exc_info=True)
        """
        if self.isEnabledFor(logging.WARNING):
            self._log(logging.WARNING, msg, args, **kwargs)

    def e(self, *args):
        """
        Convenience method for logging an Exception.
        """
        msg = ""
        e = list(filter(lambda arg: isinstance(arg, Exception), args))
        strings = list(filter(lambda arg: isinstance(arg, str), args))
        if strings:
            msg += ", ".join(strings)
        if e:
            msg += format_traceback(e=e[0])
        if self.isEnabledFor(logging.ERROR):
            self._log(logging.ERROR, msg, args[1:])
            
    def c(self, msg, *args, **kwargs):
        """
        Log 'msg % args' with severity 'CRITICAL'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.c("Houston, we have a %s", "major disaster", exc_info=True)
        """
        if self.isEnabledFor(logging.CRITICAL):
            self._log(logging.CRITICAL, msg, args, **kwargs)