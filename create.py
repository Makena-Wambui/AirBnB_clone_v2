import os
import subprocess

def create_city(state_id, city_name):
    # Set the required environment variables
    os.environ['HBNB_MYSQL_USER'] = 'hbnb_dev'
    os.environ['HBNB_MYSQL_PWD'] = 'hbnb_dev_pwd'
    os.environ['HBNB_MYSQL_HOST'] = 'localhost'
    os.environ['HBNB_MYSQL_DB'] = 'hbnb_dev_db'
    os.environ['HBNB_TYPE_STORAGE'] = 'db'

    # Define the command to create the City object
    command = f'echo \'create City state_id="{state_id}" name="{city_name}"\' | ./console.py'

    # Execute the command
    subprocess.run(command, shell=True, env=os.environ)

# Usage example
if __name__ == "__main__":
    state_id = "95a5abab-aa65-4861-9bc6-1da4a36069aa"
    city_name = "San_Francisco"
    create_city(state_id, city_name)

