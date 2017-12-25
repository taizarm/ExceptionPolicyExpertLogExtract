import os


def filter_logs():
    # String that identifies the plug-in logs
    plugin_log_id = 'br.ufrn.lets.exceptionExpert'

    log_line_pattern = '!ENTRY {}'.format(plugin_log_id)

    input_directory = 'input'

    # Iterate over all log files
    for filename in os.listdir(input_directory):

        # Input file with all the log lines
        input_filename = '{}/{}'.format(input_directory, filename)
        input_file = os.path.normpath(input_filename)

        # Output file with only the filtered lines
        output_filename = 'filtered/{}'.format(filename)
        output_file = os.path.normpath(output_filename)

        # Initialize the file to ensure that is a blank one
        with open(output_file, "w") as out_file:
            out_file.write("")

        # Open output file in 'append' mode
        with open(output_file, "a") as open_output_file:
            # Open input file in 'read' mode
            with open(input_file, "r") as open_input_file:

                lines = []
                for line in open_input_file:
                    lines.append(line)

                # Write in output file the couple of line that is related to the log plugin
                for index, line in enumerate(lines):
                    if log_line_pattern in line:
                        open_output_file.write(line)
                        open_output_file.write(lines[index+1])


def main():

    # Filter the log lines with only lines related to the plugin
    filter_logs()

if __name__ == "__main__":
    main()
