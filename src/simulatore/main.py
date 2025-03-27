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

"""

rng = np.random.default_rng() # genero un'istanza di Generator, per usare la nuova API sulla generazione di valori random (come descritto nella documentazione di numpy)

KEY_VALUE = {
    # Variabili operative
    "mining_depth": {"low": 304.8, "high": 762},
    "annual_extracted_ammount_raw": {"avg": 101876, "stdev": 29829}, # Dati per estrazione annuale, dopo il calcolo della distribuzione viene trasformata in giornaliera
    "daily_energy_consumtion": {"mean": np.log(35), "sigma": 0.2},
    "daily_working_hours": {"avg": 12, "stdev": 2},
    "copper_content": {"avg": 0.43, "stdev": 0.05}, # % di rame nel materiale estratto
    
    # Variabili economiche   
    "material_price": {"avg": 7148.60, "stdev": 1686}, # Da fonte (testa del file)
    "daily_expenses": {"shape": 2, "scale": 25000},
    #daily_earnings = (material_price * daily_extracted_ammount) - daily_expences
    
    # Variabili ambientali
    "temperature": {"avg": 17.1, "stdev": 5},
    
    # Fenomeni imprevedibili
    "strike_days": {"avg": 0.01}, # Sarebbero gli scioperi, google traduttore me la da così
    "machine_breakdowns": {"avg": 0.03}
}

DAYS_RANGE = 253 # sono stati esclusi dai giorni lavorativi le principali feste e i weekend del paese in cui nasce la miniera (USA)
TRUNKED_DECIMAL = 2
DATASET_PATH = os.path.abspath("../dataset/mining_dataset.csv")

# Referenza: np.random.normal(loc: float o array <media>, scale: floats o array <deviazione standard>, scale: int o tuple <forma della distribuzione>)

def normal_distr_calc(avg, stdev):
    #avg, stdev = KEY_VALUE[value]
    return np.round(rng.normal(avg, stdev, DAYS_RANGE), TRUNKED_DECIMAL)

def poisson_distr_calc(avg):
    #avg = KEY_VALUE[value]
    return np.round(rng.poisson(avg, DAYS_RANGE), TRUNKED_DECIMAL)

def uniform_distr_calc(low, high):
    #low, high = KEY_VALUE[value]
    return np.round(rng.uniform(low, high, DAYS_RANGE), TRUNKED_DECIMAL)

def gamma_distr_calc(shape, scale):
    #shape, scale = KEY_VALUE[value]
    return np.round(rng.gamma(shape, scale, DAYS_RANGE), TRUNKED_DECIMAL)

def  beta_distr_calc(a, b):
    #a, b = KEY_VALUE[value]
    return np.round(rng.beta(a, b, DAYS_RANGE), TRUNKED_DECIMAL)

def lognormal_dist_calc(mean, sigma):
    #mean, sigma = KEY_VALUE[value]
    return np.round(rng.lognormal(mean, sigma, DAYS_RANGE), TRUNKED_DECIMAL)

def generate_dataset():
    mining_depth = uniform_distr_calc(KEY_VALUE["mining_depth"]["low"], KEY_VALUE["mining_depth"]["high"])
    annual_extracted_ammount_raw = normal_distr_calc(KEY_VALUE["annual_extracted_ammount_raw"]["avg"], KEY_VALUE["annual_extracted_ammount_raw"]["stdev"])
    daily_extracted_ammount_raw = np.round((annual_extracted_ammount_raw / DAYS_RANGE), TRUNKED_DECIMAL)
    copper_content = normal_distr_calc(KEY_VALUE["copper_content"]["avg"], KEY_VALUE["copper_content"]["stdev"])
    daily_energy_consumtion = lognormal_dist_calc(KEY_VALUE["daily_energy_consumtion"]["mean"], KEY_VALUE["daily_energy_consumtion"]["sigma"])
    daily_working_hours = normal_distr_calc(KEY_VALUE["daily_working_hours"]["avg"], KEY_VALUE["daily_working_hours"]["stdev"])
    material_price = normal_distr_calc(KEY_VALUE["material_price"]["avg"], KEY_VALUE["material_price"]["stdev"])
    daily_expenses = gamma_distr_calc(KEY_VALUE["daily_expenses"]["shape"], KEY_VALUE["daily_expenses"]["scale"]) + 50000
    daily_earnings = np.round((material_price * daily_extracted_ammount_raw * copper_content) - daily_expenses, TRUNKED_DECIMAL)
    temperature = normal_distr_calc(KEY_VALUE["temperature"]["avg"], KEY_VALUE["temperature"]["stdev"])
    strike_days = poisson_distr_calc(KEY_VALUE["strike_days"]["avg"])
    machine_breakdowns = poisson_distr_calc(KEY_VALUE["machine_breakdowns"]["avg"])
    
    dataset_dataframe = pd.DataFrame(
        {
            "Mining depth (m)": mining_depth,
            "Daily extracted ammount raw (tons)": daily_extracted_ammount_raw,
            "Copper content in raw material (%)": copper_content,
            "Daily energetic consumtion (MW/h)": daily_energy_consumtion,
            "Working hours": daily_working_hours,
            "Copper price ($)": material_price,
            "Daily expenses ($)": daily_expenses,
            "Estimated daily earnings ($)": daily_earnings,
            "Temperature (C°)": temperature,
            "Workers Strikes": strike_days,
            "Machine breakdowns": machine_breakdowns
        }
    )
    dataset_dataframe.to_csv(DATASET_PATH, index = False)
    
if generate_dataset() is not False:
    print(f"Dataset generato correttamente in posizione: {DATASET_PATH}")
