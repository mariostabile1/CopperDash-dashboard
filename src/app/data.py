import pandas as pd
import os
import base64
import io

#DATASET = os.path.abspath("../dataset/mining_dataset.csv")

def parse_dataset(dataset):
    dataset_type, dataset_string = dataset.split(",")
    decoded = base64.b64decode(dataset_string)
    loaded_dataset = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
    
    columns = [{"name": col, "id": col} for col in loaded_dataset.columns]
    data = loaded_dataset.to_dict('records')
    return columns, data
    
