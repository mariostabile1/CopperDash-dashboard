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
