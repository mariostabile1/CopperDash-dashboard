from dash import dcc, html, dash_table
import plotly.graph_objects as go

# Definizione del layout principale della dashboard
layout = html.Div(
    style = {
        "display": "grid",  # layout a griglia, mi risultava più facile che posizionare tutto a mano
        "gridTemplateAreas": "'header header' 'sidebar main' 'footer footer'", 
        "gridTemplateColumns": "1fr 6fr",  # sidebar di larghezza fissa, contenuto principale adattabile
        "gridTemplateRows": "auto 1fr auto",  # seader e footer con altezza automatica, contenuto principale flessibile
        "height": "120vh",  # Occupa tutta l'altezza della finestra
        "fontFamily": "sans-serif",
        "backgroundColor": "#1F2935",
        "width": "100%"
        
    },
    children = [
        # Header della dashboard
        html.Header(
            style = {
                "gridArea": "header",
                "backgroundColor": "#768188",
                "padding": "20px",
                "display": "flex",
                "justifyContent": "space-between",
                "alignItems": "center",
                "borderRadius": "8px",
                "alignText": "center",
            },
            children = [
                # testo che verrà mostrato nella barra dell'header
                html.Div("KPI Dashboard for primary sector analysis"),
            ],
        ),
        #--------------------------------------------------------------------------#
        # Barra laterale per filtri e controlli
        html.Aside(
            style = {
                "gridArea": "sidebar",
                "backgroundColor": "#7E8D9F",
                "padding": "20px",
                "borderRight": "1px solid #ccc",
                "borderRadius": "8px",
                "marginTop": "20px",
                "marginBottom": "20px"
            },
            children = [
                # letteralmente il bottone upload
                dcc.Upload(
                    id = "load_dataset_button",
                    children = html.Button(
                        "Load Dataset",
                        style = {
                            "fontSize": "20px",
                            "borderRadius": "8px",
                            "border": "1px solid #7E8D9F",
                        }
                    ),
                    multiple = False, # si può capicare solo in file alla volta
                    accept = ".csv" # accetta l'upload solo di file .csv
                ),
                html.Div(id="file_name", style={"margin": "10px", "color": "white"}),
                
                # menù a tendina
                dcc.Dropdown(
                    id = "column_selector",
                    placeholder = "choose a column", # testo che viene mostrato di default
                    style = {
                        "width": "100%", # fa usare tutta la larghezza disponibile
                        "whiteSpace": "normal", # fa andare a capo le opzioni
                    }
                )
            ],
        ),
        #--------------------------------------------------------------------------#
        # Sezione principale della dashboard
        html.Main(
            style = {
                "gridArea": "main",
                "padding": "20px",
                "display": "grid",  # Sottogriglia per KPI, grafici e tabelle
                "gridTemplateAreas": "'kpi kpi kpi kpi' 'charts charts charts charts' 'tables tables tables tables'",
                "gridGap": "20px",
                "backgroundColor": "#1F2935",
            },
            children = [
                # Sezione KPI
                html.Div(
                    style = {
                        "gridArea": "kpi",
                        "display": "flex",
                        "justifyContent": "space-around",
                        "borderBottom": "1px solid #cccc",
                        "paddingBottom": "20px",
                    },
                    children = [
                        html.Div(
                            style = {
                                "width": "25%",
                                "height": "100%",
                                "backgroundColor": "#A3D0C5",
                                "border": "1px solid black",
                                "margin": "5px",
                                "borderRadius": "8px",  # Arrotonda i bordi delle KPI
                            },
                            children = [
                                dcc.Graph(
                                    id = "kpi_1",
                                    config = {"displayModeBar": False}
                                ),
                            ],  
                        ),
                        html.Div(
                            style = {
                                "width": "25%",
                                "height": "100%",
                                "backgroundColor": "#A3D0C5",
                                "border": "1px solid black",
                                "margin": "5px",
                                "borderRadius": "8px",
                            },
                            children = [
                                dcc.Graph(
                                    id = "kpi_2", 
                                    config = {"displayModeBar": False}
                                ),    
                            ],
                        ),
                        html.Div(
                            style = {
                                "width": "25%",
                                "height": "100%",
                                "backgroundColor": "#A3D0C5",
                                "border": "1px solid black",
                                "margin": "5px",
                                "borderRadius": "8px",
                            },
                            children = [
                                dcc.Graph(
                                    id = "kpi_3", 
                                    config = {"displayModeBar": False}
                                ),
                            ],
                        ),
                        html.Div(
                            style = {
                                "width": "25%",
                                "height": "100%",
                                "backgroundColor": "#A3D0C5",
                                "border": "1px solid black",
                                "margin": "5px",
                                "borderRadius": "8px",
                            },
                            children = [
                                dcc.Graph(
                                    id = "kpi_4", 
                                    config = {"displayModeBar": False}
                                ),
                            ],
                        ),
                    ]
                ),
                # Sezione grafici
                html.Div(
                    style = {
                        "gridArea": "charts",
                        "backgroundColor": "#6DC7AF",
                        "padding": "20px",
                        "border": "1px solid #ccc",
                        "borderRadius": "8px",  # Arrotonda i bordi dei grafici
                    },
                    children = [
                        # questo è il grafico principale, sopra la tabella del dataset
                        dcc.Graph(
                            id = "dataset_graph",
                            style = {
                                "backgroundColor": "#768188",
                            }
                        )    
                    ],
                ),
                # Sezione tabelle
                html.Div(
                    style = {
                        "gridArea": "tables",
                        "backgroundColor": "#6DC7AF",
                        "padding": "10px",
                        "border": "1px solid #ccc",
                        "borderRadius": "8px", # Arrotonda i bordi delle tabelle
                        "position": "relative",
                        "overflowX": "auto", 
                        "display": "flex", # Abilita Flexbox per il contenitore
                        #"justifyContent": "center", # Allinea orizzontalmente al centro
                        "alignItems": "center", # Allinea verticalmente al centro (se l'altezza del div lo permette)
                        "minHeight": "100px", 
                    },
                    children = [
                        # tabella del dataset
                        dash_table.DataTable(
                            id = "dataset_table",
                            columns = [], # columns e data queste vengono popolate dalle funzioni di callback
                            data = [],    # quindi qui le dichiaro vuote
                            page_size = 10, # numero massimo di righe della tabella visualizzabili contemporaneamente senza cambiare pagina
                            style_table = {
                                "overflowX": "auto", # se la tabella è troppo grande abilita lo scroll interno, qui orizzontale, sotto verticale
                                "overflowY": "auto",
                                },
                            style_cell = {"textAlign": "left"}, # allineo i valori delle celle a sinistra
                            page_action = "native" # uso la paginazione nativa del browser
                        ),
                    ],
                ),
            ],
        ),
        # Footer della dashboard
        html.Footer(
            style = {
                "gridArea": "footer",
                "backgroundColor": "#768188",
                "padding": "10px",
                "textAlign": "center",
                "borderTop": "1px solid #ccc",
                "borderRadius": "8px",  # Arrotonda solo gli angoli inferiori
            },
            children = "Author: Mario Stabile",
        ),
    ],
)