# Lista degli indici KPI (Key Performance Indicator)
# - Mining Productivity
# - Cost per ton
# - Energetic Efficiency
# - Daily operating margin

def calculate_kpi(dataframe):
    # assegno un sotto-dataframe che contiene solo i dati delle singole colonne del dataset
    extracted_ton_raw = dataframe["Daily extracted ammount raw (tons)"]
    working_hours = dataframe["Working hours"]
    daily_expenses = dataframe["Daily expenses ($)"]
    raw_copper_content = dataframe["Copper content in raw material (%)"]
    daily_consumtion = dataframe["Daily energetic consumtion (MW/h)"]
    daily_earnings = dataframe["Estimated daily earnings ($)"]

    # tonnellate di rame puro estratto
    pure_copper_ton = extracted_ton_raw * (raw_copper_content / 100)
    
    return { # .mean calcola la media di tutti i valori per cui viene fatto questo calcolo, visto che sono ddei dataframe e non classiche variabili
        "kpi_1": (extracted_ton_raw / working_hours).mean(), # produttività
        "kpi_2": (daily_expenses / pure_copper_ton).mean(), # costo per tonnellata rame puro
        "kpi_3": (daily_consumtion / pure_copper_ton).mean(), # efficienza energetica
        "kpi_4": (daily_earnings / pure_copper_ton).mean(), # margine operativo
    }
