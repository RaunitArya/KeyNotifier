import os
import time
from datetime import datetime

# Specify the folder to monitor (Downloads folder)
DOWNLOADS_FOLDER = os.path.expanduser("~/Downloads")

# Function to monitor the Downloads folder for new files
def monitor_downloads_folder():
    """
    Monitors the Downloads folder for new files and logs them to the console.
    """
    try:
        print("Monitoring Downloads folder for new items...")
        # Initialize a set to store existing files in the folder
        previous_files = set(os.listdir(DOWNLOADS_FOLDER))

        while True:
            # Get the current list of files in the Downloads folder
            current_files = set(os.listdir(DOWNLOADS_FOLDER))

            # Identify new files
            new_files = current_files - previous_files

            for new_file in new_files:
                new_file_path = os.path.join(DOWNLOADS_FOLDER, new_file)
                timestamp = datetime.now()

                # Log the new file details
                print(f"New file detected: {new_file}")
                print(f"File path: {new_file_path}")
                print(f"Timestamp: {timestamp}")

            # Update the previous files set
            previous_files = current_files

            # Wait for a short interval before the next scan
            time.sleep(10)  # Adjust the interval as needed

    except Exception as e:
        print(f"Error while monitoring Downloads folder: {e}")

# Main execution
if __name__ == "__main__":
    try:
        monitor_downloads_folder()  # Start monitoring
    except KeyboardInterrupt:
        print("Monitoring stopped.")
