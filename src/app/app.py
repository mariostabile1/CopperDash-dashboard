from dash import Dash
import layout
from callbacks import register_callbacks

# Inizializzo l'app
app = Dash(__name__)

# Assegno il layout
app.layout = layout.layout

register_callbacks(app) # chiamo la funzione dei callback

# Avvio dl server
if __name__ == "__main__":
    app.run(debug = False) # di default il server gira in localhost su porta 8050 (127.0.0.1:8050)
