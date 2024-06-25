import mysql.connector
from mysql.connector import Error

def read_db_credentials(file_path):
    credentials = {}
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if ':' in line:
                    key, value = line.strip().split(':', 1)
                    credentials[key.strip()] = value.strip()
                else:
                    print(f"Error: Invalid format in line: {line}")
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    except Exception as e:
        print(f"Error: {e}")
    return credentials


def create_connection(credentials):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=credentials.get('host'),
            database=credentials.get('database'),
            user=credentials.get('user'),
            password=credentials.get('password')
        )
        if connection.is_connected():
            db_info = connection.get_server_info()
            print(f"Connected to MySQL Server version {db_info}")
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
    return connection

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"Error executing query: {e}")

if __name__ == "__main__":
    credentials = read_db_credentials('connection_details.txt')
    connection = create_connection(credentials)
    create_table_query = """CREATE TABLE friend_requests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES users(id))"""
    execute_query(connection, create_table_query)
    connection.close()
    print("MySQL connection is closed")