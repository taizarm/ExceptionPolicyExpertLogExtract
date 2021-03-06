import os


class ExtractGeneraLogLine:

    def __init__(self):

        self.general_extract_file_name = 'general_extract.txt'
        self.output_directory = 'output'

        self.processed_files = []
        self.total_logs = 0
        self.dates_running = []
        self.dates_running_by_file_log = {}

    def write_general_log_file(self):
        # Output file with general info
        filename = '{}/{}'.format(self.output_directory, self.general_extract_file_name)
        output_file = os.path.normpath(filename)

        with open(output_file, "w") as out_file:
            out_file.write('Files processed: {}\n'.format(set(self.processed_files)))
            out_file.write('Number of total logs: {}\n'.format(self.total_logs))
            out_file.write('Total of days running: {}\n'.format(len(set(self.dates_running))))
            out_file.write('Days running: {}\n'.format(set(self.dates_running)))

            out_file.write('\nDetail of days running, by file:\n\n')

            for key in self.dates_running_by_file_log.keys():
                out_file.write('{}: {}\n'.format(key, set(self.dates_running_by_file_log[key])))
                out_file.write('{}: {}\n\n'.format(key, len(set(self.dates_running_by_file_log[key]))))
