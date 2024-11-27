import mysql.connector
import psutil
import time
from datetime import datetime
from Email_Report import send_email

# MySQL Database Configuration
DB_CONFIG = {
    "host": "localhost",      # Change this to your MySQL server's host
    "user": "root",           # Your MySQL username
    "password": "password",   # Your MySQL password
    "database": "application_monitor"  # Database name
}

# Establish a connection to the MySQL database
conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

# Function to get unwanted applications from the database
def get_unwanted_apps():
    """
    Retrieves the list of unwanted applications from the database.
    Returns:
        list: A list of application names (str) that are considered unwanted.
    """
    cursor.execute("SELECT application_name FROM unwanted_apps")
    return [row[0] for row in cursor.fetchall()]

# Function to log unwanted applications and send an email alert
def log_unwanted_applications(app_name):
    """
    Logs unwanted applications into the database and sends an email alert.

    Args:
        app_name (str): The name of the unwanted application.
    """
    log_to_database(app_name, "unwanted")  # Log to the database
    email_subject = "Alert: Unwanted Application Detected"
    email_body = f"The following unwanted application was detected: {app_name}"
    send_email("admin@example.com", email_subject, email_body)
    print(f"Alert sent for unwanted application: {app_name}")

# Function to log data into the database
def log_to_database(application_name, event_type):
    """
    Logs application events into the MySQL database.

    Args:
        application_name (str): The name of the application.
        event_type (str): The type of event (e.g., 'running', 'unwanted').
    """
    timestamp = datetime.now()
    query = '''
        INSERT INTO application_logs (timestamp, application_name, event_type)
        VALUES (%s, %s, %s)
    '''
    cursor.execute(query, (timestamp, application_name, event_type))
    conn.commit()

# Function to extract running applications and detect unwanted ones
def extract_running_apps():
    """
    Extracts running applications and detects unwanted ones.

    1. Compares running applications with the unwanted applications stored in the database.
    2. Logs and sends an alert email for any unwanted applications.

    Returns:
        list: A list of currently running applications.
    """
    unwanted_apps = get_unwanted_apps()  # Fetch unwanted applications from the database
    running_apps = []

    for process in psutil.process_iter(attrs=['name']):
        try:
            app_name = process.info['name']
            running_apps.append(app_name)
            log_to_database(app_name, "running")  # Log all running applications

            # Check if the application is unwanted
            if app_name in unwanted_apps:
                log_unwanted_applications(app_name)

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    return running_apps

# Function to monitor running applications
def running_app_monitor():
    """
    Monitors running applications and logs unwanted applications.
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
