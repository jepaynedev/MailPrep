"""Contains data container class for single file data"""

class InputFile:  # pylint: disable=too-few-public-methods
    """Container for data pertaining to a single file for a bulk mail job"""

    def __init__(self, file_name, file_type, list_id, priority):
        self.file_name = file_name
        self.file_type = file_type
        self.list_id = list_id
        self.priority = priority
