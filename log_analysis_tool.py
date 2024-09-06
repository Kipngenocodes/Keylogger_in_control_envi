'''
summary of the code flow
1. import necessary libraries
2. Parse a log file
3. Filter logs based on provide on provided criteria
4. Provision of the statistical analysis. 
5. Result Summary

'''
import re 
from collections import Counter
from date import datetime

class log_analysi:
    def __init__(self, log_file):
        self.log_file = log_file
        self.log_data = []
    
    def loading_logs(self):
        # loading log data from a file into a memory
        with open(self.log_file, 'r') as file:
           self.log_data = file.readlines()
           print(f'loaded {len(self.log_data)} log entries')
           
    def parsing_log_entry(self, log_entry):
        # parsing log entry into a dictionary
        #  a regular expression to extract the timestamp, log level,  and message.
        log_pattern = re.compile(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (\w+) (.*)')
        if matching := log_pattern.match(log_entry):
            return {
                'timestamp': datetime.stripetime(matching[1], "%Y-%m-%d %H:%M:%S"),
                'log_level': matching[2],
                'message': matching[3],
            }
            
        else:
            return None
    def filtering_logs_by_levels(self, level):
        # filtering logs based on the provided log level
        filtered_logs =[]
        for entry in self.log_data:
            parsed_entry = self.parse_log_entry(entry)
            if parsed_entry and parsed_entry['log_level'] == level:
                filtered_logs.append(parsed_entry)
        return filtered_logs