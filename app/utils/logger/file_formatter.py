import logging
import copy

class FileFormatter(logging.Formatter):
    def formatException(self, exc_info):
        result = super(FileFormatter, self).formatException(exc_info)
        return result
    
    def formatStack(self, stack_info: str) -> str:
        return "\t"+"\n\t".join(super().formatStack(stack_info).split('\n'))
    
    def formatMessage(self, record: logging.LogRecord) -> str:
        """Custom message formatting: for console only the last child is 
        printed"""
        copied_record = copy.deepcopy(record)
        if '__main__' not in record.name:
            split_name = copied_record.name.split('.')
            copied_record.name = split_name[-1]
            
        return super().formatMessage(copied_record)

    def format(self, record):
        s = super(FileFormatter, self).format(record)
        if record.exc_text:
            s = s.replace("\nNoneType: None", "")
            s = s.replace('\n', '\n\t').strip()
        return s
