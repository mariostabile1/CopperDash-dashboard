from dash import Dash
import layout
from callbacks import register_callbacks

# Inizializzo l'app
app = Dash(__name__)

# Assegno il layout
app.layout = layout.layout
"""
app.layout = html.Div([
    layout.layout,
    #dcc.Store(id = "stored_dataframe")
])
"""

register_callbacks(app)

# Avvio dl server
if __name__ == "__main__":
    app.run(debug=True)