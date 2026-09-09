import pickle
from src.features import transform_input

class Predictor:
    def __init__(self):
        with open('models/model.pkl', 'rb') as f:
            self.artifacts = pickle.load(f)
        self.model = self.artifacts['model']
        self.le_target = self.artifacts['le_target']
        self.scaler = self.artifacts['scaler']
        self.le_sex = self.artifacts['le_sex']
        self.le_island = self.artifacts['le_island']

    def predict(self, input_data):
        X = transform_input(input_data, self.scaler, self.le_sex, self.le_island)
        pred = self.model.predict(X)[0]
        species = self.le_target.inverse_transform([pred])[0]
        return species