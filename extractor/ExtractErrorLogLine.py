

class ExtractErrorLogLine:

    def __init__(self):

        self.pattern_something_wrong = 'Something wrong happened when processing modified files'
        self.pattern_workspace_not_file = 'The workspace does not have the file /src-gen/contract.xml, with ECL rules.'
        self.pattern_invalid_format = 'Invalid format of contract.xml file. Plug-in aborted'
        self.pattern_file_not_found = 'File contract.xml not found'
        self.pattern_marker_error = 'Something wrong happened when creating/removing markers'

        self.dict_errors = {}

        self.error_extract_file_name = 'error_extract.csv'

    def process_error_log(self, log_line):
        '''
        Types of error logs:
            ERROR - Something wrong happened when processing modified files. (...)
            ERROR - The workspace does not have the file /src-gen/contract.xml, with ECL rules. Plug-in aborted. (...)
            ERROR - Invalid format of contract.xml file. Plug-in aborted. (...)
            ERROR - File contract.xml not found.
            ERROR - Something wrong happened when creating/removing markers. (...)
        '''
        if self.pattern_something_wrong in log_line:
            self.dict_errors['pattern_something_wrong'] = self.dict_errors.get('pattern_something_wrong', 0) + 1
        if self.pattern_workspace_not_file in log_line:
            self.dict_errors['pattern_workspace_not_file'] = self.dict_errors.get('pattern_workspace_not_file', 0) + 1
        if self.pattern_invalid_format in log_line:
            self.dict_errors['pattern_invalid_format'] = self.dict_errors.get('pattern_invalid_format', 0) + 1
        if self.pattern_file_not_found in log_line:
            self.dict_errors['pattern_file_not_found'] = self.dict_errors.get('pattern_file_not_found', 0) + 1
        if self.pattern_marker_error in log_line:
            self.dict_errors['pattern_marker_error'] = self.dict_errors.get('pattern_marker_error', 0) + 1
