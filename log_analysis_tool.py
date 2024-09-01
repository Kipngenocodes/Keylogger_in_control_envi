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
           