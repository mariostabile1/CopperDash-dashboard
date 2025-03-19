from dash import Dash
import layout

# Inizializzo l'app
app = Dash(__name__)

# Assegno il layout
app.layout = layout.layout

# Avvio dl server
if __name__ == "__main__":
    app.run(debug=True)