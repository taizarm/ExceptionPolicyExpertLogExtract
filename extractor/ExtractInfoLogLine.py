

class ExtractInfoLogLine:

    def __init__(self, dict_info):

        self.pattern_initializing = 'Initializing ExceptionPolicyExpert Plug-in...'
        self.pattern_changed_class = 'Changed class:'

        self.dict_info = dict_info

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
