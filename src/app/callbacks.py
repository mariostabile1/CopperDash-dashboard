from dash import Input, Output, State
from data import parse_dataset
from kpi import calculate_kpi
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
    # funzione che prende i dati dal dataset e popola, la tabella e il componente a tendina con le colonne da mostrare
    def update_dataset_table(contents, filename):
        if contents is not None:
            try:
                columns, data, dataframe = parse_dataset(contents) # chiamata a data per il parsing del dataset
                dropdown_coptions = [{"label": col, "value": col} for col in dataframe.columns[1:10]] # popola il menù a tendina dalla colonna 2 a 10
                return columns, data, filename, dropdown_coptions
            
            except Exception as e:
                print(f"Errore nel callback di caricamento: {e}")
                return [], [], "", [] # in caso di errore restituisce tutto vuoto
            
        return [], [], "", []
    
    #--------------------------------------------------------------------------#
    # callback per il grafico principale

    @app.callback(
        Output("dataset_graph", "figure"), # da in output i dati delle colonne scelte, al grafico
        Input("column_selector", "value"), # prende in input la colonna da mostare in output, nel menù a tendina
        State("load_dataset_button", "contents"), # prende solo i valore del contenuto dopo
        State("load_dataset_button", "filename")
    )

    def update_main_graph(selected_column, contents, filename):
        if contents is not None or selected_column is not None:
            _, _, dataframe = parse_dataset(contents) # _ indica che il parametro che dovrebbe essere la non verrà usato, quindi viene dichiarato senza nome
            
            try:
                # assegna tipo datetime alla prima colonna
                # errors = "coerce" evita di alzare errori che interrompono il flusso del codice in caso di mal formazione della data
                # dayfirst = True serve ad evitare che pandas interpreti male le date in formato europeo (giorno/mese/anno), visto che di base usa il formato americano (mese/giorno/anno)
                dataframe[dataframe.columns[0]] = pd.to_datetime(dataframe[dataframe.columns[0]], errors = "coerce", dayfirst = True)   
                return px.bar(dataframe, x = dataframe.columns[0], y = selected_column, title=f"{selected_column} - over time") # da il valore agli assi e il titolo
            except Exception as e:
                
                print(f"Errore nel grafico: {e}") # in caso di errore stampa questa linea
                return px.line(title="N/A") 
        else:
            return px.line(title = "N/A") # grafico vuoto
        
    #--------------------------------------------------------------------------#
    # callback per i grafici dei kpi
    
    def build_kpi_figure_px(value, y_label, ref_min, ref_max, title):
        dataframe = pd.DataFrame({"KPI": [value], "Categoria": [y_label]})
        kpi_figure = px.bar(dataframe, x = "KPI", y = "Categoria" , orientation = "h", title = title)
        #kpi_figure.add_vline(x=ref_min, line_dash="dash", line_color="orange")
        #kpi_figure.add_vline(x=ref_max, line_dash="dash", line_color="green")
        kpi_figure.update_layout(xaxis = dict(range=[0, max(value * 1.6, 1)]), height = 250, margin = dict(t = 40, b = 40, l = 20, r = 20))
        return kpi_figure

    @app.callback(
        [
        Output("kpi_1", "figure"),
        Output("kpi_2", "figure"),
        Output("kpi_3", "figure"),
        Output("kpi_4", "figure"),
        ],
        Input("load_dataset_button", "contents")
    )
    
    def update_kpi_graph(contents):
        if contents is not None:
            _, _, dataframe = parse_dataset(contents)
            #print(dataframe)
            try:
                kpi = calculate_kpi(dataframe)
                print(kpi.get("kpi_1", 0))  # o anche print(kpi)
                kpi_1 = build_kpi_figure_px(kpi.get("kpi_1", 0), "Ton/ora", 200, 600, "Tonnellate di minerale estratto per ora lavorativa")
                kpi_2 = build_kpi_figure_px(kpi.get("kpi_2", 0), "Costo/ton", 30, 80, "Costo operativo per tonnellata di rame puro")
                kpi_3 = build_kpi_figure_px(kpi.get("kpi_3", 0), "KW/ton", 200, 1000, "KW per tonnellata di rame estratto")
                kpi_4 = build_kpi_figure_px(kpi.get("kpi_4", 0), "$/ton", 100, 300, "Guadagno netto per tonnellata di rame")
                
                #kpi_1 = px.bar(x=[""], y=[kpi.get("kpi_1", 0)], title="Tonnellate di minerale estratto per ora lavorativa")
                #kpi_2 = px.bar(x=[""], y=[kpi.get("kpi_2", 0)], title="Costo operativo per tonnellata di rame puro")
                #kpi_3 = px.bar(x=[""], y=[kpi.get("kpi_3", 0)], title="KW per tonnellata di rame estratto")
                #kpi_4 = px.bar(x=[""], y=[kpi.get("kpi_4", 0)], title="Guadagno netto per tonnellata di rame")
                #print(kpi_1), kpi[1], kpi[2], kpi[3])
                return kpi_1, kpi_2, kpi_3, kpi_4
            
            except Exception as e:
                print(f"Errore nel grafico: {e}") # in caso di errore stampa questa linea
                return  None, None, None, None
        else:
            return None, None, None, None