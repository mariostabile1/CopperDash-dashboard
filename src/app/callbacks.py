from dash import Input, Output
from data import parse_dataset

def register_callbacks(app):
    # callback per la tabella del dataset
    @app.callback(
        [
        Output("dataset_table", "columns"), # restituisce le colonne del dataset
        Output("dataset_table", "data"), # resitutisce il contenuto del dataset
        Output("file_name", "children") # restituisce anche il nome del file
        ], 
        #Output("stored_dataframe", "data")], # Output per memorizzare il DataFrame
        [
        Input("load_dataset_button", "contents"), # prende in input proprio il file csv
        Input("load_dataset_button", "filename") # prende in input anche il nome del file CSV
        ] 
    )
    def update_table(contents, filename):
        if contents is not None:
            try:
                columns, data = parse_dataset(contents)
                return columns, data, filename
            except Exception as e:
                print(f"Errore nel callback di caricamento: {e}")
                return [], [], ""
        return [], [], ""
    
    #--------------------------------------------------------------------------#
    # callback per il grafico principale
"""
    @app.callback(
        Output("dataset_graph", "figure"),
        Input("stored_dataframe", "data")
    )

    def update_chart_on_data(stored_data):
        if stored_data is not None:
            df = pd.DataFrame(stored_data)
            numeric_cols = df.select_dtypes(include = ['number']).columns.tolist()
            if len(numeric_cols) >= 2:
                x_col = numeric_cols[0]
                y_col = numeric_cols[1]
                fig = px.line(df, x = x_col, y = y_col, title = f'Line Graph di {y_col} vs {x_col}')
                return fig
            else:
                return None
        else:
            return None
        
    #--------------------------------------------------------------------------#
    # callback per i grafici dei kpi
"""