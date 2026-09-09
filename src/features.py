import pandas as pd
import pickle

def transform_input(raw_input, scaler, le_sex, le_island):
    # raw_input – словарь с ключами: island, bill_length_mm, ...
    df = pd.DataFrame([raw_input])
    df['sex'] = le_sex.transform([df['sex'].iloc[0]])[0]
    df['island'] = le_island.transform([df['island'].iloc[0]])[0]
    num_cols = ['bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g']
    df[num_cols] = scaler.transform(df[num_cols])
    return df[['island', 'bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g', 'sex']]