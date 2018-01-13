import os
import re
from extractor.ExtractErrorLogLine import ExtractErrorLogLine
from extractor.ExtractInfoLogLine import ExtractInfoLogLine
from extractor.ExtractWarningLogLine import ExtractWarningLogLine


class ExtractLog:

    def __init__(self):

        self.filtered_directory = 'filtered'
        self.output_directory = 'output'

        self.log_info_pattern = '!MESSAGE INFO - '
        self.log_warning_pattern = '!MESSAGE WARNING - '
        self.log_error_pattern = '!MESSAGE ERROR - '

        self.info_extract_file_name = 'info_extract.csv'
        self.warning_extract_file_name = 'warning_extract.csv'
        self.error_extract_file_name = 'error_extract.csv'
        self.general_extract_file_name = 'general_extract.txt'

        self.dict_errors = {}
        self.extract_error_log = ExtractErrorLogLine(self.dict_errors)

        self.dict_info = {}
        self.extract_info_log = ExtractInfoLogLine(self.dict_info)

        self.dict_warning = {}
        self.dict_warning_improper_handling = {}
        self.dict_warning_improper_throwing = {}
        self.dict_warning_possible_handling = {}
        self.extract_warning_log = ExtractWarningLogLine(self.dict_warning, self.dict_warning_improper_handling,
                                                         self.dict_warning_improper_throwing,
                                                         self.dict_warning_possible_handling)

        self.processed_files = []
        self.total_logs = 0
        self.dates_running = []

    def process_line_log(self, log_line):
        if self.log_info_pattern in log_line:
            self.extract_info_log.process_info_log(log_line)
        elif self.log_warning_pattern in log_line:
            self.extract_warning_log.process_warning_log(log_line)
        elif self.log_error_pattern in log_line:
            self.extract_error_log.process_error_log(log_line)

    def write_general_log_file(self):
        # Output file with general info
        filename = '{}/{}'.format(self.output_directory, self.general_extract_file_name)
        output_file = os.path.normpath(filename)

        with open(output_file, "w") as out_file:
            out_file.write('Files processed: {}\n'.format(set(self.processed_files)))
            out_file.write('Number of total logs: {}\n'.format(self.total_logs))
            out_file.write('Total of days running: {}\n'.format(len(set(self.dates_running))))
            out_file.write('Days running: {}\n'.format(set(self.dates_running)))

    def write_info_log_file(self):
        # Output file with general info
        filename = '{}/{}'.format(self.output_directory, self.info_extract_file_name)
        output_file = os.path.normpath(filename)

        with open(output_file, "w") as out_file:
            out_file.write('dict_info: {}\n'.format(self.dict_info))

    def write_warning_log_file(self):
        # Output file with warning info
        filename = '{}/{}'.format(self.output_directory, self.warning_extract_file_name)
        output_file = os.path.normpath(filename)

        with open(output_file, "w") as out_file:
            out_file.write('dict_warning_improper_handling: {}\n'.format(self.dict_warning_improper_handling))
            out_file.write('dict_warning_improper_throwing: {}\n'.format(self.dict_warning_improper_throwing))
            out_file.write('dict_warning_possible_handling: {}\n'.format(self.dict_warning_possible_handling))

    def write_all_log_files(self):
        self.write_general_log_file()
        self.write_info_log_file()
        self.write_warning_log_file()

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
                        self.total_logs += 1
                    else:
                        log_date = re.search('[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]', line)
                        self.dates_running.append(log_date.group(0))
                        self.processed_files.append(input_filename)

        # self.write_all_log_files()

    def extract_all_logs(self):

        self.populate_dicts_from_log_lines()
        self.extract_warning_log.process_all_logs()
        self.write_all_log_files()
