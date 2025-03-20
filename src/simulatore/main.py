import numpy as np
import pandas as pd

"""
prezzo medio rame in USD/tonnellata tra 2015-2025
fonte: International Monetary Fund
link: https://fred.stlouisfed.org/series/PCOPPUSDM
copyright: guarda documentazione
MEDIA: 7148.60
DEV STANDARD: 1686.26 (approssimato per difetto a 2 cifre decimali)

Lista variabili da generare:

Variabili operative:
- profondità di scavo (metri)
- quantità estratta (tonnelllate/giorno) (gaussiana/normale)
- efficienza attrezzature/impianti (%)
- consumo energetico (MegaWatt/ora)
- ore di lavoro giornaliere (ore/giorno)

Variabili economiche:
- prezzo del materiale grezzo (dollaro/tonnellata) (normale)
- costo giornaliero: energia, salari, manutenzione (dollari/giorno) 
- stima guadagno giornaliero (dollari/giorno)

Variabili ambientali (generalmente imprevedibili):
- temperatura sotterranea (C°)
- qualità dell'aria (% gas nocivi)
- fattori imprevedibili (scioperi, guasti, meteo imprevedibile) (eventi discreti casuali quindi poisson)
"""

KEY_VALUE = {
    "mining_depth": (500, 150),
    "daily_extracted_ammount": (250, 80),
    "mining_efficiency": (85, 10),
    "material-price": (7148.60, 1686), # Da fonte (testa del file)
    "air-quality": (75, 15),
    "margin-of-profit": (20, 5),
    "temperature": (20, 10)
}
