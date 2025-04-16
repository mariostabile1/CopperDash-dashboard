import pandas as pd
import base64
import io

def parse_dataset(dataset_contents):
    # il componente dcc.Upload carica un qualsiasi file come stringa Base64 quindi va decodificata
    dataset_string = dataset_contents.split(",")[1] # [1] separa i metadati dal contenuto vero e proprio
    # prende la stringa dataset_string codificata, la decodifica e la mette dentro decoded
    decoded = base64.b64decode(dataset_string)
    
    try:
        # decodifica il dataset in un dataframe
        loaded_dataset_dataframe = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
        # prepara il dataset per le DataTable di dash, in colonne e dati
        columns = [{"name": col, "id": col} for col in loaded_dataset_dataframe.columns]
        data = loaded_dataset_dataframe.to_dict('records') #ogni record avrà una riga
        
        return columns, data # restituisce le colonne e i dati 
    except Exception as e:
        
        print(f"Errore durante la lettura del dataset: {e}")
        return [], [] # in caso di errore restituisce le colonne e i dati vuoti

"""
# Funzione per processare i dati per il grafico (da implementare in base alle tue esigenze)
def process_data_for_chart(df):
    # Esempio: seleziona le prime 10 righe e due colonne numeriche
    if not df.empty and len(df.columns) >= 2:
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        if len(numeric_cols) >= 2:
            return df.iloc[:10, [df.columns.get_loc(numeric_cols[0]), df.columns.get_loc(numeric_cols[1])]].rename(columns={numeric_cols[0]: 'colonna_x', numeric_cols[1]: 'colonna_y'})
    return pd.DataFrame({'colonna_x': [], 'colonna_y': []})
"""