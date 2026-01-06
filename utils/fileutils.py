import pandas as pd
import base64

def read_json(filepath):
    return pd.read_json(filepath)

def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        # Read the file and encode it
        encoded_string = base64.b64encode(image_file.read())
        
        # Convert bytes to a UTF-8 string
        return encoded_string.decode('utf-8')