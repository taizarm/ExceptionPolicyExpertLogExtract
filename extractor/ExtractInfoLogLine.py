import os


class ExtractInfoLogLine:

    def __init__(self):

        self.dict_info = {}
        self.changed_classes = []

        self.pattern_initializing = 'Initializing ExceptionPolicyExpert Plug-in...'
        self.pattern_changed_class = 'Changed class:'

        self.output_directory = 'output'
        self.info_extract_file_name = 'info_extract.csv'

    def write_info_log_file(self):
        # Output file with general info
        filename = '{}/{}'.format(self.output_directory, self.info_extract_file_name)
        output_file = os.path.normpath(filename)

        with open(output_file, "w") as out_file:
            out_file.write('dict_info: {}\n'.format(self.dict_info))

    def process_info_log(self, log_line):
        '''
        Types of info logs:
            INFO - Initializing ExceptionPolicyExpert Plug-in...
            INFO - Changed class: (...)
        '''
        if self.pattern_initializing in log_line:
            self.dict_info['pattern_initializing'] = self.dict_info.get('pattern_initializing', 0) + 1
        if self.pattern_changed_class in log_line:
            self.dict_info['pattern_changed_class'] = self.dict_info.get('pattern_changed_class', 0) + 1
            self.changed_classes.append(log_line)

    def process_changed_classes(self):
        #print self.changed_classes
        pass
