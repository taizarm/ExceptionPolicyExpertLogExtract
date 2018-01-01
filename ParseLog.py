from filter.FilterLog import FilterLog
from extractor.ExtractLog import ExtractLog


class ParseLog:

    def parse_log(self):
        filter_log = FilterLog()
        filter_log.filter_log()

        extract_log = ExtractLog()
        extract_log.extract_all_logs()

if __name__ == "__main__":
    parser = ParseLog()
    parser.parse_log()
