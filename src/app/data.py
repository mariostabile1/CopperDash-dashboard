"""
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
    
"""

import pandas as pd
import os
import base64
import io

#DATASET = os.path.abspath("../dataset/mining_dataset.csv")

def parse_dataset(dataset):
    dataset_type, dataset_string = dataset.split(",")
    decoded = base64.b64decode(dataset_string)
    try:
        loaded_dataset = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
        columns = [{"name": col, "id": col} for col in loaded_dataset.columns]
        data = loaded_dataset.to_dict('records')
        return columns, data, loaded_dataset # Restituisci anche il DataFrame
    except Exception as e:
        print(f"Errore durante la lettura del dataset: {e}")
        return [], [], pd.DataFrame()

# Funzione per processare i dati per il grafico (da implementare in base alle tue esigenze)
def process_data_for_chart(df):
    # Esempio: seleziona le prime 10 righe e due colonne numeriche
    if not df.empty and len(df.columns) >= 2:
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        if len(numeric_cols) >= 2:
            return df.iloc[:10, [df.columns.get_loc(numeric_cols[0]), df.columns.get_loc(numeric_cols[1])]].rename(columns={numeric_cols[0]: 'colonna_x', numeric_cols[1]: 'colonna_y'})
    return pd.DataFrame({'colonna_x': [], 'colonna_y': []})