import json
import csv
import pandas as pd

from . import constants as c

def save_json_file(path, json_data):
    save_info = open(path, 'w', encoding='utf-8')
    save_info.write(json.dumps(json_data) + c.NEW_LINE)
    save_info.close()

def update_json_file(path, json_data):
    save_info = open(path, 'a', encoding='utf-8')
    save_info.write(json.dumps(json_data) + c.NEW_LINE)
    save_info.close()

def create_empty_csv_file(path, columns):
    df = pd.DataFrame(columns=columns)
    df.to_csv(path, index=False)    
    

def update_csv_file(path, new_data):
    try:
        with open(path, 'a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)

            csv_writer.writerows(new_data)        

    except IOError as e:
        print(f"Error adding lines to CSV file: {e}")    