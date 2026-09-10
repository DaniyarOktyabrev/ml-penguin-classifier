import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler

def load_data(filepath):
    df = pd.read_csv(filepath)
    # Переименовываем culmen в bill для совместимости с остальным кодом
    df = df.rename(columns={
        'culmen_length_mm': 'bill_length_mm',
        'culmen_depth_mm': 'bill_depth_mm'
    })
    # Удаляем строки с пропущенными значениями (NA)
    df = df.dropna()
    return df

def preprocess_features(df):
    # Кодируем категориальные признаки (имена теперь bill_...)
    le_sex = LabelEncoder()
    le_island = LabelEncoder()
    df['sex'] = le_sex.fit_transform(df['sex'])
    df['island'] = le_island.fit_transform(df['island'])
    
    # Целевая переменная
    target = df['species']
    le_target = LabelEncoder()
    y = le_target.fit_transform(target)
    
    # Признаки – используем новые имена (после переименования они bill_...)
    feature_cols = ['island', 'bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g', 'sex']
    X = df[feature_cols].copy()
    
    # Масштабируем числовые (теперь bill_...)
    num_cols = ['bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g']
    scaler = StandardScaler()
    X[num_cols] = scaler.fit_transform(X[num_cols])
    
    return X, y, le_target, scaler, le_sex, le_island