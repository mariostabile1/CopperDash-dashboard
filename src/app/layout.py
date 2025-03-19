from dash import Dash
from dash import dcc, html

layout = html.Div(
    style={
        # Stile griglia dell'header
        "display": "grid",
        "gridTemplateAreas": "'header header header' 'sidebar main main' 'footer footer footer'",
        "gridTemplateColumns": "200px 1fr",  # fr = fractional unit, 1 = 25% della seconda colonna che si adatterà automaticamente
        "gridTemplateRows": "auto 1fr auto",
        "height": "100vh",  # vh = viewport height, la dashboard occupa tutto lo spazio della pagina
        "margin": 0,
        "padding": 0,
        "fontFamily": "sans-serif",
    },
    children=[
        # Header
        html.Header(
            style={
                "gridArea": "header",
                "backgroundColor": "#f0f0f0",  # Colore di sfondo grigio chiaro
                "padding": "20px",
                "display": "flex",
                "justifyContent": "space-between",  # Distribuzione uguale degli elementi
                "alignItems": "center",  # Allineamento verticale
                "borderBottom": "1px solid #ccc",  # Bordo inferiore che separa l'header
            },
            children=[
                html.Div("Logo Aziendale"),
                html.Div("Titolo Dashboard"),
                html.Div("Selettore Periodo"),
            ],
        ),
        # Barra laterale
        html.Aside(
            style={
                "gridArea": "sidebar",
                "backgroundColor": "#e0e0e0",  # Sfondo grigio per distingurela dal resto
                "padding": "20px",
                "borderRight": "1px solid #ccc",  # Bordo a destra per separarla
            },
            children=html.Div("Filtri e Controlli"),
        ),
        # Sezione principale
        html.Main(
            style={
                "gridArea": "main",
                "padding": "20px",
                "display": "grid",  # Sottogriglia per organizzare KPI, grafici e tabelle
                "gridTemplateAreas": "'kpi kpi kpi kpi' 'charts charts tables tables'",
                "gridGap": "20px",  # Distanza tra gli elementi
            },
            children=[
                # Sezione KPI
                html.Div(
                    style={
                        "gridArea": "kpi",
                        "display": "flex",
                        "justifyContent": "space-around",
                        "borderBottom": "1px solid #ccc",  # Bordo inferiore
                        "paddingBottom": "20px",
                    },
                    children=[html.Div(f"KPI {i+1}") for i in range(4)],
                ),
                # Sezione grafici
                html.Div(
                    style={
                        "gridArea": "charts",
                        "backgroundColor": "#fff",  # Sfondo bianco
                        "padding": "20px",
                        "border": "1px solid #ccc",  # Bordo per separare la sezione
                    },
                    children="Grafici",
                ),
                # Sezione tabelle
                html.Div(
                    style={
                        "gridArea": "tables",
                        "backgroundColor": "#fff",
                        "padding": "20px",
                        "border": "1px solid #ccc",
                    },
                    children="Tabelle",
                ),
            ],
        ),
        # Footer
        html.Footer(
            style={
                "gridArea": "footer",
                "backgroundColor": "#f0f0f0",
                "padding": "10px",
                "textAlign": "center",
                "borderTop": "1px solid #ccc",  # Bordo superiore per separare il footer
            },
            children="Footer",
        ),
    ],
)
