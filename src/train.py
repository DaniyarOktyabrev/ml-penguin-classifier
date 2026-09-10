import sys
import os
# Добавляем корневую папку проекта в путь поиска модулей
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import configparser
import pickle
from src.data_loader import load_data, preprocess_features
from sklearn.ensemble import RandomForestClassifier

def train():
    config = configparser.ConfigParser()
    config.read('config.ini')
    n_estimators = config.getint('model', 'n_estimators')
    max_depth = config.getint('model', 'max_depth')
    
    df = load_data('data/raw/penguins.csv')
    X, y, le_target, scaler, le_sex, le_island = preprocess_features(df)
    
    model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=42)
    model.fit(X, y)
    
    # Сохраняем всё необходимое
    with open('models/model.pkl', 'wb') as f:
        pickle.dump({
            'model': model,
            'le_target': le_target,
            'scaler': scaler,
            'le_sex': le_sex,
            'le_island': le_island
        }, f)
    
    print("Model trained and saved.")

if __name__ == '__main__':
    train()