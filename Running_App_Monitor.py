import mysql.connector
import psutil
import time
from datetime import datetime
from Email_Report import send_email

# MySQL Database Configuration
DB_CONFIG = {
    "host": "localhost",      # Change this to your MySQL server's host
    "user": "root",           # Your MySQL username
    "password": "22082003",   # Your MySQL password
    "database": "application_monitor"  # Database name
}

# Establish a connection to the MySQL database
conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

# Function to log data into the MySQL database
def log_to_database(application_name, event_type):
    """
    Logs application events into the MySQL database.

    Args:
        application_name (str): The name of the application.
        event_type (str): The type of event (e.g., 'installed', 'running').
    """
    timestamp = datetime.now()
    query = '''
        INSERT INTO application_logs (timestamp, application_name, event_type)
        VALUES (%s, %s, %s)
    '''
    cursor.execute(query, (timestamp, application_name, event_type))
    conn.commit()

# Function to extract running applications
def extract_running_apps():
    """
    Extracts running applications using psutil and logs them to the database.

    Returns:
        list: A list of running applications' names.
    """
    running_apps = []
    for process in psutil.process_iter(attrs=['name']):
        try:
            app_name = process.info['name']
            running_apps.append(app_name)
            log_to_database(app_name, "running")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return running_apps

# Function to monitor running applications
def running_app_monitor():
    """
    Monitors running applications and logs their details into the MySQL database.
    """
    while True:
        print("Monitoring running applications...")
        extract_running_apps()
        print("Applications logged to database.")
        time.sleep(30)

# Main Execution
if __name__ == "__main__":
    try:
        running_app_monitor()
    except KeyboardInterrupt:
        print("Monitoring stopped.")
        cursor.close()
        conn.close()
