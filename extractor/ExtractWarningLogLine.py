import re
import os


class ExtractWarningLogLine:

    def __init__(self, dict_warning, dict_warning_improper_handling,
                 dict_warning_improper_throwing, dict_warning_possible_handling):

        self.pattern_improper_handling = '!MESSAGE WARNING - Violation detected (ImproperHandlingVerifier). '
        self.pattern_improper_throwing = '!MESSAGE WARNING - Violation detected (ImproperThrowingVerifier). '
        self.pattern_handling_information = '!MESSAGE WARNING - ' \
                                            'Handling information detected (PossibleHandlersInformation). '

        self.dict_warning = dict_warning
        self.dict_warning_improper_handling = dict_warning_improper_handling
        self.dict_warning_improper_throwing = dict_warning_improper_throwing
        self.dict_warning_possible_handling = dict_warning_possible_handling

        self.output_directory = 'output'
        self.pattern_rule = '.*Rule: (R[0-9]+)'

        self.warning_possible_handling_file_name = 'warning_possible_handling.csv'

    def process_warning_log(self, log_line):
        '''
        Types of warning logs:
            WARNING - Violation detected (ImproperHandlingVerifier). Rule: (...)
            WARNING - Violation detected (ImproperThrowingVerifier). Rule: (...)
            WARNING - Handling information detected (PossibleHandlersInformation). Rule: (...)
        '''
        if self.pattern_improper_handling in log_line:
            self.dict_warning_improper_handling[log_line] = self.dict_warning_improper_handling.get(log_line, 0) + 1
        if self.pattern_improper_throwing in log_line:
            self.dict_warning_improper_throwing[log_line] = self.dict_warning_improper_throwing.get(log_line, 0) + 1
        if self.pattern_handling_information in log_line:
            self.dict_warning_possible_handling[log_line] = self.dict_warning_possible_handling.get(log_line, 0) + 1

    def process_possible_handling_warning(self):
        dict_rule_qtd = {}
        dict_rule = {}

        for k, v in sorted(self.dict_warning_possible_handling.items()):

            # Remove unnecessary characters
            k = k.replace(self.pattern_handling_information, '')

            match_rule = re.search(self.pattern_rule, k)

            rule = match_rule.group(0)
            rule_name = rule.split(':')[1]

            qtd = dict_rule_qtd.get(rule_name, 0)
            dict_rule_qtd[rule_name] = qtd + v
            dict_rule[rule_name] = k

        filename = '{}/{}'.format(self.output_directory, self.warning_possible_handling_file_name)
        output_file = os.path.normpath(filename)

        with open(output_file, "w") as out_file:
            sort_keys = sorted(dict_rule_qtd)

            out_file.write('Total warning messages:\n')
            for key in sort_keys:
                out_file.write('\t{}: {}\n'.format(key, dict_rule_qtd[key]))

            out_file.write('\n\nDetail of each rule:\n')
            for key in sort_keys:
                out_file.write('\t{}\n'.format(dict_rule[key]))

            out_file.write('\n\nRules in CSV format (className,methodName,exception,qtdOfViolations):\n\n')

            for key in sort_keys:
                class_name = re.search('Class: \S*', dict_rule[key]).group(0).split(':')[1].strip()
                method_name = re.search('Method: \S*', dict_rule[key]).group(0).split(':')[1].strip()
                exception_name = re.search('Exception: \S*', dict_rule[key]).group(0).split(':')[1].strip()

                out_file.write('{},{},{},{}\n'.format(class_name, method_name, exception_name, dict_rule_qtd[key]))

    def process_all_logs(self):
        self.process_possible_handling_warning()



