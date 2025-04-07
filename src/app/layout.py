from dash import dcc, html, dash_table

# Definizione del layout principale della dashboard
layout = html.Div(
    style = {
        "display": "grid",  # Layout a griglia
        "gridTemplateAreas": "'header header header' 'sidebar main main' 'footer footer footer'",
        "gridTemplateColumns": "200px 1fr",  # Sidebar di larghezza fissa, contenuto principale adattabile
        "gridTemplateRows": "auto 1fr auto",  # Header e footer con altezza automatica, contenuto principale flessibile
        "height": "120vh",  # Occupa tutta l'altezza della finestra
        "margin": "0",
        "padding": "0",
        "fontFamily": "sans-serif",
        "backgroundColor": "#1F2935",
        #"minHeight": "1000px",
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
                "borderBottom": "1px solid #ccc",
                "borderRadius": "8px",
            },
            children = [
                html.Div("Logo Aziendale"),
                html.Div("Titolo Dashboard"),
                html.Div("Selettore Periodo"),
            ],
        ),
        # --------------------------------------------------------------------------
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
                dcc.Upload(
                    id = "load_dataset_button",
                    children = html.Button(
                        "Carica Dataset",
                        style = {
                            "fontSize": "20px",
                            "borderRadius": "8px",
                            "border": "1px solid #7E8D9F",
                        }
                    ),
                    multiple = False,
                    accept = ".csv"
                ),
                html.Div(id="file-name", style={"marginTop": "10px", "color": "white"}),
            ],
        ),
        # --------------------------------------------------------------------------
        # Sezione principale della dashboard
        html.Main(
            style = {
                "gridArea": "main",
                "padding": "20px",
                "display": "grid",  # Sottogriglia per KPI, grafici e tabelle
                "gridTemplateAreas": "'kpi kpi kpi kpi' 'charts charts charts charts' 'tables tables tables tables'",
                "gridGap": "20px",
                "backgroundColor": "#1F2935",
                "minHeight": "1000px",  # Aumenta l'altezza minima della sezione main
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
                            children = "KPI1",
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
                            children = "KPI2",
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
                            children = "KPI3",
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
                            children = "KPI4",
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
                    children = "Grafici",
                ),
                # Sezione tabelle
                html.Div(
                    style = {
                        "gridArea": "tables",
                        "backgroundColor": "#6DC7AF",
                        "padding": "10px",
                        "border": "1px solid #ccc",
                        "borderRadius": "8px",  # Arrotonda i bordi delle tabelle
                        "position": "relative",
                        "overflowX": "auto",
                        "display": "flex",        # Abilita Flexbox per il contenitore
                        #"justifyContent": "center", # Allinea orizzontalmente al centro
                        "alignItems": "center",     # Allinea verticalmente al centro (se l'altezza del div lo permette)
                        "minHeight": "50px", 
                    },
                    children = [

                        dcc.Loading(
                            type = "circle",
                            children = [
                                dash_table.DataTable(
                                    id = "dataset_table",
                                    columns = [],
                                    data = [],
                                    page_size = 12,
                                    style_table = {
                                        "overflowX": "auto",
                                        #"overflowY": "auto",
                                        #"position": "absolute",
                                        #"top": 0,
                                        #"left": 0
                                        },
                                    style_cell = {"textAlign": "left"},
                                    page_action = "native"
                                ),
                            ],
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