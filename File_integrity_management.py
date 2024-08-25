import os
import hashlib
import time

# Hashing the file to be managed
def hash_file(file_path):
    # creating a hash object to handle the hash data as it is being computed
    sha256_hash = hashlib.sha256()
    try:
        # open the file in binary mode
        with open(file_path, 'rb') as file:
            for file_bytes in iter(lambda: file.read(4096), b""):
                sha256_hash.update(file_bytes)
        return sha256_hash.hexdigest()
    except FileNotFoundError as e:
        # print out error when the file is not found
        print(f"An error occurred: {e}")
        return None

# A function to scan the directory (or file in this case)
def scan_directory(directory):
    file_hash = {}  # empty dictionary to store file_path and hash value
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_hash[file_path] = hash_file(file_path)
    return file_hash

# A function to monitor a specific file (or directory)
def monitor_directory(directory, interval=20, log_file="integrity_log.txt"):
    previous_hashes = scan_directory(directory)
    
    while True:
        time.sleep(interval)
        current_hashes = scan_directory(directory)
        
        changes = {}
        for file_path, current_hash in current_hashes.items():
            if file_path not in previous_hashes:
                changes[file_path] = "created"
            elif previous_hashes[file_path] != current_hash:
                changes[file_path] = "modified"
                
        for file_path in previous_hashes.keys():
            if file_path not in current_hashes:
                changes[file_path] = "deleted"
                
        if changes:
            log_changes(changes, log_file)
            previous_hashes = current_hashes

# Function to log the changes
def log_changes(changes, log_file):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, 'a') as log:  # Changed to append mode
        log.write(f"{timestamp} - Changes detected:\n")
        for file_path, change_type in changes.items():
            log.write(f"{change_type}: {file_path}\n")
        log.write("\n")

if __name__ == "__main__":
    file_to_monitor = "file_to_be_monitored/sample.txt"  # Directory containing sample.txt
    monitor_directory(file_to_monitor, interval=60)
