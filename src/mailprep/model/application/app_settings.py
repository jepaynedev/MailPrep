import re

class AppSettings:

    def get_input_file_types():
        return [
            {
                'Name': 'Normal',
                'Pattern': re.compile('')
            }
        ]