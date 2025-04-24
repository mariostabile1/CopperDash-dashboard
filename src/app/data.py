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
        
        return columns, data, loaded_dataset_dataframe # restituisce le colonne e i dati e il dataframe per i grafici
    except Exception as e:
        
        print(f"Errore durante la lettura del dataset: {e}")
        return [], [], pd.DataFrame() # in caso di errore restituisce le colonne, i dati vuoti e un dataframe vuoto

