import os
import re
from extractor.ExtractErrorLogLine import ExtractErrorLogLine
from extractor.ExtractInfoLogLine import ExtractInfoLogLine
from extractor.ExtractWarningLogLine import ExtractWarningLogLine
from extractor.ExtractGeneralLogLine import ExtractGeneraLogLine


class ExtractLog:

    def __init__(self):

        self.filtered_directory = 'filtered'
        self.output_directory = 'output'

        self.log_info_pattern = '!MESSAGE INFO - '
        self.log_warning_pattern = '!MESSAGE WARNING - '
        self.log_error_pattern = '!MESSAGE ERROR - '

        self.extract_error_log = ExtractErrorLogLine()
        self.extract_info_log = ExtractInfoLogLine()
        self.extract_warning_log = ExtractWarningLogLine()
        self.extract_general_log = ExtractGeneraLogLine()

    def process_line_log(self, log_line):
        if self.log_info_pattern in log_line:
            self.extract_info_log.process_info_log(log_line)
        elif self.log_warning_pattern in log_line:
            self.extract_warning_log.process_warning_log(log_line)
        elif self.log_error_pattern in log_line:
            self.extract_error_log.process_error_log(log_line)

    def write_all_log_files(self):
        self.extract_general_log.write_general_log_file()
        self.extract_info_log.write_info_log_file()

    def populate_dicts_from_log_lines(self):

        # Iterate over all log files
        for filename in os.listdir(self.filtered_directory):

            # Input file with all the filtered log lines
            input_filename = '{}/{}'.format(self.filtered_directory, filename)
            input_file = os.path.normpath(input_filename)

            # Open input file in 'read' mode
            with open(input_file, "r") as open_input_file:

                lines = []
                for line in open_input_file:
                    lines.append(line)

                for index, line in enumerate(lines):
                    if index % 2 != 0:
                        self.process_line_log(line)
                        self.extract_general_log.total_logs += 1
                    else:
                        log_date = re.search('[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]', line)
                        self.extract_general_log.dates_running.append(log_date.group(0))

                        current_number_of_days = self.extract_general_log.\
                            dates_running_by_file_log.get(open_input_file.name, [])
                        current_number_of_days.append(log_date.group(0))
                        self.extract_general_log.dates_running_by_file_log[open_input_file.name] = \
                            current_number_of_days

                        self.extract_general_log.processed_files.append(input_filename)

    def extract_all_logs(self):

        self.populate_dicts_from_log_lines()
        self.extract_warning_log.process_all_logs()
        self.extract_info_log.process_changed_classes()

        self.write_all_log_files()

