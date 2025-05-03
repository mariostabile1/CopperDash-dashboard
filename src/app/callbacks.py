from dash import Input, Output, State
from data import parse_dataset
from kpi import calculate_kpi
import plotly.express as px
import plotly.graph_objects as go
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
                dropdown_options = [{"label": col, "value": col} for col in dataframe.columns[1:10]] # popola il menù a tendina dalla colonna 2 a 10
                return columns, data, filename, dropdown_options
            
            except Exception as e:
                print(f"Callback error: {e}")
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
                dataframe[dataframe.columns[0]] = pd.to_datetime(
                    dataframe[dataframe.columns[0]], 
                    errors = "coerce",
                    dayfirst = True
                    )
                return px.bar(
                    dataframe, 
                    x = dataframe.columns[0], 
                    y = selected_column, 
                    title=f"{selected_column} - over time") # da il valore agli assi e il titolo
            except Exception as e:
                
                print(f"Errore nel grafico: {e}") # in caso di errore stampa questa linea
                return px.line(title = "Choose a column to show on graph") # se non si sceglie la colonna dal menù a tendina lo considera come errore, quindi mostra questo
        else:
            return px.line(title = "Upload dataset then choose a column to show on graph")
        
    #--------------------------------------------------------------------------#
    # callback per i grafici dei kpi
    
    # costruisce la 'figura' che sarà visualizzata nella dashboard
    def build_kpi_figure(value, title, suffix):
        
        kpi_figure = go.Figure(go.Indicator( # crea una figura di dash con un componente chiamato Indicator
            mode = "number", # mostra solo il numero
            value = value, # il valore da visualizzare
            number = {"font": {"size": 50, "color": "gray"}, "valueformat": ",.0f", "suffix": f"{suffix}"}, # personalizzazione della scritta del numero, con il formato e il suffisso
            title = {"text": title, "font": {"size": 18, "color": "gray"}}, # il titolo del kpi con il suo stile
            domain={"x": [0, 1], "y": [0, 1]} # definisco quanto spazio occupa l'area della figura (tutto lo spazio disponibile in questo caso)
        ))
        # è un metodo che aggiorna lo stile della figura (t, b, l, r sono i vari margini)
        kpi_figure.update_layout(paper_bgcolor = "white", height = 250, margin = dict(t = 40, b = 40, l = 20, r = 20))
        
        return kpi_figure   
    
    # è la stessa identica figura rispetto a quella di sopra che viene usata solo per mantenere continuità grafica al prosto di vedere un grafico dcc.Graph vuoto
    # e viene chiamata solo nel caso in cui non sia stato caricato il dataset
    def build_empty_kpi_placeholder():
        empty_kpi_figure = go.Figure(go.Indicator( # crea una figura di dash con un componente chiamato Indicator
            mode = "number", # mostra solo il numero
            value = 0, # il valore da visualizzare
            number = {"font": {"size": 50, "color": "gray"}, "suffix": ""}, # personalizzazione della scritta del numero, con il formato e il suffisso
            title = {"text": "KPI - Awaiting for dataset to upload", "font": {"size": 18, "color": "gray"}}, # il titolo del kpi con il suo stile
            domain={"x": [0, 1], "y": [0, 1]} # definisco quanto spazio occupa l'area della figura (tutto lo spazio disponibile in questo caso)
        ))
        # è un metodo che aggiorna lo stile della figura (t, b, l, r sono i vari margini)
        empty_kpi_figure.update_layout(paper_bgcolor = "white", height = 250, margin = dict(t = 40, b = 40, l = 20, r = 20))
        
        return empty_kpi_figure  

    @app.callback(
        [
        Output("kpi_1", "figure"), # sono gli id delle sezioni del layout
        Output("kpi_2", "figure"),
        Output("kpi_3", "figure"),
        Output("kpi_4", "figure"),
        ],
        Input("load_dataset_button", "contents") # l'input del callback è la pressione del tasto nel layout
    )
    
    def update_kpi_graph(contents):
        if contents is not None:
            _, _, dataframe = parse_dataset(contents)
            
            try:
                kpi = calculate_kpi(dataframe) # calcolo i numeri dei kpi dalla funzione in kpi.py
                
                # chiamo la funzione che costruisce la figura per ogni kpi
                kpi_1 = build_kpi_figure(kpi.get("kpi_1", 0), "Tons of ore mined per working hour", " Ton/hour")
                kpi_2 = build_kpi_figure(kpi.get("kpi_2", 0), "Operating cost per ton of pure copper", " $/ton")
                kpi_3 = build_kpi_figure(kpi.get("kpi_3", 0), "KW per ton of copper mined", " KW/ton")
                kpi_4 = build_kpi_figure(kpi.get("kpi_4", 0), "Net earnings per ton of copper", " $/ton")
                
                return kpi_1, kpi_2, kpi_3, kpi_4
            
            except Exception as e:
                print(f"Graph error: {e}") # in caso di errore stampa questa linea
                return  build_empty_kpi_placeholder(), build_empty_kpi_placeholder(), build_empty_kpi_placeholder(), build_empty_kpi_placeholder() # restituisco la figura placaholder
        else:
            return build_empty_kpi_placeholder(), build_empty_kpi_placeholder(), build_empty_kpi_placeholder(), build_empty_kpi_placeholder()