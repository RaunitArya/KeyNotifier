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

# Function to get allowed applications from the database
def get_allowed_apps():
    """
    Retrieves the list of allowed/expected applications from the database.
    Returns:
        list: A list of application names (str) that are considered allowed/expected.
    """
    cursor.execute("SELECT application_name FROM allowed_apps")
    return [row[0] for row in cursor.fetchall()]

# Function to log unexpected applications and send an email alert
def log_unexpected_applications(app_name):
    """
    Logs unexpected applications into the database and sends an email alert.

    Args:
        app_name (str): The name of the unexpected application.
    """
    log_to_database(app_name, "unexpected")  # Log to the database
    email_subject = "Alert: Unexpected Application Detected"
    email_body = f"The following unexpected application was detected: {app_name}"
    send_email("admin@example.com", email_subject, email_body)
    print(f"Alert sent for unexpected application: {app_name}")

# Function to log data into the database
def log_to_database(application_name, event_type):
    """
    Logs application events into the MySQL database.

    Args:
        application_name (str): The name of the application.
        event_type (str): The type of event (e.g., 'running', 'unexpected').
    """
    timestamp = datetime.now()
    query = '''
        INSERT INTO application_logs (timestamp, application_name, event_type)
        VALUES (%s, %s, %s)
    '''
    cursor.execute(query, (timestamp, application_name, event_type))
    conn.commit()

# Function to extract running applications and detect unexpected ones
def extract_running_apps():
    """
    Extracts running applications and detects new or unexpected ones.

    1. Compares running applications with the allowed applications stored in the database.
    2. Logs and sends an alert email for any unexpected applications.

    Returns:
        list: A list of currently running applications.
    """
    allowed_apps = get_allowed_apps()  # Fetch allowed applications from the database
    running_apps = []

    for process in psutil.process_iter(attrs=['name']):
        try:
            app_name = process.info['name']
            running_apps.append(app_name)
            log_to_database(app_name, "running")  # Log all running applications

            # Check if the application is unexpected
            if app_name not in allowed_apps:
                log_unexpected_applications(app_name)

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    return running_apps

# Function to monitor running applications
def running_app_monitor():
    """
    Monitors running applications and logs unexpected applications.
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