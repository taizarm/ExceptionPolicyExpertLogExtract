import re
import os


class ExtractWarningLogLine:

    def __init__(self):

        self.pattern_improper_handling = '!MESSAGE WARNING - Violation detected (ImproperHandlingVerifier). '
        self.pattern_improper_throwing = '!MESSAGE WARNING - Violation detected (ImproperThrowingVerifier). '
        self.pattern_handling_information = '!MESSAGE WARNING - ' \
                                            'Handling information detected (PossibleHandlersInformation). '

        self.improper_handling_name = 'ImproperHandlingVerifier'
        self.improper_throwing_name = 'ImproperThrowingVerifier'
        self.handling_information_name = 'PossibleHandlersInformation'

        self.dict_warning_improper_handling = {}
        self.dict_warning_improper_throwing = {}
        self.dict_warning_possible_handling = {}

        self.output_directory = 'output'
        self.pattern_rule = '.*Rule: (R[0-9]+)'

        self.warning_possible_handling_file_name = 'warning_possible_handling.txt'
        self.warning_improper_throwing_file_name = 'warning_improper_throwing.txt'
        self.warning_improper_handling_file_name = 'warning_improper_handling.txt'

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

    def process_log_detail_by_type(self, items, violation_type, pattern, output_file_name):

        rules_list = []
        dict_violations_by_rules = {}

        for k, v in sorted(items):

            # Remove unnecessary characters
            k = k.replace(pattern, '')

            match_rule = re.search(self.pattern_rule, k)

            rule = match_rule.group(0)
            rule_name = rule.split(':')[1]

            rules_list.append(rule_name)

            current_violations = dict_violations_by_rules.get(rule_name, [])
            current_violations.append(k)
            dict_violations_by_rules[rule_name] = current_violations

        filename = '{}/{}'.format(self.output_directory, output_file_name)
        output_file = os.path.normpath(filename)

        with open(output_file, "w") as out_file:
            sorted_rules_names = sorted(set(rules_list))

            out_file.write('Total warning messages:\n')
            total = 0
            for key in sorted_rules_names:
                out_file.write('\t{}: {}\n'.format(key, len(set(dict_violations_by_rules[key]))))
                total += len(set(dict_violations_by_rules[key]))
            out_file.write('Total:{}\n'.format(total))

            # TODO add qtd of each violation
            out_file.write('\n\nRules in CSV format '
                           '(violationType,rule,className,methodName,exception):\n\n')

            for rule_name in sorted_rules_names:
                violations = dict_violations_by_rules[rule_name]

                for violation in set(violations):
                    class_name = re.search('Class: \S*', violation).group(0).split(':')[1].strip()
                    method_name = re.search('Method: \S*', violation).group(0).split(':')[1].strip()
                    exception_name = re.search('Exception: \S*', violation).group(0).split(':')[1].strip()

                    out_file.write('{},{},{},{},{}\n'.format
                                   (violation_type, rule_name.strip(), class_name, method_name, exception_name))

    def process_all_logs(self):
        self.process_log_detail_by_type(self.dict_warning_possible_handling.items(),
                                        self.handling_information_name,
                                        self.pattern_handling_information,
                                        self.warning_possible_handling_file_name)

        self.process_log_detail_by_type(self.dict_warning_improper_throwing.items(),
                                        self.improper_throwing_name,
                                        self.pattern_improper_throwing,
                                        self.warning_improper_throwing_file_name)

        self.process_log_detail_by_type(self.dict_warning_improper_handling.items(),
                                        self.improper_handling_name,
                                        self.pattern_improper_handling,
                                        self.warning_improper_handling_file_name)
