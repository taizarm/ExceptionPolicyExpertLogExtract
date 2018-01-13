from filter.FilterLog import FilterLog
from extractor.ExtractLog import ExtractLog
import shutil
import os


class ParseLog:

    def clean_output_dir(self):
        # Clean the filtered and output directories
        try:
            shutil.rmtree('./filtered')
        except OSError:
            print('There is no filtered directory - a new one will be create')

        try:
            shutil.rmtree('./output')
        except OSError:
            print('There is no output directory - a new one will be create')

        os.makedirs('filtered')
        os.makedirs('output')

    def parse_log(self):
        filter_log = FilterLog()
        filter_log.filter_log()

        extract_log = ExtractLog()
        extract_log.extract_all_logs()

if __name__ == "__main__":
    parser = ParseLog()
    parser.clean_output_dir()
    parser.parse_log()
