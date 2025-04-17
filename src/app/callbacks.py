from dash import Input, Output, State
from data import parse_dataset
import plotly.express as px
import pandas as pd

def register_callbacks(app):
    # callback per la tabella del dataset
    @app.callback(
        [
        Output("dataset_table", "columns"), # restituisce le colonne del dataset
        Output("dataset_table", "data"), # resitutisce il contenuto del dataset
        Output("file_name", "children"), # restituisce anche il nome del file
        Output("column_selector", "options"), # aggiorna il dropdown
        ], 
        [
        Input("load_dataset_button", "contents"), # prende in input proprio il file csv
        Input("load_dataset_button", "filename") # prende in input anche il nome del file CSV
        ] 
    )
    
    def update_table(contents, filename):
        if contents is not None:
            try:
                columns, data, dataframe = parse_dataset(contents)
                dropdown_coptions = [{"label": col, "value": col} for col in dataframe.columns[1:10]]
                return columns, data, filename, dropdown_coptions
            
            except Exception as e:
                print(f"Errore nel callback di caricamento: {e}")
                return [], [], "", []
            
        return [], [], "", []
    
    #--------------------------------------------------------------------------#
    # callback per il grafico principale

    @app.callback(
        Output("dataset_graph", "figure"),
        Input("column_selector", "value"),
        State("load_dataset_button", "contents"),
        State("load_dataset_button", "filename")
    )

    def update_main_graph(selected_column, contents, filename):
        if contents is not None or selected_column is not None:
            _, _, dataframe = parse_dataset(contents) # _ indica che il parametro che dovrebbe essere la non verrà usato, quindi viene dichiarato senza nome
            
            try:
                dataframe[dataframe.columns[0]] = pd.to_datetime(dataframe[dataframe.columns[0]])  # Assegna tipo datetime alla prima colonna
                return px.bar(dataframe, x = dataframe.columns[0], y = selected_column, title=f"{selected_column} nel tempo")
            except Exception as e:
                print(f"Errore nel grafico: {e}")
                return px.line(title="Errore nel grafico")
        else:
            return px.line()
    #--------------------------------------------------------------------------#
    # callback per i grafici dei kpi
