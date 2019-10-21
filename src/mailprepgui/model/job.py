"""Contains data container class for a bulk mail job"""

class Job:  # pylint: disable=too-few-public-methods,too-many-instance-attributes
    """Container for data pertaining to a bulk mail job"""

    def __init__(self, job_number, title, department, customer):
        self.job_number = job_number
        self.title = title
        self.department = department
        self.customer = customer

        self.files = []
        self.convert_to_upper = False
        self.mark_custom_campus = False
        self.custom_campus_file = None
