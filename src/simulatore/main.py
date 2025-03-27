import numpy as np
import pandas as pd
import os

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
rng = np.random.default_rng() # genero un'istanza di Generator, per usare la nuova API sulla generazione di valori random (come descritto nella documentazione di numpy)

KEY_VALUE = {
    # Variabili operative
    "mining_depth": {"low": 500, "high": 150},
    "daily_extracted_ammount": {"avg": 250, "stdev": 80},
    #"mining_efficiency": (85, 10),
    "daily_energy_consumtion": {"mean": 35, "sigma": 0.2},
    "daily_working_hours": {"avg": 12, "stdev": 2},
    
    # Variabili economiche   
    "material_price": {"avg": 7148.60, "stdev": 1686}, # Da fonte (testa del file)
    "daily_expenses": {"shape": 8500, "scale": 500},
    #daily_earnings = (material_price * daily_extracted_ammount) - daily_expences
    
    # Variabili ambientali
    #"air_quality": (75, 15),
    "temperature": {"avg": 20, "stdev": 10},
    
    # Fenomeni imprevedibili
    "strike_days": {"avg": 0.01}, # Sarebbero gli scioperi, google traduttore me la da così
    "machine_breakdowns": {"avg": 0.03}
}

DAYS_RANGE = 25
TRUNKED_DECIMAL = 2
DATASET_PATH = os.path.abspath("../dataset/mining_dataset.csv")

# Referenza: np.random.normal(loc: float o array <media>, scale: floats o array <deviazione standard>, scale: int o tuple <forma della distribuzione>)

def normal_distr_calc(avg, stdev)):
    avg, stdev = KEY_VALUE[value]
    return np.round(rng.normal(avg, stdev, DAYS_RANGE), TRUNKED_DECIMAL)

def poisson_distr_calc(avg):
    avg = KEY_VALUE[value]
    return np.round(rng.poisson(avg, DAYS_RANGE), TRUNKED_DECIMAL)

def uniform_distr_calc(low, high):
    low, high = KEY_VALUE[value]
    return np.round(rng.uniform(low, high, DAYS_RANGE), TRUNKED_DECIMAL)

def gamma_distr_calc(shape, scale):
    shape, scale = KEY_VALUE[value]
    return np.round(rng.gamma(shape, scale, DAYS_RANGE), TRUNKED_DECIMAL)

def beta_distr_calc(a, b):
    a, b = KEY_VALUE[value]
    return np.round(rng.beta(a, b, DAYS_RANGE), TRUNKED_DECIMAL)

def lognormal_dist_calc(mean, sigma):
    mean, sigma = KEY_VALUE[value]
    return np.round(rng.lognormal(mean, sigma, DAYS_RANGE), TRUNKED_DECIMAL)

def generate_dataset(DAYS_RANGE = DAYS_RANGE, output_dataset = DATASET_PATH):
    mining_depth = uniform_distr_calc(KEY_VALUE["mining_depth"])
    daily_extracted_ammount = normal_distr_calc(KEY_VALUE["daily_extracted_ammount"])
    daily_energy_consumtion = lognormal_dist_calc(KEY_VALUE["daily_energy_consumtion"])
    daily_working_hours = normal_distr_calc(KEY_VALUE["daily_working_hours"])
    material_price = normal_distr_calc(KEY_VALUE["material_price"])
    daily_expenses = gamma_distr_calc(KEY_VALUE["daily_expenses"])
    daily_earnings = (material_price * daily_extracted_ammount) - daily_expenses
    temperature = normal_distr_calc(KEY_VALUE["temperature"])
    strike_days = poisson_distr_calc(KEY_VALUE["strike_days"])
    machine_breakdowns = poisson_distr_calc(KEY_VALUE["machine_breakdowns"])
    
    dataset_dataframe = pd.DataFrame(
        {
            "Mining depth": mining_depth,
            "Daily extracted ammount": daily_extracted_ammount,
            "Daily energetic consumtion": daily_energy_consumtion,
            "Working hours": daily_working_hours,
            "Copper price": material_price,
            "Daily expenses": daily_expenses,
            "Daily earnings":daily_earnings ,
            "Temperature": temperature,
            "Workers Strikes": strike_days,
            "Machine breakdowns": machine_breakdowns
        }
    )
    dataset_dataframe.to_csv(output_dataset, index = False)
    
generate_dataset(DAYS_RANGE, DATASET_PATH)