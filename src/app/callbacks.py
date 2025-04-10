"""
from dash import Input, Output, State, callback
from data import parse_dataset

def register_callbacks(app):
    @callback(
        [Output("dataset_table", "columns"),
        Output("dataset_table", "data"),
        Output("file-name", "children")],
        [Input("load_dataset_button", "contents")],
        [State("load_dataset_button", "filename")]
    )
    
    def update_output(dataset_contents, filename):
        if dataset_contents is not None:
            columns, data = parse_dataset(dataset_contents)
            return columns, data, f"File caricato: {filename}"
        
        return [], [], ""
"""

from dash import Input, Output, State, callback, dcc
from data import parse_dataset, process_data_for_chart
import plotly.express as px
import pandas as pd

def register_callbacks(app):
    @callback(
        [Output("dataset_table", "columns"),
        Output("dataset_table", "data"),
        Output("file_name", "children"),
        Output("stored_dataframe", "data")], # Output per memorizzare il DataFrame
        [Input("load_dataset_button", "contents")],
        [State("load_dataset_button", "filename")]
    )
    def update_on_dataset_load(dataset_contents, filename):
        if dataset_contents is not None:
            try:
                columns, data, df = parse_dataset(dataset_contents)
                return columns, data, f"File caricato: {filename}", df.to_dict('records')
            except Exception as e:
                print(f"Errore nel callback di caricamento: {e}")
                return [], [], "Errore nel caricamento del file", None
        return [], [], "", None

    @callback(
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
